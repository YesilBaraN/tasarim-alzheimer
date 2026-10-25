# -*- coding: utf-8 -*-
"""
veri.py — Tek Dataset sınıfı: herkes aynı girdiyi aynı biçimde görür (PROTOKOL madde 3).

Girdi: onisle.py çıktısı `.npy` (float16, boyut³) + bölme CSV (denek_id, dosya, sinif[, yas, cinsiyet, bolum]).
Görev: 'ikili' → yalnız sinif ∈ {0 (NC), 2 (AD)} satırları, etiket 0/1 ; 'uc' → 0/1/2.
Artırma (yalnız egitim=True): sol-sağ çevirme, küçük rastgele afin (MONAI varsa), yoğunluk kaydırma/ölçek.
Rastgelelik: artırma RNG'si her DataLoader işçisinde `torch.initial_seed()`ten türetilir (işçiler aynı diziyi
üretmesin, dizi her epoch değişsin) ve MONAI RandAffine `set_random_state` ile tohumlanır — PROTOKOL madde 10.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset

SINIF_AD = {0: "NC", 1: "MCI", 2: "AD"}


def gorev_filtrele(df: pd.DataFrame, gorev: str) -> pd.DataFrame:
    df = df.copy()
    if gorev == "ikili":
        df = df[df["sinif"].isin([0, 2])].copy()
        df["etiket"] = (df["sinif"] == 2).astype(int)
    elif gorev == "uc":
        df["etiket"] = df["sinif"].astype(int)
    else:
        raise ValueError("gorev: ikili | uc")
    return df.reset_index(drop=True)


def sinif_sayisi(gorev: str) -> int:
    return 2 if gorev == "ikili" else 3


class HacimVeriSeti(Dataset):
    def __init__(self, df: pd.DataFrame, veri_kok: str | Path, gorev: str = "ikili", egitim: bool = False,
                 boyut: int | None = None, tohum: int = 2026, cevir: bool = True):
        self.df = gorev_filtrele(df, gorev)
        self.kok = Path(veri_kok)
        self.egitim = egitim
        self.boyut = boyut
        self.cevir = cevir  # sol-sağ çevirme; PROTOKOL: artırma kümesi herkeste aynı (varsayılan açık, ablation'da kapatılabilir)
        self.tohum = int(tohum)
        self._rng_onbellek = None  # işçi başına tembel kurulur (bkz. _rastgele)
        self._afin = None
        if egitim:
            try:
                from monai.transforms import RandAffine
                self._afin = RandAffine(prob=0.5, rotate_range=(0.1, 0.1, 0.1), scale_range=(0.05, 0.05, 0.05),
                                        translate_range=(4, 4, 4), padding_mode="zeros", mode="bilinear")
                self._afin.set_random_state(seed=self.tohum)  # MONAI'nin kendi RNG'si de tohuma bağlanır
            except Exception:
                self._afin = None  # MONAI yoksa yalnız çevirme + yoğunluk artırması

    def _rastgele(self) -> np.random.Generator:
        """İşçi başına ayrı RNG; torch.initial_seed() her işçide ve her epoch'ta farklı ama tohuma bağlı."""
        if self._rng_onbellek is None:
            self._rng_onbellek = np.random.default_rng((torch.initial_seed() + self.tohum) % 2**32)
        return self._rng_onbellek

    def __len__(self):
        return len(self.df)

    def etiketler(self) -> np.ndarray:
        return self.df["etiket"].to_numpy()

    def sinif_agirliklari(self) -> torch.Tensor:
        """Dengesizlik için ters frekans ağırlığı (CE loss'a verilir)."""
        say = np.bincount(self.etiketler(), minlength=int(self.etiketler().max()) + 1).astype(np.float32)
        w = say.sum() / (len(say) * np.maximum(say, 1))
        return torch.tensor(w, dtype=torch.float32)

    def _yukle(self, dosya: str) -> np.ndarray:
        yol = Path(dosya)
        if not yol.is_absolute():
            yol = self.kok / yol
        arr = np.load(yol).astype(np.float32)
        if self.boyut and arr.shape != (self.boyut,) * 3:
            arr = _yeniden_boyutlandir(arr, self.boyut)
        return arr

    def __getitem__(self, i):
        satir = self.df.iloc[i]
        arr = self._yukle(satir["dosya"])
        if self.egitim:
            rng = self._rastgele()
            if self.cevir and rng.random() < 0.5:
                arr = arr[:, :, ::-1].copy()  # sol-sağ (x ekseni) çevirme — LPS dizilişinde son eksen L-R
            olcek = 1.0 + rng.normal(0, 0.05)
            kayma = rng.normal(0, 0.05)
            arr = arr * olcek + kayma
        x = torch.from_numpy(arr)[None]  # [1, D, H, W]
        if self.egitim and self._afin is not None:
            x = torch.as_tensor(self._afin(x))
        return x.float(), int(satir["etiket"]), str(satir["denek_id"])


def _yeniden_boyutlandir(arr: np.ndarray, boyut: int) -> np.ndarray:
    t = torch.from_numpy(arr)[None, None]
    t = torch.nn.functional.interpolate(t, size=(boyut,) * 3, mode="trilinear", align_corners=False)
    return t[0, 0].numpy()


def _isci_baslat(isci_id: int):
    """Her DataLoader işçisine kendi artırma RNG'sini verir; aksi hâlde işçiler aynı diziyi üretir."""
    bilgi = torch.utils.data.get_worker_info()
    if bilgi is None:
        return
    ds = bilgi.dataset
    t = (torch.initial_seed() + isci_id) % 2**32
    ds._rng_onbellek = np.random.default_rng(t)
    if getattr(ds, "_afin", None) is not None:
        ds._afin.set_random_state(seed=int(t % 2**31))


def yukleyici(df: pd.DataFrame, veri_kok, gorev: str, egitim: bool, batch: int = 4, isci: int = 2,
              boyut: int | None = None, tohum: int = 2026) -> DataLoader:
    ds = HacimVeriSeti(df, veri_kok, gorev, egitim, boyut, tohum)
    g = torch.Generator(); g.manual_seed(tohum)
    return DataLoader(ds, batch_size=batch, shuffle=egitim, num_workers=isci, pin_memory=True,
                      drop_last=False, generator=g, worker_init_fn=_isci_baslat if isci > 0 else None)


def kat_oku(bolme_klasor, set_adi: str, kat: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """veri/bolme/<set>_kat{k}.csv → (egitim_df, dogrulama_df)."""
    df = pd.read_csv(Path(bolme_klasor) / f"{set_adi}_kat{kat}.csv")
    return df[df["bolum"] == "egitim"].reset_index(drop=True), df[df["bolum"] == "dogrulama"].reset_index(drop=True)


def test_oku(bolme_klasor, set_adi: str) -> pd.DataFrame:
    return pd.read_csv(Path(bolme_klasor) / f"{set_adi}_test.csv")
