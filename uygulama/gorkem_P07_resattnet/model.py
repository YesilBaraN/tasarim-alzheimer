# -*- coding: utf-8 -*-
"""
P07 — Zhang vd. 2021 (IEEE J-BHI, arXiv:2008.04024v2):
3D ResAttNet (3B Artık Öz-Dikkat Ağı) + 3B Grad-CAM.

Makale Mimarisi (§III):
  - Hafif Kök (Lightweight Stem): 3 ardışık 3x3x3 Conv3D (1 -> 32 -> 32 -> 64) ile
    geleneksel 7x7x7 evrişimin getirdiği parametre ve gürültü azaltılır.
  - Rezidüel Bloklar: 3D ResNet-18 ve ResNet-34 mimarisi temel alınır.
  - 3B Öz-Dikkat (Residual Self-Attention):
      Rezidüel dal r(x) üzerinden 1x1x1 Conv3D ile Q, K, V tensörleri üretilir.
      o(r(x)) = Softmax(Q^T * K / sqrt(d)) * V
      Çıktı birleştirme: y = x + r(x) + gamma * o(r(x))
      Burada gamma skaler eğitilebilir parametresi başlangıçta 0 yapılır (stabil yakınsama).
  - Küresel Ortalama Havuzlama (GAP) + Linear(C, sinif_sayisi).

Model sözleşmesi:
  olustur(varyant='resatt18'|'resatt34'|'varsayilan', sinif_sayisi=2, girdi_boyut=128, **kw)
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class SelfAttentionBlock3D(nn.Module):
    """
    Zhang 2021 Formülasyonu 3B Öz-Dikkat Modülü (Denklem 1-3).
    Bellek tasarrufu için Q ve K kanalları C // 4 veya C // 8'e indirgenir.
    gamma katsayısı sıfırdan başlatılır.
    """

    def __init__(self, in_channels: int, indirgeme: int = 4):
        super().__init__()
        self.in_channels = in_channels
        self.mid_channels = max(1, in_channels // indirgeme)

        self.query = nn.Conv3d(in_channels, self.mid_channels, kernel_size=1)
        self.key = nn.Conv3d(in_channels, self.mid_channels, kernel_size=1)
        self.value = nn.Conv3d(in_channels, in_channels, kernel_size=1)

        # Ölçekleme faktörü gamma: Başlangıçta 0 (makale §III-B)
        self.gamma = nn.Parameter(torch.zeros(1))

    def forward(self, r_x: torch.Tensor) -> torch.Tensor:
        b, c, d, h, w = r_x.shape
        n_voksel = d * h * w

        # Q, K, V projeksiyonları
        q = self.query(r_x).view(b, self.mid_channels, n_voksel).permute(0, 2, 1)  # (b, n, mid)
        k = self.key(r_x).view(b, self.mid_channels, n_voksel)                      # (b, mid, n)
        v = self.value(r_x).view(b, c, n_voksel)                                   # (b, c, n)

        # Dikkat Haritası: (b, n, n)
        # Bellek taşmasını önlemek için sqrt(mid) ile ölçeklenir
        olcek = (self.mid_channels) ** 0.5
        enerji = torch.bmm(q, k) / olcek
        dikkat = F.softmax(enerji, dim=-1)

        # Ağırlıklı Değer: (b, c, n)
        out = torch.bmm(v, dikkat.permute(0, 2, 1))
        out = out.view(b, c, d, h, w)

        return self.gamma * out


class ResAttBlock3D(nn.Module):
    """
    3B Öz-Dikkat Entegre Edilmiş Rezidüel Blok.
    y = x + r(x) + gamma * o(r(x))
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        stride: int = 1,
        dikkat_kullan: bool = True,
    ):
        super().__init__()
        self.dikkat_kullan = dikkat_kullan

        self.conv1 = nn.Conv3d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm3d(out_channels)
        self.relu = nn.ReLU(inplace=True)

        self.conv2 = nn.Conv3d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm3d(out_channels)

        if dikkat_kullan:
            self.attention = SelfAttentionBlock3D(out_channels)
        else:
            self.attention = None

        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv3d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm3d(out_channels),
            )
        else:
            self.shortcut = nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        kimlik = self.shortcut(x)

        # Rezidüel dal r(x)
        r = self.conv1(x)
        r = self.bn1(r)
        r = self.relu(r)
        r = self.conv2(r)
        r = self.bn2(r)

        # Öz-dikkat terimi: gamma * o(r(x))
        if self.attention is not None:
            r = r + self.attention(r)

        out = self.relu(kimlik + r)
        return out


class ResAttNet3D(nn.Module):
    """
    Zhang vd. 2021 3D ResAttNet Mimarisi.
    Katman konfigürasyonu:
      resatt18: [2, 2, 2, 2] blok
      resatt34: [3, 4, 6, 3] blok
    """

    def __init__(
        self,
        katman_sayilari: list[int],
        sinif_sayisi: int = 2,
        dikkat_kullan: bool = True,
    ):
        super().__init__()
        self.sinif_sayisi = sinif_sayisi
        self.dikkat_kullan = dikkat_kullan

        # 1. Hafif Kök (Lightweight Stem - 3 ardışık 3x3x3 evrişim)
        self.stem = nn.Sequential(
            nn.Conv3d(1, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm3d(32),
            nn.ReLU(inplace=True),
            nn.Conv3d(32, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm3d(32),
            nn.ReLU(inplace=True),
            nn.Conv3d(32, 64, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm3d(64),
            nn.ReLU(inplace=True),
        )

        # 2. ResAttNet Aşamaları (Katman 1-4)
        self.in_kanallar = 64
        self.layer1 = self._katman_olustur(64, katman_sayilari[0], stride=1, dikkat=False)
        self.layer2 = self._katman_olustur(128, katman_sayilari[1], stride=2, dikkat=False)
        # Makaleye göre 3B öz-dikkat ve Grad-CAM özellikle layer3 ve layer4'e odaklanır
        self.layer3 = self._katman_olustur(256, katman_sayilari[2], stride=2, dikkat=dikkat_kullan)
        self.layer4 = self._katman_olustur(512, katman_sayilari[3], stride=2, dikkat=dikkat_kullan)

        # 3. Sınıflandırıcı Başlığı
        self.gap = nn.AdaptiveAvgPool3d(1)
        self.fc = nn.Linear(512, sinif_sayisi)

    def _katman_olustur(
        self,
        kanallar: int,
        blok_sayisi: int,
        stride: int = 1,
        dikkat: bool = True,
    ) -> nn.Sequential:
        bloklar = []
        bloklar.append(ResAttBlock3D(self.in_kanallar, kanallar, stride=stride, dikkat_kullan=dikkat))
        self.in_kanallar = kanallar
        for _ in range(1, blok_sayisi):
            bloklar.append(ResAttBlock3D(kanallar, kanallar, stride=1, dikkat_kullan=dikkat))
        return nn.Sequential(*bloklar)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.stem(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.gap(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x


def olustur(
    varyant: str = "resatt18",
    sinif_sayisi: int = 2,
    girdi_boyut: int = 128,
    **kw,
) -> nn.Module:
    """
    P07 Model Fabrikası:
      varyant: 'resatt18', 'resatt34', 'varsayilan' (resatt18)
      dikkat_acik: bool (Ablasyon için False verilebilir)
    """
    v = str(varyant).lower().strip()
    dikkat_kullan = kw.get("dikkat_acik", True)

    if v in ("resatt18", "varsayilan"):
        return ResAttNet3D(
            katman_sayilari=[2, 2, 2, 2],
            sinif_sayisi=sinif_sayisi,
            dikkat_kullan=dikkat_kullan,
        )
    elif v in ("resatt34", "3d_resattnet34"):
        return ResAttNet3D(
            katman_sayilari=[3, 4, 6, 3],
            sinif_sayisi=sinif_sayisi,
            dikkat_kullan=dikkat_kullan,
        )
    raise ValueError(
        f"gorkem_P07_resattnet bilinmeyen varyant: '{varyant}'. "
        f"Desteklenenler: 'resatt18', 'resatt34', 'varsayilan'"
    )
