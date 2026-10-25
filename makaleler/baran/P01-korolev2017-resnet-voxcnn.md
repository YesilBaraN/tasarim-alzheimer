# P01 — Korolev 2017 — ResNet ve VoxCNN ile 3B beyin MRI sınıflandırma

> **Durum:** ☐ okunmadı · ☑ AI özeti hazır · ☑ Opus doğrulandı (**ÇELİŞKİ VAR**, güven: yüksek) · ☐ insan okudu · ☐ implemente edildi
> **Sorumlu:** Baran Yeşilyurt · **Grup:** A · **Tam metin (ücretsiz):** https://arxiv.org/abs/1701.06643 · **Kod:** https://github.com/neuro-ml/resnet_cnn_mri_adni (lisans yok, Theano — yalnız referans)
> **AI okuma kaynağı:** Okunan: https://arxiv.org/html/1701.06643v1 (arXiv HTML; tam metin, bölümler 1-5, Tablo 1, Şekil 1-3 özetlendi), https://arxiv.org/abs/1701.06643 (künye/özet), GitHub https://github.com/neuro-ml/resnet_cnn_mri_adni (ana sayfa, scripts/ klasör listesi, Dockerfile). Okunamayan: arxiv.org/pdf/1701.06643 ve v1 (WebFetch ikili PDF döndürdü, metin çıkmadı). UYARI: HTML sayfası küçük bir model aracılığıyla özetlendi; HTML'de bazı rakamlar çiftlenmiş (ör. "27∗10−6", "55", "150150"), bu yüzden LR/batch/epoch değerleri orijinal PDF ile (doğrulanamadı) teyit edilmeli. Kernel boyutları, VoxCNN filtre sayıları ve parametre sayısı metinde bulunamadı. Okunmayan kod dosyaları: utils.py, *_train.ipynb içerikleri, requirements.txt, lisans.

> ⚠ **Nasıl okunmalı:** §2–§12 Sonnet okuyucunun özetidir; §13 Opus hakeminin makaleye karşı denetimidir. §13'te "yanlış" işaretli her sayı için **makaledeki değer** geçerlidir; §13'teki düzeltmeler §4–§8'in üstünde okunur. Hiçbir ajan makalenin yerine geçmez: implementasyondan önce ilgili bölümü (§6, §7) makaleden bir kez daha kendin oku.

## 1. Künye
Korolev S., Safiullin A., Belyaev M., Dodonova Y. (2017). Residual and Plain Convolutional Neural Networks for 3D Brain MRI Classification. IEEE ISBI 2017, s. 835–838. arXiv:1701.06643 (cs.CV, 23 Ocak 2017, yalnız v1). Kurumlar: Skoltech ve IITP (Rusya). Kod: github.com/neuro-ml/resnet_cnn_mri_adni.

## 2. Tek paragraf özet
Makale, 3B beyin sMRI'sından Alzheimer sınıflandırmasının elle çıkarılmış özellik, otokodlayıcı ön eğitimi veya çok adımlı boru hattı olmadan, doğrudan 3B CNN ile yapılıp yapılamayacağını sınar. İki mimari karşılaştırılır: VGG tarzı düz ağ VoxCNN ve VoxResNet'ten türetilmiş, 21 katmanlı, altı VoxRes bloklu artık ağ ResNet (§2.1-2.2, Şekil 1). Veri, ADNI'nin hazır "Spatially Normalized, Masked and N3 corrected T1" görüntüleridir; her denekten yalnızca ilk tarama alınarak toplam 231 görüntü (AD 50, LMCI 43, EMCI 77, NC 61) kullanılır, girdi 110×110×110'dur (§3). Altı ikili görev 5-kat CV ile (5 farklı bölmeyle tekrar) değerlendirilir (§2.3). AD vs NC'de AUC ≈ .87-.88 ve doğruluk ≈ .79-.80 elde edilir; ara sınıflı görevlerde AUC .47-.67 aralığında, yani şansa yakındır (Tablo 1). İki ağ standart sapma içinde eşdeğerdir. Güçlü yanı sadeliği ve özellik mühendisliği gerektirmemesidir; zayıf yanı küçük örneklem, yüksek varyans ve eksik mimari ayrıntılardır. Okuyucu notu: bu çalışma bizim projede temel (baseline) mimari referansıdır; mutlak sayılar çok küçük ve ön işlenmiş bir veriden gelir.

## 3. Problem ve katkı
- **Problem:** ADNI sMRI'dan AD/MCI/NC ayrımını, çok adımlı özellik çıkarma (RBM, otokodlayıcı, yama örnekleme) olmadan uçtan uca 3B CNN ile yapmak.
- **Katkı 1:** Basit bir düz 3B CNN (VoxCNN) ve bir 3B artık ağ (ResNet) ile, ön eğitimsiz, benzer sonuçlar alınabildiğini göstermek (§1, §5).
- **Katkı 2:** Sınıf dengeli mini-batch (her batch'te her sınıftan örnek) önerisi; rastgele batch'te tek sınıf çıkma olasılığı 1/c^b (§2.3).
- **Katkı 3:** Altı ikili görevle (AD/EMCI/LMCI/NC) önceki çalışmalarla karşılaştırılabilir bir sonuç tablosu (Tablo 1).
- **Katkı 4:** Oklüzyon tabanlı dikkat haritaları (7×7×7 kutu, Şekil 3); hipokampüs ve ventriküllerle örtüştüğü söylenir ama bulanıktır.
- **Gelecek iş:** hizalanmamış/kafatası ayıklanmamış görüntüler için global pooling ile öteleme değişmezliği (§5).

## 4. Veri seti ve bölme
- **Kaynak:** ADNI, "Spatially Normalized, Masked and N3 corrected T1 images" (§3).
- **Denek/tarama:** Her denekten yalnızca ilk tarama; toplam 231 görüntü (231 denek varsayımı, doğrulanamadı) (§3).
- **Sınıf dağılımı:** AD 50, LMCI 43, EMCI 77, NC 61 (§3).
- **Görevler:** 6 ikili görev (AD-NC, AD-EMCI, AD-LMCI, LMCI-NC, LMCI-EMCI, EMCI-NC); görev başına örnek sayıları verilmemiş.
- **Bölme/CV:** 5-kat CV, 5 farklı kat bölmesiyle tekrar (§2.3); denek düzeyi mi olduğu açıkça yazılmasa da tek tarama/denek nedeniyle sızıntı kontrolü sağlanır.
- **Dış test:** Yok; ayrı bir held-out test kümesi anlatılmamış, metrikler doğrulama katlarından (doğrulanamadı).
- **Epoch seçimi:** Doğrulama metriklerinin durağanlaşmasına bakılarak sabit epoch (§2.3) — doğrulama kümesiyle ayar yapıldığı için iyimser sapma olasılığı.

**Sızıntı riski (AI):** orta — İyi yanı: yalnızca ilk tarama kullanılarak aynı denekten çoklu görüntü sızıntısı engellenmiş (§3). Riskler: ayrı test kümesi yok; epoch sayısı eğitim/doğrulama eğrilerine bakılarak seçilmiş ve raporlanan sayılar doğrulama katlarından görünüyor (§2.3, Şekil 2); katman/filtre/dropout "deneylerle seçilmiş" ama hangi veriyle seçildiği belirtilmemiş; ADNI'nin N3+uzamsal normalizasyon ön işleme çıktısı kullanıldığı için tekrar üretilebilirlik kısmen dış kaynağa bağlı. Kesin bir sızıntı kanıtı yok, bu yüzden orta.

## 5. Ön işleme
- ADNI'nin hazır işlenmiş "Spatially Normalized, Masked and N3 corrected T1" görüntüleri: uzamsal normalizasyon (hizalama), kafatası maskeleme ve N3 yanlılık düzeltmesi önceden yapılmış (§3).
- Girdi boyutu 110×110×110 (§3); yeniden örnekleme ayrıntısı yok (doğrulanamadı).
- Yoğunluk normalizasyonu raporlanmamış; veri artırma / oversampling anlatılmamış.
- Gelecek iş olarak hizalama ve kafatası ayıklama gerektirmeyen yaklaşım önerilir (§5).

## 6. Mimari
**Girdi:** 110×110×110×1 (§3). Parametre sayısı raporlanmamış (doğrulanamadı). Kernel boyutları metinde yok (doğrulanamadı; VoxResNet'te 3×3×3 kullanılır, makaleden teyit edilmedi).

**VoxCNN (§2.1, Şekil 1a):**

| Katman/Blok | Çekirdek | Kanal | Çıktı | Not |
|---|---|---|---|---|
| 4 hacimsel konv. bloğu | (doğrulanamadı) | artan (sayılar doğrulanamadı) | (doğrulanamadı) | VGG tarzı, filtre sayısı katmanla artar |
| 2 "deconvolutional" (tam bağlı benzeri) katman | (doğrulanamadı) | (doğrulanamadı) | (doğrulanamadı) | BatchNorm + Dropout |
| Softmax | - | 2 | 2 | ikili sınıflandırma |

**ResNet (§2.2, Şekil 1b):**

| Katman/Blok | Çekirdek | Kanal | Çıktı | Not |
|---|---|---|---|---|
| 6 VoxRes bloğu (toplam 21 katman) | (doğrulanamadı) | ilk 4 blok 64, son 2 blok 128 | - | Kimlik (identity) kısa yolları |
| Bloklar arası konv. | stride 2×2×2 | - | uzamsal boyut azalır | |
| Son blok çıktısı pooling | - | 128 | 2×2×2×128 | |
| FC | - | 128 gizli birim | 128 | |
| Softmax | - | 2 | 2 | |

Katman sayıları, filtre sayıları, pooling boyutları ve dropout "deneylerle seçildi" denir ama nihai değerlerin çoğu raporlanmamış (§2).

## 7. Eğitim ayarları
- **VoxCNN:** Adam, ~~LR 2×10⁻⁶~~ → **DÜZELTME (Opus §13.2): LR 27×10⁻⁶ = 2.7×10⁻⁵** (makale §2.1 alttext "27·10⁻⁶", depo kodu `_lr=0.000027`), batch 5, 150 epoch.
- **Depodan okunan ek ayrıntı (Opus §13.2):** VoxCNN 4 blok, filtre 8-16-32-64, 3³ valid konv, blok başına 2-2-3-3, MaxPool(2); Dense128 → BN → Dropout 0.7 → Dense64 → Softmax. ResNet: 32-filtreli kök, pool 7, dropout yok; depo kodu LR 1e-3 (makale 1e-4 — çelişki). Yoğunluk: hacim / max.
- **ResNet:** Nesterov momentum, LR 10⁻⁴, batch 3, 70 epoch (§2.2).
- **Sınıf dengeli batch:** her batch'te tüm sınıflardan örnek (§2.3).
- **CV:** 5-kat, 5 farklı bölmeyle tekrar (§2.3).
- **Epoch:** görev başına sabit; eğitim altkümesinde neredeyse mükemmel ayrım ve doğrulama metriklerinin durağanlaşması esas (§2.3). Şekil 2: ResNet AD-NC doğrulama AUC ~50. epoch sonrası plato.
- **Erken durdurma, veri artırma, ağırlık sönümü:** raporlanmamış.
- **Donanım ve süre:** raporlanmamış (Dockerfile CUDA 7.5/cuDNN 5, yani 2016 dönemi NVIDIA GPU, model belirtilmemiş).

## 8. Sonuçlar
| Görev | Metrik | Değer (VoxCNN / ResNet) | Test seti | Kaynak |
|---|---|---|---|---|
| AD vs NC | AUC | .88±.08 / .87±.07 | CV doğrulama katları | Tablo 1 |
| AD vs NC | Doğruluk | .79±.08 / .80±.07 | CV | Tablo 1 |
| AD vs EMCI | AUC / Doğruluk | .66±.11, .64±.07 / .67±.13, .63±.09 | CV | Tablo 1 |
| AD vs LMCI | AUC / Doğruluk | .61±.12, .62±.08 / .62±.15, .59±.11 | CV | Tablo 1 |
| LMCI vs NC | AUC / Doğruluk | .67±.13, .63±.10 / .65±.11, .61±.10 | CV | Tablo 1 |
| LMCI vs EMCI | AUC / Doğruluk | .47±.09, .56±.11 / .52±.11, .52±.09 | CV | Tablo 1 |
| EMCI vs NC | AUC / Doğruluk | .57±.12, .54±.09 / .58±.09, .56±.07 | CV | Tablo 1 |

Not: 3-sınıf sonucu, F1, duyarlılık, özgüllük raporlanmamış. Karşılaştırma için alıntılanan Suk ve ark.: doğruluk .95/.85/.76, AUC .99/.88/.75 (AD-NC / MCI-NC / MCI-C vs MCI-NC) — farklı protokol, MRI+PET (§1). Hosseini-Asl: AUC "over .96".

## 9. Açıklanabilirlik / ek analiz
Oklüzyon (occlusion) duyarlılığı: 7×7×7'lik kutuyla görüntü örtülüp çıktı değişimi ölçülür (ref 11 yöntemi). Şekil 3, bir NC deneği için yüksek dikkat bölgelerinin AD'den etkilenen alanlara (esas olarak hipokampüs ve ventriküller) "benzediğini" söyler; haritalar bulanıktır, nicel doğrulama yoktur. Şekil 2 yalnızca öğrenme eğrisidir. Grad-CAM yok; yalnız bir denekle nitel gösterim.

## 10. Kod ve tekrarlanabilirlik
- **Depo:** github.com/neuro-ml/resnet_cnn_mri_adni, master dalı, 3 commit.
- **Lisans:** LICENSE dosyası yok (görevdeki bilgiyle uyumlu; sayfada lisans görünmedi) — yasal olarak "tüm hakları saklıdır" sayılır, kod KOPYALANMAZ, yalnız okunur.
- **Çerçeve:** Theano (`.theanorc` ve görevdeki bilgi; Dockerfile CUDA 7.5 + cuDNN 5 tabanlı, Python 3, Jupyter).
- **Dosyalar:** `scripts/` (resnet_train.ipynb, vgg_like_train.ipynb, utils.py, resnet_plot_results.ipynb, vgg_like_plot_results.ipynb, resnet_plot_heatmap.ipynb, requirements.txt, README.md, data/), `jupyter/`, `test_scripts/`, Dockerfile, .theanorc.
- **Veri biçimi:** `.nii` dosyaları + `metadata.csv` (Label, Path sütunları).
- **Eksikler:** eğitilmiş ağırlık yok, ADNI verisi yok, lisans yok; Theano/CUDA 7.5 bugün çalıştırması zor. İçerikler (utils.py, defterler) okunmadı (doğrulanamadı).

## 11. Güçlü ve zayıf yönler
**Güçlü:** Basit, ön eğitimsiz, uçtan uca; iki mimari karşılaştırması; sınıf dengeli batch fikri; tek tarama/denek; 5×5-kat tekrarlı CV ve SD raporu; AD-NC için makul sonuç.

**Zayıf:** Yalnızca 231 görüntü; sonuçlar geniş SD (±.15'e kadar); ara sınıflar şansa yakın (LMCI-EMCI VoxCNN AUC .47); ayrı test seti yok; mimari ayrıntılar eksik (kernel, filtre, dropout, parametre sayısı); veri artırma/yoğunluk normalizasyonu yok; ön işlem hazır ADNI çıktısına bağlı; donanım/süre yok; atıf yapılan SOTA ile eşit koşulda karşılaştırma yok; kod lisanssız ve eski Theano; yalnız ikili görevler, 3-sınıf yok.

## 12. Bizim projeye uyarlama
Kurulumumuz: ADNI1 1.5T başlangıç T1, NC/MCI/AD, HD-BET → N4 → z-score → MNI152 afin → 128³, RID düzeyinde 5-kat CV × 3 tohum, birincil görev AD-NC, ikincil 3-sınıf.

### 12.1 Okuyucunun uyarlama notu
**Aynen alınabilecek:** ResNet'in iskeleti (6 VoxRes bloğu; 64→128 kanal; stride-2 geçişler; 2×2×2×128 pooling + FC128 + softmax), VoxCNN'in 4 blok + BN/Dropout yapısı (kernel/filtre sayısı belirsiz, tahmini 3×3×3 ve 32-64-128-256 olarak biz seçeriz), sınıf dengeli batch, Adam/Nesterov ve makaledeki LR'ler başlangıç noktası, 5-kat CV, oklüzyon haritası.

**Değiştirilecek:**
- Girdi 110³ yerine 128³ (ADNI1 1.5T, HD-BET + N4 + z-score + MNI152NLin2009cAsym afin).
- Theano yerine PyTorch + MONAI (ResNet için `monai.networks.nets.resnet`/özel VoxRes bloğu yazılır; kod kopyalanmaz, lisanssız).
- RID düzeyinde bölme, 5-kat × 3 tohum; denek başına tek baseline tarama (makaledeki ilk tarama ile uyumlu).
- Sınıflar NC/MCI/AD (≈229/382/187); EMCI/LMCI ayrımı yok. Birincil AD vs NC, ikincil 3-sınıf (makalede 3-sınıf yok, yeni).
- Metrikler: dengeli doğruluk, AUC, F1-makro, duyarlılık, özgüllük eklenmeli (makale yalnız AUC ve doğruluk).
- Epoch seçimini doğrulama katında değil, iç doğrulama kümesi + erken durdurma ile yapıp dış katı yalnız bir kez değerlendirme (sızıntıyı önlemek için, makaleden farklı).
- Veri artırma (hafif afin/gürültü), karma duyarlılık (AMP), global average pooling denenebilir.

**Zorluk:** 2/5 (mimari basit, ayrıntılar eksik olduğundan kernel/filtre seçimi bize kalır).

**VRAM/süre (tahmin, ölçülmedi):** 128³, batch 3-5, ResNet ~1-2M parametre varsayımı ile AMP kullanılırsa T4 16 GB'a rahat sığmalı (~6-10 GB tahmini; AMP'siz batch 5 sınırda olabilir). ~800 görüntü, 5-kat×3 tohum, 70-150 epoch için toplam yaklaşık 15-40 GPU saati tahmini; Kaggle/Colab oturum limitleri için kat başına checkpoint gerekir.

**Protokole uymayan noktalar:** ön işlem boru hattı farklı (hazır ADNI N3 vs bizimki), girdi boyutu, sınıf tanımı, test seti yok, makale sonuçları (AD-NC ~%79-80) bizim hedef ≥%85 ile doğrudan kıyaslanamaz.

### 12.2 Hakemin kurulum farkı analizi
Sızıntı değerlendirmesi: 'orta' derecesine katılıyorum, gerekçeyi güçlendirerek: denekler arası sızıntı yok (denek başına tek tarama, açıkça belirtilmiş); ama model seçimi sızıntısı var — epoch ve hiperparametreler, raporlanan aynı CV katlarının doğrulama eğrilerinden seçilmiş, kodda iç doğrulama yok. Bu, tahmini birkaç puan iyimser yapar; kesin veri sızıntısı olmadığı için 'yüksek' değil.

Somut farklar ve beklenen etki:
1) Veri alt kümesi: makale 231 görüntü, 4 sınıf (AD 50/LMCI 43/EMCI 77/NC 61), muhtemelen ADNI1+GO/2 karışık (EMCI sınıfı ADNI GO/2'ye özgü); biz ADNI1 1.5T baseline, NC/MCI/AD ≈229/382/187 (~800 denek). AD vs NC için bizde ~416 denek var, makalenin ~3.7 katı → daha düşük varyans, büyük olasılıkla daha yüksek ve daha kararlı AUC/doğruluk. 1.5T tek faz daha homojen, ama ADNI1'de çok merkezli tarayıcı farkı sürüyor.
2) Görev: makalenin AD-NC görevi doğrudan karşılaştırılabilir; 3-sınıf (NC/MCI/AD) makalede yok. Makalenin LMCI-NC (.65-.67 AUC) ve EMCI-NC (.57-.58) sonuçları, bizim MCI sınıfının (EMCI+LMCI benzeri heterojen) NC ve AD'den zor ayrılacağını öngörür → 3-sınıf dengeli doğrulukta ~%50-60 bandı gerçekçi beklenti.
3) Girdi boyutu: 110³ → 128³. ResNet'te pool 7 sabit bırakılırsa çıkış boyutu değişir (128→64→32→16, pool7 → 2×2×2 yine ama artık kenar kırpılır); VoxCNN'de valid konvlarla son harita 1³ yerine farklı olur ve Dense girişi değişir. AdaptiveAvgPool3d ile çözülmeli. Bellek ~(128/110)³≈1.6 kat artar.
4) Ön işleme: makale ADNI'nin hazır N3 + uzamsal normalizasyon + maske çıktısını ve hacim başına max-ölçeklemeyi kullanıyor; biz HD-BET + N4 + maske içi z-score + MNI152NLin2009cAsym afin. Yalnız afin (makalede normalizasyonun tipi belirsiz) bazı anatomik varyansı bırakır; z-score max-ölçeklemeden daha sağlam. Net etki küçük-orta; ön işleme farkı sonuç farkının bir kısmını açıklar, kıyasta belirtilmeli.
5) Bölme: makale StratifiedKFold 5×5 (denek=görüntü), iç doğrulama yok; biz RID düzeyinde 5-kat × 3 tohum + iç doğrulama ile erken durdurma → daha dürüst, makaleye göre birkaç puan daha düşük çıkabilecek ama yayınlanabilir tahmin.
6) Metrikler: makale yalnız AUC + doğruluk (dengesizlik zaten küçük); bizde AD:NC ≈ 187:229 ve 3-sınıfta MCI baskın → dengeli doğruluk ve F1-makro şart; sınıf dengeli örnekleyici (makalenin batch fikri) MCI baskınlığı için daha önemli.
7) Hedef: makale AD-NC doğruluk ~%79-80; bizim ≥%85 hedefi, daha büyük veri + daha iyi ön işleme + augmentation ile ulaşılabilir ama yalnız mimariyi kopyalamakla garanti değil; makale rakamı alt sınır referansıdır, doğrudan kıyas değil.
8) Çerçeve/donanım: Theano/Lasagne (CUDA 7.5) → PyTorch + MONAI, T4 16 GB; Lasagne varsayılanları (He/Glorot başlatma, BN momentum, valid padding) PyTorch'tan farklı, birebir sayısal yeniden üretim beklenmemeli.

### 12.3 İmplementasyon yapılacaklar (hakem)
1) Depodan KOD KOPYALANMAZ (lisans yok); yalnız scripts/vgg_like_train.ipynb ve scripts/resnet_train.ipynb içindeki build_net, run_cross_validation ve iterate_minibatches mantığı okunup PyTorch'ta sıfırdan yazılır. Makale (arXiv:1701.06643) ve defterlerin hangi satırına dayandığı kod yorumunda atıf olarak belirtilir.
2) VoxCNN (torch.nn ile özel modül): 4 blok, filtre 8-16-32-64, Conv3d k=3 (makaleye sadık için padding=0), blok başına 2-2-3-3 konv, son konvdan sonra ReLU, MaxPool3d(2); ardından AdaptiveAvgPool3d(1) veya Flatten (128³'te boyutu hesaplayıp kontrol et) → Linear(→128) → BatchNorm1d → Dropout(0.7) → Linear(128→64) → Linear(64→n_sınıf). Optimizer Adam, lr=2.7e-5 (DİKKAT: 2e-6 değil), batch 5, 150 epoch üst sınır.
3) ResNet/VoxResNet (özel modül; MONAI'nin monai.networks.blocks.Convolution / ResidualUnit yapı taşları kullanılabilir, ama monai.networks.nets.resnet bottleneck/ImageNet tarzı olduğu için 'birebir VoxResNet' değildir): kök 2×Conv3d(32,k3,pad1)+BN+ReLU → Conv3d(64,k3,s2) → 2×VoxRes(64) → Conv3d(64,s2) → 2×VoxRes(64) → Conv3d(128,s2) → 2×VoxRes(128) → AdaptiveAvgPool3d(2) (110³'teki 2×2×2×128 çıktısını 128³'te korur) → Linear(1024→128) → Linear(128→n_sınıf). VoxRes = BN→ReLU→Conv3³→BN→ReLU→Conv3³ + kimlik. Optimizer SGD(nesterov=True, momentum=0.9); LR için hem makaledeki 1e-4 hem koddaki 1e-3 kısa bir iç-doğrulama taramasıyla denenir, seçim kaydedilir. Batch 3, 70 epoch üst sınır.
4) Veri hattı (MONAI): LoadImaged → EnsureChannelFirstd → (ön işlenmiş 128³ MNI hacimleri) → maske içi z-score zaten yapılmışsa NormalizeIntensityd atlanır → augment için RandAffined(küçük döndürme/ölçek), RandGaussianNoised, RandFlipd YOK (sol-sağ asimetri tartışmalı, açılacaksa ayrı deney). CacheDataset/PersistentDataset ile disk I/O azaltılır.
5) Sınıf dengeli batch: torch.utils.data.WeightedRandomSampler veya her batch'e her sınıftan örnek koyan özel BatchSampler (makale §2.3 fikri; ResNet batch 3 ile 3-sınıfta her batch'te her sınıf birer örnek).
6) Bölme: denek (RID) düzeyinde StratifiedGroupKFold(n_splits=5), 3 tohum; her dış katın eğitim kısmından %15-20 iç doğrulama ayrılır; epoch seçimi/erken durdurma (sabır ~20) yalnız iç doğrulamada; dış kat yalnız bir kez değerlendirilir (makalenin model-seçimi sızıntısını tekrarlama). Denek başına yalnız baseline tarama.
7) Bellek/süre: torch.cuda.amp (autocast + GradScaler) aç; 128³ ResNet'te 32 kanallı tam çözünürlüklü kök en pahalı kısımdır, batch 3 sığmazsa gradient checkpointing veya gradient birikimi kullan. Kaggle/Colab için her kat+tohum sonunda checkpoint ve metrik JSON'u kaydedilir, yeniden başlatmada kalan katlardan devam edilir.
8) Metrikler: her dış katta dengeli doğruluk, ROC AUC (3-sınıfta one-vs-rest makro), F1-makro, duyarlılık, özgüllük; 15 koşunun ortalama±SD'si ve makalenin Tablo 1 AD-NC değeri (.87-.88 AUC, .79-.80 doğruluk) yan yana, 'farklı protokol' notuyla raporlanır.
9) Açıklanabilirlik: makaleye paralel olarak 7×7×7 kutu oklüzyon haritası (MONAI monai.visualize.OcclusionSensitivity, mask_size=7) + ek olarak monai.visualize.GradCAM; nitel tek denek yerine AD sınıfı ortalaması ve hipokampüs/ventrikül atlas bölgeleriyle nicel örtüşme verilir.
10) Sanity check: önce makale ayarlarıyla (110³'e kırpılmış/yeniden örneklenmiş girdi, 5-fold, AD-NC) küçük bir çalıştırma yapılıp AUC ~.85+ bandına gelindiği görülür; sonra 128³ ve tüm iyileştirmeler açılır — böylece farkın mimariden mi ön işlemeden mi geldiği ayrılır.

## 13. Opus doğrulama
- **Sonuç:** **ÇELİŞKİ VAR** · **Güven:** yüksek
- **Hakemin okuduğu kaynak:** Okunan: https://arxiv.org/html/1701.06643v1 (tam metin; WebFetch ile iki ayrı hedefli sorguyla §2.1-2.3, §3, Tablo 1, giriş alıntıları ve şekil başlıkları okundu; LaTeX alttext'i de istendi). Doğrulama için kod da okundu: https://raw.githubusercontent.com/neuro-ml/resnet_cnn_mri_adni/master/scripts/vgg_like_train.ipynb ve .../scripts/resnet_train.ipynb (yalnız okundu, kopyalanmadı). Künye/sayfa aralığı WebSearch ile DBLP kaydından teyit edildi (ISBI 2017: 835-838). Okunamayan: https://arxiv.org/pdf/1701.06643 (WebFetch ikili akış döndürdü; yerel PDF render aracı da yok). Not: HTML'de matematik ifadeleri "görünen metin + alttext" olarak çiftleniyor ("55"=5, "150150"=150, "33"=3); öğrenme hızının alttext'i "27*10^{-6}" olup kodla (_lr=0.000027) birebir uyuşuyor.

### 13.1 Kontrol edilen sayılar
| İddia | Özetteki değer | Makaledeki değer | Durum | Yer |
|---|---|---|---|---|
| Toplam görüntü sayısı | 231 | 231 görüntü, dört sınıf | **doğru** | §3 |
| AD / LMCI / EMCI / NC sayıları | 50 / 43 / 77 / 61 | 50 AD, 43 LMCI, 77 EMCI, 61 NC | **doğru** | §3 |
| Girdi boyutu | 110×110×110 | 110×110×110 (kodda da InputLayer (None,1,110,110,110)) | **doğru** | §3 |
| AD vs NC AUC VoxCNN / ResNet | .88±.08 / .87±.07 | .88±.08 / .87±.07 | **doğru** | Tablo 1 |
| AD vs NC doğruluk VoxCNN / ResNet | .79±.08 / .80±.07 | .79±.08 / .80±.07 | **doğru** | Tablo 1 |
| LMCI vs EMCI VoxCNN AUC | .47±.09 | .47±.09 | **doğru** | Tablo 1 |
| ResNet katman ve blok sayısı | 21 katman, 6 VoxRes bloğu | 21 katman, altı VoxRes bloğu | **doğru** | §2.2 |
| ResNet filtreler / pooling / FC | ilk 4 blok 64, son 2 blok 128; çıkış pooling 2×2×2×128; FC 128 | VoxRes blokları 64 filtre, son ikisi 128; son blok çıkışı pooling ile 2×2×2×128; 128 gizli birimli FC + softmax | **doğru** | §2.2 |
| VoxCNN LR / batch / epoch / optimizer | 2×10⁻⁶ / 5 / 150 / Adam | 27×10⁻⁶ (=2.7×10⁻⁵) / 5 / 150 / AdaM — HTML alttext '27*10^{-6}', kodda _lr=0.000027, batchsize=5, num_epochs=150 | **yanlış** | §2.1 |
| ResNet LR / batch / epoch / optimizer | 10⁻⁴ / 3 / 70 / Nesterov momentum | 10⁻⁴ / 3 / 70 / Nesterov momentum (NOT: depodaki resnet_train.ipynb LR=0.001 kullanıyor; makale ile kod çelişiyor) | **doğru** | §2.2 |
| CV düzeni | 5-kat, 5 farklı bölmeyle tekrar | 5-fold CV, 5 farklı kat bölmesi (kodda StratifiedKFold, 25 koşu) | **doğru** | §2.3 |
| Oklüzyon kutusu | 7×7×7 (yer: Şekil 3) | 7×7×7 kutu; değer şekil başlığında değil, sonuç/görselleştirme metninde geçiyor (Şekil 3 bu yöntemin çıktısı) | **doğru** | Görselleştirme paragrafı (metin), Şekil 3'e atıf |
| ResNet AD-NC AUC platosu | ~50. epoch sonrası | Şekil 2 yalnız 'ROC AUC plot for AD vs Normal classification of ResNet' başlığıyla var; plato epoch'u metinde yazılı değil, grafikten okunamadı | **doğrulanamadı** | Şekil 2 |
| Atıf: Suk ve ark. doğruluk / AUC | .95/.85/.76; AUC .99/.88/.75 | .95, .85, .76 doğruluk; .99, .88, .75 ROC AUC (AD/NC, MCI/NC, MCI-C/MCI-NC) | **doğru** | §1 |
| Sayfa aralığı | 835–838 | ISBI 2017: 835-838 (DBLP) | **doğru** | künye (DBLP) |

### 13.2 Düzeltmeler (özette yanlış/eksik → doğrusu)
- Eğitim/anahtar sayılar: 'VoxCNN: Adam, LR 2×10⁻⁶' YANLIŞ → 'VoxCNN: Adam, LR 27×10⁻⁶ (2.7×10⁻⁵), batch 5, 150 epoch' (§2.1; HTML alttext 27*10^{-6}, kod _lr=0.000027). Çiftlenme yalnız 5/150'de değil, LR'de de '27' gerçek değerdir; ilk rakamı alıp '2' yazmak hata.
- Mimari (VoxCNN tablosu): makale ayrıntı vermiyor ama depo ayrıntıyı veriyor; 'doğrulanamadı' hücreleri şöyle doldurulabilir (kaynak: vgg_like_train.ipynb): 4 blok, filtreler 8-16-32-64, çekirdek 3×3×3 (padding'siz), blok başına 2-2-3-3 konv, her blok sonunda 2×2×2 max-pool; ardından Dense 128 + BatchNorm + Dropout p=0.7 + Dense 64 + Softmax 2. Makaledeki 'deconvolutional layers' ifadesi kodda tam bağlı (Dense) katmandır.
- Uyarlama: 'VoxCNN tahmini 3×3×3 ve 32-64-128-256 olarak biz seçeriz' → kodda 8-16-32-64 kullanılmış; makaleye sadık temel için 8-16-32-64 alınmalı, daha geniş filtre ayrı bir deney olarak etiketlenmeli.
- Mimari (ResNet): tabloda kök (stem) eksik — kodda 2×(32 filtre, 3×3×3, BN, ReLU) + 64 filtre stride-2 konv; ardından 2 VoxRes(64) → stride-2 konv(64) → 2 VoxRes(64) → stride-2 konv(128) → 2 VoxRes(128) → 7×7×7 pooling (110³ girdide 2×2×2×128) → FC128 → softmax. VoxRes bloğu: BN→ReLU→conv3³→BN→ReLU→conv3³ + kimlik toplamı; ResNet'te dropout yok. Çekirdek 3×3×3 kodda teyitli.
- Eğitim (ResNet): makale LR 10⁻⁴ diyor, fakat depodaki resnet_train.ipynb nesterov_momentum(..., 0.001) yani 10⁻³ kullanıyor (momentum varsayılan 0.9). Özet bu çelişkiyi belirtmeli.
- Ön işleme: 'Yoğunluk normalizasyonu raporlanmamış' makale için doğru, ancak kodda her hacim kendi maksimumuna bölünüyor (max-ölçekleme); bu bilgi eklenmeli.
- Veri/bölme: 'denek düzeyi mi olduğu açıkça yazılmasa da' → makale açıkça 'her denekten yalnız ilk görüntü' seçildiğini ve bunun bilgi sızıntısını önlemek için yapıldığını söyler (§3); bölme fiilen denek düzeyindedir. Kodda tabakalı (StratifiedKFold) bölme vardır.
- Veri/bölme: 'görev başına örnek sayıları verilmemiş' doğru ama sınıf sayılarından türetilebilir (AD-NC 111, AD-EMCI 127, AD-LMCI 93, LMCI-NC 104, LMCI-EMCI 120, EMCI-NC 138) — bu türetmedir, makalede yazılı değildir.
- Eğitim: 'Şekil 2: ResNet AD-NC doğrulama AUC ~50. epoch sonrası plato' makale metninde yok; doğrulanamadı olarak işaretlenmeli.
- Açıklanabilirlik/anahtar sayılar: 7×7×7 kutu Şekil 3 başlığında değil metinde geçer; yer 'metin (Şekil 3'e atıf)' olmalı.
- Hiperparametre seçimi: makale katman sayısı, filtre, LR, pooling boyutu ve dropout'un 'deneylerle' belirlendiğini söyler; özetteki 'hangi veriyle seçildiği belirtilmemiş' doğru, ayrıca LR'nin de bu listede olduğu eklenmeli.

### 13.3 Özetin atladığı önemli noktalar
- Makale ile resmi kod arasında hiperparametre tutarsızlığı (ResNet LR 10⁻⁴ vs 10⁻³) — yeniden üretimde hangisinin esas alınacağı kararı gerekir.
- Depodaki tam mimari (VoxCNN 8-16-32-64, dropout 0.7; ResNet 32-filtreli kök, pool 7) özetin 'raporlanmamış' dediği boşlukları kapatıyor; özet utils/defterleri okumadığı için bunu kaçırmış.
- CV kodu katlardaki 'test' katını doğrulama olarak da kullanıyor: epoch sayısı ve hiperparametreler aynı katların eğrilerine bakılarak seçilmiş, iç doğrulama/iç içe CV yok — raporlanan Tablo 1 iyimser yanlı bir tahmindir.
- Şekil 3 başlığı/metni bir 'test subset'ten söz ediyor ama ayrı test kümesinin nasıl ayrıldığı tanımlanmıyor; tutarsızlık olarak not edilmeli.
- Ablation yok: sınıf dengeli batch'in, BN/dropout'un, derinliğin etkisi ayrı ölçülmemiş; iki mimari arasında istatistiksel test yok (yalnız ortalama±SD).
- Örneklem çok küçük (görev başına ~93-138 görüntü); 5 bölme tekrarı aynı 231 görüntüden geldiği için SD gerçek genellenebilirlik belirsizliğini düşük gösterebilir.
- Çok sınıflı (4 veya 3 sınıf) sonuç yok; MCI dönüşüm (pMCI/sMCI) görevi yok.
- Dış/bağımsız kohort testi (ör. ADNI2/3, AIBL, OASIS) yok.
- ADNI'nin hazır 'Spatially Normalized, Masked and N3 corrected' çıktısı hangi şablona/çözünürlüğe gittiği ve ADNI1/GO/2 fazlarından hangileri alındığı (EMCI sınıfı ADNI GO/2'den gelir, yani veri yalnız ADNI1 değildir) belirtilmemiş; bizim ADNI1 kurulumunda EMCI/LMCI hiç yok.
- Optimizasyon detayları: ağırlık sönümü, LR çizelgesi, momentum değeri, başlatma, tohumlama raporlanmamış; donanım/süre yok.

### 13.4 Doğrulanamayanlar
- ResNet AD-NC doğrulama AUC'nin ~50. epoch'ta platoya ulaştığı (Şekil 2 görseli okunamadı).
- PDF sürümündeki rakamların HTML ile birebir aynı olduğu (PDF metni çıkarılamadı; ancak LR/batch/epoch kodla tutarlı).
- Parametre sayıları (makalede yok; kod üzerinden hesaplanabilir ama burada hesaplanıp teyit edilmedi).
- Depoda LICENSE dosyası olmadığı (bu denetimde depo ana sayfası ayrıca kontrol edilmedi; görev bilgisine dayanıyor).
- Görüntülerin ADNI'nin hangi fazlarından geldiği ve kaç farklı tarayıcı/alan gücü içerdiği.

### 13.5 Okuyucunun işaretlediği anahtar sayılar (ham)
| İddia | Değer | Yer |
|---|---|---|
| Toplam görüntü sayısı | 231 | §3 |
| AD / LMCI / EMCI / NC sayıları | 50 / 43 / 77 / 61 | §3 |
| Girdi boyutu | 110×110×110 | §3 |
| AD vs NC AUC VoxCNN / ResNet | .88±.08 / .87±.07 | Tablo 1 |
| AD vs NC doğruluk VoxCNN / ResNet | .79±.08 / .80±.07 | Tablo 1 |
| LMCI vs EMCI VoxCNN AUC | .47±.09 | Tablo 1 |
| ResNet katman ve blok sayısı | 21 katman, 6 VoxRes bloğu | §2.2 |
| ResNet filtreler | ilk 4 blok 64, son 2 blok 128; çıkış pooling 2×2×2×128; FC 128 | §2.2 |
| VoxCNN LR / batch / epoch / optimizer | 2×10⁻⁶ / 5 / 150 / Adam (PDF ile teyit gerekli) | §2.1 |
| ResNet LR / batch / epoch / optimizer | 10⁻⁴ / 3 / 70 / Nesterov momentum | §2.2 |
| CV düzeni | 5-kat, 5 farklı bölmeyle tekrar | §2.3 |
| Oklüzyon kutusu | 7×7×7 | Şekil 3 |
| ResNet AD-NC AUC platosu | ~50. epoch sonrası | Şekil 2 |
| Atıf: Suk ve ark. doğruluk | .95/.85/.76; AUC .99/.88/.75 | §1 |
| Sayfa aralığı | 835–838 | künye |

## 14. Kaynaklar
- https://arxiv.org/abs/1701.06643
- https://arxiv.org/html/1701.06643v1
- https://arxiv.org/pdf/1701.06643 (ikili, okunamadı)
- https://github.com/neuro-ml/resnet_cnn_mri_adni
- https://github.com/neuro-ml/resnet_cnn_mri_adni/tree/master/scripts
- https://raw.githubusercontent.com/neuro-ml/resnet_cnn_mri_adni/master/Dockerfile
