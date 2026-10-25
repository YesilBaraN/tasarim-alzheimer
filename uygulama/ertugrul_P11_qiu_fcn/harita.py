# -*- coding: utf-8 -*-
"""
P11 — Qiu 2020: 3B Hastalık Olasılık Haritası (Disease Probability Map, DPM) Üreteci.
Tam hacimli 3B sMRI tensörü üzerinde FCN'in tam evrişimli formunu koşturarak
voksel bazlı Alzheimer risk haritası üretir ve 3 dik düzlemde görselleştirir.

Kullanım (CLI):
  python uygulama/ertugrul_P11_qiu_fcn/harita.py --girdi ornek.npy --cikti dpm_harita.png
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple, Dict, Any

import numpy as np
import torch
import torch.nn.functional as F

from uygulama.ertugrul_P11_qiu_fcn.model import olustur


def dpm_uret(
    model: torch.nn.Module,
    giris_tensör: torch.Tensor,
    hedef_sinif: int = 1,
    hedef_boyut: Tuple[int, int, int] = (128, 128, 128),
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Modelden tam hacimli 3B hastalık olasılık haritası üretir.

    Args:
        model: Eğitilmiş QiuFCN3D modeli
        giris_tensör: (1, 1, D, H, W) boyutlu tensör
        hedef_sinif: 1 (AD sınıfı)
        hedef_boyut: (D, H, W) hedef enterpolasyon boyutu

    Returns:
        dpm_3b: (D, H, W) numpy olasılık dizisi [0, 1]
        istatistik: en yüksek risk noktası, tepe olasılık, ortalama risk
    """
    model.eval()
    with torch.no_grad():
        fcn_conv = model.dense_to_conv()
        fcn_conv.eval()
        logits = fcn_conv(giris_tensör)
        probs = torch.softmax(logits, dim=1)
        
        # Hedef sınıf olasılık haritasını seç (B, 1, D', H', W')
        ad_prob = probs[:, hedef_sinif : hedef_sinif + 1, :, :, :]
        
        # Orijinal MRI boyutuna trilinear enterpolasyonla büyüt
        dpm_upsampled = F.interpolate(
            ad_prob,
            size=hedef_boyut,
            mode="trilinear",
            align_corners=False,
        )
        dpm_3b = dpm_upsampled.squeeze().cpu().numpy()

    # İstatistikler
    tepe_deger = float(np.max(dpm_3b))
    ortalama_deger = float(np.mean(dpm_3b))
    tepe_koordinat = np.unravel_index(np.argmax(dpm_3b), dpm_3b.shape)

    istatistik = {
        "tepe_risk": tepe_deger,
        "ortalama_risk": ortalama_deger,
        "tepe_koordinat": [int(c) for c in tepe_koordinat],
    }
    return dpm_3b, istatistik


def gorsellestir_3_duzlem(
    mri_hacim: np.ndarray,
    dpm_harita: np.ndarray,
    kayit_yolu: Path | str,
    kesit_merkezi: Tuple[int, int, int] | None = None,
    alfa: float = 0.45,
):
    """
    MRI ve DPM risk haritasını Aksiyel, Koronal ve Sagital düzlemlerde çizer.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    D, H, W = mri_hacim.shape
    if kesit_merkezi is None:
        cz, cy, cx = D // 2, H // 2, W // 2
    else:
        cz, cy, cx = kesit_merkezi

    # Kesitler
    kesitler_mri = [
        ("Aksiyel (Z)", mri_hacim[cz, :, :]),
        ("Koronal (Y)", mri_hacim[:, cy, :]),
        ("Sagital (X)", mri_hacim[:, :, cx]),
    ]
    kesitler_dpm = [
        dpm_harita[cz, :, :],
        dpm_harita[:, cy, :],
        dpm_harita[:, :, cx],
    ]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#1A202C")

    for ax, (ad, mri_sl), dpm_sl in zip(axes, kesitler_mri, kesitler_dpm):
        ax.set_facecolor("#1A202C")
        ax.imshow(np.rot90(mri_sl), cmap="gray", aspect="equal")
        
        # DPM ısı haritası maskeleme (yalnızca risk > 0.3 olan vokseller)
        dpm_mask = np.rot90(dpm_sl)
        dpm_plot = np.ma.masked_where(dpm_mask < 0.25, dpm_mask)
        im = ax.imshow(dpm_plot, cmap="hot", alpha=alfa, vmin=0.0, vmax=1.0, aspect="equal")
        
        ax.set_title(ad, color="white", fontsize=12, pad=8)
        ax.axis("off")

    cbar = fig.colorbar(im, ax=axes.ravel().tolist(), orientation="vertical", shrink=0.7, pad=0.02)
    cbar.set_label("Hastalık Riski P(AD)", color="white", fontsize=10)
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")

    plt.suptitle("P11 — Qiu 2020: 3B Hastalık Olasılık Haritası (DPM)", color="white", fontsize=14, y=0.98)
    Path(kayit_yolu).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(kayit_yolu, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="P11 3B FCN Hastalık Olasılık Haritası Üreteci")
    parser.add_argument("--girdi", type=str, default="", help="Girdi .npy dosya yolu")
    parser.add_argument("--cikti", type=str, default="dpm_cikis.png", help="Çıktı görseli yolu")
    parser.add_argument("--boyut", type=int, default=128, help="Hacim boyutu (varsayılan: 128)")
    args = parser.parse_args()

    # Duman testi veya gerçek veri
    if args.girdi and Path(args.girdi).exists():
        hacim = np.load(args.girdi)
        if hacim.ndim == 4:
            hacim = hacim[0]
    else:
        print("Uyarı: Girdi dosyası verilmedi, sentetik 128³ hacimle test ediliyor...")
        rng = np.random.default_rng(2026)
        hacim = rng.normal(0.5, 0.2, (args.boyut, args.boyut, args.boyut)).astype(np.float32)

    model = olustur(varyant="fcn", sinif_sayisi=2, girdi_boyut=args.boyut)
    t = torch.from_numpy(hacim).unsqueeze(0).unsqueeze(0).float()

    print("DPM hesaplanıyor...")
    dpm_harita, stats = dpm_uret(model, t, hedef_sinif=1, hedef_boyut=hacim.shape)
    print(f"Tepe risk: {stats['tepe_risk']:.3f}, Ortalama risk: {stats['ortalama_risk']:.3f}, Merkez: {stats['tepe_koordinat']}")

    gorsellestir_3_duzlem(hacim, dpm_harita, args.cikti, kesit_merkezi=tuple(stats["tepe_koordinat"]))
    print(f"Görselleştirme kaydedildi: {args.cikti}")


if __name__ == "__main__":
    main()
