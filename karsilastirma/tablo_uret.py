# -*- coding: utf-8 -*-
r"""
tablo_uret.py — `karsilastirma/kosu_kayitlari/*.json` → SONUCLAR.md satırları (PROTOKOL "sonuç satırı biçimi").

Ne yapar:
 1. Koşu kayıtlarını okur, PROTOKOL/KURULUM kurallarına uymayanları **tablodan çıkarır** ve neden çıkardığını yazar:
    - `gpu` alanı geliştirme kartını gösteriyorsa (KURULUM §0b: RTX 3050 yalnız hata ayıklama içindir),
    - `model_notu` mimari sapma bildiriyorsa (ör. VoxCNN padding=1 — PROTOKOL madde 3),
    - `commit` yoksa ("git-yok" — PROTOKOL madde 10).
 2. Kalanları (set, görev, model, varyant, ön eğitim, etiket) olarak gruplar; LR taraması varsa **doğrulama**
    BAcc'ine göre tek LR seçer (madde 2/K2: seçim asla test üstünden yapılmaz), sonra o LR'nin
    kat × tohum koşularının **test** metriklerini ortalama ± ss olarak basar.
 3. Eksik kat/tohum varsa uyarır (madde 5: 5 kat × 3 tohum).
 4. Varsa dış test sonucunu (`karsilastirma/dis_test/<ad>_dis-<set>.json`, `dis_test.py` üretir) satıra ekler.

Koş (proje kökünden):
  python karsilastirma\tablo_uret.py
  python karsilastirma\tablo_uret.py --set adni1 --gorev ikili
  python karsilastirma\tablo_uret.py --tumu          # dışlama kurallarını uygulamadan hepsini bas
  python karsilastirma\tablo_uret.py --yaz karsilastirma\TABLO-URETILDI.md
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
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

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))
from uygulama.ortak import metrikler  # noqa: E402

GELISTIRME_GPU = ("RTX 3050",)   # KURULUM §0b: tabloya girmez
BEKLENEN_KAT = 5
BEKLENEN_TOHUM = (2026, 2027, 2028)

BASLIK = ("| Model | Görev | Ön eğitim | BAcc | AUC | F1-makro | Sens | Spec | Acc | Dış test BAcc | "
          "Parametre | Epoch/süre | VRAM | Commit |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")


# ----------------------------------------------------------------------------- okuma / filtre
def kayitlari_oku(klasor: Path) -> list[dict]:
    out = []
    for f in sorted(klasor.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"ATLA {f.name}: okunamadı ({e})", file=sys.stderr)
            continue
        if "dogrulama" in d and "test" in d:
            d["_dosya"] = f.name
            out.append(d)
    return out


def dislama_nedeni(k: dict) -> str | None:
    gpu = str(k.get("gpu", ""))
    if any(g in gpu for g in GELISTIRME_GPU):
        return f"geliştirme GPU'su ({gpu}) — KURULUM §0b"
    if k.get("model_notu") and "sapma" in str(k["model_notu"]):
        return f"mimari sapma ({k['model_notu']}) — PROTOKOL madde 3"
    if str(k.get("commit", "")) in ("", "git-yok"):
        return "commit hash'i yok — PROTOKOL madde 10"
    return None


# ----------------------------------------------------------------------------- gruplama
def anahtar(k: dict) -> tuple:
    return (k["set"], k["gorev"], k["model"], k.get("varyant", ""), bool(k.get("on_egitim")), k.get("etiket", ""))


def tarama_degeri(k: dict) -> float:
    """Taranan hiperparametre: CNN'lerde LR, SVM'de C (`tarama` alanı). Gruplama anahtarı olduğu için NaN yok."""
    v = k.get("tarama", k.get("lr", k.get("ayar", {}).get("lr")))
    try:
        v = float(v)
    except (TypeError, ValueError):
        return 0.0
    return 0.0 if v != v else v


def tarama_sec(haritasi: dict[float, list[dict]]) -> tuple[float, list[dict], str]:
    """Tarama varsa DOĞRULAMA BAcc ortalamasına göre seç (test'e asla bakılmaz — PROTOKOL K2)."""
    if len(haritasi) == 1:
        v = next(iter(haritasi))
        return v, haritasi[v], ""
    puan = {v: float(np.nanmean([r["dogrulama"]["bacc"] for r in rs])) for v, rs in haritasi.items()}
    # Eşitlikte belirli davran: sıralı anahtarlar üstünden git → en küçük değer (daha fazla düzenlileştirme)
    en_iyi = max(sorted(puan), key=puan.get)
    detay = "hiperparametre seçimi (doğrulama BAcc): " + ", ".join(f"{v:.3g}→{p:.3f}" for v, p in sorted(puan.items()))
    return en_iyi, haritasi[en_iyi], detay + f" ⇒ {en_iyi:.3g}"


def kapsam_uyarisi(kosular: list[dict]) -> str:
    katlar = sorted({r["kat"] for r in kosular})
    tohumlar = sorted({r["tohum"] for r in kosular})
    uyari = []
    if len(katlar) < BEKLENEN_KAT:
        uyari.append(f"{len(katlar)}/{BEKLENEN_KAT} kat ({katlar})")
    eksik_tohum = [t for t in BEKLENEN_TOHUM if t not in tohumlar]
    if eksik_tohum:
        uyari.append(f"eksik tohum {eksik_tohum}")
    beklenen = BEKLENEN_KAT * len(BEKLENEN_TOHUM)
    if len(kosular) < beklenen:
        uyari.append(f"{len(kosular)}/{beklenen} koşu")
    return "; ".join(uyari)


# ----------------------------------------------------------------------------- dış test
def dis_test_oku(klasor: Path) -> dict[str, dict]:
    """<ad>_dis-<set>.json → {koşu adı: {dis_set, metrik}}. dis_test.py üretir."""
    out: dict[str, dict] = {}
    if not klasor.exists():
        return out
    for f in sorted(klasor.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if "ad" in d and "metrik" in d:
            out.setdefault(d["ad"], d)
    return out


def dis_bacc_ozeti(kosular: list[dict], dis: dict[str, dict]) -> str:
    v = [dis[r["ad"]]["metrik"]["bacc"] for r in kosular if r["ad"] in dis]
    if not v:
        return "—"
    return f"{np.mean(v):.3f}±{np.std(v):.3f}"


# ----------------------------------------------------------------------------- satır üretimi
def model_adi(k: dict) -> str:
    ad = f"{k['model']}"
    if k.get("varyant") and k["varyant"] not in ("varsayilan", ""):
        ad += f" ({k['varyant']})"
    if k.get("etiket"):
        ad += f" [{k['etiket']}]"
    return ad


def tablo(kayitlar: list[dict], dis: dict[str, dict]) -> list[str]:
    gruplar: dict[tuple, dict[float, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for k in kayitlar:
        gruplar[anahtar(k)][tarama_degeri(k)].append(k)
    # Birden fazla veri seti varsa satır adına seti yaz, yoksa satırlar ayırt edilemez
    cok_set = len({k["set"] for k in kayitlar}) > 1

    satirlar = [BASLIK]
    notlar = []
    for a in sorted(gruplar, key=lambda t: (t[0], t[1], t[2], t[3])):
        _secilen, kosular, tarama_notu = tarama_sec(gruplar[a])
        ozet = metrikler.ozet([r["test"] for r in kosular])
        commitler = {r.get("commit", "?") for r in kosular}
        ek = {
            "dis_bacc": dis_bacc_ozeti(kosular, dis),
            "param": f"{kosular[0].get('parametre', 0) / 1e6:.2f}M",
            "epoch_sure": f"{np.mean([r.get('epoch_kosulan', 0) for r in kosular]):.0f} ep / "
                          f"{np.mean([r.get('sure_sn', 0) for r in kosular]) / 60:.0f} dk",
            "vram": f"{max(r.get('vram_gb', 0) for r in kosular):.1f} GB",
            "commit": (commitler.pop() if len(commitler) == 1 else "KARIŞIK"),
        }
        ad_sutunu = model_adi(kosular[0]) + (f" · {a[0]}" if cok_set else "")
        satirlar.append(metrikler.satir(ad_sutunu, a[1], "evet" if a[4] else "hayır", ozet, ek))
        etiket = f"{model_adi(kosular[0])} / {a[0]} / {a[1]}"
        if tarama_notu:
            notlar.append(f"- {etiket}: {tarama_notu}")
        opt = {str(r.get("ayar", {}).get("optimizer", "adamw")).lower() for r in kosular}
        if opt - {"adamw"}:
            notlar.append(f"- {etiket}: optimizer {sorted(opt)} — PROTOKOL madde 7 AdamW ister; "
                          f"makale-sadık koşu ayrı satır olarak etiketlenmeli")
        kapsam = kapsam_uyarisi(kosular)
        if kapsam:
            notlar.append(f"- ⚠ {etiket}: EKSİK — {kapsam} (PROTOKOL madde 5)")
        if len(commitler) > 1:
            notlar.append(f"- ⚠ {etiket}: koşular farklı commit'lerden ({sorted(commitler)})")
        if ek["dis_bacc"] == "—":
            notlar.append(f"- {etiket}: dış test yok (`dis_test.py` ile üret)")
    return satirlar, notlar


# ----------------------------------------------------------------------------- ana
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--kayitlar", default="karsilastirma/kosu_kayitlari")
    p.add_argument("--dis", default="karsilastirma/dis_test")
    p.add_argument("--set", default=None, help="yalnız bu veri seti (ör. adni1)")
    p.add_argument("--gorev", default=None, choices=[None, "ikili", "uc"])
    p.add_argument("--tumu", action="store_true", help="dışlama kurallarını uygulama (hata ayıklama)")
    p.add_argument("--yaz", default=None, help="çıktıyı bu dosyaya da yaz")
    a = p.parse_args(argv)

    klasor = (KOK / a.kayitlar) if not Path(a.kayitlar).is_absolute() else Path(a.kayitlar)
    kayitlar = kayitlari_oku(klasor)
    if not kayitlar:
        print(f"Koşu kaydı bulunamadı: {klasor}\n`egit.py` koştuktan sonra tekrar dene.")
        return
    print(f"{len(kayitlar)} koşu kaydı okundu: {klasor}\n")

    if a.set:
        kayitlar = [k for k in kayitlar if k["set"] == a.set]
    if a.gorev:
        kayitlar = [k for k in kayitlar if k["gorev"] == a.gorev]

    tutulan, atilan = [], []
    for k in kayitlar:
        neden = None if a.tumu else dislama_nedeni(k)
        (atilan if neden else tutulan).append((k, neden))
    if atilan:
        print(f"TABLO DIŞI {len(atilan)} koşu:")
        for k, neden in atilan:
            print(f"  - {k['_dosya']}: {neden}")
        print()
    if not tutulan:
        print("Tabloya girecek koşu kalmadı. `--tumu` ile dışlama kurallarını atlayabilirsin.")
        return

    satirlar, notlar = tablo([k for k, _ in tutulan], dis_test_oku(KOK / a.dis))
    metin = "\n".join(satirlar)
    print(metin)
    if notlar:
        metin += "\n\n**Notlar**\n" + "\n".join(notlar)
        print("\n**Notlar**")
        print("\n".join(notlar))
    if a.yaz:
        yol = (KOK / a.yaz) if not Path(a.yaz).is_absolute() else Path(a.yaz)
        yol.parent.mkdir(parents=True, exist_ok=True)
        yol.write_text(metin + "\n", encoding="utf-8")
        print(f"\nyazıldı: {yol}")


if __name__ == "__main__":
    main()
