# -*- coding: utf-8 -*-
r"""
saglik_testi.py — PROTOKOL "K5 Sağlık testleri": hat, gerçek veri olmadan uçtan uca koşturulur.

Neyi kanıtlar:
  (a) Rastgele etiket  → doğrulama BAcc ≈ 0.5   (hat etiketten bağımsız sinyal uydurmuyor, sızıntı yok)
  (b) Ayrılabilir iki sınıf → doğrulama BAcc ≈ 1.0 (hat gerçekten öğrenebiliyor, kayıp/optimizer doğru bağlı)
  (c) Bölme kesişimi boş (`bolme.dogrula`)
  (d) Koşu kaydı PROTOKOL madde 10 alanlarını taşıyor ve farklı LR'ler birbirinin kaydını ezmiyor

Bu test ön işleme hattını değil **eğitim hattını** denetler: bolme → veri → egit → metrikler → JSON zinciri
gerçekten çalışıyor mu? Veri, GPU, ağırlık, internet gerekmez; sentetik hacimler üretilir.

Koş (proje kökünden, CPU'da ~1–3 dk):
  python uygulama\ortak\saglik_testi.py
  python uygulama\ortak\saglik_testi.py --denek 96 --boyut 32 --epoch 10 --model ortak --varyant sigcnn
  python uygulama\ortak\saglik_testi.py --tut cikti\saglik    # ara dosyaları sakla (inceleme için)

Beklenen: her satırda OK, sonda "TÜM SAĞLIK TESTLERİ OK".
"""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

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
from uygulama.ortak import bolme, egit  # noqa: E402

HATA: list[str] = []


def ok(ad: str, kosul: bool, detay: str = "") -> None:
    print(f"{'OK  ' if kosul else 'HATA'} {ad} {detay}")
    if not kosul:
        HATA.append(ad)


# ----------------------------------------------------------------------------- sentetik veri
def sentetik_uret(klasor: Path, denek: int, boyut: int, tohum: int = 2026) -> pd.DataFrame:
    """Yarısı NC (0), yarısı AD (2). AD hacimlerinde belirgin bölgesel sinyal kaybı ('atrofi' imzası)."""
    klasor.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(tohum)
    z, y, x = np.indices((boyut,) * 3).astype(np.float32)
    c = boyut / 2.0
    beyin = (np.sqrt((z - c) ** 2 + (y - c) ** 2 + (x - c) ** 2) < boyut * 0.42).astype(np.float32)
    sigma = boyut * 0.10
    imza = np.exp(-((z - c * 0.72) ** 2 + (y - c) ** 2 + (x - c * 1.28) ** 2) / (2 * sigma ** 2))
    satirlar = []
    for i in range(denek):
        sinif = 0 if i % 2 == 0 else 2
        arr = beyin * (1.0 + 0.15 * rng.normal(0, 1, (boyut,) * 3).astype(np.float32))
        if sinif == 2:
            arr = arr - 2.5 * imza * beyin
        ad = f"S{i:03d}"
        np.save(klasor / f"{ad}.npy", arr.astype(np.float16))
        satirlar.append({"denek_id": ad, "dosya": f"{ad}.npy", "sinif": sinif, "yas": 70, "cinsiyet": "F"})
    return pd.DataFrame(satirlar)


def etiket_karistir(df: pd.DataFrame, tohum: int = 7) -> pd.DataFrame:
    """Aynı hacimler, etiketler karıştırılmış: hacim ↔ etiket bağı kopar, sınıf dengesi korunur."""
    k = df.copy()
    k["sinif"] = np.random.default_rng(tohum).permutation(k["sinif"].to_numpy())
    return k


# ----------------------------------------------------------------------------- tek koşu
def kos(etiket_df: pd.DataFrame, set_adi: str, veri_dir: Path, calisma: Path, a) -> tuple[dict, bool]:
    etiket_csv = calisma / f"{set_adi}_etiket.csv"
    etiket_df.to_csv(etiket_csv, index=False)
    bolme_dir = calisma / "bolme"
    print(f"\n--- {set_adi}: bölme ---")
    bolme.bol(etiket_csv, set_adi, bolme_dir, test_oran=0.2, kat=a.kat_sayisi, tohum=a.tohum)
    temiz = bolme.dogrula(set_adi, bolme_dir)
    print(f"--- {set_adi}: eğitim ({a.epoch} epoch, {a.boyut}³) ---")
    sonuc = egit.egit(a.model, a.varyant, set_adi, "ikili", 0, a.tohum, str(veri_dir),
                      bolme_klasor=str(bolme_dir), cikti_klasor=str(calisma / "kayitlar"),
                      epoch=a.epoch, batch=a.batch, boyut=a.boyut, isci=a.isci, amp=False,
                      sabir=a.epoch, lr=a.lr)
    return sonuc, temiz


# ----------------------------------------------------------------------------- ana
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--denek", type=int, default=64, help="sentetik denek sayısı (yarısı NC, yarısı AD)")
    p.add_argument("--boyut", type=int, default=32)
    p.add_argument("--epoch", type=int, default=8)
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--isci", type=int, default=0, help="DataLoader işçisi (Windows'ta 0 daha hızlı başlar)")
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--kat_sayisi", type=int, default=3)
    p.add_argument("--tohum", type=int, default=2026)
    p.add_argument("--model", default="ortak", help="model klasörü (varsayılan: ortak = SigCNN3D temel çizgisi)")
    p.add_argument("--varyant", default="sigcnn")
    p.add_argument("--tut", default=None, help="ara dosyaları bu klasörde sakla (varsayılan: geçici, silinir)")
    a = p.parse_args(argv)

    gecici = None
    if a.tut:
        calisma = Path(a.tut).resolve(); calisma.mkdir(parents=True, exist_ok=True)
    else:
        gecici = tempfile.mkdtemp(prefix="saglik_"); calisma = Path(gecici)
    print(f"çalışma klasörü: {calisma}")

    try:
        veri_dir = calisma / "hacimler"
        gercek = sentetik_uret(veri_dir, a.denek, a.boyut, a.tohum)
        ok("sentetik veri", len(gercek) == a.denek and len(list(veri_dir.glob('*.npy'))) == a.denek,
           f"{a.denek} denek, {a.boyut}³")

        # (b) ayrılabilir iki sınıf → öğrenmeli
        s_ayri, temiz_ayri = kos(gercek, "saglik_ayrilabilir", veri_dir, calisma, a)
        # (a) rastgele etiket → öğrenmemeli
        s_rast, temiz_rast = kos(etiket_karistir(gercek, a.tohum + 1), "saglik_rastgele", veri_dir, calisma, a)

        b_ayri = s_ayri["dogrulama"]["bacc"]
        b_rast = s_rast["dogrulama"]["bacc"]
        print()
        ok("(c) bölme kesişimi yok (ayrılabilir)", temiz_ayri)
        ok("(c) bölme kesişimi yok (rastgele)", temiz_rast)
        ok("(b) ayrılabilir iki sınıf → BAcc ≈ 1.0", b_ayri >= 0.85, f"BAcc={b_ayri:.3f} (eşik 0.85)")
        ok("(a) rastgele etiket → BAcc ≈ 0.5", 0.25 <= b_rast <= 0.75, f"BAcc={b_rast:.3f} (bant 0.25–0.75)")
        ok("(a) rastgele, ayrılabilirden belirgin düşük", b_rast < b_ayri - 0.10,
           f"{b_rast:.3f} < {b_ayri:.3f} - 0.10")

        # (d) PROTOKOL madde 10 kayıt alanları
        gerekli = {"ad", "lr", "boyut", "etiket", "model_notu", "ayar", "parametre", "cihaz", "gpu",
                   "sure_sn", "epoch_kosulan", "en_iyi_epoch", "dogrulama", "test", "commit", "torch"}
        eksik = gerekli - set(s_ayri)
        ok("(d) koşu kaydı madde 10 alanları", not eksik, f"eksik={sorted(eksik) or '-'}")
        ok("(d) koşu adı lr ve boyut taşıyor", "_lr" in s_ayri["ad"] and f"_b{a.boyut}" in s_ayri["ad"],
           s_ayri["ad"])

        # (d) LR taraması çakışma regresyonu: aynı kat/tohum, farklı LR → iki ayrı kayıt
        print("\n--- LR çakışma regresyon testi (2 kısa koşu) ---")
        kisa = argparse.Namespace(**{**vars(a), "epoch": 2})
        bolme_dir = calisma / "bolme"
        kayitlar = calisma / "kayitlar"
        s1 = egit.egit(a.model, a.varyant, "saglik_ayrilabilir", "ikili", 1, a.tohum, str(veri_dir),
                       bolme_klasor=str(bolme_dir), cikti_klasor=str(kayitlar), epoch=2, batch=a.batch,
                       boyut=a.boyut, isci=a.isci, amp=False, sabir=2, lr=1e-3)
        s2 = egit.egit(a.model, a.varyant, "saglik_ayrilabilir", "ikili", 1, a.tohum, str(veri_dir),
                       bolme_klasor=str(bolme_dir), cikti_klasor=str(kayitlar), epoch=2, batch=a.batch,
                       boyut=a.boyut, isci=a.isci, amp=False, sabir=2, lr=3e-4)
        ok("(d) farklı LR → farklı koşu adı", s1["ad"] != s2["ad"], f"{s1['ad'][-18:]} vs {s2['ad'][-18:]}")
        ok("(d) farklı LR → iki ayrı JSON kaydı",
           (kayitlar / f"{s1['ad']}.json").exists() and (kayitlar / f"{s2['ad']}.json").exists())
        ok("(d) bitmiş koşuda devam dosyası silindi", not (kayitlar / f"{s1['ad']}_son.pth").exists())
        del kisa
    finally:
        if gecici:
            shutil.rmtree(gecici, ignore_errors=True)

    print("\nTÜM SAĞLIK TESTLERİ OK" if not HATA else f"\nHATALI: {HATA}")
    raise SystemExit(0 if not HATA else 1)


if __name__ == "__main__":
    main()
