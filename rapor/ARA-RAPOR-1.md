# 1. ARA RAPOR — PROJE ÖNERİSİ VE PLANLAMA

## KAPAK

**Proje adı:** Alzheimer Hastalığının Erken Teşhisi İçin 3B Derin Öğrenme Tabanlı Karar Destek Sistemi Geliştirilmesi

**Öğrenciler:**
Ahmet Görkem Yavuz (G231210032) · Ertuğrul Kabaoğlu (G231210376) · Baran Yeşilyurt (G231210078)

**Danışman:** Dr. Öğr. Üyesi Can Yüzkollar

**Ders:** BSM 401 Bilgisayar Mühendisliği Tasarımı — 2026-2027 Güz


**Proje deposu:** https://github.com/YesilBaraN/tasarim-alzheimer

---

## 1. PROJE TANIMI

### 1.1 Amaç

Alzheimer hastalığı, beynin belirli bölgelerinin zamanla küçülmesiyle ilerler. Bu küçülme beyin MR görüntüsünde görülebilir, ama erken evrede çok hafiftir ve bir uzmanın bile her zaman yakalaması kolay değildir. Bu projede, bir beyin MR görüntüsünü alıp kişinin sağlıklı mı yoksa Alzheimer hastası mı olduğuna dair bir olasılık üreten bir **karar destek sistemi** geliştirmek istiyoruz.

Projeyi sıradan bir "model eğittik, şu kadar doğruluk aldık" çalışmasından ayıran şey şu: biz tek bir model önermiyoruz. Literatürdeki **altı farklı 3B derin öğrenme mimarisini**, aynı veri, aynı bölme ve aynı eğitim yöntemiyle yan yana koyup karşılaştırıyoruz.

### 1.2 Neden böyle bir karşılaştırma?

Literatürü okurken fark ettiğimiz şey şuydu: her makale kendi veri alt kümesiyle, kendi ön işlemesiyle ve kendi bölme yöntemiyle çalışıyor. Bu yüzden makalelerdeki doğruluk oranlarını yan yana koyup "şu model daha iyi" demek mümkün değil. Daha kötüsü, bazı çalışmalarda aynı hastanın taramaları hem eğitimde hem testte yer alıyor. Buna **veri sızıntısı** deniyor ve sonuçları 25–55 puan şişirebiliyor.

Bu yüzden projenin ilk işi model yazmak değil, adil bir karşılaştırma protokolü yazmak olacak.

### 1.3 Kapsam

Projeye dahil olanlar:

- Altı mimarinin gerçekleştirilmesi ve ortak protokolle eğitilmesi
- İki temel çizgi (basit bir 3B CNN ve voksel tabanlı SVM), böylece derin modellerin gerçekten bir şey katıp katmadığı görülebilsin
- Ham MR görüntülerini standart hale getiren bir ön işleme hattı
- Modelin kararını görselleştiren açıklanabilirlik haritaları
- Eğitilmiş modeli çalıştıran bir çıkarım katmanı ve web arayüzü prototipi

Projeye dahil olmayanlar:

- Klinik kullanım veya tıbbi cihaz onayı. Sistem bir karar destek aracıdır, tek başına tanı koymaz.
- Yeni bir mimari önermek
- MR dışındaki veriler (kan testi, bilişsel testler vb.)

### 1.4 Önemi ve katma değer

Alzheimer erken yakalandığında hastalığın seyrini yavaşlatan tedaviler ve yaşam düzenlemeleri daha etkili oluyor. MR zaten rutin bir tetkik, yani bu yönde bir araç ek maliyet getirmiyor.

Projenin katkıları:

1. **Karşılaştırılabilir sonuçlar.** Altı mimarinin aynı koşullarda yan yana görülmesi, hangi tasarım kararının gerçekten fark yarattığını gösterir.
2. **Sızıntıya karşı korunmuş protokol.** Protokol yalnız bir belge olarak kalmayacak, kodla zorlanacak. Kurala uymayan bir koşu sonuç tablosuna girmeyecek.
3. **Açıklanabilirlik.** Sistem yalnız bir olasılık değil, kararın beynin hangi bölgesinden geldiğini de gösterecek.
4. **Tekrarlanabilirlik.** Kod, bölme listeleri ve ayarlar açık depoda duracak, başkası aynı sonuca ulaşabilecek.

---

## 2. LİTERATÜR ÖZETİ

Projeye başlarken yirmi yediye yakın makale taradık, bunlardan sekizi bu raporun konusuyla en doğrudan ilgili. Tamamı ikinci raporda ayrıntılı işlenecek.

**Wen vd. (2020)** [1] alandaki 32 çalışmayı inceleyip 16'sında veri sızıntısı olasılığı buldu. Sonra aynı protokolle dört farklı yaklaşımı (tüm beyin 3B, hipokampüs, yama, 2B dilim) karşılaştırdı. En ilginç sonuç: basit bir doğrusal SVM, 3B derin ağlarla yarışacak düzeyde (dengeli doğruluk 0,88'e karşı 0,82). Projemizin protokolü büyük ölçüde bu makaleye dayanıyor ve iki temel çizgiyi eklememizin sebebi de bu.

**Yagis vd. (2021)** [2] bölme yönteminin etkisini doğrudan ölçtü. Dilim düzeyinde bölme yapılınca doğruluk %66–70'ten %94–99'a çıkıyor. Etiketler rastgele karıştırıldığında bile dilim düzeyi bölme %94 civarında kalıyor, denek düzeyi ise %50'de. Yani yanlış bölme, öğrenilecek bir şey olmasa bile yüksek skor üretiyor. Bu bizim için "bölme her zaman denek düzeyinde olacak" kuralının gerekçesi.

**Korolev vd. (2017)** [3] 3B ağlarda düz mimari (VoxCNN) ile artık bağlantılı mimariyi (VoxResNet) karşılaştırdı. Alzheimer-sağlıklı ayrımında AUC yaklaşık 0,88 elde etti, ama erken ve geç MCI arasında başarı şansa düştü. Bu, erken evre ayrımının ne kadar zor olduğunu gösteriyor. İki mimariyi de projemize alıyoruz.

**Chen vd. (2019)** [4] 23 farklı tıbbi veri setinde ön eğitilmiş 3B ResNet ağırlıkları yayımladı. Ön eğitim, az veriyle çalışırken özellikle işe yarıyor. Makale, kazancı göstermek için aynı mimarinin sıfırdan eğitilmiş halinin de koşulmasını şart koşuyor. Biz de bunu iki ayrı koşu olarak planlıyoruz.

**Böhle vd. (2019)** [5] 3B ağların kararlarını voksel düzeyinde açıklayan LRP yöntemini kullandı. Sağlıklı kişilerde ilgi neredeyse sıfır, hastalarda hipokampüs ve temporal lob öne çıkıyor. Açıklanabilirlik katmanımız için temel aldığımız çalışma bu.

**Zhang vd. (2021)** [6] ResNet'e öz-dikkat ekleyen bir model önerdi. Modelin sonuçlarının kararlılığı belirgin biçimde arttı (standart sapma %14,7'den %1,2'ye düştü). Projedeki dördüncü modelimiz bu.

**Qiu vd. (2020)** [7] tüm beyin için bir hastalık olasılık haritası üreten, yama tabanlı bir ağ geliştirdi. Yalnız MR ile elde ettiği %83,4 doğruluk, on bir uzman nörologun ortalamasını (%82,3) geçti. Beşinci modelimizin temeli bu.

**Lian vd. (2020)** [8] çok ölçekli yamalarla çalışan hiyerarşik bir ağ ile sızıntısız bir kurulumda AD-sağlıklı ayrımında %90,3 doğruluk elde etti. Hedeflerimizi belirlerken bunu üst sınır olarak aldık.

---

## 3. PROJENİN TEKNİK ALTYAPISI

### 3.1 Donanım

Geliştirme tek bir dizüstü bilgisayarda yapılıyor:

| Bileşen | Özellik |
|---|---|
| İşlemci | Intel Core i5-12450H (8 çekirdek / 12 iş parçacığı) |
| Ekran kartı | NVIDIA GeForce RTX 3050 Laptop, **4 GB VRAM** |
| Bellek | 16 GB RAM |
| Depolama | 185 GB boş alan |
| İşletim sistemi | Windows 11 |

4 GB'lık ekran kartı projenin en önemli kısıtı. Bu bellek 3B modeller için dardır, bu yüzden hangi modelin hangi ayarla sığacağını tahmin etmek yerine ölçeceğiz. Sığmayan modellerde küçük batch ve gradyan biriktirme kullanacağız, etkin batch'i sabit tutarak karşılaştırmayı bozmayacağız.

### 3.2 Yazılım

| Alan | Araç |
|---|---|
| Dil | Python 3.12 |
| Derin öğrenme | PyTorch 2.14 (CUDA 12.6), MONAI 1.6 |
| Görüntü işleme | SimpleITK (bias düzeltme ve kayıt), NiBabel, HD-BET (kafatası ayıklama) |
| Analiz | scikit-learn, pandas, NumPy, Matplotlib |
| Dağıtım | ONNX ve ONNX Runtime |
| Sürüm kontrolü | Git ve GitHub, GitHub Actions ile otomatik test |

Bütün bileşenler MIT, Apache veya BSD lisanslı. Lisansı GPL olan kodu projeye almayacağız.

### 3.3 Veri

Birincil veri seti olarak **ADNI** (Alzheimer's Disease Neuroimaging Initiative) hedefliyoruz. Bu veriye erişim kurumsal onay gerektiriyor, başvurumuzu yaptık ve onay bekliyoruz. Aynı şekilde **OASIS** için de başvurduk.

Onay gelene kadar çalışmanın durmaması için açık erişimli bir köprü veri seti arıyoruz. Bu veri hem hattı sınamamızı sağlayacak, hem de ADNI geldiğinde bağımsız bir dış test kümesine dönüşecek.

Veri kullanım sözleşmeleri gereği ham görüntüler depoya konmayacak. Depoda yalnız denek kimliği ve bölme bilgisi duracak.

---

## 4. PROJE ZAMAN ÇİZELGESİ

Dönem sonu 27 Aralık 2026, raporlar için en geç teslim 28 Aralık. Planı haftalara böldük (H5 = 24–30 Ekim).

| İş | H5 | H6 | H7 | H8 | H9 | H10 | H11 | H12 | H13 | H14 |
|---|---|---|---|---|---|---|---|---|---|---|
| ADNI / OASIS erişim başvurusu | ■ | ■ | | | | | | | | |
| 15 makale incelemesi | | ■ | ■ | | | | | | | |
| Gereksinim analizi | | ■ | ■ | | | | | | | |
| Mimari, ER ve akış tasarımı | | | ■ | ■ | | | | | | |
| **Ara Rapor 2** | | | | ■ | | | | | | |
| Ön işleme hattı | | | ■ | ■ | ■ | | | | | |
| Altı modelin eğitimi ve karşılaştırma | | | | ■ | ■ | ■ | | | | |
| Açıklanabilirlik, ONNX, API, arayüz | | | | | | ■ | ■ | | | |
| **Ara Rapor 3** | | | | | | | ■ | | | |
| Final rapor, poster, sunum | | | | | | | | ■ | ■ | ■ |

H5 = 24–30 Ekim · H8 = 14–20 Kasım · H11 = 5–11 Aralık · H14 = 26–28 Aralık.

### 4.1 Risk ve önlem

| Risk | Önlem |
|---|---|
| ADNI onayı gecikebilir | Açık erişimli köprü veriyle hattı kurup sınıyoruz, kod veri yoluna bağlı değil |
| 4 GB ekran kartı modellere dar gelebilir | Hangi modelin sığacağını ölçüyoruz, sığmayana küçük batch + gradyan biriktirme |
| Tüm koşular için hesaplama süresi yetmeyebilir | Koşuları öncelik sırasına böldük, birincil görev tam protokolle, ikincil görev kısaltılmış koşulur |
| Veri sızıntısı | Bölme denek düzeyinde yapılır, test kümesi kilitlidir, sızıntı kontrolü her bölmeden sonra çalışır |

---

## 5. BEKLENEN SONUÇLAR

Proje sonunda şunları elde etmeyi hedefliyoruz:

1. **Altı mimarinin karşılaştırma tablosu.** Hepsi aynı veri, aynı bölme ve aynı eğitim ayarıyla, ortalama ve standart sapma değerleriyle.
2. **Ön eğitimin etkisinin ölçümü.** Aynı mimarinin ön eğitimli ve sıfırdan eğitilmiş hali yan yana.
3. **Çalışan bir karar destek prototipi.** Bir MR yüklenir, ön işlemeden geçer, model olasılık üretir, karar bir ısı haritasıyla görselleştirilir.
4. **Açık depo.** Kod, protokol, bölme listeleri ve koşu kayıtlarıyla başkasının tekrarlayabileceği bir çalışma.

**Hedef başarım:** Alzheimer-sağlıklı ayrımında en az %85 dengeli doğruluk. Bu, sızıntısız kurulumlarda literatürün üst bandı (%82–90). Üç sınıflı görev (sağlıklı, MCI, Alzheimer) çok daha zor olduğu için ikincil görev olarak, gerçekçi bir beklentiyle raporlanacak.

---

## KAYNAKLAR

[1] J. Wen vd., "Convolutional neural networks for classification of Alzheimer's disease: Overview and reproducible evaluation," *Medical Image Analysis*, c. 63, 2020.

[2] E. Yagis vd., "Effect of data leakage in brain MRI classification using 2D convolutional neural networks," *Scientific Reports*, c. 11, 2021.

[3] S. Korolev, A. Safiullin, M. Belyaev, Y. Dodonova, "Residual and plain convolutional neural networks for 3D brain MRI classification," *IEEE ISBI*, 2017.

[4] S. Chen, K. Ma, Y. Zheng, "Med3D: Transfer learning for 3D medical image analysis," *arXiv:1904.00625*, 2019.

[5] M. Böhle, F. Eitel, M. Weygandt, K. Ritter, "Layer-wise relevance propagation for explaining deep neural network decisions in MRI-based Alzheimer's disease classification," *Frontiers in Aging Neuroscience*, c. 11, 2019.

[6] X. Zhang vd., "An explainable 3D residual self-attention deep neural network for joint atrophy localization and Alzheimer's disease diagnosis using structural MRI," *IEEE J. Biomed. Health Inform.*, 2021.

[7] S. Qiu vd., "Development and validation of an interpretable deep learning framework for Alzheimer's disease classification," *Brain*, c. 143, sy. 6, 2020.

[8] C. Lian vd., "Hierarchical fully convolutional network for joint atrophy localization and Alzheimer's disease diagnosis using structural MRI," *IEEE TPAMI*, c. 42, 2020.
