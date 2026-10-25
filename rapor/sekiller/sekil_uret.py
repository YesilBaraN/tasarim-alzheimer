# -*- coding: utf-8 -*-
r"""
sekil_uret.py — `rapor/sekiller/*.puml` tasarımlarını rapora gömülebilir PNG'ye çevirir.

Neden bu betik var: diyagramlar PlantUML ile tasarlandı ama PlantUML render için Java ister
ve ekip makinelerinde Java kurulu değil. Kaynağı bir dış PlantUML sunucusuna göndermek yerine
aynı tasarımları matplotlib ile çiziyoruz — böylece şekiller depodan, tek komutla, internet
olmadan üretiliyor ve `.puml` dosyaları tasarımın kaynağı olarak kalmaya devam ediyor.

A4 sayfa genişliği 21 cm, kenarlar 3 + 2,5 cm → kullanılabilir 15,5 cm ≈ 6,1 inç.
Şekiller bu genişliğe göre ölçeklendi; 200 DPI ile Word'de net görünüyor.

Koş (proje kökünden):
  python rapor\sekiller\sekil_uret.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(errors="replace")
    except Exception:
        pass

KLASOR = Path(__file__).resolve().parent
EN = 6.1                      # inç — 15,5 cm kullanılabilir sayfa genişliği
DPI = 200

plt.rcParams.update({
    "font.family": "DejaVu Sans",      # Türkçe karakterleri tam destekliyor
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

# PlantUML dosyalarındaki renk paleti
R = {
    "veri":   "#EDF2F7", "onisleme": "#EBF8FF", "model": "#FEFCBF",
    "dogrula": "#FEEBC8", "dagitim": "#E6FFFA", "sunum": "#F7FAFC",
    "kenar":  "#4A5568", "ok": "#2B6CB0", "baslik": "#1A365D",
    "aktor":  "#BEE3F8", "aktor2": "#C6F6D5", "aktor3": "#FEFCBF",
    "karar":  "#FED7D7", "hata": "#FFF5F5",
}


def kutu(ax, x, y, g, y_, metin, dolgu="#FFFFFF", punto=6.0, kalin=False,
         kenar=None, yuvarlak=0.012, hiza="center"):
    ax.add_patch(FancyBboxPatch(
        (x, y), g, y_, boxstyle=f"round,pad=0,rounding_size={yuvarlak}",
        linewidth=0.7, edgecolor=kenar or R["kenar"], facecolor=dolgu, zorder=2))
    ax.text(x + g / 2, y + y_ / 2, metin, ha="center", va="center",
            fontsize=punto, zorder=3, linespacing=1.35,
            fontweight="bold" if kalin else "normal")
    return (x + g / 2, y, x + g / 2, y + y_)      # (alt_orta_x, alt_y, ust_orta_x, ust_y)


def kusak(ax, x, y, g, y_, baslik, dolgu, punto=6.5):
    """Katman/aşama kuşağı: arka plan + sol üstte başlık."""
    ax.add_patch(FancyBboxPatch(
        (x, y), g, y_, boxstyle="round,pad=0,rounding_size=0.015",
        linewidth=0.9, edgecolor=R["kenar"], facecolor=dolgu, alpha=0.95, zorder=1))
    ax.text(x + 0.012, y + y_ - 0.016, baslik, ha="left", va="top",
            fontsize=punto, fontweight="bold", color=R["baslik"], zorder=3)


def ok(ax, x1, y1, x2, y2, metin="", kesikli=False, punto=5.2, renk=None):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=7,
        linewidth=0.9, color=renk or R["ok"], zorder=4,
        linestyle=(0, (2.5, 1.8)) if kesikli else "solid",
        shrinkA=0, shrinkB=0))
    if metin:
        # Etiket yeri okun yönüne göre değişir ve bu ayrım gerekli:
        #  - yatay okta üste ortalanır (kutular arası boşluk dar, yana koyunca kutuya taşıyor),
        #  - dikey okta orta noktanın yanına konur (üste koyunca kaynak kutunun son satırına değiyor).
        dikey = abs(x2 - x1) < abs(y2 - y1)
        if dikey:
            kx, ky, hiza, dikey_hiza = (x1 + x2) / 2 + 0.012, (y1 + y2) / 2, "left", "center"
        else:
            kx, ky, hiza, dikey_hiza = (x1 + x2) / 2, max(y1, y2) + 0.006, "center", "bottom"
        ax.text(kx, ky, metin, fontsize=punto, ha=hiza, va=dikey_hiza,
                color=R["ok"], zorder=5,
                bbox=dict(boxstyle="square,pad=0.12", facecolor="white",
                          edgecolor="none", alpha=0.85))


def eksen(yuksek_inc, baslik):
    fig, ax = plt.subplots(figsize=(EN, yuksek_inc))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title(baslik, fontsize=7.6, fontweight="bold", color=R["baslik"], pad=6)
    return fig, ax


def kirp(fig, ax, y_alt, tasarim_yukseklik):
    """Kullanılmayan alt boşluğu atar ve kutuların fiziksel boyutunu korur.

    Şekilleri 0–1 normalize uzayda çiziyoruz; içerik çoğu zaman bu aralığın tamamını
    doldurmuyor ve altta boş bir şerit kalıyor. `bbox_inches="tight"` bunu kırpmıyor,
    çünkü eksen kutusu (görünmez olsa da) sınırlayıcı kutuya dahil.

    Çözüm: y eksenini içeriğin bittiği yere kadar daraltmak ve figür yüksekliğini aynı
    oranda küçültmek. İkisi birlikte yapıldığında kutular ve yazılar santim cinsinden
    tasarlandığı boyutta kalıyor, yalnız boşluk gidiyor.
    """
    y_alt = max(0.0, min(y_alt, 0.95))
    ax.set_ylim(y_alt, 1.0)
    fig.set_size_inches(EN, (1.0 - y_alt) * tasarim_yukseklik)


def kaydet(fig, ad):
    yol = KLASOR / f"{ad}.png"
    fig.savefig(yol, dpi=DPI, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print(f"  {ad}.png")


# ---------------------------------------------------------------- Şekil 1: mimari
def sekil_mimari():
    fig, ax = eksen(8.6, "Şekil 1. Sistem mimarisi — altı katmanlı blok diyagramı (§4.1)")
    KAT = [
        ("1. VERİ KATMANI", R["veri"], [
            "Ham sMRI verisi\n(ADNI1 1.5T · OASIS)\nNIfTI, DUA korumalı",
            "Denek bazlı bölme motoru\n(bolme.py)\nkilitli test + 5-kat CV",
            "Bölme haritaları\n(veri/bolme/*.csv)\nanonim denek kimliği"]),
        ("2. ÖN İŞLEME KATMANI", R["onisleme"], [
            "dcm2niix\nDICOM → NIfTI",
            "HD-BET\nkafatası ayıklama",
            "N4ITK\nbias düzeltme",
            "MNI152 afin\nşablon hizalama",
            "z-score + 128³\nfloat16 .npy"]),
        ("3. MODEL VE EĞİTİM KATMANI (uygulama/)", R["model"], [
            "Ortak veri yükleyici\n(ortak/veri.py)\nartırma: çevirme, afin",
            "Eğitim döngüsü\n(ortak/egit.py)\nAMP, erken durdurma",
            "Altı model + iki temel çizgi\nP01 P02 P06 P07 P11 P12\nSigCNN3D · voksel SVM"]),
        ("4. DOĞRULAMA VE DEĞERLENDİRME KATMANI", R["dogrula"], [
            "Sağlık testleri\n(saglik_testi.py)\nrastgele≈0,5 · ayrılabilir≈1,0",
            "Dış test motoru\n(dis_test.py)\nsıfır-atış, sızıntı kapısı",
            "Tablo üreteci\n(tablo_uret.py)\n→ SONUCLAR.md"]),
        ("5. DAĞITIM VE ÇIKARIM KATMANI", R["dagitim"], [
            "ONNX dönüştürücü\n(onnx_disa_aktar.py)",
            "ONNX Runtime\n(model.onnx)\nPyTorch'suz çalışır",
            "FastAPI servisi\nPOST /tahmin\nGET /saglik",
            "XAI ısı haritası\nGrad-CAM · LRP · DPM"]),
        ("6. SUNUM VE VERİTABANI KATMANI", R["sunum"], [
            "Web karar destek arayüzü\nE1–E7 ekranları\n3 düzlem kesit + PDF rapor",
            "İlişkisel veritabanı\nSQLite → PostgreSQL\nKullanıcı·Tarama·Tahmin·Model"]),
    ]
    ust, bosluk = 0.975, 0.016
    kusak_y = []
    for baslik, renk, ogeler in KAT:
        h = 0.118 if len(ogeler) <= 3 else 0.104
        kusak(ax, 0.008, ust - h, 0.984, h, baslik, renk)
        n = len(ogeler)
        g = (0.95 - 0.012 * (n - 1)) / n
        for i, m in enumerate(ogeler):
            kutu(ax, 0.028 + i * (g + 0.012), ust - h + 0.012, g, h - 0.042, m,
                 punto=4.7 if n >= 5 else 5.2)
        kusak_y.append((ust, ust - h))
        ust -= h + bosluk
    for (_, alt), (ust2, _) in zip(kusak_y[:-1], kusak_y[1:]):
        ok(ax, 0.5, alt, 0.5, ust2)
    ax.text(0.5, ust - 0.006, "Oklar katmanlar arası veri akışını gösterir. "
            "Ham görüntüler ve model ağırlıkları depoya girmez (DUA).",
            ha="center", va="top", fontsize=5.0, style="italic", color="#4A5568")
    kirp(fig, ax, ust - 0.030, 8.6)
    kaydet(fig, "mimari")


# ---------------------------------------------------------------- Şekil 2: use-case
def sekil_usecase():
    fig, ax = eksen(6.4, "Şekil 2. Kullanım senaryosu (use-case) diyagramı (§3.3)")
    AKTOR = [("Radyolog /\nKlinisyen\n(birincil)", 0.86, R["aktor"]),
             ("Araştırmacı /\nGeliştirici", 0.50, R["aktor2"]),
             ("Sistem\nYöneticisi", 0.17, R["aktor3"])]
    for ad, y, renk in AKTOR:
        kutu(ax, 0.012, y - 0.052, 0.155, 0.104, ad, renk, punto=5.4, kalin=True)

    ax.add_patch(FancyBboxPatch((0.195, 0.045), 0.795, 0.90,
                boxstyle="round,pad=0,rounding_size=0.012", linewidth=1.0,
                edgecolor=R["kenar"], facecolor="#FCFCFD", zorder=1))
    ax.text(0.5925, 0.962, "Alzheimer 3B Derin Öğrenme Karar Destek Sistemi",
            ha="center", va="bottom", fontsize=6.2, fontweight="bold", color=R["baslik"])

    PAKET = [
        ("Klinik karar destek işlevleri", R["onisleme"], 0.655, 0.275, [
            ("UC-1: MRI yükle ve tahmin al", True),
            ("UC-1.1: otomatik ön işleme  «include»", False),
            ("UC-1.2: voksel kalite kontrolü  «include»", False),
            ("UC-2: açıklanabilirlik haritasını incele", True),
            ("UC-2.1: 3 eksenli dilim gezinimi  «include»", False),
            ("UC-2.2: LRP / Grad-CAM eşik ayarı  «include»", False),
            ("UC-3: karar destek raporu üret (PDF)", True)]),
        ("Model geliştirme ve araştırma", R["model"], 0.345, 0.185, [
            ("UC-4: modelleri eğit ve karşılaştır (6 model)", True),
            ("UC-4.1: 5-kat denek düzeyi CV  «include»", False),
            ("UC-4.2: metrik ve ROC analizi  «include»", False),
            ("UC-5: modeli ONNX'e aktar ve yayınla", True)]),
        ("Sistem ve kullanıcı yönetimi", R["sunum"], 0.075, 0.115, [
            ("UC-6: kullanıcı ve rol yönetimi", True),
            ("UC-6.1: sistem sağlığı ve log izleme  «include»", False)]),
    ]
    birincil = {}
    for baslik, renk, y0, h, ucler in PAKET:
        kusak(ax, 0.212, y0, 0.762, h, baslik, renk, punto=5.6)
        ic = h - 0.030
        yh = ic / len(ucler)
        for i, (m, ana) in enumerate(ucler):
            yy = y0 + ic - (i + 1) * yh
            kutu(ax, 0.232 + (0.0 if ana else 0.045), yy + 0.004,
                 0.72 - (0.0 if ana else 0.045), yh - 0.008, m,
                 "#FFFFFF" if ana else "#F7FAFC", punto=4.9, kalin=ana,
                 kenar=R["kenar"] if ana else "#A0AEC0")
            if ana:
                birincil.setdefault(baslik, []).append(yy + yh / 2)

    eslesme = [(0.86, "Klinik karar destek işlevleri"),
               (0.50, "Model geliştirme ve araştırma"),
               (0.17, "Sistem ve kullanıcı yönetimi")]
    for ay, paket in eslesme:
        for uy in birincil.get(paket, []):
            ok(ax, 0.167, ay, 0.232, uy)
    ax.text(0.5925, 0.012, "«include»: ana senaryonun zorunlu alt adımı. "
            "Girintili kutular ilgili ana senaryonun içinde çalışır.",
            ha="center", va="bottom", fontsize=5.0, style="italic", color="#4A5568")
    kirp(fig, ax, 0.0, 6.4)
    kaydet(fig, "usecase")


# ---------------------------------------------------------------- Şekil 3: ER
def dirsek(ax, noktalar, metin="", punto=5.0):
    """Köşeli (ortogonal) bağlantı: ara noktalardan geçip son parçada ok ucu koyar.

    Düz çizgi kullanılamıyor çünkü Kullanici ile Tahmin arasındaki ilişki, araya giren
    varlık kutularının üzerinden geçiyordu. Ara noktaları kutuların arasındaki boş
    şeritten seçerek hiçbir kutuyu kesmeyen bir yol çiziyoruz.
    """
    for (x1, y1), (x2, y2) in zip(noktalar, noktalar[1:-1]):
        ax.plot([x1, x2], [y1, y2], color=R["ok"], linewidth=0.9, zorder=4,
                solid_capstyle="round")
    (sx, sy), (ex, ey) = noktalar[-2], noktalar[-1]
    ok(ax, sx, sy, ex, ey)
    if metin:
        mx, my = noktalar[len(noktalar) // 2]
        ax.text(mx + 0.008, my + 0.010, metin, fontsize=punto, ha="left",
                va="bottom", color=R["ok"], zorder=5)


def sekil_er():
    fig, ax = eksen(7.8, "Şekil 3. Veritabanı varlık-ilişki (ER) şeması (§4.2)")
    SATIR_Y = 0.0235          # alan satırı yüksekliği
    BASLIK_Y = 0.034          # varlık adı şeridi

    V = {
        "Kullanici": (0.030, 0.945, 0.275, [
            "kullanici_id : UUID  [PK]", "ad : VARCHAR(100)", "e_posta : VARCHAR(150) [UNIQUE]",
            "rol : Radyolog | Arastirmaci |", "        Yonetici", "parola_hash · aktif",
            "olusturma_tarihi : TIMESTAMP"]),
        "Tarama": (0.363, 0.945, 0.275, [
            "tarama_id : UUID  [PK]", "kaynak : ADNI1 | ADNI2 |", "        OASIS1 | Klinik",
            "dis_kimlik  (anonim RID)", "cekim_tarihi · alan_gucu",
            "dosya_hash  (SHA-256)", "yuklenme_tarihi : TIMESTAMP"]),
        "OnIsleme": (0.696, 0.945, 0.275, [
            "onisleme_id : UUID  [PK]", "tarama_id : UUID  [FK]", "boru_hatti_surumu",
            "kafatasi_arac  (HD-BET)", "n4_duzeltme · normalizasyon",
            "kayit_sablonu · cikti_boyutu", "sure_saniye · durum"]),
        "Model": (0.030, 0.545, 0.275, [
            "model_id : UUID  [PK]", "kod  (P01 … P12) · ad", "mimari_tipi · gorev_tipi",
            "egitim_veri · protokol_surumu", "onnx_dosya_yolu",
            "test_bacc · test_auc · test_f1", "aktif_canli_model"]),
        "Tahmin": (0.363, 0.545, 0.275, [
            "tahmin_id : UUID  [PK]", "tarama_id · model_id ·", "        kullanici_id : UUID [FK]",
            "ad_olasilik · mci_olasilik ·", "        nc_olasilik",
            "nihai_karar : AD | MCI | NC", "guven_skoru · cikarim_suresi_ms",
            "klinisyen_notu · tahmin_tarihi"]),
        "AciklamaHaritasi": (0.696, 0.545, 0.275, [
            "harita_id : UUID  [PK]", "tahmin_id : UUID  [FK]", "yontem : GradCAM_3D |",
            "        LRP_Beta0 | DPM_Risk", "katman_adi · harita_nii_yolu",
            "overlay_png_yolu", "en_yuksek_ilgi_bolgesi"]),
    }
    kutular = {}
    for ad, (x, ust, g, alanlar) in V.items():
        h = BASLIK_Y + len(alanlar) * SATIR_Y + 0.012
        ax.add_patch(FancyBboxPatch((x, ust - h), g, h,
                    boxstyle="round,pad=0,rounding_size=0.010", linewidth=0.9,
                    edgecolor=R["kenar"], facecolor="#FFFFFF", zorder=2))
        ax.add_patch(FancyBboxPatch((x, ust - BASLIK_Y), g, BASLIK_Y,
                    boxstyle="round,pad=0,rounding_size=0.008", linewidth=0.9,
                    edgecolor=R["kenar"], facecolor=R["veri"], zorder=3))
        ax.text(x + g / 2, ust - BASLIK_Y / 2, ad, ha="center", va="center",
                fontsize=5.8, fontweight="bold", zorder=4)
        for i, alan in enumerate(alanlar):
            ax.text(x + 0.012, ust - BASLIK_Y - (i + 0.62) * SATIR_Y, alan,
                    ha="left", va="center", fontsize=4.6, zorder=4,
                    fontweight="bold" if "[PK]" in alan else "normal")
        kutular[ad] = (x, ust, g, ust - h)      # sol, üst, genişlik, alt

    def kenarlar(ad):
        x, ust, g, alt = kutular[ad]
        return {"sol": x, "sag": x + g, "ust": ust, "alt": alt,
                "orta_x": x + g / 2, "orta_y": (ust + alt) / 2}

    K, T, O = kenarlar("Kullanici"), kenarlar("Tarama"), kenarlar("OnIsleme")
    M, P, X = kenarlar("Model"), kenarlar("Tahmin"), kenarlar("AciklamaHaritasi")

    # Komşu kutular arasında düz bağlantılar — hiçbiri bir kutuyu kesmiyor
    ok(ax, T["sag"], T["orta_y"], O["sol"], T["orta_y"], "1—1")
    ok(ax, T["orta_x"], T["alt"], P["orta_x"], P["ust"], "1—N")
    ok(ax, M["sag"], M["orta_y"], P["sol"], M["orta_y"], "1—N")
    ok(ax, P["sag"], P["orta_y"], X["sol"], P["orta_y"], "1—N")
    # Kullanici → Tahmin: iki satır arasındaki boş şeritten dolaşan köşeli yol
    ara_y = (K["alt"] + M["ust"]) / 2
    dirsek(ax, [(K["orta_x"], K["alt"]), (K["orta_x"], ara_y),
                (P["sol"] + 0.055, ara_y), (P["sol"] + 0.055, P["ust"])], "1—N")

    alt_sinir = min(k[3] for k in kutular.values())
    ax.text(0.5, alt_sinir - 0.055,
            "ADNI / OASIS Veri Kullanım Sözleşmesi gereği ham tıbbi görüntüler veritabanında "
            "saklanmaz;\nsunucuda yalnız anonimleştirilmiş meta veriler ve SHA-256 özetleri tutulur.",
            ha="center", va="center", fontsize=5.2, color="#9B2C2C", zorder=5,
            bbox=dict(boxstyle="round,pad=0.45", facecolor=R["hata"],
                      edgecolor="#FC8181", linewidth=0.7))
    kirp(fig, ax, alt_sinir - 0.095, 7.8)
    kaydet(fig, "er")


# ---------------------------------------------------------------- akış yardımcıları
def akis_kutu(ax, y, metin, h=0.040, dolgu="#FFFFFF", punto=5.2, g=0.70, kalin=False):
    x = (1 - g) / 2
    kutu(ax, x, y, g, h, metin, dolgu, punto=punto, kalin=kalin)
    return y


def akis_karar(ax, y, metin, h=0.052, punto=5.0, g=0.46):
    x = (1 - g) / 2
    ax.add_patch(Polygon([[x + g / 2, y + h], [x + g, y + h / 2], [x + g / 2, y], [x, y + h / 2]],
                 closed=True, linewidth=0.8, edgecolor=R["kenar"],
                 facecolor=R["karar"], zorder=2))
    ax.text(x + g / 2, y + h / 2, metin, ha="center", va="center", fontsize=punto, zorder=3)
    return y


def baslat_bitir(ax, y, metin, h=0.030):
    kutu(ax, 0.40, y, 0.20, h, metin, "#2D3748", punto=5.4, kalin=True, yuvarlak=0.02)
    for t in ax.texts[-1:]:
        t.set_color("white")
    return y


# ---------------------------------------------------------------- Şekil 4: ön işleme akışı
def sekil_akis_onisleme():
    fig, ax = eksen(8.8, "Şekil 4. Ön işleme akış diyagramı (§4.4 · A1)")
    y = 0.955
    def ilerle(d=0.0135):
        nonlocal y
        y -= d
    baslat_bitir(ax, y - 0.030, "BAŞLA"); y -= 0.030; ilerle()
    akis_kutu(ax, y - 0.040, "Ham 3B sMRI taraması girişi\n(DICOM klasörü veya .nii / .nii.gz)"); y -= 0.040; ilerle()
    akis_karar(ax, y - 0.052, "Dosya formatı DICOM mu?"); y -= 0.052; ilerle()
    ax.text(0.28, y + 0.022, "evet", fontsize=4.8, color=R["ok"]);
    ax.text(0.70, y + 0.022, "hayır", fontsize=4.8, color=R["ok"])
    akis_kutu(ax, y - 0.036, "evet: dcm2niix ile NIfTI'ye dönüştür    |    hayır: nibabel / SimpleITK ile doğrudan yükle",
              h=0.036, punto=4.9); y -= 0.036; ilerle()
    akis_kutu(ax, y - 0.032, "Görüntü boyutları ve voksel boşluklarını denetle (QA-1)", h=0.032); y -= 0.032; ilerle()

    ADIM = [
        ("Adım 1 · Kafatası ayıklama", R["onisleme"], [
            "Önceden eğitilmiş HD-BET sinir ağını çalıştır",
            "Beyin parankim maskesini (ikili maske) üret",
            "Görüntüyü maskeyle çarparak beyin dışı dokuyu ayıkla"]),
        ("Adım 2 · Manyetik homojensizlik düzeltmesi", R["model"], [
            "SimpleITK N4BiasFieldCorrection filtresini uygula",
            "Düşük frekanslı yoğunluk sapmalarını (B1) düzelt"]),
        ("Adım 3 · Yoğunluk normalizasyonu", R["dogrula"], [
            "Yalnız beyin vokselleri üzerinde ortalama ve std hesapla",
            "Robust z-skor: z = (x − ortalama) / std",
            "Aykırı değerleri kırp ([−2,5 · +2,5]) ve [0, 1]'e ölçekle"]),
        ("Adım 4 · Standart şablona kayıtlama", R["dagitim"], [
            "MNI152 simetrik şablonunu yükle",
            "Afin dönüşüm matrisini hesapla (12 serbestlik derecesi)",
            "1 mm³ izotropik MNI152 uzayına yeniden örnekle"]),
        ("Adım 5 · Kübik tensör kırpma ve kaydetme", R["veri"], [
            "MNI uzayındaki beyni 128×128×128 matrise kırp / ölçekle",
            "Veri tipini float16'ya sıkıştır (disk ve bellek tasarrufu)",
            "<tarama_id>_128cube.npy olarak kaydet"]),
    ]
    for baslik, renk, satirlar in ADIM:
        h = 0.030 + 0.0265 * len(satirlar)
        kusak(ax, 0.10, y - h, 0.80, h, baslik, renk, punto=5.4)
        for i, s in enumerate(satirlar):
            kutu(ax, 0.125, y - 0.028 - (i + 1) * 0.0255 + 0.004, 0.75, 0.0225, s, punto=4.8)
        y -= h; ilerle()

    akis_kutu(ax, y - 0.032, "Kalite kontrolü: voksel yoğunluk dağılımı ve boyut doğrulama (QA-2)", h=0.032); y -= 0.032; ilerle()
    akis_karar(ax, y - 0.050, "Ön işleme başarılı mı?"); y -= 0.050; ilerle()
    akis_kutu(ax, y - 0.052,
              "evet: işlenmiş tensörü model / tahmin katmanına ilet   →   BİTİR\n"
              "hayır: QA-Fail günlüğü oluştur ve kullanıcıya hata bildir   →   SONLAN",
              h=0.052, dolgu=R["hata"], punto=4.9)
    kirp(fig, ax, y - 0.064, 8.8)
    kaydet(fig, "akis_onisleme")


# ---------------------------------------------------------------- Şekil 5: eğitim akışı
def sekil_akis_egitim():
    fig, ax = eksen(8.4, "Şekil 5. Eğitim ve doğrulama akış diyagramı (§4.4 · A2)")
    y = 0.955
    baslat_bitir(ax, y - 0.030, "BAŞLA"); y -= 0.046
    akis_kutu(ax, y - 0.038, "Ön işlenmiş 128³ sMRI tensörlerini yükle"); y -= 0.052

    ASAMA = [
        ("Aşama 1 · Sızıntısız denek düzeyinde bölme (PROTOKOL K1–K3)", R["veri"], [
            "Tüm taramaları denek kimliği (RID) bazında grupla",
            "Kilitli dış test kümesini ayır (yaş / cinsiyet eşlenmiş)",
            "Kalan veriyi 5-kat tabakalı çapraz doğrulamaya böl",
            "Bölme listelerini CSV olarak sabitle · kesişim kümesi = BOŞ"]),
        ("Aşama 2 · Altı model ailesi için eğitim döngüsü", R["model"], [
            "her model için  (P01 · P02 · P06 · P07 · P11 · P12)",
            "    her kat için  (k = 0 … 4)",
            "        3B artırma: ±10° rotasyon, ölçekleme, gürültü, çevirme",
            "        epoch döngüsü: ileri geçiş → AMP (FP16) → sınıf ağırlıklı kayıp",
            "        geri yayılım ve AdamW ile ağırlık güncellemesi",
            "        doğrulama katında BAcc ve AUC hesapla",
            "        yeni en iyi ise ağırlığı kaydet, sabrı sıfırla; değilse sabrı artır",
            "        erken durdurma tetiklendiyse döngüden çık",
            "    beş katın ortalama ± standart sapmasını hesapla"]),
        ("Aşama 3 · PROTOKOL K5 sağlık denetimleri", R["dogrula"], [
            "Ayrılabilir sentetik veride doğrula  (hedef BAcc ≈ 1,000)",
            "Rastgele etiketli veride doğrula  (hedef BAcc ≈ 0,500)",
            "Başarısızsa: model ezberliyor ya da öğrenemiyor → protokol ihlali, dur"]),
        ("Aşama 4 · Bağımsız dış test ve raporlama (PROTOKOL K4)", R["dagitim"], [
            "Eğitilmiş model ağırlıklarını dondur",
            "Kilitli dış test kümesinde sıfır-atış çıkarım yap",
            "Tüm sonuçları koşu kaydı JSON dosyalarına yaz",
            "tablo_uret.py ile SONUCLAR.md tablosunu üret",
            "En başarılı modeli ONNX dağıtımına seç"]),
    ]
    for baslik, renk, satirlar in ASAMA:
        h = 0.030 + 0.0245 * len(satirlar)
        kusak(ax, 0.045, y - h, 0.91, h, baslik, renk, punto=5.5)
        for i, s in enumerate(satirlar):
            girinti = (len(s) - len(s.lstrip())) * 0.0045
            kutu(ax, 0.068 + girinti, y - 0.028 - (i + 1) * 0.0235 + 0.003,
                 0.865 - girinti, 0.0205, s.strip(), punto=4.7, hiza="left")
        y -= h + 0.016
        ok(ax, 0.5, y + 0.016, 0.5, y + 0.002)
    baslat_bitir(ax, y - 0.032, "BİTİR")
    kirp(fig, ax, y - 0.046, 8.4)
    kaydet(fig, "akis_egitim")


# ---------------------------------------------------------------- Şekil 6: tahmin akışı
def sekil_akis_tahmin():
    fig, ax = eksen(8.6, "Şekil 6. Klinik çıkarım ve tahmin akış diyagramı (§4.4 · A3)")
    y = 0.955
    baslat_bitir(ax, y - 0.030, "BAŞLA"); y -= 0.046
    akis_kutu(ax, y - 0.038, "Radyolog web arayüzünden (E1 / E2) 3B sMRI dosyası yükler"); y -= 0.050
    akis_kutu(ax, y - 0.034, "FastAPI servisine istek:  POST /tahmin  (multipart/form-data)", h=0.034); y -= 0.048

    ASAMA = [
        ("Aşama 1 · Dosya doğrulama ve ön işleme", R["onisleme"], [
            "Dosya bütünlüğü ve SHA-256 özeti çıkarılır",
            "Geçerli T1 ağırlıklı beyin MR'ı değilse: 400 Hatalı İstek → dur",
            "Hızlı ön işleme: HD-BET + N4 + MNI afin",
            "128×128×128 float16 tensörü üretilir"]),
        ("Aşama 2 · ONNX Runtime model çıkarımı", R["model"], [
            "Tensör ONNX çıkarım motoruna aktarılır (model.onnx)",
            "İleri geçişle çıkış lojitleri hesaplanır",
            "Softmax ile sınıf olasılıkları: P(NC) · P(MCI) · P(AD)",
            "Nihai klinik karar ve güven skoru belirlenir"]),
        ("Aşama 3 · Açıklanabilirlik (XAI) ısı haritası", R["dogrula"], [
            "Grad-CAM: son evrişim katmanı gradyanları  |  LRP (β=0) / DPM haritası",
            "Isı haritası trilineer enterpolasyonla 128³ hacme büyütülür",
            "En yüksek ilgili anatomik bölge saptanır (ör. bilateral hipokampus)",
            "Aksiyel · koronal · sagital düzlemlerde bindirilmiş PNG dilimler üretilir"]),
        ("Aşama 4 · Veritabanı ve güvenlik kaydı", R["veri"], [
            "Anonim meta veri ve tahmin sonucu veritabanına yazılır",
            "Ham MRI görüntüsü DUA uyarınca bellekten temizlenir"]),
        ("Aşama 5 · Web arayüzü sunumu ve raporlama (E3–E7)", R["dagitim"], [
            "Sonuç JSON paketi arayüze iletilir",
            "Olasılık çubukları, güven skoru ve 3B dilim gezgini çizilir",
            "Talep edilirse klinik karar destek PDF raporu indirilir (E6)"]),
    ]
    for baslik, renk, satirlar in ASAMA:
        h = 0.030 + 0.0255 * len(satirlar)
        kusak(ax, 0.045, y - h, 0.91, h, baslik, renk, punto=5.5)
        for i, s in enumerate(satirlar):
            kutu(ax, 0.068, y - 0.028 - (i + 1) * 0.0245 + 0.003, 0.865, 0.0215, s, punto=4.7)
        y -= h + 0.016
        ok(ax, 0.5, y + 0.016, 0.5, y + 0.002)

    ax.text(0.5, y - 0.030,
            "⚠  YASAL KLİNİK UYARI — her sonuç ekranında ve raporda görünür:\n"
            "\"Bu sistem bir karar destek aracıdır; tek başına tanı yerine geçmez.\"",
            ha="center", va="center", fontsize=5.3, fontweight="bold", color="#9B2C2C",
            bbox=dict(boxstyle="round,pad=0.5", facecolor=R["hata"],
                      edgecolor="#FC8181", linewidth=0.8), zorder=5)
    baslat_bitir(ax, y - 0.092, "BİTİR")
    kirp(fig, ax, y - 0.106, 8.6)
    kaydet(fig, "akis_tahmin")


if __name__ == "__main__":
    print(f"şekiller üretiliyor → {KLASOR}")
    sekil_mimari()
    sekil_usecase()
    sekil_er()
    sekil_akis_onisleme()
    sekil_akis_egitim()
    sekil_akis_tahmin()
    print("altı şekil hazır (200 DPI, 15,5 cm genişlik)")
