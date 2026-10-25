# P05 — Yagis 2021 — Beyin MRI sınıflandırmasında veri sızıntısının etkisi

> **Durum:** ☐ okunmadı · ☑ AI özeti hazır · ☑ Opus doğrulandı (**ÇELİŞKİ YOK**, güven: yüksek) · ☐ insan okudu · ☐ implemente edildi
> **Sorumlu:** Baran Yeşilyurt · **Grup:** A · **Tam metin (ücretsiz):** https://www.nature.com/articles/s41598-021-01681-w · **Kod:** — (kod yok)
> **AI okuma kaynağı:** Tam metin okundu: https://pmc.ncbi.nlm.nih.gov/articles/PMC8604922/ (özet, veri kümeleri, yöntem, Tablo 4-5, tartışma, sınırlılıklar, kod erişimi; sayfanın son ~4.7 bin karakteri, yani kaynakça sonu, okunmadı). nature.com adresi giriş yönlendirmesi (303) verdi, okunamadı. Kod deposu GitHub ana sayfası okundu (https://github.com/Imaging-AI-for-Health-virtual-lab/Slice-Level-Data-Leakage); depo içi dosyalar ayrıca açılmadı. Supplementary tablolar (S1-S8) okunmadı.

> ⚠ **Nasıl okunmalı:** §2–§12 Sonnet okuyucunun özetidir; §13 Opus hakeminin makaleye karşı denetimidir. §13'te "yanlış" işaretli her sayı için **makaledeki değer** geçerlidir; §13'teki düzeltmeler §4–§8'in üstünde okunur. Hiçbir ajan makalenin yerine geçmez: implementasyondan önce ilgili bölümü (§6, §7) makaleden bir kez daha kendin oku.

## 1. Künye
Yagis E., Atnafu S.W., García Seco de Herrera A., Marzi C., Scheda R., Giannelli M., Tessa C., Citi L., Diciotti S. (2021). Effect of data leakage in brain MRI classification using 2D convolutional neural networks. Scientific Reports 11:22544. DOI 10.1038/s41598-021-01681-w

## 2. Tek paragraf özet
Makale, 3B beyin MRI hacimlerinden alınan 2B kesitlerle çalışan CNN'lerde "kesit düzeyinde" (slice-level) bölmenin veri sızıntısı yarattığını deneyle gösterir. Aynı denekten gelen kesitler hem eğitim hem test kümesine düşünce kesitler birbirine çok benzediği için model deneği "ezberler". Üç 2B CNN (VGG16-v1, VGG16-v2, ResNet-18) AD/HC (OASIS, ADNI) ve PD/HC (PPMI, Versilia) görevlerinde hem denek düzeyinde hem kesit düzeyinde iç içe (nested) çapraz doğrulamayla eğitildi. Denek düzeyinde test doğruluğu büyük kümelerde %71'in, küçüklerde %59'un altında kalırken kesit düzeyinde %92-99'a çıktı (Tablo 4). Etiketler rastgele atandığında bile kesit düzeyi bölme %93-96 doğruluk verdi, denek düzeyi ~%50 (şans düzeyi) verdi. Sonuç: 3B hacimlerden türetilen 2B girdilerde bölme mutlaka denek düzeyinde olmalı; bizim PROTOKOL madde 1'in doğrudan kanıtıdır. Makale yeni bir yüksek doğruluk yöntemi sunmaz; gerçek performans (~%66-70 AD/HC) düşük ve aşırı uyum belirgindir.

## 3. Problem ve katkı
- Problem: 2B CNN + 3B MRI çalışmalarında kesit düzeyi rastgele bölme, aynı deneğin kesitlerini eğitim ve teste dağıtarak şişirilmiş sonuç üretir.
- Katkı 1: Dört veri kümesi (OASIS-200, ADNI, PPMI, Versilia) ve üç mimaride kesit vs denek düzeyi bölmenin kontrollü, nested CV ile karşılaştırması (Tablo 4).
- Katkı 2: Rastgele etiketli OASIS (OASIS-random) deneyi: sızıntı varken etiket anlamsız olsa da %93-96 doğruluk (Tablo 4), sızıntının ezber olduğunun kanıtı.
- Katkı 3: Küçük örneklemde (OASIS-34) sızıntı etkisi daha büyük (fark ~41-45 puan) ve kesit düzeyinde küçük küme büyükten daha yüksek skor veriyor (Tablo 4, Tartışma).
- Katkı 4: Önceki literatürü sızıntı riskine göre sınıflayan Tablo 1-3 (net / şüpheli / yetersiz bilgi).
- Katkı 5: Açık kod ve Docker imajı (tekrarlanabilirlik).
- Öneri: 3B model + denek düzeyi bölme, CV yönteminin belgelenmesi, kod paylaşımı, kör dış test.

## 4. Veri seti ve bölme
- Kaynaklar: OASIS-1 (AD vs HC), ADNI (ADNI 2, 3T), PPMI (PD vs HC), özel Versilia veri kümesi (§Datasets, Tablo 5).
- Denek sayıları: OASIS-200 = 100 AD + 100 HC; OASIS-34 = 17 AD + 17 HC (OASIS-200'den 10 örnek); ADNI = 100 AD + 100 HC (denek başına ilk tarama); PPMI = 100 PD + 100 HC; Versilia = 17 PD + 17 HC (Tablo 5).
- Sınıf dağılımı dengeli (1:1). OASIS etiketi: CDR 0 = HC, CDR >=0.5 = AD.
- Her hacimden entropiye göre en yüksek 8 aksiyel kesit alındı: OASIS-200 için 200x8 = 1600 kesit (türetilmiş, makalede açıkça toplam yazılmadı - doğrulanamadı).
- Bölme: iki strateji. Denek düzeyi (doğru): deneğin tüm kesitleri aynı katlama. Kesit düzeyi (sızıntılı): kesitler havuzlanıp rastgele bölünür.
- CV: nested CV; dış döngü test tahmini, iç döngü hiperparametre seçimi. Metin "tenfold" der, Tablo 4 başlığı "fivefold nested" der: tutarsızlık (doğrulanamadı hangisi doğru).
- Dış test: ayrı bir bağımsız dış test kümesi yok; tüm sonuçlar CV dış katlarından. Kesit sayısı değil kesit doğruluğu raporlanıyor, denek düzeyi oylama/toplama yok.

**Sızıntı riski (AI):** orta — Makalenin konusu sızıntıyı yaratmak ve ölçmektir; "doğru" kolda denek düzeyi bölme kullanılır, nested CV ile hiperparametre seçimi dış testten ayrılmıştır. Bu açıdan kendi sonuçları temizdir. Riskler: (1) ADNI örneklemi denek başına ilk taramadır, iyi; ama dış bağımsız test yok. (2) Fold sayısı çelişkisi (10 vs 5). (3) Geç bölme/artırma-önce-böl ve test üzerinde hiperparametre ayarı sızıntıları test edilmedi (yazarların kendi sınırlılığı). (4) Ön işleme (z-score maske içi, entropi seçimi) denek içi olduğundan sızıntı sayılmaz. Orta işaretlendi çünkü kesit doğruluğu denek düzeyinde toplanmıyor ve dış test yok; makale 'sızıntıyı gösteren' bir kanıt olarak güvenilir.

## 5. Ön işleme
- OASIS: halka açık işlenmiş veri (gain-field düzeltme, beyin maskesi, Talairach atlasına kayıt); matris 176x208x176, 1 mm izotropik (§Preprocessing).
- Diğer kümeler: ANTs SyN (v2.1.0, varsayılan parametre) ile MNI152'ye (1 mm, FSL 6.0.3) kayıt, şablon beyin maskesi uygulama; matris 182x218x182.
- Kesit seçimi: her aksiyel kesit için Shannon entropisi (Eq. 1), en yüksek 8 kesit.
- Yeniden boyutlandırma: 224x224 (kübik spline, OpenCV).
- Standardizasyon: beyin maskesi içindeki ortalama/SD ile voksel bazlı z-score.
- N4 bias düzeltme ve HD-BET benzeri ayrı kafatası ayıklama adımı metinde yer almıyor (README'de skull-stripping var; ayrıntı doğrulanamadı).

## 6. Mimari
| Katman/Blok | Çekirdek | Kanal | Çıktı | Not |
|---|---|---|---|---|
| VGG16-v1: 5 konvolüsyon bloğu (ImageNet ön eğitimli) | 3x3 (standart VGG16) | 64-128-256-512-512 (standart VGG16, makalede ayrıca yazılmadı) | 7x7x512 (224 girdi için standart; doğrulanamadı) | Yalnız üst FC katmanları eğitilir (metin) / son 3 FC ince ayar (Şekil 2 yazısı): tutarsız |
| VGG16-v1: 3 FC katman (ReLU, Xavier) | - | - | sınıf çıktısı | Rastgele başlatılmış |
| VGG16-v2: 5 konv bloğu + global average pooling | 3x3 | aynı | sınıf çıktısı | Tüm katmanlar ince ayar |
| ResNet-18 (ImageNet ön eğitimli) | 7x7 stem + 3x3 kalıntı bloklar (standart) | 64-512 | 1 sigmoid | Fazladan 1 FC + sigmoid; tüm katmanlar ince ayar |

- Parametre sayısı: makalede verilmedi (doğrulanamadı).
- Girdi: 224x224 2B aksiyel kesit (tek kanal, ön eğitimli ağa uyum için kanal çoğaltma muhtemel; doğrulanamadı). Modeller 2B'dir; 3B girdi yok.

## 7. Eğitim ayarları
- Optimizer: Adam. Batch: 128. Epoch: 50 (§Methods).
- LR ızgarası: {1e-5, 3e-5, 1e-4, 3e-4, 1e-3}; LR decay ızgarası: {0, 0.1, 0.3, 0.5}; iç katlarda ızgara aramasıyla seçildi.
- Erken durdurma: belirtilmemiş. Kayıp fonksiyonu: açıkça yazılmadı (ikili sınıflandırma, muhtemelen binary cross-entropy; doğrulanamadı).
- Veri artırma: belirtilmemiş (geç bölme/artırma testi yapılmadı, yazarların sınırlılığı).
- Donanım: NVIDIA TITAN X (Pascal) 12 GB, 64 GB RAM, 8 CPU; Python 3.6.8, TensorFlow-gpu 1.12.0, Keras 2.2.4, CUDA 9.0.
- Süre: 34 denek için VGG16-v1 5.68 sa, v2 5.63 sa, ResNet-18 2.94 sa; 200 denek için 33.93 / 33.82 / 14.12 sa. Toplam yaklaşık 17 gün (§Hardware).
- Aşırı uyum: denek düzeyinde eğitim doğruluğu %73-100, test %43-71 (Tablo 4).

## 8. Sonuçlar
| Görev | Metrik | Değer | Test seti | Kaynak |
|---|---|---|---|---|
| AD/HC OASIS-200, denek düzeyi | ort. kesit doğruluğu (test) | VGG16-v1 %66.00; v2 %66.13; ResNet-18 %68.87 | nested CV dış katları | Tablo 4 |
| AD/HC OASIS-200, kesit düzeyi | ort. kesit doğruluğu (test) | %94.18 / %96.99 / %98.96 | aynı | Tablo 4 |
| AD/HC OASIS-34, denek | doğruluk | %54.35 / %54.34 / %57.49 | aynı | Tablo 4 |
| AD/HC OASIS-34, kesit | doğruluk | %99.19 / %99.33 / %98.96 | aynı | Tablo 4 |
| OASIS-random, denek | doğruluk | %53.37 / %49.25 / %50.80 | aynı | Tablo 4 |
| OASIS-random, kesit | doğruluk | %95.93 / %94.81 / %93.74 | aynı | Tablo 4 |
| AD/HC ADNI, denek | doğruluk | %70.12 / %66.49 / %68.68 | aynı | Tablo 4 |
| AD/HC ADNI, kesit | doğruluk | %95.31 / %95.24 / %96.87 | aynı | Tablo 4 |
| PD/HC PPMI, denek | doğruluk | %48.24 / %46.93 / %48.06 | aynı | Tablo 4 |
| PD/HC PPMI, kesit | doğruluk | %93.99 / %94.37 / %96.12 | aynı | Tablo 4 |
| PD/HC Versilia, denek | doğruluk | %53.86 / %42.97 / %51.36 | aynı | Tablo 4 |
| PD/HC Versilia, kesit | doğruluk | %95.97 / %97.80 / %92.63 | aynı | Tablo 4 |
| Şişirme farkı (kesit - denek) | puan | OASIS-200 28.18-30.86; ADNI 25.19-30.19; PPMI 44.06-47.44; Versilia 41.27-54.83; OASIS-34 41.47-44.99 | - | Tablo 4 |
| Özet inflasyon (özet bölümü) | % | ~30 (OASIS), 29 (ADNI), 48 (PPMI), 55 (Versilia) | - | Abstract (Tablo 4 farklarıyla birebir uyuşmuyor) |
| Wen ve ark. (alıntı) | dengeli doğruluk | %79 (denek) -> %100 (kesit), ADNI 330 HC + 336 AD | - | Tartışma |
AUC, F1, duyarlılık, özgüllük raporlanmadı; yalnız doğruluk.

## 9. Açıklanabilirlik / ek analiz
Makalede aciklanabilirlik/Grad-CAM analizi yok (ana metin ve okunan bölümlerde yer almıyor; README bağımlılıklarında keras-vis ve tf-explain geçtiği için kodda görselleştirme araçları var, makaledeki sonuçlarda kullanımı doğrulanamadı).

## 10. Kod ve tekrarlanabilirlik
- Depo: https://github.com/Imaging-AI-for-Health-virtual-lab/Slice-Level-Data-Leakage (4 yıldız, 0 fork, 70 commit); Docker: hub.docker.com/repository/docker/ai4healthvlab/slice-level-data-leakage.
- Lisans: LICENSE dosyası YOK (depo sayfasında lisans belirtilmemiş). Lisanssız kod varsayılan olarak tüm hakları saklıdır; protokolümüze göre KOPYALANMAZ, yalnız okunur.
- Çerçeve: Python, Keras/TensorFlow (keras-vis, image-classifiers, tf-explain; TF 1.12 çağı). Bizim PyTorch + MONAI ile uyumsuz.
- Dosyalar: model_training.py, config/ (JSON yapılandırma), data/, docs/, requirements_list.txt, README (ANTs/FSL ön işleme, Anaconda/Docker kurulumu).
- Ağırlık/veri: veri yok; eğitilmiş ağırlık yok görünüyor (pretrained_model yalnız mimari seçici; kesin değil). Denek kimlikleri Supplementary Tablo S4, S6, S7'de.
- Eksikler: lisans, PyTorch sürümü, ağırlıklar, fold sayısı netliği.

## 11. Güçlü ve zayıf yönler
**Güçlü:** Kontrollü karşılaştırma (aynı model/veri, yalnız bölme farklı); rastgele etiket deneyi sızıntının ezber olduğunu çok net kanıtlar; dört veri kümesi ve üç mimari; nested CV; kod ve Docker paylaşımı; literatürü sızıntı riskine göre sınıflayan tablolar.
**Zayıf:** Yalnız doğruluk raporlanıyor (AUC/F1/duyarlılık yok); denek düzeyi toplama yok, kesit doğruluğu raporlanıyor; fold sayısı (10 vs 5) ve VGG16-v1 eğitilen katmanlar tutarsız; aşırı uyum yüksek (eğitim ~%100, test ~%66), düzenlileştirme/erken durdurma/artırma yok; dış bağımsız test yok; küçük örneklem (200/34); eski yazılım (TF 1.12); kod lisanssız; ADNI 3T ADNI-2 verisi (bizim ADNI1 1.5T değil); hacmi 2B'ye indirgemek bizim 3B yaklaşımımızla uyumsuz.

## 12. Bizim projeye uyarlama
Kurulumumuz: ADNI1 1.5T başlangıç T1, NC/MCI/AD, HD-BET → N4 → z-score → MNI152 afin → 128³, RID düzeyinde 5-kat CV × 3 tohum, birincil görev AD-NC, ikincil 3-sınıf.

### 12.1 Okuyucunun uyarlama notu
**Aynen alınan fikir:** Denek (RID) düzeyinde bölme kuralı; sızıntı kontrolü için "rastgele etiket" sağlama deneyi; nested CV mantığı (iç döngüde hiperparametre); denek içi z-score.
**Değiştirilen:** 2B kesit yerine 3B 128³ hacim (bir denek = bir örnek, sızıntı yapısal olarak azalır); Keras/TF yerine PyTorch + MONAI; HD-BET + N4 + MNI afin; 5-kat CV x 3 tohum, RID'e göre stratified (StratifiedGroupKFold); AUC, dengeli doğruluk, F1-makro, duyarlılık, özgüllük; gerekirse denek başına birden çok tarama olursa aynı RID grupta tutulur (ADNI1 baseline tek tarama ama yinelenen RID kontrolü yap).
**Önerilen ek deney:** Kendi veride "rastgele etiket" testi: etiketleri karıştırıp denek düzeyi bölmede ~%50 (AUC ~0.5) beklenir; çıkmazsa boru hattında sızıntı vardır. İsteğe bağlı: bilinçli kesit-düzeyi sızıntı kolu gösterimle rapor (yalnız kanıt amaçlı, sonuçlara karıştırma).
**Kod:** Lisanssız depo kopyalanmaz; bölme ve rastgele etiket mantığı kendi kodumuzla yeniden yazılır.
**Zorluk:** 2/5 (sızıntı testi ve bölme uygulaması kolay; makalenin kendi modellerini yeniden üretmeye gerek yok).
**VRAM/süre tahmini (tahmin):** 3B küçük ağ (ör. MONAI DenseNet/ResNet-10/18, batch 2-4, 128³, AMP) T4 16 GB'a sığar (~6-12 GB); rastgele etiket testi 1 kat x 1 tohum için ~30-60 dk, tam 5x3 koşu birkaç saat (tahmin).
**Protokole uymayan noktalar:** Makale AD/HC ile PD; bizim 3 sınıf (NC/MCI/AD) yok; ADNI-2 3T vs bizim ADNI1 1.5T; yalnız doğruluk metriği; makale ağdan elde edilen performans (~%66-70) hedefimizin (%85) çok altında olduğundan sonuç kıyası için kullanılmaz, yalnız sızıntı gerekçesi olarak atıf yapılır.

### 12.2 Hakemin kurulum farkı analizi
Sızıntı riski değerlendirmesi: özet 'orta' demiş, ben 'düşük' derim. Makalenin doğru kolu denek düzeyinde bölüyor ve hiperparametreleri iç katlarda seçiyor. Rastgele etiket kontrolü (~%50) boru hattının temiz olduğunu deneyle gösteriyor. Dış test olmaması ve kesitlerin denekte birleştirilmemesi sızıntı değil; genellenebilirlik ve raporlama sınırlılığı. Atıf amacına (PROTOKOL madde 1) güvenle hizmet eder.

Makale ile bizim kurulum arasındaki somut farklar ve beklenen etkileri:

1. **Veri:** Makale 100 AD + 100 HC ADNI-2 3T kullanıyor. Biz ADNI1 1.5T baseline ile ≈187 AD, 229 NC, 382 MCI denekle çalışıyoruz. Örneklemimiz daha büyük, ancak 1.5T'de kontrast daha düşük. MCI makalede hiç yok, yani 3 sınıflı görev için referans değeri yok.

2. **Girdi boyutu:** Makale denek başına 8 adet 2B 224x224 kesit kullanıyor; biz 3B 128³ hacim kullanıyoruz ve bir denek bir örnek oluyor. Kesit düzeyindeki sızıntı bizde yapısal olarak oluşamaz, ama aynı RID'in birden çok taraması gelirse sızıntı yine mümkün. 3B girdi bağlamı koruduğu için daha yüksek gerçek doğruluk beklenir (literatürde 3B ve denek düzeyi bölmeyle AD/NC ~%80-88).

3. **Ön işleme:** Makale OASIS'te Talairach'a hazır işlenmiş veri, diğer kümelerde ANTs SyN (doğrusal olmayan) ile MNI152 kaydı ve şablon maskesi kullanıyor; N4 yok. Biz HD-BET, N4 ve yalnız afin MNI152NLin2009cAsym kullanıyoruz. Afin kayıt anatomik hizalamayı SyN kadar sıkı yapmaz, dolayısıyla modelin bireysel varyasyonu öğrenmesi gerekir. Maske içi z-score iki kurulumda da aynı.

4. **Bölme:** Makale nested CV kullanıyor (kat sayısı belirsiz: 5 mi 10 mu); biz RID düzeyinde 5-kat ve 3 tohum kullanıyoruz. Makaledeki iç döngü bizde yoksa hiperparametre seçimi test katına sızabilir. Ya iç doğrulama ayrımı yapılmalı ya da hiperparametreler önceden sabitlenmeli.

5. **Görev ve metrik:** Makale yalnız doğruluk raporluyor (AD/HC ve PD/HC). Biz dengeli doğruluk, AUC, F1-makro, duyarlılık ve özgüllük raporluyoruz. Sınıflar dengesiz olduğu için (NC 229 / AD 187, MCI 382) dengeli metrikler şart; makalenin 1:1 dengeli kurgusu bunu gerektirmiyordu.

6. **Çerçeve:** Makale Keras/TF 1.12 kullanıyor, biz PyTorch + MONAI. Kod doğrudan taşınamaz ve depo lisanssız olduğu için kopyalanmaz.

7. **Sonuçların kıyaslanması:** Makalenin performansı (~%66-70) hedefimiz olan ≥%85 için kıyas noktası değil. Yalnız 'sızıntı ~25-30 puanlık sahte artış üretir' kanıtı olarak atıf yapılmalı.

### 12.3 İmplementasyon yapılacaklar (hakem)
1. **Bölmeyi denek düzeyinde kur.** Bölmeyi RID'e göre `sklearn.model_selection.StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=tohum)` ile yap (groups=RID, y=etiket), 3 tohumu da kaydet. Katların CSV'lerini diske yaz ve her katta eğitim ile test RID kümelerinin kesişiminin boş olduğunu `assert` ile doğrula.

2. **Tekrarlanan RID'leri kontrol et.** ADNI1 baseline tablosunda aynı RID'in birden çok tarama veya görüntü kimliği taşıyıp taşımadığına bak (ör. `df.RID.duplicated()`); varsa tek tarama tut ya da hepsini aynı grupta bırak.

3. **Hiperparametreleri teste sızdırma.** Her dış katın eğitim kısmından RID düzeyinde ayrı bir doğrulama kümesi ayır (~%15-20, yine grup bazlı). LR, epoch ve erken durdurma yalnız bu kümeye göre seçilsin; test katı sadece son raporda kullanılsın.

4. **Veri hattını MONAI ile kur.** `monai.data.CacheDataset` veya `PersistentDataset` kullan; dönüşümler `LoadImaged`, `EnsureChannelFirstd`, `NormalizeIntensityd(nonzero=True)` (maske içi z-score, makaleyle uyumlu) ve gerekiyorsa `Resized((128,128,128))`. Veri artırmayı (`RandFlipd`, `RandAffined`) yalnız eğitim dönüşümlerine koy; artırmadan önce bölme yapılmış olsun.

5. **Model ve eğitim ayarları.** Model olarak `monai.networks.nets.DenseNet121(spatial_dims=3, in_channels=1, out_channels=2)` veya `monai.networks.nets.resnet18(spatial_dims=3, n_input_channels=1, num_classes=2)` kullan. Ayarlar: AdamW, LR ızgarası makaleden esinle {1e-5, 1e-4, 3e-4}; batch 2-4; AMP (`torch.cuda.amp`) açık; T4 16 GB'a sığmalı.

6. **Rastgele etiket kontrolünü ekle.** Makalenin OASIS-random fikrini uygula: etiketleri tohumla karıştır, aynı RID katlarıyla eğit. Beklenen sonuç dengeli doğruluk ≈ 0.5 ve AUC ≈ 0.5; anlamlı ölçüde yüksek çıkarsa boru hattında sızıntı vardır. Bunu ayrı bir betik (ör. `sizinti_testi.py`) olarak tut, sonuç tablosuna karıştırma.

7. **Metrikleri denek düzeyinde hesapla.** Dengeli doğruluk (`sklearn.metrics.balanced_accuracy_score`), AUC (`roc_auc_score`), F1-makro, duyarlılık ve özgüllük raporla; 5 kat x 3 tohum üzerinden ortalama ± SD ver. 3B'de bir örnek bir denek olduğundan birleştirme sorunu yok; makaledeki 'kesit doğruluğu' tuzağına düşülmez.

8. **Kodu kopyalama.** Depo (Slice-Level-Data-Leakage) lisanssız, dolayısıyla hiçbir dosyası kopyalanmaz. `model_training.py` yalnız nested CV mantığını anlamak için okunabilir; bölme ve test mantığını kendi kodumuzla yaz.

9. **İsteğe bağlı gösterim kolu.** Yalnız ek materyal olarak, 2B kesit çıkarıp kesitleri havuzda rastgele bölen kasıtlı sızıntılı bir kol çalıştır ve şişmeyi göster (makalede ~25-30 puan). Bu kolu ana sonuçlarda kullanma, açıkça 'sızıntılı' diye etiketle.

10. **Raporlama.** Protokolde makaleyi yalnız denek düzeyinde bölmenin gerekçesi olarak an. Makalenin kendi içindeki iki tutarsızlığı (5 ile 10 kat; VGG16-v1'in eğitilen katmanları) dipnotta belirt ve performans kıyaslamasında kullanma.

## 13. Opus doğrulama
- **Sonuç:** **ÇELİŞKİ YOK** · **Güven:** yüksek
- **Hakemin okuduğu kaynak:** Tam metni PMC'den okudum (https://pmc.ncbi.nlm.nih.gov/articles/PMC8604922/). Sayfanın ilk 100.000 karakterini iki ayrı sorguyla taradım: özet, veri kümeleri, Tablo 5, ön işleme, modeller ve Şekil 2 alt yazısı, eğitim, CV, donanım, Tablo 4'ün tamamı, tartışma, sınırlılıklar ve kod erişimi. Son ~4,7 bin karakter (kaynakça sonu) okunmadı. GitHub deposunun ana sayfasını da okudum (https://github.com/Imaging-AI-for-Health-virtual-lab/Slice-Level-Data-Leakage). Ek tabloları (S1-S8) ve depo içindeki dosyaları açmadım. nature.com sürümünü denemedim.

### 13.1 Kontrol edilen sayılar
| İddia | Özetteki değer | Makaledeki değer | Durum | Yer |
|---|---|---|---|---|
| OASIS-200 denek sayısı | 100 AD + 100 HC | OASIS-1'den 100 AD + 100 HC (1.5T Siemens Vision, MPRAGE) | **doğru** | Yöntem/Veri kümeleri, Tablo 5 |
| ADNI denek sayısı | 100 AD + 100 HC (ADNI 2, 3T, ilk tarama) | ADNI 2'den 100 AD + 100 HC, katılımcı başına ilk tarama, 3T (6 Siemens + 6 Philips) | **doğru** | Tablo 5 |
| OASIS-34 denek sayısı | 17 AD + 17 HC, 10 örnek | OASIS-200'den bağımsız olarak 10 kez örneklenmiş, her biri 17 AD + 17 HC | **doğru** | Yöntem/Veri kümeleri |
| Denek başına kesit sayısı | Entropisi en yüksek 8 aksiyel kesit | Shannon entropisine göre en üstteki 8 aksiyel kesit | **doğru** | Ön işleme |
| Kesit boyutu | 224x224 | 224x224, kübik spline | **doğru** | Ön işleme |
| Batch / epoch / optimizer | 128 / 50 / Adam | 128 / 50 / Adam | **doğru** | Yöntem (Eğitim) |
| LR ızgarası | 1e-5, 3e-5, 1e-4, 3e-4, 1e-3; decay 0, 0.1, 0.3, 0.5 | LR {1e-5, 3e-5, 1e-4, 3e-4, 1e-3}; decay {0, 0.1, 0.3, 0.5}; iç katlarda ızgara aramasıyla | **doğru** | Yöntem |
| OASIS-200 test doğruluğu, denek düzeyi | %66.00 / %66.13 / %68.87 | 66.0 / 66.13 / 68.87 | **doğru** | Tablo 4 |
| OASIS-200 test doğruluğu, kesit düzeyi | %94.18 / %96.99 / %98.96 | 94.18 / 96.99 / 98.96 | **doğru** | Tablo 4 |
| ADNI test doğruluğu, denek / kesit | %70.12/%66.49/%68.68 ; %95.31/%95.24/%96.87 | 70.12/66.49/68.68 ; 95.31/95.24/96.87 | **doğru** | Tablo 4 |
| OASIS-random doğruluğu | Kesit 95.93/94.81/93.74; denek 53.37/49.25/50.80 | Kesit 95.93/94.81/93.74; denek 53.37/49.25/50.8 | **doğru** | Tablo 4 |
| CV kat sayısı | Metinde 10, Tablo 4'te 5 (tutarsız) | Metin 'tenfold CV' diyor, Tablo 4 başlığı 'fivefold nested CV' diyor | **doğru** | Yöntem ve Tablo 4 başlığı |
| Donanım | NVIDIA TITAN X Pascal 12 GB | TITAN X (Pascal) 12 GB, 64 GB RAM, 8 CPU | **doğru** | Donanım |
| Eğitim süresi, 200 denek | VGG16 33.9 sa, ResNet-18 14.1 sa | VGG16-v1 33.93 sa, VGG16-v2 33.82 sa, ResNet-18 14.12 sa; toplam ~17 gün | **doğru** | Donanım |
| Özetteki şişme yüzdeleri | ~%30 OASIS, 29 ADNI, 48 PPMI, 55 Versilia | ~%30 OASIS, %29 ADNI, %48 PPMI, %55 Versilia; rastgele etikette kesit ~%96, denek %50 | **doğru** | Abstract |
| Wen ve ark. alıntısı | Dengeli doğruluk %79 -> %100 (ADNI 330 HC + 336 AD) | ADNI 330 HC / 336 AD; doğrulamada dengeli doğruluk denek düzeyinde %79, kesit düzeyinde %100 | **doğru** | Tartışma |
| Şişme farkı aralıkları (kesit eksi denek) | OASIS-200 28.18-30.86; ADNI 25.19-30.19; PPMI 44.06-47.44; Versilia 41.27-54.83; OASIS-34 41.47-44.99 | Aynı (Tablo 4'teki fark sütunu) | **doğru** | Tablo 4 |
| PPMI ve Versilia denek/kesit doğrulukları | PPMI 48.24/46.93/48.06 ; 93.99/94.37/96.12 — Versilia 53.86/42.97/51.36 ; 95.97/97.80/92.63 | Aynı | **doğru** | Tablo 4 |
| VGG16-v1'de eğitilen katmanlar tutarsız | Metin: yalnız üst FC katmanı; Şekil 2: son 3 FC | Metin: son FC katmanı dışında tüm katmanlar dondurulmuş; Şekil 2 alt yazısı: yalnız son üç FC katmanı ince ayarlanıyor | **doğru** | Yöntem ve Şekil 2 alt yazısı |
| OASIS etiketleme kuralı | CDR 0 = HC, CDR >= 0.5 = AD | Okuduğum bölümlerde CDR eşiğini bulamadım | **doğrulanamadı** | Veri kümeleri |

### 13.2 Düzeltmeler (özette yanlış/eksik → doğrusu)
- Aşırı uyum cümlesi şöyle olmalı: 'Denek düzeyinde eğitim doğruluğu %63.38 (OASIS-random) ile %100 arasında, test doğruluğu %42.97 ile %70.12 arasında.' Özetteki '%73-100' alt sınırı, rastgele etiketli kol hariç tutulursa doğru (73.19, PPMI VGG16-v2); kol dahil edildiğinde alt sınır 63.38.
- Şu cümle düzeltilmeli: 'OASIS-34'te kesit düzeyi skoru OASIS-200'den daha yüksek.' VGG16 modellerinde bu doğru, ancak ResNet-18'de iki küme de 98.96 ile eşit. Makale bu durumu 'küçük kümede hatalı biçimde daha iyi sonuç' olarak niteliyor.
- Özetteki 'ResNet-18: 1 sigmoid' doğru; makaleye göre eklenen katman rastgele başlatılıyor ve aktarılan tüm katmanlar ince ayarlanıyor.
- Kafatası ayıklama: ayrı bir HD-BET benzeri adım yok, ancak beyin maskesi uygulanıyor. OASIS için hazır işlenmiş veri kullanılmış (gain-field düzeltme ve beyin maskeleme); diğer kümelerde MNI152 şablon maskesi uygulanıyor. N4 metinde hiç geçmiyor. Özetin bu ifadesi doğru, yalnız 'README'de skull-stripping var' notunu doğrulayamadım.
- Kesit sayısı (OASIS-200 için 200x8 = 1600) makalede açıkça yazmıyor; özet bunu zaten 'türetilmiş' olarak işaretlemiş, yerinde.
- Rastgele etiket deneyi için makalenin kendi özeti kesit düzeyinde '~%96' diyor; Tablo 4'teki değerler 93.74-95.93 aralığında. Özetteki '%93-96' Tablo 4 ile uyumlu.

### 13.3 Özetin atladığı önemli noktalar
- Makale her kesiti bağımsız sınıflandırıyor ve denek düzeyinde birleştirme (oylama) yapmıyor. Bu yüzden denek düzeyindeki ~%66-70 bir 'denek doğruluğu' değil, kesit doğruluğu.
- OASIS-34'ün 10 kopya halinde örneklendiği yazıyor, ama sonuçların 10 kopyanın ortalaması mı olduğu ve varyansı makalede açıkça verilmiyor. Tablo 4 standart sapma da vermiyor.
- Yazarların kendi sınırlılığı: geç bölme ve test kümesinde hiperparametre ayarı gibi diğer sızıntı türleri incelenmedi; denek düzeyinde ciddi aşırı uyum var.
- Veri kümeleri tarayıcı açısından heterojen: PPMI'de 1.5T ve 3T karışık, birden çok üretici; ADNI-2'de 6 Siemens ve 6 Philips 3T tarayıcı. Denek düzeyinde PD/HC sonuçları şans düzeyinde (~%43-54), yani PPMI/Versilia'da gerçek sinyal neredeyse yok.
- Ablation yok: kesit sayısı (8), entropi seçimi, girdi boyutu ya da veri artırmanın etkisi test edilmedi.
- Bağımsız bir dış test kümesi kullanılmadı; bütün sonuçlar nested CV'nin dış katlarından geliyor.
- Demografi verilmiş (yaş ve cinsiyet, Tablo 5), ama sınıflar arası yaş/cinsiyet karıştırıcı etkisi analiz edilmemiş.
- Makale CC BY 4.0 lisanslı; kod için ayrı bir lisans belirtilmemiş ve depo sayfasında görünür bir LICENSE dosyası yok.

### 13.4 Doğrulanamayanlar
- OASIS etiketleme kuralı (CDR 0 = HC, CDR >= 0.5 = AD): okuduğum bölümlerde bulamadım
- README'de skull-stripping adımının geçip geçmediği (depo dosyalarını açmadım)
- Depoda eğitilmiş ağırlık olup olmadığı
- Kayıp fonksiyonu (makalede yazmıyor; binary cross-entropy yalnız bir tahmin)
- Tablo 4'teki 5-kat ile metindeki 10-kat arasında hangisinin doğru olduğu
- Ek tablolardaki (S4, S6, S7) denek kimlik listeleri
- Kodda keras-vis ve tf-explain araçlarının makaledeki sonuçlarda kullanılıp kullanılmadığı

### 13.5 Okuyucunun işaretlediği anahtar sayılar (ham)
| İddia | Değer | Yer |
|---|---|---|
| OASIS-200 denek sayısı | 100 AD + 100 HC | Tablo 5 / §Datasets |
| ADNI denek sayısı | 100 AD + 100 HC (ADNI 2, 3T, ilk tarama) | Tablo 5 |
| OASIS-34 denek sayısı | 17 AD + 17 HC, 10 örnek | Tablo 5 |
| Denek başına kesit sayısı | En yüksek entropili 8 aksiyel kesit | §Preprocessing |
| Kesit boyutu | 224x224 | §Preprocessing |
| Batch / epoch / optimizer | 128 / 50 / Adam | §Methods (Training) |
| LR ızgarası | 1e-5, 3e-5, 1e-4, 3e-4, 1e-3; decay 0, 0.1, 0.3, 0.5 | §Methods |
| OASIS-200 test doğruluğu denek düzeyi | %66.00 (VGG16-v1), %66.13 (v2), %68.87 (ResNet-18) | Tablo 4 |
| OASIS-200 test doğruluğu kesit düzeyi | %94.18 / %96.99 / %98.96 | Tablo 4 |
| ADNI test doğruluğu denek / kesit | %70.12/%66.49/%68.68 ; %95.31/%95.24/%96.87 | Tablo 4 |
| OASIS-random kesit düzeyi doğruluk | %95.93 / %94.81 / %93.74 (denek ~%50: 53.37/49.25/50.80) | Tablo 4 |
| CV katlama sayısı | Metinde 10, Tablo 4'te 5 (tutarsız) | §Methods vs Tablo 4 |
| Donanım | NVIDIA TITAN X Pascal 12 GB | §Hardware |
| Eğitim süresi 200 denek | VGG16 33.9 sa, ResNet-18 14.1 sa | §Hardware |
| Özet inflasyon yüzdeleri | ~%30 OASIS, 29 ADNI, 48 PPMI, 55 Versilia | Abstract |
| Wen ve ark. alıntı | %79 dengeli doğruluk -> %100 | Tartışma |

## 14. Kaynaklar
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8604922/
- https://www.nature.com/articles/s41598-021-01681-w
- https://github.com/Imaging-AI-for-Health-virtual-lab/Slice-Level-Data-Leakage
- https://hub.docker.com/repository/docker/ai4healthvlab/slice-level-data-leakage
- DOI 10.1038/s41598-021-01681-w
