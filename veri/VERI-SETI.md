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
