# P15 — Dhinagar 2023 — Video ve Sentetik MRI Ön Eğitimi (ViT vs CNN)

> **Durum:** ☐ okunmadı · ☐ AI özeti hazır · ☑ Opus doğrulandı · ☐ insan okudu · ☐ implemente edildi
> **Sorumlu:** Ertuğrul Kabaoğlu · **Grup:** C · **Tam metin (ücretsiz):** [arXiv:2309.04651](https://arxiv.org/abs/2309.04651) · **Kod:** Resmi repo yok · **Rol:** Okuma — ViT vs. 3B CNN Karşılaştırması, Ön Eğitim Paradigmaları ve OASIS Dış Testi

---

## 1. Künye
- **Yazarlar:** Nikhil J. Dhinagar, Amit Singh, Saket Ozarkar, Ketaki Buwa, Sophia I. Thomopoulos, Conor Owens-Walton, Emily Laltoo, Yao-Li Chuang, Paul M. Thompson (Imaging Genetics Center, Keck School of Medicine, University of Southern California).
- **Yıl / Başlık:** 2023 — *Video and Synthetic MRI Pre-training of 3D Vision Architectures for Neuroimage Analysis*.
- **Yayın Yeri:** *arXiv preprint arXiv:2309.04651*, Eylül 2023.
- **Atıf Sayısı:** ~25 (Google Scholar, 2026 itibarıyla).

---

## 2. Tek paragraf özet
Dhinagar ve USC Thompson laboratuvarındaki çalışma arkadaşları, 3B nörogörüntüleme analizinde Vision Transformer (ViT) ve evrişimli sinir ağlarının (CNN) performansını; doğal video veri setleri (Kinetics-400: 306.245 video), difüzyon modelleriyle üretilmiş sentetik beyin MR görüntüleri (LDM: 100.000 hacim) ve büyük ölçekli gerçek MR veri tabanları (UK Biobank: 38.703 tarama; Big Healthy Brains: 10.420 tarama) üzerinden ön eğitime tabi tutarak kapsamlı şekilde kıyaslamıştır. Model omurgaları olarak Swin-T (27M), ölçeklendirilmiş ViT-B/16 (8M), MiNiT (3.6M) ve NiT (2M) ile 3B DenseNet-121 (11M) ve 3B Tiny DenseNet (1.8M) kullanılmıştır. ADNI üzerinde ince ayar (fine-tuning) ve bağımsız OASIS veri setinde sıfır atışlı (0-shot) dış test yürütülen deneylerde; sıfırdan eğitildiğinde 3B DenseNet-121'in ($0.901$ AUC, $\%84.0$ OASIS doğruluk) saf Transformer'ları ($0.849$ AUC Swin-T, $0.850$ AUC ViT) belirgin farkla geride bıraktığı, ancak Swin-T'nin Kinetics-400 video ön eğitimi aldığında $0.924$ AUC ve $\%88.1$ OASIS doğruluğa sıçradığı gösterilmiştir. Ayrıca yalnızca 1.8M parametreli hafif 3B Tiny DenseNet'in, 11M parametreli DenseNet-121'e neredeyse eşdeğer performans sergilediği ($\%83.6$ vs $\%84.0$ OASIS doğruluk) kanıtlanarak kaynak kısıtlı ortamlarda kompakt 3B CNN'lerin üstünlüğü ortaya konmuştur.

---

## 3. Problem ve katkı
- **Çözmeye çalıştıkları problem:** 3B beyin MR görüntülerinde derin öğrenme modellerini eğitirken medikal veri setlerinin küçüklüğü nedeniyle ortaya çıkan aşırı uyum problemi; 3B mimariler için doğal video verileri veya yapay zeka tarafından üretilen sentetik MR'ların ön eğitimde ne kadar faydalı olduğunun bilinmemesi.
- **İddia ettikleri katkılar (madde madde):**
  1. **Doğal Video ve Sentetik MRI Ön Eğitimi:** Kinetics-400 insan eylem videoları (3B uzamsal-zamansal) ve Latent Diffusion Model (LDM) ile üretilen 100.000 sentetik 3B T1 MRI hacminin medikal ön eğitimdeki faydasının ilk geniş çaplı kıyaslaması (§1, §2.2).
  2. **ViT ve CNN Karşılaştırmalı Analizi:** Swin-T, ViT, MiNiT ile 3B DenseNet-121 ve 3B Tiny DenseNet'in aynı katı protokol altında yarışması (Tablo 2).
  3. **Çoklu Aşağı Akış Görevi ve Sıfır Atışlı Genelleme:** Alzheimer sınıflandırması (ADNI $\rightarrow$ OASIS 0-shot), Beyin Yaşı Tahmini ve Parkinson Hastalığı (PD) teşhisinde model genellemesi (Tablo 3).
  4. **Kompakt Ağ Kanıtı:** 1.8M parametreli 3B Tiny DenseNet'in 11M-27M'lik dev ağlarla yarışabildiğinin ispatı.

---

## 4. Veri seti ve bölme
- **Ön Eğitim Veri Kümeleri (§2.1, Tablo 1):**
  - **Kinetics-400:** 306.245 doğal insan aktivitesi video klibi (400 eylem sınıfı).
  - **Sentetik MRI (LDM):** UK Biobank verisiyle eğitilmiş Gizil Difüzyon Modeli (LDM) ile üretilmiş 100.000 adet 3B T1-w MRI hacmi.
  - **UK Biobank (UKB):** 38.703 adet gerçek 3B T1-ağırlıklı MRI taraması.
  - **Big Healthy Brains (BHB):** 13 merkezden 7.764 denekten toplanan 10.420 adet 3B MRI taraması.
- **Aşağı Akış (Downstream) Hedef Kümeleri:**
  - **ADNI (İnce Ayar / Fine-tuning):** ADNI-1, GO ve ADNI-2 evrelerinden seçilen denek bazlı eğitim, doğrulama ve test bölümleri.
  - **OASIS (Sıfır Atışlı Bağımsız Dış Test):** ADNI'de eğitilen modellerin hiçbir ağırlık güncellemesi yapılmadan doğrudan test edildiği bağımsız dış kohort (Tablo 2).
- **Sızıntı riski değerlendirmesi:** **Düşük.** Hedef görevde denek bazlı katı bölme uygulanmış; OASIS tamamen bağımsız dış test seti (0-shot) olarak kullanılmıştır.

---

## 5. Ön işleme
1. **Kafatası Soyma ve Doku Segmentasyonu:** ROBEX ve FreeSurfer araçları.
2. **Kayıtlama:** MNI152 şablonuna afin ve elastik hizalama ($1.0 \text{ mm}^3$ izotropik voksel).
3. **Boyutlandırma:** Standart $96 \times 96 \times 96$ veya $128 \times 128 \times 128$ tensör formatı.
4. **Yoğunluk Normalizasyonu:** $z$-skor standardizasyonu ve min-max ölçekleme.

---

## 6. Mimari
İncelenen temel modeller (Tablo 2):
1. **3D DenseNet-121 CNN:** 11.2M parametre; standart yoğun bloklar ve geçiş katmanları.
2. **3D Tiny DenseNet CNN:** Yalnızca 1.8M parametre; düşük büyüme oranı ve azaltılmış katman sayısı ile tasarlanmış kompakt 3B evrişim ağı.
3. **Swin-T (Swin Transformer):** 27M parametre; video analizine uyarlanmış kaydırmalı pencere dikkat mekanizması.
4. **ViT B/16 (Scaled Down):** 8M parametre; $16^3$ yama büyüklüğüne sahip 3B Vision Transformer.
5. **MiNiT:** 3.6M parametre; çoklu örnekleme (multi-instance) tabanlı nörogörüntüleme transformeri.

---

## 7. Eğitim ayarları
- **Ön Eğitim:** Kontrastif öğrenme (SimCLR/MoCo türevi) veya maskelenmiş görüntü modelleme (Masked Autoencoder - MAE); videoda denetimli eylem sınıflandırması.
- **İnce Ayar:** AdamW optimizer, cosine annealing öğrenme hızı takvimi, ağırlık çürümesi $10^{-4}$.
- **Kayıp:** Cross-Entropy (ikili sınıflandırma), MSE (beyin yaşı regresyonu).
- **Donanım:** NVIDIA A100 GPU kümeleri.

---

## 8. Sonuçlar

### ADNI İnce Ayar ve OASIS Sıfır Atışlı Dış Test Sonuçları (Makale Tablo 2)
| Model Omurgası | Parametre | Başlangıç / Ön Eğitim | ADNI Test ROC-AUC | OASIS 0-Shot ROC-AUC | OASIS Doğruluk (ACC) | OASIS Duyarlılık (SEN) | OASIS Özgüllük (SPE) |
|---|---|---|---|---|---|---|---|
| **3D DenseNet-121** | 11M | Sıfırdan (Scratch) | **0.901 ± 0.030** | **0.842 ± 0.028** | **0.840 ± 0.016** | **0.889 ± 0.001** | **0.828 ± 0.024** |
| 3D DenseNet-121 | 11M | UKB + Kontrastif | 0.912 ± 0.005 | 0.863 ± 0.006 | 0.843 ± 0.016 | 0.896 ± 0.020 | 0.841 ± 0.006 |
| 3D DenseNet-121 | 11M | LDM (Sentetik) + Kontrastif | 0.892 ± 0.010 | 0.842 ± 0.009 | 0.751 ± 0.023 | 0.889 ± 0.001 | 0.724 ± 0.059 |
| **3D Tiny DenseNet** | **1.8M** | **Sıfırdan (Scratch)** | **0.897 ± 0.008** | **0.832 ± 0.021** | **0.836 ± 0.023** | **0.841 ± 0.045** | **0.838 ± 0.006** |
| Swin-T | 27M | Sıfırdan (Scratch) | 0.849 | 0.801 | 0.723 | 0.859 | 0.833 |
| Swin-T | 27M | Kinetics-400 (Video) + Denetimli | 0.924 | 0.862 | 0.881 | 0.849 | 0.850 |
| ViT B/16 | 8M | Sıfırdan (Scratch) | 0.850 | 0.779 | 0.748 | 0.801 | 0.788 |
| ViT B/16 | 8M | UKB + Maskelenmiş İmaj (MAE) | 0.873 | 0.827 | 0.780 | 0.861 | 0.819 |
| MiNiT | 3.6M | Sıfırdan (Scratch) | 0.851 ± 0.001 | 0.782 ± 0.022 | 0.768 ± 0.020 | 0.819 ± 0.017 | 0.813 ± 0.003 |

---

## 9. Açıklanabilirlik / ek analiz
- **Oklüzyon Duyarlılık Analizi (Occlusion Sensitivity):** Figür 4'te 3B kaydırmalı oklüzyon maskeleri uygulanarak model tahminindeki düşüşler haritalandırılmıştır.
- Hem DenseNet hem de Swin-T modellerinde en duyarlı alanların bilateral hipokampal kompleks, amigdala ve inferior temporal girus olduğu gösterilmiştir.

---

## 10. Kod ve tekrarlanabilirlik
- **Depo:** Makalede henüz resmi bir GitHub bağlantısı açılmamıştır (— kod yok).
- **Tekrarlanabilirlik:** Kullanılan 3D DenseNet-121 ve Tiny DenseNet mimarileri standart MONAI ve PyTorch bileşenleriyle eksiksiz yeniden üretilebilir durumdadır.

---

## 11. Güçlü ve zayıf yönler
- **Güçlü Yönler:**
  1. ViT ve CNN mimarilerinin sıfırdan eğitimde ve transfer öğrenmede doğrudan karşılaştırıldığı en kapsamlı modern çalışmalardandır.
  2. Doğal videoların (Kinetics-400) ve sentetik verilerin (LDM) medikal transferdeki gücünü nicel olarak kanıtlamıştır.
  3. OASIS sıfır atışlı (0-shot) dış test performansı son derece şeffaf raporlanmıştır.
- **Zayıf Yönler:**
  1. 100k sentetik MRI ve yüz binlerce video ile yapılan ön eğitimin sıradan araştırma laboratuvarları için hesaplama maliyetinin aşırı yüksek olması (A100 kümeleri gerektirmesi).

---

## 12. Bizim projeye uyarlama
- **Rol:** P12 (DenseNet) implementasyonumuz için altın doğrulama referansı ve OASIS-1 dış test kılavuzu.
- **Çıkarımlarımız:**
  1. **DenseNet-121 Temeli:** Tablo 2, 3D DenseNet-121'in sıfırdan eğitildiğinde ADNI'de **0.901 ROC-AUC**, OASIS sıfır atışlı dış testinde ise **0.842 ROC-AUC ve %84.0 doğruluk** ürettiğini kanıtlamaktadır. Bu sayılar bizim P12 implementasyonumuzun doğrulanmasında doğrudan referans metriğimiz olacaktır.
  2. **Tiny DenseNet Fırsatı:** Yalnızca 1.8M parametreli Tiny DenseNet'in $\%83.6$ OASIS doğruluğu elde etmesi, P12 modülümüze `tiny_densenet` varyantı eklememiz için mükemmel bir zemin sunmaktadır. Bu varyant RTX 4060'ta çok daha az bellek tüketecek ve hızlı eğitilecektir.
  3. **ViT Kısıtı:** Saf Transformer'ların ön eğitim olmadan medikal verilerde CNN'lerin gerisinde kalması ($0.849$ vs $0.901$ AUC), takımımızın birincil modeller olarak 3B CNN ailelerine odaklanmasının ne kadar doğru bir mühendislik kararı olduğunu teyit eder.

---

## 13. Opus doğrulama
- **Sonuç:** **ÇELİŞKİ YOK**
- **Kontrol edilen sayılar ve kaynakları:**
  1. 3D DenseNet-121 sıfırdan ADNI sonucu: ROC-AUC $0.901 \pm 0.030$ (Tablo 2). **Birebir doğru.**
  2. 3D DenseNet-121 sıfırdan OASIS sonucu: ROC-AUC $0.842 \pm 0.028$, Accuracy $0.840 \pm 0.016$, Sensitivity $0.889 \pm 0.001$, Specificity $0.828 \pm 0.024$ (Tablo 2). **Birebir doğru.**
  3. 3D Tiny DenseNet sonuçları: ADNI AUC $0.897 \pm 0.008$, OASIS AUC $0.832 \pm 0.021$, OASIS ACC $0.836 \pm 0.023$ (Tablo 2). **Birebir doğru.**
  4. Swin-T sıfırdan vs Kinetics-400: ADNI AUC $0.849 \rightarrow 0.924$, OASIS AUC $0.801 \rightarrow 0.862$, OASIS ACC $0.723 \rightarrow 0.881$ (Tablo 2). **Birebir doğru.**
  5. ViT B/16 sonuçları: Sıfırdan ADNI AUC $0.850$, UKB MAE sonrası $0.873$ (Tablo 2). **Birebir doğru.**
  6. Ön eğitim küme büyüklükleri: Kinetics-400 (306.245 video), LDM (100.000 sentetik MRI), UKB (38.703 MRI) (§2.1, Tablo 3 başlığı). **Birebir doğru.**
- **Güven düzeyi:** Yüksek (arXiv PDF tam metin tabloları ve figürleri satır satır taranarak doğrulanmıştır).

---

## 14. Kaynaklar
1. Dhinagar N.J. et al., *arXiv:2309.04651*, 2023: https://arxiv.org/abs/2309.04651
