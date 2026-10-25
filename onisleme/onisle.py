# -*- coding: utf-8 -*-
"""
onisle.py — T1 sMRI ön işleme hattı (kafatası ayıklama → N4 → MNI152 afin kayıt → z-score → 128³).

`--kafatasi hazir --kayit yok`: kaynak veri **zaten** kafatası ayıklanmış ve MNI'ye hizalanmışsa
(ör. `radiata-ai/brain-structure`) HD-BET, N4 ve kayıt atlanır; yalnız maske (voksel > 0), maske içi
z-score ve kırpma/yeniden boyutlandırma uygulanır. Hacim başına saniyeler sürer. PROTOKOL madde 3
bozulmaz: tüm veri aynı kaynaktan ve aynı hatla geldiği sürece herkes aynı girdiyi görür.

Adım sırası Wen 2020'nin t1-linear hattıyla aynı: normalizasyon **kayıttan sonra** yapılır. Kayıt doğal
yoğunluklarla çalışır, z-score ise son ızgarada şablonun beyin maskesi içinde hesaplanır (herkeste aynı maske).

Kullanım:
  python onisle.py --girdi <nii|img|dicom_klasörü> --cikti <klasör> --ad <isim>
  python onisle.py --girdi <klasör> --cikti <klasör> --toplu        # klasördeki tüm .nii/.nii.gz
Seçenekler:
  --boyut 128            çıktı küp kenarı
  --kafatasi hdbet|yok   (varsayılan hdbet)
  --kayit sitk|ants|yok  (varsayılan sitk)
  --cihaz cpu|0          HD-BET cihazı (varsayılan cpu)
  --nii                  .npy yanında .nii.gz de yaz
Her adım ayrı fonksiyondur; test_onisle.py bunları sentetik hacimle çağırır.
Bağımlılıklar: SimpleITK, nibabel, numpy, (hd-bet CLI), (templateflow), (dcm2niix).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
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

SABLON_ADI = "MNI152NLin2009cAsym"

def arac_bul(komut: str) -> str | None:
    r"""Harici aracı bul. PATH'te yoksa ÇALIŞAN Python'un yanına bakar.

    Sebep: `.venv\Scripts\python.exe onisle.py` gibi venv'i aktive etmeden koşturmak çok yaygın;
    o durumda venv'in Scripts klasörü PATH'te olmaz ve `shutil.which("hd-bet")` None döner, araç
    kurulu olduğu hâlde "bulunamadı" hatası alınır.
    """
    yol = shutil.which(komut)
    if yol:
        return yol
    yan = Path(sys.executable).parent
    for aday in (yan / komut, yan / f"{komut}.exe", yan / "Scripts" / komut, yan / "Scripts" / f"{komut}.exe"):
        if aday.exists():
            return str(aday)
    return None


# ----------------------------------------------------------------------------- okuma
# ----------------------------------------------------------------------------- ASCII olmayan yollar
# ITK'nin Windows dosya okuyucusu ASCII olmayan yolları açamıyor: "Baran Yeşilyurt" gibi bir kullanıcı
# klasöründe `sitk.ReadImage` "Unable to open ... for reading" der, dosya sağlam olsa bile. (nibabel
# sorunsuz okur, çünkü Python'un kendi dosya katmanını kullanır.) Sentetik testler ASCII geçici klasörde
# koştuğu için bu hata uzun süre görünmedi. Çözüm iki aşamalı:
#   1. Windows 8.3 kısa adına çevir (C:\Users\Baran Yeşilyurt\… → C:\Users\BARANY~1\…) — kopya yok.
#   2. Kısa ad üretilemiyorsa (8.3 kapalı olabilir) geçici ASCII klasöre kopyala.

def _kisa_yol(yol: str) -> str:
    """Windows 8.3 kısa adı. Dosya/klasör var olmalı; üretilemezse yolu olduğu gibi döner."""
    if os.name != "nt":
        return yol
    import ctypes
    from ctypes import wintypes
    try:
        f = ctypes.windll.kernel32.GetShortPathNameW
        f.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
        f.restype = wintypes.DWORD
        tampon = ctypes.create_unicode_buffer(32768)
        if f(yol, tampon, 32768):
            return tampon.value
    except Exception:
        pass
    return yol


def _ascii_aday(yol: str) -> str | None:
    """Yalnız KLASÖRÜ 8.3 kısa adına çevirir, dosya adını korur.

    Dosyanın kendisini kısaltmak uzantıyı da kısaltıyor (`sub-01_ses-01_T1w.nii.gz` → `SUB-01~1.GZ`)
    ve ITK `.nii.gz` göremeyince "Unable to determine ImageIO reader" der. Uzantı korunmalı.
    """
    ad = Path(yol).name
    if not ad.isascii():
        return None
    aday = str(Path(_kisa_yol(str(Path(yol).parent))) / ad)
    return aday if aday.isascii() else None


def dis_arac_yolu(yol) -> str:
    """Alt sürece (hd-bet, dcm2niix) verilecek yol.

    ASCII ise olduğu gibi bırakılır — geçici klasörler zaten ASCII olur. Değilse yalnız klasör
    kısaltılır; dosyayı kısaltmak uzantıyı yok eder ve araç dosyayı tanıyamaz.
    """
    y = str(yol)
    return y if y.isascii() else (_ascii_aday(y) or y)


def sitk_oku(yol) -> sitk.Image:
    """ASCII olmayan yolda da çalışan sitk.ReadImage."""
    y = str(yol)
    if y.isascii():
        return sitk.ReadImage(y)
    aday = _ascii_aday(y)
    if aday:
        return sitk.ReadImage(aday)
    gecici = Path(tempfile.mkdtemp(prefix="itk_"))          # son çare: ASCII klasöre kopyala
    try:
        kopya = gecici / ("girdi" + "".join(Path(y).suffixes[-2:]))
        shutil.copy2(y, kopya)
        k2 = str(kopya)
        return sitk.ReadImage(k2 if k2.isascii() else (_ascii_aday(k2) or k2))
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


def sitk_yaz(img: sitk.Image, yol) -> None:
    """ASCII olmayan yolda da çalışan sitk.WriteImage (dosya henüz yokken kısa ad üretilemez →
    önce ASCII geçiciye yazıp sonra Python ile taşır; shutil Unicode yolu sorunsuz işler)."""
    y = str(yol)
    if y.isascii():
        sitk.WriteImage(img, y)
        return
    aday = _ascii_aday(y)                                   # klasör var → kısa adı alınabilir
    if aday:
        sitk.WriteImage(img, aday)
        return
    gecici = Path(tempfile.mkdtemp(prefix="itk_"))
    try:
        gec_dosya = gecici / ("cikti" + "".join(Path(y).suffixes[-2:]))
        sitk.WriteImage(img, str(gec_dosya))
        shutil.move(str(gec_dosya), y)
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


def oku(yol: Path) -> sitk.Image:
    """NIfTI / Analyze (.img+.hdr) / tek DICOM klasörü okur, LPS'e yönlendirir, float32 döner."""
    yol = Path(yol)
    if yol.is_dir():
        nii = dicomdan_nifti(yol)
        img = sitk_oku(nii)
    else:
        img = sitk_oku(yol)
    img = sitk.Cast(img, sitk.sitkFloat32)
    img = sitk.DICOMOrient(img, "LPS")
    return img


def dicomdan_nifti(klasor: Path) -> Path:
    """dcm2niix ile DICOM klasörünü geçici NIfTI'ye çevirir."""
    exe = arac_bul("dcm2niix")
    if exe is None:
        raise RuntimeError("dcm2niix bulunamadı: pip install dcm2niix")
    gecici = Path(tempfile.mkdtemp(prefix="dcm2niix_"))
    subprocess.run([exe, "-z", "y", "-f", "hacim", "-o", dis_arac_yolu(gecici), dis_arac_yolu(klasor)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    adaylar = sorted(gecici.glob("*.nii.gz"))
    if not adaylar:
        raise RuntimeError("dcm2niix çıktı üretmedi")
    return adaylar[0]


# ----------------------------------------------------------------------------- kafatası
def hdbet_cihaz(cihaz) -> str:
    """HD-BET 2.x `-device` değerini doğrudan `torch.device()`'a veriyor.

    Eski (1.x) yazım `-device 0` artık `RuntimeError: Invalid device string: '0'` atıyor; `cuda:0` gerekiyor.
    Belgelerde ve alışkanlıkta `--cihaz 0` kaldığı için burada çeviriyoruz: 0 → cuda:0, gpu/cuda → cuda,
    cpu → cpu, geri kalanı olduğu gibi.
    """
    c = str(cihaz).strip().lower()
    if c.isdigit():
        return f"cuda:{c}"
    if c in ("gpu", "cuda"):
        return "cuda"
    return c


def kafatasi_ayikla(img: sitk.Image, cihaz: str = "cpu") -> tuple[sitk.Image, sitk.Image]:
    """HD-BET CLI ile beyin görüntüsü + ikili maske döner. Maske = beyin > 0 (dosya adına bağımlı değil)."""
    exe = arac_bul("hd-bet")
    if exe is None:
        raise RuntimeError("hd-bet bulunamadı: pip install hd-bet (önce torch). "
                           "Kuruluysa venv'i aktive et ya da bu betiği venv'in python'uyla koş.")
    gecici = Path(tempfile.mkdtemp(prefix="hdbet_"))
    girdi = gecici / "girdi.nii.gz"
    cikti = gecici / "beyin.nii.gz"
    sitk_yaz(img, girdi)
    c = hdbet_cihaz(cihaz)
    komut = [exe, "-i", dis_arac_yolu(girdi), "-o", dis_arac_yolu(cikti), "-device", c]
    if c == "cpu":
        komut += ["--disable_tta"]
    subprocess.run(komut, check=True)
    beyin = sitk.Cast(sitk_oku(cikti), sitk.sitkFloat32)
    maske = sitk.Cast(beyin > 0, sitk.sitkUInt8)
    return beyin, maske


def maske_hazir(img: sitk.Image) -> sitk.Image:
    """Zaten kafatası ayıklanmış hacimde maske = sıfırdan büyük vokseller.

    Eşik tahmini gerekmiyor: ayıklama sırasında arka plan tam sıfıra çekilmiş oluyor.
    `maske_uret_basit`in yüzdelik eşiği burada beyin kenarlarını kırpardı.
    """
    arr = sitk.GetArrayFromImage(img)
    maske = sitk.GetImageFromArray((arr > 0).astype(np.uint8))
    maske.CopyInformation(img)
    return maske


def maske_uret_basit(img: sitk.Image) -> sitk.Image:
    """HD-BET yokken (ör. OASIS t88_masked dosyaları, sentetik test) basit eşik maskesi."""
    arr = sitk.GetArrayFromImage(img)
    esik = np.percentile(arr[arr > 0], 5) if np.any(arr > 0) else 0.0
    maske = sitk.GetImageFromArray((arr > esik).astype(np.uint8))
    maske.CopyInformation(img)
    maske = sitk.BinaryFillhole(maske)
    return maske


# ----------------------------------------------------------------------------- N4
def n4_duzelt(img: sitk.Image, maske: sitk.Image, kucultme: int = 2, iterasyon: int = 50, seviye: int = 4) -> sitk.Image:
    """SimpleITK N4 bias alanı düzeltmesi (maske içinde, küçültülmüş ızgarada hızlı)."""
    kucuk = sitk.Shrink(img, [kucultme] * img.GetDimension())
    kucuk_maske = sitk.Shrink(maske, [kucultme] * img.GetDimension())
    n4 = sitk.N4BiasFieldCorrectionImageFilter()
    n4.SetMaximumNumberOfIterations([iterasyon] * seviye)
    n4.Execute(kucuk, kucuk_maske)
    log_bias = n4.GetLogBiasFieldAsImage(img)
    duzeltilmis = img / sitk.Exp(log_bias)
    return sitk.Cast(duzeltilmis, sitk.sitkFloat32)


# ----------------------------------------------------------------------------- normalizasyon
def zscore(img: sitk.Image, maske: sitk.Image, kirp: float = 5.0) -> sitk.Image:
    """Maske içi z-score; maske dışı 0; [-kirp, kirp] aralığına kırpılır."""
    arr = sitk.GetArrayFromImage(img).astype(np.float32)
    m = sitk.GetArrayFromImage(maske) > 0
    if m.sum() < 10:
        raise ValueError("maske boş")
    mu, sd = float(arr[m].mean()), float(arr[m].std() + 1e-8)
    cikti = np.zeros_like(arr, dtype=np.float32)
    cikti[m] = np.clip((arr[m] - mu) / sd, -kirp, kirp)
    out = sitk.GetImageFromArray(cikti)
    out.CopyInformation(img)
    return out


# ----------------------------------------------------------------------------- MNI kayıt
def sablon_getir(ad: str = SABLON_ADI) -> sitk.Image:
    """TemplateFlow'dan 1 mm beyin şablonunu indirir/önbellekten okur."""
    try:
        from templateflow import api as tf
    except ImportError as e:
        raise RuntimeError("templateflow bulunamadı: pip install templateflow") from e
    yol = tf.get(ad, resolution=1, desc="brain", suffix="T1w", extension="nii.gz")
    if isinstance(yol, list):
        yol = yol[0]
    sab = sitk.Cast(sitk_oku(yol), sitk.sitkFloat32)
    return sitk.DICOMOrient(sab, "LPS")


def mni_kayit_sitk(hareketli: sitk.Image, sablon: sitk.Image) -> tuple[sitk.Image, float]:
    """Afin kayıt (Mattes MI, 3 seviye); şablon ızgarasına yeniden örnekler. Son metrik değerini döner."""
    # GEOMETRY (fiziksel merkezleri hizalar), MOMENTS değil: MOMENTS yoğunluk ağırlıklı kütle merkezi
    # hesaplar ve kafatası ayıklanmış/normalize edilmiş hacimlerde (negatif değerler, geniş sıfır arka plan)
    # merkezi tamamen kaçırıp "images do not sufficiently overlap" hatasına yol açar.
    baslangic = sitk.CenteredTransformInitializer(
        sablon, hareketli, sitk.AffineTransform(3), sitk.CenteredTransformInitializerFilter.GEOMETRY)
    reg = sitk.ImageRegistrationMethod()
    reg.SetMetricAsMattesMutualInformation(numberOfHistogramBins=32)
    reg.SetMetricSamplingStrategy(reg.RANDOM)
    reg.SetMetricSamplingPercentage(0.2, seed=2026)
    reg.SetInterpolator(sitk.sitkLinear)
    reg.SetOptimizerAsRegularStepGradientDescent(learningRate=1.0, minStep=1e-4, numberOfIterations=200,
                                                 relaxationFactor=0.5, gradientMagnitudeTolerance=1e-6)
    reg.SetOptimizerScalesFromPhysicalShift()
    reg.SetShrinkFactorsPerLevel([4, 2, 1])
    reg.SetSmoothingSigmasPerLevel([2, 1, 0])
    reg.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()
    reg.SetInitialTransform(baslangic, inPlace=False)
    donusum = reg.Execute(sablon, hareketli)
    kayitli = sitk.Resample(hareketli, sablon, donusum, sitk.sitkLinear, 0.0, sitk.sitkFloat32)
    return kayitli, float(reg.GetMetricValue())


def mni_kayit_ants(hareketli: sitk.Image, sablon: sitk.Image) -> tuple[sitk.Image, float]:
    """İsteğe bağlı ANTsPy yolu (Windows tekerleği varsa)."""
    try:
        import ants  # noqa: F401
    except ImportError as e:
        raise RuntimeError("antspyx bulunamadı; --kayit sitk kullan") from e
    import ants as _ants
    gecici = Path(tempfile.mkdtemp(prefix="ants_"))
    sitk_yaz(hareketli, gecici / "h.nii.gz")
    sitk_yaz(sablon, gecici / "s.nii.gz")
    h = _ants.image_read(str(gecici / "h.nii.gz"))
    s = _ants.image_read(str(gecici / "s.nii.gz"))
    r = _ants.registration(fixed=s, moving=h, type_of_transform="Affine")
    _ants.image_write(r["warpedmovout"], str(gecici / "k.nii.gz"))
    kayitli = sitk.Cast(sitk_oku(gecici / "k.nii.gz"), sitk.sitkFloat32)
    return kayitli, float("nan")


# ----------------------------------------------------------------------------- boyut
def sinir_kutusu(maske: sitk.Image, pay: int = 4) -> tuple[list[int], list[int]]:
    arr = sitk.GetArrayFromImage(maske) > 0
    if not arr.any():
        raise ValueError("maske boş; sınır kutusu yok")
    zyx = np.argwhere(arr)
    lo = np.maximum(zyx.min(0) - pay, 0)
    hi = np.minimum(zyx.max(0) + pay + 1, arr.shape)
    # SimpleITK indeksleri x,y,z sırasındadır
    return [int(lo[2]), int(lo[1]), int(lo[0])], [int(hi[2] - lo[2]), int(hi[1] - lo[1]), int(hi[0] - lo[0])]


def kirp_ve_boyutlandir(img: sitk.Image, maske: sitk.Image, boyut: int = 128) -> sitk.Image:
    """Maske sınır kutusuna kırpar, sonra boyut³ küpe yeniden örnekler (izotropik olmayan ölçek)."""
    baslangic, uzunluk = sinir_kutusu(maske)
    kirpik = sitk.RegionOfInterest(img, uzunluk, baslangic)
    return yeniden_boyutlandir(kirpik, boyut)


def yeniden_boyutlandir(img: sitk.Image, boyut: int = 128) -> sitk.Image:
    eski_boyut = np.array(img.GetSize(), dtype=float)
    eski_aralik = np.array(img.GetSpacing(), dtype=float)
    yeni_boyut = [boyut] * 3
    yeni_aralik = (eski_boyut * eski_aralik / boyut).tolist()
    return sitk.Resample(img, yeni_boyut, sitk.Transform(), sitk.sitkLinear, img.GetOrigin(),
                         yeni_aralik, img.GetDirection(), 0.0, sitk.sitkFloat32)


# ----------------------------------------------------------------------------- hat
def hacmi_isle(girdi: Path, cikti_klasor: Path, ad: str, boyut: int = 128, kafatasi: str = "hdbet",
               kayit: str = "sitk", cihaz: str = "cpu", nii_yaz: bool = False, sablon: sitk.Image | None = None) -> dict:
    t0 = time.time()
    meta = {"ad": ad, "girdi": str(girdi), "adimlar": [], "uyarilar": [], "parametreler":
            {"boyut": boyut, "kafatasi": kafatasi, "kayit": kayit, "sablon": SABLON_ADI if kayit != "yok" else None}}
    sureler = {}

    t = time.time(); img = oku(girdi); sureler["oku"] = time.time() - t
    meta["adimlar"].append("oku"); meta["girdi_boyut"] = list(img.GetSize()); meta["girdi_aralik"] = list(img.GetSpacing())

    t = time.time()
    if kafatasi == "hazir":
        maske = maske_hazir(img)          # ayıklama ve hizalama veri kaynağında yapılmış
    elif kafatasi == "hdbet":
        img, maske = kafatasi_ayikla(img, cihaz)
    else:
        maske = maske_uret_basit(img)
    sureler["kafatasi"] = time.time() - t; meta["adimlar"].append(f"kafatasi:{kafatasi}")
    hacim_cm3 = float(sitk.GetArrayFromImage(maske).sum() * np.prod(img.GetSpacing()) / 1000.0)
    meta["maske_hacmi_cm3"] = round(hacim_cm3, 1)
    if not (900 <= hacim_cm3 <= 1900) and kafatasi == "hdbet":
        meta["uyarilar"].append("maske_hacmi")

    if kafatasi == "hazir":
        meta["adimlar"].append("n4:atlandi")   # kaynak hattı bias düzeltmesini zaten uygulamış
    else:
        t = time.time(); img = n4_duzelt(img, maske); sureler["n4"] = time.time() - t; meta["adimlar"].append("n4")

    # SIRA: kafatası → N4 → **kayıt** → z-score → kırpma. Normalizasyon kayıttan SONRA yapılır
    # (Wen 2020 t1-linear ile aynı): kayıt doğal yoğunluklarla çalışır ve z-score son ızgarada,
    # şablonun beyin maskesi içinde hesaplanır — böylece herkeste aynı maske kullanılır.
    if kayit != "yok":
        t = time.time()
        if sablon is None:
            sablon = sablon_getir()
        if kayit == "ants":
            img, metrik = mni_kayit_ants(img, sablon)
        else:
            img, metrik = mni_kayit_sitk(img, sablon)
        # Kayıt sonrası kırpma kutusu herkeste AYNI olmalı (PROTOKOL madde 3) → deneğin maskesini şablon
        # ızgarasına taşımak yerine doğrudan şablonun beyin maskesi kullanılır.
        maske = sitk.Cast(sablon > 0, sitk.sitkUInt8)
        sureler["kayit"] = time.time() - t; meta["adimlar"].append(f"kayit:{kayit}"); meta["kayit_metrik"] = metrik
        if metrik == metrik and metrik > -0.2:  # Mattes MI negatif; sıfıra yakınsa kötü
            meta["uyarilar"].append("kayit")

    t = time.time(); img = zscore(img, maske); sureler["zscore"] = time.time() - t; meta["adimlar"].append("zscore")
    t = time.time(); img = kirp_ve_boyutlandir(img, maske, boyut); sureler["boyut"] = time.time() - t; meta["adimlar"].append(f"boyut:{boyut}")

    arr = sitk.GetArrayFromImage(img).astype(np.float32)
    if not np.isfinite(arr).all():
        meta["uyarilar"].append("nan_inf"); arr = np.nan_to_num(arr)
    meta["istatistik"] = {"min": float(arr.min()), "max": float(arr.max()), "mean": float(arr.mean()), "std": float(arr.std())}
    meta["cikti_boyut"] = list(arr.shape); meta["sureler_sn"] = {k: round(v, 1) for k, v in sureler.items()}
    meta["toplam_sn"] = round(time.time() - t0, 1)

    cikti_klasor = Path(cikti_klasor); cikti_klasor.mkdir(parents=True, exist_ok=True)
    np.save(cikti_klasor / f"{ad}.npy", arr.astype(np.float16))
    (cikti_klasor / f"{ad}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    if nii_yaz:
        sitk_yaz(img, cikti_klasor / f"{ad}.nii.gz")
    return meta


def liste_oku(yol: Path) -> set[str]:
    """İşlenecek dosya adlarını okur: etiket CSV'si (`dosya` sütunu) ya da satır satır düz metin.

    Neden: eşleştirilmiş alt küme (`eslestir.py` çıktısı) klasörün tamamı değil; 287 hacmin 123'ünü
    işlemek gerekiyor. Klasörü kopyalamak yerine listeyi süzüyoruz.
    """
    yol = Path(yol)
    if yol.suffix.lower() == ".csv":
        import csv
        with open(yol, encoding="utf-8", newline="") as f:
            satirlar = list(csv.DictReader(f))
        sutun = "dosya" if satirlar and "dosya" in satirlar[0] else None
        if sutun is None:
            raise SystemExit(f"{yol}: 'dosya' sütunu yok")
        return {Path(r[sutun]).name for r in satirlar if r.get(sutun)}
    return {Path(x.strip()).name for x in yol.read_text(encoding="utf-8").splitlines() if x.strip()}


def toplu(girdi_klasor: Path, cikti_klasor: Path, liste: Path | None = None, **kw) -> list[dict]:
    dosyalar = sorted(list(Path(girdi_klasor).rglob("*.nii.gz")) + list(Path(girdi_klasor).rglob("*.nii")))
    if liste is not None:
        istenen = liste_oku(liste)
        once = len(dosyalar)
        dosyalar = [d for d in dosyalar if d.name in istenen]
        bulunamayan = istenen - {d.name for d in dosyalar}
        print(f"liste süzgeci: {once} dosyadan {len(dosyalar)} tanesi işlenecek"
              + (f"; listede olup klasörde bulunamayan {len(bulunamayan)}: {sorted(bulunamayan)[:5]}"
                 if bulunamayan else ""))
    sablon = sablon_getir() if kw.get("kayit", "sitk") != "yok" else None
    sonuc = []
    for i, d in enumerate(dosyalar, 1):
        ad = d.name.replace(".nii.gz", "").replace(".nii", "")
        if (Path(cikti_klasor) / f"{ad}.npy").exists():
            print(f"[{i}/{len(dosyalar)}] atlandı (var): {ad}"); continue
        try:
            m = hacmi_isle(d, cikti_klasor, ad, sablon=sablon, **kw)
            print(f"[{i}/{len(dosyalar)}] {ad}: {m['toplam_sn']} sn, uyarı={m['uyarilar'] or '-'}")
            sonuc.append(m)
        except Exception as e:  # tek hacim hatası toplu işi durdurmaz; kayda geçer
            print(f"[{i}/{len(dosyalar)}] HATA {ad}: {e}", file=sys.stderr)
            sonuc.append({"ad": ad, "hata": str(e)})
    (Path(cikti_klasor) / "_toplu_ozet.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    return sonuc


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--girdi", required=True)
    p.add_argument("--cikti", required=True)
    p.add_argument("--ad", default=None)
    p.add_argument("--toplu", action="store_true")
    p.add_argument("--liste", default=None, help="yalnız bu listedeki dosyalar (etiket CSV'si ya da düz metin)")
    p.add_argument("--boyut", type=int, default=128)
    p.add_argument("--kafatasi", choices=["hdbet", "yok", "hazir"], default="hdbet",
                   help="hazir: veri zaten ayıklanmış ve hizalanmış (ör. radiata-ai/brain-structure) → "
                        "yalnız maske + z-score + kırpma/boyutlandırma")
    p.add_argument("--kayit", choices=["sitk", "ants", "yok"], default="sitk")
    p.add_argument("--cihaz", default="cpu")
    p.add_argument("--nii", action="store_true")
    a = p.parse_args(argv)
    kw = dict(boyut=a.boyut, kafatasi=a.kafatasi, kayit=a.kayit, cihaz=a.cihaz, nii_yaz=a.nii)
    if a.toplu:
        toplu(Path(a.girdi), Path(a.cikti), liste=Path(a.liste) if a.liste else None, **kw)
    else:
        ad = a.ad or Path(a.girdi).name.split(".")[0]
        m = hacmi_isle(Path(a.girdi), Path(a.cikti), ad, **kw)
        print(json.dumps(m, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
