# P12 — Solano-Rojas 2021 / 2020 — Düşük maliyetli 3B DenseNet-121

> **Durum:** ☐ okunmadı · ☐ AI özeti hazır · ☑ Opus doğrulandı · ☐ insan okudu · ☑ implemente edildi
> **Sorumlu:** Ertuğrul Kabaoğlu · **Grup:** C · **Tam metin (ücretsiz):** https://pmc.ncbi.nlm.nih.gov/articles/PMC7313295/ (ANNPR 2020 / LNCS 12294) · **Genişletilmiş sürüm:** Sensors 2021 (MDPI) · **Kod:** Makale kod vermiyor $\rightarrow$ MONAI `DenseNet121(spatial_dims=3)` (Apache-2.0)

---

## 1. Künye
- **Yazarlar:** Bryan Solano-Rojas, Roberto Villalón-Fonseca.
- **Yıl / Başlık:** 2020 — *Alzheimer’s Disease Early Detection Using a Low Cost Three-Dimensional Densenet-121 Architecture*.
- **Yayın Yeri:** *Artificial Neural Networks in Pattern Recognition (ANNPR 2020)*, Lecture Notes in Computer Science (LNCS), Cilt 12294, Sayfalar 3–15, Springer, 2020. Genişletilmiş çalışma: *Sensors* 21(4): 1300, 2021.
- **DOI / PMC:** [10.1007/978-3-030-58309-5_1](https://doi.org/10.1007/978-3-030-58309-5_1) · PubMed Central: [PMC7313295](https://pmc.ncbi.nlm.nih.gov/articles/PMC7313295/).
- **Atıf Sayısı:** ~45 (Google Scholar, 2026 itibarıyla).

---

## 2. Tek paragraf özet
Solano-Rojas ve Villalón-Fonseca, gelişmekte olan ülkelerdeki araştırmacıların yüksek maliyetli GPU donanımlarına erişim kısıtını aşmak amacıyla, tamamen ücretsiz bulut bilişim kaynakları (Google Colaboratory) üzerinde çalışan 3 boyutlu bir DenseNet-121 mimarisi geliştirmiştir. ADNI veri tabanından indirilen 5.556 adet 3B T1-ağırlıklı MR taraması $1 \text{ mm}^3$ uzamsal çözünürlüğe ve $256 \times 256 \times 256$ küboid hacim boyutuna getirilmiş; sübjektif ve gürültülü olduğu tespit edilen "Belirgin Bellek Kaygısı" (Significant Memory Concern, SMC) sınıfı elenerek toplam 5.370 tarama ile 5 sınıflı (CN, EMCI, MCI, LMCI, AD) bir sınıflandırma problemi tanımlanmıştır. Model, SGD optimizer, dropout ($0.7$) ve batch boyutu 5 ile Colab'ın ücretsiz GPU oturum süresi sınırlarında (80–110 epoch) eğitilmiştir. Yazarlar, 5 sınıflı görevde mikro-ortalama $\%84$ doğruluk, $\%81$ duyarlılık, $\%84$ özgüllük ve $\%92$ AUROC bildirmektedir (özette $\%87$ doğruluk, $\%87$ duyarlılık, $\%88$ özgüllük). Ancak eğitim/test ayrımı denek (RID) bazında değil, tüm taramalar üzerinden rastgele $\%75 / \%25$ oranında yapıldığı için aynı hastanın farklı vizitlerdeki taramaları her iki kümeye de dağılmış ve ciddi veri sızıntısı (data leakage) oluşmuştur; bu durum elde edilen yüksek 5 sınıflı metriklerin şişkin olduğunu göstermektedir.

---

## 3. Problem ve katkı
- **Çözmeye çalıştıkları problem:** 3B derin evrişimli sinir ağlarının eğitilmesinin çok pahalı donanım ve GPU sunucuları gerektirmesi, bu nedenle gelişmekte olan ülkelerde klinik karar destek sistemlerinin geliştirilmesinin önündeki ekonomik engel.
- **İddia ettikleri katkılar (madde madde):**
  1. **Düşük maliyetli 3B DenseNet-121:** Pahalı yerel sunucular yerine Google Colaboratory'nin ücretsiz GPU katmanında 3B DenseNet-121 mimarisini başarıyla koşturabilmek (§1, §3).
  2. **Gürültülü SMC sınıfının tespiti ve elenmesi:** 6 sınıflı kurulumda SMC sınıfının yüksek hata ürettiğini deneysel olarak gösterip bu sınıfı veri setinden çıkararak model performansını artırmak (§3, Fig. 1).
  3. **Çok sınıflı (5 sınıf) evreleme:** İkili sınıflandırma (AD-NC) yerine hastalığın 5 farklı evresini (CN, EMCI, MCI, LMCI, AD) aynı anda sınıflandırmak (Tablo 1).

---

## 4. Veri seti ve bölme
- **Kaynak:** ADNI (Alzheimer's Disease Neuroimaging Initiative).
- **Tarama Sayısı:** Başlangıçta $5.556$ adet 3B T1 MRI taraması; SMC sınıfına ait 186 tarama elendikten sonra net **$5.370$ adet 3B MRI taraması** (§3).
- **Sınıflar (5 sınıf):**
  1. **CN (Cognitive Normal):** Bilişsel normal kontrol.
  2. **EMCI (Early Mild Cognitive Impairment):** Erken hafif bilişsel bozukluk.
  3. **MCI (Mild Cognitive Impairment):** Genel hafif bilişsel bozukluk.
  4. **LMCI (Late Mild Cognitive Impairment):** Geç hafif bilişsel bozukluk.
  5. **AD (Alzheimer's Disease):** Alzheimer demansı.
  *(Elenen 6. sınıf: SMC - Significant Memory Concern)*.
- **Bölme Yöntemi:** Tüm tarama havuzu üzerinden rastgele $\%75$ eğitim ($n = 4.027$ tarama) ve $\%25$ test ($n = 1.343$ tarama) olarak ikiye ayrılmıştır (Tablo 1).
- **Sızıntı riski değerlendirmesi:** **ÇOK YÜKSEK (Kritik Sızıntı / Data Leakage).**
  - **Gerekçe:** Bölme işlemi denek (RID/hasta) düzeyinde değil, tarama düzeyinde yapılmıştır. ADNI'de hastaların 6., 12., 24. aylarda tekrarlanan boylamsal (longitudinal) taramaları bulunmaktadır. Rastgele $\%75 / \%25$ tarama bölmesinde aynı hastanın bir taraması eğitimde, diğer taraması testte yer almıştır. Yagis vd. 2021 ve Wen vd. 2020'nin kanıtladığı gibi, hasta düzeyinde olmayan bölmeler test doğruluğunu $25–45$ puan yapay olarak şişirir. Bu nedenle bildirilen $\%84–87$'lik 5 sınıflı başarı genellenebilir değildir.

---

## 5. Ön işleme
1. **Yeniden Örnekleme (Resampling):** Tüm hacimlerin voksel aralığı enterpolasyonla $1.0 \times 1.0 \times 1.0 \text{ mm}^3$ izotropik boyuta dönüştürülmüştür (§3).
2. **Küboid Boyutlandırma:** Dilim sayısı enterpolasyonla 256'ya ayarlanmış ve her tarama $256 \times 256 \times 256$ boyutunda 3B küboid haline getirilmiştir.
3. **Kanal:** Tek kanallı (monochromatic, gri tonlama) tensör yapısına dönüştürülmüştür.
4. **Kafatası soyma / Kayıtlama:** Makalede kafatası soyma veya MNI kayıtlama açıkça belirtilmemiştir; ADNI önceden işlenmiş hacimleri kullanılmıştır.

---

## 6. Mimari
Standart 3B DenseNet-121 omurgası:
- **Girdi Boyutu:** $1 \times 256 \times 256 \times 256$ (bizim protokole uyarlamada $1 \times 128 \times 128 \times 128$).
- **Kök Katman (Stem):** Conv3D($1 \rightarrow 64$, çekirdek $7\times7\times7$, stride 2, padding 3) + BatchNorm3D + ReLU + MaxPool3D($3\times3\times3$, stride 2).
- **Yoğun Bloklar (DenseBlocks 1–4):**
  - DenseBlock 1: 6 yoğun katman ($1\times1\times1$ Conv3D $\rightarrow 3\times3\times3$ Conv3D, büyüme oranı $k=32$).
  - Geçiş Katmanı 1 (Transition): Conv3D($1\times1\times1$) + AvgPool3D($2\times2\times2$, stride 2).
  - DenseBlock 2: 12 yoğun katman ($k=32$).
  - Geçiş Katmanı 2: Conv3D($1\times1\times1$) + AvgPool3D($2\times2\times2$, stride 2).
  - DenseBlock 3: 24 yoğun katman ($k=32$).
  - Geçiş Katmanı 3: Conv3D($1\times1\times1$) + AvgPool3D($2\times2\times2$, stride 2).
  - DenseBlock 4: 16 yoğun katman ($k=32$).
- **Sınıflandırma Kafası:** AdaptiveAvgPool3D($1\times1\times1$) + Dropout($0.7$) + Linear(1024 $\rightarrow 5$ sınıf / ikili görevde 2 sınıf).
- **Toplam Parametre Sayısı:** ~11.2 Milyon.

---

## 7. Eğitim ayarları
- **Platform:** Google Colaboratory (ücretsiz GPU).
- **Optimizer:** Stokastik Gradyan İnişi (SGD) + Momentum ($0.9$).
- **Öğrenme Hızı:** Başlangıçta $\eta = 0.1$; 60. epoch'ta $0.1$ ile çarpılarak $\eta = 0.01$'e düşürülmüştür.
- **Batch Boyutu:** 5 (GPU bellek sınırları nedeniyle).
- **Epoch Sayısı:** 80–110 epoch (Google Colab kesinti sınırlarına kadar).
- **Kayıp Fonksiyonu:** Cross-Entropy Loss.
- **Düzenlileştirme:** Dropout oranı $0.7$ (aşırı uyumu engellemek için yüksek tutulmuştur).
- **Veri Artırma:** Eğitim süresini uzatmamak için veri artırma (data augmentation) uygulanmamıştır (§3).

---

## 8. Sonuçlar

### 5 Sınıflı Model Performansı (Makale Tablo 1 & §3 Metin)
| Görev | Metrik Türü | Bildirilen Değer (Özet) | Bildirilen Değer (Tablo 1 / Metin) | Test Seti | Not |
|---|---|---|---|---|---|
| 5 Sınıf (CN/EMCI/MCI/LMCI/AD) | Doğruluk (Accuracy) | %87 | **%84** | ADNI rastgele %25 | Mikro-ortalama |
| 5 Sınıf | Duyarlılık (Sensitivity) | %87 | **%81** | ADNI rastgele %25 | Mikro-ortalama |
| 5 Sınıf | Özgüllük (Specificity) | %88 | **%84** | ADNI rastgele %25 | Mikro-ortalama |
| 5 Sınıf | AUROC | %92 | **%92** | ADNI rastgele %25 | Mikro-ortalama |

- **Sınıf Bazlı Bulgular:** Yazarlar en zayıf sonuçların Alzheimer (AD) özgüllüğü ile Geç Hafif Bilişsel Bozukluk (LMCI) duyarlılığında çıktığını; LMCI olgularının büyük oranda AD olarak sınıflandırıldığını (kötümser/pessimistic sınıflandırma) belirtmektedir (§3).

---

## 9. Açıklanabilirlik / ek analiz
- Makalede Grad-CAM, LRP veya dikkat haritası görselleştirmesi yapılmamıştır (— makalede yok). Yalnızca konfüzyon matrisi analizi sunulmuştur (Fig. 1).
- Projemizde bu eksiklik MONAI `GradCAM` entegrasyonu ile giderilecektir.

---

## 10. Kod ve tekrarlanabilirlik
- **Depo:** Makalede açık bir GitHub linki verilmemiştir (— kod yok).
- **Yeniden Üretim Temeli:** MONAI kütüphanesinin standart `monai.networks.nets.DenseNet121(spatial_dims=3, in_channels=1, out_channels=k, dropout_prob=0.7)` sınıfı mimariyi birebir karşılamaktadır.
- **Lisans:** MONAI Apache-2.0 lisanslıdır; yasal uyum tamdır.

---

## 11. Güçlü ve zayıf yönler
- **Güçlü Yönler:**
  1. DenseNet mimarisinin yoğun bağlantı yapısı (feature reuse) sayesinde gradyan kaybolması sorunu yaşanmaz.
  2. Düşük kaynaklı ortamlarda (Google Colab) çalışabilirlik hedeflenmiştir.
  3. SMC sınıfının gürültü kaynağı olduğunu deneysel olarak göstermiştir.
- **Zayıf Yönler:**
  1. **Ağır veri sızıntısı:** Denek bazında bölünmediği için sonuçlar gerçek klinik performansı yansıtmaz.
  2. Çelişkili metrikler: Özet bölümündeki sayılar (%87 acc, %87 sens, %88 spec) ile metindeki nihai sayılar (%84 acc, %81 sens, %84 spec) birbiriyle uyuşmamaktadır.
  3. Açıklanabilirlik / XAI analizi bulunmamaktadır.
  4. Açık kaynak kod paylaşılmamıştır.

---

## 12. Bizim projeye uyarlama
- **Rol:** 6. implementasyon modelimiz (`uygulama/ertugrul_P12_densenet/`).
- **Uyarlama Stratejisi:**
  - MONAI `DenseNet121` ve daha düşük parametreli bir `TinyDenseNet` varyantı tanımlanır.
  - Makaledeki hatalı tarama bazlı bölme kesinlikle reddedilir; **denek (RID) düzeyinde 5-kat çapraz doğrulama** uygulanır.
  - Giriş boyutu projemizin ortak $128 \times 128 \times 128$ tensör standardına çekilir.
  - Birincil görevde ikili (AD vs NC), ikincil görevde 3 sınıflı (NC/MCI/AD) kurulumda test edilir.
- **Beklenen Zorluk:** 2/5 (MONAI'de 3B DenseNet121 hazırdır; VRAM optimizasyonu gerekir).
- **Tahminî VRAM / Süre:** 128³ boyutta batch 2-4 ile DenseNet121 ~4-6 GB VRAM tüketir (RTX 4060 8 GB için uygundur).

---

## 13. Opus doğrulama
- **Sonuç:** **ÇELİŞKİ VAR**
- **Tespit edilen çelişkiler ve düzeltmeler:**
  1. **Özet vs. Metin Metrik Çelişkisi:** Makalenin Abstract bölümünde *"87% accuracy, 87% sensitivity (micro-average), 88% specificity (micro-average), and 92% AUROC"* iddia edilirken; metin içi §3 "Around Metrics of the obtained DNN at 110 epochs" bölümünde açıkça *"the final figures of 84% accuracy, 84% specificity (micro) and 81% sensitivity (micro) are acceptable"* denmektedir. Özet bölümünde erken epoch'taki en iyi anlık değer verilmiş, nihai model metrikleri gizlenmiştir.
  2. **Veri Kümesi ve Tarama Sayısı:** Başlangıçta 5.556 MRI taraması indirilmiş; 186 SMC taraması çıkarılınca geriye 5.370 MRI kalmıştır. Denek sayısı belirtilmemiştir.
  3. **Veri Sızıntısı:** Bölme denek bazında değil, tarama bazında rastgele yapılmıştır; bu durum makalenin bilimsel güvenilirliğini zayıflatmaktadır.
- **Güven düzeyi:** Yüksek (Tam metin PMC7313295 XML incelenerek çelişki kanıtlanmıştır).

---

## 14. Kaynaklar
1. Solano-Rojas B., Villalón-Fonseca R., *ANNPR 2020*, LNCS 12294: https://pmc.ncbi.nlm.nih.gov/articles/PMC7313295/
2. MONAI DenseNet Dokümantasyonu: https://docs.monai.io/en/stable/networks.html#densenet121
