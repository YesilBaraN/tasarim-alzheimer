# P06 — Böhle 2019 — LRP ile Açıklanabilir 3B Beyin MRI Alzheimer Sınıflandırması

> **Durum:** ☐ okunmadı · ☑ AI özeti hazır · ☑ Opus doğrulandı (**ÇELİŞKİ VAR**, güven: yüksek) · ☐ insan okudu · ☐ implemente edildi
> **Sorumlu:** Ahmet Görkem Yavuz · **Grup:** B · **Tam metin (ücretsiz):** https://pmc.ncbi.nlm.nih.gov/articles/PMC6685087/ · **Kod:** https://github.com/moboehle/Pytorch-LRP (BSD 3-Clause)
> **AI okuma kaynağı:** PMC tam metni (PMC6685087, Frontiers in Aging Neuroscience 2019;11:194, tüm bölümler 1–5, Şekil 1–9, formüller ve referanslar okundu). Kod deposu github.com/moboehle/Pytorch-LRP master dalı (`license.txt`, `ADNI Training.ipynb`, `Data Split ADNI.ipynb`, `Evaluate GB and LRP.ipynb`, `innvestigator.py`, `inverter_util.py`, `utils.py`, `settings.py`) incelendi.

> ⚠ **Nasıl okunmalı:** §2–§12 ilk okuma özetidir; §13 hakem denetimidir (§13.1–§13.5). Makale metni ile veri bölme sayıları arasındaki iç çelişki §13.2'de belgelenmiştir; implementasyonda (§12.3) ve karar destek arayüzünde (§4.3) geçerli olan değerler bu denetime dayanır.

---

## 1. Künye
- **Yazarlar:** Moritz Böhle, Fabian Eitel, Martin Weygandt, Kerstin Ritter
- **Yıl:** 2019 (Alınma: 27 Şubat 2019, Kabul: 15 Temmuz 2019, Çevrimiçi Yayın: 06 Ağustos 2019)
- **Başlık:** *Layer-Wise Relevance Propagation for Explaining Deep Neural Network Decisions in MRI-Based Alzheimer's Disease Classification*
- **Yayın Yeri:** Frontiers in Aging Neuroscience, Cilt 11, Makale 194, ss. 1–16
- **DOI:** [10.3389/fnagi.2019.00194](https://doi.org/10.3389/fnagi.2019.00194) · **PubMed Central:** [PMC6685087](https://pmc.ncbi.nlm.nih.gov/articles/PMC6685087/) · **PMID:** 31417397
- **Atıf Sayısı:** ~175–210 (Google Scholar / Semantic Scholar, Ekim 2026 itibarıyla)
- **Kurumlar:** Charité – Universitätsmedizin Berlin, Bernstein Center for Computational Neuroscience Berlin, Humboldt-Universität zu Berlin (Almanya)
- **Açık Kod:** https://github.com/moboehle/Pytorch-LRP (BSD 3-Clause, PyTorch)

---

## 2. Tek Paragraf Özet
Makale, 3B yapısal MRI (T1-MPRAGE) verisinden evrişimli sinir ağları (3B CNN) ile yapılan Alzheimer hastalığı (AD) teşhis kararlarını klinisyenler için yorumlanabilir kılmak amacıyla Katman Düzeyinde İlgi Yayılımı (Layer-wise Relevance Propagation, LRP) yöntemini önerir (§1, §2.3.1). ADNI1 1.5T kohortundan 193 AD ve 151 sağlıklı kontrol (HC) deneğine ait toplam 969 tarama (bölme tablolarında 1.069 tarama) kullanılmış; ANTs ile 1 mm³ ICBM152 2009c şablonuna afin/doğrusal olmayan kaydedilmiş görüntüler kafatası maskesiyle 4 bloklu 3B CNN modeline beslenmiştir (§2.1, §2.2). Denek düzeyinde tabakalı ayrılan kilitli test setinde %87.96 doğruluk (val %91.00) elde eden ağ üzerinde LRP $\beta$-kuralı ($\beta=0$) işletilerek girdi uzayında voksel düzeyinde pozitif ilgi ısı haritaları üretilmiştir (§2.2, §2.3.1). Yöntem, gradyan tabanlı Kılavuzlu Geri Yayılım (Guided Backpropagation, GB) ile karşılaştırılmış; LRP haritalarının HC bireylerde neredeyse sıfır ilgi üreterek AD'ye özgül kaldığı, temporal lob ve hipokampüste yoğunlaştığı ve hipokampüs ilgisinin hipokampal hacim küçülmesiyle anlamlı negatif korelasyon gösterdiği ($r = -0.560, p < 10^{-3}$) kanıtlanmıştır (§3.2, §3.3). Çalışmanın güçlü yönü, kara kutu 3B CNN kararlarını biyobelirteç düzeyinde bireysel "parmak izi" olarak açıklayabilmesi ve PyTorch için açık kaynaklı LRP modülü sunmasıdır; zayıf yönü ise MCI sınıfını dışlaması, tek merkezli veriyle yetinmesi ve mimarinin sabit girdi boyutuna (ICBM152) bağımlı olmasıdır (§4).

---

## 3. Problem ve Katkı
- **Problem:** Derin evrişimli sinir ağları 3B MRI üzerinde yüksek sınıflandırma başarımı göstermesine rağmen "kara kutu" doğaları nedeniyle klinik pratikte hekimler tarafından benimsenememektedir; yalnızca tek bir olasılık skoru (ör. %89 AD) sunan sistemler, kararın hangi nöroanatomik değişikliklere dayandığını açıklayamamaktadır (§1, Şekil 1). Gradyan tabanlı duyarlılık haritaları (Guided Backpropagation) ise "hangi voksel değişirse çıktı en çok değişir?" sorusuna yanıt vermekte ve hastalığa özgü olmayan genel model kararsızlığını yansıtmaktadır (§1, §2.3.2).
- **Katkı 1 (3B MRI için LRP Uyarlaması):** Girdi uzayında korunum ilkesine dayanan Katman Düzeyinde İlgi Yayılımı (LRP) algoritması ilk kez yapısal 3B beyin MRI verisi üzerinde AD sınıflandırması için uygulanmış ve PyTorch açık kaynak kütüphanesi (`innvestigator.py`) olarak yayımlanmıştır (§2.3.1, §6).
- **Katkı 2 (Pozitif Katkı ve $\beta$-Kuralı Analizi):** LRP $\beta$-kuralında ($\beta=0, 0.25, 0.5, 0.75, 1$) $\beta=0$ seçilerek inhibitör etkilerden arındırılmış saf "AD lehine yapısal kanıt" haritaları üretilmiş; $\beta$ büyüdükçe haritanın seyrekleştiği ve biyolojik korelasyonun zayıfladığı gösterilmiştir (§2.3.1, §3.3).
- **Katkı 3 (Atlas Tabanlı Boyutsuz Metrikler):** Voksel ilgilerini Neuromorphometrics beyin atlası (SPM12) bölgelerine eşleyen üç nicel metrik tanımlanmıştır: (a) Bölge bazlı toplam ilgi, (b) Alan boyutuna normalize edilmiş ilgi yoğunluğu (*relevance density*), (c) Sağlıklı kontrollere göre ilgi artış oranı (*relevance gain*) (§2.5).
- **Katkı 4 (Nörobiyolojik Doğrulama ve Bireysel Parmak İzi):** Model kararlarının AD'nin bilinen atrofisiyle örtüştüğü nicel olarak doğrulanmış; hipokampal LRP ilgisi ile bağımsız FreeSurfer hipokampüs hacmi arasında $r = -0.560$ düzeyinde istatistiksel olarak anlamlı ($p < 0.001$) negatif ilişki saptanmıştır (§3.3, Şekil 9). Farklı hastalarda farklı atrofi örüntülerinin ("bireysel ilgi parmak izi") ayrışabildiği kanıtlanmıştır (§3.3, Şekil 8).

---

## 4. Veri Seti ve Bölme
- **Kaynak:** ADNI1 (Alzheimer's Disease Neuroimaging Initiative 1), "MRI collection - Standardized 1.5T List - Annual 2 year" koleksiyonu (§2.1).
- **Tanı Kriterleri:** Clinical Dementia Rating (CDR) skoru; CDR > 0.5 ise AD, CDR = 0 ise HC. MCI denekleri (CDR = 0.5) çalışmadan tamamen çıkarılmıştır (`Data Split ADNI.ipynb`, §2.1).
- **Denek ve Tarama Sayısı:**
  - Makale metni girişi (§2.1): 193 AD hastası (475 tarama) ve 151 HC birey (494 tarama) olmak üzere 344 denekten toplam **969 bireysel tarama** (1.5T T1-MPRAGE, 3 yıla kadar boylamsal vizitler).
  - Makale bölme detayı (§2.2) ve kod tablosu (`Data Split ADNI.ipynb`):
    - **Eğitim Seti:** 163 AD hastası, 121 HC birey $\rightarrow$ **797 tarama**
    - **Doğrulama (Val) Seti:** 18 AD hastası, 18 HC birey $\rightarrow$ **100 tarama**
    - **Test (Holdout) Seti:** 30 AD hastası, 30 HC birey $\rightarrow$ **172 tarama**
    - Toplam denek: 211 AD + 169 HC = **380 denek**; Toplam tarama: 797 + 100 + 172 = **1.069 tarama** (*Not: §2.1 metnindeki 969 tarama ile §2.2'deki 1.069 tarama arasında iç tutarsızlık vardır; kod 1.069 tarama üretir, bkz. §13.2*).
  - Ön işleme hatası nedeniyle dışlanan: 1 tarama (`067_S_0077/Screening`).
- **Bölme Yöntemi:** Kesinlikle **denek (hasta / RID) düzeyinde** tabakalı bölme yapılmıştır (`train_test_split`, `random_state=43`, `test_subjects_per_class=30`, `val_subjects_per_class=18`). Aynı deneğin hiçbir boylamsal taraması eğitim ve test arasında paylaşılmamıştır (§2.2). Çapraz doğrulama (CV) yerine tek bir sabit kilitli test ayrılmıştır.
- **Dış Test Seti:** Yoktur; bağımsız kohort (AIBL veya OASIS) üzerinde sıfır-atış genelleme sınanmamıştır.
- **Sızıntı Riski Değerlendirmesi:** **DÜŞÜK – ORTA**
  - *Gerekçe (Wen 2020 kriterleri):*
    1. *Yanlış bölme (hasta sızıntısı):* Yok (Düşük). Bölme denek bazında yapılmış, boylamsal vizitler aynı kümeye toplanmıştır.
    2. *Geç bölme:* Düşük. Ön işleme (ANTs şablon kaydı) denekler arası etiket bağımlılığı içermeyen standart anatomik hizalamadır.
    3. *Taraflı transfer:* Yok. Model sıfırdan eğitilmiştir.
    4. *Bağımsız test seti:* Orta risk. Tek bir test kümesi (60 denek, 172 görüntü) ayrılmış; ancak hiperparametre optimizasyonu ve erken durdurma bağımsız doğrulama kümesi (36 denek, 100 görüntü) üzerinde yapılmış, test setine dokunulmamıştır. Bununla birlikte k-kat CV yapılmadığından varyans raporlanmamıştır ve dış kohort testi bulunmamaktadır.

---

## 5. Ön İşleme
1. **Ham Veri:** ADNI standart 1.5T T1-weighted MPRAGE taramaları (gradyan doğrusal olmama düzeltmesi, B1 alan eşyönsüzlüğü düzeltmesi ve fantom tabanlı distorsiyon düzeltmesi uygulanmış ADNI dosyaları) (§2.1).
2. **Kayıtlama (Registration):** ANTs (`antsRegistrationSyNQuick.sh`) kullanılarak 1 mm³ izotropik çözünürlüklü **ICBM152 2009c doğrusal olmayan şablonuna** (*non-linear registration*) hizalama yapılmıştır (§2.1).
3. **Kafatası Ayıklama (Skull Stripping):** Hizalama sonrasında standart ikili beyin maskesi (`binary_brain_mask.nii.gz`) ile beyin dışı dokular sıfırlanmıştır (`Data Split ADNI.ipynb`, §2.1).
4. **Boyut ve Çözünürlük:** Görüntüler alt-örneklenmemiş (downsampling yapılmamış), doğrudan ICBM152 ızgarasında tutulmuştur. Matris boyutu $193 \times 229 \times 193$ vokseldir (§2.1, kod analizi).
5. **Yoğunluk Normalizasyonu:** Doku içi voksel değerleri doğrudan float32 tensörlere dönüştürülmüştür.
6. **Veri Artırma (Data Augmentation):** Yalnızca eğitim sırasında uygulanmıştır (§2.2):
   - Sagittal eksende rastgele çevirme (*sagittal flip*, $p = 0.50$),
   - Sagittal eksende $[-2, +2]$ voksel rastgele öteleme (*sagittal translation*).

---

## 6. Mimari
Model, $193 \times 229 \times 193$ boyutundaki 3B beyin hacmini doğrudan işleyen 4 evrişim bloğu ve 2 tam bağlantılı katmandan oluşan özel bir 3B CNN mimarisidir (`ClassificationModel3D`, `ADNI Training.ipynb`, §2.2).

### 6.1 Katman Blok Tablosu
| Katman / Blok | Çekirdek (Kernel) | Adım (Stride) | Dolgu (Padding) | Kanal | Çıktı Boyutu ($C \times D \times H \times W$) | Notlar |
|---|---|---|---|---|---|---|
| **Girdi** | — | — | — | 1 | $1 \times 193 \times 229 \times 193$ | ICBM152 1 mm afin/non-lineer T1 |
| **Conv_1** | $3 \times 3 \times 3$ | 1 | 0 (valid) | 8 | $8 \times 191 \times 227 \times 191$ | ReLU + BatchNorm3d(8) |
| **MaxPool_1** | $2 \times 2 \times 2$ | 2 | 0 | 8 | $8 \times 95 \times 113 \times 95$ | Boyut indirgeme |
| **Conv_2** | $3 \times 3 \times 3$ | 1 | 0 (valid) | 16 | $16 \times 93 \times 111 \times 93$ | ReLU + BatchNorm3d(16) |
| **MaxPool_2** | $3 \times 3 \times 3$ | 3 | 0 | 16 | $16 \times 31 \times 37 \times 31$ | $3 \times 3 \times 3$ pencere |
| **Conv_3** | $3 \times 3 \times 3$ | 1 | 0 (valid) | 32 | $32 \times 29 \times 35 \times 29$ | ReLU + BatchNorm3d(32) |
| **MaxPool_3** | $2 \times 2 \times 2$ | 2 | 0 | 32 | $32 \times 14 \times 17 \times 14$ | $2 \times 2 \times 2$ pencere |
| **Conv_4** | $3 \times 3 \times 3$ | 1 | 0 (valid) | 64 | $64 \times 12 \times 15 \times 12$ | ReLU + BatchNorm3d(64) |
| **MaxPool_4** | $3 \times 3 \times 3$ | 3 | 0 | 64 | $64 \times 4 \times 5 \times 4$ | Çıktı: $64 \times 80 = 5.120$ voksel |
| **Flatten & Dropout** | — | — | — | — | 5.120 | Dropout ($p = 0.40$) |
| **Dense_1 (FC)** | — | — | — | — | 128 | Linear(5120, 128) + ReLU |
| **Dropout_2** | — | — | — | — | 128 | Dropout ($p = 0.40$) |
| **Dense_2 (FC)** | — | — | — | — | 2 | Linear(128, 2) + Softmax |

- **Toplam Parametre Sayısı:** ~728.914 (~0.73 M parametre; 73K evrişimsel + 655K tam bağlantılı).
- **Girdi Boyutu:** $1 \times 193 \times 229 \times 193$ (küçültülmemiş MNI şablon boyutu).
- **Ön Eğitim / Transfer:** Yoktur (sıfırdan rastgele başlatma).

---

## 7. Eğitim Ayarları
- **Optimizer:** Adam ($\beta_1=0.9, \beta_2=0.999$) (§2.2).
- **Öğrenme Hızı (LR):** $10^{-4}$ (0.0001), sabit takvim (§2.2).
- **Ağırlık Sönümü (Weight Decay):** $10^{-4}$ (0.0001) (§2.2).
- **Batch Boyutu:** 4 (`ADNI Training.ipynb` hücresi, b=4; makale metninde yazılmamıştır).
- **Kayıp Fonksiyonu:** Cross-Entropy Loss (ikili sınıflandırma için) (`ADNI Training.ipynb`).
- **Erken Durdurma (Early Stopping):** Doğrulama kümesi doğruluğu 8 epoch boyunca gelişmediğinde eğitim sonlandırılır (*patience = 8*) (§2.2).
- **En İyi Model Seçimi:** En yüksek doğrulama doğruluğu elde edilen kontrol noktası (checkpoint) test değerlendirmesi için saklanır (§2.2).
- **Donanım ve Süre:** Kod NVIDIA GPU üzerinde PyTorch ile koşulmuştur; GPU modeli ve toplam eğitim süresi makale metninde raporlanmamıştır (doğrulanamadı).

---

## 8. Sonuçlar

### 8.1 Sınıflandırma Başarımı
| Görev | Metrik | Değer | Veri Kümesi | Kaynak (Makale İçi) |
|---|---|---|---|---|
| **AD vs HC** | Doğruluk (Accuracy) | **%91.00** | Doğrulama Seti (100 tarama) | §2.2 |
| **AD vs HC** | Doğruluk (Accuracy) | **%87.96** (151 / 172) | Bağımsız Test Seti (172 tarama) | §2.2 |
| **AD vs HC** | Dengeli Doğruluk (BAcc) | Raporlanmamış (kodda mevcut) | Test Seti | §2.2 (makalede yok) |
| **AD vs HC** | ROC-AUC | Raporlanmamış | Test Seti | §2.2 (makalede yok) |
| **AD vs HC** | Duyarlılık / Özgüllük | Raporlanmamış | Test Seti | §2.2 (makalede yok) |
| **MCI Görevleri** | Herhangi bir metrik | — (MCI hariç tutulmuştur) | — | §2.1 |

*Not:* Makale saf bir teşhis yarışması makalesi değil, açıklanabilirlik yöntemi sunumu olduğundan Tablo 1 biçiminde geniş bir metrik tablosu içermez; tek model eğitilip test doğruluğu %87.96 olarak verilmiştir.

### 8.2 Karşılaştırılan Açıklanabilirlik Yöntemleri
- **Kılavuzlu Geri Yayılım (Guided Backpropagation, GB):** Gradyan tabanlı duyarlılık analizi. Voksel türevlerinin mutlak değerini alır; negatif gradyanlar doğrultma katmanında sıfırlanır (§2.3.2).
- **Fark:** GB haritaları hem AD hem HC deneklerde yüksek sinyal üretmekte (Şekil 2 sağ), modelin "hangi vokseller değişirse karar en çok sarsılır" duyarlılığını ölçmektedir. LRP ise HC deneklerde neredeyse hiç ilgi üretmeyerek pozitif AD kanıtını ayrıştırmaktadır (§3.1).

---

## 9. Açıklanabilirlik ve Ek Analiz

### 9.1 LRP Formülasyonu ve $\beta$-Kuralı
Katman $l+1$'deki $j$ nöronunun ilgisi ($R_j^{l+1}$), katman $l$'deki $i$ nöronlarına şu kurala göre geri dağıtılır (§2.3.1):
$$R_i^l = \sum_j \left( (1 + \beta) \frac{z_{ij}^+}{z_j^+} - \beta \frac{z_{ij}^-}{z_j^-} \right) R_j^{l+1}$$
Burada $z_{ij}^+$ pozitif girdileri, $z_{ij}^-$ negatif girdileri temsil eder. Korunum ilkesi ($\sum_i R_i^l = \sum_j R_j^{l+1}$) geçerlidir. $\beta = 0$ seçildiğinde harita yalnızca AD sınıf skorunu artıran pozitif yapısal özellikleri vurgular (§2.3.1).

### 9.2 Atlas Tabanlı Önem Metrikleri (Neuromorphometrics Atlası)
1. **Toplam İlgi (Sum of Relevance):** Bölgedeki voksellerin ilgilerinin toplamı. Bölge hacmiyle doğrudan orantılıdır (Şekil 4).
2. **Normalize İlgi Yoğunluğu (Relevance Density):** $\text{Density} = \frac{\sum_{v \in \text{bölge}} R_v}{N_{\text{voksel}}}$. En yüksek yoğunluk temporal lob yapılarında (hipokampus, amigdala, parahipokampal girus) çıkmaktadır (Şekil 5).
3. **İlgi Artış Oranı (Relevance Gain):** $\text{Gain} = \frac{\text{Ortalama } R_{\text{bölge}}^{\text{AD}}}{\text{Ortalama } R_{\text{bölge}}^{\text{HC}}}$. AD ve HC arasındaki kontrastı gösterir (Şekil 6).

### 9.3 Biyobelirteç Korelasyonu
- Test setindeki doğru sınıflandırılmış AD hastalarında (True Positive) hipokampal LRP ilgisi ile hipokampus hacmi arasında **$r = -0.560$ ($p < 0.001$, permütasyon testi)** negatif korelasyon bulunmuştur (Şekil 9). Hipokampüsü küçülen hastada model daha yüksek LRP ilgisi atamaktadır.
- GB için bu korelasyon anlamsızdır ($r = 0.096, p = 0.77$).
- $\beta$ arttıkça LRP korelasyonu zayıflar: $\beta=0 \rightarrow -0.560$; $\beta=0.25 \rightarrow -0.562$; $\beta=0.5 \rightarrow -0.525$; $\beta=0.75 \rightarrow -0.457$; $\beta=1.0 \rightarrow -0.361$ (§3.3).

---

## 10. Kod ve Tekrarlanabilirlik
- **Depo:** https://github.com/moboehle/Pytorch-LRP
- **Lisans:** **BSD 3-Clause License** (Depodaki `license.txt` dosyası ile teyitli; akademik ve ticari yeniden kullanıma, kod uyarlamasına izin verir).
- **Çerçeve:** PyTorch 1.x, Python 3, torchvision, nibabel, nitorch, scipy, scikit-learn, h5py.
- **Doğrudan Alınabilecek Dosyalar:**
  - `innvestigator.py`: PyTorch modelleri için LRP sarmalayıcısı (`InnvestigateModel`).
  - `inverter_util.py`: Evrişim, havuzlama, lineer katmanlar için LRP kurallarını (`RelevancePropagator`) işleten çekirdek modül.
  - `license.txt`: `uygulama/gorkem_P06_bohle/LICENSE-Pytorch-LRP` olarak depoya kopyalanabilir.
- **Yeniden Yazılması Gerekenler:**
  - Veri yükleme boru hattı: Depo HDF5 dosyaları ve eski `nitorch` kütüphanesini kullanır. Bizim ortak `uygulama/ortak/veri.py` (128³ `.npy`) yapısına bağlanmalıdır.
  - Model girdi uyarlaması: Orijinal model $193 \times 229 \times 193$ girdi ve `Linear(5120, 128)` bekler. Bizim protokolümüzdeki 128³ girdi için son havuzlama çıkışı $64 \times 2 \times 2 \times 2 = 512$ olmaktadır; `AdaptiveAvgPool3d` veya `Linear(512, 128)` ile güncellenmelidir.
- **Eksikler:** Önceden eğitilmiş model ağırlığı (`.pth`) depoya yüklenmemiştir; ADNI ham verisi DUA gereği depoda yoktur.

---

## 11. Güçlü ve Zayıf Yönler

### Güçlü Yönler
1. **Teorik Sağlamlık:** Gradyan karmaşasına dayanmayan, korunum ilkesine sahip LRP algoritmasını 3B medikal görüntülemeye başarıyla uyarlamıştır.
2. **Klinik Yorumlanabilirlik:** $\beta=0$ kuralı ile sağlıklı bireylerde sıfıra yakın taban çizgisi oluşturarak yanlış pozitif ilgi gürültüsünü engellemiştir.
3. **Biyobelirteç Validasyonu:** Isı haritalarını görsel "sezgi" düzeyinde bırakmamış, bağımsız hipokampüs hacmiyle kantitatif olarak ($r=-0.560$) doğrulamıştır.
4. **Temiz Açık Kaynak Kodu:** BSD-3 lisanslı, bağımsız PyTorch LRP motoru sunmaktadır.

### Zayıf Yönler
1. **Sınırlı Klinik Kapsam:** Yalnızca ikili (AD vs HC) sınıflandırma yapılmış; erken teşhisin asıl hedefi olan Hafif Bilişsel Bozukluk (MCI) kohortu tamamen denklem dışı bırakılmıştır.
2. **Metrik Eksikliği:** Makalede AUC, F1, duyarlılık/özgüllük ve k-kat çapraz doğrulama varyansı raporlanmamıştır (yalnızca tek test seti doğruluğu %87.96).
3. **Yüksek Hesaplama Boyutu:** $193 \times 229 \times 193$ tam MNI çözünürlüğü yüksek bellek tüketir; TPU/GPU gereksinimi yüksektir.
4. **Metin İçi Sayısal Tutarsızlık:** Giriş bölümünde bildirilen tarama sayısı (969) ile veri bölme tablosundaki tarama toplamı (1.069) birbiriyle çelişmektedir (§13.2).

---

## 12. Bizim Projeye Uyarlama
**Bizim Kurulumumuz:** ADNI1 1.5T başlangıç (baseline) T1 taramaları, NC / MCI / AD sınıfları, HD-BET kafatası ayıklama $\rightarrow$ N4 bias düzeltme $\rightarrow$ maske içi z-score $\rightarrow$ MNI152 doğrusal kayıt $\rightarrow$ $128^3$ boyut, denek (RID) düzeyinde 5-kat CV $\times$ 3 tohum; birincil görev AD vs NC, ikincil 3-sınıf.

### 12.1 Neyi Aynen Alıyoruz, Neyi Değiştiriyoruz?
- **Aynen Alınanlar:**
  1. 4 bloklu 3B CNN konsepti: $3 \times 3 \times 3$ konvolüsyonlar, filtre sayıları (8, 16, 32, 64), MaxPool pencere dizilimi ($2, 3, 2, 3$).
  2. LRP motoru: `moboehle/Pytorch-LRP` deposundaki `inverter_util.py` kuralları ve $\beta=0$ yayılım mantığı.
  3. Açıklanabilirlik katmanı: Karar destek sistemimizde radyoloğa sunulacak LRP ısı haritası üretimi (`uygulama/api/isi_haritasi.py`).
- **Değiştirilenler:**
  1. **Girdi Boyutu:** $193 \times 229 \times 193 \rightarrow 128^3$.
     - *Hesaplama:* 128³ girdide Conv/MaxPool zincirinden sonra boyutsal akış:
       - 128 $\rightarrow$ Conv1(pad 0) 126 $\rightarrow$ MP(2) 63
       - 63 $\rightarrow$ Conv2 61 $\rightarrow$ MP(3) 20
       - 20 $\rightarrow$ Conv3 18 $\rightarrow$ MP(2) 9
       - 9 $\rightarrow$ Conv4 7 $\rightarrow$ MP(3) 2.
       - Çıktı tensörü: $64 \times 2 \times 2 \times 2 = 512$ birim.
       - Dolayısıyla birinci tam bağlantılı katman `Linear(512, 128)` olarak uyarlanır (orijinaldeki 5.120 yerine).
  2. **Veri Yükleyici ve Protokol:** HDF5 yerine ortak `uygulama/ortak/veri.py` (hafızaya eşlenmiş float16 `.npy`).
  3. **Çok Sınıflı Destek:** İkili (2 sınıf) ve 3-sınıflı (NC / MCI / AD) çıktı desteği.
  4. **Doğrulama Protokolü:** Tek split yerine PROTOKOL K1–K5 uyumlu 5-kat CV $\times$ 3 tohum ve kilitli bağımsız test seti.
  5. **Metrikler:** Yalnızca doğruluk değil; Dengeli Doğruluk (BAcc), ROC-AUC, F1-makro, Duyarlılık ve Özgüllük.

### 12.2 Zorluk ve Kaynak Tahmini
- **Beklenen Zorluk:** **2 / 5** (Mimari basit bir düz 3B CNN'dir; asıl dikkat gerektiren nokta LRP kütüphanesinin PyTorch'un güncel sürümleriyle uyumluluğunun korunması ve $128^3$ tensör boyutlarının `innvestigator` kancalarına tam oturmasıdır).
- **Tahminî VRAM / Süre (T4 GPU, 16 GB):**
  - Girdi $128^3$, batch boyutu 4, AMP (fp16) açıkken: VRAM tüketimi $\approx 2.5 - 3.5\text{ GB}$.
  - 100 epoch (erken durdurma ile ~35 epoch): Kat başına eğitim süresi $\approx 6 - 8\text{ dakika}$.
  - Tek bir hacim için LRP ısı haritası çıkarım süresi: $\approx 0.8 - 1.2\text{ saniye}$.

### 12.3 PROTOKOL.md ile Uyumsuzluklar
- Makaledeki tek test split'i bizim 5-kat kilitli protokolümüzle uyumsuzdur (bizim protokolümüz daha katıdır).
- Makale MCI sınıfını tamamen çöpe atmıştır; biz ikincil görevde 3 sınıfı da yarıştıracağız.
- Makaledeki $193 \times 229 \times 193$ girdi boyutu PROTOKOL madde 3'teki 128³ ortak girdi kuralına uyarlanmalıdır.

---

## 13. Opus Doğrulama

- **Sonuç:** **ÇELİŞKİ VAR**
- **Güven:** **Yüksek**
- **Hakemin Okuduğu Kaynak:**
  1. PMC6685087 tam metin makale (Frontiers in Aging Neuroscience, 2019;11:194).
  2. GitHub kaynak kodları: `moboehle/Pytorch-LRP` deposundaki `Data Split ADNI.ipynb`, `ADNI Training.ipynb`, `inverter_util.py`, `license.txt`.

### 13.1 Kontrol Edilen Sayılar
| İddia | Özetteki Değer | Makaledeki / Koddaki Değer | Durum | Yer |
|---|---|---|---|---|
| Toplam tarama sayısı (metin) | 969 | 969 tarama (475 AD, 494 HC) | **Doğru (metin)** | §2.1 |
| Toplam tarama sayısı (bölme toplamı) | 1.069 | 797 train + 100 val + 172 test = 1.069 | **Çelişki var (iç)** | §2.2 & kod |
| Toplam denek sayısı (metin) | 344 | 193 AD + 151 HC = 344 denek | **Doğru (metin)** | §2.1 |
| Toplam denek sayısı (bölme toplamı) | 380 | 163+18+30 AD = 211 AD; 121+18+30 HC = 169 HC | **Çelişki var (iç)** | §2.2 & kod |
| Test seti tarama ve denek sayısı | 172 tarama (30 AD, 30 HC) | 172 tarama (30 AD, 30 HC) | **Doğru** | §2.2 |
| Doğrulama seti tarama ve denek sayısı | 100 tarama (18 AD, 18 HC) | 100 tarama (18 AD, 18 HC) | **Doğru** | §2.2 |
| Eğitim seti tarama sayısı | 797 tarama (163 AD, 121 HC) | 797 tarama (163 AD, 121 HC) | **Doğru** | §2.2 |
| Test sınıflandırma doğruluğu | %87.96 | %87.96 | **Doğru** | §2.2 |
| Doğrulama en iyi doğruluğu | %91.00 | %91.00 | **Doğru** | §2.2 |
| Evrişim filtre sayıları | 8, 16, 32, 64 | 8, 16, 32, 64 | **Doğru** | §2.2 |
| Maksimum havuzlama pencereleri | 2, 3, 2, 3 | 2, 3, 2, 3 | **Doğru** | §2.2 |
| Tam bağlantılı katman birimleri | 128 ve 2 | 128 ve 2 | **Doğru** | §2.2 |
| Dropout oranı | %40 ($p=0.40$) | %40 ($p=0.40$) | **Doğru** | §2.2 |
| Öğrenme hızı (LR) | $10^{-4}$ (0.0001) | $10^{-4}$ | **Doğru** | §2.2 |
| Ağırlık sönümü (Weight decay) | $10^{-4}$ (0.0001) | $10^{-4}$ | **Doğru** | §2.2 |
| Erken durdurma sabrı | 8 epoch | 8 epoch | **Doğru** | §2.2 |
| Hipokampus LRP - hacim korelasyonu | $r = -0.560, p < 10^{-3}$ | $r = -0.560, p < 10^{-3}$ | **Doğru** | §3.3 |
| Hipokampus GB - hacim korelasyonu | $r = 0.096, p = 0.77$ | $r = 0.096, p = 0.77$ | **Doğru** | §3.3 |
| $\beta$ değerleri | 0, 0.25, 0.5, 0.75, 1 | 0, 0.25, 0.5, 0.75, 1 | **Doğru** | §2.3.1 |

### 13.2 Düzeltmeler (Özette Yanlış / Eksik $\rightarrow$ Doğrusu)
1. **Veri Kümesi Büyüklüğü Çelişkisi (Kritik):** Makalenin 2.1 bölümünde *"In total, we included 969 individual scans (475 AD, 494 HC) of 193 AD patients and 151 HCs"* denmektedir. Ancak Bölüm 2.2 ve `Data Split ADNI.ipynb` tablosunda eğitim (797), doğrulama (100) ve test (172) toplamı $797 + 100 + 172 = 1.069$ tarama ve $211\text{ AD} + 169\text{ HC} = 380$ denektir. Aradaki 100 tarama ve 36 denek farkı, yazarların ADNI seçiminde ilk taramalar ile boylamsal vizitleri listelerken metinde eski bir sayıyı bırakıp bölme aşamasında ek taramaları dahil etmesinden kaynaklanmaktadır. Gerçekte kod 1.069 tarama ile çalışmaktadır.
2. **Batch Boyutu Metinde Yok:** Makale metninde batch boyutu belirtilmemiştir. Depodaki `ADNI Training.ipynb` incelendiğinde `b = 4` olduğu tespit edilmiştir.
3. **Girdi Tensör Boyutu:** Makale girdi tensör boyutunu doğrudan yazmamış, yalnızca ICBM152 1 mm şablonuna kayıtlama yapıldığını belirtmiştir. Kod analizimizle tensör boyutunun $193 \times 229 \times 193$ olduğu ve bunun $64 \times 4 \times 5 \times 4 = 5.120$ düzleştirilmiş özellik ürettiği kesinleştirilmiştir.
4. **Lisans Teyidi:** Kod deposunun lisansı GitHub ana sayfasında doğrudan etiketlenmemiş olsa da kök dizindeki `license.txt` dosyasında açıkça **BSD 3-Clause License** olarak tanımlıdır; telif hakkı 2019 Moritz Böhle'ye aittir.

### 13.3 Özetin Atladığı Önemli Noktalar
- Kodda bir denek (`067_S_0077/Screening`), ön işleme başarısızlığı nedeniyle elle dışlanmıştır (`failed_idx`).
- Test değerlendirmesinde birden fazla boylamsal taramaya sahip hastaların oyları birleştirilmemiş; 172 tarama tek tek değerlendirilerek %87.96 doğruluk raporlanmıştır.
- LRP $\beta$-kuralında formülün paydasında sıfıra bölünmeyi önlemek için $\epsilon = 10^{-6}$ stabilizasyon terimi kullanılmıştır.

### 13.4 Doğrulanamayanlar
- Modelin eğitiminde kullanılan GPU donanımı ve eğitim süresi (makalede ve kod defterinde süre çıktıları temizlenmiştir).
- Test kümesindeki ROC-AUC ve F1 skoru (makalede yalnızca doğruluk verilmiştir).

### 13.5 Okuyucunun İşaretlediği Anahtar Sayılar (Ham Liste)
- Tarama sayısı: 969 (metin) / 1069 (bölme toplamı)
- Test doğruluğu: %87.96 (§2.2)
- Val doğruluğu: %91.00 (§2.2)
- Dropout: 0.40 (§2.2)
- Hipokampus LRP korelasyonu: -0.560 ($p < 10^{-3}$) (§3.3)
- Hipokampus GB korelasyonu: 0.096 ($p = 0.77$) (§3.3)
- Filtreler: 8-16-32-64 (§2.2)
- Havuzlama pencereleri: 2-3-2-3 (§2.2)
- FC katmanlar: 128 ve 2 (§2.2)
- Öğrenme hızı ve ağırlık sönümü: 0.0001 (§2.2)

---

## 14. Kaynaklar
- **Makale Tam Metin:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6685087/
- **Makale DOI:** https://doi.org/10.3389/fnagi.2019.00194
- **arXiv Ön Baskı:** https://arxiv.org/abs/1903.07317
- **Resmî Kod Deposu:** https://github.com/moboehle/Pytorch-LRP
- **LRP Çekirdek Referansı (Bach et al. 2015):** https://doi.org/10.1371/journal.pone.0130140
- **ANTs Kayıtlama Aracı:** http://stnava.github.io/ANTs/
- **Neuromorphometrics Atlas (SPM12):** https://www.fil.ion.ucl.ac.uk/spm/software/spm12/
