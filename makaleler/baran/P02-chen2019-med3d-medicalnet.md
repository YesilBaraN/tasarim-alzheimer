# P02 — Chen 2019 — Med3D / MedicalNet: 3B tıbbi görüntü için transfer öğrenme

> **Durum:** ☐ okunmadı · ☑ AI özeti hazır · ☑ Opus doğrulandı (**ÇELİŞKİ VAR**, güven: yüksek) · ☐ insan okudu · ☐ implemente edildi
> **Sorumlu:** Baran Yeşilyurt · **Grup:** A · **Tam metin (ücretsiz):** https://arxiv.org/abs/1904.00625 · **Kod:** https://github.com/Tencent/MedicalNet (MIT)
> **AI okuma kaynağı:** Tam metin olarak OKUNAN: (1) https://ar5iv.labs.arxiv.org/html/1904.00625 (Bölüm 1-5, Tablo 1-4 okundu; ar5iv dönüşümü olduğundan sayfa numarası yok, yerler bölüm/tablo ile verildi; hangi arXiv sürümünün dönüşümü olduğu belirtilmiyor). (2) https://arxiv.org/html/1904.00625v4 (v4 HTML; §3-§4 eğitim ayrıntıları, Şekil 4 deneyi, Kinetics tabanı için tarandı). (3) https://arxiv.org/abs/1904.00625 (künye, sürüm geçmişi). https://arxiv.org/pdf/1904.00625 PDF olarak indi ama WebFetch ikili akışı çözemedi, METİN OKUNAMADI. Şekil 2 (mimari), Şekil 4-6 (veri miktarı, yakınsama eğrileri) görsel olarak görülmedi; yalnız metin ve alt yazı düzeyinde bilgi var. Kod deposu: https://github.com/Tencent/MedicalNet ana sayfası, LICENSE, models/resnet.py, setting.py okundu. train.py, model.py ve requirements.txt içeriği okunmadı.

> ⚠ **Nasıl okunmalı:** §2–§12 Sonnet okuyucunun özetidir; §13 Opus hakeminin makaleye karşı denetimidir. §13'te "yanlış" işaretli her sayı için **makaledeki değer** geçerlidir; §13'teki düzeltmeler §4–§8'in üstünde okunur. Hiçbir ajan makalenin yerine geçmez: implementasyondan önce ilgili bölümü (§6, §7) makaleden bir kez daha kendin oku.

## 1. Künye
Chen S., Ma K., Zheng Y. (2019). Med3D: Transfer Learning for 3D Medical Image Analysis. arXiv:1904.00625 [cs.CV]. Sürümler: v1 1 Nisan 2019, v2 9 Nisan 2019, v3 10 Haziran 2019, v4 17 Temmuz 2019 (güncel). Hakemli dergi/konferans yayını belirtilmiyor (yalnız ön baskı). Yazarlar Tencent Jarvis Lab. DOI: 10.48550/arXiv.1904.00625.

## 2. Tek paragraf özet
Makale, 3B tıbbi görüntü analizinde ImageNet benzeri büyük ve hazır bir ön eğitim kaynağı olmadığı sorununa yanıt arıyor. Yazarlar sekiz farklı 3B segmentasyon veri kümesini (BraTS, Hippo, Prostate, LiTS, Heart, Pancreas, Vessel, Spleen; toplam 1.638 vaka, MR ve BT karışık) birleştirip 3DSeg-8 adını veriyor. Bu veri üzerinde ResNet-10 ile 200 arası 3B ağları, her veri kümesine ayrı bir kod çözücü dalı olan çok dallı bir yapıyla ön eğitiyor (Med3D). Ön eğitilmiş kodlayıcı akciğer segmentasyonuna (Visceral), akciğer nodülü iyi/kötü huylu sınıflandırmasına (LIDC) ve karaciğer segmentasyonuna (LiTS) aktarılıyor. Med3D, sıfırdan eğitime (TFS) ve Kinetics video ön eğitimine (Kin) göre belirgin biçimde daha iyi: ör. ResNet-18 akciğer Dice %87,26 (TFS %75,22, Kin %83,21), nodül doğruluğu %88,89 (TFS %80,80, Kin %82,83), Tablo 3. Özet, yakınsamanın Kinetics'e göre yaklaşık 2, sıfırdan eğitime göre yaklaşık 10 kat hızlandığını ve doğrulukta %3 ile %20 kazanç olduğunu söylüyor; 2x ve 10x iddiaları gövde metninde sayısallaştırılmamış (yalnız Şekil 5-6'da eğri olarak). Önemli not: makale ve ön eğitimin hiçbiri Alzheimer veya beyin sMRI sınıflandırması içermiyor; bizim projede bu bir alan ve görev uyuşmazlığı riski olarak kalıyor. Kod ve ağırlıklar MIT lisanslı olarak açık.

## 3. Problem ve katkı
- **Problem:** 3B tıbbi görüntüde (BT/MR) küçük etiketli veri kümeleri var; 2B için ImageNet gibi bir 3B ön eğitim kaynağı yok. Kinetics (video) ön eğitiminin tıbbi hacimlere uygunluğu tartışmalı (§1: "güçlü yanlılık").
- **Katkı 1:** 3DSeg-8, farklı modalite/organ/patoloji içeren 8 kümeden oluşan çok alanlı 3B segmentasyon veri seti (Tablo 1, §4.1).
- **Katkı 2:** Çok dallı (8 dallı) kod çözücülü 3B ResNet ön eğitimi; her dal yalnız kendi veri kümesinden öğrenir, böylece eksik/farklı etiketler sorun olmaz (§3.2, §4.1, Şekil 2).
- **Katkı 3:** Aktarım deneyleri: akciğer seg., nodül sınıflama, LiTS karaciğer seg.; TFS ve Kin ile karşılaştırma (Tablo 3, 4).
- **Katkı 4:** Önceden eğitilmiş modellerin ve kodun yayımlanması (§5; depo: Tencent/MedicalNet, MIT).
- **Ek bulgular:** Ön eğitimde alan sayısı arttıkça (1, 2, 4, 8) tüm veri kümelerinde Dice yükseliyor (Tablo 2); eğitim verisi %10-20'ye düşünce keskin düşüş var (Şekil 4, ResNet-152, metinde "Fig. 3" olarak anılıyor).

## 4. Veri seti ve bölme
**Ön eğitim (3DSeg-8, Tablo 1, §4.1):** Brain/BraTS 485 (MR, tümör), Hippo 261 (MR), Prostate 33 (MR), Liver/LiTS 131 (BT), Heart 100 (MR), Pancreas 282 (BT), Vessel 304 (BT), Spleen 42 (BT); satır toplamı 1.638 (makalede toplam yazmıyor, tarafımızdan toplandı). Her kümede 90% eğitim / 10% test (§4.1). Alanlar arası denge: en büyük kümeden alıp diğerlerini artırma ile dengeleme (§4.1).
**Aktarım:** Akciğer seg. (Visceral): 80 hacim, 72 eğitim / 8 test, 4 modalite (§4.2). Nodül sınıflama (LIDC): 1.010 hasta, 1.050 nodül eğitim / 99 nodül test; etiket 1-3 iyi huylu, 4-5 kötü huylu (§4.2). LiTS: 201 BT, 131 eğitim / 70 test (test etiketleri gizli, sunucuyla değerlendirme) (§4.3).
**Bölme düzeyi:** Hasta/nodül düzeyi ayrımı (LIDC'de nodül sayısı hasta sayısından fazla, yani aynı hastadan nodüllerin eğitim ve teste dağılıp dağılmadığı belirtilmiyor, doğrulanamadı). Çapraz doğrulama yok, tek bölme, tekrarlı tohum yok. Sınıf dağılımı (iyi/kötü huylu oranı) verilmemiş (doğrulanamadı). Dış test: yok (LiTS gizli test hariç).

**Sızıntı riski (AI):** orta — Makale Alzheimer ile ilgili değil; bizim bölme protokolü açısından değerlendirme: (1) Tek sabit bölme, CV ve çok tohum yok, sonuç varyansı bilinmiyor. (2) LIDC'de 1.050 nodül eğitim / 99 test; bölmenin hasta düzeyinde yapılıp yapılmadığı belirtilmiyor, aynı hastanın nodülleri iki tarafa düşmüş olabilir (doğrulanamadı). (3) Test seti 99 nodül: bir vaka yaklaşık %1 puan eder, farklar gürültü içinde. (4) Hiperparametre/kontrol noktası seçimi için ayrı doğrulama kümesi anılmıyor; seçim test üzerinde yapılmış olabilir (doğrulanamadı). (5) Ön eğitim verisi (BraTS, Hippo vb.) ile bizim ADNI verisi arasında örtüşme olasılığı: Hippo (Medical Segmentation Decathlon) ve BraTS beyin MR içerir; MSD Hippocampus verisinin kaynağı ADNI değil, Vanderbilt'in çalışması (doğrulanamadı); ADNI örtüşmesi makaleden çıkarılamaz. Bizim tarafta asıl kural: ön eğitim ağırlığı denek sızıntısı yaratmaz ama bizim ince ayarda RID düzeyi bölme şart.

## 5. Ön işleme
- **Uzamsal (§3.1, Denklem 1):** Her alan için ortanca voksel aralığına yeniden örnekleme; kırpma, hedef sınırlayıcı kutunun 2 katından tüm hacme kadar değişir.
- **Yoğunluk (§3.1, Denklem 2):** 0,5-99,5 yüzdelik kırpma, ardından hacim başına z-score normalizasyonu.
- **LiTS (§4.3):** Pencereleme -200 ile 250 HU; iki aşama: kaba karaciğer ROI, sonra ince DenseASPP-3D segmentasyon.
- **Artırma (§4.1):** Hedef sınırlayıcı kutu kenarının %10'u içinde öteleme, [-5, 5] dönme (birim belirtilmemiş, muhtemelen derece), [0,8, 1,2] ölçekleme.
- **Girdi boyutu:** Makalede verilmemiş (doğrulanamadı). Depo varsayılanı 56x448x448 (setting.py; MRBrainS18 demosu içindir, makaleyle aynı olduğu doğrulanamadı).
- **Kafatası ayıklama, N4, kayıt:** Yok (BT ve farklı MR görevleri; beyin sMRI için standart hat tarif edilmiyor).

## 6. Mimari
| Katman/Blok | Çekirdek | Kanal | Çıktı | Not |
|---|---|---|---|---|
| Stem conv1 (depo, resnet.py) | 7x7x7, stride 2, pad 3 | 1 → 64 | girdi/2 | Tek kanallı girdi (§4.1: 3 → 1 kanal) |
| BN + ReLU + MaxPool | 3x3x3, stride 2 | 64 | girdi/4 | |
| layer1 | BasicBlock 3x3x3 (veya Bottleneck) | 64 (BB) / 256 (BN) | girdi/4 | stride 1, dilation 1 |
| layer2 | aynı | 128 / 512 | girdi/8 | stride 2 |
| layer3 | aynı | 256 / 1024 | girdi/8 | stride 1, dilation 2 (§4.1: 3. ve 4. blokta downsample yok, r=2) |
| layer4 | aynı | 512 / 2048 | girdi/8 | stride 1, dilation 4 (depo kodu; makale yalnız r=2'den söz ediyor, fark var) |
| Ön eğitimde çözücü (§4.1, Şekil 2) | 1x1x1 conv + yukarı örnekleme | 8 dal | girdi boyutu | Her dal bir veri kümesi |
| Depodaki conv_seg | ConvTranspose3d(k2,s2) → 32 → Conv3d 3x3x3 → Conv3d 1x1x1 | 32 → n_sınıf | girdi/4 | FC/sınıflandırma başı YOK |

**Katman sayıları (ResNet-18):** [2,2,2,2] BasicBlock. **Kısayol:** ResNet-10 B, ResNet-18 A, ResNet-34 A, ResNet-50 B, 101/152/200 B (depo README). Tip A: ortalama havuz + sıfır dolgu; tip B: 1x1x1 conv + BN (resnet.py).
**Parametre sayısı:** Makalede verilmemiş. Depo README tablosu: ResNet-10 14,36 M; ResNet-18 32,99 M; ResNet-34 63,31 M; ResNet-50 46,21 M; ResNet-101 85,31 M; ResNet-152 117,51 M; ResNet-200 126,74 M (Tesla P40 süre 0,18/0,19/0,22/0,21/0,29/0,34/0,45 s; neyi ölçtüğü belirtilmiyor). ResNet-34 > ResNet-50 sıralaması bir yazım hatası olabilir (doğrulanamadı); bu sayılar çözücü başını içerebilir.
**Girdi:** 1 kanallı 3B hacim; boyut makalede yok. Ağırlıkları kullanırken 1 kanal zorunlu (bizim T1 için uygun).

## 7. Eğitim ayarları
- **Ön eğitim (§4.1):** SGD, çapraz entropi kaybı, LR 0,1, momentum 0,9, weight decay 0,001. Batch boyutu, epoch, LR çizelgesi, girdi yaması, donanım ve süre verilmemiş (doğrulanamadı).
- **Akciğer seg. aktarım (§4.2):** Med3D ve Kin için Adam, başlangıç LR 0,001; sıfırdan eğitim (TFS) için LR 0,01. Bu §4.1'deki SGD ayarıyla çelişiyor/belirsiz (iki sürümde de aynı).
- **LiTS (§4.3):** "Önceki segmentasyon deneyleriyle aynı hiperparametreler."
- **Nodül sınıflama (§4.2):** Önceki görevle aynı optimizasyon denmiş, belirsiz. Sınıflayıcı başı ayrıntısı verilmemiş (doğrulanamadı).
- **Artırma:** §4.1 (yukarıda). **Erken durdurma:** belirtilmemiş.
- **Yakınsama (özet, Şekil 5-6):** Med3D, Kin'e göre yaklaşık 2x, TFS'ye göre yaklaşık 10x hızlı yakınsama iddiası yalnız özette; gövdede sayı yok, TFS eğrileri "çok daha dalgalı" (§4.2).
- **Depo varsayılanları (setting.py, makale değil):** LR 0,001, batch 1, 200 epoch, girdi 56x448x448, tohum 1, model_depth 50, pretrain_path pretrain/resnet_50.pth, yeni katman conv_seg.
- **Donanım/süre (makale):** verilmemiş. Depo: Tesla P40 (README).

## 8. Sonuçlar
| Görev | Metrik | Değer | Test seti | Kaynak |
|---|---|---|---|---|
| Ön eğitim alan sayısı, 1/2/4/8 alan, Brain | Dice | 54,67 / 54,81 / 54,83 / 55,41 % | 3DSeg-8 %10 test | Tablo 2 |
| Aynı, Hippo | Dice | 89,41 / 89,45 / 89,76 / 90,86 % | aynı | Tablo 2 |
| Aynı, Prostate | Dice | 72,58 / 72,94 / 73,29 / 75,07 % | aynı | Tablo 2 |
| Aynı, Liver | Dice | 88,12 / 88,75 / 90,01 / 90,11 % | aynı | Tablo 2 |
| Aynı, Heart | Dice | 86,73 / 88,16 / 89,74 / 91,05 % | aynı | Tablo 2 |
| Aynı, Pancreas | Dice | 72,66 / 73,81 / 74,08 / 74,33 % | aynı | Tablo 2 |
| Aynı, Vessel | Dice | 53,98 / 54,12 / 54,49 / 54,51 % | aynı | Tablo 2 |
| Aynı, Spleen | Dice | 91,33 / 92,08 / 92,67 / 93,80 % | aynı | Tablo 2 |
| Akciğer seg., ResNet-10 | Dice | TFS 71,30; Med3D 87,16 % | 8 hacim | Tablo 3 |
| Akciğer seg., ResNet-18 | Dice | TFS 75,22; Kin 83,21; Med3D 87,26 % | 8 hacim | Tablo 3 |
| Akciğer seg., ResNet-34 | Dice | TFS 76,82; Kin 85,82; Med3D 89,31 % | 8 hacim | Tablo 3 |
| Akciğer seg., ResNet-50 | Dice | TFS 71,75; Kin 87,11; Med3D 93,31 % | 8 hacim | Tablo 3 |
| Akciğer seg., ResNet-101 | Dice | TFS 72,10; Kin 88,32; Med3D 92,79 % | 8 hacim | Tablo 3 |
| Akciğer seg., ResNet-152 | Dice | TFS 73,29; Kin 88,61; Med3D 92,33 % | 8 hacim | Tablo 3 |
| Akciğer seg., ResNet-200 / PreResNet-200 | Dice | Med3D 92,06 / 93,82 (TFS 71,29 / 70,66) % | 8 hacim | Tablo 3 |
| Nodül sınıf., ResNet-10 | Doğruluk | TFS 79,80; Med3D 86,87 % | 99 nodül | Tablo 3 |
| Nodül sınıf., ResNet-18 | Doğruluk | TFS 80,80; Kin 82,83; Med3D 88,89 % | 99 nodül | Tablo 3 |
| Nodül sınıf., ResNet-34 | Doğruluk | TFS 83,84; Kin 83,84; Med3D 89,90 % | 99 nodül | Tablo 3 |
| Nodül sınıf., ResNet-50 | Doğruluk | TFS 84,85; Kin 74,75; Med3D 89,90 % | 99 nodül | Tablo 3 |
| Nodül sınıf., ResNet-101 / 152 / 200 / PreRes-200 | Doğruluk | Med3D 90,91 / 90,91 / 90,91 / 91,92 % | 99 nodül | Tablo 3 |
| LiTS karaciğer | Dice / ASSD | Med3D 94,6 % / 1,9; Kin 89,6 / 5,0; TFS 66,0 / 30,4 | LiTS 70 gizli test | Tablo 4 |
| LiTS en iyi (TencentX / mastermind) | Dice / ASSD | 96,6 % / 1,0 | LiTS | Tablo 4 |

Not: AUC, duyarlılık, özgüllük, F1 raporlanmamış; varyans/güven aralığı yok. TFS ResNet-18/34/50 Med3D'ye göre geride: sınıflamada +8,1 / +6,1 / +5,0 puan (Tablo 3'ten hesaplandı).

## 9. Açıklanabilirlik / ek analiz
Makalede Grad-CAM, dikkat haritası veya başka bir açıklanabilirlik analizi yok (doğrulanan metinde yer almıyor). Yalnız Şekil 5-6 yakınsama eğrileri ve Şekil 4 veri miktarı eğrisi var. Bizim projede açıklanabilirlik için MONAI GradCAM/occlusion kullanılması ayrı bir iş olarak planlanmalı.

## 10. Kod ve tekrarlanabilirlik
> **DÜZELTME (Opus §13.2):** MONAI resnet18/34 için MedicalNet ağırlığı `shortcut_type='A'`, `bias_downsample=True`, `feed_forward=False`, `spatial_dims=3`, `n_input_channels=1`, `pretrained=True` ister (10/50/101/152/200 için 'B' ve False); `pretrained=True` HF Hub'dan önce `resnet_18_23dataset.pth`, yoksa `resnet_18.pth` indirir. MONAI ResNet'te dilation yoktur (MedicalNet layer3/4 dilation 2/4) → 128³'te son harita 4³ (MedicalNet'te 16³). Uygulama `uygulama/baran_P02_medicalnet/model.py` bu düzeltmeye göre yazıldı.

- **Depo:** https://github.com/Tencent/MedicalNet, lisans MIT (LICENSE: THL A29 Limited, Tencent, 2019; ayrıca Kensho Hara'nın 3D-ResNets-PyTorch bileşeni MIT, 2017). Kopyalanabilir.
- **Çerçeve:** PyTorch; README gereksinimleri Python 3.7.0, PyTorch 0.4.1, CUDA 9.0, cuDNN 7.0.5 (çok eski; yeni PyTorch ile doğrudan çalışması doğrulanamadı).
- **Dosyalar:** train.py, test.py, model.py, setting.py, models/resnet.py, datasets/brains18.py (MRBrainS18 ön işleme), utils/logger.py, test_ci.py, toy_data/.
- **Ağırlıklar:** Evet. MedicalNet_pytorch_files.zip (Google Drive / Tencent Weiyun bağlantıları). resnet_N.pth: N=10,18,34,50,101,152,200; ek olarak 2019/07/30'da eklenen resnet_N_23dataset.pth: N=10,18,34,50 (23 veri kümesi, makaledeki 8 kümeli sürümden farklı; hangisinin makale sonuçlarıyla eşleştiği doğrulanamadı). Dosya boyutları listelenmemiş.
- **Veri:** Depoda yok; yalnız toy_data ve MRBrainS18 için dizin düzeni (images/, labels/, train.txt, val.txt).
- **Eksikler:** Ön eğitim betiği ve 3DSeg-8 verisi yok (yalnız aktarım/ince ayar demosu); sınıflandırma başı yok (yalnız conv_seg); yeni PyTorch uyumu belirsiz.
- **MONAI (benim ek bilgim, bu oturumda doğrulanmadı):** MONAI `monai.networks.nets.resnet` MedicalNet ağırlıklarını yüklemeyi (pretrained=True, ResNet-10/18/34/50) destekler; resnet18 için shortcut_type='A', bias_downsample=False ve n_input_channels=1, num_classes ayarı gerekir. Kullanmadan önce MONAI belgesinden doğrulanmalı.

## 11. Güçlü ve zayıf yönler
**Güçlü:**
- Açık lisans (MIT), hazır 3B ön eğitimli ağırlıklar, 1 kanallı tıbbi hacimlere uygun.
- Kinetics ve TFS'ye karşı tutarlı kazanç (Tablo 3, ResNet-18'de sınıflamada +8,1 puan TFS'ye göre).
- Çok alanlı ön eğitimin alan sayısıyla iyileştiği gösterilmiş (Tablo 2).
**Zayıf:**
- Hiçbir deney beyin sMRI sınıflandırması veya Alzheimer içermiyor; ön eğitimin çoğu segmentasyon, BT ağırlıklı.
- Sınıflandırma kanıtı yalnız LIDC nodülleri ve 99 örneklik testle; varyans, CV, AUC, güven aralığı yok.
- Eğitim ayrıntıları eksik (batch, epoch, girdi boyutu, donanım); §4.1 SGD ve §4.2 Adam çelişkisi.
- 2x/10x hızlanma gövde metinde ölçülmemiş.
- Makale ile depo arasında mimari farklar (dilation: makale r=2, kod layer4 dilation 4) ve çoklu ağırlık seti (8 küme vs 23 veri kümesi) karışıklığı.
- Depo bağımlılıkları eski (PyTorch 0.4.1).

## 12. Bizim projeye uyarlama
Kurulumumuz: ADNI1 1.5T başlangıç T1, NC/MCI/AD, HD-BET → N4 → z-score → MNI152 afin → 128³, RID düzeyinde 5-kat CV × 3 tohum, birincil görev AD-NC, ikincil 3-sınıf.

### 12.1 Okuyucunun uyarlama notu
**Aynen alınan:** MedicalNet ResNet-18 ağırlığı (MIT), tek kanallı girdi, 3B ResNet-18 omurgası (MONAI resnet18 spatial_dims=3, n_input_channels=1), kodlayıcıyı ağırlıkla başlatma.
**Değiştirilen:** (1) Segmentasyon başı yerine global ortalama havuz + FC (2 sınıf AD vs NC, ikincil 3 sınıf). (2) Girdi 128³; ön eğitim girdisi farklı alan (BT ve çeşitli MR, ortanca aralığa yeniden örnekleme), bizde MNI 128³ z-score; yoğunluk dağılımı farklı olduğu için ilk epoch'larda BN istatistik sapması beklenir. (3) Ön eğitim 3. ve 4. blokta dilation kullandı, MONAI standart stride kullanır; ağırlık şekilleri uyumlu ama davranış kayması olabilir (doğrulanamadı). (4) Optimizer: Adam/AdamW LR 1e-4 ile 1e-3 aralığı (makale Adam 0,001 kullanmış; biz katman bazlı LR ve kademeli çözme önerilir), ağırlık azalması, kosinüs çizelgesi, erken durdurma doğrulama AUC'ye göre (makalede yok). (5) Kayıp: sınıf ağırlıklı çapraz entropi (NC/MCI/AD ≈229/382/187). (6) RID düzeyi 5-kat CV x 3 tohum; makale tek bölme. (7) Artırma: hafif afin, yoğunluk kayması; makalenin dönme/ölçek aralığı küçük tutulmalı.
**Protokole uymayan noktalar:** Makale CV/çok tohum/AUC/dengeli doğruluk/F1/duyarlılık/özgüllük raporlamıyor; bunları kendimiz hesaplayıp raporlarız. Ön eğitim BT ağırlıklı, beyin sMRI ile alan uyuşmazlığı var; bu yüzden sıfırdan eğitim temel çizgisi (TFS) ve gerekirse ağırlıksız MONAI resnet18 kıyası zorunlu, aksi halde transfer kazancı gösterilemez. Hangi ağırlık dosyası kullanılacağı kayda geçmeli (resnet_18.pth mi resnet_18_23dataset.pth mi).
**Zorluk:** 2/5 (ağırlık yükleme ve baş değişimi kolay; anahtar adı eşlemesi ve shortcut tipi dikkat ister).
**VRAM/süre tahmini (tahmin, ölçülmedi):** ResNet-18 3B, 128³, karma duyarlık (AMP) ile batch 8 yaklaşık 8-12 GB, T4 16 GB'a sığar; batch 16 için gradyan birikimi gerekebilir. Yaklaşık 800 denek x %80 eğitim ≈ 640 görüntü/epoch; T4'te epoch başına yaklaşık 30-60 sn tahmini; 50 epoch x 5 kat x 3 tohum ≈ 15 koşu, yaklaşık 10-20 saat toplam (Kaggle/Colab oturum sınırına bölünmeli). Önbelleğe alınmış 128³ tensörlerle veri yükleme darboğazı azaltılır.
**Bizim hedef (AD vs NC ≥%85):** Makale bu hedefe doğrudan kanıt sunmuyor; yalnız başlatma stratejisi olarak değerli.

### 12.2 Hakemin kurulum farkı analizi
1) Görev: makalede ön eğitim 8 kümeli 3B segmentasyon. Aktarım akciğer segmentasyonu, LIDC nodül iyi/kötü sınıflaması (99 test nodülü) ve LiTS. Bizde tüm-beyin T1 ile denek düzeyinde AD/NC (ve 3 sınıf) sınıflaması var. Lezyon yerine yaygın atrofi sinyali aranıyor, yani hedef ön eğitimin öğrendiği yerel organ ve sınır özelliklerinden farklı. Beklenen etki: Tablo 3'teki +8 puanlık kazancın bize taşınacağı varsayılamaz; kazanç çoğunlukla daha hızlı ve kararlı yakınsama biçiminde görülebilir.
2) Veri ve alan: ön eğitim karışık BT ve MR (BraTS tümör, Hippo). Bizde 1.5T T1 ADNI1 kullanılıyor, yaklaşık 800 denek (AD/NC görevi için 416). Kinetics'in derin ağlarda TFS'nin altına düşmesi (Tablo 3), uyumsuz ön eğitimin zarar verebileceğini gösterir. Bu yüzden TFS temel çizgisi şart.
3) Ön işleme: makalede alan başına ortanca voksel aralığına yeniden örnekleme, hedef kutuya göre kırpma, 0,5-99,5 yüzdelik kırpma ve hacim z-score var. Bizde HD-BET, N4, maske içi z-score ve MNI afin ile 128³ var. Arka plan sıfır olduğu için yoğunluk dağılımı farklı. BN istatistikleri kayar; BN'yi yeniden ısıtmak (ilk epoch'larda BN'yi eğitilebilir bırakmak) gerekir. Maske içi z-score'a 0,5-99,5 kırpma eklemek ön eğitime yaklaşır.
4) Mimari: MedicalNet layer3/4'te stride 1 + dilation 2/4 kullanır (çıktı girdi/8). MONAI resnet18 stride 2 kullanır (çıktı girdi/32, 128³ için 4³). Ağırlıklar aynı şekilde yüklenir ama öznitelikler ön eğitimdeki ölçekte çalışmaz; kazanç azalabilir. Alternatif olarak MedicalNet resnet.py (MIT) kopyalanıp conv_seg yerine GAP+FC takılabilir.
5) Baş: makalede sınıflama için GAP + FC. Bizde de GAP + Dropout + Linear(512→2/3); MONAI feed_forward=False ile baş kendimiz eklenir.
6) Bölme ve değerlendirme: makalede tek rastgele bölme, doğrulama kümesi yok, yalnız doğruluk raporlanıyor. Bizde RID düzeyinde 5-kat CV × 3 tohum, iç doğrulama ile erken durdurma; dengeli doğruluk, AUC, F1, duyarlılık, özgüllük. Makale sayılarıyla doğrudan kıyas anlamlı değil.
7) Ağırlık sürümü: MONAI pretrained=True, 23 veri kümeli ağırlığı indirir; makale 8 kümelidir. İçeriği bilinmediği için ADNI örtüşmesi dışlanamaz. Raporda dosya adı ve SHA256 kaydedilmeli; mümkünse resnet_18.pth ile de koşulmalı.
8) Sızıntı değerlendirmesi: makale için 'orta' değerlendirmesine katılıyorum. Doğrulama kümesi yok, 99 örneklik test var, LIDC'de hasta düzeyinde bölme belirsiz. Bizim için ince ayarda RID düzeyinde bölme yeterli; ön eğitim kaynaklı denek örtüşmesi 8 kümeli sürümde düşük, 23 kümeli sürümde bilinmiyor.

### 12.3 İmplementasyon yapılacaklar (hakem)
1) Ağırlık: MONAI `monai.networks.nets.resnet18(spatial_dims=3, n_input_channels=1, feed_forward=False, shortcut_type='A', bias_downsample=True, pretrained=True)`. Bu çağrı HF Hub'dan resnet_18_23dataset.pth indirir. Makaledeki 8 kümeli sürüm için MedicalNet zip'inden resnet_18.pth alın, `torch.load` ile açın, 'module.' önekini ayıklayın, `load_state_dict(strict=False)` ile yükleyin ve missing/unexpected anahtarları loglayın (yalnız fc beklenmeli). Not: bias_downsample=False verirseniz MONAI hata fırlatır.
2) Baş: `nn.Sequential(nn.AdaptiveAvgPool3d(1), nn.Flatten(), nn.Dropout(0.3), nn.Linear(512, C))`, C=2 (AD/NC) veya 3. Makalede de sınıflama başı GAP + FC (§3.3).
3) conv1 ayarı: MedicalNet conv1 7x7x7, stride 2, pad 3, bias yok. MONAI'de `conv1_t_size=7, conv1_t_stride=2` açıkça verin ve yüklenen ağırlıkla şeklin eşleştiğini doğrulayın.
4) Dilation kararı: MONAI stride kullanır, MedicalNet ise layer3/4'te dilation 2/4. Bir ablation yapın: (a) MONAI resnet18; (b) MedicalNet models/resnet.py (MIT, kopyalanabilir) conv_seg çıkarılıp GAP+FC eklenmiş hali. 128³'te (b) için VRAM'i ölçün (öznitelik haritası 16³, daha ağır).
5) Ön işleme uyumu: maske içi z-score'dan sonra 0,5-99,5 yüzdelik kırpma ekleyin (§3.1). Tek kanal, float32, (B,1,128,128,128).
6) Optimizasyon: AdamW. Omurgada LR 1e-4, başta 1e-3 (makalede ince ayar Adam 1e-3, TFS 1e-2). wd 1e-4 ile 1e-2 arası, kosinüs çizelgesi, AMP. İlk 3-5 epoch omurga dondurulup yalnız baş ve BN eğitilir, sonra tamamı çözülür. Batch 4-8 (T4 16 GB, AMP); VRAM ilk koşuda ölçülmeli.
7) Kayıp: sınıf ağırlıklı CrossEntropy (AD/NC'de 187/229 dengesizliği hafif). Erken durdurma yalnız iç doğrulama katmanında, dengeli doğruluk veya AUC'ye göre; test katında asla.
8) Artırma: makaledeki küçük aralıklar (dönme ±5°, ölçek 0,8-1,2, küçük öteleme) MONAI RandAffined ile. Ek olarak RandFlip (sol-sağ) ve hafif RandScaleIntensity/RandShiftIntensity. MNI'ye kayıtlı veride büyük afin kullanmayın.
9) Deney matrisi: (i) TFS (pretrained=False, aynı mimari, LR 1e-3); (ii) MedicalNet 8 küme; (iii) MedicalNet 23 küme. Hepsi RID düzeyinde 5-kat × 3 tohum. Kazancı eşleştirilmiş testle raporlayın (kat × tohum başına fark, ortalama ± SD). Ağırlık dosyası adı ve SHA256 kayda geçsin.
10) Dikkat: depo PyTorch 0.4.1 içindir. train.py/setting.py doğrudan kullanılmamalı; yalnız models/resnet.py ve ağırlıklar alınır. MIT lisans metni ve atıf (Tencent + Kensho Hara 3D-ResNets) kopyalanan dosyanın başına eklenir.

## 13. Opus doğrulama
- **Sonuç:** **ÇELİŞKİ VAR** · **Güven:** yüksek
- **Hakemin okuduğu kaynak:** Tam metin okundu: https://arxiv.org/html/1904.00625v4 (v4 HTML; Özet, §1, §3.1, §3.3, §4.1-4.3, Tablo 1-4, Şekil 3-6 alt yazıları; iki ayrı geçişte sorgulandı). Kod: https://github.com/Tencent/MedicalNet README (parametre tablosu, kısayol tipleri, gereksinimler, ağırlık listesi, lisans) ve https://raw.githubusercontent.com/Tencent/MedicalNet/master/models/resnet.py okundu. MONAI uyumu için https://raw.githubusercontent.com/Project-MONAI/MONAI/dev/monai/networks/nets/resnet.py okundu (docs.monai.io sertifika hatası nedeniyle açılamadı). PDF ve ar5iv ayrıca açılmadı; şekiller görsel olarak görülmedi.

### 13.1 Kontrol edilen sayılar
| İddia | Özetteki değer | Makaledeki değer | Durum | Yer |
|---|---|---|---|---|
| 3DSeg-8 toplam vaka | 1.638 (485+261+33+131+100+282+304+42) | Tablo 1: 485, 261, 33, 131, 100, 282, 304, 42 (toplam yazılmıyor; toplamı 1.638) | **doğru** | Tablo 1 |
| 3DSeg-8 küme sayısı ve bölme | 8 küme; %90 eğitim / %10 test | 8 küme, her biri rastgele %90/%10 | **doğru** | §4.1 |
| Ön eğitim optimizer | SGD, LR 0,1, momentum 0,9, wd 0,001, çapraz entropi | SGD, 0.1, 0.9, 0.001, cross-entropy | **doğru** | §4.1 |
| Aktarım optimizer ve LR | Adam 0,001 (Med3D, Kin); TFS 0,01; '§4.1 ile çelişki' | Adam, önceden eğitilmiş modeller 0.001, sıfırdan 0.01. Sayılar doğru; ancak §4.1 ön eğitim, §4.2 ince ayar ayarıdır, çelişki değil | **doğru** | §4.2 |
| ResNet-18 akciğer Dice | Med3D %87,26; TFS %75,22; Kin %83,21 | 87.26 / 75.22 / 83.21 | **doğru** | Tablo 3 |
| ResNet-18 nodül doğruluğu | Med3D %88,89; TFS %80,80; Kin %82,83 | 88.89 / 80.80 / 82.83 | **doğru** | Tablo 3 |
| En iyi nodül doğruluğu | %91,92 PreResNet-200; ResNet-101/152/200 %90,91 | 91.92; 90.91 / 90.91 / 90.91 | **doğru** | Tablo 3 |
| En iyi akciğer Dice | %93,82 PreResNet-200; ResNet-50 %93,31 | 93.82; 93.31 | **doğru** | Tablo 3 |
| LIDC bölmesi | 1.010 hasta; 1.050 nodül eğitim / 99 test | 1.010 hasta; 1.050 / 99 nodül; 1-3 iyi, 4-5 kötü huylu | **doğru** | §4.2 |
| Visceral bölmesi | 80 hacim; 72/8; 4 modalite | 80 hacim, 72 eğitim / 8 test, 4 modalite | **doğru** | §4.2 |
| LiTS Med3D Dice/ASSD | %94,6/1,9 (Kin 89,6/5,0; TFS 66,0/30,4) | 94.6/1.9; 89.6/5.0; 66.0/30.4 | **doğru** | Tablo 4 |
| LiTS bölmesi | 201 BT; 131/70 | 201 BT, 131 eğitim / 70 test (test etiketi gizli) | **doğru** | §4.3 |
| Hızlanma ve kazanç | 2x Kinetics, 10x sıfırdan; %3-%20 | Özette 2x, 10x, %3-%20; gövdede sayısal değil | **doğru** | Özet |
| ResNet-18 parametre sayısı (depo) | 32,99 M | README: 32.99 M (Tesla P40, 0.19 s) | **doğru** | GitHub README |
| Depo lisansı | MIT, Tencent 2019 | README: MIT License (LICENSE metni bu oturumda ayrıca açılmadı) | **doğru** | GitHub README |
| Heart Dice 1→8 alan | %86,73 → %91,05 | 86.73 → 91.05 | **doğru** | Tablo 2 |
| Nodül sınıflayıcı başı | Sınıflayıcı başı ayrıntısı verilmemiş | §3.3: Med3D kodlayıcısına ortalama havuzlama + tam bağlantılı katman eklenir; §4.2: kodlayıcıya FC katmanları bağlanır | **yanlış** | §3.3, §4.2 |
| MONAI resnet18 MedicalNet yükleme ayarı | shortcut_type='A', bias_downsample=False, n_input_channels=1 | MONAI kodu: resnet18 için shortcut_type='A' ve bias_downsample=True gerekir; ayrıca feed_forward=False zorunlu, spatial_dims=3; pretrained=True önce resnet_18_23dataset.pth indirir | **yanlış** | MONAI monai/networks/nets/resnet.py (get_medicalnet_pretrained_resnet_args, _resnet) |
| LiTS omurgası | Belirtilmemiş (yalnız DenseASPP-3D) | DenseASPP, Med3D ile başlatılmış ResNet-152 omurgası | **doğru** | §4.3 (özet eksik bırakmış, çelişki değil) |
| Depo resnet.py dilation | layer3 dilation 2, layer4 dilation 4; conv1 7x7x7 s2 | layer3 stride1 dil2, layer4 stride1 dil4; conv1 1→64, k7, s2, p3, bias yok | **doğru** | models/resnet.py |

### 13.2 Düzeltmeler (özette yanlış/eksik → doğrusu)
- egitim/nodül sınıflama: 'Sınıflayıcı başı ayrıntısı verilmemiş' YANLIŞ. Doğrusu: §3.3'e göre sınıflamada Med3D kodlayıcısının üstüne ortalama havuzlama + tam bağlantılı (FC) katman eklenir; §4.2 de kodlayıcıya FC katmanları bağlandığını söyler. Nodül kırpma boyutu verilmiyor.
- egitim/guclu_zayif: '§4.1 SGD ve §4.2 Adam çelişkisi' yanlış yorum. §4.1'deki SGD (LR 0,1) ön eğitimin ayarı, §4.2'deki Adam (0,001 / TFS 0,01) aktarımdaki ince ayarın ayarı. İki farklı aşama oldukları için çelişki yok.
- kod_tekrar/MONAI: 'resnet18 için shortcut_type=A, bias_downsample=False' YANLIŞ. MONAI get_medicalnet_pretrained_resnet_args değerleri: 18 ve 34 için shortcut_type='A' ve bias_downsample=True; 10/50/101/152/200 için 'B' ve False. pretrained=True ayrıca spatial_dims=3, n_input_channels=1 ve feed_forward=False ister (FC olmadan gelir, başı biz ekleriz). num_classes yüklemede kontrol edilmez.
- kod_tekrar/uyarlama: MONAI pretrained=True, HF Hub'dan (TencentMedicalNet/MedicalNet-Resnet18) ÖNCE resnet_18_23dataset.pth dosyasını indirir, olmazsa resnet_18.pth'e düşer. Yani 'hangi ağırlık' sorusu MONAI ile kendiliğinden 23 veri kümeli sürüme çözülür. Makaledeki 8 kümeli sürüm isteniyorsa pretrained='yol/resnet_18.pth' olarak yerel dosya verilmeli. Bu yolda MONAI uyumluluk kontrolü çalıştırmaz.
- mimari/uyarlama: MONAI ResNet'te dilation hiç yok; layer2-4 stride=2. 128³ girdide son öznitelik haritası yaklaşık 4³ olur (MedicalNet dilation ile girdi/8 ≈ 16³ üretir). Ağırlık şekilleri aynı, ama alıcı alan ve ölçek davranışı farklıdır.
- on_isleme/LiTS: 'ince DenseASPP-3D segmentasyon' ifadesine omurga eklenmeli: DenseASPP, ResNet-152 Med3D ağırlıklarıyla başlatılıyor (§4.3). Tablo 4'teki Med3D satırı bu modeldir, ResNet-18 değil.
- sonuclar: Nodül satırında ResNet-101/152/200/PreRes-200 için TFS ve Kin değerleri atlanmış. Tablo 3: TFS 81,82 / 73,74 / 76,77 / 74,75; Kin (yalnız 101/152) 74,75 / 75,76. Kinetics derin ağlarda sınıflamada TFS'nin bile altında kalıyor (ResNet-50/101/152). Bu, 'Kin her zaman TFS'den iyi' algısını düzeltir.

### 13.3 Özetin atladığı önemli noktalar
- Doğrulama kümesi hiç anılmıyor. Yalnız eğitim/test bölmeleri var (90/10, 72/8, 1.050/99). Model ve kontrol noktası seçiminin test üzerinde yapıldığı izlenimi güçlü. Özet bunu 'doğrulanamadı' diye yumuşatmış, oysa makalede doğrulama kümesi tanımı yok.
- Tablo 3'te ResNet-10 ve ResNet-200/PreResNet-200 için Kinetics satırı yok. Kin karşılaştırması yalnız 18-152 arasında yapılabilir.
- Derin ağlarda Kinetics ön eğitimi nodül sınıflamada TFS'nin altında (ResNet-50: Kin 74,75 / TFS 84,85). Uyumsuz alandan transferin zarar verebileceğine somut kanıt. Bizim beyin sMRI senaryosunda TFS kıyasının neden zorunlu olduğunu destekler.
- Şekil 4 deneyi (ResNet-152 Med3D, eğitim verisinin %10/20/40/80/100'ü) gövdede yanlışlıkla 'Fig. 3' (karaciğer çerçevesi) olarak anılıyor. Özet bunu doğru not etmiş, ancak deneyin hangi görevde yapıldığı (3DSeg-8) ve sayısal değerleri metinden çıkarılamıyor.
- Alan dengeleme: en büyük kümenin tüm verisi alınıp diğerleri rastgele artırmayla dengeleniyor (§4.1). Batch'lerin alanlar arasında nasıl kurulduğu yazmıyor.
- Açık bir sınırlılıklar bölümü yok. Belirsizlik ölçüsü yok (CV, tohum tekrarı, güven aralığı, istatistiksel test). Dış test yok; LiTS gizli testi sunucuyla yapılıyor.
- 3DSeg-8'deki tek beyin kümeleri BraTS tümör MR'ı ve Hippo. Ön eğitim verisinde dejeneratif hastalık ya da tüm-beyin T1 sınıflaması yok.
- Depo: MedicalNet 23 veri kümeli ağırlıkların hangi kümeleri içerdiği README'de listelenmiyor. ADNI türevi veri içerip içermediği bilinmiyor; sızıntı değerlendirmesi açısından önemli.

### 13.4 Doğrulanamayanlar
- Hippo (MSD Hippocampus) kümesinin kaynağının ADNI olmadığı (Vanderbilt) iddiası makalede yok; bu oturumda doğrulanmadı.
- MedicalNet resnet_N_23dataset.pth içeriği (hangi 23 küme, ADNI var mı) doğrulanamadı.
- Makale sonuçlarının hangi ağırlık dosyasıyla (8 kümeli resnet_18.pth) üretildiği; büyük olasılıkla 8 kümeli sürüm, ancak açıkça belirtilmiyor.
- Ön eğitimde batch boyutu, epoch, girdi yaması, donanım ve süre makalede yok.
- LIDC bölmesinin hasta düzeyinde yapılıp yapılmadığı belirtilmiyor.
- Dönme aralığı [-5,5] birimi (derece olması muhtemel) belirtilmiyor.
- LiTS için 'önceki segmentasyon deneyleriyle aynı hiperparametreler' ifadesi bu oturumda ayrıca teyit edilmedi.
- MONAI pretrained='yol' (yerel dosya) kullanımında 'module.' önekinin otomatik ayıklanıp ayıklanmadığı net değil; elle ayıklanmalı.
- MONAI ResNet conv1_t_stride varsayılanının MedicalNet (stride 2) ile aynı olup olmadığı bu oturumda doğrulanmadı.
- README'deki ResNet-34 (63,31 M) > ResNet-50 (46,21 M) parametre sıralaması yazım hatası mı, doğrulanamadı.

### 13.5 Okuyucunun işaretlediği anahtar sayılar (ham)
| İddia | Değer | Yer |
|---|---|---|
| 3DSeg-8 toplam vaka (satır toplamı) | 1.638 (485+261+33+131+100+282+304+42) | Tablo 1, §4.1 (toplam makalede yazmıyor) |
| 3DSeg-8 küme sayısı ve bölme | 8 küme; her birinde %90 eğitim / %10 test | §4.1, Tablo 1 |
| Ön eğitim LR / momentum / weight decay / optimizer | SGD, 0,1 / 0,9 / 0,001, çapraz entropi | §4.1 Training |
| Aktarım optimizer ve LR | Adam 0,001 (Med3D, Kin); TFS için 0,01 | §4.2 (§4.1 ile çelişki) |
| ResNet-18 Med3D akciğer segmentasyonu Dice | %87,26 (TFS %75,22, Kin %83,21) | Tablo 3 |
| ResNet-18 Med3D nodül sınıflama doğruluğu | %88,89 (TFS %80,80, Kin %82,83) | Tablo 3 |
| En iyi nodül doğruluğu | %91,92 (PreResNet-200 Med3D); ResNet-101/152/200 %90,91 | Tablo 3 |
| En iyi akciğer Dice | %93,82 (PreResNet-200), ResNet-50 %93,31 | Tablo 3 |
| LIDC bölmesi | 1.010 hasta; 1.050 nodül eğitim / 99 nodül test | §4.2 |
| Visceral akciğer bölmesi | 80 hacim; 72 eğitim / 8 test; 4 modalite | §4.2 |
| LiTS Med3D Dice / ASSD | %94,6 / 1,9 (Kin %89,6 / 5,0; TFS %66,0 / 30,4) | Tablo 4, §4.3 |
| LiTS bölmesi | 201 BT; 131 eğitim / 70 test | §4.3 |
| Hızlanma iddiası ve kazanç aralığı | 2x (Kinetics), 10x (sıfırdan); doğrulukta %3-%20 | Özet (gövdede sayısal değil) |
| MedicalNet ResNet-18 parametre sayısı (depo) | 32,99 M | GitHub README Experiments tablosu (makalede yok) |
| Depo lisansı | MIT, THL A29 Limited (Tencent), 2019 | GitHub LICENSE |
| Ön eğitimde alan sayısı etkisi, Heart Dice 1 alan → 8 alan | %86,73 → %91,05 | Tablo 2 |

## 14. Kaynaklar
- https://arxiv.org/abs/1904.00625
- https://arxiv.org/pdf/1904.00625 (metin okunamadı)
- https://ar5iv.labs.arxiv.org/html/1904.00625
- https://arxiv.org/html/1904.00625v4
- https://github.com/Tencent/MedicalNet
- https://raw.githubusercontent.com/Tencent/MedicalNet/master/models/resnet.py
- https://raw.githubusercontent.com/Tencent/MedicalNet/master/setting.py
- https://raw.githubusercontent.com/Tencent/MedicalNet/master/LICENSE
