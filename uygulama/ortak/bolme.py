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
   python bolme.py etiket-radiata --metadata D:\veri\radiata\radiata_metadata.csv --veri D:\veri\radiata\islenmis --kohort OASIS-1 OASIS-2 --min_yas 60 --cikti veri\oasis_etiket.csv
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


def etiket_bids(katilimcilar: Path, veri_klasor: Path, cikti: Path, sutun: str | None = None,
                kaynak: str | None = None) -> pd.DataFrame:
    """BIDS participants.tsv + görüntü klasörü → etiket CSV (denek_id, dosya, sinif, yas, cinsiyet).

    `veri_klasor` ön işlenmiş `.npy` klasörü olabilir (eğitim için) ya da ham `.nii.gz` klasörü
    (ön işlemeden önce kohort bileşimini görmek için). Eşleşme denek kimliğine göre yapılır.
    """
    df = pd.read_csv(katilimcilar, sep="\t", dtype=str)
    kimlik = "participant_id" if "participant_id" in df.columns else df.columns[0]
    # Kaynak kohort adı: verilmezse veri setinin klasör adından türetilir (ds007561, ds007857…).
    # Birden çok kohort birleştirildiğinde bu sütun hem katları dengelemek hem merkez etkisini
    # raporlamak için gerekir (VERI-SETI §2d).
    kaynak = kaynak or Path(katilimcilar).resolve().parent.parent.name or "bilinmeyen"
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
                         "cinsiyet": r.get(cins_s, "") if cins_s else "",
                         "kaynak": kaynak})

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


DX_RADIATA = {"cognitively_normal": 0, "mild_cognitive_impairment": 1, "Alzheimers_disease": 2}


def etiket_radiata(metadata: Path, veri_klasor: Path, cikti: Path, kohortlar: list[str],
                   min_yas: int = 60, max_iqr: float | None = None) -> pd.DataFrame:
    r"""`radiata-ai/brain-structure` metadata.csv -> etiket CSV (denek basina TEK satir).

    Bu koleksiyon boylamsal: OASIS-2'de ayni denegin 5 oturumu olabiliyor. Etiket CSV'de denek
    tekrarli olamaz (`bol()` bunu dogruluyor), dolayisiyla oturum secmek gerekiyor. Secim kurali
    keyfi degil, **Wen 2020 (madde 2.2) protokolu**:

    - **AD grubu:** denegin **ilk AD tanili** oturumu. En gec oturumu almak atrofiyi yapay olarak
      buyutur (en ileri evreyi secmek demek), temel oturumu almak ise CN'ken cekilmis goruntuyu
      AD etiketlemek demek olur. Ilk AD oturumu ikisinin de hatasini yapmaz.
    - **CN grubu:** **yalniz kararli CN** -- hicbir oturumunda AD tanisi almamis denekler, temel
      oturumuyla. Sonradan AD'ye donusen bir denegi "saglikli" saymak kontrol grubunu kirletir:
      beyninde hastalik sureci zaten baslamistir, model onu AD'ye benzer bulur ve ceza alir.
      OASIS-2'de **14 denek** boyle donusuyor; bunlar CN'den cikar, AD'ye kendi AD oturumuyla girer.
    - **Tanisi MCI olan ya da oturumlari arasinda tutarsiz giden denek atilir.**

    `--min_yas`: AD yalniz yaslilarda goruldugu icin suzgecsiz kullanilirsa CN grubu 20 yasindaki
    gonullulerle dolar ve model yasi ogrenir, hastaligi degil (OASIS-1'de CN yas ortalamasi 51,8).
    Varsayilan 60 ile yas farki istatistiksel olarak kayboluyor (Welch p = 0,39).

    `--max_iqr`: veri kartindaki kalite notu (**buyuk deger = kotu**). Varsayilanda suzgec yok;
    uygulanirsa kac denegin dustugu basilir.
    """
    df = pd.read_csv(metadata)
    for sut in ("participant_id", "session_id", "age", "sex", "clinical_diagnosis", "study"):
        if sut not in df.columns:
            raise SystemExit(f"metadata.csv'de '{sut}' sutunu yok - kolonlar: {list(df.columns)}")
    tum_kohort = sorted(set(df["study"]))
    df = df[df["study"].isin(kohortlar)].copy()
    if df.empty:
        raise SystemExit(f"{kohortlar} kohortlarindan satir yok - metadata'da olanlar: {tum_kohort}")

    df["session_id"] = df["session_id"].astype(str)
    df = df.sort_values(["participant_id", "session_id"])

    satirlar, eslesmeyen = [], []
    atlanan = {"mci": 0, "tutarsiz": 0, "yas": 0, "iqr": 0}
    for denek, g in df.groupby("participant_id", sort=True):
        taniler = set(g["clinical_diagnosis"])
        if not taniler <= set(DX_RADIATA) or any(DX_RADIATA[t] == 1 for t in taniler):
            atlanan["mci"] += 1            # MCI ya da eslenemeyen tani degeri
            continue
        ad = g[g["clinical_diagnosis"] == "Alzheimers_disease"]
        if len(ad):
            kayit, sinif = ad.iloc[0], 2                       # ilk AD oturumu
        elif taniler == {"cognitively_normal"}:
            kayit, sinif = g.iloc[0], 0                        # kararli CN, temel oturum
        else:
            atlanan["tutarsiz"] += 1
            continue
        if float(kayit["age"]) < min_yas:
            atlanan["yas"] += 1
            continue
        if max_iqr is not None and float(kayit.get("image_quality_rating", 0) or 0) > max_iqr:
            atlanan["iqr"] += 1
            continue

        kok = f"{kayit['study']}_{kayit['participant_id']}_{kayit['session_id']}"
        adaylar = sorted(Path(veri_klasor).glob(f"{kok}*.npy"))
        if not adaylar:
            eslesmeyen.append(kok)
            continue
        satirlar.append({"denek_id": f"{kayit['study']}_{denek}", "dosya": adaylar[0].name,
                         "sinif": sinif, "yas": float(kayit["age"]),
                         "cinsiyet": "F" if str(kayit["sex"]).lower().startswith("f") else "M",
                         "kaynak": kayit["study"]})

    out = pd.DataFrame(satirlar)
    if len(out):
        out = out.sort_values("denek_id")
    Path(cikti).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(cikti, index=False)

    sayim = out["sinif"].value_counts().sort_index().to_dict() if len(out) else {}
    print(f"radiata etiket (yas >= {min_yas}): {len(out)} denek -> {sayim}  (0 NC, 2 AD)  -> {cikti}")
    print(f"  atlanan: MCI/eslenemeyen {atlanan['mci']} - tutarsiz tani {atlanan['tutarsiz']} - "
          f"yas < {min_yas} {atlanan['yas']} - IQR {atlanan['iqr']}")
    if eslesmeyen:
        print(f"  UYARI {len(eslesmeyen)} denek icin islenmis .npy yok: {eslesmeyen[:5]}"
              f"{' ...' if len(eslesmeyen) > 5 else ''}")
        print("  -> once onisle.py'yi kos, sonra bu komutu tekrar calistir.")
    if len(out):
        _karistirici_raporu(out)
    return out


def _karistirici_raporu(out: pd.DataFrame) -> None:
    """Yas/cinsiyet/kohort karistiricilarini basar. Rapor yontem bolumune bu sayilar yazilacak."""
    from scipy import stats
    g = list(out.groupby("sinif"))
    print("  sinif basina: " + " - ".join(
        f"{int(k)}: n={len(v)} yas {v['yas'].mean():.1f}+-{v['yas'].std():.1f} "
        f"kadin {(v['cinsiyet'] == 'F').mean():.0%}" for k, v in g))
    if len(g) == 2:
        a, b = [v["yas"].dropna() for _, v in g]
        t, py = stats.ttest_ind(a, b, equal_var=False)
        print(f"  yas farki Welch t={t:+.2f} p={py:.4f}" + ("  -> DENGELI" if py > 0.05 else
              "  -> UYARI yas karistirici: eslestir.py ile eslestir ya da raporda belirt"))
        tab = pd.crosstab(out["sinif"], out["cinsiyet"])
        if tab.shape == (2, 2):
            _, pc = stats.fisher_exact(tab.values)
            print(f"  cinsiyet farki Fisher p={pc:.4f}" + ("  -> DENGELI" if pc > 0.05 else
                  "  -> UYARI cinsiyet karistirici: raporda ortak degisken olarak belirtilmeli, "
                  "ayrica cinsiyete gore ayri metrik sunulmali"))
    if "kaynak" in out.columns and out["kaynak"].nunique() > 1:
        print("  kohort x sinif:")
        print("    " + pd.crosstab(out["kaynak"], out["sinif"]).to_string().replace("\n", "\n    "))
        tek = [k for k, v in out.groupby("kaynak")["sinif"].nunique().items() if v < 2]
        if tek:
            print(f"  UYARI tek sinifli kohort: {tek} -> model kohortu (tarayiciyi) ogrenebilir")


def birlestir(girdiler: list[Path], cikti: Path) -> pd.DataFrame:
    """Birden çok etiket CSV'sini tek dosyada birleştirir ve kohort × sınıf tablosunu basar.

    UYARI (VERI-SETI §2d): birleştirme ancak **her kohort kendi içinde birden çok sınıfa sahipse**
    meşrudur. Sınıfları kohortlara bölüştürmek (AD'yi bir setten, kontrolü başkasından almak) modelin
    hastalık yerine tarayıcıyı öğrenmesine yol açar. Bu fonksiyon o durumu tespit edip uyarır.
    """
    parcalar = []
    for g in girdiler:
        d = pd.read_csv(g)
        if "kaynak" not in d.columns:
            d["kaynak"] = Path(g).stem
        parcalar.append(d)
    out = pd.concat(parcalar, ignore_index=True)

    # Kimlik çakışması olursa kaynak önüne eklenir (iki sette aynı sub-01 olabilir)
    if not out["denek_id"].is_unique:
        cak = out[out["denek_id"].duplicated(keep=False)]["denek_id"].nunique()
        out["denek_id"] = out["kaynak"].astype(str) + "_" + out["denek_id"].astype(str)
        print(f"UYARI {cak} denek kimliği iki sette de vardı → kimliklerin başına kaynak eklendi")

    tablo = pd.crosstab(out["kaynak"], out["sinif"])
    print(f"birleştirildi: {len(out)} denek, {out['kaynak'].nunique()} kohort → {cikti}")
    print(tablo.to_string())
    tek_sinifli = [k for k, s in out.groupby("kaynak")["sinif"].nunique().items() if s < 2]
    if tek_sinifli:
        print(f"  !! TEHLİKE: {tek_sinifli} kohortunda tek sınıf var. Sınıf ile kohort birbirine karışmış "
              f"durumda; model tarayıcıyı öğrenir. Bu birleşim PROTOKOL'e göre KULLANILAMAZ (VERI-SETI §2d).")
    Path(cikti).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(cikti, index=False)
    return out


def bol(etiket: Path, set_adi: str, cikti: Path, test_oran: float = 0.15, kat: int = 5, tohum: int = 2026):
    df = pd.read_csv(etiket)
    assert df["denek_id"].is_unique, "etiket CSV'de denek_id tekrarlı — her denek tek satır olmalı"
    cikti = Path(cikti); cikti.mkdir(parents=True, exist_ok=True)

    # Çok kohortlu veride katlar hem SINIF hem KAYNAK bakımından dengeli olmalı: yoksa bir kat
    # ağırlıklı olarak tek bir tarayıcıdan gelir ve o katın sonucu merkez etkisini ölçer.
    # Hücrelerden biri kat sayısından küçükse bu mümkün değil → sınıfa göre dengelemeye düşülür.
    def _tabaka(d):
        if "kaynak" in d.columns and d["kaynak"].nunique() > 1:
            birlesik = d["sinif"].astype(str) + "|" + d["kaynak"].astype(str)
            if birlesik.value_counts().min() >= max(kat, 2):
                return birlesik, True
            print("  not: kohort×sınıf hücrelerinden biri çok küçük → katlar yalnız sınıfa göre dengelendi")
        return d["sinif"], False

    tab, kohort_dengeli = _tabaka(df)
    try:
        kalan, test = train_test_split(df, test_size=test_oran, stratify=tab, random_state=tohum)
    except ValueError:
        print("  not: kilitli test kohort×sınıfa göre bölünemedi → yalnız sınıfa göre bölündü")
        kohort_dengeli = False
        kalan, test = train_test_split(df, test_size=test_oran, stratify=df["sinif"], random_state=tohum)
    test.to_csv(cikti / f"{set_adi}_test.csv", index=False)
    sgkf = StratifiedGroupKFold(n_splits=kat, shuffle=True, random_state=tohum)
    kalan_tab = (kalan["sinif"].astype(str) + "|" + kalan["kaynak"].astype(str)) if kohort_dengeli else kalan["sinif"]
    try:
        bolmeler = list(sgkf.split(kalan, kalan_tab, groups=kalan["denek_id"]))
    except ValueError:
        print("  not: katlar kohort×sınıfa göre bölünemedi → yalnız sınıfa göre bölündü")
        kohort_dengeli = False
        bolmeler = list(sgkf.split(kalan, kalan["sinif"], groups=kalan["denek_id"]))
    harita = [{"denek_id": r, "bolum": "test", "kat": -1} for r in test["denek_id"]]
    for k, (egitim_idx, dogrulama_idx) in enumerate(bolmeler):
        d = kalan.copy(); d["bolum"] = "egitim"
        d.iloc[dogrulama_idx, d.columns.get_loc("bolum")] = "dogrulama"
        d.to_csv(cikti / f"{set_adi}_kat{k}.csv", index=False)
        harita += [{"denek_id": t.denek_id, "bolum": t.bolum, "kat": k} for t in d.itertuples()]
    # Paylaşılabilir bölme haritası: yalnız denek kimliği + kat/bölüm — tanı, yaş, cinsiyet YOK.
    # ADNI DUA klinik veriyi üçüncü tarafa dağıtmayı yasaklar; tekrarlanabilirlik için bölme bilgisi yeterli
    # (clinicadl de bölmeleri böyle yayımlar). Depoya giren dosya BUDUR; klinik sütunlu CSV'ler yerelde kalır.
    harita_yolu = cikti / f"{set_adi}_bolme_haritasi.csv"
    pd.DataFrame(harita).to_csv(harita_yolu, index=False)
    print(f"{set_adi}: test {len(test)} denek, CV {len(kalan)} denek, {kat} kat → {cikti}"
          + ("  [katlar kohort×sınıf dengeli]" if kohort_dengeli else ""))
    if "kaynak" in df.columns and df["kaynak"].nunique() > 1:
        print("  kohort × sınıf (tüm set):")
        print(pd.crosstab(df["kaynak"], df["sinif"]).to_string())
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
    bd = s.add_parser("etiket-bids"); bd.add_argument("--katilimcilar", required=True); bd.add_argument("--veri", required=True); bd.add_argument("--cikti", required=True); bd.add_argument("--sutun", default=None); bd.add_argument("--kaynak", default=None)
    rd = s.add_parser("etiket-radiata"); rd.add_argument("--metadata", required=True); rd.add_argument("--veri", required=True)
    rd.add_argument("--cikti", required=True); rd.add_argument("--kohort", nargs="+", required=True)
    rd.add_argument("--min_yas", type=int, default=60); rd.add_argument("--max_iqr", type=float, default=None)
    br = s.add_parser("birlestir"); br.add_argument("--girdi", nargs="+", required=True); br.add_argument("--cikti", required=True)
    b = s.add_parser("bol"); b.add_argument("--etiket", required=True); b.add_argument("--set", required=True); b.add_argument("--cikti", default="veri/bolme"); b.add_argument("--test_oran", type=float, default=0.15); b.add_argument("--kat", type=int, default=5); b.add_argument("--tohum", type=int, default=2026)
    d = s.add_parser("dogrula"); d.add_argument("--set", required=True); d.add_argument("--bolme", default="veri/bolme")
    x = p.parse_args()
    if x.komut == "etiket-adni": etiket_adni(Path(x.adnimerge), Path(x.islenmis), Path(x.cikti))
    elif x.komut == "etiket-oasis": etiket_oasis(Path(x.csv), Path(x.islenmis), Path(x.cikti), x.min_yas)
    elif x.komut == "etiket-bids": etiket_bids(Path(x.katilimcilar), Path(x.veri), Path(x.cikti), x.sutun, x.kaynak)
    elif x.komut == "etiket-radiata": etiket_radiata(Path(x.metadata), Path(x.veri), Path(x.cikti), x.kohort, x.min_yas, x.max_iqr)
    elif x.komut == "birlestir": birlestir([Path(g) for g in x.girdi], Path(x.cikti))
    elif x.komut == "bol": bol(Path(x.etiket), x.set, Path(x.cikti), x.test_oran, x.kat, x.tohum)
    elif x.komut == "dogrula": raise SystemExit(0 if dogrula(x.set, Path(x.bolme)) else 1)


if __name__ == "__main__":
    main()
