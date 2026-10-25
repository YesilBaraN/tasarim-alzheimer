# -*- coding: utf-8 -*-
r"""
altgrup_analiz.py — Test kümesi sonucunu alt gruplara ayırır ve karıştırıcıları ölçer.

Neden gerekli: OASIS alt kümemizde **cinsiyet karıştırıcı** (AD %54 kadın, CN %72 kadın,
Fisher p = 0,0009; `veri/VERI-SETI.md §2g`). Tek bir toplam BAcc sayısı bu durumda iki ayrı
soruyu gizliyor:

  1. Model **beyinden** mi karar veriyor, yoksa cinsiyetle ilişkili ipuçlarından mı?
  2. Başarı alt gruplar arasında **eşit** mi dağılıyor? (Bir grupta iyi, diğerinde rastgele
     olan bir model, ortalamada iyi görünür ama klinik olarak kullanılamaz.)

Üç şey üretiyor:

**(a) Karıştırıcı tavan çizgisi.** Yalnız cinsiyetten (ya da yalnız yaştan) AD tahmin eden
lojistik regresyonun aynı test kümesindeki AUC'si. Bu, "hiç beyne bakmayan" bir modelin
alabileceği skordur. Modelimizin AUC'si buna yakınsa sonuç karıştırıcıdan geliyor olabilir;
belirgin şekilde üstündeyse model beyinden bilgi çıkarıyor. Tek sayı yerine bu **fark**
raporlanabilir hale geliyor.

**(b) Alt grup metrikleri.** cinsiyet (K/E), kohort (OASIS-1/OASIS-2), yaş bandı (<75 / ≥75).

**(c) Bootstrap %95 güven aralığı.** Test kümesi 53 denek; tek bir deneğin yeri değişince
BAcc ~%2 oynuyor. Güven aralığı olmadan "0,72 vs 0,75" karşılaştırması anlamsız.

Kullanım:
  python karsilastirma\altgrup_analiz.py --kayit karsilastirma\kosu_kayitlari\<ad>.json --veri D:\veri\radiata\islenmis
  python karsilastirma\altgrup_analiz.py --hepsi --set oasis --veri D:\veri\radiata\islenmis --cikti karsilastirma\ALTGRUP.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from uygulama.ortak import metrikler, veri                     # noqa: E402
from uygulama.ortak.egit import model_olustur                   # noqa: E402

for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:
        pass


def tahmin_et(kayit: dict, veri_kok: str, bolme_klasor: Path, batch: int = 4) -> pd.DataFrame:
    """Checkpoint'i yükler, test kümesinde tahmin üretir → denek_id, etiket, olasilik."""
    ad = kayit["ad"]
    ckpt = Path(kayit.get("ckpt") or (KOK / "karsilastirma/kosu_kayitlari" / f"{ad}.pth"))
    if not ckpt.exists():
        raise SystemExit(f"checkpoint yok: {ckpt}\n"
                         f"  (.pth dosyalari .gitignore'da; kosuyu yapan makinede calistirilmali)")
    gorev = kayit["gorev"]
    boyut = int(kayit.get("boyut", 128))
    cihaz = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = model_olustur(kayit["model"], kayit["varyant"], veri.sinif_sayisi(gorev), boyut)
    d = torch.load(ckpt, map_location="cpu", weights_only=False)
    model.load_state_dict(d["model"] if "model" in d else d)
    model = model.to(cihaz).eval()

    test_df = veri.test_oku(bolme_klasor, kayit["set"])
    yuk = veri.yukleyici(test_df, veri_kok, gorev, False, batch, isci=0, boyut=boyut,
                         tohum=int(kayit.get("tohum", 2026)))
    kimlik, ys, probs = [], [], []
    with torch.no_grad():
        for x, y, kid in yuk:
            x = x.to(cihaz)
            with torch.autocast(device_type=cihaz.type, enabled=(cihaz.type == "cuda")):
                out = model(x)
            probs.append(torch.softmax(out.float(), 1).cpu().numpy())
            ys.append(np.asarray(y)); kimlik += list(kid)
    P = np.concatenate(probs); Y = np.concatenate(ys)
    out = pd.DataFrame({"denek_id": kimlik, "etiket": Y, "olasilik": P[:, 1] if P.shape[1] == 2 else P.max(1)})
    return out.merge(test_df[["denek_id", "yas", "cinsiyet", "kaynak"]], on="denek_id", how="left")


def esik_sec(kayit: dict, veri_kok: str, bolme_klasor: Path, batch: int = 4) -> float:
    """Karar eşiğini **doğrulama** katında seçer (test'e asla bakmaz).

    Eşik, o koşunun **kendi doğrulama katında** dengeli doğruluğu en büyükleyen değer olarak
    seçiliyor. Bu PROTOKOL madde 7 ile uyumlu: hiperparametre ve eşik seçimi yalnız doğrulamada
    yapılır, kilitli test kümesi tek seferlik ölçüm için saklanır. Test'te eşik aramak sonucu
    şişirirdi ve literatürdeki en yaygın sızıntı biçimlerinden biridir.

    ⚠ **Ölçtük: tek katta bu işe yaramıyor.** VoxCNN kat 0'da duyarlılık 0,778 / özgüllük 0,462
    veriyor ve AUC (0,758) ile BAcc (0,620) arasında büyük boşluk var. İlk tahminimiz eşiğin
    yanlış yerde olmasıydı; ölçüm bunu çürüttü:

      doğrulamada seçilen eşik   0,4821  → doğrulama BAcc 0,809, test BAcc 0,620
      argmax 0,5                         → doğrulama BAcc 0,809, test BAcc 0,620
      test'te ulaşılabilir en iyi        → test BAcc 0,736   (oracle, RAPORLANAMAZ)

    Yani test'te 0,736 veren bir eşik **var**, ama doğrulama katı onu göstermiyor. Sorun eşik
    aramasının yetersizliği değil, **kalibrasyonun doğrulama katından test kümesine taşınmaması**:
    236 eğitim ve 53 test deneğiyle olasılık dağılımları kat başına kayıyor. Daha iyi eşik aramak
    bunu çözmez; çözüm **5 katın doğrulama eşiklerinin ortalamasını** kullanmak (tek katın
    gürültüsü ortalamada söner). Bu yüzden:

      - **Birincil metrik AUC** olmalı — eşikten bağımsız, bu sorundan etkilenmiyor.
      - BAcc protokolün sabit kuralıyla (argmax) raporlanır ve bu kısıt yazılır.
      - 5 kat bittiğinde `--esik_kaynak katlar` ile kat-ortalaması eşik kullanılır.
    """
    ad = kayit["ad"]
    ckpt = Path(kayit.get("ckpt") or (KOK / "karsilastirma/kosu_kayitlari" / f"{ad}.pth"))
    gorev, boyut = kayit["gorev"], int(kayit.get("boyut", 128))
    cihaz = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model_olustur(kayit["model"], kayit["varyant"], veri.sinif_sayisi(gorev), boyut)
    d = torch.load(ckpt, map_location="cpu", weights_only=False)
    model.load_state_dict(d["model"] if "model" in d else d)
    model = model.to(cihaz).eval()

    _, dog_df = veri.kat_oku(bolme_klasor, kayit["set"], int(kayit["kat"]))
    yuk = veri.yukleyici(dog_df, veri_kok, gorev, False, batch, isci=0, boyut=boyut,
                         tohum=int(kayit.get("tohum", 2026)))
    ys, ps = [], []
    with torch.no_grad():
        for x, y, _ in yuk:
            with torch.autocast(device_type=cihaz.type, enabled=(cihaz.type == "cuda")):
                out = model(x.to(cihaz))
            ps.append(torch.softmax(out.float(), 1).cpu().numpy()[:, 1]); ys.append(np.asarray(y))
    y = np.concatenate(ys); p = np.concatenate(ps)
    from sklearn.metrics import balanced_accuracy_score
    adaylar = np.unique(np.round(p, 4))
    en_iyi, en_iyi_bacc = 0.5, -1.0
    for e in adaylar:
        b = balanced_accuracy_score(y, (p >= e).astype(int))
        if b > en_iyi_bacc:
            en_iyi, en_iyi_bacc = float(e), float(b)
    print(f"  esik dogrulamada secildi: {en_iyi:.4f} (dogrulama BAcc {en_iyi_bacc:.3f}, "
          f"argmax 0.5 ile {balanced_accuracy_score(y, (p >= 0.5).astype(int)):.3f})")
    return en_iyi


def bootstrap_ga(y, p, n: int = 2000, tohum: int = 2026) -> dict:
    """Denek düzeyinde yeniden örnekleme ile %95 GA. Tek sınıflı örnek düşerse AUC atlanır."""
    rng = np.random.default_rng(tohum)
    bacc, auc = [], []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if len(np.unique(y[i])) < 2:
            continue
        m = metrikler.hesapla(y[i], np.stack([1 - p[i], p[i]], 1), "ikili")
        bacc.append(m["bacc"])
        if not np.isnan(m.get("auc", np.nan)):
            auc.append(m["auc"])
    g = lambda v: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) if v else (float("nan"),) * 2
    return {"bacc_ga": g(bacc), "auc_ga": g(auc), "gecerli": len(bacc)}


def karistirici_tavani(df: pd.DataFrame) -> dict:
    """Yalnız demografiden AD tahmin eden lojistik regresyonun AUC'si = beyne bakmayan tavan."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    y = (df["etiket"].to_numpy() == 1).astype(int)
    out = {}
    secim = {"yalniz_cinsiyet": [(df["cinsiyet"] == "F").astype(float)],
             "yalniz_yas": [df["yas"].astype(float).fillna(df["yas"].astype(float).mean())],
             "cinsiyet+yas": [(df["cinsiyet"] == "F").astype(float),
                              df["yas"].astype(float).fillna(df["yas"].astype(float).mean())]}
    kat = min(5, int(np.bincount(y).min()))
    for ad, sut in secim.items():
        X = np.column_stack([np.asarray(s) for s in sut])
        if kat < 2:
            out[ad] = float("nan"); continue
        p = cross_val_predict(LogisticRegression(max_iter=1000), X, y, method="predict_proba",
                              cv=StratifiedKFold(kat, shuffle=True, random_state=2026))[:, 1]
        from sklearn.metrics import roc_auc_score
        out[ad] = float(roc_auc_score(y, p))
    return out


def _esikli(y, p, esik: float) -> dict:
    """Verilen eşikle metrikler. metrikler.hesapla argmax kullandığı için olasılığı kaydırıyoruz:
    p' = p - esik + 0.5 ile argmax(0.5) tam olarak p >= esik kuralına denk düşüyor."""
    kaydirilmis = np.clip(p - esik + 0.5, 0.0, 1.0)
    return metrikler.hesapla(y, np.stack([1 - kaydirilmis, kaydirilmis], 1), "ikili")


def analiz(df: pd.DataFrame, esik: float = 0.5) -> dict:
    y = df["etiket"].to_numpy(); p = df["olasilik"].to_numpy()
    toplam = metrikler.hesapla(y, np.stack([1 - p, p], 1), "ikili")
    toplam.update(bootstrap_ga(y, p))
    if abs(esik - 0.5) > 1e-9:
        # AUC eşikten bağımsız olduğu için değişmiyor; değişen BAcc/duyarlılık/özgüllük.
        toplam["esik"] = esik
        toplam["esikli"] = _esikli(y, p, esik)

    gruplar = {}
    df = df.copy()
    df["yas_bandi"] = np.where(df["yas"].astype(float) < 75, "<75", ">=75")
    for sut in ("cinsiyet", "kaynak", "yas_bandi"):
        for deger, g in df.groupby(sut):
            if len(np.unique(g["etiket"])) < 2:
                gruplar[f"{sut}={deger}"] = {"n": len(g), "not": "tek sinif, metrik hesaplanamaz"}
                continue
            m = metrikler.hesapla(g["etiket"].to_numpy(),
                                  np.stack([1 - g["olasilik"], g["olasilik"]], 1), "ikili")
            m["n_ad"] = int((g["etiket"] == 1).sum())
            gruplar[f"{sut}={deger}"] = m
    return {"toplam": toplam, "altgruplar": gruplar, "karistirici_tavani": karistirici_tavani(df)}


def bas(ad: str, r: dict) -> list[str]:
    s = [f"\n### {ad}"]
    t = r["toplam"]
    s.append(f"  TOPLAM  n={t['n']}  BAcc {t['bacc']:.3f} [{t['bacc_ga'][0]:.3f}-{t['bacc_ga'][1]:.3f}]  "
             f"AUC {t['auc']:.3f} [{t['auc_ga'][0]:.3f}-{t['auc_ga'][1]:.3f}]  "
             f"duyarlilik {t['sens']:.3f}  ozgulluk {t['spec']:.3f}   (esik 0.5 / argmax)")
    if "esikli" in t:
        e = t["esikli"]
        s.append(f"  ESIK DUZELTILMIS (esik {t['esik']:.4f}, DOGRULAMADA secildi)  "
                 f"BAcc {e['bacc']:.3f}  duyarlilik {e['sens']:.3f}  ozgulluk {e['spec']:.3f}  "
                 f"-> BAcc {e['bacc'] - t['bacc']:+.3f}   (AUC esikten bagimsiz, degismez)")
    kt = r["karistirici_tavani"]
    s.append("  KARISTIRICI TAVANI (beyne bakmayan model): " +
             " - ".join(f"{k} AUC {v:.3f}" for k, v in kt.items()))
    en = max(v for v in kt.values() if not np.isnan(v))
    fark = t["auc"] - en
    s.append(f"  -> modelin AUC'si demografi tavaninin {fark:+.3f} uzerinde" +
             ("  [model beyinden bilgi cikariyor]" if fark > 0.05 else
              "  [UYARI: tavandan ayirt edilemiyor, sonuc karistiricidan gelebilir]"))
    s.append("  alt gruplar:")
    for k, m in r["altgruplar"].items():
        if "not" in m:
            s.append(f"    {k:<22} n={m['n']:<3} {m['not']}")
        else:
            s.append(f"    {k:<22} n={m['n']:<3} (AD {m['n_ad']:<2}) BAcc {m['bacc']:.3f}  AUC {m['auc']:.3f}")
    bacc = [m["bacc"] for m in r["altgruplar"].values() if "bacc" in m]
    if bacc and max(bacc) - min(bacc) > 0.15:
        s.append(f"  UYARI alt gruplar arasi BAcc yayilimi {max(bacc) - min(bacc):.3f} > 0.15 "
                 f"-> basari esit dagilmiyor, raporda belirtilmeli")
    return s


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--kayit", default=None, help="tek kosu kaydi JSON'u")
    p.add_argument("--hepsi", action="store_true", help="--set'teki tum kosu kayitlari")
    p.add_argument("--set", default="oasis")
    p.add_argument("--kayitlar", default=str(KOK / "karsilastirma/kosu_kayitlari"))
    p.add_argument("--veri", required=True)
    p.add_argument("--bolme", default=str(KOK / "veri/bolme"))
    p.add_argument("--cikti", default=None, help="markdown dosyasi (yoksa yalniz ekrana)")
    p.add_argument("--esik_yok", action="store_true",
                   help="esigi dogrulamada secme, argmax 0.5 kullan (egit.py ile birebir ayni sonuc)")
    a = p.parse_args()

    if a.kayit:
        yollar = [Path(a.kayit)]
    elif a.hepsi:
        yollar = sorted(Path(a.kayitlar).glob(f"*_{a.set}_*.json"))
    else:
        raise SystemExit("--kayit ya da --hepsi verin")
    if not yollar:
        raise SystemExit(f"kosu kaydi bulunamadi: {a.kayitlar}")

    satirlar = [f"# Alt grup analizi — {a.set}", "",
                "Toplam BAcc tek basina yeterli degil: veri setinde cinsiyet karistirici "
                "(AD %54 kadin, CN %72 kadin, Fisher p = 0,0009). Asagidaki **karistirici tavani** "
                "beyne hic bakmayan bir modelin ayni test kumesinde alabilecegi AUC'dir; "
                "modelin skoru bu tavanin ne kadar uzerinde, asil soru o.", ""]
    for y in yollar:
        kayit = json.load(open(y, encoding="utf-8"))
        print(f"\n--- {kayit['ad']}", flush=True)
        try:
            esik = 0.5 if a.esik_yok else esik_sec(kayit, a.veri, Path(a.bolme))
            df = tahmin_et(kayit, a.veri, Path(a.bolme))
        except SystemExit as e:
            print(f"ATLA {y.name}: {e}"); continue
        r = analiz(df, esik)
        blok = bas(kayit["ad"], r)
        print("\n".join(blok), flush=True)
        satirlar += ["```"] + blok + ["```", ""]
        kayit["altgrup"] = r
        with open(y, "w", encoding="utf-8") as f:
            json.dump(kayit, f, ensure_ascii=False, indent=2)

    if a.cikti:
        Path(a.cikti).write_text("\n".join(satirlar), encoding="utf-8")
        print(f"\n-> {a.cikti}")


if __name__ == "__main__":
    main()
