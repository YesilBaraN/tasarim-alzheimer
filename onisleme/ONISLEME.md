# ÖN İŞLEME HATTI

Tek betik: `onisle.py`. Her hacim için aynı adımlar, aynı parametreler → altı model aynı girdiyi görür (PROTOKOL madde 4).

## Adımlar
| # | Adım | Araç (lisans) | Parametre | Çıktı |
|---|---|---|---|---|
| 0 | DICOM → NIfTI (gerekirse) | dcm2niix (BSD) | `-z y` | `.nii.gz` |
| 1 | Yeniden yönlendirme | SimpleITK (Apache) | RAS/LPS'e DICOMOrient | aynı |
| 2 | Kafatası ayıklama | **HD-BET** (Apache) | `-device cpu --disable_tta` (GPU varsa `-device 0`) | beyin + maske (maske = beyin > 0) |
| 3 | N4 bias düzeltme | SimpleITK `N4BiasFieldCorrectionImageFilter` | shrink 2, 4 seviye × 50 iterasyon, maske içinde | düzeltilmiş |
| 4 | Yoğunluk normalizasyonu | numpy | maske içi z-score; maske dışı 0; [-5, 5] kırpma | float32 |
| 5 | MNI152 hizalama | SimpleITK afin kayıt (Mattes MI, 3 seviye) → TemplateFlow `MNI152NLin2009cAsym` res-1 `desc-brain T1w` (isteğe bağlı ANTsPy `--kayit ants`) | lineer interpolasyon | şablon ızgarasında (193×229×193, 1 mm) |
| 6 | Kırpma + yeniden boyutlandırma | SimpleITK | şablon beyin sınır kutusuna kırp → `--boyut 128` küp | 128³ |
| 7 | Kayıt | numpy | float16 `.npy` + `.json` meta (kaynak, adımlar, süreler, maske hacmi, kayıt metriği) | dosya |

Çıktı boyutu **128³** (Wen 2020'nin 169×208×179 kırpması referans; 128³ T4 16 GB'de batch 4'e izin verir). Gerekirse `--boyut 96` ile daha küçük — ama P01 VoxCNN'in valid konvolüsyonu ≥100³ ister, 96³'te padding=1'e düşer (PROTOKOL madde 3: boyut değişirse herkes değişir, modelin de aynı kalması gerekir).

## Kalite kontrol (otomatik, `.json`'a yazılır)
- Maske hacmi 900–1900 cm³ aralığında değilse `uyari: maske_hacmi`.
- Kayıt sonrası Mattes MI metriği eşiğin altındaysa `uyari: kayit`.
- Hacimde NaN/inf yoksa, min/max/mean/std kaydedilir.
Uyarılı hacimler `karsilastirma/` tablosuna girmeden elle bakılır.

## Komutlar
```powershell
# tek dosya
python onisleme\onisle.py --girdi D:\veri\oasis1\ham\OAS1_0001_MR1\PROCESSED\MPRAGE\T88_111\OAS1_0001_MR1_mpr_n4_anon_111_t88_masked_gfc.img --cikti D:\veri\oasis1\islenmis --ad OAS1_0001
# klasördeki tüm .nii/.nii.gz (ad = dosya adı)
python onisleme\onisle.py --girdi D:\veri\adni1\ham --cikti D:\veri\adni1\islenmis --toplu
# GPU'da HD-BET
python onisleme\onisle.py ... --cihaz 0
# sentetik duman testi (veri gerekmez)
python onisleme\test_onisle.py
```
OASIS-1 `_t88_masked_gfc` dosyaları zaten kafatası ayıklanmış ve Talairach hizalı gelir; onlar için `--kafatasi yok` kullanılabilir, kayıt yine MNI'ye yapılır (Talairach ≠ MNI).

## Referanslar
- Wen 2020 t1-linear tanımı (N4 + ANTs afin + kırpma): https://clinicadl.readthedocs.io/en/v0.2.2/Preprocessing/T1_Linear/
- Folego 2020 ANTs zinciri: https://github.com/gfolego/alzheimers
- HD-BET: https://github.com/MIC-DKFZ/HD-BET · SimpleITK N4: https://simpleitk.readthedocs.io · TemplateFlow: https://www.templateflow.org
