# -*- coding: utf-8 -*-
r"""
vram_olc.py — Hangi model, hangi girdi boyutunda, hangi batch'te bu karta SIĞIYOR? Tahmin değil, ölçüm.

Neden gerekli: `KURULUM.md §0b` tablosundaki değerler tahmindi ("ResNet-18 128³ sığmaz, tahmini 8–12 GB").
Yanlış tahminle 5 kat × 3 tohum başlatıp üçüncü saatte OOM almak pahalı. Bu betik her kombinasyonu bir
ileri + bir geri geçişle gerçekten dener, tepe VRAM'i okur ve sığmayanı `OOM` diye işaretler.

CPU'da da koşar (o zaman VRAM yerine yalnız "çalıştı mı" bilgisi verir).

Kullanım (proje kökünden):
  python uygulama\ortak\vram_olc.py                                   # varsayılan tarama
  python uygulama\ortak\vram_olc.py --boyutlar 96 128 --batchlar 1 2 4
  python uygulama\ortak\vram_olc.py --modeller ortak:sigcnn baran_P01_korolev:resnet --md
`--md` çıktıyı Markdown tablosu olarak basar; doğrudan KURULUM.md'ye yapıştırılabilir.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:
        pass

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
from uygulama.ortak import egit  # noqa: E402

VARSAYILAN_MODELLER = [
    "ortak:sigcnn",
    "baran_P01_korolev:voxcnn",
    "baran_P01_korolev:resnet",
    "baran_P02_medicalnet:resnet18",
]


def bir_olc(model_klasor: str, varyant: str, boyut: int, batch: int, cihaz: torch.device,
            amp: bool = True) -> dict:
    """Tek kombinasyon: ileri + geri geçiş. Döner: {durum, vram_gb, parametre}."""
    sonuc = {"model": f"{model_klasor}:{varyant}", "boyut": boyut, "batch": batch}
    try:
        if cihaz.type == "cuda":
            torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
        model = egit.model_olustur(model_klasor, varyant, 2, boyut, agirlik=None).to(cihaz)
        sonuc["parametre_M"] = round(sum(p.numel() for p in model.parameters()) / 1e6, 2)
        opt = torch.optim.AdamW(model.parameters(), lr=1e-4)
        scaler = egit.grad_scaler(amp and cihaz.type == "cuda")
        x = torch.randn(batch, 1, boyut, boyut, boyut, device=cihaz)
        y = torch.randint(0, 2, (batch,), device=cihaz)
        model.train()
        with torch.autocast(device_type=cihaz.type, enabled=(amp and cihaz.type == "cuda")):
            kayip = torch.nn.functional.cross_entropy(model(x), y)
        scaler.scale(kayip).backward()
        scaler.step(opt); scaler.update()
        sonuc["durum"] = "OK"
        sonuc["vram_gb"] = round(torch.cuda.max_memory_allocated() / 2**30, 2) if cihaz.type == "cuda" else 0.0
    except torch.cuda.OutOfMemoryError:
        sonuc["durum"] = "OOM"; sonuc["vram_gb"] = None
    except Exception as e:
        sonuc["durum"] = f"HATA: {type(e).__name__}"; sonuc["vram_gb"] = None
        sonuc["detay"] = str(e).splitlines()[0][:90]
    finally:
        for ad in ("model", "opt", "x", "y", "kayip"):
            if ad in dir():
                pass
        if cihaz.type == "cuda":
            torch.cuda.empty_cache()
    return sonuc


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modeller", nargs="*", default=VARSAYILAN_MODELLER, help="klasor:varyant")
    p.add_argument("--boyutlar", type=int, nargs="*", default=[96, 128])
    p.add_argument("--batchlar", type=int, nargs="*", default=[1, 2, 4])
    p.add_argument("--amp", type=int, default=1)
    p.add_argument("--md", action="store_true", help="Markdown tablosu bas")
    a = p.parse_args(argv)

    cihaz = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if cihaz.type == "cuda":
        ad = torch.cuda.get_device_name(0)
        top = torch.cuda.get_device_properties(0).total_memory / 2**30
        print(f"cihaz: {ad} · {top:.1f} GB VRAM · torch {torch.__version__} · AMP={bool(a.amp)}\n")
    else:
        print(f"cihaz: CPU (VRAM ölçülemez, yalnız çalışıp çalışmadığı görülür) · torch {torch.__version__}\n")

    sonuclar = []
    for m in a.modeller:
        klasor, _, varyant = m.partition(":")
        for boyut in a.boyutlar:
            for batch in a.batchlar:
                s = bir_olc(klasor, varyant or "varsayilan", boyut, batch, cihaz, bool(a.amp))
                sonuclar.append(s)
                vram = f"{s['vram_gb']:.2f} GB" if s.get("vram_gb") else "-"
                print(f"  {s['model']:34s} {boyut}³ batch {batch}: {s['durum']:14s} {vram}"
                      + (f"  {s.get('detay','')}" if "HATA" in s["durum"] else ""))

    if a.md:
        print("\n| Model | Girdi | Batch | Durum | Tepe VRAM | Parametre |")
        print("|---|---|---|---|---|---|")
        for s in sonuclar:
            vram = f"{s['vram_gb']:.2f} GB" if s.get("vram_gb") else "—"
            isaret = "✅" if s["durum"] == "OK" else ("❌" if s["durum"] == "OOM" else "⚠")
            print(f"| `{s['model']}` | {s['boyut']}³ | {s['batch']} | {isaret} {s['durum']} | {vram} "
                  f"| {s.get('parametre_M','—')}M |")

    olan = [s for s in sonuclar if s["durum"] == "OK"]
    print(f"\n{len(olan)}/{len(sonuclar)} kombinasyon sığdı.")
    if cihaz.type == "cuda" and olan:
        en_buyuk = max(olan, key=lambda s: (s["boyut"], s["batch"]))
        print(f"Bu kartta en büyük çalışan ayar: {en_buyuk['model']} {en_buyuk['boyut']}³ batch {en_buyuk['batch']}")
        print("PROTOKOL madde 3: tabloya giren koşular herkeste AYNI boyutta olmalı — sığmayan model varsa "
              "ya herkes küçültür ya o model Kaggle/Colab'da koşar (KOSU-PLANI.md).")


if __name__ == "__main__":
    main()
