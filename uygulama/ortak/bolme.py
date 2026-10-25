# -*- coding: utf-8 -*-
r"""
bolme.py — Denek (RID / OASIS ID) düzeyinde kilitli test + 5-kat CV bölmesi (PROTOKOL madde 1–2).

1) Etiket CSV üret:
   python bolme.py etiket-adni  --adnimerge D:\veri\adni1\ADNIMERGE.csv --islenmis D:\veri\adni1\islenmis --cikti veri\adni1_etiket.csv
   python bolme.py etiket-oasis --csv D:\veri\oasis1\oasis_cross-sectional.csv --islenmis D:\veri\oasis1\islenmis --cikti veri\oasis1_etiket.csv
2) Böl:
   python bolme.py bol --etiket veri\adni1_etiket.csv --set adni1 --cikti veri\bolme --test_oran 0.15 --kat 5 --tohum 2026
3) Doğrula (sızıntı kontrolü):
   python bolme.py dogrula --set adni1 --bolme veri\bolme
Etiket CSV sütunları: denek_id, dosya (islenmis klasörüne göre), sinif (0 NC, 1 MCI, 2 AD), yas, cinsiyet
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold, train_test_split

# Windows konsolu Türkçe kod sayfasında (cp1254) açılır; '→', '±', '≈', '≥', '█' gibi karakterler
# UnicodeEncodeError atıp betiği çökertir. Konsolun kendi kodlamasını koruyup kodlanamayan karakteri
# '?' ile değiştiriyoruz (Türkçe harfler doğru görünmeye devam eder). UTF-8 konsolda hiçbir şey değişmez.
for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:  # eski Python, yönlendirilmiş akış ya da reconfigure'ü olmayan sarmalayıcı
        pass

DX_ADNI = {"CN": 0, "SMC": None, "EMCI": 1, "LMCI": 1, "MCI": 1, "AD": 2, "Dementia": 2}


def etiket_adni(adnimerge: Path, islenmis: Path, cikti: Path) -> pd.DataFrame:
    df = pd.read_csv(adnimerge, low_memory=False)
    bl = df[df["VISCODE"] == "bl"].copy()
    bl["sinif"] = bl["DX_bl"].map(DX_ADNI)
    bl = bl.dropna(subset=["sinif"])
    satirlar, belirsiz = [], []
    for _, r in bl.iterrows():
        rid = int(r["RID"]); ptid = str(r["PTID"])
        adaylar = sorted(Path(islenmis).glob(f"*{ptid}*.npy")) or sorted(Path(islenmis).glob(f"{rid}.npy"))
        if not adaylar:
            continue
        if len(adaylar) > 1:  # başlangıç dışı tarama karışmasın: seçim belirli (sıralı ilk) ama uyarılır
            belirsiz.append(f"RID{rid}: {[d.name for d in adaylar]}")
        satirlar.append({"denek_id": f"RID{rid}", "dosya": adaylar[0].name, "sinif": int(r["sinif"]),
                         "yas": r.get("AGE", np.nan), "cinsiyet": r.get("PTGENDER", "")})
    out = pd.DataFrame(satirlar).drop_duplicates("denek_id")
    out.to_csv(cikti, index=False)
    print(f"ADNI etiket: {len(out)} denek → {out['sinif'].value_counts().sort_index().to_dict()}  (0 NC, 1 MCI, 2 AD)")
    if belirsiz:
        print(f"UYARI {len(belirsiz)} denekte birden fazla .npy eşleşti; sıralı ilki alındı — başlangıç taraması mı, bak:")
        for s in belirsiz[:10]:
            print("  ", s)
    return out


def etiket_oasis(csv: Path, islenmis: Path, cikti: Path, min_yas: int = 60) -> pd.DataFrame:
    df = pd.read_csv(csv)
    df = df[(df["Age"] >= min_yas)].copy()
    df = df.dropna(subset=["CDR"])
    # CDR 0 → NC (0); CDR ≥ 0.5 → AD tarafı (2). Üç sınıf OASIS-1'de yapılmaz (VERI-SETI.md §3.2).
    df["sinif"] = np.where(df["CDR"] == 0, 0, 2)
    satirlar = []
    for _, r in df.iterrows():
        oid = str(r["ID"])
        adaylar = sorted(Path(islenmis).glob(f"{oid}*.npy"))
        if not adaylar:
            continue
        satirlar.append({"denek_id": oid, "dosya": adaylar[0].name, "sinif": int(r["sinif"]),
                         "yas": r["Age"], "cinsiyet": r.get("M/F", "")})
    out = pd.DataFrame(satirlar).drop_duplicates("denek_id")
    out.to_csv(cikti, index=False)
    print(f"OASIS-1 etiket (≥{min_yas} yaş): {len(out)} denek → {out['sinif'].value_counts().sort_index().to_dict()}")
    return out


def bol(etiket: Path, set_adi: str, cikti: Path, test_oran: float = 0.15, kat: int = 5, tohum: int = 2026):
    df = pd.read_csv(etiket)
    assert df["denek_id"].is_unique, "etiket CSV'de denek_id tekrarlı — her denek tek satır olmalı"
    cikti = Path(cikti); cikti.mkdir(parents=True, exist_ok=True)
    # kilitli test: denek düzeyi (her satır zaten bir denek), sınıf dengeli
    kalan, test = train_test_split(df, test_size=test_oran, stratify=df["sinif"], random_state=tohum)
    test.to_csv(cikti / f"{set_adi}_test.csv", index=False)
    sgkf = StratifiedGroupKFold(n_splits=kat, shuffle=True, random_state=tohum)
    harita = [{"denek_id": r, "bolum": "test", "kat": -1} for r in test["denek_id"]]
    for k, (egitim_idx, dogrulama_idx) in enumerate(sgkf.split(kalan, kalan["sinif"], groups=kalan["denek_id"])):
        d = kalan.copy(); d["bolum"] = "egitim"
        d.iloc[dogrulama_idx, d.columns.get_loc("bolum")] = "dogrulama"
        d.to_csv(cikti / f"{set_adi}_kat{k}.csv", index=False)
        harita += [{"denek_id": t.denek_id, "bolum": t.bolum, "kat": k} for t in d.itertuples()]
    # Paylaşılabilir bölme haritası: yalnız denek kimliği + kat/bölüm — tanı, yaş, cinsiyet YOK.
    # ADNI DUA klinik veriyi üçüncü tarafa dağıtmayı yasaklar; tekrarlanabilirlik için bölme bilgisi yeterli
    # (clinicadl de bölmeleri böyle yayımlar). Depoya giren dosya BUDUR; klinik sütunlu CSV'ler yerelde kalır.
    harita_yolu = cikti / f"{set_adi}_bolme_haritasi.csv"
    pd.DataFrame(harita).to_csv(harita_yolu, index=False)
    print(f"{set_adi}: test {len(test)} denek, CV {len(kalan)} denek, {kat} kat → {cikti}")
    print(f"  depoya girecek paylaşılabilir harita (klinik sütun yok): {harita_yolu.name}")
    dogrula(set_adi, cikti)


def dogrula(set_adi: str, bolme: Path) -> bool:
    bolme = Path(bolme)
    test = set(pd.read_csv(bolme / f"{set_adi}_test.csv")["denek_id"])
    sorun = 0
    dogrulamalar = []
    for f in sorted(bolme.glob(f"{set_adi}_kat*.csv")):
        d = pd.read_csv(f)
        e = set(d[d["bolum"] == "egitim"]["denek_id"]); v = set(d[d["bolum"] == "dogrulama"]["denek_id"])
        if e & v: print(f"HATA {f.name}: eğitim∩doğrulama = {len(e & v)}"); sorun += 1
        if (e | v) & test: print(f"HATA {f.name}: CV∩test = {len((e | v) & test)}"); sorun += 1
        dogrulamalar.append(v)
    for i in range(len(dogrulamalar)):
        for j in range(i + 1, len(dogrulamalar)):
            if dogrulamalar[i] & dogrulamalar[j]:
                print(f"HATA kat{i}∩kat{j} doğrulama = {len(dogrulamalar[i] & dogrulamalar[j])}"); sorun += 1
    print("SIZINTI KONTROLÜ:", "TEMİZ (0 kesişim)" if sorun == 0 else f"{sorun} sorun")
    return sorun == 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="komut", required=True)
    a = s.add_parser("etiket-adni"); a.add_argument("--adnimerge", required=True); a.add_argument("--islenmis", required=True); a.add_argument("--cikti", required=True)
    o = s.add_parser("etiket-oasis"); o.add_argument("--csv", required=True); o.add_argument("--islenmis", required=True); o.add_argument("--cikti", required=True); o.add_argument("--min_yas", type=int, default=60)
    b = s.add_parser("bol"); b.add_argument("--etiket", required=True); b.add_argument("--set", required=True); b.add_argument("--cikti", default="veri/bolme"); b.add_argument("--test_oran", type=float, default=0.15); b.add_argument("--kat", type=int, default=5); b.add_argument("--tohum", type=int, default=2026)
    d = s.add_parser("dogrula"); d.add_argument("--set", required=True); d.add_argument("--bolme", default="veri/bolme")
    x = p.parse_args()
    if x.komut == "etiket-adni": etiket_adni(Path(x.adnimerge), Path(x.islenmis), Path(x.cikti))
    elif x.komut == "etiket-oasis": etiket_oasis(Path(x.csv), Path(x.islenmis), Path(x.cikti), x.min_yas)
    elif x.komut == "bol": bol(Path(x.etiket), x.set, Path(x.cikti), x.test_oran, x.kat, x.tohum)
    elif x.komut == "dogrula": raise SystemExit(0 if dogrula(x.set, Path(x.bolme)) else 1)


if __name__ == "__main__":
    main()
