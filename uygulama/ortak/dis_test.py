# -*- coding: utf-8 -*-
r"""
dis_test.py — PROTOKOL "Dış test": bir veri setinde eğitilmiş modelin BAŞKA sette sıfır-atış (zero-shot) sonucu.

PROTOKOL: "ADNI1'de eğitilen her modelin ikili görevde OASIS-1 (≥60 yaş) üzerinde sıfır-atış sonucu ayrı
sütunda raporlanır. Genelleme düşüşü (iç − dış) tartışma bölümünün ana konusudur."

Burada eğitim YOKTUR: checkpoint olduğu gibi yüklenir, hedef setin TÜM denekleri bir kez değerlendirilir
(hedef sette bölme yapılmaz — hiçbir parçası eğitimde kullanılmadığı için tamamı test setidir).
K4 (transfer sızıntısı) kontrolü: kaynak setin denek kimlikleri hedef sette görünüyorsa iş durur.

Çıktı: `karsilastirma/dis_test/<kosu_adi>_dis-<set>.json` — `tablo_uret.py` bunu "Dış test BAcc" sütununa koyar.

Koş (proje kökünden):
  python uygulama\ortak\dis_test.py --model baran_P02_medicalnet --ckpt karsilastirma\kosu_kayitlari\<ad>.pth ^
      --dis_set oasis1 --etiket veri\oasis1_etiket.csv --veri D:\veri\oasis1\islenmis
  python uygulama\ortak\dis_test.py --model baran_P01_korolev --tum_ckpt "*adni1_ikili*" ^
      --dis_set oasis1 --etiket veri\oasis1_etiket.csv --veri D:\veri\oasis1\islenmis
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

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

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
from uygulama.ortak import egit, veri  # noqa: E402


def kosu_adi(ckpt: Path) -> str:
    ad = ckpt.stem
    return ad[:-4] if ad.endswith("_son") else ad


def tek_dis_test(model_klasor: str, ckpt: Path, dis_set: str, etiket_csv: Path, veri_kok: str,
                 varyant: str | None = None, batch: int = 4, isci: int = 2, amp: bool = True,
                 cikti_klasor: Path | None = None, kaynak_denekler: set[str] | None = None) -> dict:
    d = egit.ckpt_yukle(ckpt, torch.device("cpu"))
    gorev = d.get("gorev", "ikili")
    ayar = d.get("ayar", {})
    boyut = int(ayar.get("boyut", 128))
    v = varyant or d.get("varyant", "varsayilan")
    cihaz = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    df = pd.read_csv(etiket_csv)
    gerekli = {"denek_id", "dosya", "sinif"}
    if not gerekli <= set(df.columns):
        raise SystemExit(f"{etiket_csv}: {sorted(gerekli - set(df.columns))} sütunları eksik "
                         f"(bolme.py etiket-oasis / etiket-adni ile üret)")
    if kaynak_denekler:
        kesisim = kaynak_denekler & set(df["denek_id"].astype(str))
        if kesisim:
            raise SystemExit(f"K4 TRANSFER SIZINTISI: kaynak setin {len(kesisim)} deneği hedef sette de var "
                             f"(ör. {sorted(kesisim)[:5]}). Dış test geçersiz.")

    model = egit.model_olustur(model_klasor, v, veri.sinif_sayisi(gorev), boyut, agirlik=None)
    model.load_state_dict(d["model"])
    model = model.to(cihaz)

    yl = veri.yukleyici(df, veri_kok, gorev, False, batch, isci=isci, boyut=boyut, tohum=2026)
    n = len(yl.dataset)
    if n == 0:
        raise SystemExit(f"{etiket_csv}: '{gorev}' görevi için değerlendirilecek denek yok")
    m = egit.degerlendir(model, yl, cihaz, gorev, amp)

    sonuc = {"ad": kosu_adi(ckpt), "dis_set": dis_set, "gorev": gorev, "model": model_klasor, "varyant": v,
             "boyut": boyut, "n": n, "sifir_atis": True, "kaynak_ckpt": str(ckpt),
             "en_iyi_epoch": d.get("en_iyi_epoch"), "cihaz": str(cihaz), "metrik": m}

    cikti_klasor = cikti_klasor or (KOK / "karsilastirma" / "dis_test")
    cikti_klasor.mkdir(parents=True, exist_ok=True)
    yol = cikti_klasor / f"{sonuc['ad']}_dis-{dis_set}.json"
    yol.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"DIŞ TEST {sonuc['ad']} → {dis_set}: n={n} BAcc {m['bacc']:.3f} AUC {m['auc']:.3f} "
          f"F1 {m['f1_makro']:.3f} → {yol.name}")
    return sonuc


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", required=True, help="model klasörü (uygulama/<klasor>/model.py)")
    p.add_argument("--varyant", default=None, help="boş bırakılırsa checkpoint'ten okunur")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--ckpt", help="tek checkpoint (.pth)")
    g.add_argument("--tum_ckpt", help="kosu_kayitlari içinde glob deseni, ör. \"*adni1_ikili*\"")
    p.add_argument("--dis_set", required=True, help="hedef setin adı (ör. oasis1)")
    p.add_argument("--etiket", required=True, help="hedef setin etiket CSV'si (denek_id, dosya, sinif)")
    p.add_argument("--veri", required=True, help="hedef setin işlenmiş .npy klasörü")
    p.add_argument("--kaynak_etiket", default=None, help="kaynak setin etiket CSV'si (K4 sızıntı kontrolü)")
    p.add_argument("--kayitlar", default="karsilastirma/kosu_kayitlari")
    p.add_argument("--batch", type=int, default=4)
    p.add_argument("--isci", type=int, default=2)
    p.add_argument("--amp", type=int, default=1)
    p.add_argument("--cikti", default=None, help="dış test kaydı klasörü (varsayılan karsilastirma/dis_test)")
    a = p.parse_args(argv)

    kaynak = None
    if a.kaynak_etiket:
        kaynak = set(pd.read_csv(a.kaynak_etiket)["denek_id"].astype(str))
        print(f"K4 kontrolü için kaynak setten {len(kaynak)} denek kimliği okundu")

    if a.ckpt:
        ckptler = [Path(a.ckpt)]
    else:
        klasor = (KOK / a.kayitlar) if not Path(a.kayitlar).is_absolute() else Path(a.kayitlar)
        ckptler = sorted(f for f in klasor.glob(f"{a.tum_ckpt}.pth") if not f.stem.endswith("_son"))
        if not ckptler:
            raise SystemExit(f"desen eşleşmedi: {klasor / (a.tum_ckpt + '.pth')}")
        print(f"{len(ckptler)} checkpoint bulundu")

    sonuclar = []
    for c in ckptler:
        if not c.exists():
            raise SystemExit(f"checkpoint yok: {c}")
        sonuclar.append(tek_dis_test(a.model, c, a.dis_set, Path(a.etiket), a.veri, a.varyant,
                                     a.batch, a.isci, bool(a.amp),
                                     cikti_klasor=Path(a.cikti) if a.cikti else None,
                                     kaynak_denekler=kaynak))

    if len(sonuclar) > 1:
        import numpy as np
        b = np.array([s["metrik"]["bacc"] for s in sonuclar], dtype=float)
        print(f"\n{len(sonuclar)} koşu ortalaması → dış test BAcc {b.mean():.3f}±{b.std():.3f} "
              f"({a.dis_set}); satıra `tablo_uret.py` koyar")


if __name__ == "__main__":
    main()
