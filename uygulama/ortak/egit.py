# -*- coding: utf-8 -*-
r"""
egit.py — Ortak eğitim döngüsü (PROTOKOL madde 5–7, 10). Her model aynı döngü, aynı bütçe.

Kullanım (proje kökünden):
  python uygulama\ortak\egit.py --model baran_P01_korolev --varyant resnet --set oasis1 --gorev ikili --kat 0 --tohum 2026 --veri D:\veri\oasis1\islenmis
  python uygulama\ortak\egit.py --model baran_P02_medicalnet --varyant resnet18 --agirlik uygulama\baran_P02_medicalnet\agirliklar\resnet_18_23dataset.pth ...
  --tum_katlar  → 5 katı sırayla koşar;  --tohumlar 2026 2027 2028 → üç tohum
  --lrler 1e-3 3e-4 1e-4  → PROTOKOL madde 7 LR taraması; her LR KENDİ koşu adıyla kaydedilir (çakışma yok)
  --etiket ablation-cevirsiz → koşu adına ek etiket;  --sifirdan → mevcut checkpoint'i yok sayıp baştan eğit
Model sözleşmesi: uygulama/<model>/model.py içinde  olustur(varyant: str, sinif_sayisi: int, girdi_boyut: int, **kw) -> torch.nn.Module
Çıktı: karsilastirma/kosu_kayitlari/<model>-<varyant>_<set>_<gorev>_t<tohum>_k<kat>_lr<lr>_b<boyut>[_<etiket>].json
       + <ad>.pth (en iyi doğrulama BAcc) ve <ad>_son.pth (her epoch; kesintiden devam)
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

# Windows konsolu Türkçe kod sayfasında (cp1254) açılır; '→', '±', '≈', '≥', '█' gibi karakterler
# UnicodeEncodeError atıp betiği çökertir. Konsolun kendi kodlamasını koruyup kodlanamayan karakteri
# '?' ile değiştiriyoruz (Türkçe harfler doğru görünmeye devam eder). UTF-8 konsolda hiçbir şey değişmez.
for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:  # eski Python, yönlendirilmiş akış ya da reconfigure'ü olmayan sarmalayıcı
        pass

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
from uygulama.ortak import metrikler, veri  # noqa: E402

VARSAYILAN = dict(epoch=100, lr=3e-4, batch=4, accum=1, sabir=15, wd=1e-4, amp=True, boyut=128, isci=2,
                  optimizer="adamw")


def optimizer_olustur(ad: str, parametreler, lr: float, wd: float):
    """PROTOKOL madde 7 tabloya giren koşularda AdamW ister; adam/sgd yalnız makale-sadık kontrol koşuları için."""
    ad = str(ad).lower()
    if ad == "adamw":
        return torch.optim.AdamW(parametreler, lr=lr, weight_decay=wd)
    if ad == "adam":
        return torch.optim.Adam(parametreler, lr=lr, weight_decay=wd)
    if ad in ("sgd", "sgd_nesterov", "nesterov"):
        return torch.optim.SGD(parametreler, lr=lr, momentum=0.9, nesterov=True, weight_decay=wd)
    raise ValueError("optimizer: adamw | adam | sgd")


def grad_scaler(etkin: bool):
    """torch ≥2.4'te torch.cuda.amp.GradScaler deprecated → torch.amp.GradScaler('cuda', ...)."""
    try:
        return torch.amp.GradScaler("cuda", enabled=etkin)
    except (AttributeError, TypeError):
        return torch.cuda.amp.GradScaler(enabled=etkin)


def ckpt_yukle(yol, cihaz):
    """Kendi checkpoint'imiz: weights_only=False gerekir (ayar/gecmis gibi düz Python nesneleri taşır)."""
    try:
        return torch.load(yol, map_location=cihaz, weights_only=False)
    except TypeError:  # weights_only parametresi olmayan eski torch
        return torch.load(yol, map_location=cihaz)


def tohum_sabitle(t: int):
    random.seed(t); np.random.seed(t); torch.manual_seed(t); torch.cuda.manual_seed_all(t)
    torch.backends.cudnn.deterministic = True; torch.backends.cudnn.benchmark = False
    os.environ["PYTHONHASHSEED"] = str(t)


def model_olustur(model_klasor: str, varyant: str, sinif_sayisi: int, girdi_boyut: int, **kw) -> nn.Module:
    mod = importlib.import_module(f"uygulama.{model_klasor}.model")
    return mod.olustur(varyant=varyant, sinif_sayisi=sinif_sayisi, girdi_boyut=girdi_boyut, **kw)


def commit_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=KOK, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "git-yok"


def surumler() -> dict:
    """PROTOKOL madde 10: her sonucun yanında sürümler bulunur (pip freeze yerine ilgili paketler)."""
    import importlib.metadata as md

    out = {"python": sys.version.split()[0], "torch": torch.__version__,
           "cuda": torch.version.cuda or "-", "cudnn": str(torch.backends.cudnn.version() or "-")}
    for ad in ("monai", "numpy", "scikit-learn", "pandas", "SimpleITK", "nibabel", "onnxruntime"):
        try:
            out[ad] = md.version(ad)
        except Exception:
            out[ad] = "-"
    return out


@torch.no_grad()
def degerlendir(model, yukleyici, cihaz, gorev, amp=True):
    model.eval(); probs, ys = [], []
    for x, y, _ in yukleyici:
        x = x.to(cihaz, non_blocking=True)
        with torch.autocast(device_type=cihaz.type, enabled=(amp and cihaz.type == "cuda")):
            out = model(x)
        probs.append(torch.softmax(out.float(), 1).cpu().numpy()); ys.append(np.asarray(y))
    return metrikler.hesapla(np.concatenate(ys), np.concatenate(probs), gorev)


def egit(model_klasor: str, varyant: str, set_adi: str, gorev: str, kat: int, tohum: int, veri_kok: str,
         bolme_klasor: str = "veri/bolme", cikti_klasor: str = "karsilastirma/kosu_kayitlari", agirlik: str | None = None,
         etiket: str = "", sifirdan: bool = False, **ayar) -> dict:
    a = {**VARSAYILAN, **{k: v for k, v in ayar.items() if v is not None}}
    tohum_sabitle(tohum)
    cihaz = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    egitim_df, dogrulama_df = veri.kat_oku(KOK / bolme_klasor, set_adi, kat)
    tr = veri.yukleyici(egitim_df, veri_kok, gorev, True, a["batch"], isci=a["isci"], boyut=a["boyut"], tohum=tohum)
    va = veri.yukleyici(dogrulama_df, veri_kok, gorev, False, a["batch"], isci=a["isci"], boyut=a["boyut"], tohum=tohum)
    k = veri.sinif_sayisi(gorev)
    model = model_olustur(model_klasor, varyant, k, a["boyut"], agirlik=agirlik).to(cihaz)
    param = sum(p.numel() for p in model.parameters())
    kayip = nn.CrossEntropyLoss(weight=tr.dataset.sinif_agirliklari().to(cihaz))  # sınıf dengesizliği
    opt = optimizer_olustur(a["optimizer"], model.parameters(), a["lr"], a["wd"])
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=a["epoch"])
    scaler = grad_scaler(a["amp"] and cihaz.type == "cuda")

    # Koşu adı: lr ve boyut ADA GİRER — PROTOKOL madde 7 LR taraması ile 96³/128³ ablation'ı aynı dosyayı
    # ezmesin, ikinci koşu birincinin checkpoint'inden devam etmesin.
    ad = f"{model_klasor}-{varyant}_{set_adi}_{gorev}_t{tohum}_k{kat}_lr{a['lr']:.0e}_b{a['boyut']}"
    if str(a["optimizer"]).lower() != "adamw":   # makale-sadık koşu PROTOKOL koşusunun kaydını ezmesin
        ad += f"_{str(a['optimizer']).lower()}"
    if etiket:
        ad += f"_{etiket}"
    cikti = KOK / cikti_klasor; cikti.mkdir(parents=True, exist_ok=True)
    ckpt = cikti / f"{ad}.pth"; son_ckpt = cikti / f"{ad}_son.pth"; kayit = cikti / f"{ad}.json"
    en_iyi, en_iyi_epoch, sabir, baslangic_epoch, gecmis = -1.0, -1, 0, 0, []
    if son_ckpt.exists() and sifirdan:
        print(f"--sifirdan: mevcut checkpoint yok sayılıyor ({son_ckpt.name})")
    elif son_ckpt.exists():  # kesintiden devam: optimizer + scheduler + scaler + sabır sayacı birlikte
        d = ckpt_yukle(son_ckpt, cihaz)
        model.load_state_dict(d["model"]); opt.load_state_dict(d["opt"])
        sched.load_state_dict(d["sched"]); scaler.load_state_dict(d["scaler"])
        baslangic_epoch = d["epoch"] + 1
        en_iyi, en_iyi_epoch, sabir, gecmis = d["en_iyi"], d["en_iyi_epoch"], d["sabir"], d["gecmis"]
        print(f"devam: epoch {baslangic_epoch}, en iyi BAcc {en_iyi:.3f} (epoch {en_iyi_epoch}), sabır {sabir}")

    t0 = time.time()
    for ep in range(baslangic_epoch, a["epoch"]):
        model.train(); toplam, n = 0.0, 0; bekleyen = False; opt.zero_grad(set_to_none=True)
        for i, (x, y, _) in enumerate(tr):
            x, y = x.to(cihaz, non_blocking=True), torch.as_tensor(y).to(cihaz)
            with torch.autocast(device_type=cihaz.type, enabled=(a["amp"] and cihaz.type == "cuda")):
                loss = kayip(model(x), y) / a["accum"]
            scaler.scale(loss).backward()
            if (i + 1) % a["accum"] == 0:
                scaler.step(opt); scaler.update(); opt.zero_grad(set_to_none=True); bekleyen = False
            else:
                bekleyen = True
            toplam += loss.item() * len(y) * a["accum"]; n += len(y)
        if bekleyen:  # son yarım birikim grubunun gradyanları düşmesin
            scaler.step(opt); scaler.update(); opt.zero_grad(set_to_none=True)
        sched.step()
        m = degerlendir(model, va, cihaz, gorev, a["amp"])
        gecmis.append({"epoch": ep, "kayip": toplam / max(n, 1), "dogrulama": m})
        print(f"[{ad}] ep {ep:3d} kayıp {toplam / max(n, 1):.4f} BAcc {m['bacc']:.3f} AUC {m['auc']:.3f}")
        iyilesti = m["bacc"] > en_iyi
        if iyilesti:
            en_iyi, en_iyi_epoch, sabir = m["bacc"], ep, 0
        else:
            sabir += 1
        durum = {"model": model.state_dict(), "opt": opt.state_dict(), "sched": sched.state_dict(),
                 "scaler": scaler.state_dict(), "epoch": ep, "en_iyi": en_iyi, "en_iyi_epoch": en_iyi_epoch,
                 "sabir": sabir, "gecmis": gecmis, "ayar": a, "varyant": varyant, "gorev": gorev}
        torch.save(durum, son_ckpt)   # her epoch: kesintiden devam (KURULUM.md §6)
        if iyilesti:
            torch.save(durum, ckpt)   # en iyi doğrulama BAcc
        if sabir >= a["sabir"]:
            print("erken durdurma"); break
    sure = time.time() - t0
    vram = torch.cuda.max_memory_allocated() / 2**30 if cihaz.type == "cuda" else 0.0

    # en iyi epoch ile doğrulama + kilitli test (test yalnızca raporlanır, seçimde kullanılmaz)
    d = ckpt_yukle(ckpt, cihaz); model.load_state_dict(d["model"])
    dogrulama_son = degerlendir(model, va, cihaz, gorev, a["amp"])
    test_df = veri.test_oku(KOK / bolme_klasor, set_adi)
    te = veri.yukleyici(test_df, veri_kok, gorev, False, a["batch"], isci=a["isci"], boyut=a["boyut"], tohum=tohum)
    test_son = degerlendir(model, te, cihaz, gorev, a["amp"])
    sonuc = {"ad": ad, "model": model_klasor, "varyant": varyant, "set": set_adi, "gorev": gorev, "kat": kat, "tohum": tohum,
             "lr": a["lr"], "boyut": a["boyut"], "etiket": etiket, "model_notu": getattr(model, "notu", ""),
             "on_egitim": bool(agirlik), "agirlik": agirlik, "ayar": a, "parametre": param, "cihaz": str(cihaz),
             "gpu": torch.cuda.get_device_name(0) if cihaz.type == "cuda" else "cpu", "vram_gb": round(vram, 2),
             "sure_sn": round(sure, 1), "epoch_kosulan": len(gecmis), "en_iyi_epoch": en_iyi_epoch,
             "dogrulama": dogrulama_son, "test": test_son, "commit": commit_hash(), "torch": torch.__version__,
             "surumler": surumler(), "deterministic": bool(torch.backends.cudnn.deterministic)}
    kayit.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    son_ckpt.unlink(missing_ok=True)  # koşu tamamlandı: devam dosyası gereksiz, yalnız en iyi checkpoint kalır
    print(f"BİTTİ {ad}: doğrulama BAcc {dogrulama_son['bacc']:.3f} | test BAcc {test_son['bacc']:.3f} AUC {test_son['auc']:.3f} → {kayit}")
    return sonuc


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", required=True); p.add_argument("--varyant", default="varsayilan")
    p.add_argument("--set", required=True); p.add_argument("--gorev", choices=["ikili", "uc"], default="ikili")
    p.add_argument("--kat", type=int, default=0); p.add_argument("--tum_katlar", action="store_true")
    p.add_argument("--tohum", type=int, default=2026); p.add_argument("--tohumlar", type=int, nargs="*")
    p.add_argument("--veri", required=True); p.add_argument("--bolme", default="veri/bolme")
    p.add_argument("--cikti", default="karsilastirma/kosu_kayitlari", help="koşu kaydı ve checkpoint klasörü")
    p.add_argument("--agirlik", default=None)
    p.add_argument("--lrler", type=float, nargs="*", help="LR taraması (PROTOKOL madde 7: 1e-3 3e-4 1e-4)")
    p.add_argument("--etiket", default="", help="koşu adına ek etiket (ablation adı gibi)")
    p.add_argument("--sifirdan", action="store_true", help="mevcut checkpoint'i yok say, baştan eğit")
    for k, v in VARSAYILAN.items():
        p.add_argument(f"--{k}", type=type(v) if not isinstance(v, bool) else int, default=None)
    x = p.parse_args()
    ayar = {k: getattr(x, k) for k in VARSAYILAN}
    if ayar["amp"] is not None: ayar["amp"] = bool(ayar["amp"])
    katlar = range(5) if x.tum_katlar else [x.kat]
    tohumlar = x.tohumlar or [x.tohum]
    lrler = x.lrler or [ayar["lr"] if ayar["lr"] is not None else VARSAYILAN["lr"]]
    for lr in lrler:
        for t in tohumlar:
            for k in katlar:
                egit(x.model, x.varyant, x.set, x.gorev, k, t, x.veri, x.bolme, x.cikti, agirlik=x.agirlik,
                     etiket=x.etiket, sifirdan=x.sifirdan, **{**ayar, "lr": lr})


if __name__ == "__main__":
    main()
