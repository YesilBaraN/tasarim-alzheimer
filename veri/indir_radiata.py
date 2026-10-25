# -*- coding: utf-8 -*-
r"""
indir_radiata.py — `radiata-ai/brain-structure` koleksiyonundan seçili kohortları indirir.

Neden ayrı betik: bu koleksiyon OpenNeuro değil HuggingFace'te ve beş çalışmayı birleştiriyor.
Hepsini indirmek 8 GB ve **yanlış** olur: AD yalnız OASIS'ten geliyor, diğer üç kohort tamamen sağlıklı.
Tümünü karıştırmak sınıf–tarayıcı karışması demek (`veri/VERI-SETI.md §2g`). Bu yüzden kohort seçilebilir.

Kullanım:
  python veri\indir_radiata.py --hedef D:\veri --kohort OASIS-1 OASIS-2      # ana görev (~1,6 GB)
  python veri\indir_radiata.py --hedef D:\veri --kohort DLBS IXI NKI-RS      # ön eğitim havuzu (~6,3 GB)
  python veri\indir_radiata.py --hedef D:\veri --kohort OASIS-1 OASIS-2 --dogrula

Lisans: koleksiyon ODC-By v1.0; tek tek taramalar çalışma-özel DUA'lara tabi (OASIS = Custom DUA).
Ekip OASIS veri kullanım başvurusunu yaptı; raporun yöntem bölümünde kaynak açıkça belirtilecek.
"""
from __future__ import annotations

import argparse
import csv
import sys
import urllib.request
from pathlib import Path

for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:
        pass

DEPO = "https://huggingface.co/datasets/radiata-ai/brain-structure/resolve/main"
KOHORTLAR = ("OASIS-1", "OASIS-2", "DLBS", "IXI", "NKI-RS")


def metadata_indir(hedef: Path) -> Path:
    yol = hedef / "radiata_metadata.csv"
    if not yol.exists() or yol.stat().st_size == 0:
        hedef.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(f"{DEPO}/metadata.csv", yol)
    return yol


def satirlar(meta: Path, kohortlar: list[str]) -> list[dict]:
    with open(meta, encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r["study"] in kohortlar]


def indir(kayit: dict, ham: Path) -> str:
    """Dosya adını kohort+denek+oturum'dan kurar; düz klasör, çakışma olmaz."""
    ad = f"{kayit['study']}_{kayit['participant_id']}_{kayit['session_id']}.nii.gz"
    hedef = ham / ad
    if hedef.exists() and hedef.stat().st_size > 1000:
        return "atlandi"
    try:
        gecici = hedef.with_suffix(".tmp")
        urllib.request.urlretrieve(f"{DEPO}/{kayit['t1_local_path']}", gecici)
        if gecici.stat().st_size < 1000:
            gecici.unlink(missing_ok=True)
            return "hata: dosya cok kucuk"
        gecici.replace(hedef)
        return "indi"
    except Exception as e:
        return f"hata: {type(e).__name__}: {e}"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--hedef", required=True, help="veri kökü (depo DIŞINDA)")
    p.add_argument("--kohort", nargs="+", choices=KOHORTLAR, required=True)
    p.add_argument("--dogrula", action="store_true", help="indirme, eldekini say")
    a = p.parse_args(argv)

    kok = Path(a.hedef).resolve()
    depo_kok = Path(__file__).resolve().parents[1]
    if kok == depo_kok or depo_kok in kok.parents:
        raise SystemExit(f"HEDEF DEPO İÇİNDE: {kok}\nVeri depoya girmemeli.")

    ham = kok / "radiata" / "ham"
    ham.mkdir(parents=True, exist_ok=True)
    (kok / "radiata" / "islenmis").mkdir(parents=True, exist_ok=True)

    meta = metadata_indir(kok / "radiata")
    kayitlar = satirlar(meta, a.kohort)
    print(f"kohort: {', '.join(a.kohort)} → {len(kayitlar)} tarama")
    tani = {}
    for r in kayitlar:
        tani[r["clinical_diagnosis"]] = tani.get(r["clinical_diagnosis"], 0) + 1
    print(f"  tanı: {tani}")
    print(f"  denek: {len({r['participant_id'] for r in kayitlar})}")

    sayim = {"indi": 0, "atlandi": 0, "hata": 0}
    for i, r in enumerate(kayitlar, 1):
        if a.dogrula:
            ad = f"{r['study']}_{r['participant_id']}_{r['session_id']}.nii.gz"
            d = "atlandi" if (ham / ad).exists() else "hata"
        else:
            sonuc = indir(r, ham)
            d = sonuc if sonuc in ("indi", "atlandi") else "hata"
            if d == "hata":
                print(f"  {r['participant_id']}: {sonuc}")
        sayim[d] += 1
        if i % 50 == 0 or i == len(kayitlar):
            print(f"  [{i}/{len(kayitlar)}] indi {sayim['indi']} · atlandı {sayim['atlandi']} · hata {sayim['hata']}")

    print(f"\nTOPLAM: {sayim} → {ham}")
    if sayim["hata"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
