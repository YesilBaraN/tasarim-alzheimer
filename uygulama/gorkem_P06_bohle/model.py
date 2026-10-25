# -*- coding: utf-8 -*-
"""
P06 — Böhle vd. 2019 (Front. Aging Neurosci., 11:194):
3B CNN + Katman Bazlı İlgi Yayılımı (Layer-wise Relevance Propagation, LRP).

Kaynak Kod: moboehle/Pytorch-LRP (BSD-3 Lisansı, PyTorch)
Makale Mimarisi:
  - 4 ardışık Conv3D + ReLU + MaxPool3D(2) bloğu (filtreler: 8, 16, 32, 64)
  - Çekirdek boyutu 3x3x3, padding=1 (aynı boyut)
  - 4 havuzlama sonrası uzamsal boyut 16'ya bölünür:
      girdi 32³  -> 2³  -> 64 x 2³ = 512
      girdi 128³ -> 8³  -> 64 x 8³ = 32.768
  - Tam bağlantılı katmanlar: Linear(linear_in, 128) -> ReLU -> Dropout(0.4) -> Linear(128, sinif_sayisi)

Model sözleşmesi:
  olustur(varyant='cnn', sinif_sayisi=2, girdi_boyut=128, **kw)
"""
from __future__ import annotations

import torch
import torch.nn as nn


class BohleCNN3D(nn.Module):
    """
    Böhle vd. 2019 Makalesindeki 3B CNN mimarisi (ClassificationModel3D).
    LRP katman tersinirliği için temiz ve sıralı modüller kullanılır.
    """

    def __init__(
        self,
        sinif_sayisi: int = 2,
        girdi_boyut: int = 128,
        dropout: float = 0.4,
    ):
        super().__init__()
        self.sinif_sayisi = sinif_sayisi
        self.girdi_boyut = int(girdi_boyut)
        self.dropout_rate = float(dropout)

        # 4 Evrişim Bloğu (Filtreler: 8 -> 16 -> 32 -> 64)
        self.conv1 = nn.Conv3d(1, 8, kernel_size=3, padding=1)
        self.conv2 = nn.Conv3d(8, 16, kernel_size=3, padding=1)
        self.conv3 = nn.Conv3d(16, 32, kernel_size=3, padding=1)
        self.conv4 = nn.Conv3d(32, 64, kernel_size=3, padding=1)

        self.relu = nn.ReLU(inplace=True)
        self.pool = nn.MaxPool3d(kernel_size=2, stride=2)

        # 4 havuzlama sonrası tensör boyutu: (girdi_boyut // 16)³
        uzamsal_son = max(1, self.girdi_boyut // 16)
        self.linear_in = 64 * (uzamsal_son**3)

        self.fc1 = nn.Linear(self.linear_in, 128)
        self.dropout = nn.Dropout(self.dropout_rate)
        self.fc2 = nn.Linear(128, sinif_sayisi)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Blok 1
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)

        # Blok 2
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)

        # Blok 3
        x = self.conv3(x)
        x = self.relu(x)
        x = self.pool(x)

        # Blok 4
        x = self.conv4(x)
        x = self.relu(x)
        x = self.pool(x)

        # Sınıflandırıcı Başlığı
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x


def olustur(
    varyant: str = "cnn",
    sinif_sayisi: int = 2,
    girdi_boyut: int = 128,
    **kw,
) -> nn.Module:
    """
    Model fabrikası sözleşmesi (uygulama/ortak/egit.py ve test_model.py ile uyumlu).

    Parametreler:
      varyant: 'cnn' veya 'varsayilan'
      sinif_sayisi: 2 (AD vs NC) veya 3 (NC/MCI/AD)
      girdi_boyut: küp kenar uzunluğu (örn. 32 veya 128)
    """
    v = str(varyant).lower().strip()
    if v in ("cnn", "varsayilan", "bohle"):
        dropout = kw.get("dropout", 0.4)
        return BohleCNN3D(
            sinif_sayisi=sinif_sayisi,
            girdi_boyut=girdi_boyut,
            dropout=dropout,
        )
    raise ValueError(
        f"gorkem_P06_bohle bilinmeyen varyant: '{varyant}'. "
        f"Desteklenenler: 'cnn', 'varsayilan'"
    )
