# -*- coding: utf-8 -*-
"""metrikler.py — PROTOKOL madde 6: BAcc, AUC, F1-makro, duyarlılık, özgüllük, doğruluk, karışıklık matrisi."""
from __future__ import annotations

import numpy as np
from sklearn.metrics import (balanced_accuracy_score, confusion_matrix, f1_score, roc_auc_score, accuracy_score)


def hesapla(y_true, y_prob, gorev: str = "ikili") -> dict:
    y_true = np.asarray(y_true); y_prob = np.asarray(y_prob)
    if y_prob.ndim == 1:
        y_prob = np.stack([1 - y_prob, y_prob], 1)
    y_pred = y_prob.argmax(1)
    cm = confusion_matrix(y_true, y_pred, labels=list(range(y_prob.shape[1])))
    out = {
        "acc": float(accuracy_score(y_true, y_pred)),
        "bacc": float(balanced_accuracy_score(y_true, y_pred)),
        "f1_makro": float(f1_score(y_true, y_pred, average="macro")),
        "cm": cm.tolist(),
        "n": int(len(y_true)),
    }
    try:
        if y_prob.shape[1] == 2:
            out["auc"] = float(roc_auc_score(y_true, y_prob[:, 1]))
        else:
            out["auc"] = float(roc_auc_score(y_true, y_prob, multi_class="ovr", average="macro"))
    except ValueError:
        out["auc"] = float("nan")  # tek sınıf varsa
    # duyarlılık / özgüllük: ikilide pozitif = 1 (AD); üç sınıfta sınıf başına ortalama (OvR)
    sens, spec = [], []
    for k in range(cm.shape[0]):
        tp = cm[k, k]; fn = cm[k].sum() - tp; fp = cm[:, k].sum() - tp; tn = cm.sum() - tp - fn - fp
        sens.append(tp / max(tp + fn, 1)); spec.append(tn / max(tn + fp, 1))
    if cm.shape[0] == 2:
        out["sens"], out["spec"] = float(sens[1]), float(spec[1])
    else:
        out["sens"], out["spec"] = float(np.mean(sens)), float(np.mean(spec))
        out["sens_sinif"], out["spec_sinif"] = [float(s) for s in sens], [float(s) for s in spec]
    return out


def ozet(sonuclar: list[dict]) -> dict:
    """Kat/tohum sonuçlarının ortalama ± ss özeti."""
    anahtarlar = ["acc", "bacc", "auc", "f1_makro", "sens", "spec"]
    o = {}
    for k in anahtarlar:
        v = np.array([s[k] for s in sonuclar if k in s], dtype=float)
        o[k] = {"ort": float(np.nanmean(v)), "ss": float(np.nanstd(v)), "n": int(np.isfinite(v).sum())}
    return o


def bicim(m: dict) -> str:
    """ortalama ± ss — ama **tek koşuda sapma basılmaz**.

    `±0,000` yazmak yanlış ve tehlikeli: sapmanın sıfır olduğunu, yani sonucun kat/tohum
    değişiminden etkilenmediğini ima ediyor. Gerçekte tek koşu olduğu için sapma
    **hesaplanamamıştır**. Prova raporunda bu yanlış okumayı elle not etmek zorunda kaldık;
    kaynağında düzeltiliyor. n ≥ 2 olunca normal `ort ± ss` biçimine dönüyor.
    """
    if m.get("n", 0) < 2:
        return f"{m['ort']:.3f} (tek koşu)"
    return f"{m['ort']:.3f}±{m['ss']:.3f}"


def satir(model: str, gorev: str, on_egitim: str, o: dict, ek: dict | None = None) -> str:
    """SONUCLAR.md satırı (PROTOKOL 'sonuç satırı biçimi')."""
    f = lambda k: bicim(o[k])
    ek = ek or {}
    return (f"| {model} | {gorev} | {on_egitim} | {f('bacc')} | {f('auc')} | {f('f1_makro')} | {f('sens')} | {f('spec')} | {f('acc')} | "
            f"{ek.get('dis_bacc', '—')} | {ek.get('param', '—')} | {ek.get('epoch_sure', '—')} | {ek.get('vram', '—')} | {ek.get('commit', '—')} |")
