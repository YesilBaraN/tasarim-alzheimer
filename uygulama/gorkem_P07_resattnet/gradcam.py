# -*- coding: utf-8 -*-
"""
P07 — Zhang vd. 2021: 3B Grad-CAM (Gradient-weighted Class Activation Mapping).

Makale Yöntemi (§III-C):
  - 3B Evrişimli katmanların (özellikle layer3 veya layer4) özellik haritaları ve
    hedef sınıf skoruna göre gradyanları kullanılarak 3B aktivasyon haritası üretilir.
  - Ağırlık hesabı: alpha_k^c = (1 / Z) * sum_{d,h,w} (d y^c / d A_{d,h,w}^k)
  - Birleştirme: L_{Grad-CAM}^c = ReLU( sum_k alpha_k^c * A^k )
  - 3B Trilinear enterpolasyon ile orijinal girdi boyutuna (128³) ölçeklenir.

Kullanım:
  from uygulama.gorkem_P07_resattnet.gradcam import acikla, gorsellestir
  harita = acikla(model, hacim_tensor, hedef_sinif=1, katman="layer3")
  gorsellestir(hacim_np, harita, "rapor/sekiller/gradcam_ornek.png")
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class GradCAM3D:
    """3B Evrişimli Ağlar için Sınıf Aktivasyon Haritalama (Grad-CAM)."""

    def __init__(self, model: nn.Module, hedef_katman: nn.Module):
        self.model = model
        self.hedef_katman = hedef_katman
        self.aktivasyonlar: Optional[torch.Tensor] = None
        self.gradyanlar: Optional[torch.Tensor] = None

        self._kancalari_kaydet()

    def _kancalari_kaydet(self):
        def forward_kanca(module, input, output):
            self.aktivasyonlar = output.detach()

        def backward_kanca(module, grad_in, grad_out):
            self.gradyanlar = grad_out[0].detach()

        self.hedef_katman.register_forward_hook(forward_kanca)
        self.hedef_katman.register_full_backward_hook(backward_kanca)

    def harita_uret(
        self,
        x: torch.Tensor,
        hedef_sinif: int = 1,
    ) -> torch.Tensor:
        """Verilen girdi için 3B Grad-CAM ısı haritası üretir."""
        self.model.eval()
        self.model.zero_grad()

        # İleri geçiş
        cikis = self.model(x)  # (b, num_classes)
        skor = cikis[:, hedef_sinif].sum()

        # Geri geçiş (gradyan yakalama)
        skor.backward(retain_graph=True)

        if self.gradyanlar is None or self.aktivasyonlar is None:
            raise RuntimeError("Grad-CAM kancaları aktivasyon veya gradyan yakalayamadı.")

        # Kanallar üzerinde küresel ortalama gradyan (Global Average Pooling): alpha_k
        alpha = torch.mean(self.gradyanlar, dim=(2, 3, 4), keepdim=True)  # (b, c, 1, 1, 1)

        # Ağırlıklı kombinasyon ve ReLU
        cam = torch.sum(alpha * self.aktivasyonlar, dim=1, keepdim=True)  # (b, 1, d, h, w)
        cam = F.relu(cam)

        # Orijinal girdi boyutuna trilinear enterpolasyon ile büyütme
        girdi_boyut = x.shape[2:]
        cam_upsampled = F.interpolate(
            cam,
            size=girdi_boyut,
            mode="trilinear",
            align_corners=False,
        )

        # [0, 1] aralığına normalize et
        b_min = cam_upsampled.amin(dim=(2, 3, 4), keepdim=True)
        b_max = cam_upsampled.amax(dim=(2, 3, 4), keepdim=True)
        cam_norm = (cam_upsampled - b_min) / (b_max - b_min + 1e-8)
        return cam_norm


def acikla(
    model: nn.Module,
    hacim: Union[torch.Tensor, np.ndarray],
    hedef_sinif: int = 1,
    katman_adi: str = "layer3",
    cihaz: str = "cpu",
) -> np.ndarray:
    """
    3D ResAttNet modeli için Grad-CAM haritası üretir.

    Parametreler:
      model: ResAttNet3D örneği
      hacim: 3B (D, H, W) veya 5B (1, 1, D, H, W) tensör/dizi
      hedef_sinif: Hedef sınıf indeksi (1: AD)
      katman_adi: Hedef öznitelik katmanı ('layer3' veya 'layer4')
      cihaz: 'cpu' veya 'cuda'
    """
    dev = torch.device(cihaz)
    model.to(dev)

    if isinstance(hacim, np.ndarray):
        x = torch.from_numpy(hacim).float()
    else:
        x = hacim.clone().float()

    if x.ndim == 3:
        x = x.unsqueeze(0).unsqueeze(0)
    elif x.ndim == 4:
        x = x.unsqueeze(0)
    x = x.to(dev)

    # Hedef katmanı bul
    if hasattr(model, katman_adi):
        hedef_katman = getattr(model, katman_adi)
    else:
        # Alternatif: son evrişim bloğu
        hedef_katman = model.layer4

    cam_modulu = GradCAM3D(model, hedef_katman)
    cam_tensor = cam_modulu.harita_uret(x, hedef_sinif=hedef_sinif)
    cam_np = cam_tensor[0, 0].detach().cpu().numpy()
    return cam_np.astype(np.float32)


def gorsellestir(
    hacim: np.ndarray,
    ilgi_haritasi: np.ndarray,
    cikti_png: Union[str, Path],
    baslik: Optional[str] = "P07 Zhang 2021 — 3B ResAttNet Grad-CAM",
    esik: float = 0.20,
) -> Path:
    """
    3B MRI hacmi ile Grad-CAM ilgi haritasını 3 ana düzlemde (Aksiyel, Koronal, Sagital)
    üst üste bindirerek kaydeder.
    """
    cikti_yolu = Path(cikti_png)
    cikti_yolu.parent.mkdir(parents=True, exist_ok=True)

    if hacim.ndim == 5:
        hacim = hacim[0, 0]
    elif hacim.ndim == 4:
        hacim = hacim[0]

    d, h, w = hacim.shape
    c_d, c_h, c_w = d // 2, h // 2, w // 2

    maskeli_ilgi = np.copy(ilgi_haritasi)
    maskeli_ilgi[maskeli_ilgi < esik] = np.nan

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    # 1. Aksiyel
    axes[0].imshow(np.rot90(hacim[c_d, :, :]), cmap="gray")
    im0 = axes[0].imshow(np.rot90(maskeli_ilgi[c_d, :, :]), cmap="jet", alpha=0.5, vmin=0, vmax=1)
    axes[0].set_title(f"Aksiyel (Z = {c_d})")
    axes[0].axis("off")

    # 2. Koronal
    axes[1].imshow(np.rot90(hacim[:, c_h, :]), cmap="gray")
    axes[1].imshow(np.rot90(maskeli_ilgi[:, c_h, :]), cmap="jet", alpha=0.5, vmin=0, vmax=1)
    axes[1].set_title(f"Koronal (Y = {c_h})")
    axes[1].axis("off")

    # 3. Sagital
    axes[2].imshow(np.rot90(hacim[:, :, c_w]), cmap="gray")
    axes[2].imshow(np.rot90(maskeli_ilgi[:, :, c_w]), cmap="jet", alpha=0.5, vmin=0, vmax=1)
    axes[2].set_title(f"Sagital (X = {c_w})")
    axes[2].axis("off")

    if baslik:
        fig.suptitle(baslik, fontsize=13, fontweight="bold", y=1.02)

    cbar = fig.colorbar(im0, ax=axes.ravel().tolist(), orientation="horizontal", fraction=0.04, pad=0.08)
    cbar.set_label("3B Grad-CAM Aktivasyon Yoğunluğu", fontsize=10)

    plt.tight_layout()
    plt.savefig(cikti_yolu, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return cikti_yolu


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P07 Grad-CAM Harita Üretici")
    parser.add_argument("--hacim", type=str, default="", help="Girdi .npy hacim yolu")
    parser.add_argument("--cikti", type=str, default="gradcam_ornek.png", help="Çıktı PNG yolu")
    parser.add_argument("--boyut", type=int, default=128, help="Küp boyutu (32 veya 128)")
    parser.add_argument("--katman", type=str, default="layer3", help="Hedef katman (layer3/layer4)")
    args = parser.parse_args()

    from uygulama.gorkem_P07_resattnet.model import olustur

    model = olustur("resatt18", sinif_sayisi=2, girdi_boyut=args.boyut)

    if args.hacim and Path(args.hacim).exists():
        hacim = np.load(args.hacim)
    else:
        print(f"Rastgele sentetik {args.boyut}³ hacim oluşturuluyor...")
        hacim = np.random.randn(args.boyut, args.boyut, args.boyut).astype(np.float32)

    harita = acikla(model, hacim, hedef_sinif=1, katman_adi=args.katman)
    cikti = gorsellestir(hacim, harita, args.cikti)
    print(f"Grad-CAM haritası başarıyla kaydedildi: {cikti}")
