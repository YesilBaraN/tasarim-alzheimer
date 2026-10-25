# -*- coding: utf-8 -*-
r"""
uyum_analiz.py — Modeller birbirleriyle ne kadar uyuşuyor? Darboğaz mimari mi, veri mi?

Bu projenin sorusu "hangi mimari daha iyi" — ama tabloya bakıp 0,700 ile 0,620'yi kıyaslamak
sorunun yarısı. Diğer yarısı: **modeller birbirinden gerçekten farklı şeyler mi öğreniyor?**

İlk ölçüm şunu gösterdi: VoxCNN (0,38M, artık bağlantısız) ile ResNet-18 (33M, çok daha derin)
53 test deneğinin **43'ünde aynı kararı** veriyor ve olasılıkları 0,808 korelasyonlu. İkisi de
aynı 20 deneği yanlış biliyor. Eğer bu örüntü tüm modellerde sürüyorsa, mimariyi değiştirmek
sonucu değiştirmiyor demektir ve asıl kısıt **veri** (236 eğitim deneği, afin normalizasyonla
silinmiş hacim bilgisi) olur. Bu, raporun tartışma bölümünün omurgası.

Üç şey üretiyor:

**(a) İkili uyum matrisi + Cohen kappa.** Ham uyum yüzdesi yanıltıcı olabilir (iki model de
çoğunluk sınıfını söylerse yüksek çıkar); kappa şansı düzeltiyor.

**(b) İndirgenemez çekirdek.** Kaç denek **her** model tarafından yanlış biliniyor? Bu küme
büyükse mimari arayışı boşa kürek. Ayrıca bu deneklerin demografisi basılıyor — belki hepsi
belirli bir alt gruptan geliyordur (ör. hafif evre AD).

**(c) Topluluk (ensemble) tavanı.** Modellerin olasılık ortalamasının AUC'si. Tek tek en iyi
modelden belirgin şekilde yüksekse modeller **tamamlayıcı** bilgi taşıyor; değilse aynı şeyi
görüyorlar. Bu, (a) ve (b)'nin bağımsız bir doğrulaması.

Kullanım:
  python karsilastirma\uyum_analiz.py --set oasis --veri D:\veri\radiata\islenmis
  python karsilastirma\uyum_analiz.py --set oasis --veri D:\veri\radiata\islenmis --cikti karsilastirma\UYUM.md
"""
from __future__ import annotations

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from karsilastirma.altgrup_analiz import tahmin_et   # noqa: E402

for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:
        pass


def kisa_ad(kayit: dict) -> str:
    a = f"{kayit['model'].split('_', 1)[-1] if '_' in kayit['model'] else kayit['model']}:{kayit['varyant']}"
    if kayit.get("etiket"):
        a += f"[{kayit['etiket']}]"
    if kayit.get("on_egitim"):
        a += "+ön"
    return a


def topla(set_adi: str, kayitlar_kl: Path, veri_kok: str, bolme: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Her koşunun test olasılıklarını tek tabloda birleştirir (satır = denek, sütun = model)."""
    tahmin, demog = {}, None
    for y in sorted(kayitlar_kl.glob(f"*_{set_adi}_*.json")):
        kayit = json.loads(y.read_text(encoding="utf-8"))
        if "test" not in kayit:
            continue
        try:
            df = tahmin_et(kayit, veri_kok, bolme).sort_values("denek_id").reset_index(drop=True)
        except SystemExit as e:
            print(f"ATLA {y.name}: {e}")
            continue
        if demog is None:
            demog = df[["denek_id", "etiket", "yas", "cinsiyet", "kaynak"]].copy()
        elif not demog["denek_id"].equals(df["denek_id"]):
            raise SystemExit(f"{y.name}: test kümesi sırası farklı — aynı bölmeden değil")
        tahmin[kisa_ad(kayit)] = df["olasilik"].to_numpy()
        print(f"  okundu: {kisa_ad(kayit)}")
    if len(tahmin) < 2:
        raise SystemExit(f"en az 2 koşu gerekiyor, {len(tahmin)} bulundu")
    return pd.DataFrame(tahmin), demog


def kappa(a: np.ndarray, b: np.ndarray) -> float:
    """Cohen kappa — ham uyumu şansa göre düzeltir."""
    n = len(a)
    po = float((a == b).mean())
    pe = sum(float((a == k).mean()) * float((b == k).mean()) for k in (0, 1))
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--set", default="oasis")
    p.add_argument("--kayitlar", default=str(KOK / "karsilastirma/kosu_kayitlari"))
    p.add_argument("--veri", required=True)
    p.add_argument("--bolme", default=str(KOK / "veri/bolme"))
    p.add_argument("--cikti", default=None)
    a = p.parse_args()

    print(f"koşu kayıtları okunuyor ({a.set}):")
    P, demog = topla(a.set, Path(a.kayitlar), a.veri, Path(a.bolme))
    y = demog["etiket"].to_numpy()
    K = (P >= 0.5).astype(int)

    # Çökmüş koşuları ayır. Tek sınıf tahmin eden bir model (ör. P06, karışıklık matrisi
    # [[26,0],[27,0]]) bu analizin üçünü de bozuyor:
    #   - kappa'sı tanımı gereği tam 0,000 çıkar (po = pe) ve ortalamayı aşağı çeker,
    #   - her AD deneğini yanlış bildiği için "modeller ayrışıyor" sayısını yapay şişirir,
    #   - olasılıkları bilgi taşımadığı için topluluk ortalamasını sulandırır.
    # Dışlanıyor ama **gizlenmiyor**: aşağıda nedeniyle listeleniyor.
    cokmus = [ad for ad in P.columns if K[ad].nunique() < 2]
    adlar = [ad for ad in P.columns if ad not in cokmus]
    s = [f"# Model uyum analizi — {a.set}", "",
         f"Test kümesi: {len(y)} denek ({int((y == 0).sum())} NC / {int((y == 1).sum())} AD) · "
         f"{len(adlar)} koşu", ""]
    if cokmus:
        s += [f"⚠ **Analiz dışı {len(cokmus)} çökmüş koşu:** " +
              ", ".join(f"`{c}` (tek sınıf tahmin ediyor)" for c in cokmus),
              "", "Tek sınıf tahmin eden bir model üç ölçümü de bozar: kappa'sı tanımı gereği "
              "0,000 çıkar, her karşı-sınıf deneğini yanlış bildiği için ayrışma sayısını yapay "
              "şişirir, olasılıkları bilgi taşımadığı için topluluğu sulandırır.", ""]
    if len(adlar) < 2:
        raise SystemExit(f"çökmüş koşular ayrıldıktan sonra {len(adlar)} koşu kaldı, en az 2 gerekiyor")
    P, K = P[adlar], K[adlar]

    # (a) ikili uyum + kappa
    s += ["## (a) İkili uyum", "",
          "Ham uyum yüzdesi yanıltıcı olabilir (iki model de çoğunluk sınıfını söylerse yüksek çıkar); "
          "**kappa** şansı düzeltir. Kappa 1 = birebir aynı kararlar, 0 = şans düzeyinde ilişki.", "",
          "| Model A | Model B | Uyum | Kappa | Olasılık korelasyonu |", "|---|---|---|---|---|"]
    uyumlar, kappalar = [], []
    for i, j in combinations(range(len(adlar)), 2):
        u = float((K.iloc[:, i] == K.iloc[:, j]).mean())
        kp = kappa(K.iloc[:, i].to_numpy(), K.iloc[:, j].to_numpy())
        r = float(np.corrcoef(P.iloc[:, i], P.iloc[:, j])[0, 1])
        uyumlar.append(u); kappalar.append(kp)
        s.append(f"| {adlar[i]} | {adlar[j]} | {u:.0%} | {kp:+.3f} | {r:+.3f} |")
    s += ["", f"**Ortalama uyum {np.mean(uyumlar):.0%} · ortalama kappa {np.nanmean(kappalar):+.3f}**", ""]

    # (b) indirgenemez cekirdek
    dogru = pd.DataFrame({ad: (K[ad].to_numpy() == y) for ad in adlar})
    hepsi_yanlis = ~dogru.any(axis=1)
    hepsi_dogru = dogru.all(axis=1)
    s += ["## (b) İndirgenemez çekirdek", "",
          f"- **Hiçbir model doğru bilemedi: {int(hepsi_yanlis.sum())}/{len(y)} denek "
          f"({hepsi_yanlis.mean():.0%})**",
          f"- Her model doğru bildi: {int(hepsi_dogru.sum())}/{len(y)} ({hepsi_dogru.mean():.0%})",
          f"- Modellerin ayrıştığı: {len(y) - int(hepsi_yanlis.sum()) - int(hepsi_dogru.sum())}/{len(y)}",
          ""]
    if hepsi_yanlis.sum():
        z = demog[hepsi_yanlis.to_numpy()]
        s += ["Hiçbir modelin bilemediği deneklerin demografisi:", "",
              f"- sınıf: AD {int((z['etiket'] == 1).sum())} · NC {int((z['etiket'] == 0).sum())}",
              f"- yaş: {z['yas'].mean():.1f} (tüm test: {demog['yas'].mean():.1f})",
              f"- kadın oranı: {(z['cinsiyet'] == 'F').mean():.0%} (tüm test: {(demog['cinsiyet'] == 'F').mean():.0%})",
              f"- kohort: {dict(z['kaynak'].value_counts())}", ""]

    # (c) topluluk tavani
    from sklearn.metrics import roc_auc_score
    tek = {ad: roc_auc_score(y, P[ad]) for ad in adlar}
    en_iyi_ad = max(tek, key=tek.get)
    ort = roc_auc_score(y, P.mean(axis=1))
    s += ["## (c) Topluluk tavanı", "",
          "| | AUC |", "|---|---|"]
    for ad in sorted(tek, key=tek.get, reverse=True):
        s.append(f"| {ad} | {tek[ad]:.3f} |")
    s += [f"| **Topluluk (olasılık ortalaması)** | **{ort:.3f}** |", "",
          f"Topluluk, en iyi tek modelden ({en_iyi_ad}, {tek[en_iyi_ad]:.3f}) "
          f"**{ort - tek[en_iyi_ad]:+.3f}** farklı."]
    if ort - tek[en_iyi_ad] > 0.03:
        s += ["", "→ Modeller **tamamlayıcı** bilgi taşıyor: mimari çeşitliliği gerçek bir kazanç."]
    else:
        s += ["", "→ Topluluk kayda değer bir şey eklemiyor: modeller büyük ölçüde **aynı sinyali** "
              "görüyor.", "",
              "**(b) ile (c) birlikte okunmalı ve ilginç olan şu:** modeller deneklerin yarısında "
              f"ayrışıyor ({len(y) - int(hepsi_yanlis.sum()) - int(hepsi_dogru.sum())}/{len(y)}), "
              "ama ortalamaları hiçbir şey kazandırmıyor. Eğer bu ayrışma **tamamlayıcı** olsaydı "
              "(her model verinin farklı ama geçerli bir yönünü görseydi) ortalama kazandırırdı. "
              "Kazandırmadığına göre ayrışma **gürültü**: her model aynı karar yüzeyinden "
              "gürültülü bir çekiliş. 236 eğitim deneğiyle kayıp yüzeyi düz olduğu için her koşu "
              "farklı bir rastgele köşeye oturuyor."]

    s += ["", "---", "",
          f"⚠ **Kapsam:** bu analiz {len(adlar)} koşu ve **tek kat** (kat 0) üzerinden, "
          f"{len(y)} deneklik test kümesinde yapıldı. Yukarıdaki yorum bir **ön işaret**, "
          "sonuç değil — mimari hakkında kesin bir şey söylemek için 5 kat bitmeli ve "
          "koşular birbirinden bağımsız mimarilerle çeşitlenmeli (şu an koşuların bir kısmı "
          "aynı mimarinin varyantı). Beş kat bitince bu betik yeniden koşturulmalı."]

    cikti = "\n".join(s)
    print("\n" + cikti)
    if a.cikti:
        Path(a.cikti).write_text(cikti + "\n", encoding="utf-8")
        print(f"\n-> {a.cikti}")


if __name__ == "__main__":
    main()
