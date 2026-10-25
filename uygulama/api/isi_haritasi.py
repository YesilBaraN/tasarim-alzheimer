# -*- coding: utf-8 -*-
r"""
isi_haritasi.py — Karar destek çıktısının "neden" tarafı: modelin hangi bölgelere baktığını gösterir.

Neden ONNX değil de checkpoint: Grad-CAM gradyan ister, ONNX çıkarım grafiği gradyan taşımaz. Bu yüzden
burada `.pth` yüklenir. Tahmin `api/tahmin.py` (ONNX) ile, açıklama bununla üretilir; ikisi aynı modelin
aynı ağırlıklarıdır (`onnx_disa_aktar.py` uyumu 1e-3 altında doğruluyor).

İki yöntem:
  • **grad-cam** — hızlı (tek ileri + tek geri geçiş). Hedef katman verilmezse modeldeki **son Conv3d**
    kendiliğinden bulunur, böylece mimariye özel isim yazmak gerekmez (P01/P02/P06/P07/P12 hepsinde çalışır).
  • **okluzyon** — yavaş ama mimariye hiç bakmaz: hacmi küpler hâlinde kapatıp skorun ne kadar düştüğüne bakar
    (Korolev 2017 ve Zeiler-Fergus usulü). Grad-CAM'in çıktısı şüpheliyse hakem olarak bunu kullan.

Çıktı: `<ad>_<yontem>.npy` (model girdisiyle aynı boyut, 0–1 ölçekli) + istenirse `.png` (üç dik kesit,
hacmin üstüne bindirilmiş). PNG matplotlib gerektirir; yoksa atlanır ve bildirilir.

**Hizalama uyarısı:** `.npy` hacimleri `onisle.py` tarafından MNI152'ye hizalanıp şablonun sınır kutusuna
kırpıldığı için harita **ön işlenmiş hacimle** birebir örtüşür, hastanın ham taramasıyla örtüşmez. Ham
taramaya bindirmek gerekirse `onisle.py --nii` ile kaydedilen hacmi referans al.

Kullanım:
  python uygulama\api\isi_haritasi.py --model ortak --varyant sigcnn ^
      --ckpt karsilastirma\kosu_kayitlari\<kosu>.pth --npy D:\veri\islenmis\RID123.npy --cikti cikti\
  python uygulama\api\isi_haritasi.py --model baran_P02_medicalnet --varyant resnet18 --ckpt <...> ^
      --npy <...> --yontem okluzyon --maske 12 --adim 8 --cikti cikti\
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import torch

# Windows konsolu Türkçe kod sayfasında (cp1254) açılır; kodlanamayan karakter betiği çökertmesin.
for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:
        pass

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
from uygulama.ortak import egit, veri  # noqa: E402


def son_konv_katmani(model: torch.nn.Module) -> str:
    """Modeldeki son Conv3d katmanının adı. Grad-CAM hedefi için mimariye özel isim yazmayı gereksiz kılar."""
    ad = None
    for isim, katman in model.named_modules():
        if isinstance(katman, torch.nn.Conv3d):
            ad = isim
    if ad is None:
        raise SystemExit("modelde Conv3d yok — Grad-CAM uygulanamaz, --yontem okluzyon kullan")
    return ad


def olcekle(h: np.ndarray) -> np.ndarray:
    """0–1 aralığına getir (sabit hacimde bölme hatası olmasın)."""
    h = np.nan_to_num(np.asarray(h, dtype=np.float32))
    alt, ust = float(h.min()), float(h.max())
    return np.zeros_like(h) if ust - alt < 1e-12 else (h - alt) / (ust - alt)


def grad_cam(model: torch.nn.Module, x: torch.Tensor, sinif: int, katman: str | None = None) -> tuple[np.ndarray, str]:
    from monai.visualize import GradCAM

    katman = katman or son_konv_katmani(model)
    cam = GradCAM(nn_module=model, target_layers=katman)
    h = cam(x=x, class_idx=sinif)          # [1,1,D,H,W]
    return olcekle(h[0, 0].detach().cpu().numpy()), katman


def okluzyon(model: torch.nn.Module, x: torch.Tensor, sinif: int, maske: int = 12,
             adim: int = 8) -> tuple[np.ndarray, str]:
    from monai.visualize import OcclusionSensitivity

    oklz = OcclusionSensitivity(nn_module=model, mask_size=maske, n_batch=1, overlap=max(0.0, 1.0 - adim / maske))
    harita, _ = oklz(x=x)                  # [1, sinif, ...]
    h = harita[0, sinif].detach().cpu().numpy()
    if h.shape != tuple(x.shape[2:]):      # kaba ızgarada üretilir → girdi boyutuna büyüt
        t = torch.nn.functional.interpolate(torch.from_numpy(h)[None, None].float(),
                                            size=tuple(x.shape[2:]), mode="trilinear", align_corners=False)
        h = t[0, 0].numpy()
    # Skor düşüşü = önem → işareti çevir ki yüksek değer "önemli" olsun
    return olcekle(-h), f"mask_size={maske}, adim={adim}"


def png_yaz(hacim: np.ndarray, harita: np.ndarray, yol: Path, baslik: str) -> bool:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"PNG atlandı (matplotlib yok: {e}) — .npy yazıldı, istersen `pip install matplotlib`")
        return False
    d, h, w = hacim.shape
    kesitler = [(hacim[d // 2], harita[d // 2], "eksenel"),
                (hacim[:, h // 2], harita[:, h // 2], "koronal"),
                (hacim[:, :, w // 2], harita[:, :, w // 2], "sagital")]
    f, eksenler = plt.subplots(1, 3, figsize=(12, 4.2))
    for eksen, (g, m, ad) in zip(eksenler, kesitler):
        eksen.imshow(np.rot90(g), cmap="gray")
        ort = eksen.imshow(np.rot90(m), cmap="jet", alpha=0.45, vmin=0, vmax=1)
        eksen.set_title(ad); eksen.axis("off")
    f.colorbar(ort, ax=eksenler, fraction=0.025, label="önem (0–1)")
    f.suptitle(baslik, fontsize=10)
    yol.parent.mkdir(parents=True, exist_ok=True)
    f.savefig(yol, dpi=130, bbox_inches="tight"); plt.close(f)
    return True


def uret(model_klasor: str, varyant: str, ckpt: str | Path, npy: str | Path, cikti: str | Path,
         yontem: str = "grad-cam", sinif: int | None = None, katman: str | None = None,
         maske: int = 12, adim: int = 8, png: bool = True) -> dict:
    d = egit.ckpt_yukle(ckpt, torch.device("cpu"))
    gorev = d.get("gorev", "ikili")
    boyut = int(d.get("ayar", {}).get("boyut", 128))
    k = veri.sinif_sayisi(gorev)
    model = egit.model_olustur(model_klasor, varyant, k, boyut, agirlik=None)
    model.load_state_dict(d["model"])
    model.eval()

    arr = np.load(npy).astype(np.float32)
    if arr.shape != (boyut,) * 3:
        raise SystemExit(f"model {boyut}³ bekliyor, hacim {arr.shape}")
    x = torch.from_numpy(arr)[None, None]

    with torch.no_grad():
        olasilik = torch.softmax(model(x).float(), 1)[0].numpy()
    hedef = int(olasilik.argmax()) if sinif is None else int(sinif)

    if yontem == "grad-cam":
        harita, detay = grad_cam(model, x, hedef, katman)
    elif yontem == "okluzyon":
        harita, detay = okluzyon(model, x, hedef, maske, adim)
    else:
        raise SystemExit("yontem: grad-cam | okluzyon")

    # Dosya adına model ve varyant GİRER: aynı hacim için iki modelin haritası birbirini ezmesin
    # (koşu adlarındaki aynı kural). Ortak depoda üç kişi harita üretiyor.
    ad = f"{Path(npy).stem}_{model_klasor}-{varyant}_{yontem}"
    cikti = Path(cikti); cikti.mkdir(parents=True, exist_ok=True)
    npy_yolu = cikti / f"{ad}.npy"
    np.save(npy_yolu, harita.astype(np.float32))
    siniflar = {2: ("NC", "AD"), 3: ("NC", "MCI", "AD")}.get(k, tuple(f"s{i}" for i in range(k)))
    baslik = (f"{model_klasor}/{varyant} · {yontem} ({detay}) · hedef: {siniflar[hedef]} "
              f"(%{100*olasilik[hedef]:.1f})")
    png_yolu = cikti / f"{ad}.png"
    png_oldu = png_yaz(arr, harita, png_yolu, baslik) if png else False

    rapor = {"npy": str(npy_yolu), "png": str(png_yolu) if png_oldu else None, "yontem": yontem,
             "detay": detay, "hedef_sinif": siniflar[hedef], "olasiliklar": dict(zip(siniflar, map(float, olasilik))),
             "harita_ozet": {"ortalama": float(harita.mean()), "tepe_konum": [int(v) for v in np.unravel_index(harita.argmax(), harita.shape)]}}
    print(f"{yontem}: {baslik}")
    print(f"  harita → {npy_yolu.name}" + (f" + {png_yolu.name}" if png_oldu else ""))
    return rapor


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", required=True)
    p.add_argument("--varyant", default="varsayilan")
    p.add_argument("--ckpt", required=True)
    p.add_argument("--npy", required=True, help="onisle.py çıktısı hacim")
    p.add_argument("--cikti", default="cikti/isi_haritalari")
    p.add_argument("--yontem", choices=["grad-cam", "okluzyon"], default="grad-cam")
    p.add_argument("--sinif", type=int, default=None, help="boş: modelin tahmin ettiği sınıf")
    p.add_argument("--katman", default=None, help="Grad-CAM hedef katmanı; boş: son Conv3d")
    p.add_argument("--maske", type=int, default=12, help="okluzyon küp kenarı")
    p.add_argument("--adim", type=int, default=8, help="okluzyon kaydırma adımı")
    p.add_argument("--png", type=int, default=1)
    a = p.parse_args(argv)
    uret(a.model, a.varyant, a.ckpt, a.npy, a.cikti, a.yontem, a.sinif, a.katman, a.maske, a.adim, bool(a.png))


if __name__ == "__main__":
    main()
