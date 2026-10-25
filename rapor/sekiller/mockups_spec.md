# Alzheimer 3B-DL Karar Destek Sistemi — Arayüz Tasarımı ve Mock-up Spesifikasyonu (E1–E7)

Bu doküman, BSM 401 Bilgisayar Mühendisliği Tasarımı projesi kapsamında Ahmet Görkem Yavuz (G231210032) tarafından hazırlanan klinik karar destek web arayüzünün (E1–E7) ekran tasarımlarını, bileşenlerini ve kullanıcı etkileşim akışını detaylandırmaktadır.

---

## E1: Giriş ve Kimlik Doğrulama Ekranı
- **Amaç:** Güvenli, rol tabanlı erişim kontrolü sağlamak.
- **Bileşenler:**
  - Kurumsal Logo ve Başlık: "Alzheimer 3B-DL Karar Destek Sistemi (SAÜ BSM 401)".
  - Kullanıcı Giriş Formu: E-posta, Parola, "Beni Hatırla" onay kutusu.
  - Rol Seçici / Göstergesi: Radyolog / Klinisyen, Araştırmacı / Geliştirici, Sistem Yöneticisi.
  - Veri Güvenliği Bildirimi: "Sistemimiz ADNI Veri Kullanım Sözleşmesi (DUA) ve KVKK hükümlerine tam uyumlu olup, kimlik bilgileri sunucuda saklanmaz."

---

## E2: MRI Tarama Yükleme ve Anonimleştirme Ekranı
- **Amaç:** Ham T1 sMRI verisinin sisteme güvenli şekilde aktarılması.
- **Bileşenler:**
  - Sürükle-Bırak Yükleme Alanı: `.nii`, `.nii.gz` veya DICOM `.zip` kabul eder.
  - Anonim Protokol Kimliği: Otomatik üretilen veya kullanıcı tarafından girilen maskelenmiş kod (örn. `ADNI-SUBJ-8412`).
  - Tarama Meta Veri Kartı: Manyetik alan gücü (1.5T / 3T), Sekans türü (T1 MPRAGE), Çözünürlük bilgisi.
  - "Analizi Başlat" Butonu (Birincil CTA).

---

## E3: Otomatik Ön İşleme ve İnferans Durum Ekranı
- **Amaç:** Kullanıcıya arka planda çalışan hesaplama aşamalarını şeffafça göstermek.
- **Bileşenler:**
  - 4 Aşamalı Dinamik İlerleme Çubuğu:
    1. *Kafatasından Arındırma (HD-BET):* Beyin dokusunun segmentasyonu [Tamamlandı - 18 sn].
    2. *Bias Düzeltme (N4ITK):* Manyetik alan homojensizliklerinin giderilmesi [Tamamlandı - 12 sn].
    3. *Uzamsal Hizalama (MNI152):* Şablona afin dönüşüm ve 128³ yeniden boyutlandırma [Tamamlandı - 8 sn].
    4. *Model İnferansı (ONNX Runtime):* 3B tensörün modelden geçirilmesi ve olasılık hesabı [Devam Ediyor...].
  - Durum Mesajı ve Tahmini Kalan Süre Sayacı (örn. "Kalan süre: ~5 saniye").

---

## E4: Klinik Teşhis ve Karar Destek Ekranı
- **Amaç:** Modelin sınıflandırma çıktısını ve güven metriklerini klinik bağlamda sunmak.
- **Bileşenler:**
  - **Zorunlu Yasal ve Klinik Uyarı Rozeti (Sarı/Kırmızı Arka Plan):**
    > **⚠️ DİKKAT:** Bu sistem bir yapay zekâ tabanlı klinik karar destek aracıdır; tek başına kesin tanı yerine geçmez. Nihai klinik karar radyolog ve nörolog hekimin sorumluluğundadır.
  - **Sınıflandırma Olasılık Göstergesi (Yatay Çubuklar):**
    - Sağlıklı Kontrol (NC): `%4.2`
    - Hafif Bilişsel Bozukluk (MCI): `%18.5`
    - Alzheimer Hastalığı (AD): **`%77.3`**
  - **Özet Teşhis Kartı:** "Model Kararı: **Alzheimer Demansı ile Yüksek Uyumlu**", Model Güven Skoru: `%94.1`.
  - **Model Meta Veri Etiketi:** `P07-ResAttNet-v1.0 (ONNX Runtime, 128x128x128 float16)`.
  - Eylemler: "Açıklanabilirlik Haritasını Aç" (E5'e yönlendirir) ve "PDF Rapor Üret" (E6'ya yönlendirir).

---

## E5: 3 Eksenli Açıklanabilirlik (XAI) Görselleştirici Ekranı
- **Amaç:** Kararın anatomik dayanağını hekimin incelemesine sunmak (Dyrba 2021 ve Zhang 2021 esinlenmesi).
- **Bileşenler:**
  - **Üçlü Ortogonal Görünüm:**
    - Panel 1: Aksiyel Düzlem (Transverse, Z ekseni).
    - Panel 2: Koronal Düzlem (Coronal, Y ekseni).
    - Panel 3: Sagital Düzlem (Sagittal, X ekseni).
  - **Dilim Gezinim Kaydırıcıları (Sliders):** Her panelin altında $0 - 127$ dilim seçici.
  - **XAI Yöntem Seçicisi:**
    - `LRP (Layer-wise Relevance Propagation, β=0)` — P06 / P08 tabanlı.
    - `3D Grad-CAM (Layer 3 Feature Map)` — P07 tabanlı.
  - **Isı Haritası Kontrolleri:**
    - Opaklık Kaydırıcısı: `%0` (Salt MRI) $\leftrightarrow$ `%100` (Yalnızca Isı Haritası).
    - Eşikleme (Threshold): Gürültüyü filtrelemek için sadece en yüksek $\%10, \%20, \%30$ aktivasyonları göster.
  - **Anatomik Atlas Etiketi Kutusu (AAL / Brainnetome):** İmlecin bulunduğu voksele karşılık gelen bölge adı (örn. *Bilateral Hipokampus / Medial Temporal Korteks — Bağıl İlgi Skoru: 0.892*).

---

## E6: Klinik Rapor Önizleme ve İndirme Ekranı (PDF)
- **Amaç:** Sağlık bilgi sistemlerine (PACS/HIS) entegre edilebilir standart bir karar destek çıktısı oluşturmak.
- **Bileşenler:**
  - PDF Önizleme Penceresi:
    - Kurum Başlığı ve Analiz Tarihi.
    - Anonim Hasta Kimliği ve Görüntü Özellikleri.
    - Model Teşhis Olasılıkları ve Güven Skoru.
    - Hipokampus Seviyesinden 3 Düzlemli Isı Haritası Kesitleri.
    - Model Sürümü ve ONNX Model Hash Değeri.
    - Standart Klinik Sorumluluk Reddi Beyanı.
  - İndirme Butonu: "Klinik Raporu İndir (.PDF)".
  - Arşiv Butonu: "Raporu Güvenli Veritabanına Kaydet".

---

## E7: Çoklu Model Karşılaştırma Paneli (Araştırmacı Ekranı)
- **Amaç:** Ekip üyelerinin 6 farklı modelini ve temel çizgilerini aynı test protokolü üzerinde yan yana değerlendirmek.
- **Bileşenler:**
  - Karşılaştırmalı Metrik Tablosu (`SONUCLAR.md` entegrasyonu):
    - Sütunlar: Model Adı, Dengeli Doğruluk (BAcc), AUC, Duyarlılık, Özgüllük, F1 Skoru, İnferans Süresi (ms), VRAM (MB).
    - Satırlar: P01 (VoxCNN), P02 (Med3D ResNet), P06 (CNN+LRP), P07 (ResAttNet), P11 (FCN), P12 (DenseNet121), SVM Baseline.
  - İnteraktif ROC Eğrileri Çizimi (Plotly): Tüm modellerin aynı grafik üzerinde ROC eğrileri.
  - Karışıklık Matrisi (Confusion Matrix) Seçicisi.
  - Harici Test Genellenebilirlik Grafiği: ADNI-1 içi test vs. OASIS-1 köprü testi düşüş oranları.
