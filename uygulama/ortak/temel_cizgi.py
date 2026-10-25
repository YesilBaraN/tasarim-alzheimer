# -*- coding: utf-8 -*-
"""
temel_cizgi.py — PROTOKOL madde 9 temel çizgileri:
 (a) SigCNN3D: 4 bloklu sığ 3B CNN (Zhang & Khalvati 2022 "sığ 3B CNN yeter" argümanı)
 (b) svm_kosu: voksel tabanlı lineer SVM (Wen 2020) — hacim 32³'e indirgenir, StandardScaler + LinearSVC
Model sözleşmesi: olustur(varyant='sigcnn', sinif_sayisi, girdi_boyut)
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class SigCNN3D(nn.Module):
    def __init__(self, sinif_sayisi: int = 2, kanallar=(8, 16, 32, 64), dropout: float = 0.5):
        super().__init__()
        katmanlar, giris = [], 1
        for c in kanallar:
            katmanlar += [nn.Conv3d(giris, c, 3, padding=1, bias=False), nn.BatchNorm3d(c), nn.ReLU(inplace=True), nn.MaxPool3d(2)]
            giris = c
        self.ozellik = nn.Sequential(*katmanlar)
        self.bas = nn.Sequential(nn.AdaptiveAvgPool3d(1), nn.Flatten(), nn.Dropout(dropout), nn.Linear(giris, sinif_sayisi))

    def forward(self, x):
        return self.bas(self.ozellik(x))


def olustur(varyant: str = "sigcnn", sinif_sayisi: int = 2, girdi_boyut: int = 128, **kw) -> nn.Module:
    return SigCNN3D(sinif_sayisi)


def svm_kosu(X_egitim: np.ndarray, y_egitim: np.ndarray, X_test: np.ndarray, boyut: int = 32, C: float = 1.0):
    """X: [N, B, B, B] float. 32³'e indirger, ölçekler, LinearSVC eğitir; olasılık benzeri karar değeri döner."""
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import LinearSVC

    def indir(X):
        t = torch.from_numpy(np.asarray(X, dtype=np.float32))[:, None]
        t = F.interpolate(t, size=(boyut,) * 3, mode="trilinear", align_corners=False)
        return t[:, 0].reshape(len(X), -1).numpy()

    olcek = StandardScaler(); A = olcek.fit_transform(indir(X_egitim)); B = olcek.transform(indir(X_test))
    svm = LinearSVC(C=C, max_iter=5000, class_weight="balanced").fit(A, y_egitim)
    karar = svm.decision_function(B)
    if karar.ndim == 1:
        p = 1 / (1 + np.exp(-karar)); return np.stack([1 - p, p], 1)
    e = np.exp(karar - karar.max(1, keepdims=True)); return e / e.sum(1, keepdims=True)
