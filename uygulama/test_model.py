# -*- coding: utf-8 -*-
r"""
test_model.py — Duman testi: modeller 32³ rastgele hacimle ileri/geri geçer mi, Dataset ve metrikler çalışır mı?
Koş (proje kökünden): python uygulama\test_model.py
Veri, GPU, ağırlık, internet gerekmez. Beklenen: her satır OK, sonda "TÜM TESTLER OK".
"""
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import torch

# Windows konsolu Türkçe kod sayfasında (cp1254) açılır; '→', '±', '≈', '≥', '█' gibi karakterler
# UnicodeEncodeError atıp betiği çökertir. Konsolun kendi kodlamasını koruyup kodlanamayan karakteri
# '?' ile değiştiriyoruz (Türkçe harfler doğru görünmeye devam eder). UTF-8 konsolda hiçbir şey değişmez.
for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:  # eski Python, yönlendirilmiş akış ya da reconfigure'ü olmayan sarmalayıcı
        pass

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from uygulama.ortak import metrikler, veri  # noqa: E402

B = 32
HATA = []


def ok(ad, kosul, detay=""):
    print(f"{'OK  ' if kosul else 'HATA'} {ad} {detay}")
    if not kosul:
        HATA.append(ad)


def ileri_geri(ad, model, sinif):
    x = torch.randn(2, 1, B, B, B); y = torch.tensor([0, sinif - 1])
    model.train(); out = model(x)
    ok(f"{ad} çıktı şekli", tuple(out.shape) == (2, sinif), str(tuple(out.shape)))
    loss = torch.nn.functional.cross_entropy(out, y); loss.backward()
    grad = sum(p.grad.abs().sum().item() for p in model.parameters() if p.grad is not None)
    ok(f"{ad} geri yayılım", np.isfinite(loss.item()) and grad > 0, f"kayıp={loss.item():.3f} param={sum(p.numel() for p in model.parameters())/1e6:.2f}M")


def main():
    # --- modeller
    from uygulama.baran_P01_korolev.model import olustur as p01
    ileri_geri("P01 VoxCNN", p01("voxcnn", 2, B), 2)   # B=32 → otomatik padding=1 (uyarı basar, normal)
    ileri_geri("P01 VoxResNet", p01("resnet", 3, B), 3)
    # PROTOKOL madde 3: tabloya giren koşu 128³ + valid konvolüsyon — o kurulum da ayağa kalkmalı
    m128 = p01("voxcnn", 2, 128).eval()
    with torch.no_grad():
        o128 = m128(torch.zeros(1, 1, 128, 128, 128))
    ok("P01 VoxCNN 128³ valid (tablo ayarı)", tuple(o128.shape) == (1, 2) and m128.padding == 0, f"padding={m128.padding}")
    from uygulama.ortak.temel_cizgi import olustur as tc
    ileri_geri("Temel SigCNN3D", tc("sigcnn", 2, B), 2)
    try:
        from uygulama.baran_P02_medicalnet.model import olustur as p02
        ileri_geri("P02 MONAI ResNet-18 (ağırlıksız)", p02("resnet18", 2, B), 2)
        from monai.networks.nets import DenseNet121
        ileri_geri("P12 MONAI DenseNet121", DenseNet121(spatial_dims=3, in_channels=1, out_channels=3), 3)
    except ImportError as e:
        print(f"ATLA MONAI yok ({e}) — pip install monai")
    # Diğer ekip üyelerinin model.py'leri yazıldıkça otomatik denenir (olustur(varyant='varsayilan', ...) sözleşmesi)
    import importlib
    for klasor in sorted(p.name for p in (KOK / "uygulama").iterdir() if (p / "model.py").exists()):
        if klasor.startswith(("baran_", "ortak")):
            continue
        try:
            mod = importlib.import_module(f"uygulama.{klasor}.model")
            ileri_geri(f"{klasor} (varsayılan varyant)", mod.olustur("varsayilan", 2, B), 2)
        except Exception as e:  # eksik bağımlılık / henüz yazılmamış sözleşme testi durdurmasın
            print(f"ATLA {klasor}: {type(e).__name__}: {e}")

    # --- Dataset + metrikler (sentetik npy)
    with tempfile.TemporaryDirectory() as td:
        satirlar = []
        rng = np.random.default_rng(0)
        for i in range(12):
            np.save(Path(td) / f"D{i}.npy", rng.normal(0, 1, (B, B, B)).astype(np.float16))
            satirlar.append({"denek_id": f"D{i}", "dosya": f"D{i}.npy", "sinif": i % 3})
        df = pd.DataFrame(satirlar)
        ds = veri.HacimVeriSeti(df, td, "ikili", egitim=True, boyut=B)
        x, y, kim = ds[0]
        ok("Dataset ikili filtre", len(ds) == 8 and tuple(x.shape) == (1, B, B, B), f"n={len(ds)} şekil={tuple(x.shape)}")
        ok("Sınıf ağırlıkları", ds.sinif_agirliklari().shape[0] == 2)
        ds3 = veri.HacimVeriSeti(df, td, "uc", egitim=False, boyut=B)
        ok("Dataset üç sınıf", len(ds3) == 12 and max(ds3.etiketler()) == 2)
        yl = veri.yukleyici(df, td, "uc", False, batch=4, isci=0, boyut=B)
        xb, yb, _ = next(iter(yl)); ok("DataLoader", tuple(xb.shape) == (4, 1, B, B, B))

    y_true = np.array([0, 0, 1, 1, 1, 0]); y_prob = np.array([[.9, .1], [.6, .4], [.2, .8], [.4, .6], [.7, .3], [.8, .2]])
    m = metrikler.hesapla(y_true, y_prob, "ikili")
    ok("Metrik ikili", abs(m["bacc"] - (2 / 3 + 1) / 2) < 1e-9 and 0 < m["auc"] <= 1, f"bacc={m['bacc']:.3f} auc={m['auc']:.3f}")
    y3 = np.array([0, 1, 2, 0, 1, 2]); p3 = np.eye(3)[y3] * 0.8 + 0.1
    m3 = metrikler.hesapla(y3, p3, "uc"); ok("Metrik üç sınıf", m3["bacc"] == 1.0 and len(m3["cm"]) == 3)
    print(metrikler.satir("test", "ikili", "hayır", metrikler.ozet([m, m])))

    print("TÜM TESTLER OK" if not HATA else f"HATALI: {HATA}")
    raise SystemExit(0 if not HATA else 1)


if __name__ == "__main__":
    main()
