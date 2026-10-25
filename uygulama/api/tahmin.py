# -*- coding: utf-8 -*-
r"""
tahmin.py — Karar destek prototipinin çıkarım katmanı: NIfTI/DICOM → ön işleme → ONNX → sınıf + olasılık.

ARAŞTIRMA PROTOTİPİDİR. Tanı aracı değildir, tıbbi karar için kullanılamaz; çıktı bir uzmanın
değerlendirmesine girdi olacak bir skordur. Her çıktıda bu uyarı `uyari` alanında taşınır.

Tasarım kuralı — **eğitim/servis uyumu:** çıkarım, eğitimdeki ön işlemenin AYNISINI kullanır
(`onisleme/onisle.py` fonksiyonları: kafatası ayıklama → N4 → maske içi z-score → MNI152 afin → boyut³).
Ayrı bir "servis ön işlemesi" yazılmaz; yazılırsa modelin gördüğü dağılım kayar ve skor anlamsızlaşır.
Modelin hangi boyutla eğitildiği ONNX girdi şeklinden okunur ve ön işleme ona göre ayarlanır.

Kullanım:
  # tek hacim, baştan sona (ön işleme dahil)
  python uygulama\api\tahmin.py --onnx model.onnx --girdi D:\hasta\T1.nii.gz
  # zaten onisle.py'den geçmiş .npy
  python uygulama\api\tahmin.py --onnx model.onnx --npy D:\veri\islenmis\RID123.npy
  # ön işleme adımlarını kıs (hızlı deneme; HD-BET ve MNI kaydı atlanır)
  python uygulama\api\tahmin.py --onnx model.onnx --girdi T1.nii.gz --kafatasi yok --kayit yok

Python'dan (web arayüzü / radyoloji eklentisi bunu çağırır):
  from uygulama.api.tahmin import KararDestek
  kd = KararDestek("model.onnx", sinif_adlari=("NC", "AD"))
  sonuc = kd.tahmin_nii("T1.nii.gz")      # {"sinif": "AD", "olasiliklar": {...}, ...}
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

# Windows konsolu Türkçe kod sayfasında (cp1254) açılır; '→', '±', '≈', '≥', '█' gibi karakterler
# UnicodeEncodeError atıp betiği çökertir. Konsolun kendi kodlamasını koruyup kodlanamayan karakteri
# '?' ile değiştiriyoruz (Türkçe harfler doğru görünmeye devam eder). UTF-8 konsolda hiçbir şey değişmez.
for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:  # eski Python, yönlendirilmiş akış ya da reconfigure'ü olmayan sarmalayıcı
        pass

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(KOK / "onisleme"))

UYARI = ("Araştırma prototipi — tanı aracı değildir. Çıktı, uzman değerlendirmesine girdi olan bir "
         "model skorudur; klinik karar için tek başına kullanılamaz.")

SINIF_ADLARI = {2: ("NC", "AD"), 3: ("NC", "MCI", "AD")}


class KararDestek:
    """Eğitilmiş ONNX modelini yükler, hacim verilip sınıf olasılıkları döndürür."""

    def __init__(self, onnx_yolu: str | Path, sinif_adlari: tuple[str, ...] | None = None,
                 saglayicilar: list[str] | None = None):
        import onnxruntime as ort

        self.yol = str(onnx_yolu)
        self.oturum = ort.InferenceSession(self.yol, providers=saglayicilar or ["CPUExecutionProvider"])
        girdi = self.oturum.get_inputs()[0]
        self.girdi_adi = girdi.name
        sekil = [s if isinstance(s, int) else None for s in girdi.shape]
        if len(sekil) != 5 or sekil[2] is None:
            raise ValueError(f"beklenen girdi şekli [1,1,B,B,B]; gelen {girdi.shape}. "
                             f"onnx_disa_aktar.py sabit boyutla dışa aktarır (dynamic_axes yok).")
        self.boyut = int(sekil[2])
        cikti = self.oturum.get_outputs()[0]
        self.sinif_sayisi = int(cikti.shape[-1]) if isinstance(cikti.shape[-1], int) else 2
        self.sinif_adlari = tuple(sinif_adlari or SINIF_ADLARI.get(self.sinif_sayisi,
                                  tuple(f"sinif{i}" for i in range(self.sinif_sayisi))))
        if len(self.sinif_adlari) != self.sinif_sayisi:
            raise ValueError(f"{self.sinif_sayisi} sınıflı model için {len(self.sinif_adlari)} ad verildi")

    # ------------------------------------------------------------------ çıkarım
    def tahmin_dizi(self, arr: np.ndarray) -> dict:
        """arr: [B,B,B] (eğitimdeki ön işlemeden geçmiş, z-score'lu) → tahmin sözlüğü."""
        arr = np.asarray(arr, dtype=np.float32)
        if arr.shape != (self.boyut,) * 3:
            raise ValueError(f"model {self.boyut}³ bekliyor, gelen {arr.shape}. Ön işlemeyi --boyut "
                             f"{self.boyut} ile koş ya da tahmin_nii kullan (otomatik ayarlar).")
        t0 = time.time()
        logit = self.oturum.run(None, {self.girdi_adi: arr[None, None]})[0][0].astype(np.float64)
        e = np.exp(logit - logit.max())
        p = e / e.sum()
        i = int(p.argmax())
        return {
            "sinif": self.sinif_adlari[i],
            "sinif_no": i,
            "guven": float(p[i]),
            "olasiliklar": {ad: float(v) for ad, v in zip(self.sinif_adlari, p)},
            "logit": [float(v) for v in logit],
            "model": self.yol,
            "boyut": self.boyut,
            "cikarim_sn": round(time.time() - t0, 3),
            "uyari": UYARI,
        }

    def tahmin_npy(self, npy_yolu: str | Path) -> dict:
        """onisle.py çıktısı .npy (float16) — eğitimdekiyle birebir aynı ön işleme varsayılır."""
        arr = np.load(npy_yolu).astype(np.float32)
        s = self.tahmin_dizi(arr)
        s["girdi"] = str(npy_yolu)
        s["onisleme"] = "hazır .npy (onisle.py çıktısı varsayıldı)"
        return s

    def tahmin_nii(self, girdi: str | Path, kafatasi: str = "hdbet", kayit: str = "sitk",
                   cihaz: str = "cpu", gecici_klasor: str | Path | None = None) -> dict:
        """Ham NIfTI / Analyze / DICOM klasörü → eğitimdeki ön işleme → tahmin."""
        import tempfile

        import onisle

        gecici = Path(gecici_klasor) if gecici_klasor else Path(tempfile.mkdtemp(prefix="tahmin_"))
        meta = onisle.hacmi_isle(Path(girdi), gecici, "vaka", boyut=self.boyut, kafatasi=kafatasi,
                                 kayit=kayit, cihaz=cihaz)
        s = self.tahmin_npy(gecici / "vaka.npy")
        s["girdi"] = str(girdi)
        s["onisleme"] = {"adimlar": meta["adimlar"], "uyarilar": meta["uyarilar"],
                         "sureler_sn": meta.get("sureler_sn", {}), "toplam_sn": meta.get("toplam_sn")}
        if meta["uyarilar"]:
            s["uyari"] = UYARI + f" Ön işleme uyarıları: {meta['uyarilar']} — skora dikkatle bak."
        return s


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--onnx", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--girdi", help="ham NIfTI / Analyze / DICOM klasörü (ön işleme uygulanır)")
    g.add_argument("--npy", help="onisle.py'den geçmiş .npy")
    p.add_argument("--siniflar", nargs="*", default=None, help="sınıf adları (ör. NC AD)")
    p.add_argument("--kafatasi", choices=["hdbet", "yok"], default="hdbet")
    p.add_argument("--kayit", choices=["sitk", "ants", "yok"], default="sitk")
    p.add_argument("--cihaz", default="cpu", help="HD-BET cihazı")
    p.add_argument("--json", action="store_true", help="yalnız JSON bas (arayüz/boru hattı için)")
    a = p.parse_args(argv)

    kd = KararDestek(a.onnx, tuple(a.siniflar) if a.siniflar else None)
    sonuc = kd.tahmin_npy(a.npy) if a.npy else kd.tahmin_nii(a.girdi, a.kafatasi, a.kayit, a.cihaz)

    if a.json:
        print(json.dumps(sonuc, ensure_ascii=False, indent=1))
        return
    print(f"\nModel : {Path(sonuc['model']).name}  ({sonuc['boyut']}³, {len(sonuc['olasiliklar'])} sınıf)")
    print(f"Girdi : {sonuc.get('girdi', '-')}")
    print(f"\n  TAHMİN: {sonuc['sinif']}   (güven {sonuc['guven']:.1%}, çıkarım {sonuc['cikarim_sn']} sn)")
    for ad, v in sorted(sonuc["olasiliklar"].items(), key=lambda t: -t[1]):
        print(f"    {ad:>5}  {v:6.1%}  {'#' * int(round(v * 40))}")
    if isinstance(sonuc.get("onisleme"), dict) and sonuc["onisleme"].get("uyarilar"):
        print(f"\n  ön işleme uyarıları: {sonuc['onisleme']['uyarilar']}")
    print(f"\n! {sonuc['uyari']}\n")


if __name__ == "__main__":
    main()
