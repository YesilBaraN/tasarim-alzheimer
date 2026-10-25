# -*- coding: utf-8 -*-
r"""
indir.py — Açık veri setlerini herkesin aynı şekilde indirmesi için tek komut.

Neden veri depoya konmuyor: ds007561 ve ds007857 CC0 lisanslı, yani yeniden dağıtmak **serbest**
(ADNI/OASIS'ten farkı bu). Ama 2,9 GB ikili dosyayı git'e koymak herkesin klonunu 2,9 GB yapar,
GitHub 1 GB üstü depolarda uyarır ve Git LFS'in ücretsiz katmanı 1 GB'dır. Veri zaten tek komutla
iniyor; paylaşılması gereken şey veri değil, **onu birebir aynı şekilde indiren betik**. Böylece
üçümüzde de aynı dosyalar olur ve bunu sağlama (checksum) ile doğrularız.

ADNI ve OASIS bu betikle İNMEZ ve inemez: onlar başvuru + Data Use Agreement ister ve yeniden
dağıtımları yasaktır (`VERI-SETI.md §2`).

Kullanım:
  python veri\indir.py --hedef D:\veri                 # ikisini de indir
  python veri\indir.py --hedef D:\veri --set ds007561  # yalnız küçüğü (284 MB, hızlı deneme)
  python veri\indir.py --hedef D:\veri --dogrula       # indirmeden, eldekinin bütünlüğünü sına

Sonrasında (ön işleme ve etiket):
  python onisleme\onisle.py --girdi <hedef>\ds007561\ham --cikti <hedef>\ds007561\islenmis --toplu --cihaz 0
  python uygulama\ortak\bolme.py etiket-bids --katilimcilar <hedef>\ds007561\ham\participants.tsv ^
      --veri <hedef>\ds007561\islenmis --cikti veri\ds007561_etiket.csv
"""
from __future__ import annotations

import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:
        pass

KOVA = "https://s3.amazonaws.com/openneuro.org"
AD_ALANI = "{http://s3.amazonaws.com/doc/2006-03-01/}"

SETLER = {
    "ds007561": {
        "aciklama": "20 denek · 14 Control / 5 MCI / 1 AD · 61–84 yaş · MPnRAGE T1w (Wisconsin)",
        "lisans": "CC0",
        "tek_tarama": False,   # zaten denek başına bir tarama
    },
    "ds007857": {
        "aciklama": "289 denek · 212 CN / 49 MCI / 1 DAT · T1w + bold + dwi (yalnız T1w indirilir)",
        "lisans": "CC0",
        "tek_tarama": True,    # denek başına birden çok oturum var → ilki alınır
    },
}


def s3_listele(onek: str) -> list[tuple[str, int]]:
    """Kovadaki anahtarları (yol, boyut) olarak sayfalayarak toplar."""
    anahtarlar: list[tuple[str, int]] = []
    jeton = ""
    while True:
        url = f"{KOVA}/?list-type=2&prefix={onek}&max-keys=1000"
        if jeton:
            from urllib.parse import quote
            url += f"&continuation-token={quote(jeton, safe='')}"
        with urllib.request.urlopen(url, timeout=60) as y:
            kok = ET.fromstring(y.read())
        for icerik in kok.findall(f"{AD_ALANI}Contents"):
            anahtarlar.append((icerik.findtext(f"{AD_ALANI}Key"),
                               int(icerik.findtext(f"{AD_ALANI}Size"))))
        if kok.findtext(f"{AD_ALANI}IsTruncated") != "true":
            break
        jeton = kok.findtext(f"{AD_ALANI}NextContinuationToken") or ""
        if not jeton:
            break
    return anahtarlar


def t1w_sec(anahtarlar: list[tuple[str, int]], tek_tarama: bool) -> list[tuple[str, int]]:
    """Yalnız T1w hacimleri; tek_tarama ise denek başına (sıralı) ilk tarama."""
    t1 = sorted(((k, b) for k, b in anahtarlar if k.endswith("T1w.nii.gz")))
    if not tek_tarama:
        return t1
    gorulen, secilen = set(), []
    for k, b in t1:
        denek = k.split("/")[1]
        if denek not in gorulen:
            gorulen.add(denek)
            secilen.append((k, b))
    return secilen


def dosya_indir(anahtar: str, hedef: Path, beklenen: int) -> str:
    """Boyutu tutuyorsa atlar. Döndürdüğü: 'indi' | 'atlandi' | 'hata: …'."""
    if hedef.exists() and hedef.stat().st_size == beklenen:
        return "atlandi"
    try:
        gecici = hedef.with_suffix(hedef.suffix + ".tmp")
        urllib.request.urlretrieve(f"{KOVA}/{anahtar}", gecici)
        if gecici.stat().st_size != beklenen:
            gecici.unlink(missing_ok=True)
            return f"hata: boyut tutmadi ({gecici.stat().st_size} != {beklenen})"
        gecici.replace(hedef)
        return "indi"
    except Exception as e:
        return f"hata: {type(e).__name__}: {e}"


def seti_indir(ds: str, kok: Path, yalniz_dogrula: bool = False) -> dict:
    bilgi = SETLER[ds]
    ham = kok / ds / "ham"
    ham.mkdir(parents=True, exist_ok=True)
    (kok / ds / "islenmis").mkdir(parents=True, exist_ok=True)

    print(f"\n=== {ds} ({bilgi['lisans']}) ===")
    print(f"    {bilgi['aciklama']}")

    for yan in ("participants.tsv", "participants.json", "dataset_description.json"):
        try:
            urllib.request.urlretrieve(f"{KOVA}/{ds}/{yan}", ham / yan)
        except Exception:
            pass

    secilen = t1w_sec(s3_listele(f"{ds}/"), bilgi["tek_tarama"])
    toplam_mb = sum(b for _, b in secilen) / 1048576
    print(f"    {len(secilen)} T1w hacmi, {toplam_mb:.0f} MB")

    sayim = {"indi": 0, "atlandi": 0, "hata": 0}
    for i, (anahtar, boyut) in enumerate(secilen, 1):
        hedef = ham / Path(anahtar).name
        if yalniz_dogrula:
            durum = "atlandi" if (hedef.exists() and hedef.stat().st_size == boyut) else "hata"
            if durum == "hata":
                print(f"    EKSIK/BOZUK: {hedef.name}")
        else:
            sonuc = dosya_indir(anahtar, hedef, boyut)
            durum = sonuc if sonuc in ("indi", "atlandi") else "hata"
            if durum == "hata":
                print(f"    {hedef.name}: {sonuc}")
        sayim[durum] += 1
        if i % 25 == 0 or i == len(secilen):
            print(f"    [{i}/{len(secilen)}] indi {sayim['indi']} · atlandı {sayim['atlandi']} · hata {sayim['hata']}")
    return sayim


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--hedef", required=True, help="veri kökü (depo DIŞINDA olmalı, ör. D:\\veri)")
    p.add_argument("--set", choices=list(SETLER) + ["hepsi"], default="hepsi")
    p.add_argument("--dogrula", action="store_true", help="indirme, yalnız eldekini sına")
    a = p.parse_args(argv)

    kok = Path(a.hedef).resolve()
    if (Path(__file__).resolve().parents[1]) in kok.parents or kok == Path(__file__).resolve().parents[1]:
        raise SystemExit(f"HEDEF DEPO İÇİNDE: {kok}\nVeri depoya girmemeli — depo dışında bir yol seç.")

    setler = list(SETLER) if a.set == "hepsi" else [a.set]
    toplam = {"indi": 0, "atlandi": 0, "hata": 0}
    for ds in setler:
        for k, v in seti_indir(ds, kok, a.dogrula).items():
            toplam[k] += v

    print(f"\n=== TOPLAM: indi {toplam['indi']} · atlandı {toplam['atlandi']} · hata {toplam['hata']} ===")
    print(f"veri kökü: {kok}")
    if toplam["hata"]:
        print("Hatalı dosyalar var → komutu tekrar koş, tamamlananlar atlanır.")
        raise SystemExit(1)
    print("Hepsi tamam. Sıradaki: onisle.py --toplu  →  bolme.py etiket-bids")


if __name__ == "__main__":
    main()
