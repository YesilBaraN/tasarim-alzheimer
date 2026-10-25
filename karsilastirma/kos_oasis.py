# -*- coding: utf-8 -*-
r"""
kos_oasis.py — OASIS AD-vs-NC karşılaştırmasının sekiz modelini sırayla koşar.

Neden ayrı betik: her modelin batch boyutu **ölçülmüş** VRAM'ine göre farklı. Hepsini aynı
`--batch 4` ile koşmak RTX 3050 (4 GB) üzerinde P07 ve P11'i paylaşılan sistem belleğine
taşırıyor — program çökmüyor ama kat başına saatler sürüyor, yani sessizce yavaşlıyor.
Buradaki tablo bu tuzağı kapatıyor: ölçüm `KURULUM.md §0b`'de.

Etkin batch her modelde 4'te sabit tutuluyor (`batch × accum = 4`), çünkü etkin batch'i
modele göre değiştirmek karşılaştırmayı bozar: PROTOKOL madde 7'ye göre modeller arasında
yalnız mimari değişebilir, eğitim yordamı değişmez.

Kullanım:
  python karsilastirma\kos_oasis.py --veri D:\veri\radiata\islenmis --kat 0
  python karsilastirma\kos_oasis.py --veri D:\veri\radiata\islenmis --tum_katlar
  python karsilastirma\kos_oasis.py --veri D:\veri\radiata\islenmis --kat 0 --model P01-voxcnn P12

Yarıda kesilirse aynı komut kaldığı yerden devam eder: `egit.py` her epoch sonunda
`<ad>_son.pth` yazıyor ve yeniden başlarken onu buluyor.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

# Dar VRAM'de parcalanma (fragmentation) tek basina yuzlerce MB yiyor: 3,13 GB isteyen bir model
# 4,0 GB kartta parcalanma yuzunden tasabiliyor. expandable_segments ayirici bloklari buyutulebilir
# yapiyor ve bu kaybi buyuk olcude kapatiyor. torch >= 2.1'de var; eski surumde yok sayilir.
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:
        pass

KOK = Path(__file__).resolve().parents[1]

# (kisa_ad, model_klasor, varyant, batch, accum, ek_argumanlar)
# batch x accum = 4 her satirda: etkin batch sabit.
#
# Batch degerleri TAHMIN DEGIL, `vram_olc.py --boyutlar 128 --batchlar 2 4` ile olculdu.
# Kart 4,0 GB; esik 4,0 degil **~3,0 GB** olarak alindi, cunku "sigdi" demek yetmiyor:
# VoxResNet batch 4'te 3,59 GB istiyor ve "OK" raporluyor, ama gercek kosuda nvidia-smi
# 3,62 GB (kartin %90'i) gosterdi ve epoch suresi 32 saniyeden **7 dakikaya** cikti —
# Windows WDDM kalan bellegi sistem RAM'ine tasidigi icin program cokmuyor, 13 kat
# yavasliyor. Bu sessiz yavaslama bir kez bize 7 saatlik bir kosuya mal oldu.
#
#   model                b2       b4      secilen
#   ortak:sigcnn        0,29     0,56     b4
#   P01 voxcnn          0,34     0,65     b4
#   P01 resnet (VoxResNet) 1,82  3,59     b2 x accum2   <- b4 cok riskli
#   P02 resnet18        0,55     0,82     b4
#   P06 cnn             0,51     0,72     b4
#   P07 resatt18        3,13     5,74     b2 x accum2   <- b2 bile sinirda, en son kosuyor
#   P11 fcn             2,36     4,43     b2 x accum2
#   P12 densenet121     1,28     2,22     b4
#
# Sira ucuzdan pahaliya: bir sey patlarsa once sonuc alinmis olur, en riskli en sonda kalir.
KOSULAR = [
    ("temel",       "ortak",                 "sigcnn",      4, 1, []),
    ("P01-voxcnn",  "baran_P01_korolev",     "voxcnn",      4, 1, []),
    ("P02-monai",   "baran_P02_medicalnet",  "resnet18",    4, 1, ["--agirlik", "monai", "--isinma", "5"]),
    ("P06",         "gorkem_P06_bohle",      "cnn",         4, 1, []),
    ("P02-sifirdan", "baran_P02_medicalnet", "resnet18",    4, 1, ["--etiket", "sifirdan-ablation"]),
    ("P12",         "ertugrul_P12_densenet", "densenet121", 4, 1, []),
    ("P01-voxresnet", "baran_P01_korolev",   "resnet",      2, 2, []),
    ("P11",         "ertugrul_P11_qiu_fcn",  "fcn",         2, 2, []),
    ("P07",         "gorkem_P07_resattnet",  "resatt18",    2, 2, []),
]


def komut(k, a) -> list[str]:
    kisa, model, varyant, batch, accum, ek = k
    c = [sys.executable, "-u", str(KOK / "uygulama/ortak/egit.py"),
         "--model", model, "--varyant", varyant,
         "--set", a.set, "--gorev", a.gorev,
         "--veri", a.veri, "--bolme", a.bolme, "--cikti", a.cikti,
         "--batch", str(batch), "--accum", str(accum),
         "--epoch", str(a.epoch), "--sabir", str(a.sabir),
         "--tohum", str(a.tohum), "--isci", str(a.isci)]
    c += ["--tum_katlar"] if a.tum_katlar else ["--kat", str(a.kat)]
    return c + ek


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--veri", required=True, help="islenmis .npy klasoru")
    p.add_argument("--set", default="oasis")
    p.add_argument("--gorev", default="ikili", choices=["ikili", "ikili-mci", "uc"])
    p.add_argument("--bolme", default=str(KOK / "veri/bolme"))
    p.add_argument("--cikti", default=str(KOK / "karsilastirma/kosu_kayitlari"))
    p.add_argument("--kat", type=int, default=0)
    p.add_argument("--tum_katlar", action="store_true")
    p.add_argument("--epoch", type=int, default=60)
    p.add_argument("--sabir", type=int, default=12)
    p.add_argument("--tohum", type=int, default=2026)
    p.add_argument("--isci", type=int, default=2)
    p.add_argument("--model", nargs="+", default=None,
                   help=f"yalniz bu kisa adlar ({', '.join(k[0] for k in KOSULAR)}); varsayilan hepsi")
    p.add_argument("--kuru", action="store_true", help="komutlari bas, kosma")
    a = p.parse_args()

    secili = KOSULAR if not a.model else [k for k in KOSULAR if k[0] in set(a.model)]
    if a.model and (eksik := set(a.model) - {k[0] for k in KOSULAR}):
        raise SystemExit(f"bilinmeyen kisa ad: {sorted(eksik)}\nolanlar: {[k[0] for k in KOSULAR]}")
    if not secili:
        raise SystemExit("secili kosu yok")

    print(f"{len(secili)} kosu - set {a.set} - gorev {a.gorev} - "
          f"{'tum katlar' if a.tum_katlar else f'kat {a.kat}'}\n")
    sonuc, t0 = [], time.time()
    for i, k in enumerate(secili, 1):
        c = komut(k, a)
        print(f"\n{'=' * 78}\n[{i}/{len(secili)}] {k[0]}  (batch {k[3]} x accum {k[4]})\n"
              f"  {' '.join(c[2:])}\n{'=' * 78}", flush=True)
        if a.kuru:
            continue
        t = time.time()
        r = subprocess.run(c, cwd=str(KOK))
        sure = (time.time() - t) / 60
        sonuc.append((k[0], r.returncode, sure))
        print(f"\n[{i}/{len(secili)}] {k[0]}: {'OK' if r.returncode == 0 else f'HATA {r.returncode}'} "
              f"({sure:.1f} dk)", flush=True)

    if a.kuru:
        return
    print(f"\n{'=' * 78}\nTOPLAM {(time.time() - t0) / 60:.1f} dk")
    for ad, rc, sure in sonuc:
        print(f"  {ad:<14} {'OK   ' if rc == 0 else f'HATA{rc:<2}'} {sure:6.1f} dk")
    basarisiz = [ad for ad, rc, _ in sonuc if rc != 0]
    if basarisiz:
        print(f"\nBASARISIZ: {basarisiz}")
        raise SystemExit(1)
    print("\nHEPSI TAMAM -> simdi: python karsilastirma\\tablo_uret.py "
          f"--set {a.set} --gorev {a.gorev}")


if __name__ == "__main__":
    main()
