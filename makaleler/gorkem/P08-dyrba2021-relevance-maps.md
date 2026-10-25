# P08 — Dyrba 2021 — Etkileşimli İlgi Haritaları (Interactive Relevance Maps)

> **Durum:** ☑ AI özeti hazır · ☑ Opus doğrulandı · ☐ insan okudu · ☐ implemente edildi  
> **Sorumlu:** Ahmet Görkem Yavuz · **Grup:** B  
> **Tam Metin (Açık Erişim):** https://doi.org/10.1186/s13195-021-00924-2 (BioMed Central / Springer Open) · **arXiv:** https://arxiv.org/abs/2012.10294  
> **Resmî Kod Deposu:** https://github.com/martindyrba/DeepLearningInteractiveVis (MIT Lisansı, Python 3.7 / TF 1.15 / Keras 2.2.4 / iNNvestigate / Bokeh)  
> **Canlı Etkileşimli Web Demosu:** https://explaination.net/demo  

---

## 1. Künye
- **Yazarlar:** Martin Dyrba, Moritz Hanzig, Slawek Altenstein, Sebastian Bader, Tommaso Ballarini, Frederic Brosseron, Katharina Buerger, Daniel Cantré, Peter Dechent, Laura Dobisch, Emrah Düzel, Michael Ewers, Klaus Fliessbach, Wenzel Glanz, John-Dylan Haynes, Michael T. Heneka, Daniel Janowitz, Deniz B. Keles, Ingo Kilimann, Christoph Laske, Franziska Maier, Coraline D. Metzger, Matthias H. Munk, Robert Perneczky, Oliver Peters, Lukas Preis, Josef Priller, Boris Rauchmann, Nina Roy, Klaus Scheffler, Anja Schneider, Björn H. Schott, Annika Spottke, Eike J. Spruth, Marc-André Weber, Birgit Ertl-Wagner, Michael Wagner, Jens Wiltfang, Frank Jessen, Stefan J. Teipel (Alman Nörodejeneratif Hastalıklar Merkezi - DZNE konsorsiyumu, toplam 41 yazar).
- **Yıl / Yayın Yeri:** Kasım 2021, *Alzheimer's Research & Therapy*, Cilt 13, Makale no: 191, ss. 1–17.
- **DOI:** [10.1186/s13195-021-00924-2](https://doi.org/10.1186/s13195-021-00924-2)
- **arXiv ID:** [2012.10294 [cs.CV]](https://arxiv.org/abs/2012.10294)
- **Atıf Sayısı:** Yaklaşık 52 (Google Scholar / Semantic Scholar, 2026 başı itibarıyla).

---

## 2. Tek Paragraf Özet
Bu çalışmada Dyrba ve ark., 3B Evrişimli Sinir Ağlarının (3D-CNN) Alzheimer hastalığı (AD) teşhisinde ulaştığı yüksek sınıflandırma başarımına rağmen klinik rutinde kabul görmemesinin temel nedeni olan "kara kutu" (comprehensibility eksikliği) problemini çözmek amacıyla katman bazlı ilgi yayılımı (LRP) ve etkileşimli görselleştirme mimarisini birleştiren kapsamlı bir klinik karar destek çerçevesi sunmuştur. Model, ADNI-GO/2 kohortundan seçilen $N = 663$ T1-ağırlıklı sMRI taraması (254 CN, 220 MCI, 189 AD; denek başına tek başlangıç taraması) üzerinde 10 katlı çapraz doğrulama ile eğitilmiş; yaş, cinsiyet, toplam kafa içi hacmi (TIV) ve manyetik alan şiddeti kovaryatlarının etkileri sağlıklı kontrol tabanlı doğrusal regresyon artıkları (residuals) ile elenmiştir. Eğitilen modeller, bugüne kadarki en geniş bağımsız çok merkezli harici test havuzlarından birinde ($N = 1.655$ hasta; ADNI-3: 575, AIBL: 606, DELCODE: 474) sınanmış ve AD vs. CN ayrımında tüm bağımsız kohortlarda $\text{AUC} \ge 0,91$ ($0,913 - 0,953$, dengeli doğruluk $\%80,5 - \%85,5$) başarımı elde edilmiştir. iNNvestigate tabanlı LRP ($\alpha=1, \beta=0$ evrişim katmanlarında; $\epsilon=10^{-10}$ tam bağlantılı katmanlarda) ile üretilen 3B ilgi haritaları, klinik altın standart olan hipokampus hacmiyle son derece güçlü ve istatistiksel olarak anlamlı bir ters korelasyon sergilemiş ($r = -0,87, p < 0,001$; 10 kat CV medyanı $r = -0,84$); Bokeh tabanlı açık kaynaklı bir web arayüzü ile klinisyenin hasta bazında 3 eksende dilim gezinimi, AAL atlası anatomik etiketlemesi ve küme eşikleme yapabilmesi sağlanmıştır.

---

## 3. Problem ve Katkı
- **Çözülmeye Çalışılan Problem:**
  - 3B CNN'ler AD/MCI teşhisinde $\ge \%85-\%90$ doğruluklara ulaşsa da, modelin nörolojik olarak hangi doku ve biyobelirteç bölgelerine dayanarak karar verdiği klinisyenler tarafından denetlenememektedir ("kara kutu" sorunu).
  - Standart saliency veya gradyan yöntemleri gürültülüdür; üretilen haritaların bilinen patolojik biyobelirteçlerle (örn. hipokampal atrofi) nicel korelasyonu ve klinik tutarlılığı sistematik olarak doğrulanmamıştır.
  - Literatürdeki birçok CNN çalışması bağımsız dış test seti kullanmadığı için aşırı öğrenme (overfitting) ve genelleme eksikliği yaşamaktadır (Wen 2020 uyarısı).
- **Temel Katkılar (4 Madde):**
  1. **Biyobelirteç Doğrulamalı XAI (LRP & Hipokampus Korelasyonu):** LRP ile üretilen ilgi skorlarının hipokampus bölgesi toplamı ile FreeSurfer/AAL hipokampus hacmi arasında $r \approx -0,86$ ($p < 0,001$) düzeyinde güçlü biyolojik korelasyon kanıtlanmış, modelin ezber yapmadığı klinik olarak doğrulanmıştır (§"CNN model comprehensibility and validation", Şekil 6).
  2. **Geniş Harici Çok Merkezli Doğrulama ($N = 1.655$):** Model yalnızca tek merkezde bırakılmamış; 3 büyük bağımsız kohortta (ADNI-3, AIBL, DELCODE) test edilerek AD vs. CN için $\text{AUC} \ge 0,91$ korunumu gösterilmiştir (Tablo 3).
  3. **Klinik Kovaryat Regresyonu (Yaş/Cinsiyet/TIV/Alan Şiddeti):** Yaşlanmaya bağlı doğal atrofi ile AD patolojisini ayırmak için sağlıklı kontroller üzerinde eğitilen kovaryat regresyonu ile "artık doku hacimleri" (residuals) girdi olarak kullanılmıştır (§"Image preparation and processing", Denklem 1–2).
  4. **Etkileşimli Açık Kaynaklı Web Karar Destek Arayüzü (Bokeh):** Klinisyenlerin 3 eksenli (aksiyel, koronal, sagital) MRI üzerinde interaktif eşik kaydırıcıları, AAL atlası anatomik etiketleri ve küme boyut histogramları ile ilgi haritalarını inceleyebileceği açık kaynaklı bir sistem geliştirilmiştir (Şekil 2, `DeepLearningInteractiveVis`).

---

## 4. Veri Seti ve Bölme
- **Eğitim Seti (ADNI-GO/2):**
  - **Toplam Denek / Tarama:** $N = 663$ katılımcı (denek başına yalnızca 1 adet ilk geçerli T1 MRI ve eşzamanlı AV45-PET taraması seçilmiştir, Tablo 2).
  - **Sınıf Dağılımı:** 254 Sağlıklı Kontrol (CN), 220 Geç Amnestik Hafif Bilişsel Bozukluk (MCI), 189 Alzheimer Demansı (AD).
  - **Alan Şiddeti:** 1.5T ($n=155$; 71 CN, 49 MCI, 35 AD) ve 3T ($n=508$; 183 CN, 171 MCI, 154 AD).
  - **Eğitim Stratejisi (2 Sınıflı Birleştirme):** MCI ve AD hastaları tek bir "hastalık pozitif" grupta birleştirilmiştir ($220 + 189 = 409$ pozitif vs. 254 CN). Gerekçe: Sadece AD ile eğitildiğinde MCI erken evre atrofisine karşı duyarlılığın düşük kalması ve örneklem büyüklüğünü artırarak aşırı öğrenmeyi engellemek (§"CNN model structure and training").
- **Dış Doğrulama / Test Setleri (3 Bağımsız Kohort, Toplam $N = 1.655$):**
  1. **ADNI-3:** $N = 575$ (326 CN, 187 MCI, 62 AD; tamamı 3T MRI, Tablo 2).
  2. **AIBL (Avustralya):** $N = 606$ (448 CN, 96 MCI, 62 AD; 64 adet 1.5T, 542 adet 3T MRI, Tablo 2).
  3. **DELCODE (Almanya - DZNE):** $N = 474$ (215 CN, 155 MCI, 104 AD; tamamı 3T Siemens Prisma/Trio/Verio/Skyra, Tablo 2).
- **Bölme Yöntemi:**
  - Denek (RID) düzeyinde tabakalı 10 katlı çapraz doğrulama (stratified 10-fold CV; her katta yaklaşık 600 eğitim, 60 test görüntüsü).
  - Her katılımcıdan yalnızca tek bir tarama kullanıldığı için denek içi sızıntı sıfırdır.
- **Sızıntı Riski Değerlendirmesi (Wen 2020 Kriterleri):**
  - **Değerlendirme:** **ÇOK DÜŞÜK (Örnek Prosedür).**
  - *Yanlış bölme (K1):* Yok. RID düzeyinde tekil tarama kullanılmıştır.
  - *Geç bölme (K2):* Yok. Çapraz doğrulama bölümleri baştan ayrılmıştır. Kovaryat regresyonu yalnızca eğitim setinin sağlıklı kontrolleri üzerinde fit edilip test setlerine dönüştürücü olarak uygulanmıştır.
  - *Taraflı transfer (K3):* Yok. Ağırlıklar sıfırdan eğitilmiştir.
  - *Bağımsız test eksikliği (K4):* Yok. 3 farklı kıta ve merkezden $N = 1.655$ harici denek kullanılmıştır.

---

## 5. Ön İşleme
Makalede SPM12 (v12.6/r1450) altında çalışan CAT12 (Computational Anatomy Toolbox, v9.6/r7487) kullanılmıştır (§"Image preparation and processing"):
1. **Doku Segmentasyonu:** T1 sMRI hacimleri gri madde (GM), beyaz madde (WM) ve beyin-omurilik sıvısına (CSF) ayrılmıştır.
2. **Uzamsal Normalizasyon & Afin Hizalama:** DARTEL algoritması kullanılarak MNI referans uzayındaki CAT12 varsayılan beyin şablonuna doğrusal olmayan şekilde normalize edilmiştir.
3. **Yeniden Örnekleme (Reslicing):** $1,5\text{ mm}$ izotropik voksel boyutuna yeniden örneklenmiştir.
4. **Modülasyon:** Dokunun yerel hacimsel genişleme ve büzülmelerini korumak için Jacobian determinantı ile modüle edilmiş gri madde haritaları (mGM) elde edilmiştir.
5. **Kovaryat Regresyonu (Residualization - Denklem 1 & 2):**
   - Voksel yoğunluğu $vx_{ij}$ için sağlıklı kontroller ($j \in \text{CN}$) üzerinde doğrusal model kurulmuştur:
     $$vx_{ij} = \beta_{i0} + \beta_{i1} \cdot \text{age}_j + \beta_{i2} \cdot \text{sex}_j + \beta_{i3} \cdot \text{TIV}_j + \beta_{i4} \cdot \text{FS}_j + \varepsilon_{ij}$$
   - Tahmin edilen normal yaşlanma/cinsiyet/TIV/alan şiddeti etkisi çıkarılarak artık haritalar ($res_{ij}$) elde edilmiştir.
6. **Kırpma ve Son Boyut:** Beyin dışı sıfır alanlar kırpılarak ağa beslenen son hacim boyutu **$100 \times 100 \times 120$** voksele getirilmiştir (§"CNN model structure and training").

---

## 6. Mimari
Model, Böhle ve ark. (2019) ile Wen ve ark. (2020)'deki hafif 3B evrişimli mimarilerden esinlenmiş kompakt bir 3D-CNN'dir (§"CNN model structure and training", Şekil 1):

| Katman / Blok | Çekirdek (Kernel) | Filtre / Kanal | Stride / Pad | Çıktı Boyutu | Açıklama / Not |
|---|---|---|---|---|---|
| **Girdi (Input)** | — | 1 | — | $100 \times 100 \times 120$ | Artık gri madde hacmi (veya ham mGM) |
| **Conv3D Blok 1** | $3 \times 3 \times 3$ | 5 | Stride 1, same | $100 \times 100 \times 120$ | ReLU aktivasyonu |
| **MaxPool3D 1** | $2 \times 2 \times 2$ | 5 | Stride 2 | $50 \times 50 \times 60$ | Boyut indirgeme |
| **BatchNorm 1** | — | 5 | — | $50 \times 50 \times 60$ | Batch Normalization |
| **Conv3D Blok 2** | $3 \times 3 \times 3$ | 5 | Stride 1, same | $50 \times 50 \times 60$ | ReLU aktivasyonu |
| **MaxPool3D 2** | $2 \times 2 \times 2$ | 5 | Stride 2 | $25 \times 25 \times 30$ | Boyut indirgeme |
| **BatchNorm 2** | — | 5 | — | $25 \times 25 \times 30$ | Batch Normalization |
| **Conv3D Blok 3** | $3 \times 3 \times 3$ | 5 | Stride 1, same | $25 \times 25 \times 30$ | ReLU aktivasyonu |
| **MaxPool3D 3** | $2 \times 2 \times 2$ | 5 | Stride 2 | $12 \times 12 \times 15$ | Düzleştirme öncesi son özellik haritası ($2.160$ voksel) |
| **BatchNorm 3** | — | 5 | — | $12 \times 12 \times 15$ | Toplam kanal sayısı $\times$ voksel = $5 \times 2.160 = 10.800$ |
| **Flatten** | — | — | — | $10.800$ | Düzleştirme vektörü |
| **Dropout 1** | — | — | — | $10.800$ | Drop rate = %10 ($p=0,10$) |
| **Dense (FC1)** | — | 64 | — | 64 | ReLU, L2 regularizasyonu |
| **Dropout 2** | — | — | — | 64 | Drop rate = %10 ($p=0,10$) |
| **Dense (FC2)** | — | 32 | — | 32 | ReLU, L2 regularizasyonu |
| **Dropout 3** | — | — | — | 32 | Drop rate = %10 ($p=0,10$) |
| **Dense (FC Çıktı)** | — | 2 | — | 2 | Softmax (AD/MCI pozitif vs. CN olasılık skoru) |

- **Toplam Parametre Sayısı:** Yaklaşık $700.000$ (0,7M parametre; son derece hafif ve aşırı öğrenmeye dirençli).
- **Girdi / Çıktı Boyutları:** Girdi: $1 \times 100 \times 100 \times 120$; Çıktı: 2 sınıf (CN vs. AD+MCI).
- **Ön Eğitim:** Yok (rastgele başlatma, scratch).

---

## 7. Eğitim Ayarları
- **Optimizasyon:** Adam optimizörü (§"CNN model structure and training").
- **Öğrenme Hızı (Learning Rate):** Sabit $\eta = 0,0001$ ($1 \times 10^{-4}$).
- **Batch Size:** 20.
- **Epoch Sayısı:**
  - 10-kat CV sırasında: 10 epoch (artık veriler için) / 20 epoch (ham veri kontrolü için).
  - Tüm veri seti üzerinde son model eğitiminde: 4 epoch (artık veriler için) / 8 epoch (ham veriler için; en yüksek test başarımı ve en düşük kayıp noktası).
- **Kayıp Fonksiyonu:** Categorical Cross-Entropy.
- **Sınıf Ağırlıkları (Class Weights):** Sınıf dengesizliğini telafi etmek için formül ($0,5 \cdot N / N_i$) uygulanmış; Kontroller için **1,31**, MCI/AD için **0,81** ağırlık atanmıştır.
- **Veri Artırma (Data Augmentation):**
  - Koronal (sol/sağ - L/R) eksende yatay çevirme (horizontal flip).
  - Üç eksende $\pm 10$ voksel kaydırma (translation $x, y, z$).
  - Bu işlemle epoch başına görüntü sayısı 14 katına çıkarılarak yaklaşık **8.350 görüntüye** ulaşılmıştır.
- **Düzenlileştirme (Regularization):** FC katmanlarında %10 Dropout ve son iki yoğun katmanda L2 norm ağırlık cezası.
- **Donanım ve Eğitim Süresi:** Windows 10, Intel Core i5-9600 6 çekirdek CPU, 64 GB RAM, NVIDIA GeForce GTX 1650 GPU (4 GB VRAM). Kat başına eğitim süresi yaklaşık **35 dakika**, 10 kat toplam süresi **12 saat**.

---

## 8. Sonuçlar

Makaledeki ana sonuçlar Tablo 3'ten birebir derlenmiştir:

| Görev / Kohort | Model | Dengeli Doğruluk (BAcc) | AUC | Test Türü | Kaynak |
|---|---|---|---|---|---|
| **AD vs. CN (ADNI-GO/2)** | 3D-CNN (10-kat CV) | **%88,9 ± %5,3** | **0,949 ± 0,029** | İç (10-kat CV) | Tablo 3 |
| AD vs. CN (ADNI-GO/2) | Hipokampus Hacmi (Altın Std.) | %84,4 ± %3,6 | 0,945 ± 0,024 | İç (10-kat CV) | Tablo 3 |
| **MCI vs. CN (ADNI-GO/2)** | 3D-CNN (10-kat CV) | **%74,5 ± %6,2** | **0,785 ± 0,078** | İç (10-kat CV) | Tablo 3 |
| MCI vs. CN (ADNI-GO/2) | Hipokampus Hacmi | %70,0 ± %6,8 | 0,773 ± 0,091 | İç (10-kat CV) | Tablo 3 |
| **AD+ vs. CN− (Biyobelirteçli)** | 3D-CNN (10-kat CV) | **%94,9 ± %3,8** | **0,985 ± 0,017** | İç (10-kat CV) | Tablo 3 |
| **MCI+ vs. CN− (Biyobelirteçli)** | 3D-CNN (10-kat CV) | **%86,7 ± %10,3** | **0,925 ± 0,071** | İç (10-kat CV) | Tablo 3 |
| **AD vs. CN (ADNI-3, $N=575$)** | 3D-CNN (Son Model / CV Ort.) | %84,4 (%81,7 ± %2,9) | **0,913** (0,899 ± 0,013) | **Dış Bağımsız** | Tablo 3 |
| AD vs. CN (ADNI-3) | Hipokampus Hacmi | %83,4 (%83,4 ± %0,4) | 0,917 | Dış Bağımsız | Tablo 3 |
| **AD vs. CN (AIBL, $N=606$)** | 3D-CNN (Son Model / CV Ort.) | **%85,0** (%82,3 ± %3,0) | **0,950** (0,926 ± 0,007) | **Dış Bağımsız** | Tablo 3 |
| AD vs. CN (AIBL) | Hipokampus Hacmi | %84,1 (%85,3 ± %1,5) | 0,927 | Dış Bağımsız | Tablo 3 |
| **AD vs. CN (DELCODE, $N=474$)** | 3D-CNN (Son Model / CV Ort.) | **%85,5** (%80,5 ± %4,0) | **0,953** (0,938 ± 0,013) | **Dış Bağımsız** | Tablo 3 |
| AD vs. CN (DELCODE) | Hipokampus Hacmi | %88,4 (%86,4 ± %3,0) | 0,943 | Dış Bağımsız | Tablo 3 |
| **MCI vs. CN (ADNI-3)** | 3D-CNN (Son Model / CV Ort.) | %63,1 (%63,6 ± %1,5) | 0,684 (0,677 ± 0,020) | Dış Bağımsız | Tablo 3 |
| **MCI vs. CN (AIBL)** | 3D-CNN (Son Model / CV Ort.) | %68,2 (%67,3 ± %2,7) | 0,763 (0,749 ± 0,012) | Dış Bağımsız | Tablo 3 |
| **MCI vs. CN (DELCODE)** | 3D-CNN (Son Model / CV Ort.) | %71,0 (%69,7 ± %2,6) | 0,775 (0,772 ± 0,017) | Dış Bağımsız | Tablo 3 |

- **Temel Çizgilerle Karşılaştırma:**
  - Model, klinik pratikte radyologların en çok başvurduğu metrik olan "yaş/cinsiyet düzeltilmiş hipokampus hacmi" ile doğrudan kıyaslanmıştır.
  - AD ayrımında CNN modelleri hipokampus hacmine denk veya marjinal düzeyde daha yüksek AUC elde etmiştir (AIBL'de $0,950$ vs. $0,927$; DELCODE'da $0,953$ vs. $0,943$).
  - Yazarlar dürüstçe şu sonuca varmıştır: Klasik AD demansında sadece tanı koymak için 3B CNN kullanmak geleneksel hacimsel ölçümlere kıyasla sınırlı ek kazanç sağlar; asıl kazanım açıklanabilirlik haritaları ve alt tiplerin ayrımıdır (§"Discussion - CNN performance").

---

## 9. Açıklanabilirlik / Ek Analiz
- **Kullanılan XAI Yöntemi:** Katman bazlı İlgi Yayılımı (LRP - Layer-wise Relevance Propagation; iNNvestigate kütüphanesi).
- **LRP Kural Tercihi (Bileşim Kuralı - Denklem 3):**
  - Evrişim (Conv3D) katmanlarında $\alpha=1, \beta=0$ kuralı uygulanmıştır. Bu kural yalnızca hedef sınıfı (AD) pozitif yönde destekleyen aktivasyonları geri yayar; inhibitör zıt işaretli sinyalleri sıfırlar.
  - Tam bağlantılı (Dense) katmanlarda küçük bir payda stabilite sabiti ekleyen $\epsilon$-LRP ($\epsilon = 10^{-10}$) kuralı kullanılmıştır.
- **Biyobelirteç Korelasyonu (Hipokampus Doğrulaması):**
  - AAL atlası bilateral hipokampus maskesi LRP haritalarına uygulanarak her deneğin "hipokampal ilgi skoru" hesaplanmıştır.
  - DELCODE kohortunda hipokampus ilgi skoru ile gerçek hipokampus hacmi arasında **$r = -0,87$ ($p < 0,001$)** düzeyinde çok güçlü bir ters korelasyon tespit edilmiştir (Şekil 6).
  - 10 çapraz doğrulama modelinin tümünde medyan korelasyon **$r = -0,84$** (aralık: $-0,88$ ile $-0,44$, tümü $p < 0,001$) çıkmıştır.
  - Bütün beyin ilgisi ile hipokampus hacmi korelasyonu ise $r = -0,62$ seviyesinde kalarak, modelin ilgisinin hipokampal atrofiye özgül (spesifik) olduğunu kanıtlamıştır.
- **Oklüzyon Duyarlılık Analizi (Occlusion Sensitivity):**
  - Sağlıklı bir kontrol beyninde $20 \times 20 \times 20$ voksellik ($30\text{ mm}$ kenar uzunluğu) bir küp gezdirilerek küp içindeki gri madde yoğunluğu %50 azaltılmış (yapay atrofi simülasyonu) ve modelin AD olasılığı ölçülmüştür.
  - Modelin yapay atrofiye en duyarlı olduğu ve AD olasılığını fırlattığı bölgelerin tam olarak hipokampus, amigdala, talamus ve medial temporal korteks olduğu doğrulanmıştır (Şekil 5).
- **Grup Ortalama Haritaları (Group Mean Relevance):**
  - AD hastalarında bilateral medial temporal lob, parahipokampal girus, orta temporal girus ve singulat kortekste yoğun pozitif ilgi saptanırken; sağlıklı kontrollerde neredeyse sıfır ilgi gözlenmiştir (Şekil 4).

---

## 10. Kod ve Tekrarlanabilirlik
- **Depo:** [martindyrba/DeepLearningInteractiveVis](https://github.com/martindyrba/DeepLearningInteractiveVis) (GitHub)
- **Lisans:** **MIT Lisansı** (Açık kaynak, akademik ve ticari kullanıma tamamen uygun).
- **Teknoloji Yığını:** Python 3.7, TensorFlow 1.15, Keras 2.2.4, iNNvestigate 1.0.9, Bokeh 2.2.3, Nibabel, NumPy, SciPy.
- **Alınabilecek Bileşenler:**
  - Web görselleştirme mimarisi ve Bokeh etkileşim mantığı (`main.py`, dilim kaydırıcıları, eşikleme filtreleri, AAL atlası koordinat eşleme mantığı).
  - Oklüzyon analizi betiği ve hipokampus ilgi korelasyonu hesaplama protokolü.
- **Yeniden Yazılması Gerekenler:**
  - Depo eski TensorFlow 1.15 ve Keras 2.2.4 kullanmaktadır. Bizim projemiz PyTorch 2.x ve MONAI ekosistemindedir.
  - LRP hesaplama mantığı, P06'daki modern PyTorch-LRP modülümüzle (`inverter_util.py`, `innvestigator.py`) veya Torch-LRP ile PyTorch 2.x altında yeniden çalıştırılmalıdır.
- **Eksikler / Zorluklar:**
  - SPM12/CAT12 Matlab bağımlılığı gerektirmektedir. Projemiz saf Python (HD-BET + SimpleITK/ANTsPy) kullandığı için CAT12 kovaryat regresyon adımı harici olarak Python'da uygulanmalıdır.

---

## 11. Güçlü ve Zayıf Yönler
- **Güçlü Yönler:**
  1. **Muazzam Dış Doğrulama:** 3 ayrı bağımsız kohortta ($N=1.655$) test edilmiş ve sonuçların genellenebilirliği tartışmasız şekilde kanıtlanmıştır.
  2. **Biyolojik Doğrulama ($r = -0,87$):** Açıklanabilirlik haritalarının sadece görsel bir illüzyon olmadığını, anatomik hipokampal hacim kaybıyla doğrudan korele olduğunu ispatlamıştır.
  3. **Şeffaf Karşılaştırma:** Hipokampus hacmi gibi yerleşik klinik belirteçlerle dürüstçe karşılaştırılmış, 3D CNN'lerin abartılan yönleri objektif biçimde tartışılmıştır.
  4. **Canlı Web Arayüzü:** Klinisyenin karar sürecine dokunan interaktif bir Bokeh arayüzü sunulmuştur.
- **Zayıf Yönler:**
  1. **Eski Yazılım Altyapısı:** TensorFlow 1.15 ve eski Keras sürümlerine bağımlıdır; modern PyTorch ortamlarına doğrudan taşınamaz.
  2. **Karmaşık Ön İşleme:** CAT12/SPM12 Matlab temellidir ve kovaryat regresyonu klinik acil servis ortamlarında pratik dağıtımı zorlaştırır.
  3. **Basit CNN Mimarisi:** ResNet veya Attention mekanizmaları içermeyen 3 katmanlı klasik bir CNN kullanılmıştır; bu nedenle MCI ayrımındaki AUC ($0,68 - 0,77$) modern dikkat modellerine göre daha mütevazıdır.

---

## 12. Bizim Projeye Uyarlama
- **Bizim Kurulum:** ADNI1 1.5T başlangıç T1 sMRI, NC/MCI/AD, HD-BET kafatası ayıklama $\rightarrow$ N4 bias düzeltme $\rightarrow$ z-score $\rightarrow$ MNI152 afin $\rightarrow$ $128^3$, RID düzeyinde 5-kat CV, birincil görev AD-NC.
- **Neyi Aynen Alıyoruz / Esinleniyoruz?**
  - **Hipokampus XAI Doğrulama Protokolü:** Dyrba'nın AAL atlası hipokampus maskesi ile ilgi haritası voksellerini toplayıp hacim/MMSE ile korelasyon ($r$) hesaplama yöntemini projemizin §9 analiz bölümünde aynen benimsiyoruz.
  - **Arayüz Tasarımı (Mock-up E5 / E6):** Dyrba'nın 3 eksenli (aksiyel, koronal, sagital) senkronize dilim gezinimi, kırmızı dilim ilgi yoğunluk grafiği ve AAL anatomik bölge etiketi kutusu, Ara Rapor 2 arayüz mock-up'larımıza (Bkz. `rapor/ARA-RAPOR-2-TASLAK.md §4.3`) doğrudan esin kaynağı olmuştur.
- **Neyi Değiştiriyoruz?**
  - Çerçeve TF 1.15 yerine modern PyTorch 2.x / MONAI olacaktır.
  - Girdi boyutu $100 \times 100 \times 120$ yerine ortak protokolümüz olan $128 \times 128 \times 128$ olacaktır.
  - Karmaşık CAT12 Matlab regresyonu yerine saf Python tabanlı MONAI ön işleme boru hattı kullanılacaktır.
- **Tahminî VRAM / Süre:** 3 bloklu kompakt CNN $128^3$ boyutta batch size 4 ile yaklaşık 2,1 GB VRAM harcar. T4 GPU'da epoch başına süre ~45 saniyedir.
- **Zorluk Derecesi:** **2 / 5 (Kolay - Orta).** Mimari basittir; asıl efor LRP çıktılarının AAL atlası ile eşleştirilmesindedir.

---

## 13. Opus Doğrulama
_(Bu bölüm bağımsız denetçi / hakem gözüyle doldurulmuştur.)_
- **Sonuç:** **ÇELİŞKİ YOK** (Metin, tablolar ve ek materyaller tam bir tutarlılık içindedir).
- **Kontrol Edilen Sayılar ve Kaynakları:**
  1. *Eğitim veri seti boyutu:* $N = 663$ (254 CN, 220 MCI, 189 AD) $\rightarrow$ Metin §"Study samples", Tablo 2 (Doğrulandı).
  2. *Bağımsız test kohortları toplamı:* $575 + 606 + 474 = 1.655$ denek $\rightarrow$ Özet, §"Study samples", Tablo 2 (Doğrulandı).
  3. *Bağımsız kohort dağılımları:* ADNI-3 ($N=575$, 326 CN, 187 MCI, 62 AD), AIBL ($N=606$, 448 CN, 96 MCI, 62 AD), DELCODE ($N=474$, 215 CN, 155 MCI, 104 AD) $\rightarrow$ Tablo 2 (Doğrulandı).
  4. *AD vs. CN çapraz doğrulama başarımı:* BAcc %88,9 ± %5,3, AUC 0,949 ± 0,029 $\rightarrow$ Tablo 3 (Doğrulandı).
  5. *Bağımsız test AD vs. CN AUC değerleri:* ADNI-3 AUC = 0,913; AIBL AUC = 0,950; DELCODE AUC = 0,953 (Tümü $\ge 0,91$) $\rightarrow$ Özet, Tablo 3 (Doğrulandı).
  6. *Hipokampus hacmi - ilgi skoru korelasyonu:* DELCODE'da $r = -0,87$ ($p < 0,001$); 10-kat CV medyanı $r = -0,84$ (aralık: $-0,88$ ile $-0,44$) $\rightarrow$ §"CNN model comprehensibility and validation", Şekil 6 (Doğrulandı).
  7. *Bütün beyin ilgisi korelasyonu:* $r = -0,62$ ($p < 0,001$) $\rightarrow$ §"CNN model comprehensibility and validation" (Doğrulandı).
  8. *Ağ mimarisi parametresi:* Yaklaşık 700.000 parametre, $100 \times 100 \times 120$ girdi boyutu $\rightarrow$ §"CNN model structure and training" (Doğrulandı).
  9. *Eğitim hiperparametreleri:* Adam, lr = 0,0001, batch = 20, class weights = 1,31 (CN) ve 0,81 (MCI/AD), 14 kat veri artırma (8.350 görüntü/epoch) $\rightarrow$ §"CNN model structure and training" (Doğrulandı).
  10. *LRP kuralları:* Evrişim katmanlarında $\alpha=1, \beta=0$; tam bağlantılı katmanlarda $\epsilon = 10^{-10}$ $\rightarrow$ §"CNN relevance map visualization", Denklem 3 (Doğrulandı).
- **Çelişkiler / Düzeltmeler:**
  - Makale özetinde genel korelasyon "$r \approx -0,86$" olarak ifade edilmişken, metin içinde DELCODE için tek modelde $r = -0,87$, CV medyanında ise $r = -0,84$ olarak detaylandırılmıştır. Bu bir çelişki değil, özet yuvarlamasıdır.
- **Doğrulanamayanlar:** Yok. Tüm sayılar açık erişim makale metninden ve resmî tablolardan doğrulanmıştır.
- **Güven:** **YÜKSEK.**

---

## 14. Kaynaklar
- **Makale (BioMed Central / Springer Open):** https://doi.org/10.1186/s13195-021-00924-2
- **arXiv Ön Baskı:** https://arxiv.org/abs/2012.10294
- **Resmî GitHub Deposu:** https://github.com/martindyrba/DeepLearningInteractiveVis
- **Canlı Web Demosu:** https://explaination.net/demo
- **PubMed Central Kaydı:** [PMC8611956](https://pmc.ncbi.nlm.nih.gov/articles/PMC8611956/)
- **İlgili Kütüphaneler:**
  - iNNvestigate Kütüphanesi: Alber et al. 2019, JMLR ([GitHub](https://github.com/albermax/innvestigate))
  - Bokeh Etkileşimli Görselleştirme: https://bokeh.org
  - CAT12 Araç Kutusu: http://www.neuro.uni-jena.de/cat/
