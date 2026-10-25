# P04 — Folego 2020 — Tüm beyin 3B CNN (ADNet) ile AD tespiti

> **Durum:** ☐ okunmadı · ☑ AI özeti hazır · ☑ Opus doğrulandı (**ÇELİŞKİ VAR**, güven: yüksek) · ☐ insan okudu · ☐ implemente edildi
> **Sorumlu:** Baran Yeşilyurt · **Grup:** A · **Tam metin (ücretsiz):** https://pmc.ncbi.nlm.nih.gov/articles/PMC7661929/ · **Kod:** https://github.com/gfolego/alzheimers (Apache-2.0)
> **AI okuma kaynağı:** Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC7661929/ (makale gövdesi + kaynakça okundu; ilk 100.000 karakter ayrıntılı, son 13.281 karakter kaynakça/veri bölümü). Frontiers URL'si denenmedi. Depo: https://github.com/gfolego/alzheimers ve /tree/master/src sayfaları okundu (README ve dosya listesi; kaynak kodun içi açılmadı). Not: özetleme aracı sayfayı bölümlere indirgedi, Tablo 6 sütun başlıkları bozuk geldi (doğrulanamadı kısımlar işaretli).

> ⚠ **Nasıl okunmalı:** §2–§12 Sonnet okuyucunun özetidir; §13 Opus hakeminin makaleye karşı denetimidir. §13'te "yanlış" işaretli her sayı için **makaledeki değer** geçerlidir; §13'teki düzeltmeler §4–§8'in üstünde okunur. Hiçbir ajan makalenin yerine geçmez: implementasyondan önce ilgili bölümü (§6, §7) makaleden bir kez daha kendin oku.

## 1. Künye
Folego G., Weiler M., Casseb R.F., Pires R., Rocha A. (2020). Alzheimer's Disease Detection Through Whole-Brain 3D-CNN MRI. Frontiers in Bioengineering and Biotechnology 8:534592. DOI 10.3389/fbioe.2020.534592. PMC7661929.

## 2. Tek paragraf özet
Makale, ham T1 sMRI taramalarından CN/MCI/AD (3 sınıf) ayrımı yapan ADNet adlı tüm beyin 3B CNN'ini sunar. Ön işleme tamamen ANTs ile yapılır (kafatası ayıklama, bias düzeltme, MNI152 2009c asimetrik şablona rijit+afin+SyN kayıt, 145×182×155'e kırpma). Altı mimari (LeNet-5, VGG 2048/512, GoogLeNet, ResNet A/B) 2B'den 3B'ye çevrilip denenir; en iyisi VGG 512'dir (26,8 M parametre). Eğitim ADNI1 (Dset. 1; 845 denek, 9.149 görüntü) ile yapılır, model seçimi CADDementia eğitim kümesindeki avgTPF'e göre yapılır. Alan uyarlaması (ADNet-DA) için son katmandan önceki 512 özellik üzerine lojistik regresyon eğitilir. CADDementia gizli test kümesinde ADNet %51,4, ADNet-DA %52,3 doğruluk alır (48 gönderimde 25. ve 21.). Sonuçlar mütevazıdır, MCI duyarlılığı düşüktür; makalenin asıl katkısı sıfırdan, alana özgü bilgi kullanmayan bir hat ve hızlı çıkarım (<1 sn) olmasıdır. Bizim projede asıl değer ANTs ön işleme zinciri ve harici test fikridir; sınıflandırma sonuçları bizim hedefimiz (AD-NC ≥%85) için referans olamaz, çünkü makale AD-NC ikili görevi raporlamaz.

## 3. Problem ve katkı
- Problem: Elle özellik çıkarmadan, tüm beyin hacminden doğrudan CN/MCI/AD sınıflandırması; tutarlı karşılaştırma için bağımsız CADDementia testi.
- Katkı 1: Tam otomatik, ANTs tabanlı ön işleme ve MNI152 normalizasyonu; 3B CNN'lerin (LeNet, VGG, GoogLeNet, ResNet) 3 sınıflı problemde sistematik karşılaştırması (Tablo 1, Tablo 5).
- Katkı 2: Çok veri kümeli (ADNI, AIBL, MIRIAD, OASIS) birleşik eğitim denemesi (Tablo 2-4); ADNI1 tek başına en iyi sonucu verdi (Sec. 4.2).
- Katkı 3: Basit alan uyarlaması (ADNet-DA): 512 boyutlu özellik + lojistik regresyon (Sec. 2.3).
- Katkı 4: Açıklanabilirlik (guided backprop, occlusion, t-SNE; Fig. 4-5) ve çıkarım hızı (<1 sn; CADDementia'nın en iyi yöntemine göre ~80 kat hızlı).
- Kod ve eğitilmiş model herkese açık (Apache-2.0, figshare).

## 4. Veri seti ve bölme
- Kaynaklar (Tablo 2, Sec. 3.1): ADNI 18.303 görüntü; AIBL 1.098; CADDementia 384; MIRIAD 708; OASIS 3.056.
- Dset. 1 (ADNI1, yalnız MP-RAGE): 845 denek, 9.149 görüntü; CN 2.701 / MCI 4.845 / AD 1.603 (Tablo 4). Birden fazla tarama/denek içerir (tüm ziyaretler), yalnız başlangıç taraması DEĞİL.
- Dset. 2: 15.885 görüntü (tüm ADNI MP-RAGE); Dset. 3: 18.303; Dset. 4: 23.165 görüntü, 2.984 denek, CN 8.462 / MCI 10.460 / AD 4.243 (Tablo 3-4).
- Bölme: denek düzeyinde, tabakalı 70/10/20 %. Dset. 1: eğitim 591, doğrulama 84, test 170 denek. Sonraki veri kümelerinde önceki denekler korunup yalnız yeni denekler bölünür (Sec. 3.1).
- Çapraz doğrulama: ana eğitimde YOK (tek bölme). CADDementia eğitim kümesinde (30 görüntü: CN 12, MCI 9, AD 9) alan uyarlaması için leave-one-out CV kullanıldı (Sec. 2.3/4.2).
- Dış test: CADDementia test, 354 görüntü, gizli etiketler, çevrimiçi gönderim (Tablo 4, Sec. 4.2).
- Sınıf birleştirme: eMCI+lMCI → MCI; SMC dışlandı (Sec. 3.1).

**Sızıntı riski (AI):** orta — Olumlu: denek düzeyinde bölme, normalizasyon istatistiklerinin yalnız eğitim kümesinden hesaplanması ve gizli etiketli CADDementia testi. Riskler: (1) model/hiperparametre seçimi CADDementia EĞİTİM kümesindeki avgTPF'e göre yapılmış, aynı küme alan uyarlaması ve LOO-CV için de kullanılmış; yazarlar kendileri bunun performansı olduğundan yüksek gösterebileceğini belirtiyor (Sec. 4.1-4.2; Tablo 6'da LOO %76,7 vs gizli test %52,3). (2) Dset. 1'de bir denekten çoklu tarama var; bölme denek düzeyinde olduğu için sızıntı beklenmez ama bu açıkça 'tüm ziyaretler' olarak doğrulanamadı. (3) ADNI-AIBL/OASIS arası denek örtüşmesinin kontrolü anlatılmıyor (doğrulanamadı). (4) Dset. 4'te minimum yaş 18 ve CN yaş SD 16,1 (Tablo 4): genç OASIS denekleri veri kümesi kaynağı kestirimi (confound) yaratabilir. (5) Dset. 1 test bölümünün model seçimde hiç kullanılmadığı açıkça yazılmamış (doğrulanamadı).

## 5. Ön işleme
- Araç: ANTs 2.1.0, antsBrainExtraction.sh ve antsRegistrationSyNQuick.sh, varsayılan parametreler (Sec. 2.1, Fig. 1A).
- Sıra: intensity winsorizing → bias alanı düzeltme (N4 olarak adlandırılmıyor, doğrulanamadı) → ikinci winsorizing → çeviri hizalama → rijit → afin → SyN deformable kayıt → atlas beyin maskesiyle kafatası ayıklama → aralık normalizasyonu.
- Şablon: MNI152 ICBM 2009c Nonlinear Asymmetric, 1 mm³ izotropik (193×229×193) (Sec. 2.1).
- Kırpma: 145×182×155 voksel; seyreklik %78 → %54 (Sec. 2.1).
- Normalizasyon: sıfır ortalama, birim varyans; istatistik yalnız eğitim kümesinden, Welford çevrimiçi algoritması ile (Sec. 2.1).
- Süre: hacim başına çoğunlukla 7-15 dk, ortalama ~12 dk; 151 hacim (%0,7) >25 dk (Fig. 2).
- Dikkat: SyN deformable kayıt kullanıyor; bizim kurulumdaki afin kayıt farklı (daha az beyin şekli bozulması, ama daha az hizalama).

## 6. Mimari
| Katman/Blok | Çekirdek | Kanal | Çıktı | Not |
|---|---|---|---|---|
| Girdi | - | 1 | 145×182×155 | z-score, MNI152 (Sec. 2.1) |
| VGG 512 (en iyi, Tablo 1, Sec. 2.2/4.2) | 3×3×3 | VGG'nin yarı filtre sayısı (kesin kanal listesi doğrulanamadı) | - | Her conv+FC sonrası BatchNorm + ReLU |
| FC katmanları | - | 512 birim (2 FC) | 512 | Dropout %50; L2 λ=1e-4 (Tablo 5) |
| Çıkış | - | 3 | 3 (CN/MCI/AD) | Softmax |
| Diğer: LeNet-5 | - | - | - | 7 katman, 0,3 M param |
| VGG 2048 | - | - | - | 11 katman, 89,8 M |
| GoogLeNet | - | - | - | 22 katman, 14,6 M; dropout %40 |
| ResNet A / B | - | - | - | 18 katman, 33,0 / 33,2 M; B projeksiyon kısayol |

Parametre sayısı (Tablo 1): VGG 512 = 26,8 M (11 katman). Girdi: 145×182×155, tek kanal. Katman bazında kanal/çıktı boyutları metin özetinde bulunamadı (doğrulanamadı); tam liste için kod (adnet.py) ve Fig. 1B incelenmeli.

## 7. Eğitim ayarları
- Optimizer: Adam (varsayılan β), başlangıç LR 1e-4; ağırlık başlatma Glorot uniform (Sec. 3.2).
- Batch: VGG için 3, diğerleri için 9 (Sec. 3.2); Sec. 4.2 ile tutarsızlık olabilir, en iyi modelin batch'i açık değil (doğrulanamadı). Sınıf-dengeli batch (her sınıftan eşit).
- Kayıp: kategorik çapraz entropi; multiclass hinge fayda sağlamadı.
- Düzenlileştirme: L2 (λ=1e-4) genelde en iyi, dropout %50 (VGG), %40 (GoogLeNet) (Tablo 5).
- Erken durdurma: doğrulama avgTPF üzerinde sabır 50 epoch, en fazla 200 epoch.
- Veri artırma: tanımlanmamış (yok gibi görünüyor, doğrulanamadı).
- Donanım: GTX TITAN X, Tesla K40c, K80; yazılım Lasagne/Theano, Python 2.7.6, CUDA 7.5, cuDNN 5.
- Süre: 121 deney için toplam ~4 gün (Sec. 4.2); çıkarım VGG 512'de <1 sn; alan uyarlaması grid search <1 dk.
- Alan uyarlaması: 512 özellik (sondan ikinci katman) → hedef eğitim verisinde standardizasyon → one-vs-rest lojistik regresyon, LOO-CV grid search, en iyi C=0,001 (Sec. 2.3/4.2).

## 8. Sonuçlar
| Görev | Metrik | Değer | Test seti | Kaynak |
|---|---|---|---|---|
| Model seçimi: LeNet-5 | avgTPF | 56,5 | CADDementia eğitim (30) | Tablo 5 |
| Model seçimi: VGG 512 | avgTPF | 75,9 (≈%76,7 doğruluk) | CADDementia eğitim | Tablo 5, Sec. 4.2 |
| Model seçimi: GoogLeNet | avgTPF | 58,3 | CADDementia eğitim | Tablo 5 |
| Model seçimi: ResNet B | avgTPF | 60,2 | CADDementia eğitim | Tablo 5 |
| Dataset 2 ile eğitim | avgTPF | 72,2 (Dset. 1'den düşük) | CADDementia eğitim | Sec. 4.2 |
| 3 sınıf, ADNet | Doğruluk | 60,6 / 44,1 / 43,6 (eğitim/doğrulama/test; sütun sırası doğrulanamadı) | Dset. 1 | Tablo 6 |
| 3 sınıf, ADNet | Doğruluk | 51,4 (TPF: CN 77,5; MCI 27,9; AD 46,6) | CADDementia test (354) | Tablo 6 |
| 3 sınıf, ADNet-DA | Doğruluk | 52,3 | CADDementia test | Tablo 6, Abstract |
| 3 sınıf, ADNet-DA LOO-CV | Doğruluk | 76,7 (TPF CN 75,0; MCI 55,6; AD 100) | CADDementia eğitim (30) | Tablo 6 |
| ADNet-DA karışıklık (satır %) | CN→CN/MCI/AD | 68,2 / 25,6 / 6,2 | CADDementia test | Tablo 7 |
| | MCI→ | 51,6 / 37,7 / 10,7 | | Tablo 7 |
| | AD→ | 29,1 / 21,4 / 49,5 | | Tablo 7 |
| Sıralama | Yarışma sırası | ADNet 25./48; ADNet-DA 21./48 | CADDementia | Sec. 4.2 |

~~AUC ve AD-vs-NC ikili sonuç makalede raporlanmamış görünüyor (doğrulanamadı).~~
**DÜZELTME (Opus §13.2): AUC Tablo 6'da VAR** — ADNet-DA CADDementia test: AUC All 70.9, CN 72.8, MCI 60.5, **AD 79.0**; ADNet CADD test All 68.5 (AD 73.6); ADNet Dset.1 test All 68.0 (AD 68.9). AD-vs-NC ikili sonuç yok, ama AD one-vs-rest AUC bizim AD-NC hedefimize en yakın referanstır. Ayrıca Tablo 6'da ADNet CADD Train Acc 76.7 ve ADNet-DA CADD Train (yeniden yerine koyma) Acc 90.0 / AUC 98.0 satırları da var.

## 9. Açıklanabilirlik / ek analiz
Sec. 4.3, Fig. 4-5: filtre görselleştirme, aktivasyon haritaları, occlusion (Zeiler & Fergus), gradyan ve guided backpropagation. Guided backprop (Fig. 4): CN'de dağınık temporal/oksipital/posterior aktivasyon; MCI'da sol posterior parietal, sağ anterior singulat ve prefrontal; AD'de sol posterior parietal, sağ temporal kutup ve beyincik. Fig. 5: t-SNE ile 512 boyutlu özellik uzayında eğitim örnekleri 3 boyutlu softmax uzayından daha iyi ayrışıyor. Beyincik vurgusu klinik olarak beklenen değildir; yazarlar bu konuda dikkatli yorum yapar (ayrıntı doğrulanamadı). Nicel doğrulama (ör. atlas örtüşmesi) yok.

## 10. Kod ve tekrarlanabilirlik
- Depo: https://github.com/gfolego/alzheimers, Apache-2.0 (LICENSE dosyası var) → kopyalanabilir.
- Dosyalar: README.md, docker-compose.yml, src/Dockerfile-brain, src/Dockerfile-cnn, src/adnet.py, src/brain_process.py, src/brain_process.sh, src/cnn_process.py, src/utils.py. requirements dosyası yok.
- Çerçeve: sayfada belirtilmiyor; makale Lasagne/Theano (Python 2.7) diyor, depo da muhtemelen aynı (doğrulanamadı, kodun içi açılmadı).
- Ağırlıklar: depoda yok; README modelin figshare'de olduğunu söylüyor (doi 10.6084/m9.figshare.11908536).
- Veri: yok. Yalnızca çıkarım hattı (adnet-brain: .nii.gz → ANTs çıktısı; adnet-cnn: olasılıklar CN/MCI/AD .txt). Eğitim betiği görünmüyor olabilir (doğrulanamadı).
- Ortam: Docker 19.03.6, docker-compose 1.17.1, Ubuntu 18.04.5 test edilmiş; ANTs tekrarlanabilirlik uyarısı var.
- 2 commit; eski yığın (Theano/Py2.7) PyTorch/MONAI'ye doğrudan taşınmaz; ANTs betikleri (brain_process.sh) yeniden kullanılabilir.

## 11. Güçlü ve zayıf yönler
Güçlü: Gizli etiketli dış test (CADDementia); denek düzeyinde bölme; eğitim istatistiklerinin sızıntısız kullanımı; ayrıntılı ön işleme süresi/seyreklik bilgisi; kod+model açık; çok mimari karşılaştırması; basit ve hızlı alan uyarlaması. Zayıf: Doğruluk düşük (%51-52), MCI TPF %27,9-37,7; AUC yok; AD-NC ikili görevi yok; model seçimi CADDementia eğitim (30 örnek) ile, çok küçük ve gürültülü; eğitim/doğrulama/test farkı büyük (60,6 → 43,6) aşırı öğrenme; veri artırma yok; çapraz doğrulama ve çoklu tohum yok; eski yığın (Theano/Py2.7); VGG batch bilgisi tutarsız; Tablo 6 okunaksız; Dset. 4'te yaş confound riski; ANTs SyN hacim başına ~12 dk (maliyetli).

## 12. Bizim projeye uyarlama
Kurulumumuz: ADNI1 1.5T başlangıç T1, NC/MCI/AD, HD-BET → N4 → z-score → MNI152 afin → 128³, RID düzeyinde 5-kat CV × 3 tohum, birincil görev AD-NC, ikincil 3-sınıf.

### 12.1 Okuyucunun uyarlama notu
Aynen alınabilir: ANTs → MNI152NLin2009cAsym fikri ve şablon seçimi (bizimki aynı şablon), eğitim istatistikleriyle z-score fikri (biz maske içinde denek bazlı z-score yapıyoruz), sınıf-dengeli batch, Adam 1e-4, L2 1e-4, erken durdurma, VGG tipi 3×3×3 blok + BatchNorm, 512 boyutlu özellik + lojistik regresyon (alan uyarlama/özellik probu).
Değiştirilecek: (1) ANTs SyN yerine HD-BET + SimpleITK N4 + afin (makale deformable, biz afin; biraz farklı hizalama); (2) 145×182×155 yerine 128³ (yeniden örnekleme; çözünürlük ~1,3-1,4 mm); (3) Theano/Lasagne yerine PyTorch+MONAI (ör. 3B VGG-benzeri ya da monai.networks.nets.DenseNet/ResNet); (4) makale tüm ziyaretleri kullanıyor, biz yalnız baseline (798 denek); (5) bölme RID düzeyinde 5-kat CV × 3 tohum (makalede tek bölme); (6) AD-NC ikili birincil görev, makale yalnız 3 sınıf; (7) AUC, F1-makro, duyarlılık, özgüllük, dengeli doğruluk raporla; (8) veri artırma (hafif afin/gürültü) ekle, makalede yok.
Protokole uymayan: model seçimi CADDementia eğitiminde (biz yalnız iç doğrulama kat içinde); CADDementia'ya erişimimiz/dış testimiz yok (ADNI2/AIBL gibi başka bir dış küme ancak izinle); makalenin MCI birleştirmesi (eMCI+lMCI) bizim MCI ile benzer; çoklu tarama/denek bizde yok.
Zorluk: 2/5 (ön işleme fikri), 3/5 (model eğitimi), kodu doğrudan çalıştırmak 4/5 (Py2.7/Theano/Docker).
VRAM/süre tahmini (tahmin): 128³ girdi, 26,8 M parametreli VGG-512 benzeri, batch 4-8, karışık hassasiyetle T4 16 GB'a sığar (~6-10 GB; tahmin). Epoch başına ~600 eğitim hacmi ile ~1-2 dk; 5-kat × 3 tohum × ~100 epoch toplamda ~15-30 GPU saati (tahmin). ANTs SyN'yi 800 hacme uygulamak ~12 dk × 800 ≈ 160 saat CPU, bu yüzden afin tercih edilmesi isabetli.

### 12.2 Hakemin kurulum farkı analizi
Sızıntı değerlendirmesi: 'orta' düzeyine katılıyorum, gerekçeler büyük ölçüde doğru. Asıl risk, model ve hiperparametre seçiminin CADDementia eğitim kümesinde (30 görüntü) yapılması; ADNet ve ADNet-DA'nın bu kümede 76,7, DA'nın yeniden yerine koymada 90,0 alması, gizli testte ise 51-52'ye düşmesi bunun kanıtı. Dset.1'de denek başına ~11 tarama var ama bölme denek düzeyinde, bu yüzden iç bölmede sızıntı beklenmez. Veri kümeleri arası denek örtüşmesi ve Dset.4'teki yaş karıştırıcısı (en düşük yaş 18, CN 71,3 ± 16,1) belirsizliği sürüyor.

Somut farklar ve beklenen etkileri:
(1) Veri. Makale ADNI1'in bütün MP-RAGE taramalarını kullanıyor (9.149 görüntü / 845 denek, ~11 tarama/denek). Biz yalnız baseline kullanıyoruz (~798 tarama). Örnek sayımız ~11 kat az; çoklu ziyaret de bir tür doğal veri artırması işlevi görüyordu. Hafif artırma ve düzenlileştirme olmadan 26,8 M parametreli bir VGG aşırı öğrenir; daha küçük bir ağ (≤5-10 M) tercih edilmeli.
(2) Görev. Makale yalnız 3 sınıf raporluyor (Dset.1 iç test doğruluğu %43,6, CADD testi %51-52). Bizim birincil görevimiz AD-NC ikili. İkili görev çok daha kolay; literatürde %85 ve üstü yaygın. Makalenin AD one-vs-rest AUC değeri (test 79,0, Dset.1 test 68,9) alt sınır gibi okunabilir, doğrudan kıyas değildir.
(3) Ön işleme. Makale ANTs SyN deformable kayıt (hacim başına ~12 dk) ve atlas maskesi kullanıyor. Biz HD-BET, N4, maske içi z-score ve yalnız afin kayıt yapıyoruz. Afin kayıtta denekler arası anatomik varyans kalır. Bu hem AD atrofisi bilgisini korur hem de modelin hizalama gürültüsüne karşı daha fazla veri istemesine yol açar. Hesap maliyeti dakikalar yerine saniyeler.
(4) Normalizasyon. Makale eğitim kümesinin voksel düzeyindeki ortalama ve varyansını kullanıyor (Welford). Biz denek bazlı maske içi z-score yapıyoruz; bu kat dışı istatistik gerektirmediği için sızıntısız. Yoğunluk ölçeği farkı tarayıcılar arası genellemeyi iyileştirebilir.
(5) Boyut. Makalenin girdisi 145×182×155 ve 1 mm. Bizimki 128³ ve ~1,4-1,5 mm (kırpma ve yeniden örneklemeye bağlı). Bu VRAM'i ~2 kat azaltır, T4'te batch 4-8 mümkün olur; ince hipokampus ayrıntısı biraz kaybolur.
(6) Bölme ve değerlendirme. Makalede tek bir 70/10/20 bölme var ve görüntü düzeyinde metrik raporlanıyor. Bizde RID düzeyinde 5 kat × 3 tohum var; ortalama ± std ve dengeli doğruluk, AUC, F1 raporlanır. Bu daha güvenilir ama varyansı daha görünür kılar.
(7) Dış test. Makalede gizli etiketli CADDementia testi var; bizde yok. Bulgularımız iç CV ile sınırlı kalır, genelleme iddiası zayıflar.
(8) Yığın. Makale Theano/Lasagne ve Python 2.7 kullanıyor; biz PyTorch ve MONAI. Kod doğrudan taşınamaz, yalnız ön işleme mantığı ve hiperparametreler alınabilir.

### 12.3 İmplementasyon yapılacaklar (hakem)
1) Depodan (Apache-2.0) yalnız referans olarak src/brain_process.sh ve brain_process.py'deki ANTs adım sırasını oku (winsorize, bias, rijit, afin, SyN, maske, aralık normalizasyonu). Bizim hat bunun yerine HD-BET, sitk.N4BiasFieldCorrectionImageFilter, sitk afin kayıt (MNI152NLin2009cAsym) ve maske içi z-score kullanır. SyN'yi kullanma: 800 hacim × ~12 dk ≈ 160 CPU saati eder.
2) Kayıttan sonra 128³'e ulaşmak için önce makaledeki gibi beyin kutusuna kırp (yaklaşık 145×182×155 mm bölgesi), sonra monai.transforms.Resized veya Spacingd ile yeniden örnekle. Bunu bir kez yapıp .npy veya .nii.gz olarak önbelleğe al (monai.data.PersistentDataset).
3) Bölmeyi sklearn StratifiedGroupKFold(n_splits=5, groups=RID) ile kur; 3 tohum için ayrı karıştırmalar kullan. Her katta eğitimin %10-15'ini (yine RID düzeyinde) doğrulama olarak ayır. Erken durdurma ve eşik seçimi yalnız bu iç doğrulamayla yapılmalı; test katına asla dokunulmaz.
4) Model: VGG tarzı 3B ağ kur (3×3×3 conv, BatchNorm3d, ReLU, MaxPool; filtreler 16-32-64-128-256; GAP; FC 512; Dropout 0,5). Alternatif olarak monai.networks.nets.DenseNet121(spatial_dims=3, in_channels=1, out_channels=2) veya ResNet(10/18) kullanılabilir. 26,8 M parametreli tam VGG-512 baseline veriyle aşırı öğrenir; ilk FC'deki parametre patlamasından kaçınmak için GAP kullan.
5) Hiperparametreler (makaleden): Adam lr=1e-4 (β 0,9/0,999), weight_decay≈1e-4 (L2 ile eşdeğer), sınıf-dengeli örnekleme (torch WeightedRandomSampler), çapraz entropi kaybı, erken durdurma sabrı ≈20-30 epoch, en fazla 100-200 epoch. Makaledeki sabır 50 ve 4 günlük koşu Colab/Kaggle oturum sınırına sığmaz; checkpoint ile devam ettir.
6) Makalede veri artırma yok ve bizde örnek ~11 kat az. Bu yüzden hafif artırma ekle: monai RandAffined (±10°, ±%10 ölçek), RandGaussianNoised, RandAdjustContrastd. Sol-sağ çevirmeyi dikkatli kullan; makaledeki guided backprop asimetrik bulgular gösteriyor.
7) T4 için torch.cuda.amp karışık hassasiyet kullan; 128³ girdiyle batch 4-8 dene. Bellek yetmezse gradient checkpointing veya batch 2 ile gradient accumulation kullan.
8) Metrikleri denek düzeyinde raporla (baseline'da zaten tek tarama/denek): dengeli doğruluk, ROC-AUC, F1-makro, duyarlılık, özgüllük. 5 kat × 3 tohum için ortalama ± std ver. Makaleyle kıyas yalnız 3 sınıflı ikincil görevde anlamlı (Dset.1 test %43,6, AUC 68,0); AD-NC için makale doğrudan kıyas sunmaz.
9) İsteğe bağlı ADNet-DA benzeri deney: sondan ikinci katmanın 512 boyutlu özelliklerini çıkar, ölçeklemeyi yalnız eğitim katına uydur (StandardScaler) ve LogisticRegression (C grid, C≈1e-3) ile 'özellik probu' kur. C seçimi iç doğrulamada yapılmalı; makalenin aynı kümede seçip raporlama hatası tekrarlanmamalı.
10) Açıklanabilirlik için monai.visualize GradCAM veya OcclusionSensitivity kullan; sonuçları atlas bölgeleriyle (hipokampus, temporal) nicel karşılaştır. Makale yalnız nitel yorum yapmış; beyincik vurgusu gibi beklenmeyen bulguları kaynak/hizalama artefaktı açısından kontrol et.

## 13. Opus doğrulama
- **Sonuç:** **ÇELİŞKİ VAR** · **Güven:** yüksek
- **Hakemin okuduğu kaynak:** PMC tam metni (https://pmc.ncbi.nlm.nih.gov/articles/PMC7661929/) WebFetch ile iki kez sorgulandı. Sayfanın ilk 100.000 karakteri okundu (gövde, Tablo 1-7, Bölüm 2-4); son 13.281 karakter (kaynakça/veri bildirimi) okunmadı. Tablo 6 sütun başlıkları bu kez düzgün geldi: Accuracy | TPF (CN, MCI, AD) | AUC (All, CN, MCI, AD). GitHub deposunun ana sayfası (README, LICENSE) da okundu; src/ içindeki kod açılmadı. Frontiers URL'si denenmedi.

### 13.1 Kontrol edilen sayılar
| İddia | Özetteki değer | Makaledeki değer | Durum | Yer |
|---|---|---|---|---|
| ADNet-DA CADDementia test doğruluğu | 52,3 % | 52,3 (Tablo 6, ADNet-DA CADD Test) | **doğru** | Abstract, Tablo 6 |
| ADNet (DA'sız) CADDementia test doğruluğu | 51,4 % | 51,4; TPF CN 77,5 / MCI 27,9 / AD 46,6 | **doğru** | Tablo 6 |
| Yarışma sırası ADNet / ADNet-DA | 25. / 21. (48 gönderim) | 25. (iki gönderimle berabere) / 21.; toplam 48 gönderim | **doğru** | Sec. 4.2 |
| Dset. 1 denek ve görüntü sayısı | 845 denek, 9.149 görüntü | 845 denek / 9.149 görüntü (CN 2.701, MCI 4.845, AD 1.603) | **doğru** | Tablo 3-4 |
| Dset. 1 denek bölmesi | 591 / 84 / 170 (70/10/20 %) | 591 denek/6.314 görüntü; 84/951; 170/1.884; hedef oran 70/10/20 | **doğru** | Tablo 4, Sec. 3.1 |
| Kırpma sonrası girdi boyutu | 145×182×155 (193×229×193'ten) | 145×182×155, özgün hacmin %48'i; atlas 193×229×193 | **doğru** | Sec. 2.1 |
| VGG 512 parametre sayısı | 26,8 M, 11 katman | 26,8 M, 11 katman | **doğru** | Tablo 1 |
| VGG 512 avgTPF (CADDementia eğitim) | 75,9 (≈%76,7 doğruluk) | 75,9; metin bunun %76,7 doğruluğa karşılık geldiğini söylüyor | **doğru** | Tablo 5, Sec. 4.2 |
| Optimizer ve LR | Adam, 1e-4 | Adam (β1=0,9, β2=0,999, ε=1e-8), LR 1e-4 | **doğru** | Sec. 3.2 |
| Batch boyutu | VGG için 3, diğerleri 9 (tutarsızlık olabilir) | VGG 3, diğerleri 9, sınıf-dengeli batch. Makalede tutarsızlık bulunmadı | **doğru** | Sec. 3.2 |
| Erken durdurma | sabır 50, en fazla 200 epoch | doğrulama avgTPF'te 50 epoch iyileşme olmazsa durur, en fazla 200 epoch | **doğru** | Sec. 3.2/4.1 |
| Alan uyarlaması C ve LOO doğruluğu | C=0,001; LOO %76,7 | C=0,001; ADNet-DA Train* (LOO) 76,7 (TPF 75,0/55,6/100) | **doğru** | Sec. 4.2, Tablo 6 |
| Hacim başına ön işleme süresi | 7-15 dk, ortalama ~12 dk | çoğunlukla 7-15 dk, ortalama ~12 dk; 151 hacim (%0,7) >25 dk; en kötü ~2 sa | **doğru** | Fig. 2, Sec. 2.1 |
| Kırpma öncesi/sonrası seyreklik | %78 → %54 | %78 → %54 | **doğru** | Sec. 2.1 |
| ADNet-DA MCI satırı karışıklık | CN 51,6 / MCI 37,7 / AD 10,7 | 51,6 / 37,7 / 10,7 | **doğru** | Tablo 7 |
| Toplam eğitim süresi ve deney sayısı | 121 deney için toplam ~4 gün | 121 deney yapıldı, ama ~4 gün TEK bir eğitim koşusunun süresi ("about 100 epochs, taking around 4 days"). 121 deneyin toplam süresi verilmiyor | **yanlış** | Sec. 4.1/4.2 |
| AUC raporlanmamış (özetin sonuçlar ve güçlü/zayıf bölümleri) | AUC yok / raporlanmamış görünüyor | Tablo 6'da AUC var (All/CN/MCI/AD). ADNet-DA CADD test: 70,9 / 72,8 / 60,5 / 79,0. ADNet CADD test: 68,5. Dset.1 test: 68,0 | **yanlış** | Tablo 6 |

### 13.2 Düzeltmeler (özette yanlış/eksik → doğrusu)
- Eğitim süresi: '121 deney için toplam ~4 gün' yanlış. Doğrusu: tipik bir eğitim koşusu ~100 epoch sürüyor ve ~4 gün alıyor (Sec. 4.1). Toplam 121 deney yapıldı; bunların toplam süresi verilmiyor ve gün değil aylar mertebesinde olmalı.
- AUC raporlanıyor. Tablo 6'da AUC var (All, CN, MCI, AD). ADNet-DA CADDementia test: All 70,9; CN 72,8; MCI 60,5; AD 79,0. ADNet CADD test: All 68,5 (AD 73,6). ADNet Dset.1 test: All 68,0. 'AUC yok' ifadesi sonuçlar ve güçlü/zayıf bölümlerinden çıkarılmalı. AD-vs-NC ikili AUC yok, ama AD one-vs-rest AUC (79,0) var.
- Tablo 6'nın sütunları okunabilir durumda: Acc | TPF CN/MCI/AD | AUC All/CN/MCI/AD. Dset.1 satırları Train 60,6 / Val 44,1 / Test 43,6; sıra doğrulandı.
- Tablo 6'da özetin atladığı iki satır var. (1) ADNet (DA'sız) CADD Train: doğruluk 76,7. (2) ADNet-DA CADD Train (LOO'suz, yeniden yerine koyma): 90,0, AUC 98,0. Özet %76,7'yi yalnız LOO satırına bağlıyor.
- VGG 512 mimarisi: makale yalnızca 'her FC katmanında 512 birim' ve 'tüm konvolüsyon filtre sayıları yarıya indirildi' diyor. '2 FC' sayısı makalede açıkça yazmıyor (doğrulanamadı). Glorot uniform başlatmanın ölçek faktörü 2.
- Açıklanabilirlik: beyincik yalnızca AD'deki aktivasyon bölgelerinden biri olarak sayılıyor. Yazarların bu konuda 'dikkatli yorum yaptığı' iddiası makalede yok. CN bölgeleri: sağ temporal lob, oksipital lob merkezi, posterior singulat, posterior parietal. MCI: sağ dorsolateral prefrontal.
- Batch boyutu konusunda Sec. 4.2 ile 'tutarsızlık' bulunamadı. VGG için 3 (GPU belleği nedeniyle) açıkça yazılı; tutarsızlık notu kaldırılmalı.
- Aşırı öğrenme yorumu: yazarlar eğitim ile doğrulama arasındaki farkı aşırı öğrenme olarak not ediyor, ama Dset.1 doğrulama-test farkının küçük olduğunu (44,1 ile 43,6) belirtiyor. '60,6 → 43,6' farkının kaynağı eğitim-doğrulama arasındadır.
- Düzenlileştirme araması: L1 ve L2 için λ 1e-5'ten 1e2'ye 10'un katlarıyla, birim sayısı 32-2048, dropout %40-%99,9 tarandı. En iyi değerler Tablo 5'te mimariye göre değişiyor: LeNet L2 1e-2; GoogLeNet L1 1e-3, dropout %80; ResNet B L2 1e-2. 'L2 1e-4 genelde en iyi' ifadesi yalnız VGG 512 için doğru.
- Ön işleme: bias düzeltmesinin N4 olarak adlandırılmadığı doğru ('bias field correction'). Kafatası ayıklama ayrı bir sıralı adım değil; SyN'den sonra atlas beyin maskesi uygulanıyor. Ön işleme donanımı: 2 çekirdek, ~2 GB RAM, Xeon E5645.
- Kod/model: makale metni GitHub'ı veriyor, figshare'den söz etmiyor. Figshare DOI yalnız README'de geçiyor.

### 13.3 Özetin atladığı önemli noktalar
- Tablo 6'daki AUC değerleri (özellikle AD one-vs-rest AUC: test 79,0, Dset.1 test 68,9) bizim AD-NC AUC hedefimize en yakın referans; özet bunları atlamış.
- Dış test anlamlılığı: %95 güven aralığına göre ADNet yalnızca ilk ve son üç sistemden, ADNet-DA ilk ve son dört sistemden anlamlı biçimde farklı. Sıralamanın büyük kısmı istatistiksel olarak ayırt edilemiyor.
- Yazarların kendi sızıntı uyarısı: girişte birçok CNN-AD çalışmasında veri sızıntısı olduğu ya da doğrulamanın yeterince açıklanmadığı söyleniyor. Mehmood ve ark. için veri artırmanın sızıntıya yol açmış olabileceği belirtiliyor. Bizim protokol için önemli bir kaynak.
- Sec. 4.2'deki kabul: aynı veride geliştirip değerlendirmek genellemeyi olduğundan yüksek gösterdi, ve LOO-CV test kestirimini anlamlı biçimde iyileştirmedi (LOO 76,7 iken gizli test 52,3).
- Ablasyon/karşılaştırmalar: veri kümesi ablasyonu (Dset.2 avgTPF 72,2, yani daha fazla veri daha iyi sonuç vermedi); GoogLeNet L2 ile ve ResNet A ile 57,4; hinge ile çapraz entropi kaybı karşılaştırması.
- Hız: worst-case ~10 kat, ortalamada ~80 kat daha hızlı (19 saatlik en iyi yönteme göre). 354 test örneğinin DA sınıflandırması ~1 ms.
- Yazarların sınırlılıkları: sMRI ile MCI TPF'nin düşük olması beklenir; eğitimden teste MCI/AD TPF düşüşü beklenenden büyük; derin ağlar daha büyük veri ister; batch boyutunu GPU belleği sınırladı; softmax sınıflandırıcı özelliklerinden daha kötü; klinik veri kullanılmadı.
- Dset.1'de denek başına ~11 görüntü var (9.149/845). Bu, çoklu ziyaret/tekrar taramalarını ve yüksek denek içi korelasyonu gösteriyor. Görüntü düzeyindeki metrikler denek düzeyindekinden farklı yorumlanmalı.

### 13.4 Doğrulanamayanlar
- VGG 512'de FC katmanı sayısı (2 FC) ve blok bazında kanal listesi; makale yalnız 'filtreler yarıya indirildi, FC 512 birim' diyor
- Dset.1 test bölümünün model seçiminde hiç kullanılmadığı; makale bunu açıkça yazmıyor, model seçimi CADDementia eğitim kümesine göre yapılmış
- ADNI ile AIBL/OASIS/MIRIAD arasında denek örtüşmesi kontrolü; makalede anlatılmıyor
- Depoda eğitim betiği olup olmadığı ve kullanılan çerçeve (src/ içi açılmadı; makale Lasagne/Theano diyor)
- PMC sayfasının son 13.281 karakteri (kaynakça/veri bildirimi) okunmadı

### 13.5 Okuyucunun işaretlediği anahtar sayılar (ham)
| İddia | Değer | Yer |
|---|---|---|
| CADDementia test doğruluğu ADNet-DA | 52,3 % | Abstract, Tablo 6 |
| CADDementia test doğruluğu ADNet (alan uyarlamasız) | 51,4 % | Tablo 6 |
| Yarışma sırası ADNet / ADNet-DA | 25. / 21. (48 gönderim) | Sec. 4.2 |
| Dset. 1 denek ve görüntü sayısı | 845 denek, 9.149 görüntü | Tablo 3-4 |
| Dset. 1 bölme (denek) | 591 / 84 / 170 (70/10/20 %) | Tablo 4, Sec. 3.1 |
| Girdi boyutu (kırpma sonrası) | 145×182×155 voksel (MNI 193×229×193'ten) | Sec. 2.1 |
| VGG 512 parametre sayısı | 26,8 M, 11 katman | Tablo 1 |
| VGG 512 avgTPF (CADDementia eğitim) | 75,9 (≈%76,7 doğruluk) | Tablo 5, Sec. 4.2 |
| Optimizer ve LR | Adam, 1e-4 | Sec. 3.2 |
| Batch boyutu | VGG için 3, diğerleri 9 (tutarsızlık olabilir) | Sec. 3.2 |
| Erken durdurma | sabır 50, en fazla 200 epoch | Sec. 3.2/4.1 |
| Alan uyarlaması C ve LOO doğruluğu | C=0,001; LOO %76,7 | Sec. 4.2, Tablo 6 |
| Ön işleme süresi hacim başına | 7-15 dk, ortalama ~12 dk | Fig. 2 |
| Seyreklik kırpma öncesi/sonrası | %78 → %54 | Sec. 2.1 |
| ADNet-DA MCI satırı karışıklık | CN 51,6 / MCI 37,7 / AD 10,7 | Tablo 7 |
| Toplam eğitim süresi ve deney sayısı | ~4 gün, 121 deney | Sec. 4.2 |

## 14. Kaynaklar
- https://pmc.ncbi.nlm.nih.gov/articles/PMC7661929/
- https://www.frontiersin.org/articles/10.3389/fbioe.2020.534592/full
- https://github.com/gfolego/alzheimers
- https://github.com/gfolego/alzheimers/tree/master/src
- https://doi.org/10.6084/m9.figshare.11908536
