# -*- coding: utf-8 -*-
"""
P06 — Böhle vd. 2019: Katman Bazlı İlgi Yayılımı (Layer-wise Relevance Propagation, LRP).

Makale Formülasyonu:
  - LRP beta-kuralı (beta=0, alpha=1): Yalnızca hedef sınıfı pozitif yönde destekleyen
    aktivasyonları geri yayar; inhibitör zıt işaretli ağırlıkları eler.
  - Formül: R_j = sum_k ( (a_j * w_jk^+) / (sum_j a_j * w_jk^+ + epsilon) ) * R_k
  - Montavon vd. ve Kohlbrenner vd. 2020 tarafından önerilen kararlı PyTorch
    otomatik türev (autograd) ters yayılım yaklaşımı kullanılır.

Kullanım:
  from uygulama.gorkem_P06_bohle.lrp import acikla, gorsellestir
  harita = acikla(model, hacim_tensor, hedef_sinif=1)
  gorsellestir(hacim_np, harita, "rapor/sekiller/lrp_ornek.png")
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def lrp_linear_katman(
    layer: nn.Linear,
    x: torch.Tensor,
    r_cikis: torch.Tensor,
    eps: float = 1e-9,
) -> torch.Tensor:
    """Tam bağlantılı katman için LRP alpha=1, beta=0 ters yayılımı."""
    w_pos = torch.clamp(layer.weight, min=0.0)
    x_det = x.detach().requires_grad_(True)
    z = F.linear(x_det, w_pos, None) + eps
    s = r_cikis / z
    (z * s.detach()).sum().backward()
    return (x_det * x_det.grad).detach()


def lrp_conv3d_katman(
    conv: nn.Conv3d,
    x: torch.Tensor,
    r_cikis: torch.Tensor,
    eps: float = 1e-9,
) -> torch.Tensor:
    """3B Evrişim katmanı için LRP alpha=1, beta=0 ters yayılımı."""
    w_pos = torch.clamp(conv.weight, min=0.0)
    x_det = x.detach().requires_grad_(True)
    z = (
        F.conv3d(
            x_det,
            w_pos,
            bias=None,
            stride=conv.stride,
            padding=conv.padding,
            dilation=conv.dilation,
            groups=conv.groups,
        )
        + eps
    )
    s = r_cikis / z
    (z * s.detach()).sum().backward()
    return (x_det * x_det.grad).detach()


def lrp_maxpool3d_katman(
    pool: nn.MaxPool3d,
    x: torch.Tensor,
    r_cikis: torch.Tensor,
    eps: float = 1e-9,
) -> torch.Tensor:
    """3B Maksimum Havuzlama katmanı için LRP ters yayılımı (kazanan voksellere aktarır)."""
    x_det = x.detach().requires_grad_(True)
    z, indices = F.max_pool3d(
        x_det,
        kernel_size=pool.kernel_size,
        stride=pool.stride,
        padding=pool.padding,
        return_indices=True,
    )
    z = z + eps
    s = r_cikis / z
    (z * s.detach()).sum().backward()
    return (x_det * x_det.grad).detach()


def acikla(
    model: nn.Module,
    hacim: Union[torch.Tensor, np.ndarray],
    hedef_sinif: int = 1,
    cihaz: str = "cpu",
    eps: float = 1e-9,
) -> np.ndarray:
    """
    Böhle 3D CNN modeli için LRP (beta=0) ilgi haritası üretir.

    Parametreler:
      model: Eğitilmiş BohleCNN3D modeli
      hacim: 3B veya 5B MRI tensörü/dizisi (D, H, W) veya (1, 1, D, H, W)
      hedef_sinif: İlgi üretilecek sınıf (1: AD / Pozitif)
      cihaz: 'cpu' veya 'cuda'
    Dönüş:
      (D, H, W) boyutlu normalize pozitif LRP ilgi haritası (np.float32)
    """
    model.eval()
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

    # İleri geçiş: Ara aktivasyonları sakla
    with torch.no_grad():
        a0 = x
        a1_c = model.relu(model.conv1(a0))
        a1_p = model.pool(a1_c)

        a2_c = model.relu(model.conv2(a1_p))
        a2_p = model.pool(a2_c)

        a3_c = model.relu(model.conv3(a2_p))
        a3_p = model.pool(a3_c)

        a4_c = model.relu(model.conv4(a3_p))
        a4_p = model.pool(a4_c)

        a_flat = torch.flatten(a4_p, 1)
        a_fc1 = model.relu(model.fc1(a_flat))
        out = model.fc2(a_fc1)

    # LRP Başlangıç İlgi Vektörü: Yalnızca hedef sınıf skoru pozitifse başlatılır
    r_cikis = torch.zeros_like(out)
    r_cikis[0, hedef_sinif] = torch.clamp(out[0, hedef_sinif], min=0.0)

    # Geriye yayılım (LRP zinciri)
    # fc2 -> fc1
    r_fc1 = lrp_linear_katman(model.fc2, a_fc1, r_cikis, eps=eps)

    # fc1 -> flat
    r_flat = lrp_linear_katman(model.fc1, a_flat, r_fc1, eps=eps)
    r_pool4 = r_flat.view_as(a4_p)

    # pool4 -> conv4
    r_conv4 = lrp_maxpool3d_katman(model.pool, a4_c, r_pool4, eps=eps)
    r_pool3 = lrp_conv3d_katman(model.conv4, a3_p, r_conv4, eps=eps)

    # pool3 -> conv3
    r_conv3 = lrp_maxpool3d_katman(model.pool, a3_c, r_pool3, eps=eps)
    r_pool2 = lrp_conv3d_katman(model.conv3, a2_p, r_conv3, eps=eps)

    # pool2 -> conv2
    r_conv2 = lrp_maxpool3d_katman(model.pool, a2_c, r_pool2, eps=eps)
    r_pool1 = lrp_conv3d_katman(model.conv2, a1_p, r_conv2, eps=eps)

    # pool1 -> conv1 -> input
    r_conv1 = lrp_maxpool3d_katman(model.pool, a1_c, r_pool1, eps=eps)
    r_input = lrp_conv3d_katman(model.conv1, a0, r_conv1, eps=eps)

    # Tensörden NumPy'a aktar ve normalize et
    relevance_3d = r_input[0, 0].detach().cpu().numpy()
    relevance_3d = np.maximum(relevance_3d, 0.0)
    max_val = float(np.max(relevance_3d))
    if max_val > 1e-8:
        relevance_3d /= max_val

    return relevance_3d.astype(np.float32)


def gorsellestir(
    hacim: np.ndarray,
    ilgi_haritasi: np.ndarray,
    cikti_png: Union[str, Path],
    baslik: Optional[str] = "P06 Bohle 2019 — 3B LRP İlgi Haritası",
    esik: float = 0.15,
) -> Path:
    """
    3B MRI hacmi ile LRP ilgi haritasını 3 ana düzlemde (Aksiyel, Koronal, Sagital)
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

    # Eşikleme: Gürültüyü engellemek için düşük ilgi değerlerini sıfırla
    maskeli_ilgi = np.copy(ilgi_haritasi)
    maskeli_ilgi[maskeli_ilgi < esik] = np.nan

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    # 1. Aksiyel (Transverse) - Z dilimi
    axes[0].imshow(np.rot90(hacim[c_d, :, :]), cmap="gray")
    im0 = axes[0].imshow(np.rot90(maskeli_ilgi[c_d, :, :]), cmap="hot", alpha=0.6, vmin=0, vmax=1)
    axes[0].set_title(f"Aksiyel (Z = {c_d})")
    axes[0].axis("off")

    # 2. Koronal - Y dilimi
    axes[1].imshow(np.rot90(hacim[:, c_h, :]), cmap="gray")
    axes[1].imshow(np.rot90(maskeli_ilgi[:, c_h, :]), cmap="hot", alpha=0.6, vmin=0, vmax=1)
    axes[1].set_title(f"Koronal (Y = {c_h})")
    axes[1].axis("off")

    # 3. Sagital - X dilimi
    axes[2].imshow(np.rot90(hacim[:, :, c_w]), cmap="gray")
    axes[2].imshow(np.rot90(maskeli_ilgi[:, :, c_w]), cmap="hot", alpha=0.6, vmin=0, vmax=1)
    axes[2].set_title(f"Sagital (X = {c_w})")
    axes[2].axis("off")

    if baslik:
        fig.suptitle(baslik, fontsize=13, fontweight="bold", y=1.02)

    cbar = fig.colorbar(im0, ax=axes.ravel().tolist(), orientation="horizontal", fraction=0.04, pad=0.08)
    cbar.set_label("LRP Bağıl İlgi Düzeyi (Relevance Score)", fontsize=10)

    plt.tight_layout()
    plt.savefig(cikti_yolu, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return cikti_yolu


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P06 LRP İlgi Haritası Üretici")
    parser.add_argument("--hacim", type=str, default="", help="Girdi .npy hacim yolu")
    parser.add_argument("--cikti", type=str, default="lrp_ornek.png", help="Çıktı PNG yolu")
    parser.add_argument("--boyut", type=int, default=128, help="Küp boyutu (32 veya 128)")
    args = parser.parse_args()

    from uygulama.gorkem_P06_bohle.model import olustur

    model = olustur("cnn", sinif_sayisi=2, girdi_boyut=args.boyut)

    if args.hacim and Path(args.hacim).exists():
        hacim = np.load(args.hacim)
    else:
        print(f"Rastgele sentetik {args.boyut}³ hacim oluşturuluyor...")
        hacim = np.random.randn(args.boyut, args.boyut, args.boyut).astype(np.float32)

    harita = acikla(model, hacim, hedef_sinif=1)
    cikti = gorsellestir(hacim, harita, args.cikti)
    print(f"LRP ilgi haritası başarıyla kaydedildi: {cikti}")
