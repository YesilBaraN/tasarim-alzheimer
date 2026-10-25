# P11 — Qiu 2020 — FCN yama + risk haritası (brain2020)

> **Durum:** ☐ okunmadı · ☐ AI özeti hazır · ☑ Opus doğrulandı · ☐ insan okudu · ☑ implemente edildi
> **Sorumlu:** Ertuğrul Kabaoğlu · **Grup:** C · **Tam metin (ücretsiz):** https://pmc.ncbi.nlm.nih.gov/articles/PMC7296847/ (Brain 2020) · **Kod:** https://github.com/vkola-lab/brain2020 (MIT Lisansı, PyTorch)

---

## 1. Künye
- **Yazarlar:** Shengxiang Qiu, Preeti S. Joshi, Matthew I. Miller, Chonghua Xue, Xiao Zhou, Cody Karjadi, Ting Fang Alvin Ang, Rhoda Au, Vijaya B. Kolachalama.
- **Yıl / Başlık:** 2020 — *Development and validation of an interpretable deep learning framework for Alzheimer’s disease classification*.
- **Yayın Yeri:** *Brain: A Journal of Neurology*, Cilt 143, Sayı 6, Sayfalar 1920–1933, Haziran 2020.
- **DOI / PMC:** [10.1093/brain/awaa137](https://doi.org/10.1093/brain/awaa137) · PubMed Central: [PMC7296847](https://pmc.ncbi.nlm.nih.gov/articles/PMC7296847/).
- **Atıf Sayısı:** ~310 (Google Scholar / CrossRef, 2026 itibarıyla).

---

## 2. Tek paragraf özet
Qiu ve arkadaşları, 3B T1-ağırlıklı yapısal MR görüntülerinden Alzheimer hastalığı (AD) teşhisi koymak ve yüksek çözünürlüklü, nöropatolojik olarak doğrulanabilir hastalık risk haritaları üretmek amacıyla iki aşamalı bir derin öğrenme çerçevesi geliştirmiştir. İlk aşamada, $47 \times 47 \times 47$ voksellik yerel 3B yamalar üzerinde 4 evrişim bloklu bir Tam Evrişimli Ağ (FCN) eğitilmiş; tam hacim çıkarımında tam bağlantılı katmanlar $1\times1\times1$ ve $6\times6\times6$ evrişim çekirdeklerine dönüştürülerek (`dense_to_conv`), tüm beyin için tek bir ileri geçişte kesintisiz "hastalık olasılık haritası" (Disease Probability Map, DPM) elde edilmiştir. İkinci aşamada, bu risk haritalarından en yüksek riske sahip $K=200$ vokal seçilerek çok katmanlı algılayıcıya (MLP) aktarılmış ve denek bazlı nihai sınıflandırma yapılmıştır. Model, ADNI test kümesinde yalnızca MRI verisiyle $\%83.4 \pm 2.0$ doğruluk elde ederek 11 bağımsız uzman nöroloğun ortalama doğruluğunu ($\%82.3 \pm 9.4$) geride bırakmış; yaş, cinsiyet ve MMSE skoru eklendiğinde doğruluk $\%96.8 \pm 1.4$'e ve AUC $0.996$'ya yükselmiştir. Ayrıca AIBL ($\%87.0$), FHS ($\%76.6$) ve NACC ($\%81.8$) dış kohortlarında genellenebilirlik kanıtlanmış ve Framingham Kalp Çalışması'ndan (FHS) otopsi yapılmış 11 hastada modelin tahmin ettiği yüksek riskli voksellerin amiloid-$\beta$ ve nörofibriler yumak patolojileriyle mekânsal olarak örtüştüğü doğrulanmıştır.

---

## 3. Problem ve katkı
- **Çözmeye çalıştıkları problem:** 3B MRI tabanlı derin öğrenme modellerinin genellikle "kara kutu" niteliğinde olması, tüm beyin hacmi üzerinde eğitim yapıldığında yüksek bellek ve parametre yükü doğurması, dilim bazlı yöntemlerin 3B bağlamı kaybetmesi ve model kararlarının klinik/nöropatolojik zeminle doğrudan örtüştürülmesindeki zorluklar.
- **İddia ettikleri katkılar (madde madde):**
  1. **Yama tabanlı FCN ve tek geçişli DPM üretimi:** $47^3$ boyutundaki yerel alt-hacimlerle eğitilen FCN, çıkarım evresinde tam evrişimli forma dönüştürülerek tüm beyin için kaydırma penceresi döngülerine gerek kalmadan doğrudan ve yüksek çözünürlüklü hastalık olasılık haritası üretir (§2, Fig. 1).
  2. **Nörolog düzeyinde teşhis başarısı:** Yalnızca MRI verisi kullanan FCN+MLP modeli, 11 uzman nöroloğun ADNI test denekleri üzerindeki ortalama teşhis başarısını ($\%83.4$ vs $\%82.3$) geride bırakmıştır (§Results, Fig. 5A).
  3. **Çok kohortlu dış doğrulama:** Model, ADNI dışında üç bağımsız dış kohortta (AIBL, FHS, NACC; toplam 1.466 denek) test edilerek yüksek genellenebilirlik sergilemiştir (Tablo 2).
  4. **Post-mortem histopatolojik doğrulama:** 11 deneğin otopsi beyin dokularında ölçülen amiloid-$\beta$ plakları ve fosforile tau/nörofibriler yumak yoğunluklarının, modelin işaret ettiği yüksek riskli beyin bölgeleriyle korelasyon gösterdiği kanıtlanmıştır (§Neuropathological validation).

---

## 4. Veri seti ve bölme
- **Kaynak kohortlar ve denek sayıları (Tablo 1):**
  - **ADNI (Model geliştirme):** $N = 417$ denek (229 NC, 188 AD; ortanca yaş 76).
  - **AIBL (Avustralya dış test):** $N = 382$ denek (320 NC, 62 AD; ortanca yaş 72 NC, 73 AD).
  - **FHS (Framingham Heart Study dış test):** $N = 102$ denek (73 NC, 29 AD; ortanca yaş 73 NC, 81 AD).
  - **NACC (ABD ulusal dış test):** $N = 565$ denek (356 NC, 209 AD; ortanca yaş 74 NC, 77 AD).
  - **Toplam:** 4 kohortta $1.466$ denek. Ayrıca FHS kohortundan otopsi doğrulamalı 11 deneklik alt küme.
- **Bölme yöntemi:** ADNI veri seti denek (RID) düzeyinde $3:1:1$ oranında rastgele bölünmüştür: $\%60$ eğitim ($n \approx 250$), $\%20$ doğrulama ($n \approx 83$), $\%20$ test ($n \approx 84$). Dış kohortların tamamı (AIBL, FHS, NACC) kesinlikle eğitime dahil edilmemiş, tam bağımsız dış test seti olarak kullanılmıştır.
- **Sızıntı riski değerlendirmesi:** **Düşük**. Bölme kesinlikle denek düzeyindedir. Her denekten yalnızca klinik tanı tarihine en yakın (±6 ay) tek bir başlangıç 1.5T T1 taraması seçilmiştir (longitudinal tarama sızıntısı yok). Dış kohortlar model eğitiminden tamamen izole tutulmuştur.

---

## 5. Ön işleme
1. **Format:** Tüm taramalar NIfTI formatında işlenmiştir.
2. **Kayıtlama (Registration):** FSL FLIRT aracı kullanılarak MNI152 şablonuna (ICBM 2009c Nonlinear Symmetric) afin kayıtlama yapılmıştır. Başarısız kayıtlanan olgular manuel afin dönüşümle düzeltilmiştir.
3. **Yoğunluk Normalizasyonu:** $z$-skor normalizasyonu uygulanmış; $2.5$ standart sapmadan büyük vokseller $2.5$ değerine kırpılmıştır (outlier clipping).
4. **Arka Plan Temizleme:** Kafatası dışındaki arka plan vokselleri $-1$ değerine eşitlenerek homojen arka plan sağlanmıştır.
5. **Yama Örnekleme (Eğitimde):** Beyin parankimi içinden rastgele $47 \times 47 \times 47$ boyutunda alt-hacimler (yamalar) kesilmiştir.

---

## 6. Mimari
FCN ve MLP olmak üzere iki ana bileşenden oluşur:

### A) Yama FCN Mimarisi (`_FCN`)
| Blok / Katman | Girdi Boyutu | Çekirdek / Adım / Dolgu | Çıktı Boyutu | Parametre / Açıklama |
|---|---|---|---|---|
| Girdi | $1 \times 47 \times 47 \times 47$ | — | — | Tek kanal 3B yama |
| Blok 1 | $1 \times 47^3$ | Conv3D(1 $\rightarrow$ 20, $4^3$, s=1, p=0) + MaxPool3D($2^3$, s=1, p=0) | $20 \times 43^3$ | BN, LeakyReLU, Dropout(0.1) |
| Blok 2 | $20 \times 43^3$ | Conv3D(20 $\rightarrow$ 40, $4^3$, s=1, p=0) + MaxPool3D($2^3$, s=2, p=0) | $40 \times 20^3$ | BN, LeakyReLU, Dropout(0.1) |
| Blok 3 | $40 \times 20^3$ | Conv3D(40 $\rightarrow$ 80, $3^3$, s=1, p=0) + MaxPool3D($2^3$, s=2, p=0) | $80 \times 9^3$ | BN, LeakyReLU, Dropout(0.1) |
| Blok 4 | $80 \times 9^3$ | Conv3D(80 $\rightarrow$ 160, $3^3$, s=1, p=0) + MaxPool3D($2^3$, s=1, p=0) | $160 \times 6^3$ | BN, LeakyReLU, Dropout yok |
| Sınıflandırıcı | $160 \times 6^3 = 34.560$ | Linear($34.560 \rightarrow 30$) + Linear($30 \rightarrow 2$) | $2$ sınıf | Düzleştirme (eğitimde) |

### B) Tam Evrişimli Dönüşüm (`dense_to_conv`)
Tam hacim çıkarımında `classifier` katmanları 3B evrişime dönüştürülür:
- `Linear(34560, 30)` $\rightarrow$ `Conv3d(160, 30, kernel_size=6, stride=1, padding=0)`
- `Linear(30, 2)` $\rightarrow$ `Conv3d(30, 2, kernel_size=1, stride=1, padding=0)`
Bu sayede örneğin $128^3$ veya $181 \times 217 \times 181$ tam beyin hacmi verildiğinde, ağ tek seferde mekânsal olarak karşılık gelen 3B olasılık tensörü üretir.

### C) Nihai Sınıflandırıcı MLP (`_MLP_A`)
- Girdi: DPM haritasından seçilen en yüksek riskli $K=200$ voksel değeri (eşik $\ge 0.6$).
- Katmanlar: BatchNorm1d(200) $\rightarrow$ Dropout(0.5) $\rightarrow$ Linear(200 $\rightarrow$ 100) $\rightarrow$ BatchNorm1d(100) $\rightarrow$ LeakyReLU $\rightarrow$ Dropout(0.5) $\rightarrow$ Linear(100 $\rightarrow$ 2).

---

## 7. Eğitim ayarları
- **Optimizer:** Adam optimizer.
- **Öğrenme hızı:** FCN için $\eta = 10^{-4}$; MLP_A için $\eta = 10^{-2}$.
- **Batch boyutu:** FCN için 10 (yama bazlı); MLP için 8.
- **Epoch:** FCN 3.000 epoch; MLP 300 epoch.
- **Kayıp fonksiyonu:** Cross-Entropy Loss (sınıf dengeli ağırlıklandırma ile).
- **Düzenlileştirme:** Dropout ($0.1$ ara katmanlarda, $0.5$ sınıflandırıcıda), BatchNorm3D.
- **Donanım:** NVIDIA TITAN Xp / V100 GPU.

---

## 8. Sonuçlar

### Model Performans Tablosu (Makale Tablo 2)
| Model Konfigürasyonu | Test Kümesi | Doğruluk (ACC) | Duyarlılık (SEN) | Özgüllük (SPE) | F1-Skoru | MCC | Kaynak |
|---|---|---|---|---|---|---|---|
| **Yalnızca MRI (Model A)** | **ADNI test** | **0.834 ± 0.020** | **0.767 ± 0.036** | **0.889 ± 0.030** | **0.806 ± 0.024** | **0.666 ± 0.042** | Tablo 2 |
| Yalnızca MRI (Model A) | AIBL dış test | 0.870 ± 0.022 | 0.594 ± 0.119 | 0.924 ± 0.025 | 0.593 ± 0.088 | 0.520 ± 0.095 | Tablo 2 |
| Yalnızca MRI (Model A) | FHS dış test | 0.766 ± 0.064 | 0.901 ± 0.096 | 0.712 ± 0.123 | 0.692 ± 0.044 | 0.571 ± 0.056 | Tablo 2 |
| Yalnızca MRI (Model A) | NACC dış test | 0.818 ± 0.033 | 0.764 ± 0.031 | 0.849 ± 0.052 | 0.757 ± 0.033 | 0.613 ± 0.059 | Tablo 2 |
| Görüntü Dışı (Yaş, Cins, MMSE) | ADNI test | 0.957 ± 0.010 | 0.924 ± 0.019 | 0.983 ± 0.032 | 0.951 ± 0.010 | 0.915 ± 0.020 | Tablo 2 |
| **Füzyon (MRI + Klinik, Model C)** | **ADNI test** | **0.968 ± 0.014** | **0.957 ± 0.014** | **0.977 ± 0.031** | **0.965 ± 0.014** | **0.937 ± 0.026** | Tablo 2 |
| Füzyon (Model C) | AIBL dış test | 0.932 ± 0.031 | 0.877 ± 0.032 | 0.943 ± 0.042 | 0.814 ± 0.054 | 0.780 ± 0.059 | Tablo 2 |
| Füzyon (Model C) | FHS dış test | 0.792 ± 0.039 | 0.742 ± 0.185 | 0.808 ± 0.082 | 0.633 ± 0.076 | 0.517 ± 0.098 | Tablo 2 |
| Füzyon (Model C) | NACC dış test | 0.852 ± 0.037 | 0.924 ± 0.025 | 0.810 ± 0.068 | 0.824 ± 0.032 | 0.714 ± 0.053 | Tablo 2 |

- **ROC-AUC Değerleri (Füzyon):** ADNI test: 0.996, AIBL: 0.974, FHS: 0.876, NACC: 0.954 (§Abstract & §Results).
- **Klinisyen Karşılaştırması:** 11 nöroloğun ADNI test denekleri üzerindeki ortalama doğruluğu $\%82.3 \pm 9.4$ iken yalnızca MRI kullanan model $\%83.4 \pm 2.0$ ile hekimleri geçmiştir (hekimler arası uyum Cohen's $\kappa = 0.493 \pm 0.16$, orta düzey).

---

## 9. Açıklanabilirlik / ek analiz
- **Hastalık Olasılık Haritası (DPM):** FCN modelinin ürettiği vokal bazlı olasılık değerleri, AD'de belirgin olarak hipokampus, parahipokampal girus, entorinal korteks ve genişlemiş lateral ventriküllerde yoğunlaşmaktadır (Fig. 2, Fig. 3).
- **Post-Mortem Nöropatoloji Korelasyonu:** FHS otopsi serisinde (11 hasta), histopatolojik olarak boyanan amiloid-$\beta$ plakları ve nörofibriler yumak (tau) yoğunluk dereceleri (1+ ila 4+) ile modelin o bölgeye atadığı risk olasılıkları arasında anlamlı pozitif korelasyon (Spearman's $\rho$, $p < 0.05$) bulunmuştur (§Results).

---

## 10. Kod ve tekrarlanabilirlik
- **Depo:** [https://github.com/vkola-lab/brain2020](https://github.com/vkola-lab/brain2020)
- **Lisans:** **MIT Lisansı** (Kolachalama Laboratory, 2020). Depoda `LICENSE.md` mevcut.
- **Çerçeve:** PyTorch.
- **Durum:** Kod temiz, modüler ve eksiksizdir (`model.py`, `dataloader.py`, `config.json`, `main.py`). `dense_to_conv()` metodu sayesinde doğrudan tam hacim çıkarımı yapılabilir.
- **Alınacak Parçalar:** `_FCN` mimarisi ve ağırlık dönüştürme fonksiyonu doğrudan projemize adapte edilebilir.

---

## 11. Güçlü ve zayıf yönler
- **Güçlü Yönler:**
  1. Düşük bellek tüketimi: $47^3$ yamalar üzerinde eğitildiği için GPU VRAM gereksinimi düşüktür.
  2. Kaydırmasız tam hacim çıkarımı: `dense_to_conv` ile tam hacim çıkarımı çok hızlıdır.
  3. Biyolojik doğrulama: Otopsi histopatolojisiyle doğrulanmış ender derin öğrenme çalışmalarındandır.
  4. Açık kaynak kod ve MIT lisansı.
- **Zayıf Yönler:**
  1. İki aşamalı boru hattı: FCN eğitimi sonrasında DPM çıkarılıp ayrı bir MLP eğitilmesi gerekmektedir.
  2. Yama etiketlemesi: Her yamaya hastanın global etiketi verilmektedir (zayıf gözetim gürültüsü).

---

## 12. Bizim projeye uyarlama
- **Rol:** 5. implementasyon modelimiz (`uygulama/ertugrul_P11_qiu_fcn/`).
- **Uyarlama Stratejisi:**
  - Projemizin $128 \times 128 \times 128$ ön işlenmiş MNI hacimlerinden $47^3$ rastgele yamalar örneklenerek FCN eğitilir.
  - Ortak model sözleşmemize (`olustur(varyant='fcn', sinif_sayisi=2, girdi_boyut=128)`) uygun bir sarmalayıcı yazılarak, uçtan uca tek modül halinde hem yama hem tam hacim tahmini sağlanır.
  - Görselleştirme modülü (`harita.py`) ile 3 dik düzlemde (aksiyel, koronal, sagital) DPM ısı haritası üretilerek arayüze aktarılır.
- **Beklenen Zorluk:** 2/5 (Kod temiz ve PyTorch uyumlu; yama örnekleyici basit).
- **Tahminî VRAM / Süre:** 128³ tam hacimde çıkarım ~1.2 GB VRAM; eğitim yama bazlı olduğu için RTX 4060'ta rahatlıkla koşar (~1 saat).

---

## 13. Opus doğrulama
- **Sonuç:** **ÇELİŞKİ YOK**
- **Kontrol edilen sayılar ve kaynakları:**
  1. ADNI denek sayısı: $N = 417$ (NC: 229, AD: 188) (Tablo 1). **Doğru.**
  2. Dış kohort denek sayıları: AIBL $N = 382$ (320 NC, 62 AD), FHS $N = 102$ (73 NC, 29 AD), NACC $N = 565$ (356 NC, 209 AD); toplam $1.466$ denek (Tablo 1). **Doğru.**
  3. Otopsi kohortu: FHS 11 denek (4 doğrulanmış AD) (§Neuropathological validation). **Doğru.**
  4. Yalnızca MRI modeli sonuçları (Tablo 2): ADNI test ACC $0.834 \pm 0.020$, SEN $0.767 \pm 0.036$, SPE $0.889 \pm 0.030$, F1 $0.806 \pm 0.024$, MCC $0.666 \pm 0.042$. **Birebir doğru.**
  5. AIBL MRI sonuçları (Tablo 2): ACC $0.870 \pm 0.022$, SEN $0.594 \pm 0.119$, SPE $0.924 \pm 0.025$. **Birebir doğru.**
  6. FHS MRI sonuçları (Tablo 2): ACC $0.766 \pm 0.064$, SEN $0.901 \pm 0.096$, SPE $0.712 \pm 0.123$. **Birebir doğru.**
  7. NACC MRI sonuçları (Tablo 2): ACC $0.818 \pm 0.033$, SEN $0.764 \pm 0.031$, SPE $0.849 \pm 0.052$. **Birebir doğru.**
  8. Füzyon modeli ADNI test (Tablo 2): ACC $0.968 \pm 0.014$, AUC $0.996$. **Birebir doğru.**
  9. Nörolog grubu başarısı: 11 nörolog, ortalama ACC $0.823 \pm 0.094$, Cohen's $\kappa = 0.493 \pm 0.16$ (§Results). **Birebir doğru.**
  10. Yama boyutu: $47 \times 47 \times 47$ vokseller (Fig. 1, config.json). **Doğru.**
  11. MLP_A parametresi: $K=200$ vokseller, eşik $0.6$ (config.json). **Doğru.**
  12. Lisans: MIT (repo `LICENSE.md`). **Doğru.**
- **Güven düzeyi:** Yüksek (Tam metin PMC XML ve resmî GitHub deposu kaynak kodları karşılaştırılarak doğrulandı).

---

## 14. Kaynaklar
1. Qiu S. et al., *Brain*, 143(6): 1920–1933, 2020: https://pmc.ncbi.nlm.nih.gov/articles/PMC7296847/
2. Kolachalama Lab GitHub Repo: https://github.com/vkola-lab/brain2020
3. ICBM 2009c Nonlinear Symmetric Template: https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009
