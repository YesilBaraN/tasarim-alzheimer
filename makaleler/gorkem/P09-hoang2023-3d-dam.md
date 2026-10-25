# P09 — Hoang 2023 — 3D-DAM Çift Dikkat Modülü (Dual Attention Module)

> **Durum:** ☑ AI özeti hazır · ☑ Opus doğrulandı · ☐ insan okudu · ☐ implemente edildi  
> **Sorumlu:** Ahmet Görkem Yavuz · **Grup:** B  
> **Tam Metin (Açık Erişim):** https://arxiv.org/abs/2310.12574 · **PDF:** https://arxiv.org/pdf/2310.12574.pdf  
> **Resmî Kod Deposu:** Makalede doğrudan link verilmemiş (`— (makalede yok)`); Clinica / PyTorch CBAM tabanlı açık mimari.  

---

## 1. Künye
- **Yazarlar:** Gia Minh Hoang, Youngjoo Lee, Jae Gwan Kim (Biyomedikal Bilim ve Mühendislik Bölümü, Gwangju Bilim ve Teknoloji Enstitüsü - GIST, Kore Cumhuriyeti).
- **Yıl / Yayın Yeri:** Ekim 2023, arXiv ön baskı, arXiv:2310.12574v1 [cs.CV], ss. 1–13.
- **DOI / arXiv:** [arXiv:2310.12574](https://arxiv.org/abs/2310.12574)
- **Atıf Sayısı:** Yaklaşık 8 (Google Scholar, 2026 başı itibarıyla yeni yayın).

---

## 2. Tek Paragraf Özet
Bu çalışmada Hoang ve ark., yapısal manyetik rezonans görüntülerinden (sMRI) Alzheimer hastalığı (AD) teşhisi ve Hafif Bilişsel Bozukluğun (MCI) AD'ye ilerlemesinin (pMCI vs. sMCI) tahmini için 3B Evrişimli Blok Dikkat Modülü (CBAM) mantığını 3B hacimsel alana uyarlayan "3D-DAM" (3D Dual Attention Module) mimarisini önermiştir. Veri sızıntısını (data leakage) engellemek amacıyla ADNI veri tabanından seçilen 1.426 denek ($5.552$ seans; 403 AD, 653 CN, 165 pMCI, 205 sMCI) Clinica yazılımının `t1-linear` boru hattı (N4 bias düzeltme + ANTs SyN ile ICBM 2009c MNI şablonuna afin hizalama) üzerinden BIDS formatına dönüştürülmüştür. Önerilen 3D-DAM ağı; kanal dikkat mekanizmasıyla (3B AvgPool ve MaxPool + paylaşımlı MLP) hangi dilim ve özelliklerin anlamlı olduğuna odaklanırken, uzamsal dikkat mekanizmasıyla (kanal ekseninde ortalama/maksimum havuzlama + 3B Conv) beyin içerisindeki kritik patolojik hacimsel koordinatları vurgulamaktadır. Model, ADNI test setinde AD vs. CN için **%98,18 ± %0,42** doğruluk (Duyarlılık: %96,73, Özgüllük: %98,97) ve pMCI vs. sMCI için **%91,78 ± %0,63** doğruluk (Duyarlılık: %95,06, Özgüllük: %88,62) elde ederek son teknoloji (SOTA) başarıma ulaşmıştır. Yöntemin genellenebilirliği iki harici bağımsız veri setinde (AIBL: %86,37 doğruluk; OASIS-1: %83,42 doğruluk) ve tersine eğitim deneyinde (AIBL+OASIS eğitim $\rightarrow$ ADNI test: %85,4 doğruluk) doğrulanmış; 3B Grad-CAM görselleştirmeleri ile modelin kararlarını hipokampus, amigdala ve medial temporal lob atrofisine dayandırdığı gösterilmiştir.

---

## 3. Problem ve Katkı
- **Çözülmeye Çalışılan Problem:**
  - Klasik AD vs. CN ikili sınıflandırması klinik olarak geç evre bir teşhistir; asıl klinik değer taşıyan erken evre MCI ilerlemesinin (pMCI vs. sMCI) saptanması zorlu ve modellerin başarımının düşük kaldığı bir alandır.
  - Standart 3B CNN'ler tüm beyin hacmine eşit ağırlık vermekte, küçük ama kritik patolojik bölgeleri (hipokampus, entorinal korteks) gözden kaçırmaktadır.
  - Literatürdeki birçok derin öğrenme çalışması bağımsız dış veri setlerinde sınanmadığı için genellenebilirlik yetersizliği yaşamakta ve Wen ve ark. (2020) tarafından vurgulanan veri sızıntısı (yanlış/geç bölme) tuzaklarına düşmektedir.
- **Temel Katkılar (3 Madde):**
  1. **3B Çift Dikkat Modülü (3D-DAM):** 2B CBAM modülünü 3B medikal tensörlere genişleterek hem kanallar arası (dilim/öznitelik düzeyi) hem de uzamsal (3B anatomik koordinat düzeyi) dikkat haritalarını ardışık olarak çıkaran ve rezidüel bloklarla birleştiren hafif bir mimari sunulmuştur (§2.2, Şekil 2).
  2. **Yüksek pMCI/sMCI Başarımı:** Erken evre MCI ilerleme tahmininde ADNI test setinde %91,78 doğruluk ve %95,06 duyarlılık elde edilerek literatürdeki en yüksek skorlardan birine ulaşılmıştır (Tablo 2).
  3. **Çift Yönlü Harici Genellenebilirlik Doğrulaması:** Model yalnızca ADNI içinde bırakılmamış; AIBL ve OASIS-1 harici veri setlerinde doğrudan sınanmış (%86,37 ve %83,42), ayrıca tam tersi senaryoda (AIBL+OASIS ile eğitilip ADNI'da test edilerek %85,4) çapraz platform dayanıklılığı kanıtlanmıştır (§3.2, Tablo 4).

---

## 4. Veri Seti ve Bölme
- **Kaynak Veri Tabanları ve Denek Dağılımı:**
  1. **ADNI (Eğitim ve İç Test - Tablo 1):**
     - AD: 403 denek, 1.241 seans (Yaş: $75,65 \pm 7,8$, Cinsiyet: 225 E / 178 K).
     - CN: 653 denek, 2.564 seans (Yaş: $76,15 \pm 4,9$, Cinsiyet: 277 E / 376 K).
     - pMCI: 165 denek, 825 seans (Yaş: $75,44 \pm 7,27$, Cinsiyet: 104 E / 64 K).
     - sMCI: 205 denek, 922 seans (Yaş: $74,64 \pm 5,14$, Cinsiyet: 121 E / 84 K).
     - Toplam ADNI: **1.426 denek, 5.552 seans/tarama** (1.5T T1-ağırlıklı sMRI).
  2. **AIBL (Harici Test Seti 1 - Tablo 3):**
     - AD: 77 denek (Yaş: $84 \pm 25,7$, 34 E / 43 K).
     - CN: 449 denek (Yaş: $73,96 \pm 6,5$, 187 E / 262 K). Toplam: 526 denek.
  3. **OASIS-1 (Harici Test Seti 2 - Tablo 3):**
     - AD: 100 denek (Yaş: $76,76 \pm 7,11$, 41 E / 59 K).
     - CN: 316 denek (Yaş: $65 \pm 13,89$, 119 E / 197 K). Toplam: 416 denek.
- **Bölme Yöntemi:**
  - Wen ve ark. (2020) ve ClinicaDL standartlarına uygun olarak denek (RID / Subject ID) düzeyinde ayrılmıştır (§2.1).
  - Tablo 2'de ortalama ve standart sapma ($\pm$) değerleri raporlanmıştır; ancak metinde kaç katlı çapraz doğrulama yapıldığı açıkça yazılmamıştır (`(metinde kat sayısı açıkça yazılmamış; ClinicaDL standardı 5-kat CV)`).
- **Sızıntı Riski Değerlendirmesi (Wen 2020 Kriterleri):**
  - **Değerlendirme:** **DÜŞÜK - ORTA.**
  - *Gerekçe:* Clinica yazılımının `adni-to-bids` ve `t1-linear` boru hatları kullanılarak RID bazında ayrım yapıldığı açıkça vurgulanmıştır. Ancak çoklu seansların (örneğin 165 pMCI hastasından 825 seans) çapraz doğrulamada eğitim ve test arasına seans bazlı sızıp sızmadığı konusunda metinde tam detay verilmemiştir; harici test setlerindeki (AIBL, OASIS-1) %83–%86 doğruluk başarımı modelin genellenebilir olduğunu doğrulamaktadır.

---

## 5. Ön İşleme
Makalede açık kaynaklı Clinica yazılımının `t1-linear` boru hattı kullanılmıştır (§2.1, Şekil 1):
1. **BIDS Dönüşümü:** ADNI verileri BIDS (Brain Imaging Data Structure) formatına getirilmiştir (`adni-to-bids`).
2. **Kafatasından Arındırma ve Bias Düzeltme:** Manyetik alan homojensizlikleri N4ITK (Tustison et al. 2010) algoritmasıyla düzeltilmiştir.
3. **Afin Hizalama:** ANTs yazılım paketinin SyN algoritması kullanılarak MNI uzayındaki ICBM 2009c doğrusal olmayan simetrik şablonuna afin (lineer) kayıt yapılmıştır.
4. **Hacim Boyutu:** Metin içinde son tensör matris boyutu rakamsal olarak belirtilmemiştir (`(makalede belirtilmemiş; Clinica t1-linear varsayılanı 169x208x179 veya kırpılmış standart MNI hacmidir)`).

---

## 6. Mimari

Model; evrişimli kök katmanı, iki adet çift dikkat modülü (DAM), rezidüel bloklar, global ortalama havuzlama ve tam bağlantılı sınıflandırıcıdan oluşmaktadır (§2.2 & §2.3, Şekil 2 & Şekil 3):

### A. Çift Dikkat Modülü (DAM) Formülasyonu
1. **Kanal Dikkat Modülü (Channel Attention):**
   - Girdi özellik haritası: $F \in \mathbb{R}^{C \times H \times W \times D}$.
   - Uzamsal boyutlar boyunca 3B ortalama havuzlama ve maksimum havuzlama uygulanır:
     $$F_{avg}^c = \text{AvgPool}(F), \quad F_{max}^c = \text{MaxPool}(F) \quad \in \mathbb{R}^{C \times 1 \times 1 \times 1}$$
   - Parametreleri paylaşımlı çok katmanlı algılayıcı (shared MLP) uygulanır ve toplanır:
     $$F_{out}^c = \sigma\left(\text{MLP}(F_{avg}^c) + \text{MLP}(F_{max}^c)\right)$$
     $$F' = F \otimes F_{out}^c$$
2. **Uzamsal Dikkat Modülü (Spatial Attention):**
   - Kanal ekseni boyunca ortalama ve maksimum işlemler uygulanır:
     $$F_{mean}^s = \text{torch.mean}(F', \text{dim}=1), \quad F_{max}^s = \text{torch.max}(F', \text{dim}=1)$$
   - Bu haritalar toplanıp (veya birleştirilip) $3\times3\times3$ Conv3D ve sigmoid filtresinden geçirilir:
     $$F_{out}^s = \sigma\left(\text{Conv3D}(F_{mean}^s + F_{max}^s)\right)$$
     $$F'' = F' \otimes F_{out}^s$$

### B. Katman / Blok Akış Tablosu

| Katman / Blok | Çekirdek (Kernel) / Filtre | Açıklama |
|---|---|---|
| **Girdi (Input)** | $1 \times H \times W \times D$ | 3B sMRI hacmi |
| **Giriş Conv3D** | 8 kanal (metinde "8x8x8 kernel" yazılmış) | BatchNorm + ReLU |
| **Rezidüel Blok 1** | 16 kanal ve 32 kanal | 2 ardışık Conv3D + BN + ReLU + Skip Connection |
| **DAM Modülü 1** | Kanal Dikkat + Uzamsal Dikkat | $F \rightarrow F''$ öznitelik ağırlıklandırma |
| **Rezidüel Blok 2** | 64 kanal | Conv3D + BN + ReLU + Skip Connection |
| **DAM Modülü 2** | Kanal Dikkat + Uzamsal Dikkat | İkinci aşama odaklanma |
| **Global AvgPool** | — | Özellik haritalarını tek vektöre indirgeme |
| **Dense (FC)** | 2 nöron | Softmax çıkışı (AD vs. CN veya pMCI vs. sMCI) |

- **Parametre Sayısı:** Belirtilmemiş (`— (makalede yok); hafif CBAM türevi, ~1,5M - 2,5M tahmin edilmektedir`).

---

## 7. Eğitim Ayarları
- **Optimizasyon:** SGD (Metinde ilginç şekilde: *"SGD optimizer with a first momentum of 0.9 and the second momentum of 0.999"* ifadesi yer almaktadır; muhtemelen Adam formülasyonu SGD adıyla yazılmıştır veya PyTorch SGD momentum=0.9 kullanılmıştır, §2.4).
- **Öğrenme Hızı (Learning Rate):** Başlangıç $\eta = 10^{-7}$ ($1 \times 10^{-7}$).
- **Düzenlileştirme:** L2-Regularization (Weight Decay) $= 10^{-6}$.
- **Batch Size:** 16.
- **Epoch Sayısı:** 200 epoch.
- **Kayıp Fonksiyonu:** Cross-Entropy Loss.
- **Donanım:** Intel Xeon Gold 6258R CPU @ 2.70GHz, 256 GB RAM, **4 $\times$ NVIDIA GeForce RTX 3090 (24 GB)**.
- **Yazılım:** Python, PyTorch.

---

## 8. Sonuçlar

Makaledeki birincil ve harici test sonuçları Tablo 2 ve Tablo 4'ten birebir derlenmiştir:

### A. ADNI Test Seti Başarımı (Tablo 2)
| Yöntem / Model | AD vs. CN Doğruluk (Acc) | AD vs. CN Duyarlılık (Sen) | AD vs. CN Özgüllük (Spec) | pMCI vs. sMCI Doğruluk (Acc) | pMCI vs. sMCI Duyarlılık (Sen) | pMCI vs. sMCI Özgüllük (Spec) |
|---|---|---|---|---|---|---|
| Zhang et al. 2021 [20] | %97,35 | %97,10 | %97,95 | %78,79 | %75,16 | %82,42 |
| Zhu et al. 2021 [21] | %92,40 | %91,00 | %93,80 | %80,20 | %77,10 | %82,60 |
| Ashtari-Majlan 2022 [22] | %97,78 | %95,59 | %99,82 | %79,90 | %75,55 | %99,70 |
| Wang et al. 2022 [23] | — | — | — | %87,80 | %88,00 | %88,00 |
| Zhang et al. 2022 (P07) [6]| %91,30 | %91,00 | %91,90 | %82,10 | %81,20 | %80,90 |
| **Önerilen 3D-DAM** | **%98,18 ± %0,42** | **%96,73 ± %1,08** | **%98,97 ± %0,51** | **%91,78 ± %0,63** | **%95,06 ± %1,11** | **%88,62 ± %1,15** |

### B. Harici Veri Setlerinde Genellenebilirlik Başarımı (Tablo 4)
| Deney Türü | Eğitim Seti | Test Seti | Doğruluk (Acc) | Duyarlılık (Sen) | Özgüllük (Spec) |
|---|---|---|---|---|---|
| **Deney 1 (Harici Test)** | ADNI | **AIBL ($N=526$)** | **%86,30** (%86,37) | %80,20 | %87,10 |
| **Deney 1 (Harici Test)** | ADNI | **OASIS-1 ($N=416$)** | **%83,40** (%83,42) | %85,80 | %82,60 |
| **Deney 2 (Tersine Test)** | AIBL + OASIS-1 | **ADNI ($N=1.056$)** | **%85,40** | %80,10 | %89,50 |

---

## 9. Açıklanabilirlik / Ek Analiz
- **Kullanılan XAI Yöntemi:** 3B Grad-CAM (Gradient-weighted Class Activation Mapping).
- **Görselleştirilen Katman:** Son evrişimli dikkat blokları.
- **Saptanan Patolojik Bölgeler:**
  - Modelin en yüksek dikkat skoru ürettiği anatomik bölgeler aksiyel, koronal ve sagital düzlemlerde incelenmiştir (§3.3, Şekil 6).
  - En belirgin aktivasyonların **hipokampus**, **amigdala** ve **medial temporal lob** üzerinde yoğunlaştığı saptanmıştır.
  - Bu bulgular, Alzheimer patolojisindeki nörofibriler yumak birikimi ve hücresel kayıpla birebir uyumlu nörolojik kanıtlar sunmaktadır.

---

## 10. Kod ve Tekrarlanabilirlik
- **Depo Durumu:** Makalede doğrudan GitHub adresi verilmemiştir (`— (makalede yok)`).
- **Teknoloji Yığını:** Python, PyTorch.
- **Tekrarlanabilirlik Durumu:**
  - Makale başlığında "A reproducible 3D convolutional neural network..." ifadesi geçmekle birlikte kodun açık bir linki verilmemiştir.
  - Bununla birlikte, Clinica yazılımının `t1-linear` boru hattı tamamen açık kaynaklıdır (`pip install clinica`).
  - Çift Dikkat Modülü (DAM), standart 2B CBAM modülünün (Woo et al. 2018) `nn.Conv3d`, `nn.AdaptiveAvgPool3d` ve `nn.AdaptiveMaxPool3d` ile 3B'ye genişletilmiş doğrudan bir uyarlamasıdır; PyTorch ile sıfırdan implementasyonu 60–80 satır temiz kod ile kolayca gerçekleştirilebilir.

---

## 11. Güçlü ve Zayıf Yönler
- **Güçlü Yönler:**
  1. **Yüksek pMCI Tahmini:** Erken teşhis açısından kritik olan pMCI vs. sMCI görevinde %91,78 doğruluk ve %95,06 duyarlılık elde edilmiştir.
  2. **Çift Yönlü Harici Doğrulama:** AIBL ve OASIS-1 gibi iki farklı bağımsız merkezde test edilmiş; ayrıca tersine eğitimle modelin aşırı ezber yapmadığı ispatlanmıştır.
  3. **Clinica Standartlarına Uyum:** Veri hazırlığında Clinica ve BIDS standartları izlenerek Wen 2020 sızıntı riskleri en aza indirilmiştir.
- **Zayıf Yönler:**
  1. **Kod Deposu Eksikliği:** Makalede doğrudan bir GitHub bağlantısı paylaşılmamıştır.
  2. **Yazım / Terminoloji Hataları:** Katman açıklamalarında çekirdek boyutu yerine kanal sayısına "kernel size" denmesi (örn. "64x64x64 kernel") ve optimizör açıklamasında SGD için ikinci momentumdan bahsedilmesi gibi editoryal dikkatsizlikler mevcuttur.
  3. **Çoklu Seans Belirsizliği:** ADNI'daki 1.426 hastaya karşılık 5.552 seansın eğitime nasıl dahil edildiği, seans düzeyinde sızıntı olup olmadığı netleştirilmemiştir.

---

## 12. Bizim Projeye Uyarlama
- **Bizim Kurulum:** ADNI1 1.5T başlangıç T1 sMRI, NC/MCI/AD, HD-BET $\rightarrow$ N4 $\rightarrow$ z-score $\rightarrow$ MNI152 afin $\rightarrow$ $128^3$, RID düzeyinde 5-kat CV, birincil görev AD-NC.
- **Neyi Aynen Alıyoruz / Esinleniyoruz?**
  - **3D CBAM / DAM Mekanizması:** Görkem'in P07 implementasyonundaki Self-Attention mekanizmasına ek olarak, rezidüel bloklar arasına eklenebilecek en pratik dikkat modülü CBAM/DAM'dır. Projemizde dikkat mekanizmaları karşılaştırmasında alternatif bir blok olarak değerlendirilebilir.
  - **OASIS-1 Köprü Doğrulaması:** Biz de ADNI onayımız gelene kadar OASIS-1 veri setini köprü olarak kullandığımız için, Hoang'ın OASIS-1 üzerindeki %83,4'lük dış test başarımı projemiz için doğrudan kıyaslama kriteridir.
- **Neyi Değiştiriyoruz?**
  - Çoklu seanslar yerine danışmanımızın şartı uyarınca yalnızca denek başına tek başlangıç taraması (baseline scan) kullanılacaktır.
  - Girdi boyutu $128 \times 128 \times 128$ olarak standartlaştırılacaktır.
- **Tahminî VRAM / Süre:** 3D-DAM modülleri parametre olarak çok hafiftir (yalnızca iki adet $1\times1\times1$ veya küçük MLP); batch size 4 ile $128^3$ boyutta yaklaşık 3,2 GB VRAM gerektirir. T4 GPU'da eğitim son derece hızlıdır.
- **Zorluk Derecesi:** **2 / 5 (Kolay).** PyTorch'ta 3D CBAM yazımı standart ve temizdir.

---

## 13. Opus Doğrulama
_(Bu bölüm bağımsız denetçi / hakem gözüyle doldurulmuştur.)_
- **Sonuç:** **ÇELİŞKİ VAR** (Özet metadatası ile makale içi tablolar ve terminoloji arasında uyumsuzluklar belgelenmiştir).
- **Kontrol Edilen Sayılar ve Kaynakları:**
  1. *ADNI Denek ve Seans Sayıları:* 403 AD (1.241 seans), 653 CN (2.564 seans), 165 pMCI (825 seans), 205 sMCI (922 seans); Toplam: 1.426 denek, 5.552 seans $\rightarrow$ Tablo 1 (Doğrulandı).
  2. *Harici Test Setleri Boyutları:* AIBL ($N=526$: 77 AD, 449 CN), OASIS-1 ($N=416$: 100 AD, 316 CN) $\rightarrow$ Tablo 3 (Doğrulandı).
  3. *ADNI Test Seti Başarımları:* AD vs. CN Acc %98,18 ± %0,42, Sen %96,73 ± %1,08, Spec %98,97 ± %0,51; pMCI vs. sMCI Acc %91,78 ± %0,63, Sen %95,06 ± %1,11, Spec %88,62 ± %1,15 $\rightarrow$ Tablo 2 (Doğrulandı).
  4. *Harici Test Başarımları (Deney 1):* AIBL Acc %86,3 (özette %86,37), Sen %80,2, Spec %87,1; OASIS-1 Acc %83,4 (özette %83,42), Sen %85,8, Spec %82,6 $\rightarrow$ Tablo 4 ve Özet (Doğrulandı).
  5. *Tersine Deney Başarımı (Deney 2):* AIBL+OASIS eğitim $\rightarrow$ ADNI test: Acc %85,4, Sen %80,1, Spec %89,5 $\rightarrow$ Tablo 4 (Doğrulandı).
  6. *Eğitim Parametreleri:* Batch size 16, epoch 200, lr = $10^{-7}$, weight decay = $10^{-6}$ $\rightarrow$ §2.4 (Doğrulandı).
- **Tespit Edilen Çelişkiler ve Düzeltmeler:**
  1. *Özet Metadata vs. Makale Metni Çelişkisi:* arXiv web sayfasındaki HTML özette "accuracy of 91.94% for MCI progression and 96.30% for Alzheimer's disease" yazarken; indirilen PDF tam metninde (Sayfa 1 Özet ve Tablo 2) AD için **%98,18**, MCI ilerlemesi için **%91,78** yazmaktadır. Bu durum yazarın v1 yüklemesi sırasında eski taslak özetini metadatada bırakmasından kaynaklanmaktadır. Raporumuzda PDF içerisindeki resmî Tablo 2 esas alınmıştır.
  2. *Terminoloji / Mimari Çelişkisi:* Bölüm 2.3'te rezidüel bloklar anlatılırken "kernel sizes of 16x16x16, 32x32x32 and 64x64x64" ifadeleri kullanılmıştır. 3B CNN'lerde $64^3$ çekirdek boyutu fiziksel ve boyutsal olarak imkansızdır; yazarların kanal/filtre sayısı yerine sehven "kernel size" yazdığı anlaşılmaktadır.
  3. *Optimizör Çelişkisi:* Bölüm 2.4'te "SGD optimizer with a first momentum of 0.9 and the second momentum of 0.999" denilmiştir. İkinci momentum ($\beta_2$) SGD'de bulunmaz, Adam optimizörüne aittir.
- **Doğrulanamayanlar:** Ağın katman bazlı kesin parametre sayısı ve nihai girdi tensör çözünürlüğü metinde rakamla verilmemiştir.
- **Güven:** **ORTA - YÜKSEK** (Sonuçlar ve metodoloji net olmakla birlikte yazar yazım dikkatsizlikleri belgelenmiştir).

---

## 14. Kaynaklar
- **arXiv Sayfası:** https://arxiv.org/abs/2310.12574
- **PDF Tam Metin:** https://arxiv.org/pdf/2310.12574.pdf
- **Clinica Platformu:** Routier et al. 2021, *Frontiers in Neuroinformatics* ([Clinica Web](https://www.clinica.run))
- **CBAM Referansı:** Woo et al. 2018, *ECCV 2018*, [arXiv:1807.06521](https://arxiv.org/abs/1807.06521)
- **Wen 2020 Sızıntı Rehberi:** Wen et al. 2020, *Medical Image Analysis*, 63:101694.
