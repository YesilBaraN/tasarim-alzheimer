# P03 — Wen 2020 — CNN ile AD sınıflandırma: derleme ve tekrarlanabilir değerlendirme

> **Durum:** ☐ okunmadı · ☑ AI özeti hazır · ☑ Opus doğrulandı (**ÇELİŞKİ VAR**, güven: yüksek) · ☐ insan okudu · ☐ implemente edildi
> **Sorumlu:** Baran Yeşilyurt · **Grup:** A · **Tam metin (ücretsiz):** https://arxiv.org/abs/1904.07773 · **Kod:** https://github.com/aramis-lab/clinicadl (MIT)
> **AI okuma kaynağı:** Yayıncı sürümü wen2020_yayinci.txt (tamamı, s.1-19; s.1-16 ana metin, s.17-19 kaynakça) + arXiv v3 wen2020_arxiv_v3.txt'in YALNIZCA ek materyal bölümü (eTable 1-5, arXiv-PDF sayfa 55-60). Yayıncı metninde ek tablolar yok; mimari ayrıntıları ve hiperparametreler eTable'lardan geliyor, bunların yeri 'arXiv v3 eTable' diye işaretlendi. Kod deposuna gidilmedi; kod_tekrar bölümündeki depo durumu makale dışı bilgidir (doğrulanamadı).

> ⚠ **Nasıl okunmalı:** §2–§12 Sonnet okuyucunun özetidir; §13 Opus hakeminin makaleye karşı denetimidir. §13'te "yanlış" işaretli her sayı için **makaledeki değer** geçerlidir; §13'teki düzeltmeler §4–§8'in üstünde okunur. Hiçbir ajan makalenin yerine geçmez: implementasyondan önce ilgili bölümü (§6, §7) makaleden bir kez daha kendin oku.

## 1. Künye
Wen J., Thibeau-Sutre E., Diaz-Melo M., Samper-González J., Routier A., Bottani S., Dormont D., Durrleman S., Burgos N., Colliot O. (2020). Convolutional neural networks for classification of Alzheimer's disease: Overview and reproducible evaluation. Medical Image Analysis 63:101694. DOI 10.1016/j.media.2020.101694; arXiv:1904.07773. Eğitilmiş modeller Zenodo 10.5281/zenodo.3491003 (s.2).

## 2. Tek paragraf özet
Çalışma üç katkı sunuyor: (i) 32 uçtan uca CNN çalışmasının sistematik taraması ve veri sızıntısı etiketlemesi, (ii) ADNI/AIBL/OASIS'i BIDS'e çeviren, önişleme, mimari ve doğrulama modüllerini içeren açık kaynak çerçeve, (iii) dört yaklaşımın (3B denek-düzeyi, 3B ROI, 3B yama, 2B dilim) sıkı protokolle karşılaştırması. Taramada çalışmaların yaklaşık yarısında (10 'belirsiz' + 6 'açık' = 16/32) sızıntı olasılığı bulundu (Tablo 1, s.3; §2.3.5, s.6). Test kümeleri en başta ayrılıp hakem sürecinin sonuna kadar kilitli tutuldu (§4.6.1, s.10). ADNI bağımsız testinde AD-CN BAcc 0.76-0.89, sMCI-pMCI 0.69-0.74 aralığında kaldı; üç 3B yaklaşım benzer, 2B dilim daha düşük çıktı (§6, s.14-15). Doğrusal SVM (DARTEL GM) AD-CN'de en iyi CNN ile aynı düzeyde (0.88), sMCI-pMCI'da ADNI testinde CNN'lerden iyi (0.75-0.76) (Tablo 6, s.13). Modeller ADNI ve AIBL'e AD-CN'de iyi genelledi, OASIS'e (tanı ölçütü farklı) kötü, sMCI-pMCI'da AIBL'e çok kötü genelledi (§5.2, s.12-14).

## 3. Problem ve katkı
- Çalışmalar arası kıyas yok: katılımcı seçimi, önişleme, CV ve metrik farklı (§1, s.2).
- Yeniden üretilemezlik: kod ve ayrıntılar eksik; iki çalışma Hosseini-Asl kodunu yeniden koştuğunda 0.99 yerine 0.82 doğruluk buldu (§6, s.14).
- Veri sızıntısı taraması: 32 çalışmanın yarısında olası sızıntı; 4 tür tanımlandı (§2.2, s.4).
- Açık kaynak çerçeve: Clinica BIDS dönüştürücüleri, 'Minimal' ve 'Extensive' önişleme, 4 CNN yaklaşımı, kilitli test protokolü, sentetik 'ayrılamaz' (0.5) ve 'tam ayrılabilir' (1.00) sağlık testleri (§4.6.1, s.11; §5.1, s.11).
- Sızıntı simülasyonu: dilim düzeyinde bölme doğrulamada BAcc 1.00 verirken ADNI testte 0.75, AIBL testte 0.80 (§6, s.14).
- Kıyas: 4 yaklaşım ve SVM, üç ayrı test kümesi üzerinde.
- Bulgular: yoğunluk ölçekleme şart; AE ön eğitimi küçük fark; boylamsal veri küçük fark; doğrusal ve doğrusal olmayan kayıt eşdeğer (§5.1, §6).

## 4. Veri seti ve bölme
KATILIMCILAR. ADNI: 1455 katılımcı (T1w en az bir vizitte) (§3, s.6). Tablo 2 (s.7), denek/oturum: CN 330/1830, MCI 787/3458, sMCI 298/1046, pMCI 295/865, AD 336/1106. AIBL: 598 katılımcı (Tablo 3, s.7): CN 429, MCI 93 (sMCI 13, pMCI 20), AD 76. OASIS: 193 katılımcı, 62 yaş ve üstü (Tablo 4, s.7): CN 76, AD 78 (MCI'lar AD sayılıyor; önişleme sonrası 22 AD + 17 CN dışlandı, §3 s.7); OASIS tanısı yalnızca CDR'a dayanıyor. Etiketler: CN/AD için başlangıçta tanı almış ve takipte değişmeyenler; ≥2 etiket değişimi olan MCI dışlandı; sMCI/pMCI 36 ay ölçütüyle (§3, s.6). AIBL için 7, ADNI için 30 oturum QC'den, OASIS için 39 tarama kalite kontrolünden çıkarıldı (§4.2, s.8); 2 pMCI deneği tamamen çıkarıldı (§3, s.6).
TEST. ADNI testi: yaş ve cinsiyeti eşleştirilmiş, rastgele seçilmiş her sınıftan 100 denek (100 CN + 100 AD); geri kalan ADNI eğitim/doğrulama (§4.6.1, s.10). AIBL ve OASIS'in tamamı ayrı test kümesi (s.10). Eğitim/doğrulama ile test arasında yaş/cinsiyet farkı anlamlı değil kontrol edildi. ADNI eğitim/doğrulama AD-CN denek sayıları metinde verilmemiş; Tablo 2'den türetilirse CN 230, AD 236 olur (türetilmiş, doğrulanamadı).
CV. 5 katlı CV, bir kez, sabit tohum (random_state=2); her kat %20 doğrulama (§4.6.1, s.10). CV tekrar edilmedi, bu sınırlılık olarak belirtildi (§6, s.16). SVM'de C için iç içe 10 katlı CV (s.11).
KİLİTLEME. Test kümesi en başta üretilip gizlendi, hakem sürecinin sonuna kadar dokunulmadı; yalnızca her yaklaşımın CV ile seçilen en iyi modeli teste sokuldu (s.10, s.15). Mimari ve eğitim hiperparametreleri yalnızca eğitim/doğrulama ile seçildi. AE ön eğitimi ve sınıflandırma aynı bölmeyi kullandı; AE yalnızca eğitim kümesindeki tüm AD+MCI+CN ile eğitildi (§4.4.1, s.10). AD-CN kaynak görevinden sMCI-pMCI'ya transfer sızıntısız: AE'de kullanılan MCI'lar ile sMCI-pMCI test kümesi çakışmıyor (s.10-11). Otomatik sızıntı testleri kodda var (s.11).
4 SIZINTI TÜRÜ (§2.2, s.4): (a) yanlış veri bölme (denek düzeyinde değil; yama/dilim çıkarımında veya çok vizitli veride), (b) bağımsız test kümesi yokluğu (hiperparametre seçiminde test kullanımı), (c) geç bölme (artırma, öznitelik seçimi, AE ön eğitimi bölmeden önce), (d) yanlı transfer öğrenme (kaynak görev CN'leri hedef testte). Tablo 1'e göre (s.3): 17 satır sızıntı tablosunda; Bäckström kasıtlı olarak iki tabloda geçer. Çalışma sayısı (Tablo 1B'den sayım, sayımım): tür başına toplamı metin vermiyor (doğrulanamadı; satırlardan: a≈10, b≈10, c≈5, d=1). Kesin sayılar: toplam 32 çalışma, 10 belirsiz + 6 açık = 16 (~%50); Bäckström ayrı (s.6). Metin ek olarak, sızıntı olmayan çalışmaların çoğunda mimari seçiminin test üzerinde yapılıp yapılmadığının bilinemediğini belirtiyor (s.4).

**Sızıntı riski (AI):** düşük — Protokol en başta test ayırıyor, test kümesini hakem sürecine kadar kilitliyor, 5 katlı CV'yi tek seferlik sabit tohumla yapıyor, AE ön eğitimini yalnızca eğitim kümelerinde yapıyor, transfer öğrenmede kaynak/hedef örtüşmesini denetliyor ve kodda sızıntı testleri ile sentetik sağlık testleri bulunduruyor (s.10-11). Kalan zayıflıklar: (1) aynı bölme birden çok deneyin model seçiminde yeniden kullanıldı (5 kat tek seferlik, tekrar yok), (2) mimari arama stratejisi doğrulama BAcc'sine bakıyordu, test'e değil, (3) 'Minimal' ve 'Extensive' ile boylamsal/başlangıç kıyaslarında seçim doğrulama BAcc ile, yani aşırı uyum riski küçük ama var; (4) Tablo 6'daki ROI sMCI-pMCI doğrulama değeri '0.7 ± 0.05' basılmış, Tablo 5'te 0.77 (yazım hatası, s.12-13). Boylamsal eğitimde deneğe göre bölme zorunlu; makale denek düzeyinde böldüğünü belirtiyor (Tablo 5 'subject-level').

## 5. Ön işleme
t1-linear ('Minimal', §4.2, s.7): (1) N4ITK ile yanlılık alanı düzeltmesi (Tustison 2010); (2) ANTs (SyN algoritması) ile doğrusal/afin kayıt, ICBM 2009c nonlinear symmetric MNI şablonuna (Fonov 2011, 2009); (3) arka planı atan kırpma, son boyut 169×208×179, 1 mm³ izotropik; (4) isteğe bağlı MinMax yoğunluk ölçekleme [0,1] (CNN'lerde zorunlu bulundu: ölçeklemesiz BAcc 0.50, ölçeklemeli 0.80, Tablo 5 Exp 1-2, s.12). Kafatası ayıklama YOK. QC: Fonov et al. 2018 deep-QC (github vfonov/deep-qc); olasılık <0.5 dışlandı, <0.70 olanlar görsel kontrol (s.8).
t1-extensive (§4.2, s.7-8): SPM12 Unified Segmentation ile yanlılık düzeltme + doğrusal olmayan kayıt (yalnızca bias-düzeltilmiş doğrusal olmayan kayıtlı görüntü kullanılıyor, doku olasılık haritaları kullanılmıyor); ardından MNI uzayında çizilmiş beyin maskesiyle kafatası ayıklama (görüntü tabanlı yöntemler verilerinde dayanıklı çıkmadığı için maske tercih edildi); MinMax ölçekleme. Çıktı boyutu 121×145×121 (eTable 1, arXiv v3 s.55). Sonuç: Minimal 0.85 vs Extensive 0.86 (Exp 4-5, s.11-12) yani eşdeğer.
SVM girişi: DARTEL ile MNI'ya doğrusal olmayan kayıtlı, modüle gri madde yoğunluk haritaları (SPM tabanlı) (§4.3.5, s.9).
Yama ve ROI: 50×50×50 mm³ kayan pencere, örtüşmesiz, görüntü başına 36 yama; hipokampüs ROI'si MNI şablonunda elle merkezlenmiş 50³ mm küp, sol ve sağ ayrı (§4.3.2, s.8). 2B: sagittal dilimler, ilk ve son 20 dilim atılır, 129 dilim/denek, R=G=B kopyalanır (§4.3.3, s.8). Uygulama: Nipype (s.11).

## 6. Mimari
Kaynak: §4.3 (s.8-9), Şekil 1-3 (s.9-10), eTable 1-3 (arXiv v3 s.55-57). 'Conv5_FC3' adı bu makalede geçmiyor, bu ad ClinicaDL kod tabanındaki adlandırma olabilir (doğrulanamadı); makale '5 konvolüsyon bloğu + 3 FC' diyor.

| Yaklaşım | Katmanlar | Kanal / çekirdek / çıktı |
|---|---|---|
| 3B denek-düzeyi (Conv5_FC3; Minimal giriş 169×208×179) | 5 blok = Conv3³(pad 1, stride 1) + BN + ReLU + MaxPool 2³ (stride 2, adaptif pad) | Kanallar 8→16→32→64→128; çıktılar 8×85×104×90 → 16×43×52×45 → 32×22×26×23 → 64×11×13×12 → 128×6×7×6; Dropout 0.5; FC1 1300; FC2 50; FC3 2; Softmax (eTable 1) |
| Aynı, Extensive giriş 121×145×121 | Aynı | Son çıktı 128×4×5×4, FC aynı |
| 3B ROI (hipokampüs 50³) ve 3B yama (50³) | 4 blok = Conv3³(pad 0) + BN + ReLU + MaxPool 2³ | Kanallar 15→25→50→50; çıktılar 15×24³ → 25×11³ → 50×5³ → 50×2³; Dropout 0.5; FC1 50; Dropout 0.5; FC2 40; FC3 2; Softmax (eTable 2) |
| 2B dilim | ImageNet ön eğitimli ResNet-18, üstüne 1 ek FC (FC2); son 5 konv katmanı + son FC + eklenen FC ince ayarlı, diğerleri dondurulmuş | Dropout 0.8 (eTable 4); girişe 129 RGB dilim/denek (§4.3.3) |
| Otokodlayıcı ön eğitimi | Kodlayıcı = sınıflandırıcının konv blokları; kod çözücü ayna (konv ile ReLU sırası değişik); MSE kaybı; eğitim kümesindeki tüm AD+MCI+CN ile | 'adaptif' havuz dolgusu, konv dolgusu 1 (yeniden yapılandırma için) (§4.4.1, eTable 1) |
| Yama modları | single-CNN: 36 yama tek ağda; multi-CNN: yama başına 1 ağ (toplam 36), BAcc<0.7 olan zayıf sınıflandırıcıların ağırlığı 0 | Denek kararı: doğrulama BAcc'siyle ağırlıklandırılmış yumuşak oylama (§4.3.4, s.9) |

Parametre sayısı makalede verilmemiş. Kendi hesabım (doğrulanamadı): denek düzeyi için FC1 ≈ 128·6·7·6·1300 ≈ 41,9M; 128³ girişle 128·4³·1300 ≈ 10,6M. Mimari seçimi: 4 konv+5 FC'den 7 konv+2 FC'ye kadar iteratif tarama, benzer performans, en sığ iyi olan seçildi (s.8).

## 7. Eğitim ayarları
Ortak (eTable 4, arXiv v3 s.58): optimizer Adam (betas 0.9/0.999, eps 1e-8), kayıp çapraz entropi; AE için MSE ('mean squared entropy loss' diye yazılmış, eTable 5). Hiperparametre tablosu (eTable 4B, s.59), epoch / LR / batch / dropout / weight decay / patience:
- 3B denek-düzeyi AD-CN (Exp 1-3): 50 / 1e-4 / 12 / 0.5 / 0 / 10; boylamsal ve Extensive (Exp 4-5): patience 5; sMCI-pMCI CTT (Exp 6): LR 1e-5, patience 10; (Exp 7): LR 1e-5, patience 20.
- 3B ROI: 200 / 1e-5 / 32 / 0.5 / wd 1e-4 (AD-CN) veya 1e-3 (sMCI-pMCI) / patience 10 veya 20.
- 3B yama: 200 / 1e-5 / 32 / 0.5 / wd 1e-3 (single) ve 1e-4 (multi AD-CN) / patience 20 veya 15.
- 2B dilim: 50-100 / 1e-6 / 32 / dropout 0.8 / wd 1e-4 / patience 15.
- AE ön eğitim (eTable 5): denek-düzeyi 50 epoch (Minimal) ve 30 (Extensive), LR 1e-4, batch 12; ROI 200 ve 100 epoch, LR 1e-5, batch 32; yama 20 ve 15 epoch, LR 1e-5, batch 32; durdurma ölçütü epoch sayısı; doğrulama kaybı ve yeniden yapılandırma kalitesi görsel denetlenir (s.11).
Erken durdurma (§4.7, s.11): doğrulama kaybı N epoch (patience) boyunca en düşük değerden yüksek kalırsa durur; seçilen model, eğitim boyunca en yüksek doğrulama BAcc'li olandır. BAcc her epoch'ta tüm eğitim/doğrulama verisi üzerinden hesaplanır.
Artırma: ana metinde artırma yok (veri artırma tanımlanmamış); örneklem artımı yalnızca boylamsal veri ve 2B/3B-yama dilim/yama ile (doğrulanamadı: kodda ek artırma olabilir).
Hiperparametre arama: sistematik ızgara yok; mimari için sezgisel tarama (yukarıda), LR/weight decay eğitim doğruluğunun seyrine göre elle ayarlandı (§4.3, s.8).
Donanım ve süre: makalede GPU modeli ve eğitim süresi verilmiyor (doğrulanamadı); yalnızca HPC kaynağı Jean Zay (IDRIS/GENCI) teşekkür bölümünde anılıyor (s.16). Kütüphane: PyTorch, TensorboardX, scikit-learn, Nipype (§4.7).

## 8. Sonuçlar
Doğrulama (5 kat ort., Tablo 5, s.12) ve test (Tablo 6, s.13). Tüm Tablo 6 satırlarında önişleme Minimal, MinMax; denek düzeyinde bölme; AD-CN için AE (2B için ImageNet); sMCI-pMCI için AD-CN'den transfer.

| Görev | Yaklaşım | Ön işleme | Ön eğitim | Eğitim verisi | Doğrulama BAcc | BAcc ADNI test | BAcc AIBL | BAcc OASIS | Tablo |
|---|---|---|---|---|---|---|---|---|---|
| AD-CN | 3B denek | Minimal | AE | Baseline | 0.82 | 0.82 | 0.83 | 0.67 | T5 Exp3, T6 |
| AD-CN | 3B denek | Minimal | AE | Boylamsal | 0.85 | 0.85 | 0.86 | 0.68 | T5 Exp4, T6 |
| AD-CN | 3B denek | Extensive | AE | Boylamsal | 0.86 | (testte yok) | - | - | T5 Exp5 |
| AD-CN | 3B denek | Minimal | Yok, MinMax var | Baseline | 0.80 | - | - | - | T5 Exp2 |
| AD-CN | 3B denek | Minimal | Yok, ölçekleme YOK | Baseline | 0.50 | - | - | - | T5 Exp1 |
| AD-CN | 3B ROI (hipokampüs) | Minimal | AE | Baseline | 0.88 | 0.89 | 0.84 | 0.69 | T5 Exp8, T6 |
| AD-CN | 3B ROI | Minimal | AE | Boylamsal | 0.86 | 0.85 | 0.81 | 0.73 | T5 Exp10, T6 |
| AD-CN | 3B yama multi-CNN | Minimal | AE | Baseline | 0.81 | 0.81 | 0.81 | 0.64 | T5 Exp14, T6 |
| AD-CN | 3B yama multi-CNN | Minimal | AE | Boylamsal | 0.83 | 0.86 | 0.80 | 0.71 | T5 Exp16, T6 |
| AD-CN | 3B yama single-CNN | Minimal | AE | Baseline/Boylamsal | 0.74 / 0.76 | (testte yok) | - | - | T5 Exp12-13 |
| AD-CN | 2B dilim (ResNet-18) | Minimal | ImageNet | Baseline | 0.79 | 0.76 | 0.76 | 0.65 | T5 Exp18, T6 |
| AD-CN | 2B dilim | Minimal | ImageNet | Boylamsal | 0.74 | 0.74 | 0.73 | 0.61 | T5 Exp19, T6 |
| AD-CN | 2B dilim, SIZINTILI (dilim düzeyi bölme) | Minimal | ImageNet | Baseline | 1.00 | 0.75 | 0.80 | 0.68 | T5 Exp20, T6 |
| AD-CN | Doğrusal SVM (DARTEL GM) | SPM tabanlı | Yok | Baseline | 0.88 | 0.88 | 0.88 | 0.70 | T5 Exp21, T6 |
| AD-CN | Doğrusal SVM | SPM tabanlı | Yok | Boylamsal | 0.87 | 0.87 | 0.87 | 0.71 | T5 Exp24, T6 |
| sMCI-pMCI | 3B denek | Minimal | AD-CN transfer | Baseline | 0.73 | 0.69 | 0.52 | - | T5 Exp7, T6 |
| sMCI-pMCI | 3B denek | Minimal | AD-CN transfer | Boylamsal | 0.73 | 0.73 | 0.50 | - | T5 Exp6, T6 |
| sMCI-pMCI | 3B ROI | Minimal | AD-CN transfer | Baseline | 0.77 (T6'da 0.7 basılmış) | 0.74 | 0.60 | - | T5 Exp9, T6 |
| sMCI-pMCI | 3B ROI | Minimal | AD-CN transfer | Boylamsal | 0.78 | 0.74 | 0.57 | - | T5 Exp11, T6 |
| sMCI-pMCI | 3B yama multi-CNN | Minimal | AD-CN transfer | Baseline | 0.75 | 0.70 | 0.64 | - | T5 Exp15, T6 |
| sMCI-pMCI | 3B yama multi-CNN | Minimal | AD-CN transfer | Boylamsal | 0.77 | 0.70 | 0.44 | - | T5 Exp17, T6 |
| sMCI-pMCI | SVM (AD-CN'de eğitilip uygulanan) | SPM tabanlı | - | Baseline | 0.70 | 0.75 | 0.60 | - | T5 Exp23, T6 |
| sMCI-pMCI | SVM (aynı) | SPM tabanlı | - | Boylamsal | 0.70 | 0.76 | 0.68 | - | T5 Exp26, T6 |
| sMCI-pMCI | SVM (doğrudan sMCI-pMCI'da eğitilen) | SPM tabanlı | - | Baseline | 0.68 | (testte yok) | - | - | T5 Exp22 |

Not: Sentetik testler: ayrılamaz veri 0.5, tam ayrılabilir 1.00 BAcc (s.11). Çalışmaların literatür aralığı (sızıntısız): AD-CN doğruluk 0.76-0.91, sMCI-pMCI 0.62-0.83 (s.14). 3B yaklaşımlar arasında güçlü üstünlük yok; 3B yama biraz düşük eğilimli (s.15). Çoklu yama tezi: eşik sistemi aynı verilince multi ve single eşdeğer (eTable 6-7, s.16).

## 9. Açıklanabilirlik / ek analiz
Ana metinde (s.1-16) açıklanabilirlik/saliency/Grad-CAM analizi YOK. Yalnızca softmax olasılıklarının kalibre olmadığı uyarısı var (§4.3.4, s.9) ve hipokampüsün erken etkilendiği bilgisi ROI seçimini gerekçelendiriyor (§6, s.15). Bu nedenle bu makale açıklanabilirlik için kaynak değil.

## 10. Kod ve tekrarlanabilirlik
Makaleye göre: genel amaçlı araçlar Clinica'ya entegre (www.clinica.run), makaleye özgü kod https://github.com/aramis-lab/AD-DL, makalede kullanılan sürüm etiketi v.0.0.1; eğitilmiş modeller Zenodo 10.5281/zenodo.3491003 (§1, s.2). Veri: ADNI/AIBL/OASIS için Clinica dönüştürücüleri (BIDS) (§4.1, s.7). Sentetik veri üretim betikleri depoda (s.11).
Makale dışı (görev tanımından; doğrulanamadı): AD-DL arşivli, devamı https://github.com/aramis-lab/clinicadl (MIT). ClinicaDL komutları (ör. `clinicadl preprocessing`, `clinicadl train`) makalede geçmiyor, güncel dokümantasyondan doğrulanmalı. Bu makalenin 'Conv5_FC3' adı da makalede geçmiyor.

## 11. Güçlü ve zayıf yönler
GÜÇLÜ: Test kümesinin gerçekten kilitlenmesi; 3 ayrı test kümesi (aynı çalışma, benzer ve farklı çalışma); sızıntının sayısal gösterimi (1.00 vs 0.75/0.80); sentetik sağlık testleri; dört yaklaşımın aynı koşulda kıyası; SVM referansı; BAcc ve denek düzeyinde karar; tüm hiperparametreler ek tablolarda.
ZAYIF: CV tek sefer, tekrar yok, güven aralığı yok (s.16); katman başına çekirdek ayrıntıları ve tablolar ana metinde değil; test kümesi küçük (200 denek) ve yalnızca bir bölme; AIBL sMCI-pMCI yalnızca 33 denek; GPU/süre yok; yoğunluk ölçeklemesi dışında artırma çalışılmadı; mimari seçimi sezgisel; ADNI'ye göre OASIS tanı ölçütü eşdeğer değil (genelleme karşılaştırması sınırlı); CNN'ler SVM'yi geçmedi, yani 'sığ mimari + küçük veri' rejiminde; Tablo 6'da ROI sMCI-pMCI doğrulama değeri yazım hatası (0.7); 3B yama multi/single farkı eşikleme sistemine bağlı.

## 12. Bizim projeye uyarlama
Kurulumumuz: ADNI1 1.5T başlangıç T1, NC/MCI/AD, HD-BET → N4 → z-score → MNI152 afin → 128³, RID düzeyinde 5-kat CV × 3 tohum, birincil görev AD-NC, ikincil 3-sınıf.

### 12.1 Okuyucunun uyarlama notu
YAKINLIK: Bizim 128³ MNI afin kurulumu t1-linear'a kavramsal olarak yakın (N4 + MNI ICBM2009c afin + yoğunluk ölçekleme + denek düzeyi 3B CNN), ancak üç farkla: (1) HD-BET kafatası ayıklama var, t1-linear'da yok (t1-extensive'de maske tabanlı ayıklama var, sonuç eşdeğer, Exp 4 vs 5); (2) z-score, MinMax yerine; makale yalnızca MinMax denedi, ölçekleme olmadan eğitimin çöktüğünü (0.50) gösterdi, z-score için kanıt yok; (3) 128³ yeniden örnekleme (169×208×179 1 mm yerine; çözünürlük yaklaşık 1.3-1.7 mm) makalede denenmedi. Ek fark: biz yalnız ADNI1 1.5T başlangıç görüntüsü kullanıyoruz (makale 1455 denek, boylamsal, 1.5T+3T karışık olabilir: doğrulanamadı), bu da makalenin başlangıç-veri sonuçlarına (0.82 test) karşılık gelir.
MONAI İLE Conv5_FC3: 5 blok × [Conv3d(k=3, s=1, p=1) + BatchNorm3d + ReLU + MaxPool3d(2)] kanallar 1→8→16→32→64→128 (MONAI'de `monai.networks.nets.Classifier` / `Regressor` benzeri ya da düz nn.Sequential); sonra Dropout(0.5), Flatten, Linear(128·4³=8192 → 1300), ReLU, Linear(1300→50), ReLU, Linear(50→2) (FC arası ReLU/dropout ayrıntısı makalede 'Dropout 0.5' yalnızca konv sonrası, eTable 1; doğrulanamadı). Girişte 128 / 2⁵ = 4. Eğitim: Adam lr 1e-4, batch 12, ağırlık azalması 0, 50 epoch, patience 10, erken durdurma doğrulama kaybı ile, model seçimi doğrulama BAcc'ye göre; kayıp CE. İsteğe bağlı AE ön eğitimi (+0.02 BAcc, anlamlılığı kanıtlanmamış).
HEDEF İÇİN REFERANS: Bizim birincil AD-NC hedefi ≥%85 BAcc. Makalenin ADNI bağımsız test BAcc'si: 3B denek baseline 0.82 (AIBL 0.83), boylamsal 0.85; ROI 0.89; SVM 0.88. Yani ≥%85'e doğrudan 'başlangıç görüntüsü + tek 3B CNN' ile ulaşılması 0.82'ye göre zor; ROI/hipokampüs 0.89 (Tablo 6) ve SVM 0.88 en güçlü referanslar. 3 sınıf (NC/MCI/AD) için makalede referans yok. sMCI-pMCI makalede 0.69-0.74 (ADNI test).
ZORLUK: 3/5 (mimari basit, ama ≥%85 sınırda; küçük veri, 5×3 CV'nin hesap maliyeti).
VRAM TAHMİNİ (kendi hesabım, makalede yok; doğrulanamadı): 128³ girişte konv1 çıktısı 8×128³ ≈ 16,8 M float ≈ 67 MB/denek; BN+ReLU ve geri yayılım dahil ≈ 0,4-0,6 GB/denek, batch 12 için ≈ 5-8 GB fp32; AMP ile ≈ 3-4 GB; T4 16 GB'a sığar. Orijinal 169×208×179 girişte ≈ 2× fazla.

### 12.2 Hakemin kurulum farkı analizi
SIZINTI RİSKİ: 'düşük' değerlendirmesine katılıyorum. Test kümesi en başta ayrılıp hakem sürecine kadar kilitlendi, bölme denek düzeyinde, AE ön eğitimi eğitim katı içinde, transfer örtüşmesi denetlendi, sentetik testler ve otomatik sızıntı testleri var. Küçük belirsizlik: sMCI-pMCI ADNI testinin bileşimi tanımlanmamış ve tek bir sabit bölme tüm deneylerde yeniden kullanılmış.

FARKLAR VE BEKLENEN ETKİLERİ:
(1) HD-BET. Minimal'de kafatası ayıklama yok. Extensive'de MNI maskesiyle kaba ayıklama var ve sonuç eşdeğer (0.85 / 0.86, boylamsal, CV). Beklenti: nötr ile hafif olumlu arası. HD-BET, maske içi z-score'u anlamlı kılıyor. Risk: başarısız maskeler; QC şart.
(2) Maske içi z-score / MinMax. Makale yalnız ölçeklemenin ŞART olduğunu gösteriyor (0.50 → 0.80); z-score test edilmemiş. Beklenti: benzer sonuç. Arka plan değeri sabit (0 veya maske dışı min) tutulmalı. Aykırı değerlere karşı z-score MinMax'tan daha dayanıklı.
(3) 128³ / 169×208×179 @1 mm. Tam FOV'u izotropik vokselle sığdırmak yaklaşık ≥1.63 mm voksel gerektirir (208/128); aksi halde kırpma ya da anizotropi olur. Extensive 1.5 mm ve 121×145×121 ile eşdeğer çıktığı için ~1.5 mm'nin zarar vermemesi beklenir. Hipokampüs ayrıntısında küçük kayıp olabilir. Yan etki: FC1 girdisi 32256'dan 8192'ye iner (≈41.9M → 10.6M parametre); aşırı uyumu azaltabilir, Extensive'in 10240 girdisine yakın.
(4) Baseline-only. Doğrudan karşılığı Exp3: doğrulama 0.82 ± 0.05, ADNI test 0.82. Boylamsal 0.85 bize uygulanamaz. ADNI1 1.5T tek protokol olduğu için homojenlik hafif avantaj sağlayabilir. Ancak AD-NC örneklemi ≈416 denek; makalenin eğitim/doğrulama havuzu ≈466 artı 200 test.
(5) Protokol. Bizde ayrı kilitli test yok (5 kat × 3 tohum). Hiperparametreler aynı katlarda seçilip aynı katlarda raporlanırsa bu, makalenin 'b: bağımsız test yokluğu' türüne girer. Ya başta bir test kümesi kilitlenmeli ya da iç içe CV yapılmalı; hiç değilse hiperparametreler P03 değerlerinde dondurulup ayarlanmamalı. [Fable notu: VERI-SETI §4 ve bolme.py zaten %15 kilitli test ayırıyor; kural PROTOKOL'de açıkça yazıldı.]
(6) AE ön eğitimi planımızda yoksa beklenen kayıp yaklaşık -0.02 (0.82 → 0.80); makale de bu farkın anlamlı olmadığını söylüyor.
(7) Dış test yok (AIBL/OASIS yok); genelleme iddiası kurulamaz. [Fable notu: ADNI geldikten sonra OASIS-1 dış test planlı, PROTOKOL.]

HEDEF ≥%85 BAcc: Conv5_FC3 + baseline için makale referansı 0.82. Fold yayılımı (0.74-0.90) ile 0.85 tek koşuda mümkün, ama ortalamada iyimser. Gerçekçi beklenti 0.80-0.85. ≥0.85 için en güçlü referanslar ROI 0.89 ve SVM 0.88; ikisi de baseline. Bu nedenle 3B ROI (hipokampüs) kolu ve DARTEL/GM benzeri SVM temel çizgisi hedefe ulaşmak için daha olası. Sonuç: ≥0.85 'zorlayıcı ama makul', 0.82 alt referans. 3 sınıf (NC/MCI/AD) için makalede referans yok.

### 12.3 İmplementasyon yapılacaklar (hakem)
CONV5_FC3 (PyTorch/MONAI, 128³):
1) Blok × 5: Conv3d(k=3, s=1, p=1) → BatchNorm3d → ReLU → MaxPool3d(2, 2). Kanallar 1→8→16→32→64→128. 128³ giriş 2'nin kuvveti olduğu için adaptif dolguya gerek yok; çıktı 128×4×4×4.
2) Baş: Dropout(0.5) → Flatten → Linear(8192, 1300) → Linear(1300, 50) → Linear(50, C), C=2 veya 3. FC aralarına ReLU koymak makale dışı karardır (eTable 1'de yok) ve belgelenmeli. Softmax modele konmaz; CrossEntropyLoss kullanılır.
3) Optimizasyon: Adam(lr=1e-4, betas=(0.9, 0.999), eps=1e-8, weight_decay=0), batch 12, en çok 50 epoch. T4'te AMP önerilir; batch 12 sığmazsa gradyan biriktirme kullanılır ve raporlanır.
4) İki ayrı ölçüt: (a) erken durdurma, doğrulama kaybı en iyi değerin üstünde 10 ardışık epoch kalırsa; (b) checkpoint, en yüksek doğrulama BAcc. BAcc batch ortalaması değil, tüm doğrulama kümesi üzerinden hesaplanır.
5) Bölme: RID başına tek baseline hacim. Kat atamaları bir kez üretilip CSV olarak kaydedilir; tüm deneyler (CNN, ROI, SVM, ablasyon) aynı katları kullanır. '3 tohum' ile neyin değiştiği açıkça yazılır: başlatma/karıştırma mı, bölme mi.
6) Yoğunluk: maske içi z-score, ardından arka plan sabit değere set edilir. Ölçeklemesiz koşu yapılmaz; makalede 0.50'de çöküyor. İsteğe bağlı ablasyon: MinMax [0,1].
7) Artırma makalede yok. Eklenirse yalnız eğitim katında ve anlık (on-the-fly) yapılır; normalizasyon istatistikleri katlar arasında taşınmaz.
8) Sağlık testleri: (a) gürültülü kopyalar + rastgele etiket → BAcc ≈ 0.5; (b) bir yarıkürede yoğunluğu düşürülmüş sentetik iki sınıf → BAcc ≈ 1.0; (c) eğitim/doğrulama/test arasında RID kesişimi boş mu diye otomatik assert.
9) Raporlama: kat başına BAcc, AUC, duyarlılık ve özgüllük; ortalama ± SS (5×3). 3 sınıfta dengesizlik (229/382/187) nedeniyle BAcc ana metrik; ağırlıklı CE kullanmak makale dışı karardır.
10) İsteğe bağlı AE ön eğitimi: kodlayıcı = 5 konv bloğu, kod çözücü ayna; MSE kaybı; 50 epoch, lr 1e-4, batch 12; YALNIZ eğitim katındaki NC+MCI+AD ile. Beklenen kazanç yaklaşık +0.02.

PROTOKOL.md'YE ALINACAK KURALLAR:
K1. Bütün bölmeler denek (RID) düzeyinde yapılır. Normalizasyon istatistiği, öznitelik seçimi, artırma ve AE ön eğitimi bölmeden SONRA ve yalnız eğitim katında yapılır (geç bölme yasağı).
K2. Mimari ve hiperparametre seçimi yalnız eğitim/doğrulama verisiyle yapılır. Başta ayrılmış, yaş/cinsiyet eşli, kilitli bir test kümesi (ya da iç içe CV) tutulur; test yalnız dondurulmuş final modelde, bir kez koşulur.
K3. Kat atamaları sabit tohumla bir kez üretilir, kaydedilir ve tüm deneylerde aynen kullanılır.
K4. Transfer öğrenmede (ör. AD-NC → MCI görevleri) kaynak görevin eğitim deneklerinden hiçbiri hedef görevin test kümesinde yer almaz.
K5. Her hat sentetik ayrılamaz/ayrılabilir testlerden ve RID-örtüşme testinden geçer. Birincil metrik denek düzeyinde BAcc'dir. Her raporda doğrusal SVM temel çizgisi ile 3B denek ve ROI referansları (0.82 / 0.89 / 0.88) yan yana verilir.

## 13. Opus doğrulama
- **Sonuç:** **ÇELİŞKİ VAR** · **Güven:** yüksek
- **Hakemin okuduğu kaynak:** Yayıncı sürümü wen2020_yayinci.txt s.1-16: başlık/özet, §2.1-2.3.5, Tablo 1A/1B, §3, Tablo 2-4, §4.2-4.7, Tablo 5-6, §5.1-5.2, §6, teşekkür. arXiv v3 wen2020_arxiv_v3.txt yalnız ek tablolar: eTable 1-5 (PDF s.55-60). Ayrıca arXiv'de sMCI/pMCI test kümesinin bileşimi grep ile arandı, bulunamadı. eTable 6-7 ile eMethod'lar okunmadı.

### 13.1 Kontrol edilen sayılar
| İddia | Özetteki değer | Makaledeki değer | Durum | Yer |
|---|---|---|---|---|
| ADNI toplam katılımcı ve sınıf dağılımı | 1455 (CN 330, MCI 787, sMCI 298, pMCI 295, AD 336) | 1455 katılımcı. Tablo 2: CN 330/1830, MCI 787/3458, sMCI 298, pMCI 295, AD 336. Not: CN+MCI+AD=1453, metindeki 1455 ile 2 fark var; makalenin kendi tutarsızlığı, özetin hatası değil. | **doğru** | §3 s.6; Tablo 2 s.7 |
| AIBL katılımcı | 598 (CN 429, MCI 93, AD 76) | 598; CN 429, MCI 93 (sMCI 13, pMCI 20), AD 76 | **doğru** | §3 s.6; Tablo 3 s.7 |
| OASIS katılımcı | 193 (QC sonrası CN 76, AD 78) | 193 katılımcı (≥62 yaş); ön işleme sonrası 22 AD + 17 CN dışlandı. Tablo 4: CN 76, AD 78; 193-39=154 tutarlı. | **doğru** | §3 s.7; Tablo 4 s.7 |
| ADNI bağımsız test | 100 CN + 100 AD, yaş/cinsiyet eşli | Her sınıftan rastgele seçilmiş 100 denek, yaş ve cinsiyet eşli (100 CN, 100 AD) | **doğru** | §4.6.1 s.10 |
| Sızıntı olasılığı olan çalışma oranı | 32 çalışmadan 16 (10 belirsiz + 6 açık), ~%50 | 10 Unclear + 6 Clear; Bäckström sayılmıyor; yaklaşık %50. Özet bölümünde 'yarıdan fazla' deniyor. | **doğru** | §2.3.5 s.6; §6 s.14; Tablo 1B s.3 |
| Sızıntı simülasyonu (dilim düzeyinde bölme) | Doğrulama 1.00; ADNI test 0.75; AIBL 0.80 | 1.00 ± 0; ADNI 0.75; AIBL 0.80; OASIS 0.68 | **doğru** | Tablo 5 Exp20 s.12; Tablo 6 s.13; §6 s.14 |
| Bäckström: görüntü düzeyinde bölmenin kazancı | +8 puan doğruluk | Denek düzeyindeki bölmeye göre 8 yüzde puanı artış | **doğru** | §2.2 madde 1, s.4 |
| Yoğunluk ölçeklemenin etkisi | ölçeksiz 0.50 → MinMax 0.80 | 0.50 ± 0.00 → 0.80 ± 0.05 | **doğru** | Tablo 5 Exp1-2 s.12; §5.1.1 s.11 |
| 3B denek: AE / boylamsal / Extensive | 0.80 → 0.82 (AE); 0.85 (boylamsal); 0.86 (Extensive) | 0.82 ± 0.05; 0.85 ± 0.04; 0.86 ± 0.06. Extensive deneyi de boylamsal veriyle yapıldı (Exp5). | **doğru** | Tablo 5 Exp3-5 s.12 |
| En iyi CNN, AD-CN, ADNI test | 3B ROI baseline 0.89 (AIBL 0.84, OASIS 0.69) | 0.89 / 0.84 / 0.69 | **doğru** | Tablo 6 s.13 |
| 3B denek AD-CN test (baseline / boylamsal) | ADNI 0.82/0.85; AIBL 0.83/0.86; OASIS 0.67/0.68 | Aynı | **doğru** | Tablo 6 s.13 |
| SVM AD-CN baseline | 0.88 doğrulama; 0.88 ADNI; 0.88 AIBL; 0.70 OASIS | 0.88 ± 0.02; 0.88; 0.88; 0.70 | **doğru** | Tablo 5 Exp21; Tablo 6 |
| sMCI-pMCI ADNI test aralığı (CNN / SVM) | CNN 0.69-0.74; SVM 0.75-0.76; AIBL'de 0.44-0.68 | CNN 0.69-0.74; SVM 0.75/0.76. AIBL'de CNN 0.44-0.64, SVM 0.60-0.68; ikisi birlikte 0.44-0.68. | **doğru** | Tablo 6 s.13; §6 s.14 |
| t1-linear (Minimal) çıktısı | 169×208×179, 1 mm³, MNI ICBM2009c, N4 + afin | N4ITK; ANTs SyN ile afin kayıt (ICBM 2009c nonlinear symmetric); kırpma sonrası 169×208×179, 1 mm³ | **doğru** | §4.2 s.7 |
| Conv5_FC3 hiperparametreleri | Adam lr 1e-4, batch 12, 50 epoch, dropout 0.5, wd 0, patience 10; FC 1300-50-2 | Exp1-3: 50 / 1e-4 / 12 / 0.5 / 0 / 10. Exp4-5'te patience 5; Exp6-7'de lr 1e-5, patience 10 ve 20. FC1 1300, FC2 50, FC3 2. | **doğru** | eTable 1 s.55; eTable 4B s.59 |
| Konv kanalları ve blok yapısı (3B denek) | 8-16-32-64-128; Conv3³ p1 s1 + BN + ReLU + MaxPool 2³ s2 (adaptif dolgu) | Aynı. Çıktılar 8×85×104×90 ... 128×6×7×6. Dropout 0.5 FC1'den önce tek kez. FC'ler arasında aktivasyon tabloda yok. | **doğru** | eTable 1 s.55; §4.3.1 s.8 |
| Extensive giriş boyutu | 121×145×121; son çıktı 128×4×5×4 | Conv1 çıktısı 8×121×145×121; MaxPool5 çıktısı 128×4×5×4 | **doğru** | eTable 1 s.55 |
| ROI/yama mimarisi | 4 blok, 15-25-50-50, pad 0; FC 50-40-2, iki dropout 0.5 | Aynı (15×48³ → 50×2³; Dropout1, FC1 50, Dropout2, FC2 40, FC3 2) | **doğru** | eTable 2 s.56 |
| ROI ve yama tanımı | 50³ mm küp; yama örtüşmesiz, 36 adet; hipokampüs sol ve sağ ayrı, MNI'de elle merkezlenmiş | Aynı | **doğru** | §4.3.2 s.8 |
| ROI eğitim hiperparametreleri | 200 epoch / 1e-5 / 32 / 0.5 / wd 1e-4 (AD-CN), 1e-3 (sMCI-pMCI) / patience 10 veya 20 | Exp8 ve Exp10: wd 1e-4, patience 10. Exp9 ve Exp11: wd 1e-3, patience 20. | **doğru** | eTable 4B s.59 |
| AE ön eğitimi hiperparametreleri | denek düzeyi 50 (Minimal) / 30 (Extensive), 1e-4, batch 12; ROI 200 ve 100; yama 20 ve 15 | Aynı; kayıp 'mean squared entropy loss' diye yazılmış; AE AD+MCI+CN ile eğitiliyor | **doğru** | eTable 5 s.60 |
| Erken durdurma ve model seçimi | Doğrulama kaybı patience boyunca en iyiden yüksekse durur; seçilen model en yüksek doğrulama BAcc'li olan | Aynı; BAcc yalnız mevcut batch'te değil, tüm eğitim/doğrulama verisinde hesaplanıyor | **doğru** | §4.7 s.11 |
| Tablo 5/6: 3B denek sMCI-pMCI baseline / boylamsal | 0.73/0.69/0.52 ; 0.73/0.73/0.50 (Exp7 / Exp6) | Aynı (Exp6 boylamsal, Exp7 baseline) | **doğru** | Tablo 5-6 |
| Tablo 5/6: ROI sMCI-pMCI baseline / boylamsal | 0.77 (Tablo 6'da 0.7 basılmış)/0.74/0.60 ; 0.78/0.74/0.57 | Tablo 5'te 0.77 ± 0.05, Tablo 6'da 0.7 ± 0.05; ADNI 0.74, AIBL 0.60; 0.78/0.74/0.57 | **doğru** | Tablo 5 Exp9, Exp11; Tablo 6 |
| Tablo 6: ROI AD-CN boylamsal | 0.86/0.85/0.81/0.73 | Aynı | **doğru** | Tablo 6 |
| Tablo 6: yama multi-CNN AD-CN baseline / boylamsal | 0.81/0.81/0.81/0.64 ; 0.83/0.86/0.80/0.71 | Aynı | **doğru** | Tablo 6 |
| Tablo 6: yama multi-CNN sMCI-pMCI | 0.75/0.70/0.64 ; 0.77/0.70/0.44 | Aynı | **doğru** | Tablo 6 |
| Tablo 6: 2B dilim baseline / boylamsal | 0.79/0.76/0.76/0.65 ; 0.74/0.74/0.73/0.61 | Aynı | **doğru** | Tablo 6 |
| Tablo 6: SVM AD-CN boylamsal | 0.87/0.87/0.87/0.71 | Aynı | **doğru** | Tablo 6 |
| Tablo 5/6: SVM sMCI-pMCI (AD-CN'de eğitilmiş) | 0.70/0.75/0.60 ; 0.70/0.76/0.68; doğrudan eğitim 0.68 | Aynı (Exp22 0.68; Exp25 de 0.68, özette yok) | **doğru** | Tablo 5 Exp22-26; Tablo 6 |
| Tablo 5: yama single-CNN | 0.74 / 0.76 | 0.74 ± 0.08 / 0.76 ± 0.04 | **doğru** | Tablo 5 Exp12-13 |
| QC dışlamaları | ADNI 30 oturum, AIBL 7, OASIS 39; olasılık <0.5 dışlandı, <0.70 görsel kontrol | Aynı | **doğru** | §4.2 s.8; §3 s.6 |
| Hosseini-Asl kodunun yeniden üretilmesi | 0.99 yerine 0.82 | İki çalışma 0.82 doğruluk raporluyor; özgün çalışma 0.99 | **doğru** | §6 s.14 |
| Sızıntı türü başına çalışma sayısı (veri_bolme bölümü, özette 'sayımım') | a≈10, b≈10, c≈5, d=1 | Tablo 1B sayımı (Bäckström hariç): a=8 (Bäckström dahil 9), b=9, c=6, d=1 | **yanlış** | Tablo 1B s.3 |
| Tablo 1B satır sayısı | 17 satır; Bäckström iki tabloda | 10 Unclear + 7 Clear (Bäckström dahil) = 17; dipnot: Bäckström her iki kategoride | **doğru** | Tablo 1 s.3 |
| 5 katlı CV tek sefer, sabit tohum | random_state=2, her kat %20 | Aynı; tekrar yapılmadığı sınırlılık olarak belirtilmiş | **doğru** | §4.6.1 s.10; §6 s.16 |
| SVM'de C seçimi | İç içe 10 katlı CV | Aynı | **doğru** | §4.6.1 s.11 |
| Multi-CNN eşiği | BAcc<0.7 olan sınıflandırıcının ağırlığı 0 | Aynı | **doğru** | §4.3.4 s.9 |
| 2B dilim girişi | İlk ve son 20 dilim atılır, 129 RGB dilim; dropout 0.8 | Aynı (§4.3.3); dropout 0.8 eTable 4B | **doğru** | §4.3.3 s.8; eTable 4B |

### 13.2 Düzeltmeler (özette yanlış/eksik → doğrusu)
- veri_bolme: sızıntı türü başına sayım Tablo 1B'ye göre a (yanlış bölme)=8, Bäckström dahil 9; b (bağımsız test yok)=9; c (geç bölme)=6; d (yanlı transfer)=1. Özetteki 'a≈10, b≈10, c≈5' yanlış.
- ozet / sonuclar: makale §6'da ADNI testinde CNN aralığını 0.76-0.89 diye veriyor. Oysa Tablo 6'da 2B boylamsal model 0.74 (sızıntılı model ise 0.75). Aralık en iyi modeller ve sızıntısız deneyler için geçerli; özet bu çelişkiyi notsuz aktarmış.
- sizinti: sızıntılı çalışma oranı özet bölümünde 'yarıdan fazla', §2.3.5 ve §6'da 'yaklaşık yarı (16/32)' olarak geçiyor. Doğru ifade: 16/32 (%50); Bäckström hariç.
- anahtar_sayilar 'Extensive 0.86': bu değer boylamsal veriyle elde edildi (Exp5). Doğru karşılaştırma Minimal-boylamsal 0.85 ile, baseline 0.82 ile değil.
- ADNI 1455: Tablo 2'de CN+MCI+AD=1453 ediyor; 2 deneklik farkı makale açıklamıyor. Notla aktarılmalı.
- sonuclar: ADNI test sütunu sMCI-pMCI için de doldurulmuş. Ancak makale ADNI test kümesini yalnız 100 CN + 100 AD olarak tanımlıyor; sMCI/pMCI test deneklerinin nasıl ayrıldığı ana metinde yazmıyor. 'ADNI test sMCI-pMCI 0.69-0.74' değeri doğru, ama test kümesinin bileşimi doğrulanamadı diye işaretlenmeli.

### 13.3 Özetin atladığı önemli noktalar
- Tablo 6'daki test BAcc, 5 katın her birinden çıkan 5 modelin test sonucunun ortalaması; topluluk (ensemble) değil, tek final model de değil. Bizim CV × tohum raporlamamız için önemli bir protokol ayrıntısı.
- Oylama ağırlıkları doğrulama kümesinden hesaplanıp teste aynen uygulanıyor (§4.3.4 s.9).
- Boylamsal eğitimin baseline teste neden az katkı yaptığına dair yorum eksik: ileri evre örnekler eklenir, bireyler arası çeşitlilik artmaz (§6 s.15). Bizim baseline-only seçimimizi destekliyor.
- Makalenin önerisi eksik: performans/karmaşıklık dengesi için 3B ROI veya 3B denek yaklaşımı; ROI daha az bellek ve süre istiyor (§6 s.15-16).
- Ana metinde yalnız BAcc raporlanıyor; AUC, duyarlılık ve özgüllük Zenodo'da (§4.6.2 s.11).
- Minimal (1 mm, 169×208×179) ile Extensive (1.5 mm, 121×145×121) eşdeğer çıktı. Bu, 128³ gibi daha kaba çözünürlüğün tek başına zarar vermeyeceğine dair dolaylı kanıt; özet bu bağı kurmamış.
- Fold BAcc yayılımı (Exp3: 0.74-0.90) özette yok; hedef gerçekçiliği için önemli.
- SVM için yorum eksik: doğrulamada sMCI-pMCI'da DL'den düşük (0.68-0.70), testte ise en iyi CNN'lerle aynı düzeyde veya üstünde (§5.1.5, §5.2.5).
- AIBL sMCI-pMCI genellemesinin kötülüğü için makalenin önerdiği açıklama eksik: AIBL MCI'ları daha yaşlı (§6 s.15).

### 13.4 Doğrulanamayanlar
- ADNI sMCI-pMCI test kümesinin bileşimi ve büyüklüğü (ana metin ve arXiv'de grep ile bulunamadı; eMethod'larda olabilir)
- FC katmanları arasında ReLU olup olmadığı: eTable 1'de yok, ClinicaDL kodunda var olduğu biliniyor ama makaleden doğrulanamaz
- 'Conv5_FC3' adı makalede geçmiyor (grep: yok); ClinicaDL adlandırması olduğu makale dışı bilgi
- ADNI 1.5T/3T karışımı, GPU türü, eğitim süresi
- Özetin VRAM ve parametre tahminleri (hesap tutarlı: FC1 32256×1300≈41.9M, 8192×1300≈10.6M; VRAM ölçülmedi)
- eTable 6-7 değerleri; yalnız §6'daki özetleri (0.76/0.72 ve 0.74/0.76) görüldü

### 13.5 Okuyucunun işaretlediği anahtar sayılar (ham)
| İddia | Değer | Yer |
|---|---|---|
| ADNI toplam katılımcı | 1455 (CN 330, MCI 787, sMCI 298, pMCI 295, AD 336) | §3 s.6; Tablo 2 s.7 |
| AIBL katılımcı | 598 (CN 429, MCI 93, AD 76) | §3 s.6; Tablo 3 s.7 |
| OASIS katılımcı | 193 (QC sonrası CN 76, AD 78) | §3 s.7; Tablo 4 s.7 |
| ADNI bağımsız test | 100 CN + 100 AD, yaş/cinsiyet eşli | §4.6.1 s.10 |
| Sızıntı olasılığı olan çalışma oranı | 32 çalışmadan 16 (10 belirsiz + 6 açık), ~%50 | §2.3.5 s.6; Tablo 1 s.3 |
| Sızıntı simülasyonu (dilim düzeyi bölme) | Doğrulama 1.00; ADNI test 0.75; AIBL 0.80 | Tablo 5 Exp20, Tablo 6 s.12-13; §6 s.14 |
| Bäckström: görüntü düzeyi bölme kazancı | +8 puan doğruluk | §2.2 s.4 |
| Yoğunluk ölçekleme etkisi (3B denek, AD-CN) | ölçeksiz 0.50 → MinMax 0.80 | Tablo 5 Exp1-2 s.12; §5.1.1 s.11 |
| 3B denek AE ön eğitimi / boylamsal / Extensive | 0.80 → 0.82 (AE); 0.85 (boylamsal); 0.86 (Extensive) | Tablo 5 Exp2-5 s.12 |
| En iyi CNN AD-CN ADNI test BAcc | 3B ROI baseline 0.89 (AIBL 0.84, OASIS 0.69) | Tablo 6 s.13 |
| 3B denek-düzeyi AD-CN test (baseline / boylamsal) | ADNI 0.82 / 0.85; AIBL 0.83 / 0.86; OASIS 0.67 / 0.68 | Tablo 6 s.13 |
| SVM AD-CN (baseline) | 0.88 doğrulama; 0.88 ADNI; 0.88 AIBL; 0.70 OASIS | Tablo 5 Exp21; Tablo 6 s.12-13 |
| sMCI-pMCI ADNI test aralığı CNN / SVM | CNN 0.69-0.74; SVM 0.75-0.76; AIBL'de 0.44-0.68 | Tablo 6 s.13; §6 s.14 |
| Önişleme çıktısı (t1-linear) | 169×208×179, 1 mm³, MNI ICBM2009c, N4 + afin | §4.2 s.7 |
| Conv5_FC3 hiperparametreleri | Adam lr 1e-4, batch 12, 50 epoch, dropout 0.5, wd 0, patience 10; FC 1300-50-2 | eTable 1 ve eTable 4B (arXiv v3 s.55, s.59) |

## 14. Kaynaklar
- Wen J. ve ark. (2020) Med Image Anal 63:101694, DOI 10.1016/j.media.2020.101694 (yayıncı sürümü, tam metin okundu)
- arXiv:1904.07773 v3 (yalnızca ek materyal eTable 1-5, eFigure 1 okundu)
- Kod (makalede anılan): github.com/aramis-lab/AD-DL (v0.0.1), Clinica www.clinica.run; Zenodo 10.5281/zenodo.3491003
- ClinicaDL: github.com/aramis-lab/clinicadl (MIT) yalnızca görev tanımından, doğrulanamadı
