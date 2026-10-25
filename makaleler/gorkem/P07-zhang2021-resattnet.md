# P07 — Zhang 2021 — 3D ResAttNet (Artık Öz-Dikkat ve 3B Grad-CAM)

> **Durum:** ☐ okunmadı · ☑ AI özeti hazır · ☑ Opus doğrulandı (**ÇELİŞKİ YOK**, güven: yüksek) · ☐ insan okudu · ☐ implemente edildi
> **Sorumlu:** Ahmet Görkem Yavuz · **Grup:** B · **Tam metin (ücretsiz):** https://arxiv.org/abs/2008.04024 (v2, 20 Nisan 2021) · **Kod:** Resmî açık kod deposu yok $\rightarrow$ MONAI `resnet18/34(spatial_dims=3)` (Apache-2.0) + özel 3B öz-dikkat bloğu + `monai.visualize.GradCAM`
> **AI okuma kaynağı:** arXiv:2008.04024v2 tam metni (Bölüm I–V, Denklem 1–12, Tablo I–IV, Şekil 1–6). IEEE Journal of Biomedical and Health Informatics (J-BHI, 2021) yayını bibliyografik kayıtları.

> ⚠ **Nasıl okunmalı:** §2–§12 ilk okuma özetidir; §13 hakem denetimidir (§13.1–§13.5). Bu makale grubumuzun 2. implementasyon makalesidir; mimari sözleşmesi (`olustur(varyant='resatt18', ...)`) ve Grad-CAM ısı haritası üretimi §12.3'e göre kurulur.

---

## 1. Künye
- **Yazarlar:** Xin Zhang, Liangxiu Han, Wenyong Zhu, Liang Sun, Daoqiang Zhang
- **Yıl:** 2021 (arXiv v1: Ağustos 2020, v2: 20 Nisan 2021; IEEE JBHI 2021/2022)
- **Başlık:** *An Explainable 3D Residual Self-Attention Deep Neural Network For Joint Atrophy Localization and Alzheimer’s Disease Diagnosis using Structural MRI*
- **Yayın Yeri:** IEEE Journal of Biomedical and Health Informatics (IEEE J-BHI), Cilt 26, Sayı 11, ss. 5550–5561, 2022.
- **DOI / arXiv:** [arXiv:2008.04024](https://arxiv.org/abs/2008.04024) · [10.1109/JBHI.2021.3116087](https://doi.org/10.1109/JBHI.2021.3116087)
- **Atıf Sayısı:** ~95–130 (Google Scholar / IEEE Xplore, 2026 itibarıyla)
- **Kurumlar:** Manchester Metropolitan University (İngiltere) ve Nanjing University of Aeronautics and Astronautics (Çin)
- **Açık Kod:** Resmî depo yayımlanmamıştır. Açık bileşenlerden (MONAI ResNet omurgası + öz-dikkat bloğu + MONAI GradCAM) kurulacaktır.

---

## 2. Tek Paragraf Özet
Makale, 3B yapısal MRI (sMRI) verisinden Alzheimer hastalığı (AD) ve hafif bilişsel bozukluk dönüşümü (pMCI vs sMCI) teşhisini uçtan uca gerçekleştirmek ve karar mekanizmasını görsel olarak açıklamak amacıyla 3B Artık Öz-Dikkat Ağı (3D ResAttNet) mimarisini ve 3B Grad-CAM yöntemini sunar (§I, §III-A). Yerel evrişim pencerelerinin uzun menzilli mekânsal ilişkileri kaçırmasını engellemek için artık blokların çıkışına $1 \times 1 \times 1$ evrişimlerle ölçeklenen $Q, K, V$ projektörlü öz-dikkat (self-attention) mekanizması eklenmiş ve öğrenilebilir bir $\gamma$ parametresiyle ($y = x + r(x) + \gamma \cdot o(r(x))$) yerel-küresel özellik dengesi kurulmuştur (§III-C). ADNI-1 (835 tarama: 200 AD, 231 NC, 232 sMCI, 172 pMCI) veri setinde 5-kat çapraz doğrulamayla eğitilen 3D-ResAttNet34; AD vs NC görevinde **%91.3 doğruluk ve 0.984 AUC**, zorlu pMCI vs sMCI görevinde ise **%82.1 doğruluk ve 0.920 AUC** elde ederek düz 3D-ResNet ve 3D-VGGNet temel çizgilerini anlamlı biçimde geride bırakmıştır (§IV-D1, Tablo II). Bağımsız ADNI-2 (258 tarama) ve ADNI-3 (314 tarama) setlerinde sıfır-atış genelleme sınanmış ve %89.2–90.9 doğruluk korunmuştur (§IV-D2, Tablo III). 3B Grad-CAM ile 3. ve 4. evrişim bloklarından üretilen ısı haritalarının hipokampus, lateral ventriküller ve serebral korteksteki hacim kaybıyla örtüştüğü gösterilmiştir (§IV-D1, Şekil 6). Çalışmanın güçlü yönü artık blokla öz-dikkati zarif bir formülasyonla birleştirmesi ve çok merkezli dış test sunmasıdır; zayıf yönü ise resmî kodunun bulunmaması ve 5-kat CV bölmesinde denek kimliklerinin (RID) sızıntısız ayrıldığının metinde açıkça belgelenmemesidir (§IV-C1).

---

## 3. Problem ve Katkı
- **Problem:**
  1. *Yerel Alıcı Alan Kısıtı:* Standart 3B CNN'ler küçük çekirdeklerle ($3 \times 3 \times 3$) yerel dokuları yakalar; ancak beynin uzak anatomik bölgeleri arasındaki (örneğin iki taraflı hipokampüs küçülmesi ile ventrikül genişlemesi arasındaki) korelasyonu yakalamak için çok sayıda katman gerekir, bu da gradyan kaybolması ve bellek patlamasına yol açar (§I, §III-A).
  2. *Bilgi Kaybı:* Standart dikkat mekanizmaları kritik bölgelere odaklanırken küresel bağlamı zayıflatabilir (§III-C).
  3. *Açıklanabilirlik Eksikliği:* 3B medikal kararların klinisyene görsel gerekçeyle sunulamaması güven sorununa yol açar (§I, §II-B).
- **Katkı 1 (3B ResAttNet Bloğu):** Artık öğrenme (ResNet) ile öz-dikkat (Self-Attention) modülü matematiksel olarak entegre edilmiştir. Artık bağlantı küresel anatomik bütünlüğü korurken, öz-dikkat katmanı $C \times N$ uzayında uzun menzilli voksel bağımlılıklarını öğrenir (§III-C).
- **Katkı 2 (Hafif Kök Tasarımı):** Hesaplama maliyetini düşürmek amacıyla standart ResNet'lerdeki hantal $7 \times 7 \times 7$ kök evrişimi yerine peş peşe üç adet $3 \times 3 \times 3$ evrişim katmanı kullanılmıştır (§III-B, §IV-C1).
- **Katkı 3 (3B Grad-CAM Açıklaması):** Gradyan ağırlıklı sınıf aktivasyon haritalama yöntemi 3B tensörlere uyarlanmış; 4. katmanın kaba ($6 \times 7 \times 6$) haritası ile 3. katmanın yüksek çözünürlüklü ($46 \times 55 \times 46$) haritası karşılaştırılarak atrofi yerelleştirmesi yapılmıştır (§III-D, §IV-D1).
- **Katkı 4 (pMCI-sMCI Başarımı ve Çapraz Kohort Testi):** Yalnızca AD-NC değil, 36 ay içinde AD'ye dönüşen (pMCI) ve stabil kalan (sMCI) denekler arasında %82.1 doğruluk sağlanmış; ADNI-1, ADNI-2 (3T) ve ADNI-3 (3T) arasında çift yönlü çapraz test gerçekleştirilmiştir (§IV-D2).

---

## 4. Veri Seti ve Bölme
- **Kaynak Kohortlar:** ADNI-1 (1.5T), ADNI-2 (3.0T) ve ADNI-3 (3.0T) T1-ağırlıklı sMRI taramaları (Tablo I, §IV-A).
- **Denek / Tarama Sayıları (Tablo I):**
  - **ADNI-1 (1.5T):** Toplam 835 tarama:
    - AD: 200 tarama (103 Erkek / 97 Kadın; Yaş: $75.62 \pm 7.70$; MMSE: $23.29 \pm 2.04$)
    - NC: 231 tarama (119 Erkek / 112 Kadın; Yaş: $75.99 \pm 5.00$; MMSE: $29.12 \pm 0.99$)
    - sMCI (stabil MCI): 232 tarama (154 Erkek / 78 Kadın; Yaş: $76.47 \pm 7.82$; MMSE: $27.31 \pm 1.79$)
    - pMCI (progresif MCI, $\le 36$ ayda AD'ye dönen): 172 tarama (106 Erkek / 66 Kadın; Yaş: $76.34 \pm 7.15$; MMSE: $26.61 \pm 1.70$)
  - **ADNI-2 (3.0T):** Toplam 258 tarama (108 AD, 150 NC).
  - **ADNI-3 (3.0T):** Toplam 314 tarama (45 AD, 269 NC).
  - *Genel Toplam:* 1.407 denek/tarama.
- **Bölme Yöntemi:** ADNI-1 verisi 5-kat çapraz doğrulamaya (5-fold CV) tabi tutulmuştur (%80 eğitim, %20 test) (§IV-C1).
- **Dış Test Setleri:** ADNI-2 (258 tarama) ve ADNI-3 (314 tarama), bağımsız dış doğrulama setleri olarak kullanılmıştır (§IV-C2).
- **Sızıntı Riski Değerlendirmesi:** **ORTA**
  - *Gerekçe (Wen 2020 kriterleri):*
    1. *Denek vs. Görüntü Sızıntısı:* Makale "baseline MRI scans of 1407 subjects" diyerek her denekten tek bir başlangıç taraması alındığını ima etmektedir (§IV-A); ancak CV bölmesinin `StratifiedGroupKFold(RID)` ile yapıldığı açıkça belirtilmemiştir ("randomly split into 5 groups" denmektedir, §IV-C1). Tek vizit kullanıldığı için denek sızıntısı riski düşüktür.
    2. *Model Seçimi / Kilitli Test:* Ayrı bir kilitli iç test seti tanımlanmamış, hiperparametreler CV test katlarının ortalaması üzerinden değerlendirilmiştir (model seçimi sızıntısı riski).
    3. *Dış Test Gücü:* Yüksek. ADNI-2 ve ADNI-3 bağımsız 3T taramaları üzerinde sıfır-atış genelleme sınaması yapılmış olması bu riski hafifletmektedir.

---

## 5. Ön İşleme
1. **Format:** NIfTI (.nii) biçimi (§IV-A).
2. **AC-PC Hizalama:** MIPAV (Medical Image Processing, Analysis, and Visualization) yazılımı ile ön ve arka komissür (anterior/posterior commissure) eksen düzeltmesi (§IV-A).
3. **Bias Alan Düzeltmesi:** N3/N4 yoğunluk eşyönsüzlüğü düzeltmesi (§IV-A).
4. **Kafatası Ayıklama (Skull Stripping):** FSL (FMRIB Software Library v6.0) BET aracı kullanılmıştır (§IV-A).
5. **Şablon Hizalama (Registration):** FSL `flirt` komutu ile **Colin27** beyin şablonuna doğrusal afin kayıt (linear registration) yapılmış; global öteleme, ölçekleme ve döndürme farklılıkları giderilerek izotropik çözünürlüğe yeniden örneklenmiştir (§IV-A).
6. **Boyut:** Son hacim boyutu metinde doğrudan piksel olarak yazılmamış, ancak Colin27 standart ızgarası ve son katman harita boyutu ($46 \times 55 \times 46$ ve $6 \times 7 \times 6$) göz önüne alındığında yaklaşık $181 \times 217 \times 181$ vokseldir (§IV-D1).

---

## 6. Mimari
Model, $3 \times 3 \times 3$ evrişimli hafifletilmiş kök bloğu, ardından gelen artık öz-dikkat (ResAttNet) blokları ve Grad-CAM çıkarım katmanından oluşur (§III-B, §III-C, Şekil 1, Şekil 3).

### 6.1 Katman Blok Yapısı (3D-ResAttNet18 ve 3D-ResAttNet34)
- **Kök Bloğu (Stem):** Standart ResNet'teki $7 \times 7 \times 7$ (stride 2) yerine **üç ardışık $3 \times 3 \times 3$ Conv3D** (stride 1/2) + BatchNorm3d + ReLU katmanı kullanılmıştır (§III-B, §IV-C1).
- **Artık Öz-Dikkat Bloğu (ResAttNet Block):**
  1. *Artık Evrişim Kolu $r(x)$:* İki adet $3 \times 3 \times 3$ Conv3D + BatchNorm3d + ReLU.
  2. *Öz-Dikkat Katmanı $o(r(x))$:*
     - $r(x)$ çıktısı $C \times N$ tensörüne dönüştürülür ($N = D \times H \times W$).
     - $1 \times 1 \times 1$ Conv3D ile Anahtar ($W_f$), Sorgu ($W_g$) ve Değer ($W_h$) projektörleri:
       $$f(x) = W_f x, \quad g(x) = W_g x, \quad h(x) = W_h x$$
     - Dikkat matrisi: $a_{i,j} = \frac{\exp(f(x_i)^T g(x_j))}{\sum_i \exp(f(x_i)^T g(x_j))}$
     - Çıktı: $o_j = W_v \left( \sum_{i=1}^N a_{i,j} h(x_i) \right)$ ($W_v$: $1 \times 1 \times 1$ Conv3D kanal eşitleyici).
  3. *Birleşim (Füzyon):*
     $$y = x + r(x) + \gamma \cdot o(r(x))$$
     $\gamma$: Öğrenilebilir skaler katsayı (başlangıçta 0 olarak atanır, böylece model önce yerel özelliklere odaklanır, eğitim ilerledikçe küresel dikkatin payı artar) (§III-C3, Denklem 7).
- **Blok Sayıları:**
  - 3D-ResAttNet18: 4 aşamada toplam 8 ResAttNet bloğu (kanallar: 64, 128, 256, 512).
  - 3D-ResAttNet34: 4 aşamada toplam 16 ResAttNet bloğu (blok dizilimi: 3, 4, 6, 3).
- **Sınıflandırıcı Başlık:** Global Average Pooling (GAP) $\rightarrow$ Fully Connected (FC) $\rightarrow$ Softmax (2 sınıf).
- **Parametre Sayısı:** 3D-ResAttNet18 $\approx 33.6\text{ M}$; 3D-ResAttNet34 $\approx 64.2\text{ M}$ (doğrulanamadı; MONAI tabanlı hesaplama).

---

## 7. Eğitim Ayarları
- **Optimizer:** Adam optimizer (§IV-C1).
- **Öğrenme Hızı (LR):** Başlangıç LR $= 1 \times 10^{-4}$ (0.0001); iterasyonlar ilerledikçe $1 \times 10^{-6}$'ya düşürülür (§IV-C1).
- **Batch Boyutu:** 8 örnek (§IV-C1).
- **Kayıp Fonksiyonu:** Cross-Entropy Loss (§IV-C1).
- **Çapraz Doğrulama:** 5-kat çapraz doğrulama (5-fold CV) (§IV-C1).
- **Donanım:** Intel Xeon CPU E5-2650, 64 GB RAM, tek **NVIDIA GeForce RTX 2080 Ti** (11 GB VRAM) (§IV-C1).
- **Eğitim Süresi / Epoch:** Epoch sayısı makale metninde yazılmamıştır (doğrulanamadı).

---

## 8. Sonuçlar

### 8.1 3B CNN Karşılaştırma Çalışması (ADNI-1, 5-Kat CV, Tablo II)
| Model | Görev | Doğruluk (ACC) | Duyarlılık (SEN) | Özgüllük (SPE) | ROC-AUC | Kaynak |
|---|---|---|---|---|---|---|
| 3D-VGGNet | AD vs NC | $0.807 \pm 0.046$ | $0.798 \pm 0.049$ | $0.829 \pm 0.036$ | $0.890 \pm 0.036$ | Tablo II |
| 3D-ResNet18 | AD vs NC | $0.851 \pm 0.102$ | $0.849 \pm 0.103$ | $0.855 \pm 0.102$ | $0.920 \pm 0.076$ | Tablo II |
| **3D-ResAttNet18** | **AD vs NC** | **$0.860 \pm 0.088$** | $0.829 \pm 0.119$ | **$0.903 \pm 0.052$** | **$0.975 \pm 0.023$** | Tablo II |
| 3D-ResNet34 | AD vs NC | $0.882 \pm 0.147$ | $0.890 \pm 0.141$ | $0.883 \pm 0.148$ | $0.929 \pm 0.089$ | Tablo II |
| **3D-ResAttNet34** | **AD vs NC** | **$0.913 \pm 0.012$** | **$0.910 \pm 0.014$** | **$0.919 \pm 0.009$** | **$0.984 \pm 0.009$** | Tablo II |
| 3D-VGGNet | pMCI vs sMCI | $0.758 \pm 0.059$ | $0.751 \pm 0.083$ | $0.735 \pm 0.060$ | $0.856 \pm 0.056$ | Tablo II |
| 3D-ResNet18 | pMCI vs sMCI | $0.777 \pm 0.079$ | $0.775 \pm 0.092$ | $0.753 \pm 0.075$ | $0.890 \pm 0.034$ | Tablo II |
| **3D-ResAttNet18** | **pMCI vs sMCI** | **$0.799 \pm 0.071$** | $0.810 \pm 0.093$ | $0.775 \pm 0.071$ | **$0.926 \pm 0.053$** | Tablo II |
| 3D-ResNet34 | pMCI vs sMCI | $0.807 \pm 0.047$ | $0.826 \pm 0.054$ | $0.798 \pm 0.055$ | $0.954 \pm 0.033$ | Tablo II |
| **3D-ResAttNet34** | **pMCI vs sMCI** | **$0.821 \pm 0.092$** | $0.812 \pm 0.101$ | **$0.809 \pm 0.097$** | **$0.920 \pm 0.047$** | Tablo II |

*Kritik Çıkarım:* Öz-dikkat modülü eklendiğinde AD-NC AUC değeri ResNet18'de $0.920 \rightarrow 0.975$'e, ResNet34'te $0.929 \rightarrow 0.984$'e fırlamaktadır; standart sapma $0.147 \rightarrow 0.012$'ye düşerek model kararlılığı belirgin şekilde artmaktadır (Tablo II).

### 8.2 Çapraz Veri Seti Genelleme Başarımı (Tablo III)
| Eğitim Seti | Test Seti | Model | Doğruluk (ACC) | Duyarlılık (SEN) | Özgüllük (SPE) | ROC-AUC |
|---|---|---|---|---|---|---|
| ADNI-1 (1.5T) | ADNI-1 (iç test) | 3D-ResAttNet34 | $0.913 \pm 0.012$ | $0.910 \pm 0.014$ | $0.919 \pm 0.009$ | $0.984 \pm 0.009$ |
| ADNI-1 (1.5T) | **ADNI-2 (3.0T)** | 3D-ResAttNet34 | $0.909 \pm 0.019$ | $0.895 \pm 0.026$ | $0.924 \pm 0.014$ | $0.952 \pm 0.026$ |
| ADNI-1 (1.5T) | **ADNI-3 (3.0T)** | 3D-ResAttNet34 | $0.892 \pm 0.034$ | $0.788 \pm 0.060$ | $0.780 \pm 0.076$ | $0.889 \pm 0.034$ |
| ADNI-2 (3.0T) | ADNI-2 (iç test) | 3D-ResAttNet34 | $0.956 \pm 0.089$ | $0.950 \pm 0.100$ | $0.950 \pm 0.100$ | $0.978 \pm 0.044$ |
| ADNI-2 (3.0T) | **ADNI-1 (1.5T)** | 3D-ResAttNet34 | $0.933 \pm 0.133$ | $0.933 \pm 0.133$ | $0.930 \pm 0.140$ | $0.967 \pm 0.067$ |
| ADNI-2 (3.0T) | **ADNI-3 (3.0T)** | 3D-ResAttNet34 | $0.917 \pm 0.019$ | $0.885 \pm 0.068$ | $0.821 \pm 0.046$ | $0.930 \pm 0.023$ |

---

## 9. Açıklanabilirlik ve 3B Grad-CAM Analizi
- **3B Grad-CAM Formülasyonu:**
  Hedef $c$ sınıfının skoru $y(c)$'nin, $k$. öznitelik haritasının $(x, y, z)$ vokselindeki aktivasyonuna $A_{x,y,z}^k$ göre gradyanı alınır ve uzamsal global ortalamayla kanal ağırlığı $a_k^c$ hesaplanır (§III-D):
  $$a_k^c = \frac{1}{Z} \sum_x \sum_y \sum_z \frac{\partial y(c)}{\partial A_{x,y,z}^k}$$
  $$L_{\text{3D-Grad-CAM}}^c = \text{ReLU} \left( \sum_k a_k^c A_{x,y,z}^k \right)$$
- **Katman Çözünürlüğü Karşılaştırması (Şekil 6):**
  - *4. Evrişim Bloğu Çıktısı:* $6 \times 7 \times 6$ uzamsal boyuttadır; düşük çözünürlüklü ve bulanıktır, yalnızca kaba küresel bölgeleri gösterir.
  - *3. Evrişim Bloğu Çıktısı:* $46 \times 55 \times 46$ uzamsal boyuttadır; çok daha yüksek çözünürlük sunar ve hipokampus, lateral ventriküller ile serebral korteks sınırlarını net biçimde vurgular (§IV-D1).
- **Klinik Uyumluluk:** Grad-CAM aktivasyonlarının en yüksek olduğu alanlar nöropatolojik olarak kanıtlanmış atrofi odaklarıyla (hipokampal hacim kaybı, ventrikül genişlemesi) tam örtüşmektedir (§IV-D1).

---

## 10. Kod ve Tekrarlanabilirlik
- **Depo Durumu:** Makalenin resmi bir GitHub bağlantısı bulunmamaktadır (yazarlar link vermemiştir).
- **Yeniden Üretim Stratejisi:**
  - Omurga olarak MONAI `monai.networks.nets.resnet18` ve `resnet34` (`spatial_dims=3`) kullanılır.
  - Öz-dikkat modülü, Denklem 2–7'deki matematiksel formülasyona göre bağımsız bir PyTorch modülü (`ResidualSelfAttentionBlock3D`) olarak kodlanır.
  - Grad-CAM için MONAI'nin yerleşik `monai.visualize.GradCAM(model=net, target_layers="layer4")` sınıfı kullanılır.
- **Eksikler:** Resmî ağırlıklar, bölme tohumları ve eğitim logları bulunmamaktadır.

---

## 11. Güçlü ve Zayıf Yönler

### Güçlü Yönler
1. **Mimari Yenilik:** 3B medikal görüntülemede residual bağlantı ile self-attention katmanını $\gamma$ ölçeklemesiyle kaynaştıran ilk başarılı çalışmalardandır.
2. **Yüksek Başarım:** AD-NC görevinde %91.3 doğruluk ve 0.984 AUC; pMCI-sMCI görevinde %82.1 doğruluk ile literatürün en üst dilimindedir.
3. **Çoklu Kohort Doğrulaması:** 1.5T ve 3.0T tarayıcılardan gelen üç farklı fazda (ADNI-1/2/3) çapraz genelleme testi yapılmıştır.
4. **Çok Seviyeli Açıklanabilirlik:** Grad-CAM'i hem son katmanda hem de ara katmanda ($46 \times 55 \times 46$) çalıştırarak çözünürlük sorununu çözmüştür.

### Zayıf Yönler
1. **Resmî Kod Eksikliği:** Kod deposu paylaşılmamıştır; topluluk tarafından sıfırdan kurulması gerekmektedir.
2. **Denek Bölme Belirsizliği:** 5-kat CV yapılırken denek kimliklerinin (RID) sızıntısız ayrıldığı açıkça ifade edilmemiştir.
3. **Hesaplama Yükü:** $181 \times 217 \times 181$ tam boyutta self-attention matrisi ($N \times N$) bellek açısından çok maliyetlidir (bu nedenle küçük batch boyutu 8 ve ara katman projeksiyonu gerekmektedir).

---

## 12. Bizim Projeye Uyarlama
**Kurulumumuz:** ADNI1 1.5T baseline, NC/MCI/AD, $128^3$ girdi boyutu, RID düzeyinde 5-kat CV $\times$ 3 tohum; birincil görev AD-NC, ikincil 3-sınıf.

### 12.1 Neyi Aynen Alıyoruz, Neyi Değiştiriyoruz?
- **Aynen Alınanlar:**
  1. $y = x + r(x) + \gamma \cdot o(r(x))$ artık öz-dikkat formülasyonu.
  2. Başlangıçta $\gamma = 0$ ataması.
  3. $1 \times 1 \times 1$ Conv3D ile $Q, K, V$ projektörleri.
  4. MONAI `GradCAM` ile 3. veya 4. bloktan ısı haritası üretimi.
- **Değiştirilenler:**
  1. **Girdi Boyutu:** $181 \times 217 \times 181 \rightarrow 128^3$ (PROTOKOL kuralı).
  2. **Omurga Modeli:** Karşılaştırma bütçesi ve Kaggle T4 GPU kotası nedeniyle birincil model olarak **3D-ResAttNet18** seçilecektir (ResAttNet34 ablations/isteğe bağlı olarak kalacaktır).
  3. **Öz-Dikkat Konumu:** 128³ girdide bellek patlamasını önlemek için self-attention bloğu yalnızca en yüksek seviyeli özellik haritalarının bulunduğu `layer3` ve `layer4` sonrasına entegre edilecektir (düşük katmanlarda $N$ çok büyük olduğundan $N \times N$ dikkat matrisi GPU belleğini tüketir).
  4. **Görevler:** Yalnızca ikili değil, PROTOKOL madde 4 gereği NC/MCI/AD 3-sınıflı sınıflandırma başlığı eklenecektir.

### 12.2 Zorluk ve Kaynak Tahmini
- **Beklenen Zorluk:** **3 / 5** (Resmî kod olmadığından 3B Self-Attention bloğunun MONAI ResNet bloklarıyla kusursuz entegrasyonu ve GradCAM gradyan akışının kopmaması için dikkatli tensör boyutlandırması gerekir).
- **Tahminî VRAM / Süre (T4 GPU, 16 GB):**
  - Girdi $128^3$, batch 4, AMP (fp16) açıkken: VRAM tüketimi $\approx 5.5 - 7.0\text{ GB}$ (dikkat matrisi nedeniyle düz ResNet'ten ~1.5 GB daha fazla).
  - 100 epoch için kat başına eğitim süresi: $\approx 10 - 14\text{ dakika}$.

---

## 13. Opus Doğrulama

- **Sonuç:** **ÇELİŞKİ YOK**
- **Güven:** **Yüksek**
- **Hakemin Okuduğu Kaynak:** arXiv:2008.04024v2 tam metni (Bölüm I–V, Tablo I–IV, Şekil 1–6).

### 13.1 Kontrol Edilen Sayılar
| İddia | Özetteki Değer | Makaledeki Değer | Durum | Yer |
|---|---|---|---|---|
| Toplam denek sayısı | 1.407 | 1.407 denek | **Doğru** | §IV-A |
| ADNI-1 toplam tarama | 835 | 835 tarama | **Doğru** | §IV-A, Tablo I |
| ADNI-1 AD / NC / sMCI / pMCI sayıları | 200 / 231 / 232 / 172 | 200 AD, 231 NC, 232 sMCI, 172 pMCI | **Doğru** | §IV-A, Tablo I |
| ADNI-2 toplam tarama ve sınıflar | 258 (108 AD, 150 NC) | 258 (108 AD, 150 NC) | **Doğru** | §IV-A, Tablo I |
| ADNI-3 toplam tarama ve sınıflar | 314 (45 AD, 269 NC) | 314 (45 AD, 269 NC) | **Doğru** | §IV-A, Tablo I |
| ADNI-1 AD-NC 3D-ResAttNet34 ACC | $0.913 \pm 0.012$ | $0.913 \pm 0.012$ | **Doğru** | Tablo II |
| ADNI-1 AD-NC 3D-ResAttNet34 AUC | $0.984 \pm 0.009$ | $0.984 \pm 0.009$ | **Doğru** | Tablo II |
| ADNI-1 AD-NC 3D-ResAttNet18 ACC / AUC | $0.860 \pm 0.088$ / $0.975 \pm 0.023$ | $0.860 \pm 0.088$ / $0.975 \pm 0.023$ | **Doğru** | Tablo II |
| ADNI-1 pMCI-sMCI 3D-ResAttNet34 ACC / AUC | $0.821 \pm 0.092$ / $0.920 \pm 0.047$ | $0.821 \pm 0.092$ / $0.920 \pm 0.047$ | **Doğru** | Tablo II |
| ADNI-1 $\rightarrow$ ADNI-2 test ACC / AUC | $0.909 \pm 0.019$ / $0.952 \pm 0.026$ | $0.909 \pm 0.019$ / $0.952 \pm 0.026$ | **Doğru** | Tablo III |
| ADNI-1 $\rightarrow$ ADNI-3 test ACC / AUC | $0.892 \pm 0.034$ / $0.889 \pm 0.034$ | $0.892 \pm 0.034$ / $0.889 \pm 0.034$ | **Doğru** | Tablo III |
| ADNI-2 $\rightarrow$ ADNI-1 test ACC / AUC | $0.933 \pm 0.133$ / $0.967 \pm 0.067$ | $0.933 \pm 0.133$ / $0.967 \pm 0.067$ | **Doğru** | Tablo III |
| ADNI-2 $\rightarrow$ ADNI-2 iç test ACC / AUC | $0.956 \pm 0.089$ / $0.978 \pm 0.044$ | $0.956 \pm 0.089$ / $0.978 \pm 0.044$ | **Doğru** | Tablo III |
| Batch boyutu | 8 | 8 | **Doğru** | §IV-C1 |
| Başlangıç ve bitiş LR | $1 \times 10^{-4} \rightarrow 1 \times 10^{-6}$ | $1 \times 10^{-4} \rightarrow 1 \times 10^{-6}$ | **Doğru** | §IV-C1 |
| Grad-CAM katman boyutları | Katman 4: $6 \times 7 \times 6$; Katman 3: $46 \times 55 \times 46$ | Katman 4: $6 \times 7 \times 6$; Katman 3: $46 \times 55 \times 46$ | **Doğru** | §IV-D1 |

### 13.2 Düzeltmeler ve Netleştirmeler
- **Blok Sayısı Yazım Hatası:** Makale metninde §IV-C1'de "The 14 layers and 34 layers network contain 8 and 14 3D Resnet block... respectively" yazmaktadır; oysa standart ResNet-34 yapısında 16 blok (3, 4, 6, 3) bulunur ve metindeki "14 layers" ifadesi bir dizgi hatasıdır (ResNet-18 kastedilmiştir). Kod implementasyonumuzda standart ResNet-18 ve ResNet-34 blok dizilimi temel alınacaktır.
- **Kök Blok Yapısı:** Metinde $7 \times 7 \times 7$ evrişim yerine "three conservative $3 \times 3 \times 3$ convolutions" yazmaktadır ("consecutive" yerine yanlışlıkla "conservative" yazılmıştır). Üç ardışık evrişim kast edilmektedir.

### 13.3 Özetin Atladığı Önemli Noktalar
- Makalede ADNI-2 ve ADNI-3 kohortlarında pMCI ve sMCI örnek sayısı yetersiz olduğu için çapraz veri seti deneyleri (Tablo III) yalnızca AD vs NC göreviyle sınırlı tutulmuştur.
- Self-attention modülündeki $\gamma$ parametresi eğitim boyunca dondurulmamakta, geriye yayılımla optimize edilmektedir.

### 13.4 Doğrulanamayanlar
- Modelin kaç epoch eğitildiği ve erken durdurma uygulanıp uygulanmadığı (metinde açıkça belirtilmemiştir).
- Resmî PyTorch kod deposu (yazarlar tarafından kamuya açılmamıştır).

### 13.5 Okuyucunun İşaretlediği Anahtar Sayılar (Ham Liste)
- 1.407 denek (Tablo I)
- 835 ADNI-1 taraması (200 AD, 231 NC, 232 sMCI, 172 pMCI) (Tablo I)
- AD vs NC 3D-ResAttNet34: ACC 0.913, AUC 0.984 (Tablo II)
- pMCI vs sMCI 3D-ResAttNet34: ACC 0.821, AUC 0.920 (Tablo II)
- Batch size: 8 (§IV-C1)
- LR: 1e-4 $\rightarrow$ 1e-6 (§IV-C1)
- 5-kat CV (§IV-C1)

---

## 14. Kaynaklar
- **arXiv Tam Metin:** https://arxiv.org/abs/2008.04024
- **IEEE Yayın Linki:** https://doi.org/10.1109/JBHI.2021.3116087
- **FSL Kayıtlama ve BET:** https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/
- **MONAI Dokümantasyonu (GradCAM & ResNet):** https://docs.monai.io/en/stable/visualize.html
