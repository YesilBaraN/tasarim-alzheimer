# -*- coding: utf-8 -*-
"""
P12 — Solano-Rojas 2021 (Sensors 21:1300 / ANNPR 2020) & Dhinagar 2023:
3 Boyutlu DenseNet (Yoğun Evrişimli Sinir Ağı) Mimarisi.

Özellikler:
  - `DenseNet121_3D`: Standart 3B DenseNet-121 omurgası (yoğun bloklar: 6, 12, 24, 16 katman; k=32).
  - `TinyDenseNet_3D`: Düşük parametreli (1.8M) kompakt 3B DenseNet (Dhinagar 2023 standardı).
  - MONAI varsa `monai.networks.nets.DenseNet121` ile entegre olur;
    yoksa saf PyTorch 3B DenseNet omurgası ile bağımlılıksız çalışır.

Model sözleşmesi:
  olustur(varyant='densenet121'|'tiny_densenet', sinif_sayisi=2, girdi_boyut=128, **kw)
"""
from __future__ import annotations

import math
from typing import List, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F


class _DenseLayer3D(nn.Module):
    """3B DenseNet Temel Yoğun Katmanı: BN -> ReLU -> 1x1x1 Conv3D -> BN -> ReLU -> 3x3x3 Conv3D"""

    def __init__(self, in_features: int, growth_rate: int, bn_size: int = 4, drop_rate: float = 0.2):
        super().__init__()
        self.drop_rate = float(drop_rate)
        mid_features = bn_size * growth_rate

        self.bn1 = nn.BatchNorm3d(in_features)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv1 = nn.Conv3d(in_features, mid_features, kernel_size=1, stride=1, bias=False)

        self.bn2 = nn.BatchNorm3d(mid_features)
        self.relu2 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv3d(mid_features, growth_rate, kernel_size=3, stride=1, padding=1, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.conv1(self.relu1(self.bn1(x)))
        out = self.conv2(self.relu2(self.bn2(out)))
        if self.drop_rate > 0:
            out = F.dropout(out, p=self.drop_rate, training=self.training)
        return torch.cat([x, out], 1)


class _DenseBlock3D(nn.Module):
    """Ardışık _DenseLayer3D katmanlarından oluşan 3B Yoğun Blok"""

    def __init__(self, num_layers: int, in_features: int, growth_rate: int, bn_size: int = 4, drop_rate: float = 0.2):
        super().__init__()
        layers = []
        for i in range(num_layers):
            layers.append(
                _DenseLayer3D(
                    in_features=in_features + i * growth_rate,
                    growth_rate=growth_rate,
                    bn_size=bn_size,
                    drop_rate=drop_rate,
                )
            )
        self.block = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.block(x)


class _Transition3D(nn.Module):
    """Bloklar arası kanal indirgeme ve uzamsal alt örnekleme (AvgPool3D)"""

    def __init__(self, in_features: int, out_features: int):
        super().__init__()
        self.bn = nn.BatchNorm3d(in_features)
        self.relu = nn.ReLU(inplace=True)
        self.conv = nn.Conv3d(in_features, out_features, kernel_size=1, stride=1, bias=False)
        self.pool = nn.AvgPool3d(kernel_size=2, stride=2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.conv(self.relu(self.bn(x)))
        out = self.pool(out)
        return out


class DenseNet3D(nn.Module):
    """
    Parametrik 3B DenseNet Mimarisi.
    DenseNet-121 (6, 12, 24, 16; k=32) ve Tiny DenseNet (4, 4, 4, 4; k=16) konfigürasyonlarını destekler.
    """

    def __init__(
        self,
        block_config: Tuple[int, ...] = (6, 12, 24, 16),
        growth_rate: int = 32,
        init_features: int = 64,
        bn_size: int = 4,
        drop_rate: float = 0.2,
        sinif_sayisi: int = 2,
        girdi_boyut: int = 128,
    ):
        super().__init__()
        self.sinif_sayisi = int(sinif_sayisi)
        self.girdi_boyut = int(girdi_boyut)

        # Kök Katman (Stem): 1 kanal -> init_features (7x7x7 Conv, stride 2)
        # Boyut <= 32 ise kernel=3, stride=1 kullanarak aşırı küçülmeyi engeller
        stem_k = 7 if girdi_boyut >= 64 else 3
        stem_s = 2 if girdi_boyut >= 64 else 1
        stem_p = 3 if girdi_boyut >= 64 else 1

        self.features = nn.Sequential()
        self.features.add_module("conv0", nn.Conv3d(1, init_features, kernel_size=stem_k, stride=stem_s, padding=stem_p, bias=False))
        self.features.add_module("norm0", nn.BatchNorm3d(init_features))
        self.features.add_module("relu0", nn.ReLU(inplace=True))
        if girdi_boyut >= 64:
            self.features.add_module("pool0", nn.MaxPool3d(kernel_size=3, stride=2, padding=1))

        # Yoğun Bloklar ve Geçiş Katmanları
        num_features = init_features
        for i, num_layers in enumerate(block_config):
            block = _DenseBlock3D(
                num_layers=num_layers,
                in_features=num_features,
                growth_rate=growth_rate,
                bn_size=bn_size,
                drop_rate=drop_rate,
            )
            self.features.add_module(f"denseblock{i + 1}", block)
            num_features = num_features + num_layers * growth_rate

            if i != len(block_config) - 1:
                # Geçiş katmanı: kanal sayısını yarıya indir (reduction = 0.5)
                out_features = num_features // 2
                trans = _Transition3D(in_features=num_features, out_features=out_features)
                self.features.add_module(f"transition{i + 1}", trans)
                num_features = out_features

        # Son Normalizasyon
        self.features.add_module("norm_final", nn.BatchNorm3d(num_features))
        self.features.add_module("relu_final", nn.ReLU(inplace=True))

        # Sınıflandırıcı Kafa
        self.gap = nn.AdaptiveAvgPool3d((1, 1, 1))
        self.classifier = nn.Sequential(
            nn.Dropout(drop_rate),
            nn.Linear(num_features, self.sinif_sayisi),
        )

        # Ağırlık İlklendirme
        for m in self.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, nn.BatchNorm3d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.constant_(m.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        feat = self.features(x)
        pooled = self.gap(feat).view(x.size(0), -1)
        out = self.classifier(pooled)
        return out


def olustur(
    varyant: str = "densenet121",
    sinif_sayisi: int = 2,
    girdi_boyut: int = 128,
    **kw,
) -> nn.Module:
    """
    P12 3B DenseNet Model Fabrikası.

    Varyantlar:
      - 'densenet121', 'varsayilan': Standart 3B DenseNet-121 (~11.2M parametre)
      - 'tiny_densenet', 'dusuk_maliyet': Kompakt 3B DenseNet (~1.8M parametre, 4x4 blok, k=16)
    """
    v = str(varyant).lower().strip()

    if v in ("tiny_densenet", "tiny", "dusuk_maliyet", "kompakt"):
        return DenseNet3D(
            block_config=(4, 4, 4, 4),
            growth_rate=16,
            init_features=32,
            bn_size=2,
            drop_rate=0.2,
            sinif_sayisi=sinif_sayisi,
            girdi_boyut=girdi_boyut,
        )

    # Standart DenseNet-121
    # Eğer ortamda MONAI varsa ve girdi boyutu >= 64 ise MONAI sınıfını kullanabilir
    use_monai = kw.get("use_monai", False)
    if use_monai and girdi_boyut >= 64:
        try:
            from monai.networks.nets import DenseNet121 as MonaiDenseNet121
            return MonaiDenseNet121(
                spatial_dims=3,
                in_channels=1,
                out_channels=sinif_sayisi,
                dropout_prob=kw.get("drop_rate", 0.5),
            )
        except ImportError:
            pass

    # Bağımsız saf PyTorch 3B DenseNet-121
    return DenseNet3D(
        block_config=(6, 12, 24, 16),
        growth_rate=32,
        init_features=64,
        bn_size=4,
        drop_rate=kw.get("drop_rate", 0.5),
        sinif_sayisi=sinif_sayisi,
        girdi_boyut=girdi_boyut,
    )
