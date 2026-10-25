# 3. ARA RAPOR — UYGULAMA

## KAPAK

**Proje adı:** Alzheimer Hastalığının Erken Teşhisi İçin 3B Derin Öğrenme Tabanlı Karar Destek Sistemi
**Ders:** BSM 401 — Tasarım Projesi
**Bölüm:** Sakarya Üniversitesi, Bilgisayar Mühendisliği
**Grup üyeleri:**
- Baran Yeşilyurt — ortak altyapı, P01 (VoxCNN / VoxResNet), P02 (MedicalNet ResNet-18), dağıtım zinciri
- Ahmet Görkem Yavuz (G231210032) — P06 (CNN + LRP), P07 (ResAttNet), gereksinim analizi, arayüz tasarımı
- Ertuğrul Kabaoğlu (G231210376) — P11 (FCN-yama), P12 (DenseNet121), mimari ve akış diyagramları

**Depo:** https://github.com/YesilBaraN/tasarim-alzheimer
**Rapor tarihi:** 25 Ekim 2026

---

## 1. GİRİŞ — İkinci ara rapordan bu yana ne yaptık

İkinci ara raporda literatürü taramış, gereksinimleri çıkarmış ve sistemi tasarlamıştık. Bu raporun
konusu **tasarladığımız sistemin gerçekleştirilmesi**: altı mimariyi kodladık, ortak bir eğitim
altyapısı kurduk, gerçek MRI verisi bulup indirdik, uçtan uca ön işleme hattını çalıştırdık ve
modelleri aynı veri üzerinde aynı protokolle karşılaştırmaya başladık.

Projenin özgün katkısı tek bir model eğitmek değil — literatürdeki altı farklı 3B mimariyi
**aynı veri, aynı bölme, aynı eğitim yordamı** altında yan yana koymak. Bu kulağa basit geliyor
ama alandaki en yaygın sorun tam burada: makaleler birbirinden farklı veri alt kümeleri, farklı
ön işleme hatları ve farklı bölme yöntemleri kullandığı için yayınlanan doğruluk oranları
karşılaştırılabilir değil. Wen vd. (2020) ve Yagis vd. (2021), dilim düzeyinde bölme yapan
çalışmalarda başarının **25–55 puan** şiştiğini göstermiş. Bu yüzden işe önce bir *protokol*
yazarak başladık, model yazarak değil.

Bu raporda sırayla şunları anlatıyoruz: gerçekleştirdiğimiz sistem (§2), veri ve ön işleme (§3),
adil karşılaştırma protokolü ve sızıntı denetimi (§4), deneysel sonuçlar (§5), karıştırıcı ve
model-uyum analizleri (§6), test altyapısı (§7), çalışırken bulduğumuz şeyler (§8), kısıtlarımız
(§9) ve kalan iş (§10).

---

## 2. GERÇEKLEŞTİRİLEN SİSTEM

Depoda **33 Python dosyası, 5.535 satır** kod var. Her push'ta GitHub Actions bu kodu Windows ve
Ubuntu üzerinde ayrı ayrı derleyip test ediyor.

### 2.1 Ortak altyapı (`uygulama/ortak/`)

Altı mimarinin adil karşılaştırılabilmesi için eğitim döngüsünü **bir kez** yazdık; modeller
yalnızca bir arayüz sözleşmesi uyguluyor. Sözleşme tek satır:

```python
olustur(varyant: str, sinif_sayisi: int, girdi_boyut: int, **kw) -> nn.Module
```

Bir ekip üyesi `uygulama/<ad>_<makale>/model.py` içine bu fonksiyonu yazdığı anda model ortak
eğitim döngüsünden çağrılabilir hale geliyor ve sürekli bütünleştirme onu kendiliğinden bulup
sınıyor. Böylece hiç kimse kendi eğitim döngüsünü yazmıyor — yazsaydı karşılaştırma anlamsız olurdu.

| Dosya | Satır | Ne yapıyor |
|---|---|---|
| `egit.py` | 266 | Ortak eğitim döngüsü: AMP, gradyan biriktirme, erken durdurma, her epoch'ta checkpoint, koşu kaydı JSON'u |
| `veri.py` | 144 | `Dataset`/`DataLoader`, görev tanımları, artırma (çevirme + afin + yoğunluk), işçi başına tohumlanmış RNG |
| `bolme.py` | 402 | Etiket üretimi (ADNI / OASIS / BIDS / Radiata) ve denek düzeyinde kilitli test + 5-kat CV bölmesi |
| `metrikler.py` | 70 | BAcc, AUC, F1-makro, duyarlılık, özgüllük, karışıklık matrisi, kat/tohum özeti |
| `saglik_testi.py` | 176 | Sentetik veriyle uçtan uca hat denetimi (§7.2) |
| `onnx_disa_aktar.py` | 65 | Eğitilmiş checkpoint → ONNX |
| `vram_olc.py` | 124 | Model × boyut × batch için tepe VRAM ölçümü |
| `dis_test.py` | 142 | Başka veri setinde sıfır-atış test (sızıntı kapısıyla) |
| `eslestir.py` | 137 | Yaş/cinsiyet eşleştirilmiş kontrol seçimi |
| `svm_kos.py` | 123 | Voksel tabanlı lineer SVM temel çizgisi |
| `temel_cizgi.py` | 49 | Sığ 3B CNN temel çizgisi (SigCNN3D) |

**Tekrarlanabilirlik.** Her eğitim koşusu, bittiğinde kendi künyesini JSON olarak yazıyor: model,
varyant, görev, kat, tohum, tüm hiperparametreler, parametre sayısı, GPU adı, tepe VRAM, süre,
doğrulama ve test metrikleri, **git commit hash'i** ve kütüphane sürümleri (python, torch, cuda,
cudnn, monai, numpy). Commit hash'i olmayan bir koşu sonuç tablosuna alınmıyor — çünkü hangi
kodun ürettiği bilinmeyen bir sayı savunulamaz.

Koşu adları çakışmaya karşı korunuyor: ad, modelin yanı sıra öğrenme oranını, girdi boyutunu,
optimizatörü, ısınma süresini ve varsa ablation etiketini taşıyor. Bunu baştan böyle yapmamıştık;
öğrenme oranı taraması yaptığımızda koşuların birbirinin checkpoint'ini ezdiğini fark edip düzelttik.

### 2.2 Altı mimari

| Kod | Makale | Mimari | Parametre (128³) | Normalizasyon katmanı | Yazan |
|---|---|---|---|---|---|
| P01a | Korolev vd. 2017 | VoxCNN (düz 3B CNN, valid konvolüsyon) | 0,38M | 0 | Baran |
| P01b | Korolev vd. 2017 | VoxResNet (artık bağlantılı) | 3,21M | 15 | Baran |
| P02 | Chen vd. 2019 | MedicalNet ResNet-18, 23 veri setinde ön eğitimli | 32,99M | 17 | Baran |
| P06 | Böhle vd. 2019 | 4 bloklu 3B CNN + Katman Bazlı İlgi Yayılımı | 4,27M | 0 | Görkem |
| P07 | Zhang vd. 2021 | ResAttNet — artık bloklar + öz-dikkat | 34,21M | 22 | Görkem |
| P11 | Qiu vd. 2020 | Tam evrişimli ağ, yama tabanlı | 1,52M | 4 | Ertuğrul |
| P12 | Solano-Rojas vd. 2021 | 3B DenseNet-121 | 11,24M | 121 | Ertuğrul |

Buna iki **temel çizgi** ekledik: sığ bir 3B CNN (SigCNN3D, 0,07M parametre) ve voksel tabanlı
lineer SVM. Temel çizgiler olmadan "derin öğrenme işe yarıyor" demek mümkün değil — neye göre
yarıyor?

Ödünç aldığımız kodların lisansları `uygulama/<model>/LICENSE-*` altında duruyor. P14 (M3T
Transformer) için bulduğumuz gayriresmî uygulama GPL-3.0 olduğu için depoya kod almadık, yalnız
makaleyi okuyup inceleme notu yazdık.

### 2.3 Açıklanabilirlik

Karar destek sistemi, kararının *nereden* geldiğini gösteremiyorsa klinik ortamda kullanılamaz.
Üç yöntemi gerçekleştirdik, her biri ilgili makalenin kendi yöntemi:

| Dosya | Satır | Yöntem |
|---|---|---|
| `gorkem_P06_bohle/lrp.py` | 259 | Katman Bazlı İlgi Yayılımı (Böhle 2019'un kendi yöntemi) |
| `gorkem_P07_resattnet/gradcam.py` | 214 | Grad-CAM, dikkat haritalarıyla birlikte |
| `ertugrul_P11_qiu_fcn/harita.py` | 161 | Yama düzeyinde hastalık olasılık haritası (Qiu 2020) |
| `uygulama/api/isi_haritasi.py` | 180 | Mimariden bağımsız Grad-CAM + tıkama (occlusion) duyarlılığı |

`isi_haritasi.py` son `Conv3d` katmanını kendiliğinden bulduğu için altı mimarinin hepsinde
çalışıyor; model-özel yöntemler ise ilgili makalenin iddiasını sınamak için duruyor.

### 2.4 Dağıtım zinciri

Eğitilmiş model bir dosyada kalırsa karar destek sistemi olmaz. Zinciri uçtan uca kurduk:

```
checkpoint (.pth)  →  onnx_disa_aktar.py  →  model.onnx  →  tahmin.py (KararDestek)  →  olasılık + ısı haritası
```

`uygulama/api/tahmin.py` içindeki `KararDestek` sınıfı ONNX modelini `onnxruntime` ile yüklüyor,
ham NIfTI'yi ön işleme hattından geçirip olasılık döndürüyor. PyTorch kurulu olmayan bir makinede
de çalışıyor — hastane ortamında bu önemli bir kolaylık.

**Bu zincirin çalıştığını her push'ta sürekli bütünleştirme doğruluyor:** sağlık testinin ürettiği
checkpoint ONNX'e aktarılıyor, karar destek katmanı onu okuyup çıkarım yapıyor ve tablo üreteci
koşu kaydından satır basıyor. Zincirin herhangi bir halkası kırılırsa rozet kırmızıya dönüyor.

---

## 3. VERİ VE ÖN İŞLEME

### 3.1 Gerçek veriyi nasıl bulduk

Ortak veri seti olarak ADNI1 1.5T temel taramalarını hedeflemiştik ve ADNI ile OASIS başvurularımızı
yaptık; onay bekliyoruz. Onayı beklerken boş durmak yerine **anında indirilebilen, etiketli, 3B T1**
bir veri seti aradık. Bu arayış kendi başına bir bulguya dönüştü, çünkü böyle bir seti bulmak
sanıldığı kadar kolay değil:

- **OpenNeuro'nun 2.522 veri setinin tamamını** program yazıp taradık (arama motoruyla değil, depo
  listesini çekip her birinin katılımcı dosyasına bakarak). AD etiketli, yeterli denek sayısı olan
  tek bir set bulamadık.
- Kaggle'daki üç "ADNI/OASIS preprocessed" setini tek tek inceleyip **reddettik**: ya 2B dilim
  (dilim düzeyinde bölme sızıntı demek), ya denek kimliği yok (denek düzeyinde bölme yapılamaz),
  ya da veri kullanım sözleşmesine aykırı yeniden dağıtım.
- ANMerge'in yalnız FreeSurfer tabloları olduğunu, görüntü içermediğini gördük.

Sonunda **`radiata-ai/brain-structure`** koleksiyonunu bulduk. Bu koleksiyon beş çalışmayı
birleştiriyor ve kritik olan şu: AD etiketli denekler **yalnız OASIS'ten** geliyor, diğer üç kohort
tamamen sağlıklı. Hepsini karıştırmak sınıf ile tarayıcıyı karıştırmak olurdu — model hastalığı
değil cihazı öğrenirdi. Bu yüzden **yalnız OASIS-1 + OASIS-2** alt kümesini indirdik; bu ikisi
**aynı tarayıcıda** çekilmiş (Siemens Vision 1,5T), dolayısıyla birleştirmek karıştırıcı yaratmıyor.

İndirdiğimiz: **787 tarama, 1,6 GB.**

### 3.2 Denek seçimi — boylamsal veride tek oturum

Veri boylamsal: OASIS-2'de aynı deneğin beş oturumu olabiliyor. Etiket tablosunda her denek tek
satır olmak zorunda (yoksa aynı kişi hem eğitimde hem testte olur), dolayısıyla oturum seçmek
gerekiyor. Seçimi keyfi yapmadık, Wen vd. (2020) madde 2.2'yi uyguladık:

- **AD grubu:** deneğin **ilk AD tanılı** oturumu. En geç oturumu almak atrofiyi yapay olarak
  büyütür (en ileri evreyi seçmek demektir); temel oturumu almak ise kişi henüz sağlıklıyken
  çekilmiş görüntüyü AD etiketlemek olur. İlk AD oturumu ikisinin de hatasını yapmıyor.
- **Kontrol grubu:** **yalnız kararlı sağlıklılar** — hiçbir oturumunda AD tanısı almamış denekler.
- **OASIS-2'de 14 denek izlem süresince sağlıklıdan AD'ye dönüşüyor.** Bunları kontrol grubundan
  çıkardık ve AD grubuna kendi AD oturumlarıyla aldık. Dönüşen birini "sağlıklı" saymak kontrol
  grubunu kirletirdi: o kişinin beyninde hastalık süreci zaten başlamıştır, model onu haklı olarak
  AD'ye benzer bulur ve bunun için ceza alır.

Bu seçimin daha iyi olduğunu ölçtük:

| | Temel oturum | **Kararlı kontrol + ilk AD oturumu** |
|---|---|---|
| AD / sağlıklı | 165 / 183 | **178 / 170** (oran 0,96) |
| Yaş farkı (Welch) | p = 0,84 | **p = 0,39** |
| OASIS-2 dengesi | 65 AD / 85 NC | **78 AD / 72 NC** |

**Yaş süzgeci.** Süzgeç uygulamazsak kontrol grubunun yaş ortalaması 51,8'e düşüyor (OASIS-1'de
18 yaşından itibaren gönüllü var), AD grubunun ise 76. Böyle bir veriyle eğitilen model Alzheimer'ı
değil **yaşı** öğrenir. Yaş ≥ 60 süzgeciyle fark istatistiksel olarak kayboluyor.

**Son veri kümesi: 348 denek — 178 AD / 170 sağlıklı.**
OASIS-1: 100 AD / 98 NC · OASIS-2: 78 AD / 72 NC — her iki sınıf her iki kohortta mevcut.

### 3.3 Ön işleme hattı

`onisleme/onisle.py` (497 satır) şu adımları uyguluyor:

```
oku → kafatası ayıklama (HD-BET) → N4 bias düzeltme → MNI152 afin kayıt
    → maske içi z-score → kırpma ve 128³'e boyutlandırma → float16 .npy + meta JSON
```

Adım sırası Wen vd. (2020) `t1-linear` hattını izliyor ve bu sıra **önemli**: normalizasyon
kayıttan *sonra* yapılıyor. Başta ters yapmıştık ve kayıt her hacimde çöktü (§8.1).

Radiata verisi kaynağında zaten kafatası ayıklanmış ve MNI'ye hizalanmış olduğu için
`--kafatasi hazir --kayit yok` hafif yolunu kullandık: yalnız maske, z-score ve boyutlandırma.
**787 taramanın 787'si işlendi, hacim başına 0,1 saniye, tek uyarı yok, çıktı 3,1 GB.**

**Ön işleme kaynağı konusunda şeffaflık.** Radiata'nın hattı CAT12 + FSL FLIRT (12 serbestlik
dereceli afin) kullanıyor ve hedef şablonu `MNI152NLin2009cAsym` — **bizim hattımızla aynı şablon.**
Bu beklenmedik bir şans: iki hat farklı araçlar kullanıyor ama aynı standart uzayı hedefliyor.
ADNI onayı geldiğinde ham veriyi kendi hattımızdan geçirmeyi planlıyoruz, böylece her şey tek
hatla üretilmiş olur.

---

## 4. ADİL KARŞILAŞTIRMA PROTOKOLÜ VE SIZINTI DENETİMİ

`uygulama/PROTOKOL.md` bağlayıcı kurallarımızı tutuyor. Uygulamadaki karşılıkları:

**Denek düzeyinde bölme.** Bölme `StratifiedGroupKFold` ile denek kimliği üzerinden yapılıyor:
kilitli test **53 denek**, çapraz doğrulama **295 denek**, **5 kat**. Katlar kohort × sınıf dengeli,
yani her kat hem AD/NC oranını hem OASIS-1/OASIS-2 oranını koruyor.

**Sızıntı denetimi.** `bolme.py dogrula` test ve CV kümelerinin denek kimliklerini kesiştiriyor ve
kesişim boş olmak zorunda. Çıktı: **TEMİZ — 0 kesişim.**

**Test kümesi bir kez açılıyor.** Hiperparametre ve öğrenme oranı seçimi yalnız doğrulama katları
üzerinden yapılıyor. `tablo_uret.py` bunu kodla zorluyor: öğrenme oranı taraması varsa doğrulama
dengeli doğruluğuna göre tek değer seçiliyor, test metrikleri yalnız raporlanıyor.

**Aynı eğitim yordamı.** Bütün modeller aynı optimizatör (AdamW), aynı öğrenme oranı, aynı girdi
boyutu (128³), aynı artırma kümesi ve **aynı etkin batch** ile eğitiliyor. VRAM'e sığmayan modeller
`--batch 2 --accum 2` kullanıyor; etkin batch 4'te sabit kaldığı için karşılaştırma bozulmuyor.

**Paylaşılan bölme, paylaşılmayan veri.** Bölme haritasını (`oasis_bolme_haritasi.csv`) depoya
koyuyoruz — yalnız denek kimliği, bölüm ve kat numarası, hiçbir klinik sütun yok. Böylece üç kişi
de birebir aynı bölmeyi kullanıyor ama veri kullanım sözleşmesi ihlal edilmiyor. Görüntüleri ve
ağırlıkları `.gitignore` dışlıyor; herkes veriyi kendi hesabıyla indiriyor.

---

## 5. DENEYSEL SONUÇLAR

### 5.1 Koşu düzeneği

RTX 3050 Laptop (4 GB) üzerinde, AD vs sağlıklı ikili görevinde, tohum 2026, en çok 60 epoch,
erken durdurma sabrı 12. Aşağıdaki tablo **kat 0** ölçümleridir; 1–4. katlar koşmaya devam ediyor.

### 5.2 Kat 0 sonuçları

| Model | Parametre | Doğrulama BAcc | Test BAcc | **Test AUC** | Duyarlılık | Özgüllük | Doğrulama→test boşluğu | Süre |
|---|---|---|---|---|---|---|---|---|
| **P12 DenseNet121** | 11,24M | 0,760 | 0,697 | **0,792** | 0,778 | 0,615 | +0,064 | 23,8 dk |
| **P02 MedicalNet (ön eğitimli)** | 32,99M | 0,706 | **0,700** | 0,758 | 0,593 | 0,808 | **+0,006** | 11,0 dk |
| P01 VoxCNN | 0,38M | 0,809 | 0,620 | 0,758 | 0,778 | 0,462 | +0,189 | 31,6 dk |
| P02 ResNet-18 sıfırdan | 32,99M | 0,841 | 0,620 | 0,738 | 0,778 | 0,462 | +0,221 | 13,5 dk |
| Temel: SigCNN3D | 0,07M | 0,664 | 0,584 | 0,654 | 0,630 | 0,538 | +0,080 | 19,5 dk |
| P06 CNN + LRP | 4,27M | 0,500 | 0,500 | 0,603 | 0,000 | 1,000 | — | 6,4 dk |

**Birincil metriğimiz AUC**, dengeli doğruluk değil. Gerekçesini §9.2'de ölçümle anlatıyoruz.

### 5.3 Ön eğitim ablasyonu — kazanç tepe başarıda değil, genellemede

P02'yi iki kez koştuk: bir kez MedicalNet ön eğitimli ağırlıklarla, bir kez sıfırdan. **Mimari
birebir aynı, tek fark ön eğitim.**

| | Doğrulama BAcc | Test BAcc | Test AUC | **Boşluk** |
|---|---|---|---|---|
| Sıfırdan | **0,841** | 0,620 | 0,738 | **0,221** |
| MedicalNet ön eğitimli | 0,706 | **0,700** | **0,758** | **0,006** |

Sıfırdan eğitilen model doğrulamada belirgin şekilde **daha iyi**, test'te **daha kötü**. Bu klasik
aşırı öğrenme imzası: 236 eğitim deneğiyle 33 milyon parametreli bir ağ eğitim katını ezberliyor.
Ön eğitimin kazandırdığı şey tepe başarı değil **genelleme** — ki Chen vd. (2019)'un MedicalNet
iddiası tam olarak budur.

Burada test farkına (0,700 vs 0,620) değil **boşluğa** bakıyoruz, çünkü test farkı 53 deneklik tek
bir kümeden geliyor ve gürültülü; boşluk ise her koşunun kendi içinde ölçülen bir büyüklük.
0,006'ya karşı 0,221 farkı tek koşuda bile anlamlı bir işaret.

**Bundan çıkardığımız metodolojik ders:** doğrulama kümesi, aşırı öğrenen yapılandırmayı
ödüllendirebiliyor. Bu yüzden *hiperparametre* seçimini doğrulamada bırakıyoruz ama *mimari
karşılaştırmasını* kilitli test üzerinden yapıyoruz, ve `tablo_uret.py` bu ayrımı kodla koruyor.

### 5.4 P06 neden öğrenmedi — dürüst bir negatif sonuç

P06 kat 0'da hiç öğrenmedi: kayıp 13 epoch boyunca tam `ln 2 = 0,693`'te çakılı kaldı, karışıklık
matrisi `[[26, 0], [27, 0]]`, yani her deneğe "sağlıklı" dedi. Mimariyi inceleyip nedenini bulduk
ve bu yapısal bir şey:

P06, **parametre sayısı girdi boyutuna bağlı olan tek modelimiz**. Global havuzlama yerine
`flatten + Linear` kullanıyor:

```
linear_in = 64 × (girdi/16)³       32³ için 512,  128³ için 32.768
fc1 = Linear(32.768, 128)  =  4,19M parametre  =  modelin %98'i
```

Evrişimle öznitelik çıkaran kısım yalnızca 0,08M. Yani 128³ girdide P06, 236 denekle eğitilen dev
bir lineer sınıflayıcıya dönüşüyor. Diğer altı mimari adaptif havuzlama kullandığı için girdi
boyutundan bağımsız.

İlk tahminimiz "normalizasyon katmanı yok, o yüzden" idi; **bu tahmini ölçümle çürüttük** —
VoxCNN'in de hiç normalizasyon katmanı yok ve o AUC 0,758 veriyor. Ayırt edici etken normalizasyon
eksikliği değil, o tek dev tam bağlantılı katman.

Modeli "çalışmıyor" diye bir kenara atmadık; protokolün kendi çözümünü uyguluyoruz: öğrenme oranı
taraması (1e-3 / 3e-4 / 1e-4). Tarama da başarısız olursa bulgumuz şu olacak ve raporlanabilir bir
sonuçtur: *Böhle vd. (2019) mimarisi yayınlandığı haliyle 128³ girdide eğitilemiyor, çünkü makale
daha küçük girdi kullanıyordu.*

---

## 6. ANALİZ — SONUCUN GERÇEKTEN NEREDEN GELDİĞİ

Tek bir doğruluk sayısı yayımlamak kolay; o sayının neyi ölçtüğünü göstermek zor. Üç analiz aracı
yazdık.

### 6.1 Karıştırıcı tavanı — model beyne mi bakıyor?

Veri kümemizde **cinsiyet dengesiz**: AD grubunun %54'ü, kontrol grubunun %72'si kadın
(Fisher kesin testi p = 0,0009). Eşleştirme yapmak 348 deneği ~210'a düşüreceği için eşleştirmedik;
yerine karıştırıcının ne kadar işe yaradığını **ölçtük**.

`karsilastirma/altgrup_analiz.py`, yalnız demografiden AD tahmin eden bir lojistik regresyonun aynı
test kümesindeki AUC'sini hesaplıyor. Bu, **beyne hiç bakmayan** bir modelin alabileceği skordur:

| Yalnız şunu kullanan model | Test AUC |
|---|---|
| Yalnız cinsiyet | 0,418 |
| Yalnız yaş | 0,359 |
| Cinsiyet + yaş | 0,354 |

**Üçü de şans seviyesinin (0,500) altında.** Yani test kümemizde demografik bilgi AD tahmininde
kullanılabilir bir sinyal taşımıyor. Modellerimizin 0,758–0,792 bandındaki AUC'si bu tavanın
yaklaşık 0,35–0,44 üzerinde. **Sonuç karıştırıcıdan gelmiyor; modeller gerçekten görüntüden
bilgi çıkarıyor.** Ayrıca VoxCNN'in AUC'si cinsiyetten bağımsız: kadınlarda 0,756, erkeklerde 0,750.

### 6.2 Alt grup dağılımı

| Alt grup | n | AD | VoxCNN AUC |
|---|---|---|---|
| Kadın | 38 | 19 | 0,756 |
| Erkek | 15 | 8 | 0,750 |
| OASIS-1 | 30 | 15 | 0,729 |
| OASIS-2 | 23 | 12 | 0,788 |
| Yaş < 75 | 27 | 13 | 0,698 |
| Yaş ≥ 75 | 26 | 14 | **0,839** |

Model ileri yaşta belirgin şekilde daha iyi (0,839 vs 0,698). Bu klinik olarak tutarlı: atrofi ileri
evrede daha belirgin. Erken teşhis hedefi açısından ise bu bir **uyarı** — asıl değerli olan genç
hastada erken yakalamak ve orada daha zayıfız.

### 6.3 Model uyumu — darboğaz mimari mi, veri mi?

Tabloya bakıp 0,792 ile 0,758'i kıyaslamak sorunun yarısı. Diğer yarısı: modeller birbirinden
*gerçekten* farklı şeyler mi öğreniyor? `karsilastirma/uyum_analiz.py` bunu üç bağımsız yolla ölçüyor
(çökmüş koşular analiz dışı):

- **İkili uyum:** ortalama **%71**, ortalama Cohen kappa **+0,425**
- **İndirgenemez çekirdek:** 53 deneğin **6'sını hiçbir model** bilemiyor, **19'unu hepsi** biliyor,
  **28'inde ayrışıyorlar**
- **Topluluk tavanı:** olasılık ortalamasının AUC'si **0,762**; en iyi tek model 0,758 → **+0,004**

Son iki ölçüm birlikte okununca ilginç bir şey çıkıyor: modeller deneklerin yarısında ayrışıyor
**ama ortalamaları hiçbir şey kazandırmıyor.** Eğer bu ayrışma *tamamlayıcı* olsaydı — her model
verinin farklı ama geçerli bir yönünü görseydi — topluluk kazandırırdı. Kazandırmadığına göre
ayrışma **gürültü**: her model aynı karar yüzeyinden gürültülü bir çekiliş. 236 eğitim deneğiyle
kayıp yüzeyi düz olduğu için her koşu farklı bir rastgele köşeye oturuyor.

Bu bir **ön işaret**, sonuç değil — tek kat ve sınırlı sayıda koşu üzerinden. Beş kat bittiğinde
yeniden koşturacağız. Ama doğrulanırsa tartışma bölümümüzün omurgası olacak: *bu veri hacminde
mimari seçimi sanıldığı kadar belirleyici değil; asıl kısıt veri.*

---

## 7. TEST ALTYAPISI VE SÜREKLİ BÜTÜNLEŞTİRME

### 7.1 Sürekli bütünleştirme

`.github/workflows/testler.yml` her push'ta **Ubuntu ve Windows üzerinde ayrı ayrı** şunları koşuyor:

1. Sürüm raporu (python, torch, monai, numpy, SimpleITK)
2. Model duman testi — altı mimarinin hepsi sözleşmeye uyuyor mu, ileri/geri geçiş çalışıyor mu
3. Ön işleme duman testi — z-score, maske, boyutlandırma, uçtan uca hat, meta JSON
4. Sağlık testleri (§7.2)
5. ONNX dışa aktarma
6. Karar destek çıkarımı
7. Tablo üreteci

Bir ekip üyesi `model.py` yazdığı anda CI onu kendiliğinden bulup 32³ rastgele hacimde sınıyor.
Sözleşmeye uymazsa rozet kırmızıya dönüyor. Bunun işe yaradığını bilerek bir modeli bozup
doğruladık. Kuralımız: **rozet kırmızıysa önce o düzeltilir**, üstüne yeni iş yığılmaz.

### 7.2 Sağlık testleri — hattın kendisini sınamak

`saglik_testi.py` gerçek veri, GPU veya internet olmadan eğitim hattını uçtan uca sınıyor ve dört
şeyi kanıtlıyor:

| Test | Beklenen | Neyi kanıtlıyor |
|---|---|---|
| Rastgele etiket | doğrulama BAcc ≈ 0,5 | Hat etiketten bağımsız sinyal **uydurmuyor** — sızıntı yok |
| Ayrılabilir iki sınıf | doğrulama BAcc ≈ 1,0 | Hat gerçekten öğrenebiliyor — kayıp ve optimizatör doğru bağlı |
| Bölme kesişimi | boş | Denek düzeyinde ayrım çalışıyor |
| Koşu kaydı | zorunlu alanlar tam | Tekrarlanabilirlik künyesi eksiksiz, farklı LR'ler birbirini ezmiyor |

İlk iki test birlikte önemli: tek başına "model öğrendi" demek yetmez, **öğrenmemesi gerektiğinde
öğrenmediğini** de göstermek gerekir. Sızıntılı bir hat rastgele etiketlerle de yüksek skor verir.

### 7.3 Ölçüm araçları

`vram_olc.py` her model × girdi boyutu × batch için tepe VRAM'i ölçüyor. Bunu tahminle
yapmıyoruz, çünkü tahminimiz bir kez on kat yanlış çıktı (§8.3).

---

## 8. ÇALIŞIRKEN BULDUĞUMUZ ŞEYLER

Bu bölüm bize en çok şey öğreten kısım. Sentetik testlerin göremediği hataları ancak gerçek veriyle
koşunca bulduk.

### 8.1 MNI kaydı her hacimde çöküyordu
Hata mesajı "tüm örnekler hareketli görüntü tamponunun dışına düşüyor" idi. İki nedeni vardı:
başlatıcı olarak `MOMENTS` kullanıyorduk ve z-score'u kayıttan *önce* uyguluyorduk. Normalize
edilmiş veride moment tabanlı başlatma anlamsız. `GEOMETRY` başlatıcıya geçip adım sırasını
düzelttik. Sonuç: 143 hacmin 143'ünde kayıt metriği −0,53 ile −0,46 arasında, tek uyarı yok.

### 8.2 Türkçe klasör adı kütüphaneyi kırıyordu
`SimpleITK`, kullanıcı klasörümüzdeki Türkçe karakter yüzünden dosya açamıyordu; `nibabel` aynı
dosyayı sorunsuz okuyordu. Windows'un 8.3 kısa yol biçimine çevirerek çözdük. Burada ince bir
ayrıntı var: **yalnız klasörü kısaltmak gerekiyor** — dosyayı da kısaltınca uzantı bozuluyor
(`sub-01_ses-01_T1w.nii.gz` → `SUB-01~1.GZ`) ve dosya biçimi tanınamıyor.

### 8.3 VRAM tahminimiz on kat yanlıştı
Kurulum belgemizde "ResNet-18 128³ sığmaz, 8–12 GB gerekir" yazıyordu. Ölçtük: **1,58 GB.**
Bu yanlış tahmin yüzünden neredeyse bütün koşuları bulut GPU'suna taşıyacaktık. Dersimiz: bellek
tahmini yapmayın, ölçün.

### 8.4 Sessiz yavaşlama — en pahalı dersimiz
VoxResNet'i batch 4 ile başlattık ve epoch başına **7 dakika** sürdüğünü gördük; VoxCNN aynı veride
32 saniye sürüyordu. Ölçüm nedeni gösterdi: VoxResNet batch 4'te 3,59 GB istiyor, kartımız 4,0 GB.
Araç "sığdı" diyor, program çökmüyor — ama Windows WDDM kalan belleği sistem RAM'ine taşıdığı için
**13 kat yavaşlıyor.** 60 epoch o hızda 7 saat sürecekti.

Kuralımızı buna göre yazdık: **"sığdı" demek yetmiyor; eşik kartın kapasitesi değil, kapasitesinin
yaklaşık %75'i.** 4 GB kartta hedef ≤ 3,0 GB. Aşan modeller `--batch 2 --accum 2` ile koşuyor ve
etkin batch sabit kaldığı için karşılaştırma bozulmuyor. Ayrıca `expandable_segments` ayırıcısını
açtık; dar VRAM'de bellek parçalanması tek başına yüzlerce MB yiyor.

### 8.5 Kendi sonuç tablomuz sonuçlarımızı eliyordu
`tablo_uret.py`, geliştirme kartında (RTX 3050) üretilen koşuları tablodan çıkarıyordu. O kural,
modellerin bu karta *sığmadığını varsaydığımız* dönemde yazılmıştı. Ölçünce hepsinin sığdığını
görünce kural gerçek sonuçlarımızın tamamını çöpe atmaya başladı.

Kuralı silmek yerine doğru değişmez üzerine kurduk: karşılaştırmayı bozan şey kartın markası değil,
**eğitim yordamının farklı olması**. 4 GB kartta `--batch 2 --accum 2` koşan model, 24 GB kartta
`--batch 4` koşanla aynı etkin batch'i görür ve karşılaştırma geçerlidir. Yeni dışlama ölçütü
etkin batch ve girdi boyutu. Kart adı yalnızca nota düşüyor: *metrikler karşılaştırılabilir,
süre sütunu karşılaştırılamaz.*

### 8.6 "±0,000" yanıltıcıydı
Tek koşuda tablomuz `0,620±0,000` yazıyordu. Sapma sıfır değil, **hesaplanamıyor** — ama o yazım
"bu sonuç kat değişiminden etkilenmiyor" diye okunuyor. `(tek koşu)` yazacak şekilde düzelttik.

---

## 9. KISITLAR VE DÜRÜST DEĞERLENDİRME

### 9.1 Veri ölçeği
236 eğitim deneğiyle 3B evrişimli ağ eğitmek literatürdeki ölçeklerin (binlerce denek) çok
altında. §6.3'teki topluluk ölçümü bu kısıtın etkisini doğrudan gösteriyor. ADNI onayı geldiğinde
asıl koşular orada yapılacak; bu küme dış test setine dönüşecek.

### 9.2 Dengeli doğruluğun eşiği kattan teste taşınmıyor
Bunu ölçtük ve raporlamamızı buna göre kurduk. VoxCNN'de doğrulama katında seçilen karar eşiği
(0,4821) test sonucunu hiç değiştirmiyor; oysa test kümesinde 0,736 dengeli doğruluk veren bir
eşik **var**. Daha iyi eşik aramak bunu çözmüyor — 236 eğitim / 53 test deneğiyle olasılık
dağılımları kat başına kayıyor.

Bu yüzden **birincil metriğimiz AUC**: eşikten bağımsız olduğu için bu sorundan etkilenmiyor.
Dengeli doğruluğu protokolün sabit kuralıyla raporluyoruz ve kısıtı yazıyoruz. Beş kat bittiğinde
kat-ortalaması eşiğe geçeceğiz.

### 9.3 Afin normalizasyon beyin hacmini kısmen siliyor
Verinin 12 serbestlik dereceli afin dönüşümle MNI'ye normalize edildiğinin sonucunu ölçtük:
sınır kutusu her denekte **150×187×159 mm (±2)** ve maske hacmi deneğin gerçek kafa içi hacmiyle
**ilişkisiz (r = −0,18)**. Yani global kafa/beyin boyutu bir öznitelik olarak **kaldırılmış**;
model bölgesel şekle ve yoğunluk örüntülerine dayanmak zorunda.

Bu, Wen vd. (2020) `t1-linear` hattının bilinen bir özelliği, ama **kısıt olarak yazmamız gerekiyor**:
toplam beyin hacmi kaybı Alzheimer'ın en güçlü işaretlerinden biri ve kısmen normalize edilmiş durumda.

### 9.4 Cinsiyet dengesizliği
Eşleştirme yerine ölçmeyi seçtik (§6.1) ve ölçüm karıştırıcının test kümesinde işe yaramadığını
gösterdi. Yine de dengesizlik veri kümesinin bir özelliği olarak duruyor ve raporda ortak değişken
olarak belirtiliyor.

### 9.5 Koşu sayısı
PROTOKOL 5 kat × 3 tohum istiyor; ölçülen sürelerle bu 9 model için ~40–45 GPU-saat. Şu an 5 kat ×
1 tohum koşuyoruz (~12–15 saat) ve tohum tekrarını öne çıkan modellere ayırmayı planlıyoruz.
**Bu bir sapmadır ve raporun son halinde böyle yazılacaktır.**

### 9.6 Tek merkez
Bütün veri tek tarayıcıdan (Siemens Vision 1,5T). Bu karıştırıcıyı ortadan kaldırıyor ama
genellemeyi sınamıyor. Çoklu-merkez genelleme için `radiata-ai` koleksiyonunun diğer üç kohortu
(DLBS, IXI, NKI-RS — 3.007 tarama, 2.043 sağlıklı denek) hazır duruyor.

---

## 10. KALAN İŞ VE TAKVİM

| Sıra | İş | Durum |
|---|---|---|
| 1 | Kat 0'ın kalan üç modeli (VoxResNet, P11, P07) | 🔄 koşuyor |
| 2 | P06 öğrenme oranı taraması | 🔄 kuyrukta |
| 3 | Kat 1–4 (9 model × 4 kat) | 🔄 kuyrukta, ~12–15 saat |
| 4 | Beş kat ortalamasıyla sonuç tablosu + alt grup ve uyum analizlerinin tekrarı | ☐ |
| 5 | Voksel SVM temel çizgisi | ☐ |
| 6 | Üç sınıf (NC / MCI / AD) ikincil görevi | ☐ ADNI'ye bağlı |
| 7 | ADNI onayı → ham veriyi kendi hattımızdan geçirme → asıl koşular | ☐ onay bekliyor |
| 8 | Dış test: ADNI'de eğitilen model → OASIS sıfır-atış | ☐ |
| 9 | Arayüz gerçekleştirmesi (mock-up'lar tasarlandı) | ☐ |
| 10 | Final rapor ve sunum | ☐ |

**Danışmana sormak istediklerimiz:**
1. Tohum tekrarı konusunda (§9.5) 5 kat × 1 tohum kabul edilebilir mi, yoksa tam protokol şart mı?
2. ADNI onayı gecikirse OASIS sonuçlarıyla savunmaya girmek uygun olur mu?
3. Ön işleme kaynağı: OASIS'i Radiata'nın hazır sürümünden mi alalım, onay gelince ham veriyi kendi
   hattımızdan mı geçirelim? (Hedef şablon ikisinde de aynı.)

---

## KAYNAKLAR

[1] A. Korolev, A. Safiullin, M. Belyaev, Y. Dodonova, "Residual and plain convolutional neural
networks for 3D brain MRI classification," *IEEE ISBI*, 2017.

[2] S. Chen, K. Ma, Y. Zheng, "Med3D: Transfer learning for 3D medical image analysis,"
*arXiv:1904.00625*, 2019.

[3] J. Wen vd., "Convolutional neural networks for classification of Alzheimer's disease:
Overview and reproducible evaluation," *Medical Image Analysis*, c. 63, 2020.

[4] M. Böhle, F. Eitel, M. Weygandt, K. Ritter, "Layer-wise relevance propagation for explaining
deep neural network decisions in MRI-based Alzheimer's disease classification," *Frontiers in
Aging Neuroscience*, c. 11, s. 194, 2019.

[5] X. Zhang vd., "An explainable 3D residual self-attention deep neural network for joint atrophy
localization and Alzheimer's disease diagnosis using structural MRI," *IEEE Journal of Biomedical
and Health Informatics*, 2021. (3D ResAttNet, arXiv:2008.04024)

[6] S. Qiu vd., "Development and validation of an interpretable deep learning framework for
Alzheimer's disease classification," *Brain*, c. 143, sy. 6, 2020.

[7] B. Solano-Rojas, R. Villalón-Fonseca, "A low-cost three-dimensional DenseNet neural network
for Alzheimer's disease early discovery," *Sensors*, c. 21, 2021.

[8] S. Yagis vd., "Effect of data leakage in brain MRI classification using 2D convolutional
neural networks," *Scientific Reports*, c. 11, 2021.

[9] D. S. Marcus vd., "Open Access Series of Imaging Studies (OASIS): Cross-sectional MRI data in
young, middle aged, nondemented, and demented older adults," *Journal of Cognitive Neuroscience*,
c. 19, sy. 9, 2007.

[10] D. S. Marcus, A. F. Fotenos, J. G. Csernansky, J. C. Morris, R. L. Buckner, "Open Access
Series of Imaging Studies: Longitudinal MRI data in nondemented and demented older adults,"
*Journal of Cognitive Neuroscience*, c. 22, sy. 12, 2010.

[11] Radiata AI, "brain-structure: A multi-study collection of preprocessed structural brain MRI,"
HuggingFace Datasets, 2025. [Çevrimiçi]. https://huggingface.co/datasets/radiata-ai/brain-structure

[12] C. Gaser vd., "CAT: A computational anatomy toolbox for the analysis of structural MRI data,"
*Imaging Neuroscience*, 2024.

[13] F. Isensee vd., "Automated brain extraction of multisequence MRI using artificial neural
networks," *Human Brain Mapping*, c. 40, sy. 17, 2019. (HD-BET)

[14] N. J. Tustison vd., "N4ITK: Improved N3 bias correction," *IEEE Transactions on Medical
Imaging*, c. 29, sy. 6, 2010.

[15] M. J. Cardoso vd., "MONAI: An open-source framework for deep learning in healthcare,"
*arXiv:2211.02701*, 2022.

> Tam liste ve her makalenin ayrıntılı inceleme notu: `makaleler/MAKALE-LISTESI.md` ve
> `makaleler/<kişi>/P*.md`. On beş makalenin tamamı §13 doğrulama bölümüyle incelenmiştir;
> dördünde sayısal çelişki saptanıp belgelenmiştir.
