# -*- coding: utf-8 -*-
"""
P11 — Qiu vd. 2020 (Brain 143: 1920-1933):
3B FCN (Tam Evrişimli Ağ) + Hastalık Olasılık Haritası (DPM) + MLP.

Kaynak Kod: vkola-lab/brain2020 (MIT Lisansı, PyTorch)
Makale Mimarisi:
  - 4 Evrişim Bloğu (Filtreler: 20 -> 40 -> 80 -> 160)
  - MaxPool3D + BatchNorm3d + LeakyReLU + Dropout
  - Sınıflandırıcı: Linear(160*6*6*6, 30) -> LeakyReLU -> Dropout(0.5) -> Linear(30, sinif_sayisi)
  - `dense_to_conv()`: Tam evrişimli forma dönüştürerek tek geçişte 3B risk haritası üretir.

Model sözleşmesi:
  olustur(varyant='fcn', sinif_sayisi=2, girdi_boyut=128, **kw)
"""
from __future__ import annotations

import copy
import torch
import torch.nn as nn


class QiuFCN3D(nn.Module):
    """
    Qiu vd. 2020 (vkola-lab/brain2020) 3B Tam Evrişimli Ağ (FCN) Modeli.
    Hem yerel yamalarda (47³) hem de tam hacimde (128³ ve duman testi 32³)
    sorunsuz çalışacak şekilde tasarlanmıştır.
    """

    def __init__(
        self,
        fil_num: int = 20,
        drop_rate: float = 0.5,
        sinif_sayisi: int = 2,
        girdi_boyut: int = 128,
    ):
        super().__init__()
        self.fil_num = int(fil_num)
        self.drop_rate = float(drop_rate)
        self.sinif_sayisi = int(sinif_sayisi)
        self.girdi_boyut = int(girdi_boyut)

        # 4 Evrişim Bloğu (vkola-lab/brain2020 _FCN mimarisi)
        self.features = nn.Sequential(
            # Blok 1: 1 -> fil_num
            nn.Conv3d(1, self.fil_num, kernel_size=4, stride=1, padding=0, bias=False),
            nn.MaxPool3d(kernel_size=2, stride=1, padding=0),
            nn.BatchNorm3d(self.fil_num),
            nn.LeakyReLU(inplace=True),
            nn.Dropout(0.1),
            # Blok 2: fil_num -> 2*fil_num
            nn.Conv3d(self.fil_num, 2 * self.fil_num, kernel_size=4, stride=1, padding=0, bias=False),
            nn.MaxPool3d(kernel_size=2, stride=2, padding=0),
            nn.BatchNorm3d(2 * self.fil_num),
            nn.LeakyReLU(inplace=True),
            nn.Dropout(0.1),
            # Blok 3: 2*fil_num -> 4*fil_num
            nn.Conv3d(2 * self.fil_num, 4 * self.fil_num, kernel_size=3, stride=1, padding=0, bias=False),
            nn.MaxPool3d(kernel_size=2, stride=2, padding=0),
            nn.BatchNorm3d(4 * self.fil_num),
            nn.LeakyReLU(inplace=True),
            nn.Dropout(0.1),
            # Blok 4: 4*fil_num -> 8*fil_num
            nn.Conv3d(4 * self.fil_num, 8 * self.fil_num, kernel_size=3, stride=1, padding=0, bias=False),
            nn.MaxPool3d(kernel_size=2, stride=1, padding=0),
            nn.BatchNorm3d(8 * self.fil_num),
            nn.LeakyReLU(inplace=True),
        )

        # Uzamsal boyut uyarlayıcı: girdi boyutu ne olursa olsun (32³, 47³, 128³)
        # öznitelik haritasını (6, 6, 6) boyutuna hizalar (8*fil_num * 6*6*6 = 34560)
        self.adaptor = nn.AdaptiveAvgPool3d((6, 6, 6))
        self.feature_length = 8 * self.fil_num * 6 * 6 * 6

        # Sınıflandırıcı Kafa (brain2020 standardı)
        self.classifier = nn.Sequential(
            nn.Dropout(self.drop_rate),
            nn.Linear(self.feature_length, 30),
            nn.LeakyReLU(inplace=True),
            nn.Dropout(self.drop_rate),
            nn.Linear(30, self.sinif_sayisi),
        )

    def forward(self, x: torch.Tensor, cikarim_tipi: str = "siniflandir") -> torch.Tensor:
        """
        x: (B, 1, D, H, W)
        cikarim_tipi:
          - 'siniflandir': (B, sinif_sayisi) sınıf lojitleri
          - 'oznitelik': (B, 30) ara öznitelik vektörü
        """
        feat = self.features(x)
        feat_pooled = self.adaptor(feat)
        flat = feat_pooled.view(x.size(0), -1)

        if cikarim_tipi == "oznitelik":
            x_feat = self.classifier[0](flat)
            x_feat = self.classifier[1](x_feat)
            return x_feat

        out = self.classifier(flat)
        return out

    def dense_to_conv(self) -> nn.Module:
        """
        Tam bağlantılı katmanları 3B evrişime dönüştürür.
        Tüm beyin verildiğinde tek seferde 3B Hastalık Olasılık Haritası (DPM) üretir.
        """
        fcn = copy.deepcopy(self)
        weight_fc1 = fcn.classifier[1].weight.view(30, 8 * self.fil_num, 6, 6, 6)
        weight_fc2 = fcn.classifier[4].weight.view(self.sinif_sayisi, 30, 1, 1, 1)
        bias_fc1 = fcn.classifier[1].bias
        bias_fc2 = fcn.classifier[4].bias

        conv_fc1 = nn.Conv3d(8 * self.fil_num, 30, kernel_size=6, stride=1, padding=0)
        conv_fc2 = nn.Conv3d(30, self.sinif_sayisi, kernel_size=1, stride=1, padding=0)

        conv_fc1.weight = nn.Parameter(weight_fc1)
        conv_fc1.bias = nn.Parameter(bias_fc1)
        conv_fc2.weight = nn.Parameter(weight_fc2)
        conv_fc2.bias = nn.Parameter(bias_fc2)

        fcn_conv = nn.Sequential(
            fcn.features,
            conv_fc1,
            nn.LeakyReLU(inplace=True),
            conv_fc2,
        )
        return fcn_conv

    def olasilik_haritasi(self, x: torch.Tensor) -> torch.Tensor:
        """
        Tam beyin sMRI tensörü (B, 1, D, H, W) alır,
        3B uzamsal hastalık risk haritası (B, sinif_sayisi, D', H', W') üretir.
        """
        fcn_conv = self.dense_to_conv()
        fcn_conv.eval()
        with torch.no_grad():
            logits = fcn_conv(x)
            probs = torch.softmax(logits, dim=1)
        return probs


def olustur(
    varyant: str = "fcn",
    sinif_sayisi: int = 2,
    girdi_boyut: int = 128,
    fil_num: int = 20,
    drop_rate: float = 0.5,
    **kw,
) -> nn.Module:
    """
    Ortak model fabrikası sözleşmesi (uygulama/ortak/egit.py ve test_model.py).

    Args:
        varyant: 'fcn', 'brain2020', 'varsayilan'
        sinif_sayisi: 2 (AD-NC) veya 3 (AD-MCI-NC)
        girdi_boyut: 128 (protokol) veya 32 (duman testi)
    """
    return QiuFCN3D(
        fil_num=fil_num,
        drop_rate=drop_rate,
        sinif_sayisi=sinif_sayisi,
        girdi_boyut=girdi_boyut,
    )
