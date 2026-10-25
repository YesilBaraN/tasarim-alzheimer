# -*- coding: utf-8 -*-
r"""
test_onisle.py — Sentetik hacimle ön işleme duman testi (veri, HD-BET, internet gerekmez).

Koş: python onisleme\test_onisle.py
Beklenen: her satırda OK, sonda "TÜM TESTLER OK".
HD-BET ve MNI kaydı sentetikte atlanır (ağırlık/şablon indirmesi gerekir); onları gerçek bir hacimle
`python onisleme\onisle.py --girdi <nii> --cikti <klasör>` ile dene.
"""
import sys
import tempfile
from pathlib import Path

import numpy as np
import SimpleITK as sitk

# Windows konsolu Türkçe kod sayfasında (cp1254) açılır; '→', '±', '≈', '≥', '█' gibi karakterler
# UnicodeEncodeError atıp betiği çökertir. Konsolun kendi kodlamasını koruyup kodlanamayan karakteri
# '?' ile değiştiriyoruz (Türkçe harfler doğru görünmeye devam eder). UTF-8 konsolda hiçbir şey değişmez.
for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:  # eski Python, yönlendirilmiş akış ya da reconfigure'ü olmayan sarmalayıcı
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import onisle  # noqa: E402


def sentetik_hacim(boyut=(96, 112, 88), aralik=(1.0, 1.0, 1.2), tohum=2026) -> sitk.Image:
    """Kafatası benzeri kabuk + beyin benzeri küre + yumuşak bias alanı + gürültü."""
    rng = np.random.default_rng(tohum)
    z, y, x = np.indices(boyut).astype(np.float32)
    cz, cy, cx = [b / 2 for b in boyut]
    r = np.sqrt(((z - cz) / (boyut[0] / 2.2)) ** 2 + ((y - cy) / (boyut[1] / 2.2)) ** 2 + ((x - cx) / (boyut[2] / 2.2)) ** 2)
    beyin = (r < 0.8).astype(np.float32) * 100.0
    kabuk = ((r >= 0.9) & (r < 1.0)).astype(np.float32) * 180.0
    bias = 1.0 + 0.3 * (x / boyut[2]) + 0.2 * (y / boyut[1])
    arr = (beyin + kabuk) * bias + rng.normal(0, 5, boyut).astype(np.float32)
    img = sitk.GetImageFromArray(np.clip(arr, 0, None))
    img.SetSpacing(aralik)
    return sitk.Cast(img, sitk.sitkFloat32)


def ok(ad, kosul, detay=""):
    print(f"{'OK ' if kosul else 'HATA'} {ad} {detay}")
    if not kosul:
        raise SystemExit(1)


def main():
    img = sentetik_hacim()
    ok("sentetik hacim", img.GetSize() == (88, 112, 96), str(img.GetSize()))

    maske = onisle.maske_uret_basit(img)
    m = sitk.GetArrayFromImage(maske)
    ok("basit maske", 0.05 < m.mean() < 0.9, f"doluluk={m.mean():.2f}")

    n4 = onisle.n4_duzelt(img, maske, kucultme=2, iterasyon=20, seviye=3)
    a0 = sitk.GetArrayFromImage(img); a1 = sitk.GetArrayFromImage(n4)
    ok("N4 boyut korunur", a1.shape == a0.shape)
    ok("N4 sonlu", np.isfinite(a1).all())

    z = onisle.zscore(n4, maske)
    az = sitk.GetArrayFromImage(z); mm = m > 0
    ok("z-score ortalama≈0", abs(az[mm].mean()) < 1e-3, f"{az[mm].mean():.4f}")
    ok("z-score std≈1", abs(az[mm].std() - 1) < 1e-2, f"{az[mm].std():.4f}")
    ok("maske dışı 0", float(np.abs(az[~mm]).max()) == 0.0)

    kup = onisle.kirp_ve_boyutlandir(z, maske, boyut=64)
    ak = sitk.GetArrayFromImage(kup)
    ok("64³ küp", ak.shape == (64, 64, 64), str(ak.shape))

    with tempfile.TemporaryDirectory() as td:
        g = Path(td) / "sentetik.nii.gz"
        sitk.WriteImage(img, str(g))
        meta = onisle.hacmi_isle(g, Path(td) / "cikti", "sentetik", boyut=64, kafatasi="yok", kayit="yok")
        npy = np.load(Path(td) / "cikti" / "sentetik.npy")
        ok("hat uçtan uca (kafatasi=yok, kayit=yok)", npy.shape == (64, 64, 64) and npy.dtype == np.float16, str(meta["adimlar"]))
        ok("meta json", (Path(td) / "cikti" / "sentetik.json").exists())

    print("TÜM TESTLER OK")


if __name__ == "__main__":
    main()
