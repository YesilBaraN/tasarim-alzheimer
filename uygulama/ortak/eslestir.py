# -*- coding: utf-8 -*-
r"""
eslestir.py — Yaş ve cinsiyet eşleştirilmiş kontrol seçimi (karıştırıcı denetimi).

Neden gerekli: hasta grupları neredeyse her zaman kontrollerden **daha yaşlıdır**. Rastgele kontrol
seçersen model hastalığı değil yaşı öğrenir ve doğruluk yapay olarak yükselir — sonuç "MCI'yi ayırt
ettik" değil, "yaşlıyı ayırt ettik" olur. ds007857'de ölçülen: MCI 74,1 ± 5,4 · CN 71,3 ± 5,1, p = 0,0013.
Cinsiyette de fark vardı (CN %62 kadın, MCI %45).

Yöntem: azınlık sınıfının **tamamı** alınır; her hasta için **aynı cinsiyetten**, yaşı en yakın,
henüz kullanılmamış kontrol seçilir (açgözlü en yakın komşu, `--kaliper` yıl sınırıyla). Hasta başına
`--oran` kadar kontrol alınır. Eşleştirme sonrası yaş farkı yeniden sınanır ve rapor edilir.

Girdi/çıktı: `bolme.py etiket-bids` biçiminde etiket CSV'si (denek_id, dosya, sinif, yas, cinsiyet[, kaynak]).

Kullanım:
  python uygulama\ortak\eslestir.py --etiket veri\ds007857_etiket.csv --cikti veri\ds007857_eslesmis.csv
  python uygulama\ortak\eslestir.py --etiket ... --cikti ... --azinlik 1 --cogunluk 0 --oran 1.5 --kaliper 3
"""
from __future__ import annotations

import argparse
import sys

import numpy as np
import pandas as pd

for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:
        pass

SINIF_AD = {0: "NC", 1: "MCI", 2: "AD"}


def yas_sina(a: pd.Series, b: pd.Series) -> tuple[float, float]:
    """Welch t-testi; scipy yoksa normal yaklaşıklık."""
    a, b = a.dropna(), b.dropna()
    if len(a) < 2 or len(b) < 2:
        return float("nan"), float("nan")
    try:
        from scipy import stats
        t, p = stats.ttest_ind(a, b, equal_var=False)
        return float(t), float(p)
    except Exception:
        fark = a.mean() - b.mean()
        se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
        t = fark / se if se else float("nan")
        from math import erfc, sqrt
        return float(t), float(erfc(abs(t) / sqrt(2)))


def ozet(df: pd.DataFrame, azinlik: int, cogunluk: int, baslik: str) -> None:
    a = df[df["sinif"] == azinlik]
    c = df[df["sinif"] == cogunluk]
    print(f"\n--- {baslik} ---")
    print(f"  {SINIF_AD.get(cogunluk, cogunluk)}: {len(c)}   {SINIF_AD.get(azinlik, azinlik)}: {len(a)}"
          f"   oran {len(c)/max(len(a),1):.2f}:1")
    if "yas" in df.columns:
        ya, yc = pd.to_numeric(a["yas"], errors="coerce"), pd.to_numeric(c["yas"], errors="coerce")
        t, p = yas_sina(yc, ya)
        isaret = "KARIŞTIRICI" if (p == p and p < 0.05) else "dengeli"
        print(f"  yaş: {SINIF_AD.get(cogunluk,cogunluk)} {yc.mean():.1f}±{yc.std():.1f}  "
              f"{SINIF_AD.get(azinlik,azinlik)} {ya.mean():.1f}±{ya.std():.1f}   t={t:.2f} p={p:.4f}  → {isaret}")
    if "cinsiyet" in df.columns and df["cinsiyet"].notna().any():
        tab = pd.crosstab(df["sinif"].map(lambda s: SINIF_AD.get(s, s)), df["cinsiyet"])
        oranlar = (tab.T / tab.sum(axis=1)).T
        print("  cinsiyet (%):")
        for satir in (oranlar * 100).round(0).astype(int).to_string().splitlines():
            print("   ", satir)


def eslestir(df: pd.DataFrame, azinlik: int, cogunluk: int, oran: float, kaliper: float,
             tohum: int) -> pd.DataFrame:
    rng = np.random.default_rng(tohum)
    hastalar = df[df["sinif"] == azinlik].copy()
    havuz = df[df["sinif"] == cogunluk].copy()
    havuz["yas_n"] = pd.to_numeric(havuz["yas"], errors="coerce")
    hastalar["yas_n"] = pd.to_numeric(hastalar["yas"], errors="coerce")

    # Hastaları rastgele sırayla gez (sıra etkisini tohuma bağla)
    sira = rng.permutation(len(hastalar))
    kullanilan: set = set()
    secilen: list = []
    hedef = int(round(len(hastalar) * oran))

    for tur in range(int(np.ceil(oran))):
        for i in sira:
            if len(secilen) >= hedef:
                break
            h = hastalar.iloc[i]
            aday = havuz[(~havuz["denek_id"].isin(kullanilan))]
            if "cinsiyet" in havuz.columns and pd.notna(h.get("cinsiyet")):
                ayni = aday[aday["cinsiyet"] == h["cinsiyet"]]
                if len(ayni):
                    aday = ayni
            if pd.notna(h["yas_n"]) and aday["yas_n"].notna().any():
                fark = (aday["yas_n"] - h["yas_n"]).abs()
                aday = aday[fark <= kaliper] if (fark <= kaliper).any() else aday.loc[[fark.idxmin()]]
                if len(aday) > 1:
                    aday = aday.loc[[(aday["yas_n"] - h["yas_n"]).abs().idxmin()]]
            if not len(aday):
                continue
            s = aday.iloc[0]
            kullanilan.add(s["denek_id"])
            secilen.append(s)
    kontroller = pd.DataFrame(secilen).drop(columns=["yas_n"], errors="ignore")
    return pd.concat([hastalar.drop(columns=["yas_n"], errors="ignore"), kontroller], ignore_index=True)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--etiket", required=True)
    p.add_argument("--cikti", required=True)
    p.add_argument("--azinlik", type=int, default=1, help="hasta sınıfı (0 NC, 1 MCI, 2 AD)")
    p.add_argument("--cogunluk", type=int, default=0, help="kontrol sınıfı")
    p.add_argument("--oran", type=float, default=1.5, help="hasta başına kontrol sayısı")
    p.add_argument("--kaliper", type=float, default=3.0, help="izin verilen yaş farkı (yıl)")
    p.add_argument("--tohum", type=int, default=2026)
    a = p.parse_args(argv)

    df = pd.read_csv(a.etiket)
    df = df[df["sinif"].isin([a.azinlik, a.cogunluk])].copy()
    ozet(df, a.azinlik, a.cogunluk, "ESLESTIRME ÖNCESİ (tüm havuz)")

    yeni = eslestir(df, a.azinlik, a.cogunluk, a.oran, a.kaliper, a.tohum)
    ozet(yeni, a.azinlik, a.cogunluk, "ESLESTIRME SONRASI (seçilen alt küme)")

    yeni.to_csv(a.cikti, index=False)
    print(f"\n{len(yeni)} denek → {a.cikti}")
    print("Not: eşleştirme yaşı ve cinsiyeti dengeler, tarayıcı/merkez etkisini dengelemez — o ayrı "
          "(kohort sütunu ve `bolme.py` kohort dengeli katları).")


if __name__ == "__main__":
    main()
