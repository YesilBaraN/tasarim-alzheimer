# -*- coding: utf-8 -*-
r"""
onnx_disa_aktar.py — Eğitilmiş checkpoint'i sabit boyutlu (1×1×B×B×B) ONNX'e aktarır ve onnxruntime ile doğrular.

  python uygulama\ortak\onnx_disa_aktar.py --model baran_P02_medicalnet --varyant resnet18 --ckpt karsilastirma\kosu_kayitlari\<ad>.pth --cikti model.onnx --boyut 128
Dinamik eksen KULLANILMAZ (3B conv + torch.cat sorunları); API tek hacim işler — `dynamic_axes` verilmez,
girdi sabit 1×1×B³'tür. torch>=2.9'da dışa aktarma `onnxscript` paketini ister (requirements'ta); yoksa
eski TorchScript aktarıcısına düşülür.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import torch

# Windows konsolu Türkçe kod sayfasında (cp1254) açılır; '→', '±', '≈', '≥', '█' gibi karakterler
# UnicodeEncodeError atıp betiği çökertir. Konsolun kendi kodlamasını koruyup kodlanamayan karakteri
# '?' ile değiştiriyoruz (Türkçe harfler doğru görünmeye devam eder). UTF-8 konsolda hiçbir şey değişmez.
for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:  # eski Python, yönlendirilmiş akış ya da reconfigure'ü olmayan sarmalayıcı
        pass

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
from uygulama.ortak.egit import ckpt_yukle, model_olustur  # noqa: E402


def disa_aktar(model_klasor: str, varyant: str, ckpt: str, cikti: str, boyut: int = 128, opset: int = 17) -> dict:
    d = ckpt_yukle(ckpt, torch.device("cpu"))
    gorev = d.get("gorev", "ikili"); k = 2 if gorev == "ikili" else 3
    model = model_olustur(model_klasor, varyant, k, boyut, agirlik=None)
    model.load_state_dict(d["model"]); model.eval()
    ornek = torch.zeros(1, 1, boyut, boyut, boyut)
    ortak = dict(opset_version=opset, input_names=["hacim"], output_names=["logit"], do_constant_folding=True)
    try:   # torch>=2.9: dynamo tabanlı aktarıcı (onnxscript gerekir)
        torch.onnx.export(model, ornek, cikti, **ortak)
    except Exception as e:
        print(f"UYARI yeni (dynamo) ONNX aktarıcısı başarısız: {type(e).__name__}: {e}")
        print("  eski TorchScript aktarıcısına düşülüyor (dynamo=False). Kalıcı çözüm: pip install onnxscript")
        torch.onnx.export(model, ornek, cikti, dynamo=False, **ortak)
    # doğrulama
    import onnxruntime as ort
    oturum = ort.InferenceSession(cikti, providers=["CPUExecutionProvider"])
    rng = np.random.default_rng(2026); fark = []
    for _ in range(3):
        x = rng.normal(0, 1, (1, 1, boyut, boyut, boyut)).astype(np.float32)
        with torch.no_grad():
            ref = model(torch.from_numpy(x)).numpy()
        out = oturum.run(None, {"hacim": x})[0]
        fark.append(float(np.abs(ref - out).max()))
    rapor = {"onnx": cikti, "gorev": gorev, "boyut": boyut, "opset": opset, "max_fark": max(fark),
             "uyum": max(fark) < 1e-3, "boyut_mb": round(Path(cikti).stat().st_size / 2**20, 1)}
    print(rapor)
    return rapor


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--model", required=True); p.add_argument("--varyant", default="varsayilan")
    p.add_argument("--ckpt", required=True); p.add_argument("--cikti", default="model.onnx"); p.add_argument("--boyut", type=int, default=128)
    a = p.parse_args(); disa_aktar(a.model, a.varyant, a.ckpt, a.cikti, a.boyut)
