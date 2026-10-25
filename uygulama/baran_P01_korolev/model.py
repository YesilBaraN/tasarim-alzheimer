# -*- coding: utf-8 -*-
"""
P01 — Korolev vd. 2017 (ISBI, arXiv:1701.06643): VoxCNN (VGG benzeri düz 3B CNN) ve VoxResNet (3B artık ağ).

Orijinal kod (github.com/neuro-ml/resnet_cnn_mri_adni) Theano/Lasagne ve LİSANSSIZ → kopyalanmadı. Mimari, makale
(§2.1–2.2) + depodaki scripts/vgg_like_train.ipynb ve scripts/resnet_train.ipynb'nin OKUNMASIYLA (Opus hakem doğrulaması,
makaleler/baran/P01 §13) PyTorch'ta sıfırdan yazıldı. Doğrulanmış ayrıntılar:
  VoxCNN : 4 blok, filtre 8-16-32-64, çekirdek 3³ padding'siz (valid), blok başına 2-2-3-3 konv, her blok sonu MaxPool3d(2);
           Dense128 → BatchNorm → Dropout 0.7 → Dense64 → Softmax. Makalede Adam, LR 27e-6 (=2.7e-5), batch 5, 150 epoch.
  ResNet : kök 2×[Conv3d(32,3³,pad1)+BN+ReLU] → Conv3d(64,s2) → 2×VoxRes(64) → Conv3d(64,s2) → 2×VoxRes(64) → Conv3d(128,s2)
           → 2×VoxRes(128) → 7³ havuz (110³ girdide 2×2×2×128) → FC128 → Softmax; dropout YOK.
           VoxRes = BN→ReLU→Conv3³→BN→ReLU→Conv3³ + kimlik. Makalede SGD Nesterov (momentum 0.9), LR 1e-4 (depo kodu 1e-3!),
           batch 3, 70 epoch. Girdi 110³; bizde 128³ → sabit 7³ havuz yerine AdaptiveAvgPool3d(2) (aynı 2×2×2×128 çıktı).
Ortak eğitim döngüsü (egit.py) PROTOKOL gereği AdamW kullanır; makale-sadık "sanity check" koşusu README'de ayrı anlatılır.

BOYUT KISITI (25.10.2026 düzeltmesi): VoxCNN'in valid (padding'siz) 3³ konvolüsyonları her katmanda kenarı 2 kısaltır,
blok sonundaki MaxPool3d(2) ise ikiye böler. Bu zincir 100³'ün altında negatif/sıfır boyut üretip çöker (32³ → blok 3'te
-1, 64³ → blok 4'te -1, 96³ → son havuz 0). Bu yüzden girdi 100³'ün altındaysa `olustur` otomatik padding=1'e geçer ve
uyarı basar; model `padding` ve `notu` alanlarında bunu taşır. PROTOKOL madde 3 gereği tabloya giren koşular 128³ +
padding=0 olmalıdır; padding=1 yalnız duman testi ve hızlı ön deney içindir.

olustur(varyant='resnet'|'voxcnn', sinif_sayisi, girdi_boyut, padding=None)
"""
from __future__ import annotations

import torch
import torch.nn as nn

VOXCNN_EN_KUCUK_VALID = 100   # padding=0 ile çalışan en küçük kenar (99³ ve altı çöker)
VOXCNN_EN_KUCUK_SAME = 16     # padding=1 ile çalışan en küçük kenar


def voxcnn_padding(girdi_boyut: int) -> int:
    """Girdi boyutuna göre güvenli padding: ≥100³ → 0 (makale), 16–99³ → 1 (sapma), altı → hata."""
    if girdi_boyut >= VOXCNN_EN_KUCUK_VALID:
        return 0
    if girdi_boyut >= VOXCNN_EN_KUCUK_SAME:
        return 1
    raise ValueError(f"VoxCNN girdisi {girdi_boyut}³ çok küçük; en az {VOXCNN_EN_KUCUK_SAME}³ gerekir")


class VoxCNN(nn.Module):
    """Korolev 2017 VoxCNN (depo vgg_like_train.ipynb ile doğrulandı). padding=0 → makale, 1 → küçük girdi."""

    def __init__(self, sinif_sayisi: int = 2, dropout: float = 0.7, padding: int = 0,
                 bloklar=((8, 2), (16, 2), (32, 3), (64, 3))):
        super().__init__()
        self.padding = int(padding)
        self.notu = ("valid konvolusyon (makale, >=100 kenar)" if self.padding == 0
                     else f"padding={self.padding} (makaleden sapma; kucuk girdi)")
        katmanlar, giris = [], 1
        for kanal, n_conv in bloklar:
            for i in range(n_conv):
                katmanlar += [nn.Conv3d(giris if i == 0 else kanal, kanal, 3, padding=padding), nn.ReLU(inplace=True)]
            katmanlar += [nn.MaxPool3d(2)]
            giris = kanal
        self.ozellik = nn.Sequential(*katmanlar)
        # 110³ valid-padding ile son harita 1³×64 → Dense girişi 64; 128³'te 2³ olur → AdaptiveAvgPool3d(1) ile 64'e sabitlenir
        self.bas = nn.Sequential(nn.AdaptiveAvgPool3d(1), nn.Flatten(),
                                 nn.Linear(giris, 128), nn.BatchNorm1d(128), nn.ReLU(inplace=True), nn.Dropout(dropout),
                                 nn.Linear(128, 64), nn.ReLU(inplace=True), nn.Linear(64, sinif_sayisi))

    def forward(self, x):
        return self.bas(self.ozellik(x))


class VoxRes(nn.Module):
    """Ön-aktivasyonlu artık blok: BN→ReLU→Conv3³→BN→ReLU→Conv3³ + kimlik (Korolev 2017 §2.2)."""

    def __init__(self, kanal: int):
        super().__init__()
        self.govde = nn.Sequential(nn.BatchNorm3d(kanal), nn.ReLU(inplace=True), nn.Conv3d(kanal, kanal, 3, padding=1),
                                   nn.BatchNorm3d(kanal), nn.ReLU(inplace=True), nn.Conv3d(kanal, kanal, 3, padding=1))

    def forward(self, x):
        return x + self.govde(x)


class VoxResNet(nn.Module):
    """Korolev 2017 ResNet: 21 katman, 6 VoxRes bloğu (depo resnet_train.ipynb ile doğrulandı)."""

    def __init__(self, sinif_sayisi: int = 2):
        super().__init__()
        self.kok = nn.Sequential(nn.Conv3d(1, 32, 3, padding=1), nn.BatchNorm3d(32), nn.ReLU(inplace=True),
                                 nn.Conv3d(32, 32, 3, padding=1), nn.BatchNorm3d(32), nn.ReLU(inplace=True))
        self.asama1 = nn.Sequential(nn.Conv3d(32, 64, 3, stride=2, padding=1), VoxRes(64), VoxRes(64))
        self.asama2 = nn.Sequential(nn.Conv3d(64, 64, 3, stride=2, padding=1), VoxRes(64), VoxRes(64))
        self.asama3 = nn.Sequential(nn.Conv3d(64, 128, 3, stride=2, padding=1), VoxRes(128), VoxRes(128))
        self.son = nn.Sequential(nn.BatchNorm3d(128), nn.ReLU(inplace=True),
                                 nn.AdaptiveAvgPool3d(2), nn.Flatten(),            # 2×2×2×128 = 1024 (makaledeki pool-7 çıktısıyla aynı)
                                 nn.Linear(128 * 8, 128), nn.ReLU(inplace=True), nn.Linear(128, sinif_sayisi))

    def forward(self, x):
        return self.son(self.asama3(self.asama2(self.asama1(self.kok(x)))))


MAKALE_AYARI = {
    "voxcnn": dict(optimizer="Adam", lr=2.7e-5, batch=5, epoch=150),
    "resnet": dict(optimizer="SGD(nesterov, momentum=0.9)", lr=1e-4, lr_depo=1e-3, batch=3, epoch=70),
}


def olustur(varyant: str = "resnet", sinif_sayisi: int = 2, girdi_boyut: int = 128,
            padding: int | None = None, **kw) -> nn.Module:
    if varyant in ("resnet", "voxresnet", "varsayilan"):
        return VoxResNet(sinif_sayisi)
    if varyant == "voxcnn":
        p = voxcnn_padding(girdi_boyut) if padding is None else int(padding)
        if p != 0:
            print(f"UYARI VoxCNN: girdi {girdi_boyut} kenar < {VOXCNN_EN_KUCUK_VALID} -> padding={p}. Bu, "
                  f"makaledeki valid konvolusyon degil; PROTOKOL madde 3 geregi tabloya giren kosu "
                  f"128 kenar / padding=0 olmali.")
        return VoxCNN(sinif_sayisi, padding=p)
    raise ValueError("varyant: resnet | voxcnn")


if __name__ == "__main__":
    for v in ("voxcnn", "resnet"):
        for b in (64, 110, 128):
            m = olustur(v, 3, b).eval(); n = sum(p.numel() for p in m.parameters())
            with torch.no_grad():  # batch 1 + BatchNorm1d eğitim modunda hata verir
                sekil = tuple(m(torch.zeros(1, 1, b, b, b)).shape)
            print(v, b, f"{n/1e6:.2f}M parametre", sekil, getattr(m, "notu", ""))
