# Ertuğrul — kendi Claude sohbetine devir

## A) Yeni sohbete yapıştırılacak prompt

### Önce bunu yap (bir kez, ~15 dk) — prompt'u yapıştırmak TEK BAŞINA yetmez
```powershell
git clone https://github.com/YesilBaraN/tasarim-alzheimer.git
cd tasarim-alzheimer
```
Sonra `README.md` → **"Takım: GitHub'dan nasıl devam edilir"** bölümündeki kurulum adımlarını uygula
(Python 3.12 venv + paketler) ve üç testi yeşile al. Ancak ondan sonra:

- **Claude Code kullanıyorsan:** `tasarim-alzheimer` klasörünü Claude'a açtır, sonra aşağıdaki bloğu yapıştır.
- **claude.ai sohbetindeysen:** klasörü zip'leyip sohbete yükle, sonra bloğu yapıştır. O sohbette dosya
  sistemi yok; Claude'un ürettiği dosyaları indirip sen commit'leyeceksin.

Aşağıdaki **tüm bloğu** (satır başındaki `>` işaretleri olmadan) kopyala:

> **Depo:** https://github.com/YesilBaraN/tasarim-alzheimer — bu klasörün sana açık olduğunu varsayıyorum. Açık değilse ya da dosyaları göremiyorsan önce bunu söyle; klonlama ve ortam kurulumunu `README.md`'deki "Takım" bölümüne göre birlikte yapalım, sonra devam ederiz.
>
> Ben Ertuğrul Kabaoğlu (G231210376), Sakarya Üniversitesi Bilgisayar Mühendisliği, BSM 401 Bilgisayar Mühendisliği Tasarımı dersi, 2026-2027 Güz. Ekip: Ahmet Görkem Yavuz, Baran Yeşilyurt ve ben; danışman Dr. Öğr. Üyesi Can Yüzkollar. Konu: **"Alzheimer Hastalığının Erken Teşhisi İçin 3B Derin Öğrenme Tabanlı Karar Destek Sistemi Geliştirilmesi"** (ADNI T1 sMRI, NC/MCI/AD, 3D-ResNet başta 3B CNN'ler, ≥%85 hedefi, ONNX/API prototip).
>
> Danışmanın şartı: 3 kişi × 5 makale = 15 makale incelenir; her kişi 2'sini implemente eder; 6 uygulama **ortak bir veri setinde** (ADNI1 1.5T başlangıç taramaları; onay gelene dek OASIS-1) **ortak bir protokolle** karşılaştırılır. Makaleleri yapay zekâyla yorumlatarak anlamak kabul.
>
> Dersin 2. aşamasındayız: **Ara Rapor 2 — Analiz ve Tasarım** (detaylı literatür 10–15 kaynak, gereksinim analizi, use-case, mimari blok diyagramı, ER, arayüz mock-up, akış diyagramları, güncel takvim). Rapor teslimi en geç 28 Aralık 2026; ara rapor tarihi bölümden sorulacak.
>
> Yüklediğim `tasarim-alzheimer` klasöründe her şey hazır. Şu sırayla oku: `README.md` → `SUREC.md` (§6 iş bölümü, §9 nerede kaldık) → `makaleler/MAKALE-LISTESI.md` → `makaleler/SABLON-MAKALE-INCELEME.md` → `uygulama/PROTOKOL.md` → `rapor/ARA-RAPOR-2-TASLAK.md` → `uygulama/ertugrul_P11_qiu_fcn/README.md` ve `uygulama/ertugrul_P12_densenet/README.md`.
>
> **Benim grubum C — "Yama/FCN, DenseNet ve Transformer":** P11 Qiu 2020 (FCN yama + risk haritası, kod vkola-lab/brain2020 MIT), P12 Solano-Rojas & Villalón-Fonseca 2021 (düşük maliyetli 3B DenseNet), P13 Lian 2020 (H-FCN), P14 Jang & Hwang 2022 (M3T Transformer), P15 Dhinagar 2023 (ViT vs CNN ön eğitim). İmplemente edeceklerim: **P11 (brain2020 FCN)** ve **P12 (MONAI DenseNet121, spatial_dims=3)**. Rapor sorumluluklarım: sistem mimarisi blok diyagramı (§4.1), veritabanı ER (§4.2), akış diyagramları (§4.4), Gantt (§5).
>
> **Senden istediğim, bu sırayla:**
> 1. Her makale için `makaleler/ertugrul/P1x-*.md` stub'ını **şablondaki 14 bölümü** koruyarak doldur. Tam metni makale listesindeki ücretsiz linkten (PMC/arXiv/CVF/MDPI) kendin oku; link açılamazsa veya web erişimin yoksa ben PDF'i indirip sohbete yüklerim. Her sayının yanına Tablo/§ yaz; emin olmadığını "(doğrulanamadı)" işaretle; Türkçe yaz. P12'de veri setini (ADNI mi OASIS mi) ve "5 sınıf" tanımını özellikle teyit et.
> 2. Her makale bittikten sonra aynı sohbette **"Şimdi hakem ol"** de: özetteki 8–15 kritik sayıyı makaleye karşı tek tek kontrol et, yanlışları düzelt, atlananları ekle, §13 "Opus doğrulama" bölümünü doldur. Örnek: `makaleler/baran/P01-*.md` §13.
> 3. `makaleler/KARSILASTIRMA-15.md` tablosunda P11–P15 satırlarını doldur (P01–P05 satırlarındaki ayrıntı düzeyinde).
> 4. `rapor/ARA-RAPOR-2-TASLAK.md` §2.3'e her makale için 1–2 paragraf; §4.1 mimari blok diyagramı, §4.2 ER ve §4.4 üç akış diyagramı için draw.io/PlantUML taslakları üret (metinde tanımları var).
> 5. İmplementasyon: `uygulama/ertugrul_P11_qiu_fcn/README.md` ve `ertugrul_P12_densenet/README.md` yapılacaklarını izle; `model.py` sözleşmesi `uygulama/ortak/egit.py` başlığında. Kod **yalnız MIT/Apache/BSD** depolardan veya MONAI'den; M3T'nin GPL kodu kopyalanmaz. Kod ve test komutlarını sen yazarsın, ben kendi PC'mde koşarım ve çıktıyı sohbete yapıştırırım (önce `KURULUM.md` ile ortam, `python uygulama\test_model.py` yeşil olmalı). Veri gelene kadar yalnız duman testi koşulabilir; o sürede makale notları, diyagramlar ve rapor bölümleri yapılır.
> 6. Bittiğinde `SUREC.md §9` tablosundaki satırlarımı, `DEVAM.md`'yi ve `MAKALE-LISTESI.md` + `KARSILASTIRMA-15.md` **Durum** sütunlarımı güncelle. İşim GitHub'a commit'lenerek paylaşılıyor (`git pull --rebase` → `git add -A` → `git commit` → `git push`). Bu sohbette dosya sistemi yoksa değiştirdiğin her dosyayı **tam içerikle indirilebilir** olarak ver, ben klasöre koyup commit'lerim. Aynı satırı iki kişi değiştirirse rebase çakışır, o yüzden: Ortak dosyalarda (SUREC, KARSILASTIRMA, ARA-RAPOR) yalnız kendi satır/bölümlerimi düzenle.
>
> Kurallar: bölme her zaman denek (RID) düzeyinde; ADNI verisi paylaşılmaz (DUA); sonuçlar PROTOKOL'e uymuyorsa tabloya girmez; hedef metrik tartışması danışmanla (AD-NC ≥%85 birincil, 3-sınıf ikincil). İç teslimler (varsayım, bölüm tarihi gelince güncellenir): makale notları **6 Kasım**, Ara Rapor 2 katkıları **14–20 Kasım**; 28 Aralık yalnızca final raporun son teslim sınırıdır.

## B) Bu projeyi hazırlayan sohbette Baran'ın yazdığı istemler (sırayla, özet)
1. Formu verdi; "3 kişiyiz, hoca 5'er makale inceleyin, 2'sini implemente edin, ortak veri seti kullanın dedi; 15 makale belirle, 5'erli grupla, süreci de incele, ben Baran'ım, md dosyası yap ki arkadaşlar kendi sohbetinde devam etsin, Sonnet/Opus ile workflow kur".
2. "Sunucuyu sıkıştırma; sen planı ve her şeyi hazırla, gerisini kendi PC'mde çalıştırırım."
3. "Açık kaynaklı kod kullan, erişimi kolay olsun, öğrenciyiz."
4. Ara rapor yönergesini (`Tasarim_ara_raporlar.docx`) verdi: "ikinci aşamadayız, buna göre ilerle, genel taslak buna benzer olacak."

## C) Bulunan sonuçlar (yeniden üretmen gerekmez)
- 15 makale 27 adaydan seçildi; hepsinin tam metni ücretsiz; kod lisansları tabloda. Ruiz 2020 (DenseNet) paywall olduğu için yerine Solano-Rojas 2021 (MDPI açık) alındı.
- Ortak veri: ADNI1 1.5T baseline (≈229 NC / 382 MCI / 187 AD); başvuru danışman adıyla, ~2 hafta; köprü OASIS-1 (CDR 0 = NC, ≥0.5 = demans; üç sınıf OASIS-1'de yapılmaz).
- Literatür: ≥%85 yalnız AD-NC'de gerçekçi; 3 sınıf dış testte ~%50 (Folego 2020); dilim düzeyi bölme %25–55 puan şişirir (Yagis 2021); Lian 2020 H-FCN ADNI-1→ADNI-2 AD-NC 0.903 güçlü referans.
- MONAI'de `DenseNet121(spatial_dims=3, in_channels=1, out_channels=k)` hazır, 3B ön eğitim yok; `monai.visualize.GradCAM` 5B girdiyi destekler. brain2020 PyTorch/MIT, FSL ön işleme kullanıyor — biz kendi `onisle.py` çıktımızı kullanacağız.
- Veritabanı kararı: ADNI görüntüleri DB'ye konmaz; yalnız meta veri + tahmin kayıtları (6 varlık `ARA-RAPOR-2-TASLAK.md §4.2`).
- Ders: BSM 401; rapor şablonu `BSM401_Sablon_201611.docx` bölüm sitesinde; final/teslim 28 Aralık 2026.
