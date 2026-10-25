# -*- coding: utf-8 -*-
r"""
svm_kos.py — PROTOKOL madde 9(b) temel çizgisi: voksel tabanlı lineer SVM (Wen 2020).

Neden var: Wen 2020'de doğrusal SVM, ADNI testinde 0.88 dengeli doğrulukla birçok 3B CNN'i geçiyor. PROTOKOL
madde 9 "karmaşık modeller bunu geçmiyorsa raporda açıkça yazılır" diyor — ama SVM'in epoch'lu eğitimi
olmadığı için `egit.py` ile koşulamaz. Bu betik aynı bölmeyi, aynı metrikleri ve `egit.py` ile AYNI JSON
şemasını kullanarak SVM satırını üretir, böylece `tablo_uret.py` onu diğer modellerle aynı tabloya koyar.

Sızıntı: ölçekleyici (StandardScaler) ve SVM yalnız eğitim katında fit edilir (madde 2 / K1); doğrulama ve
test aynı dönüşümle yalnızca dönüştürülür. C taraması doğrulama BAcc'ine göre yapılır, test'e bakılmaz (K2).

Hacimler 32³'e indirgenir (Wen 2020 voksel özniteliği); 128³ ham voksel (2M öznitelik) lineer SVM için
gereksiz ağır ve bellek dostu değil.

Koş (proje kökünden):
  python uygulama\ortak\svm_kos.py --set oasis1 --gorev ikili --kat 0 --tohum 2026 --veri D:\veri\oasis1\islenmis
  python uygulama\ortak\svm_kos.py --set adni1 --gorev ikili --tum_katlar --Cler 0.01 1 100 --veri D:\veri\adni1\islenmis
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

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
from uygulama.ortak import egit, metrikler, temel_cizgi, veri  # noqa: E402

MODEL_ADI = "temel_svm"
VARYANT = "voksel-lineer"


def yigin_yukle(df, veri_kok: str, gorev: str, boyut: int) -> tuple[np.ndarray, np.ndarray]:
    """Hacimleri boyut³'e indirgeyerek belleğe alır (32³ float32 ≈ 131 KB/denek)."""
    ds = veri.HacimVeriSeti(df, veri_kok, gorev, egitim=False, boyut=boyut)
    if len(ds) == 0:
        raise SystemExit(f"'{gorev}' görevi için denek yok")
    X = np.empty((len(ds), boyut, boyut, boyut), dtype=np.float32)
    y = np.empty(len(ds), dtype=np.int64)
    for i in range(len(ds)):
        x, etiket, _ = ds[i]
        X[i] = x[0].numpy()
        y[i] = etiket
    return X, y


def kos(set_adi: str, gorev: str, kat: int, tohum: int, veri_kok: str, C: float, boyut: int = 32,
        bolme_klasor: str = "veri/bolme", cikti_klasor: str = "karsilastirma/kosu_kayitlari") -> dict:
    t0 = time.time()
    bolme_yolu = (KOK / bolme_klasor) if not Path(bolme_klasor).is_absolute() else Path(bolme_klasor)
    egitim_df, dogrulama_df = veri.kat_oku(bolme_yolu, set_adi, kat)
    test_df = veri.test_oku(bolme_yolu, set_adi)

    X_tr, y_tr = yigin_yukle(egitim_df, veri_kok, gorev, boyut)
    X_va, y_va = yigin_yukle(dogrulama_df, veri_kok, gorev, boyut)
    X_te, y_te = yigin_yukle(test_df, veri_kok, gorev, boyut)
    print(f"[{set_adi} k{kat} C={C:g}] eğitim {len(y_tr)} / doğrulama {len(y_va)} / test {len(y_te)} denek, {boyut}³")

    # Tek fit: ölçekleyici + SVM yalnız eğitim katında; doğrulama ve test birlikte dönüştürülüp tahmin edilir.
    p_hepsi = temel_cizgi.svm_kosu(X_tr, y_tr, np.concatenate([X_va, X_te]), boyut=boyut, C=C)
    p_va, p_te = p_hepsi[:len(y_va)], p_hepsi[len(y_va):]
    m_va = metrikler.hesapla(y_va, p_va, gorev)
    m_te = metrikler.hesapla(y_te, p_te, gorev)

    ad = f"{MODEL_ADI}-{VARYANT}_{set_adi}_{gorev}_t{tohum}_k{kat}_C{C:g}_b{boyut}"
    cikti = (KOK / cikti_klasor) if not Path(cikti_klasor).is_absolute() else Path(cikti_klasor)
    cikti.mkdir(parents=True, exist_ok=True)
    sonuc = {
        "ad": ad, "model": MODEL_ADI, "varyant": VARYANT, "set": set_adi, "gorev": gorev, "kat": kat,
        "tohum": tohum, "tarama": float(C), "lr": 0.0, "svm_C": float(C), "boyut": boyut, "etiket": "",
        "model_notu": f"voksel tabanlı lineer SVM (C={C:g}, {boyut}³ öznitelik); taranan hiperparametre C",
        "on_egitim": False, "agirlik": None,
        "ayar": {"C": float(C), "boyut": boyut, "max_iter": 5000, "class_weight": "balanced"},
        "parametre": int(boyut ** 3), "cihaz": "cpu", "gpu": "cpu", "vram_gb": 0.0,
        "sure_sn": round(time.time() - t0, 1), "epoch_kosulan": 0, "en_iyi_epoch": -1,
        "dogrulama": m_va, "test": m_te, "commit": egit.commit_hash(), "torch": "—(sklearn)",
    }
    (cikti / f"{ad}.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"BİTTİ {ad}: doğrulama BAcc {m_va['bacc']:.3f} | test BAcc {m_te['bacc']:.3f} AUC {m_te['auc']:.3f}")
    return sonuc


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--set", required=True)
    p.add_argument("--gorev", choices=["ikili", "uc"], default="ikili")
    p.add_argument("--kat", type=int, default=0)
    p.add_argument("--tum_katlar", action="store_true")
    p.add_argument("--tohum", type=int, default=2026, help="SVM deterministik; tohum yalnız kayıt adı için")
    p.add_argument("--veri", required=True)
    p.add_argument("--bolme", default="veri/bolme")
    p.add_argument("--boyut", type=int, default=32, help="voksel özniteliği için indirgeme kenarı")
    p.add_argument("--C", type=float, default=1.0)
    p.add_argument("--Cler", type=float, nargs="*", help="C taraması (ör. 0.01 1 100); her C kendi kaydına yazılır")
    p.add_argument("--cikti", default="karsilastirma/kosu_kayitlari", help="koşu kaydı klasörü")
    a = p.parse_args(argv)

    katlar = range(5) if a.tum_katlar else [a.kat]
    Cler = a.Cler or [a.C]
    sonuclar = [kos(a.set, a.gorev, k, a.tohum, a.veri, C, a.boyut, a.bolme, a.cikti)
                for C in Cler for k in katlar]
    if len(sonuclar) > 1:
        b = np.array([s["test"]["bacc"] for s in sonuclar])
        print(f"\n{len(sonuclar)} koşu: test BAcc {b.mean():.3f}±{b.std():.3f} "
              f"— satırı `tablo_uret.py` üretir (C seçimi doğrulama üstünden)")


if __name__ == "__main__":
    main()
