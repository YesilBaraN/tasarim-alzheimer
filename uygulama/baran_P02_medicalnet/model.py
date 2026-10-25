# -*- coding: utf-8 -*-
"""
P02 — Chen vd. 2019 Med3D / MedicalNet (arXiv:1904.00625; github.com/Tencent/MedicalNet, MIT): 3B ResNet transfer öğrenme.

Opus hakem doğrulaması (makaleler/baran/P02 §13) ile netleşen kurulum:
 - MONAI (≥1.3) `resnet18(spatial_dims=3, n_input_channels=1, feed_forward=False, shortcut_type='A', bias_downsample=True,
   pretrained=True)` HF Hub'dan (TencentMedicalNet/MedicalNet-Resnet18) önce resnet_18_23dataset.pth, yoksa resnet_18.pth indirir.
   ResNet-18/34 için shortcut 'A' + bias_downsample True; 10/50/101/152/200 için 'B' + False (MONAI get_medicalnet_pretrained_resnet_args).
 - feed_forward=False → ağ, GAP sonrası 512 boyutlu öznitelik döner; sınıflandırma başını biz ekleriz (makale §3.3: GAP + FC).
 - conv1: 7³, stride 2, pad 3, bias yok → MONAI'de conv1_t_size=7, conv1_t_stride=2.
 - FARK: MedicalNet layer3/4'te stride 1 + dilation 2/4 (segmentasyon); MONAI stride 2 → 128³'te son harita 4³ (MedicalNet'te 16³).
   Ağırlık şekilleri aynı, alıcı alan farklı. Ablation (b): MedicalNet models/resnet.py (MIT) kopyalanıp conv_seg → GAP+FC.
 - Makaledeki 8 kümeli ağırlık (resnet_18.pth) istenirse `agirlik=<yol>` ile elle yüklenir ('module.' öneki ayıklanır, conv_seg atlanır).
 - Ön işleme uyumu: maske içi z-score sonrası 0.5–99.5 yüzdelik kırpma (makale §3.1) — onisle.py'de `--kirp_yuzdelik` (isteğe bağlı).

olustur(varyant='resnet18'|'resnet34'|'resnet10'|'resnet50', sinif_sayisi, girdi_boyut, agirlik=None|'monai'|<yol>, dondur=False)
   agirlik=None  → sıfırdan (TFS temel çizgisi)   agirlik='monai' → MONAI HF Hub (23 kümeli)   agirlik=<.pth> → elle yükle
"""
from __future__ import annotations

from pathlib import Path

import torch
import torch.nn as nn

OZNITELIK = {10: 512, 18: 512, 34: 512, 50: 2048}


def _medicalnet_args(derinlik: int) -> dict:
    """MONAI, (bias_downsample, shortcut_type) sırasıyla döndürür — ters açmak
    `Unsupported option 'True'` hatası verir. Sürüm sırayı değiştirirse diye tipe bakıp ayırıyoruz."""
    try:
        from monai.networks.nets.resnet import get_medicalnet_pretrained_resnet_args
        a, b = get_medicalnet_pretrained_resnet_args(derinlik)
        shortcut, bias = (a, b) if isinstance(a, str) else (b, a)
        return dict(shortcut_type=str(shortcut), bias_downsample=bool(bias))
    except Exception:
        return dict(shortcut_type="A", bias_downsample=True) if derinlik in (18, 34) else dict(shortcut_type="B", bias_downsample=False)


def _govde(derinlik: int, pretrained: bool) -> nn.Module:
    from monai.networks.nets import resnet10, resnet18, resnet34, resnet50
    fab = {10: resnet10, 18: resnet18, 34: resnet34, 50: resnet50}[derinlik]
    return fab(spatial_dims=3, n_input_channels=1, feed_forward=False, conv1_t_size=7, conv1_t_stride=2,
               pretrained=pretrained, **_medicalnet_args(derinlik))


class MedicalNetSiniflayici(nn.Module):
    """MONAI ResNet gövdesi (GAP'li, FC'siz) + Dropout + Linear başı."""

    def __init__(self, govde: nn.Module, oznitelik: int, sinif_sayisi: int, dropout: float = 0.3):
        super().__init__()
        self.govde = govde
        self.bas = nn.Sequential(nn.Dropout(dropout), nn.Linear(oznitelik, sinif_sayisi))

    def forward(self, x):
        return self.bas(self.govde(x))


def medicalnet_yukle(govde: nn.Module, yol: str | Path) -> dict:
    """MedicalNet .pth → MONAI ResNet gövdesi. 'module.' önekini ayıklar, conv_seg/fc atlar; eksik/fazla anahtarları döner."""
    try:   # indirilen dosya: önce güvenli yol (torch ≥2.6 varsayılanı)
        d = torch.load(yol, map_location="cpu", weights_only=True)
    except Exception:
        d = torch.load(yol, map_location="cpu")
    sd = d.get("state_dict", d)
    yeni = {}
    for k, v in sd.items():
        k2 = k[7:] if k.startswith("module.") else k
        if k2.startswith(("conv_seg", "fc.")):
            continue
        yeni[k2] = v
    hedef = govde.state_dict()
    uyumlu = {k: v for k, v in yeni.items() if k in hedef and hedef[k].shape == v.shape}
    sonuc = govde.load_state_dict(uyumlu, strict=False)
    rapor = {"dosya": str(yol), "yuklenen": len(uyumlu), "eksik": list(sonuc.missing_keys),
             "fazla": [k for k in yeni if k not in uyumlu]}
    print(f"MedicalNet elle yükleme: {rapor['yuklenen']} tensör; eksik {len(rapor['eksik'])}, fazla {len(rapor['fazla'])}")
    if rapor["eksik"]:
        print("  eksik örnek:", rapor["eksik"][:5])
    return rapor


def olustur(varyant: str = "resnet18", sinif_sayisi: int = 2, girdi_boyut: int = 128, agirlik: str | None = None,
            dondur: bool = False, dropout: float = 0.3, **kw) -> nn.Module:
    derinlik = {"resnet10": 10, "resnet18": 18, "resnet34": 34, "resnet50": 50, "varsayilan": 18}[varyant]
    if agirlik == "monai":
        govde = _govde(derinlik, pretrained=True)          # HF Hub: resnet_<d>_23dataset.pth
    else:
        govde = _govde(derinlik, pretrained=False)
        if agirlik:                                        # yerel MedicalNet dosyası (ör. 8 kümeli resnet_18.pth)
            medicalnet_yukle(govde, agirlik)
    model = MedicalNetSiniflayici(govde, OZNITELIK[derinlik], sinif_sayisi, dropout)
    if dondur and agirlik:                                 # ilk epoch'larda yalnız baş + BN (hakem notu 12.3/6)
        for ad, p in model.govde.named_parameters():
            p.requires_grad = ("bn" in ad) or ("downsample.1" in ad)
    return model


def coz(model: nn.Module):
    """Dondurulmuş gövdeyi tamamen eğitilebilir yapar (ısınma epoch'larından sonra çağrılır)."""
    for p in model.parameters():
        p.requires_grad = True


if __name__ == "__main__":
    m = olustur("resnet18", 3, 64)
    print(f"{sum(p.numel() for p in m.parameters())/1e6:.2f}M parametre", tuple(m(torch.zeros(1, 1, 64, 64, 64)).shape))
