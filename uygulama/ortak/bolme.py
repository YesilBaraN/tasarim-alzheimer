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
   python bolme.py etiket-bids  --katilimcilar D:\veri\ds007561\ham\participants.tsv --veri D:\veri\ds007561\islenmis --cikti veri\ds007561_etiket.csv
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


# BIDS participants.tsv'deki tanı yazımları → bizim sınıf kodumuz (0 NC, 1 MCI, 2 AD).
# OpenNeuro setleri aynı şeyi farklı yazıyor; eşleme burada tek yerde tutulur.
DX_BIDS = {
    "control": 0, "controls": 0, "cn": 0, "hc": 0, "healthy": 0, "normal": 0, "nc": 0,
    "healthy control": 0, "cognitively normal": 0,
    "mci": 1, "emci": 1, "lmci": 1, "mild cognitive impairment": 1, "pmci": 1, "smci": 1,
    "ad": 2, "dat": 2, "dementia": 2, "alzheimer": 2, "alzheimers": 2, "alzheimer's": 2,
    "mild ad": 2, "moderate ad": 2, "probable ad": 2, "ad dementia": 2,
}
TANI_SUTUNLARI = ("diagnosis", "dx", "group", "condition", "cohort", "status", "clinical_status")


def _sinif_cevir(deger) -> int | None:
    s = str(deger).strip().lower()
    if s in ("", "n/a", "na", "nan", "-", "none"):
        return None
    return DX_BIDS.get(s)


def etiket_bids(katilimcilar: Path, veri_klasor: Path, cikti: Path, sutun: str | None = None) -> pd.DataFrame:
    """BIDS participants.tsv + görüntü klasörü → etiket CSV (denek_id, dosya, sinif, yas, cinsiyet).

    `veri_klasor` ön işlenmiş `.npy` klasörü olabilir (eğitim için) ya da ham `.nii.gz` klasörü
    (ön işlemeden önce kohort bileşimini görmek için). Eşleşme denek kimliğine göre yapılır.
    """
    df = pd.read_csv(katilimcilar, sep="\t", dtype=str)
    kimlik = "participant_id" if "participant_id" in df.columns else df.columns[0]
    if sutun is None:
        aday = [c for c in df.columns if c.strip().lower() in TANI_SUTUNLARI]
        if not aday:
            raise SystemExit(f"tanı sütunu bulunamadı. Sütunlar: {list(df.columns)}\n"
                             f"--sutun ile elle belirt.")
        sutun = aday[0]
        print(f"tanı sütunu otomatik seçildi: '{sutun}' (diğer adaylar: {aday[1:] or '-'})")

    yas_s = next((c for c in df.columns if c.strip().lower() in ("age", "yas")), None)
    cins_s = next((c for c in df.columns if c.strip().lower() in ("sex", "gender", "cinsiyet")), None)

    satirlar, atlanan, eslesmeyen = [], {}, []
    for _, r in df.iterrows():
        denek = str(r[kimlik]).strip()
        sinif = _sinif_cevir(r[sutun])
        if sinif is None:
            atlanan[str(r[sutun]).strip()] = atlanan.get(str(r[sutun]).strip(), 0) + 1
            continue
        adaylar = sorted(Path(veri_klasor).rglob(f"*{denek}*.npy")) or \
                  sorted(Path(veri_klasor).rglob(f"*{denek}*.nii.gz"))
        if not adaylar:
            eslesmeyen.append(denek)
            continue
        satirlar.append({"denek_id": denek, "dosya": adaylar[0].name, "sinif": sinif,
                         "yas": r.get(yas_s, np.nan) if yas_s else np.nan,
                         "cinsiyet": r.get(cins_s, "") if cins_s else ""})

    out = pd.DataFrame(satirlar).drop_duplicates("denek_id")
    Path(cikti).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(cikti, index=False)
    sayim = out["sinif"].value_counts().sort_index().to_dict() if len(out) else {}
    print(f"BIDS etiket: {len(out)} denek → {sayim}  (0 NC, 1 MCI, 2 AD)  → {cikti}")
    if atlanan:
        print(f"  eşlenemeyen tanı değerleri (atlandı): {atlanan}")
    if eslesmeyen:
        print(f"  UYARI {len(eslesmeyen)} denek için görüntü bulunamadı: {eslesmeyen[:8]}"
              f"{' …' if len(eslesmeyen) > 8 else ''}")
    if len(out) and min(out["sinif"].value_counts()) < 10:
        print("  UYARI en küçük sınıfta 10'dan az denek var → bu set SONUCLAR tablosuna giremez, "
              "yalnız hat denemesi için kullanılabilir (PROTOKOL madde 5).")
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
    bd = s.add_parser("etiket-bids"); bd.add_argument("--katilimcilar", required=True); bd.add_argument("--veri", required=True); bd.add_argument("--cikti", required=True); bd.add_argument("--sutun", default=None)
    b = s.add_parser("bol"); b.add_argument("--etiket", required=True); b.add_argument("--set", required=True); b.add_argument("--cikti", default="veri/bolme"); b.add_argument("--test_oran", type=float, default=0.15); b.add_argument("--kat", type=int, default=5); b.add_argument("--tohum", type=int, default=2026)
    d = s.add_parser("dogrula"); d.add_argument("--set", required=True); d.add_argument("--bolme", default="veri/bolme")
    x = p.parse_args()
    if x.komut == "etiket-adni": etiket_adni(Path(x.adnimerge), Path(x.islenmis), Path(x.cikti))
    elif x.komut == "etiket-oasis": etiket_oasis(Path(x.csv), Path(x.islenmis), Path(x.cikti), x.min_yas)
    elif x.komut == "etiket-bids": etiket_bids(Path(x.katilimcilar), Path(x.veri), Path(x.cikti), x.sutun)
    elif x.komut == "bol": bol(Path(x.etiket), x.set, Path(x.cikti), x.test_oran, x.kat, x.tohum)
    elif x.komut == "dogrula": raise SystemExit(0 if dogrula(x.set, Path(x.bolme)) else 1)


if __name__ == "__main__":
    main()
