# VERİ SETİ — Ortak set kararı, erişim, etiket ve bölme kuralları

Son güncelleme: 25.10.2026 (Baran). Kaynak bağlantılar en altta.

## 1. Karar
| | Seçim | Neden |
|---|---|---|
| **Ortak veri seti** | **ADNI1, 1.5T, T1 ağırlıklı, başlangıç (baseline/screening) taramaları; sınıflar NC / MCI / AD** | Formla birebir uyumlu; literatürde en yaygın ve kıyaslanabilir alt küme (≈229 NC / 382 MCI / 187 AD ≈ 798 denek); Wen 2020, Lian 2020, Korolev 2017 hepsi bu küme üzerinde |
| **Köprü veri seti** | **OASIS-1** (416 denek, 18–96 yaş; 60+ yaşta 100 kişide çok hafif–orta demans) | Erişim formu hızlı; ADNI onayı (~2 hafta) beklenirken ön işleme ve eğitim kodu burada ayağa kalkar; ADNI gelince aynı kod koşar |
| **Reddedilen** | Kaggle "Alzheimer's Dataset (4 class of Images)", "Alzheimer MRI Preprocessed", Hugging Face/Kaggle ADNI aynaları | Kaynağı belirsiz, denek kimliği yok (dilim sızıntısı), 2B, sınıflar NC/MCI/AD değil; ADNI aynaları DUA ihlali |

## 2. ADNI erişimi (kritik yol — bu hafta başlat)
1. https://ida.loni.usc.edu → "Apply for access" → ADNI seç.
2. **Data Use Agreement** (DUA) okunup kabul edilir.
3. Başvuru formu: kurum = Sakarya Üniversitesi; amaç = lisans tasarım projesi (metin `SUREC.md §8`); veri = ADNI1 1.5T T1 sMRI + klinik tanı tablosu.
4. **Başvuruyu danışman kurumsal e-postasıyla yapması** önerilir (lisans öğrencisinin tek başına kabul edilip edilmediği doğrulanamadı); üç öğrenci ekip üyesi yazılır.
5. Komite "genellikle iki hafta içinde" yanıt verir; eksik veya amaçsız başvurular reddedilir.
6. Onay sonrası IDA → **Download → Image Collections → Other Shared Collections** → `ADNI1: Screening 1.5T` (veya `ADNI1: Complete 1Yr 1.5T`) → NIfTI biçimi seçilir (DICOM gelirse `dcm2niix`).
7. IDA → **Download → Study Data** → `ADNIMERGE.csv` (tanı sütunları `DX_bl`, `DX`) ve isteğe bağlı `DXSUM_PDXCONV_ADNIALL.csv`.

**DUA kuralları (bağlayıcı):**
- Katılımcı düzeyinde veri (görüntü, tablo) **yeniden dağıtılamaz**: Drive/GitHub/Kaggle'a ham veri konmaz, WhatsApp'tan gönderilmez.
- Her öğrenci kendi IDA hesabından indirir **veya** başvuruda adı geçen kişiler arasında kalır; ön işlenmiş 128³ tensörlerin ekip içi paylaşımı ADNI'ye e-posta ile sorulur ("derived data" sayılır).
- Katılımcıyı tanımlamaya çalışmak yasak; yayınlarda ADNI atıf cümlesi zorunlu.
- Hesap yıllık yenilenir.

## 2b. "GitHub'dan direkt alamaz mıyız?" — doğrulanmış cevap (25.10.2026)
Yasal, anında ve etiketli (NC/MCI/AD) 3B T1 verisi veren bir GitHub/Kaggle yolu **yok**. ADNI ve OASIS DUA'ları yeniden dağıtımı yasaklar; "ADNI NIfTI" yükleyen depo/Kaggle seti hem ihlal hem kaynağı belirsiz. Bekleme süresini kısaltan seçenekler:
| Seçenek | Ne verir | Süre | Nasıl |
|---|---|---|---|
| **ADNI'ye kendin başvur** (danışman e-postasını beklemeden, paralel) | ortak set | ~2 hafta | ida.loni.usc.edu, üniversite e-postası (@ogr.sakarya.edu.tr), danışman adı + proje açıklaması; kabul ölçütlerine lisans öğrencisi uyuyor (deneyim raporu bulunamadı, eksik/odaksız başvuru reddediliyor) |
| **OASIS-1 formu — her üye ayrı** | NC vs demans (CDR), ~416 denek | formdan sonra onay (otomatik mi elle mi belirtilmiyor) | kurumsal e-posta + ayrıntılı araştırma açıklaması zorunlu; DUA (Temmuz 2022) 3. kişiye paylaşımı yasaklar → **Görkem ve Ertuğrul da kendi adına başvurur** |
| **OpenNeuro ds007561** (CC0, kayıtsız) — *doğrulandı 25.10: participants.tsv* | **20 denek: 14 Control, 5 MCI, 1 AD** (61–84 yaş), 1 mm MPnRAGE T1w + UCB-J PET (Wisconsin, Bendlin lab) | anında (`datalad`/git: github.com/OpenNeuroDatasets/ds007561) | https://openneuro.org/datasets/ds007561 — gerçek etiketli ama çok küçük → **yalnız hat/kod testi**, karşılaştırmaya girmez |
| OpenNeuro ds006148 (CC0) — *doğrulandı* | 266 katılımcı, "nörodejenerasyon + negatif BOLD" (Weill Cornell); participants.tsv'de **tanı sütunu yok** | anında | etiket bulunmadan kullanılamaz; phenotype/ klasörü ileride bakılabilir |
| **OASIS-2** (boylamsal) | 150 denek (60–96 yaş), 373 oturum, CDR/MMSE; NC vs demans | DUA formu → XNAT daveti ~1 hafta; ham ~18 GB | https://sites.wustl.edu/oasisbrains/home/oasis-2 — OASIS-1'e ek köprü |
| **OASIS-1'i küçült** | yalnız ≥60 yaş (~200 denek) ve denek başına tek ortalama hacim (PROCESSED/T88_111 `_masked_gfc`) | form sonrası; yalnız gereken disc'ler (disc başına ~1.5 GB) | ortak köprü set için yeterli; FreeSurfer disc'leri (11 × 9.5 GB) indirilmez |
| **ADNI'yi küçült** | onay gelince IDA'da özel koleksiyon: yalnız baseline, ör. 100 NC + 100 AD (+100 MCI); ADNI'nin hazır ön işlenmiş "MPR; GradWarp; B1; N3; Scaled" görüntüleri (Korolev 2017 bunları kullandı) | ~2 hafta onay, indirme birkaç GB | ortak set küçük başlar, sonra genişler |
| **MIRIAD** (UCL) | 46 AD + 23 HC, 1.5T, boylamsal | kayıt + DUA (süre doğrulanamadı) | https://www.nitrc.org/projects/miriad/ — küçük köprü |
| **IXI** (CC BY-SA) | ~600 sağlıklı T1, **etiketsiz** | anında | https://brain-development.org/ixi-dataset/ — yalnız ön işleme/kod testi |
| Kaggle OASIS/ADNI aynaları, HF `medarc/adni-mini`, GitHub "ADNI preprocessed" release'leri | — | — | **kullanılmaz** (DUA ihlali / şartlar kapalı); ADNI onayı gelince HF kapılı setin şartları ayrıca okunur |

## 2c. İkinci tur arama — "başka ücretsiz yol var mı?" (25.10.2026)

Soru tekrar araştırıldı. **Sonuç değişmedi: anında indirilebilen, etiketli, işe yarar büyüklükte 3B T1 AD veri seti yok.**
Ama aramadan iki işe yarar şey çıktı; biri doğrudan yapılacak işi değiştiriyor.

### ✅ Bulgu 1 — ADNI ve AIBL için **ortak başvuru formu** var (yapılacak işi değiştirir)
AIBL (Australian Imaging, Biomarkers and Lifestyle), ADNI ile **aynı LONI/IDA altyapısını** kullanıyor ve
**tek formla ikisine birlikte** başvurulabiliyor:

> https://ida.loni.usc.edu/collaboration/access/appApply.jsp?project=ADNI&project=AIBL

Neden önemli:
- **Aynı emekle iki kohort.** Başvuru yükü değişmiyor, onay süresi aynı.
- **Gerçek bağımsız dış test.** AIBL, ADNI'ye çok yakın tanı ölçütleri kullanıyor; Wen 2020 ve Bron 2021
  genellemeyi tam olarak AIBL üstünde ölçüyor. PROTOKOL'ün "Dış test" bölümü için OASIS-1'den **daha uygun**:
  OASIS-1'de yalnız CDR var (üç sınıf yapılamıyor), AIBL'de NC/MCI/AD var → **üç sınıf görevinde de dış test**
  yapılabilir.
- Risk: IDA'da proje başına ayrı onay olabilir; ortak form ikisinin de kullanım şartlarını kabul ettiriyor.
  Doğrulanmadı: iki projenin onayı aynı anda mı geliyor.

**Yapılacak değişiklik:** ADNI başvurusu yalnız ADNI formundan değil, **yukarıdaki ortak formdan** yapılacak.

### ❌ Bulgu 2 — EPAD: ücretsiz ama bize uygun değil
[EPAD](https://ep-ad.org/index.php/open-source-data/) (1356 katılımcı, 3B T1w + FLAIR, ücretsiz) elendi, üç sebep:
1. **Erişim anında değil:** ADDI "AD Workbench" hesabı + Data Access Terms + EPAD ekibinin onayı; görüntü
   istekleri "daha uzun sürebiliyor" deniyor.
2. **Veri buluttan çıkmıyor:** AD Workbench güvenli bir bulut çalışma alanı. Bizim planımız Kaggle/Colab'da
   kendi hattımızı koşmak; veriyi indirip ön işleyemezsek `onisle.py` zincirine hiç giremez.
3. **Etiket uygun değil:** EPAD bir **önleme/preklinik** kohortu — katılımcıların çoğu demans değil. AD vs NC
   ikili görevi için anlamlı bir AD grubu yok.

### Diğer kontroller (hepsi daha önceki sonucu doğruladı)
| Kaynak | Sonuç |
|---|---|
| **OpenNeuro tümü** | T1w + demans etiketi olan tek set hâlâ **ds007561** (20 denek, CC0, anında). Oradaki AD/FTD setleri (ds004504, ds006036, ds004796) **yalnız EEG**; ds003592 yaşlanma kohortu, demans tanısı yok. |
| **MIRIAD** | 46 AD + 23 HC, 708 tarama. Ama **kayıt + MIRIAD Data Use Agreement** gerekiyor ve DUA üçüncü tarafa dağıtımı kısıtlıyor — "CC BY" makalenin lisansı, verinin değil. Küçük ama meşru bir köprü; OASIS-1 gecikirse ikinci seçenek. |
| **OASIS-1/2/3** | Hepsi Data Use Terms + online form; istekler **OASIS ekibi tarafından elle inceleniyor**, yayınlanmış bir süre yok. Barındırma **NITRC-IR**'a taşınmış (eski dokümanlardaki `central.xnat.org` güncel değil) — onay NITRC hesabına proje erişimi olarak geliyor. |
| **Kaggle / HuggingFace / GitHub "ADNI preprocessed" aynaları** | Yine **kullanılmaz**: DUA ihlali, kaynağı belirsiz, çoğu 2B dilim. |

### Karar (değişmedi, bir ekleme ile)
1. **Bugün:** ortak **ADNI+AIBL** formu + OASIS-1 formu (üç üye ayrı ayrı) → kritik yol, ~2 hafta.
2. **Bugün, beklemeden:** **ds007561** indir (kayıt gerekmez) → `onisle.py`'yi gerçek MRI'da dene (HD-BET + MNI
   kaydı sentetik testte atlanıyor). 20 denek karşılaştırmaya girmez, yalnız hattın doğruluğunu kanıtlar.
3. OASIS-1 gecikirse **MIRIAD**'a başvur (46 AD + 23 HC).
4. AIBL onayı gelirse: iç test ADNI1, **dış test AIBL (üç sınıf dahil) + OASIS-1 (ikili)**.

## 2d. OpenNeuro'nun **tamamı** tarandı (25.10.2026)

Önceki turlarda OpenNeuro'ya arama motoruyla bakılmıştı. Bu sefer kovanın kendisi tarandı: her veri setinin
`participants.tsv` dosyası indirilip demans/AD/MCI terimleri arandı (`scratchpad/openneuro_tara.sh` yöntemi).

| | |
|---|---|
| Taranan veri seti | **2522** |
| `participants.tsv` içeren | 1493 |
| Demans/AD/MCI terimi geçen | 7 |
| **Gerçek aday** | **2** (diğer 5'i yanlış pozitif) |

### Adaylar
| Set | Katılımcı | Etiketler | Görüntü | Karar |
|---|---|---|---|---|
| **ds007857** | 289 | **212 CN · 49 MCI · 1 DAT** · 27 n/a (+ MoCA skoru) | **559 T1w, 5,2 GB** | ⚠ AD yok (tek DAT) → ana görev için kullanılamaz. Ama indirilebilir **en büyük etiketli T1 seti**: hattı 261 denekle prova etmek ve P15 (Dhinagar 2023) usulü ön eğitim için değerli |
| ds005048 | 35 | **16 Hafif AD · 1 Orta AD · 10 Normal · 6 MCI** | ❌ **yok** — `.set`/`.fdt` yani EEGLAB; sadece EEG | Etiketleri en iyi olan set ama MRI içermiyor → kullanılamaz |
| ds007561 | 20 | 14 Control · 5 MCI · 1 AD | 20 T1w, 284 MB | ✅ indirildi; yalnız hat denemesi |

**Yanlış pozitifler:** ds003382, ds003397, ds004796 (tanı değil, *ailede demans öyküsü* sütunu), ds005892
(22 Control / 18 PD-NC / 15 PD-MCI — Parkinson, bizim görev değil).

### Sonuç
**Anında indirilebilen, etiketli, AD vs NC yapmaya yetecek 3B T1 veri seti OpenNeuro'da yok.** Tarama
tamamlandığı için bu artık bir tahmin değil, ölçüm. ADNI/OASIS başvurusu **kritik yol olmaya devam ediyor.**

### ⚠ "Setleri birleştirip veriyi büyütelim" — yapılmaz
AD deneklerini bir setten, kontrolleri başka setten almak veriyi büyütmez, **sonucu geçersiz kılar**: farklı
tarayıcı, farklı protokol, farklı merkez demek; model hastalığı değil **tarayıcıyı** öğrenir ve doğruluk
yapay olarak yükselir. Bu, Yagis 2021 [P05] ve Wen 2020 [P03] notlarındaki sızıntı ailesinin ta kendisi.
Birden çok kohort ancak şu iki biçimde kullanılır: (a) **biri eğitim, diğeri dış test** (PROTOKOL "Dış test"),
(b) her kohort kendi içinde dengeli sınıflara sahipse ve merkez etkisi raporlanıyorsa. Sınıfları kohortlara
bölüştürmek **asla**.

### Veri indirme: `veri/indir.py`
Açık (CC0) setleri herkesin **birebir aynı** indirmesi için tek komut:
`python veri\indir.py --hedef D:\veri`

Denek başına tek tarama seçer (ds007857'de birden çok oturum var), boyut doğrulaması yapar, yarım kalan
dosyayı yeniden indirir, `--dogrula` ile eldekini sınar ve hedef **depo içindeyse reddeder** (veri git'e
sızmasın). ADNI/OASIS bu betikle inmez: başvuru + DUA gerektirirler.

### Yeni araç: `bolme.py etiket-bids`
Herhangi bir BIDS/OpenNeuro setini tek komutla etiket CSV'sine çevirir — tanı sütununu kendiliğinden bulur,
yazım farklarını (`Control`/`CN`/`Normal`, `AD`/`DAT`/`Dementia`…) tek bir eşleme tablosundan çözer, sınıfı
çok küçük olan sette uyarı verir:

```powershell
python uygulama\ortak\bolme.py etiket-bids ^
    --katilimcilar D:\veri\ds007561\ham\participants.tsv ^
    --veri D:\veri\ds007561\islenmis ^
    --cikti veri\ds007561_etiket.csv
```
ds007561'de koşuldu: `20 denek → {0: 14, 1: 5, 2: 1}` + "en küçük sınıfta 10'dan az denek var → SONUCLAR
tablosuna giremez" uyarısı. ADNI/OASIS dışındaki her açık seti aynı komut okur. Çıktıya **`kaynak`** sütunu
da yazılır (hangi kohorttan geldiği), birden çok set birleştirildiğinde gerekli.

### Çok kohortlu çalışma: `birlestir` + kohort dengeli katlar
```powershell
python uygulama\ortakolme.py birlestir --girdi veri\ds007561_etiket.csv veri\ds007857_etiket.csv --cikti veriirlesik_etiket.csv
```
- Kimlik çakışırsa (iki sette de `sub-01`) kimliklerin başına kaynak eklenir.
- **Kohort × sınıf tablosu basılır.** Bir kohortta tek sınıf varsa `!! TEHLİKE` uyarısı verir ve o birleşimin
  PROTOKOL'e göre kullanılamayacağını söyler — sınıf ile tarayıcı birbirine karışmış demektir.
- `bol` komutu `kaynak` sütununu görünce katları **hem sınıf hem kohort** bakımından dengeler; aksi hâlde bir
  kat ağırlıklı olarak tek bir tarayıcıdan gelir ve o katın sonucu merkez etkisini ölçer. Hücrelerden biri kat
  sayısından küçükse bu mümkün olmaz → yalnız sınıfa göre dengelenir ve bu durum ekrana yazılır.

## 2e. Adı geçen üç Kaggle seti — tek tek incelendi (25.10.2026)

Ekipten "şu setlere baktın mı" diye sorulan üç set, kendi açıklama metinleri okunarak değerlendirildi.
Üçü de reddedildi ama **sebepleri farklı**; aşağıda her biri kendi gerekçesiyle.

### 1. `ninadaithal/imagesoasis` — gerçek OASIS, ama 2B JPG
Kendi açıklamasından: *OASIS MRI veri seti, 80.000 görüntü, **461 hasta**. Özgün `.img/.hdr` dosyaları FSL
ile NIfTI'ye çevrilmiş. Sinir ağı eğitimi için **2B görüntüler** kullanılmış: beyin z ekseninde 256 dilime
bölünmüş, her hastadan **100–160 arası dilimler** seçilmiş. Sınıflar **CDR** değerlerinden türetilmiş.
`.nii` taramalar **`.jpg`'ye çevrilmiş**.*

Üçü ciddi, biri ölümcül:
- **2B JPG.** Bizim altı modelimiz de 3B hacim alıyor (VoxCNN, VoxResNet, MedicalNet ResNet-18, ResAttNet,
  FCN, DenseNet121). 2B dilim bu ağlara girmez.
- **JPG dönüşümü yıkıcı.** 8 bit, kayıplı sıkıştırma. MRI yoğunlukları nicel veridir; z-score, N4 bias
  düzeltme ve atrofi ölçümü JPG'den sonra anlamını yitirir.
- **Hasta başına ~173 dilim.** 80.000 / 461 ≈ 173. Görüntü düzeyinde rastgele bölersen aynı hastanın
  dilimleri hem eğitimde hem testte olur — Yagis 2021 [P05] bunun doğruluğu **25–55 puan** şişirdiğini
  ölçtü. PROTOKOL madde 1 (denek düzeyinde bölme) bu veriyle uygulanamaz.
- **OASIS yeniden dağıtımı.** Kaynak açıkça OASIS; OASIS Data Use Terms üçüncü tarafa dağıtımı yasaklar.

**Ama bu set bir şeyi doğru gösteriyor:** OASIS gerçekten bizim istediğimiz veri. Doğru yol onu
oasis-brains.org formundan almak (`§2`), ki zaten başvuru listemizde — **henüz gönderilmedi** (`SUREC §9` satır 7).

### 2. `mohiburrahmanrifat/alzheimer` — sızıntı açıkça ilan edilmiş
6.336 görüntü: 3.200 Non_Demented · 2.240 Very_Mild · 896 Mild. Bu sayılar `tourist55/alzheimers-dataset-4-class-of-images`
setinin sayılarıdır (Moderate sınıfı çıkarılmış hâli). Açıklamasında şu cümle geçiyor:

> *"The dataset has been randomly divided into training, validation, and testing subsets using a fixed random seed."*

**Görüntü düzeyinde rastgele bölme.** Dilimler hastalardan geliyor ve hasta kimliği yok; dolayısıyla bu
hazır bölme sızıntı içeriyor ve düzeltilemez. Bu setle üretilen her doğruluk şişkindir. Sabit tohum
tekrarlanabilirlik sağlar ama **yanlışı tekrarlanabilir kılar**, doğru yapmaz.

### 3. `uraninjo/augmented-alzheimer-mri-dataset` — en ağır sızıntı
Kendi açıklamasından: *"Data is augmented from an existing dataset"* — kaynak yine `tourist55`. Artırılmış
(döndürülmüş, kaydırılmış) kopyalar özgün görüntülerle aynı havuzda. Rastgele bölünce **aynı görüntünün
artırılmış kopyası** hem eğitimde hem testte oluyor. Bu, dilim sızıntısından da beter: model ezberlediği
görüntünün kopyasını test ediyor.

### Üçünün ortak sorunu, tek cümlede
Hiçbirinde **denek kimliği** yok. PROTOKOL'ün 1. maddesi "bölme her zaman denek düzeyinde" diyor ve bu
veriyle o madde **uygulanamaz** — isteğe bağlı değil, teknik olarak imkânsız. Projenin tezi sızıntısız
değerlendirme olduğu için, bu setlerle çalışmak raporun literatür bölümüyle yöntem bölümünü çelişkiye düşürür.

## 2f. ANMerge / AddNeuroMed (Synapse syn22252881) — incelendi, elendi (25.10.2026)

Ekipten önerilen aday. **Gerçek ve ciddi bir kohort:** AddNeuroMed konsorsiyumunun boylamsal çalışması,
**1702 katılımcı**, çok modlu (klinik, MRI, genotip, transkriptom, proteom, metabolom).
Yayın: *ANMerge: A comprehensive and accessible Alzheimer's disease patient-level dataset*,
J. Alzheimer's Disease (2020).

**Ama MRI verisi görüntü değil, tablo.** Synapse ağacı okunarak doğrulandı:

| Klasör | İçerik |
|---|---|
| `Data/MRI/` | `ANMerge_MRI_FS5.3_under_90.csv` · `ANMerge_MRI_FS6.0_under_90.csv` |
| `Data/Raw Data/MRI/` | `MRI_AddNeuroMedFS-5.3-6.0.xlsx` |

`FS` = **FreeSurfer**. Yani bunlar bölgesel hacim ve kortikal kalınlık **ölçümleri**; hiçbir yerde NIfTI,
DICOM ya da Analyze hacmi yok. Erişim ayrıca Synapse hesabı istiyor (dosya indirme 403 döndü).

**Sonuç: bizim altı 3B modelimiz için kullanılamaz.** Hepsi 3B konvolüsyon ile ham hacim işliyor;
FreeSurfer tablosu bu ağlara girmez.

**Ama boşa da değil — iki yerde işe yarar:**
1. **Öznitelik tabanlı temel çizgi.** PROTOKOL madde 9 voksel SVM'i zaten istiyor; ROI hacimleriyle
   (hipokampüs, entorinal korteks) çalışan klasik bir sınıflandırıcı, 3B CNN'lerin gerçekten değer katıp
   katmadığını sınamak için güçlü bir karşılaştırma noktası. Wen 2020'nin hipokampüs-ROI referansı **0,89**
   tam olarak bu aileden.
2. **Literatür/tartışma bölümü.** 1702 denekle bile MRI'ın tablo hâlinde paylaşılması, ham görüntü
   paylaşımının neden nadir olduğunu gösteren somut bir örnek.

**Not:** bu bulgu bir desen gösteriyor — büyük AD kohortları ham görüntüyü değil **türetilmiş ölçümü**
paylaşıyor (ANMerge, ayrıca EPAD'ın bulut çalışma alanı). Ham 3B hacme erişimin yolu neredeyse her zaman
başvuru + DUA: ADNI, OASIS, AIBL. `ARAMA-PROMPTU.md`'ye bu şart (3B hacim zorunlu) zaten yazılı.

## 2g. ⭐ `radiata-ai/brain-structure` (HuggingFace) — ARADIĞIMIZ VERİ (25.10.2026)

Ekipten önerildi, incelendi ve **şimdiye kadarki en iyi aday**. İlk kez ciddi bir AD grubu var.

**Nedir:** Radiata'nın beş açık çalışmayı (DLBS, IXI, NKI-RS, **OASIS-1**, **OASIS-2**) tek bir hatta
işleyip birleştirdiği koleksiyon. **3794 tarama, 2607 denek.** Hepsi 3B NIfTI T1w MPRAGE,
**kafatası ayıklanmış ve MNI152'ye afin hizalanmış**, 113×137×113 @ 1,5 mm.

### Tanı × çalışma (tarama sayısı)
| Çalışma | AD | Sağlıklı |
|---|---|---|
| DLBS | 0 | 315 |
| IXI | 0 | 409 |
| NKI-RS | 0 | 2283 |
| **OASIS-1** | **100** | 314 |
| **OASIS-2** | **165** | 208 |

### ⚠ Sınıf–kohort karışması ve çözümü
AD **yalnız OASIS'ten** geliyor; IXI/DLBS/NKI-RS tamamen sağlıklı. Tüm koleksiyonu olduğu gibi
kullanırsak model hastalığı değil **tarayıcıyı** öğrenir (`§2d`'deki tuzağın ta kendisi).

**Çözüm: yalnız OASIS-1 + OASIS-2 alt kümesiyle çalışmak.** Orada her iki sınıf da aynı kohortlarda var:

```
787 tarama · 564 denek
denek düzeyinde:  165 Alzheimer  ·  399 sağlıklı
```

### Dikkat edilecek üç şey
1. **Yaş uçurumu.** AD 76,0 ± 7,0 (61–96) · sağlıklı 51,8 ± 24,9 (**18**–94). OASIS-1 genç yetişkin de
   içeriyor. Kontroller ≥60 yaşa süzülüp `eslestir.py` ile yaş/cinsiyet eşleştirilmeli; yoksa model
   yaşı öğrenir.
2. **Boylamsal.** 94 denekte 2, 43 denekte 3, 13 denekte 4–5 tarama var. Denek başına tek tarama alınmalı
   ya da bölme denek düzeyinde yapılmalı (PROTOKOL madde 1 — `bolme.py` zaten öyle yapıyor).
3. **Depodaki hazır train/val/test bölmesi KULLANILMAYACAK.** Tarama düzeyinde görünüyor; aynı deneğin
   iki taraması farklı kümelere düşebilir. Kendi `bolme.py`'mizle denek düzeyinde böleceğiz.

### Ön işleme: bizim hattımızı atlıyor
Taramalar zaten kafatası ayıklanmış ve MNI'ye hizalanmış. Bu **sorun değil, avantaj**: beş çalışma tek bir
hatla uyumlulaştırılmış, yani PROTOKOL madde 3'ün istediği "herkes aynı ön işleme" sağlanıyor — yeter ki
tüm veri buradan gelsin. Bizim `onisle.py` zincirimiz bu veri için **atlanır**; yalnız 128³'e yeniden
boyutlandırma ve z-score uygulanır.

### Lisans — bilinçli karar gerektirir
Koleksiyonun kendisi **ODC-By v1.0**, ama kart açıkça şunu diyor: *"Individual scans are licensed under
study-specific data use agreements"* ve OASIS-1/OASIS-2 için **Custom DUA** gösteriyor. Yani AD taramaları
OASIS verisidir ve OASIS'in kendi şartlarına tabidir.

**Ekibin durumu:** OASIS başvurusu **yapıldı** (bkz. `SUREC.md §9` satır 7). Onay geldiğinde bu veriyi
kullanma hakkı zaten doğmuş olacak; bu koleksiyon o süreçte **erken başlamayı** sağlıyor.
Raporun yöntem bölümünde kaynak açıkça yazılmalı: *"OASIS-1/OASIS-2 taramaları, Radiata'nın
uyumlulaştırılmış dağıtımı üzerinden; OASIS veri kullanım başvurusu <tarih>'te yapıldı."*
Gizlenecek bir şey yok, yazıldığı sürece savunulabilir.

### Tam kohort tablosu (denek düzeyinde, ölçüldü)
| Çalışma | Denek | AD | CN | Yaş ort | Yaş aralığı | Tarayıcı |
|---|---|---|---|---|---|---|
| DLBS | 315 | 0 | 315 | 54,1 | 20–89 | Philips Achieva **3T** |
| IXI | 409 | 0 | 409 | 50,1 | 19–86 | GE/Philips **1,5T ve 3T karışık** |
| NKI-RS | 1319 | 0 | 1319 | 38,7 | 6–85 | Siemens TrioTim **3T** |
| **OASIS-1** | 414 | **100** | 314 | 52,9 | 18–96 | **Siemens Vision 1,5T** |
| **OASIS-2** | 150 | **65** | 85 | 75,4 | 60–96 | **Siemens Vision 1,5T** |

**Kritik avantaj:** OASIS-1 ve OASIS-2 **aynı tarayıcıyı** kullanıyor (Siemens Vision, 1,5T). Yani ikisini
birleştirmek tarayıcı karıştırıcısı yaratmıyor. Diğer üç kohort farklı cihaz ve alan gücünde — onları AD
görevine karıştırmak sınıf–tarayıcı karışması demek olurdu.

### Tek süzgeç her şeyi çözüyor: yaş ≥ 60
| Süzgeç | Denek | AD | CN | Oran |
|---|---|---|---|---|
| ham | 564 | 165 | 399 | 2,42:1 |
| yaş ≥ 55 | 364 | 165 | 199 | 1,21:1 |
| **yaş ≥ 60** | **348** | **165** | **183** | **1,11:1** |
| yaş ≥ 65 | 324 | 158 | 166 | 1,05:1 |

**Yaş ≥ 60 seçilince:**
```
AD  165 denek · yaş 76,0 ± 7,0
CN  183 denek · yaş 75,9 ± 8,6
yaş farkı p = 0,8352  →  ZATEN DENGELİ, eşleştirmeye gerek yok
kohort: OASIS-1 100 AD / 98 CN · OASIS-2 65 AD / 85 CN  →  her iki sınıf her iki kohortta
```
ds007857'de yaş karıştırıcısı vardı ve `eslestir.py` ile düzeltmek gerekmişti; burada **yaş süzgeci
yeterli**. Geriye tek dengesizlik **cinsiyet** kalıyor: AD %53 kadın, CN %72 kadın. İki seçenek —
(a) `eslestir.py --oran 1.0` ile cinsiyet de eşleştirilir (yaklaşık 140 AD + 140 CN kalır),
(b) 348 denek korunur ve cinsiyet raporda ortak değişken olarak belirtilir. Literatürde ikisi de kabul görüyor.

### Uzun vade: üç ayrı kullanım
Bu koleksiyon tek bir iş için değil, **üç ayrı iş** için değerli:

**1. Ana görev — AD vs NC.** OASIS alt kümesi, yaş ≥ 60: 165 AD + 183 CN. ADNI gelene kadar asıl görevde
çalışmayı sağlar; ADNI gelince bu küme **dış test** setine dönüşür (PROTOKOL "Dış test" bölümü).

**2. Ön eğitim havuzu — 3007 tarama / 2043 sağlıklı denek** (DLBS + IXI + NKI-RS, yaş 6–89).
AD etiketi yok ama **etiket gerekmiyor**: bu tam olarak **P15 (Dhinagar 2023, Ertuğrul'un makalesi)**
konusu — 3B mimarileri ön eğitip küçük hedef sete aktarmak. Ayrıca beyin-yaşı tahminiyle ön eğitim
(sağlıklı beyinden yaş kestir → AD'ye aktar) literatürde güçlü bir strateji. Bu havuz, P02'nin MedicalNet
transferine **kendi verimizle yapılmış bir alternatif** sunar ve ablation'a girer:
*sıfırdan vs MedicalNet vs kendi havuzumuzda ön eğitilmiş.*

**3. Çoklu-merkez genelleme.** Beş kohort, dört farklı tarayıcı, 1,5T ve 3T. Merkez etkisinin sonucu ne kadar
bozduğunu ölçmek için hazır bir düzenek — Wen 2020 ve Bron 2021'in genelleme tartışmasının tam konusu.

### Radiata'nın ön işleme hattı — rapor yöntem bölümü için
Veri kartındaki *Methods* bölümünden birebir (yöntem bölümüne bu yazılacak, "bir şekilde işlenmiş" denmez):

1. **Bias, gürültü ve yoğunluk düzeltmesi** — CAT12 (Gaser vd. 2024)
2. **Beyin maskesi** — CAT12, gri madde + ak madde + BOS
3. **Afin hizalama** — FSL FLIRT, 12 serbestlik derecesi,
   hedef **`MNI152NLin2009cAsym` 1,5 mm**, `-noresampblur`
4. Amaç: gürültüsü azaltılmış, **yumuşatılmamış**, standart uzaya hizalı ama bireysel anatomiyi koruyan hacim

#### Bizim hattımızla karşılaştırma
| Adım | `onisleme/onisle.py` | Radiata |
|---|---|---|
| Bias düzeltme | N4 (SimpleITK) | CAT12 |
| Kafatası ayıklama | HD-BET | CAT12 (GM+WM+BOS) |
| Hizalama | SimpleITK afin, Mattes MI, 3 seviye | FSL FLIRT, 12 DOF |
| **Hedef şablon** | **MNI152NLin2009cAsym** | **MNI152NLin2009cAsym** |
| Çözünürlük | şablon ızgarası | 1,5 mm |

**Şablon aynı.** Bu beklenmedik bir şans: iki hat farklı araçlar kullanıyor ama **aynı standart uzayı**
hedefliyor, dolayısıyla çıktılar anatomik olarak hizalı. Fark bias düzeltme ve maske yönteminde kalıyor.

#### ⚠ ADNI geldiğinde ne yapılacak
ADNI bizim hattımızdan (HD-BET + N4 + SimpleITK) geçecek, OASIS ise Radiata'nın hattından geçmiş olacak.
İkisini aynı tabloda karşılaştırmak **hat farkını kohort farkıyla karıştırır**. İki seçenek:

- **(a) Tercih edilen:** OASIS erişimi onaylandığında **ham OASIS indirilip bizim hattımızdan geçirilir.**
  Böylece her şey tek hatla üretilir ve PROTOKOL madde 3 tam anlamıyla sağlanır. Radiata sürümü o ana
  kadar **erken başlama** aracıdır.
- **(b)** Radiata sürümü korunursa, ADNI–OASIS karşılaştırmasında hat farkı raporda açıkça belirtilir ve
  dış test sonucu bu uyarıyla sunulur.

Bu karar `SUREC.md §7`'de danışmana sorulacaklar arasına eklenmeli.

#### Veri kartından iki ek bilgi
- **Bölme denek düzeyinde:** *"Subjects with multiple scans only appear in one split."* Yani depodaki
  80/10/10 bölmesi sızıntılı değil. Yine de **kendi bölmemizi üreteceğiz**, çünkü PROTOKOL 5 kat CV istiyor.
- **IQR yönü belli:** *"image quality rating (IQR; larger value = worse quality)"* — **büyük değer kötü.**
  Kalite süzgeci istenirse `metadata.csv`'deki `image_quality_rating` ile uygulanabilir.

### İndirme planı
| Ne | Tarama | Boyut | Ne zaman |
|---|---|---|---|
| OASIS-1 + OASIS-2 (tümü, boylamsal dahil) | 787 | ~1,6 GB | **şimdi** — ana görev |
| Sağlıklı ön eğitim havuzu | 3007 | ~6,3 GB | P15 implementasyonuna gelince |

Boylamsal taramalar da iniyor çünkü ileride aynı deneğin zaman içindeki değişimi (atrofi hızı) ayrı bir
analiz olabilir; denek düzeyinde bölme bunu zaten güvenli kılıyor.

## 3. Etiket kuralları
### 3.1 ADNI1 (ADNIMERGE.csv, `VISCODE == "bl"`)
| `DX_bl` | Bizim sınıf | Not |
|---|---|---|
| `CN` | **NC** (0) | |
| `LMCI` (ADNI1'de MCI tek grup) | **MCI** (1) | ADNI-GO/2'deki `EMCI`, `SMC` ADNI1'de yok; gelirse `EMCI→MCI`, `SMC` dışarıda bırakılır |
| `AD` | **AD** (2) | |
- Denek anahtarı: `RID` (`PTID` ile eşleşir). Aynı RID'nin yalnızca **bir** başlangıç taraması alınır (çoklu seri varsa `Image ID` en küçük / kalite notu iyi olan).
- İkincil görev için (isteğe bağlı): `DX` sütunundaki 24–36 aylık dönüşümle `sMCI` / `pMCI` etiketi.

### 3.2 OASIS-1 (`oasis_cross-sectional.csv`)
| `CDR` | Bizim sınıf | Not |
|---|---|---|
| 0 | **NC** | yalnızca ≥60 yaş alınır (gençlerde demans yok, yaş karıştırıcı) |
| 0.5 | **demans spektrumu (çok hafif)** | literatürde kimi çalışma MCI benzeri, kimi AD sayar; **ikili görevde AD tarafına** konur, üç sınıf OASIS-1'de **yapılmaz** |
| 1, 2 | **AD** | |
- Denek anahtarı `ID` (`OAS1_0001`). Her denekte 3–4 T1 tekrarı var → **yalnız ilk (`mpr-1`)** veya ortalaması (`_t88_` dosyaları zaten ortalama + Talairach hizalı); tekrarlar **asla** ayrı örnek sayılmaz (sızıntı).
- Yaş ve cinsiyet dağılımı kat başına raporlanır (NFR-3).

## 4. Bölme kuralı (PROTOKOL madde 1–2 ile aynı)
- **Birim = denek (RID / OASIS ID)**; bir deneğin hiçbir taraması/tekrarı farklı katlara düşmez.
- `sklearn.model_selection.StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=2026)`; `groups = RID`, `y = sınıf`.
- Önce **%15 kilitli test** (denek düzeyi, sınıf dengeli, tohum 2026) ayrılır; kalan %85 üzerinde 5-kat CV. Test seti **hiperparametre seçiminde kullanılmaz**, yalnızca son raporda bir kez açılır.
- Bölme dosyaları `veri/bolme/<set>_test.csv`, `veri/bolme/<set>_kat{0..4}.csv` (sütunlar: `denek_id, dosya, sinif, yas, cinsiyet`) → Git'e girer (denek ID anonim olduğu için DUA'ya uygun; yine de ADNI'ye sorulur). Üretici: `uygulama/ortak/bolme.py`.
- Dış test (varsa): ADNI1 ile eğitilen model OASIS-1'de (ikili) sınanır ve ayrı sütunda raporlanır.

## 5. Klasör düzeni (kendi PC'nde, repo dışı)
```
D:\veri\
  oasis1\ham\OAS1_0001_MR1\...           (indirildiği gibi)
  oasis1\islenmis\OAS1_0001.npy + .json  (onisle.py çıktısı, 128³ float16)
  adni1\ham\ADNI\<PTID>\...\*.nii
  adni1\ADNIMERGE.csv
  adni1\islenmis\<RID>.npy + .json
```
Repo içinde yalnızca `veri/bolme/*.csv` ve `veri/ornek/` (sentetik 1 hacim) bulunur.

## 6. Boyut ve süre tahminleri (tahmin, ölçülünce güncelle)
| | OASIS-1 (≥60 yaş, ~200 denek) | ADNI1 baseline (~800 denek) |
|---|---|---|
| Ham indirme | ~1.5 GB (12 arşiv) | ~15–25 GB NIfTI |
| Ön işleme CPU (HD-BET ~2 dk + N4 ~1 dk + kayıt ~1 dk) | ~3–4 saat | ~2 gün (bir PC) veya 3 PC'ye bölünür |
| İşlenmiş 128³ float16 | ~0.8 GB | ~3.4 GB |

## 7. Kaynaklar
- ADNI erişim: https://adni.loni.usc.edu/data-samples/adni-data/#access_data · DUA: https://adni-lde.loni.usc.edu/wp-content/uploads/how_to_apply/ADNI_Data_Use_Agreement.pdf
- ADNIMERGE: https://adni.loni.usc.edu/?p=4174 · MRI koleksiyonları: https://adni.loni.usc.edu/data-samples/adni-data/neuroimaging/mri/mri-image-data-sets
- OASIS-1: https://sites.wustl.edu/oasisbrains/home/oasis-1/ · NITRC: https://www.nitrc.org/projects/oasis/
- Kaggle 4-sınıf setinin sızıntı/kaynak sorunu: https://www.mdpi.com/2504-4990/8/11/344 · https://arxiv.org/pdf/2412.05666
- Wen 2020 sızıntı türleri: https://arxiv.org/abs/1904.07773 · Yagis 2021: https://www.nature.com/articles/s41598-021-01681-w
