# Görkem — kendi Claude sohbetine devir

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
> Ben Ahmet Görkem Yavuz (G231210032), Sakarya Üniversitesi Bilgisayar Mühendisliği, BSM 401 Bilgisayar Mühendisliği Tasarımı dersi, 2026-2027 Güz. Ekip: Ertuğrul Kabaoğlu, Baran Yeşilyurt ve ben; danışman Dr. Öğr. Üyesi Can Yüzkollar. Konu: **"Alzheimer Hastalığının Erken Teşhisi İçin 3B Derin Öğrenme Tabanlı Karar Destek Sistemi Geliştirilmesi"** (ADNI T1 sMRI, NC/MCI/AD, 3D-ResNet başta 3B CNN'ler, ≥%85 hedefi, ONNX/API prototip).
>
> Danışmanın şartı: 3 kişi × 5 makale = 15 makale incelenir; her kişi 2'sini implemente eder; 6 uygulama **ortak bir veri setinde** (ADNI1 1.5T başlangıç taramaları; onay gelene dek OASIS-1) **ortak bir protokolle** karşılaştırılır. Makaleleri yapay zekâyla yorumlatarak anlamak kabul.
>
> Dersin 2. aşamasındayız: **Ara Rapor 2 — Analiz ve Tasarım** (detaylı literatür 10–15 kaynak, gereksinim analizi, use-case, mimari blok diyagramı, ER, arayüz mock-up, akış diyagramları, güncel takvim). Rapor teslimi en geç 28 Aralık 2026; ara rapor tarihi bölümden sorulacak.
>
> Yüklediğim `tasarim-alzheimer` klasöründe her şey hazır. Şu sırayla oku: `README.md` → `SUREC.md` (§6 iş bölümü, §9 nerede kaldık) → `makaleler/MAKALE-LISTESI.md` → `makaleler/SABLON-MAKALE-INCELEME.md` → `uygulama/PROTOKOL.md` → `rapor/ARA-RAPOR-2-TASLAK.md` → `uygulama/gorkem_P06_bohle/README.md` ve `uygulama/gorkem_P07_resattnet/README.md`.
>
> **Benim grubum B — "Dikkat mekanizmaları ve açıklanabilirlik":** P06 Böhle 2019 (LRP), P07 Zhang 2021 (3D ResAttNet + Grad-CAM), P08 Dyrba 2021, P09 Hoang 2023 (3D-DAM), P10 Jin 2020 (3DAN). İmplemente edeceklerim: **P06 (3B CNN + LRP, kod moboehle/Pytorch-LRP BSD-3)** ve **P07 (MONAI ResNet + öz-dikkat + MONAI GradCAM)**. Rapor sorumluluklarım: gereksinim analizi (§3), use-case diyagramı, arayüz mock-up'ları (§4.3), XAI görselleri.
>
> **Senden istediğim, bu sırayla:**
> 1. Her makale için `makaleler/gorkem/P0x-*.md` stub'ını **şablondaki 14 bölümü** koruyarak doldur. Tam metni makale listesindeki ücretsiz linkten (PMC/arXiv) kendin oku; link açılamazsa veya web erişimin yoksa ben PDF'i indirip sohbete yüklerim. Her sayının yanına Tablo/§ yaz; emin olmadığını "(doğrulanamadı)" işaretle; Türkçe yaz. Makale başına bir tur.
> 2. Her makale bittikten sonra aynı sohbette **"Şimdi hakem ol"** de: özetteki 8–15 kritik sayıyı makaleye karşı tek tek kontrol et, yanlış olanları düzelt, atlananları ekle, §13 "Opus doğrulama" bölümünü doldur (ÇELİŞKİ YOK / VAR, güven). Baran'ın P01–P05 notlarında bunun nasıl göründüğünü `makaleler/baran/P01-*.md` §13'te görebilirsin.
> 3. `makaleler/KARSILASTIRMA-15.md` tablosunda P06–P10 satırlarını doldur (P01–P05 satırlarındaki ayrıntı düzeyinde).
> 4. `rapor/ARA-RAPOR-2-TASLAK.md` §2.2'ye her makale için 1–2 paragraf; §3 gereksinim tablolarını gözden geçir ve use-case diyagramı için PlantUML/draw.io taslağı üret.
> 5. İmplementasyon: `uygulama/gorkem_P06_bohle/README.md` ve `gorkem_P07_resattnet/README.md` yapılacaklarını izle; `model.py` sözleşmesi `uygulama/ortak/egit.py` başlığında (`olustur(varyant, sinif_sayisi, girdi_boyut, **kw)`). Kod **yalnız MIT/Apache/BSD** depolardan veya MONAI'den; GPL kopyalanmaz. Kod ve test komutlarını sen yazarsın, ben kendi PC'mde koşarım ve çıktıyı sohbete yapıştırırım (önce `KURULUM.md` ile ortam, `python uygulama\test_model.py` yeşil olmalı). Veri gelene kadar yalnız duman testi koşulabilir; o sürede makale notları ve rapor bölümleri yapılır.
> 6. Bittiğinde `SUREC.md §9` tablosundaki satırlarımı, `DEVAM.md`'yi ve `MAKALE-LISTESI.md` + `KARSILASTIRMA-15.md` **Durum** sütunlarımı güncelle. İşim GitHub'a commit'lenerek paylaşılıyor (`git pull --rebase` → `git add -A` → `git commit` → `git push`). Bu sohbette dosya sistemi yoksa değiştirdiğin her dosyayı **tam içerikle indirilebilir** olarak ver, ben klasöre koyup commit'lerim. Aynı satırı iki kişi değiştirirse rebase çakışır, o yüzden: Ortak dosyalarda (SUREC, KARSILASTIRMA, ARA-RAPOR) yalnız kendi satır/bölümlerimi düzenle, başkasının bölümüne dokunma.
>
> Kurallar: bölme her zaman denek (RID) düzeyinde; ADNI verisi paylaşılmaz (DUA); sonuçlar PROTOKOL'e uymuyorsa tabloya girmez; hedef metrik tartışması danışmanla (AD-NC ≥%85 birincil, 3-sınıf ikincil). İç teslimler (varsayım, bölüm tarihi gelince güncellenir): makale notları **6 Kasım**, Ara Rapor 2 katkıları **14–20 Kasım**; 28 Aralık yalnızca final raporun son teslim sınırıdır.

## B) Bu projeyi hazırlayan sohbette Baran'ın yazdığı istemler (sırayla, özet)
1. Formu verdi; "3 kişiyiz, hoca 5'er makale inceleyin, 2'sini implemente edin, ortak veri seti kullanın dedi; 15 makale belirle, 5'erli grupla, süreci de incele, ben Baran'ım, md dosyası yap ki arkadaşlar kendi sohbetinde devam etsin, Sonnet/Opus ile workflow kur".
2. "Sunucuyu sıkıştırma; sen planı ve her şeyi hazırla, gerisini kendi PC'mde çalıştırırım."
3. "Açık kaynaklı kod kullan, erişimi kolay olsun, öğrenciyiz."
4. Ara rapor yönergesini (`Tasarim_ara_raporlar.docx`) verdi: "ikinci aşamadayız, buna göre ilerle, genel taslak buna benzer olacak."

## C) Bulunan sonuçlar (yeniden üretmen gerekmez)
- 15 makale 27 adaydan seçildi; hepsinin tam metni ücretsiz; kod lisansları tabloda (`MAKALE-LISTESI.md`).
- Ortak veri: ADNI1 1.5T baseline (≈229 NC / 382 MCI / 187 AD); başvuru danışman adıyla, ~2 hafta; köprü OASIS-1. Kaggle 4-sınıf setleri reddedildi (kaynağı belirsiz, 2B, sızıntı).
- Literatür: ≥%85 yalnız AD-NC'de gerçekçi; 3 sınıf dış testte ~%50 (Folego 2020); dilim düzeyi bölme %25–55 puan şişirir (Yagis 2021).
- Ön işleme zinciri ve kod iskeleti hazır (`onisleme/onisle.py`, `uygulama/ortak/`), sunucuda test edilmedi; kendi PC'de `test_onisle.py` ve `test_model.py` koşulacak.
- P07 ResAttNet'in resmî kodu yok → MONAI ResNet + öz-dikkat bloğu + `monai.visualize.GradCAM` (5B girdiyi destekler). P06 Pytorch-LRP BSD-3, ADNI not defterleri içinde. P08 Dyrba kodu MIT ama TensorFlow 1.15 (eski) → yalnız okunur.
- Ders: BSM 401; rapor şablonu `BSM401_Sablon_201611.docx` ve poster şablonu bölüm sitesinde; final/teslim 28 Aralık 2026; not ağırlıkları yayında yok.
