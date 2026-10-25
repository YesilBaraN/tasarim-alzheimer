# KURULUM — Kendi bilgisayarında ortam (Windows)

Bu klasör taşınabilir bir pakettir: olduğu gibi kendi PC'ne kopyala (veya zip'le). Hiçbir şey sunucuda kurulmadı; aşağıdaki her komut **senin PC'nde** koşar.

## 0. Donanım yolu seç
| Durum | Ne yaparsın |
|---|---|
| **NVIDIA GPU var** (≥6 GB VRAM) | Yol A: CUDA'lı torch; 96³–128³ hacimle eğitim yerelde |
| **GPU yok** | Yol B: CPU torch yalnızca kod testi + ön işleme; eğitim **Kaggle** (haftalık ~30 GPU-saat, P100/T4) veya **Colab** (T4) |
| Bilmiyorsan | `dxdiag` → Display sekmesi; veya PowerShell: `Get-CimInstance Win32_VideoController | Select Name` |

## 0b. Baran'ın PC'si: NVIDIA GeForce RTX 3050 Laptop GPU (+ Intel UHD) — 25.10.2026
`nvidia-smi` ile VRAM'i teyit et (dizüstü 3050 çoğunlukla **4 GB**, bazı 2024 modelleri 6 GB). Sürücü sütununda CUDA 12.x görünmeli; eski sürücüde https://www.nvidia.com/drivers üzerinden güncelle.

| Ne | 4 GB VRAM'de | Not |
|---|---|---|
| Duman testleri (`test_model.py`, `test_onisle.py`) | ✅ | CPU'da da koşar |
| HD-BET kafatası ayıklama | ✅ `--cihaz 0` (GPU, ~10 sn/hacim) | VRAM yetmezse `--cihaz cpu --disable_tta` |
| N4 + MNI kayıt | CPU işi | GPU'dan bağımsız |
| VoxCNN / VoxResNet (P01) eğitimi | ✅ 96³, batch 2, AMP; 128³ batch 1 sınırda | `--boyut 96 --batch 2 --accum 2`; **VoxCNN'in valid konvolüsyonu ≥100³ ister** — 96³'te model otomatik padding=1'e düşer (makaleden sapma, uyarı basar). VoxResNet her boyutta sorunsuz |
| ResNet-18 MedicalNet (P02) | ⚠ 96³ batch 1–2 AMP; 128³ **sığmaz** (tahmini 8–12 GB) | geliştirme/ablation için 96³ |
| DenseNet121, ResAttNet, FCN-yama | ❌ 128³'te sığmaz | Kaggle/Colab |
| **Tam protokol (6 model × 5 kat × 3 tohum, 128³)** | ❌ | **Kaggle P100 16 GB / T4** — §6 |

Kural: PROTOKOL madde 3 gereği **tabloya giren** sonuçlar herkeste aynı boyutla (128³) ve aynı donanım sınıfında (Kaggle/Colab 16 GB) üretilir; RTX 3050 yalnız kod geliştirme, hata ayıklama ve hızlı ön deney içindir. Yerel koşularda `karsilastirma/kosu_kayitlari` JSON'unda `gpu` alanı "RTX 3050" görünen satırlar SONUCLAR tablosuna girmez.

Kurulum (Yol A, CUDA tekerleği — **cu124 DEĞİL**, aşağıdaki §2 tuzağını oku):
```powershell
nvidia-smi
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0), round(torch.cuda.get_device_properties(0).total_memory/2**30,1), 'GB')"
```
VRAM sığmazsa sırayla: AMP açık mı (`--amp 1`, varsayılan) → `--batch 1 --accum 4` → `--boyut 96` (VoxCNN'de padding'i değiştirir, yukarıdaki tablo satırına bak) → Kaggle. `torch.cuda.OutOfMemoryError` çıkarsa ilk olarak `nvidia-smi`'de başka işlem (tarayıcı, oyun) VRAM yemiyor mu diye bak.

## 1. Python ve sanal ortam
Python **3.11 veya 3.12** kur (https://www.python.org/downloads/ — "Add to PATH" işaretle). 3.14 henüz tüm tıbbi görüntü paketlerinde (antspyx, hd-bet bağımlılıkları) tekerlek garantisi vermiyor. **3.12.10 ile doğrulandı.** Python Install Manager varsa tek komut yeter: `py install 3.12` (yan yana kurar, `py uninstall 3.12` ile geri alınır).

```powershell
cd <bu klasörün yolu>
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

## 2. Paketler
> ### ⚠ Tuzak (25.10.2026'da yaşandı ve ölçüldü)
> `requirements.txt` içindeki **`monai>=1.4`** (güncel sürüm 1.6.1) **`torch>=2.8.0`** istiyor. PyTorch'un
> **cu124** kanalı ise **torch 2.6.0'da bitiyor**. Bu yüzden eski talimat (`cu124` ile torch, sonra
> `requirements.txt`) pip'in torch'u **PyPI'den CPU sürümüyle değiştirmesine** yol açıyor: kurulum sessizce
> başarılı görünür, `torch.cuda.is_available()` ise `False` döner ve GPU hiç kullanılmaz.
> Ölçülen kanal içerikleri: `cu124` → en fazla 2.6.0 · `cu128` → en fazla 2.11.0 · **`cu126` → 2.14.1** · `cu130` → 2.14.1.
> `cu126` seçildi: hem güncel torch'u var hem CUDA 12.x sürücüsüyle çalışır (`cu130` çok yeni sürücü ister).

**Yol A (CUDA):**
```powershell
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
pip install -r onisleme\requirements.txt
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```
Son satır **`+cpu` ya da `False`** gösteriyorsa `requirements.txt` torch'u ezmiş demektir; CUDA tekerleğini geri koy:
```powershell
pip install --force-reinstall torch torchvision --index-url https://download.pytorch.org/whl/cu126
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```
Bu kontrolü **her** `pip install` turundan sonra tekrarla: torch isteyen herhangi bir paket aynı şeyi yapabilir.
**Yol B (CPU — kod geliştirme, duman/sağlık testleri, ön işleme):**
```powershell
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r onisleme\requirements.txt
```
Bu yol 25.10.2026'da Python 3.12.10 + torch 2.14.1 + monai 1.6.1 ile **doğrulandı**: `test_model.py`, `test_onisle.py`, `saglik_testi.py`, ONNX dışa aktarma ve `api/tahmin.py` hepsi yeşil.
`onisleme\requirements.txt` içindekiler: monai, nibabel, SimpleITK, hd-bet, templateflow, dcm2niix, scikit-learn, pandas, numpy, scipy, matplotlib, tqdm, onnx, onnxruntime, pyyaml. Hepsi ücretsiz ve pip ile kurulur.

CUDA doğrulama:
```powershell
python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

## 2b. Git deposu (PROTOKOL madde 10 — ilk koşudan ÖNCE)
Tabloya giren her sonuç satırının yanında commit hash'i olmalı; `egit.py` bunu `git rev-parse` ile okur, depo yoksa koşu kaydına `"git-yok"` yazar. Bu yüzden bir kez:
```powershell
git init
git add .
git commit -m "Tasarim projesi iskeleti: protokol, on isleme, ortak egitim kodu"
```
`.gitignore` veriyi, ağırlıkları ve `.npy` / `.pth` / `.onnx` dosyalarını zaten dışlıyor.

## 3. İlk 10 dakikada koş (sırayla)
```powershell
python uygulama\test_model.py
```
→ 32³ rastgele hacimle `uygulama/*/model.py` içinde **mevcut** modellerin (şimdilik P01 ×2, P02, temel çizgi, MONAI DenseNet121; P06/P07/P11 `model.py` yazılınca otomatik eklenir) ileri/geri geçişini dener; her satırda `OK` görmelisin. VoxCNN için "UYARI … padding=1" satırı normaldir (32³ duman testi küçük); tabloya giren 128³ valid kurulum ayrıca denenir.
```powershell
python onisleme\test_onisle.py
```
→ sentetik bir NIfTI üretir, N4 + normalizasyon + yeniden boyutlandırma adımlarını koşar (HD-BET ve MNI kaydı sentetikte atlanır); `OK` görmelisin.
```powershell
python uygulama\ortak\saglik_testi.py
```
→ PROTOKOL K5 sağlık testleri: sentetik hacimlerle **eğitim hattının tamamını** koşar (bölme → veri → eğitim → metrik → JSON). Ayrılabilir iki sınıfta BAcc ≈ 1.0, rastgele etikette ≈ 0.5 beklenir; sonda "TÜM SAĞLIK TESTLERİ OK". CPU'da ~1–3 dk, veri/GPU/internet gerekmez. Gerçek koşu turlarından önce bunu yeşile al.

## 4. Ağırlık ve şablon indirmeleri (ilk gerçek koşudan önce)
| Ne | Nereden | Lisans | Nereye |
|---|---|---|---|
| MedicalNet `resnet_18_23dataset.pth` | https://github.com/Tencent/MedicalNet (README'deki Google Drive / Tencent Weiyun linki) veya https://huggingface.co/TencentMedicalNet/MedicalNet-Resnet18 | MIT | `uygulama\baran_P02_medicalnet\agirliklar\` |
| MNI152NLin2009cAsym şablonu | TemplateFlow — `onisle.py` ilk koşuda otomatik indirir (`~/.cache/templateflow`) | atıf şartı | otomatik |
| HD-BET model ağırlıkları | ilk `hd-bet` çağrısında otomatik indirilir | Apache-2.0 | otomatik |

## 5. Veri (hiçbiri bu klasöre konmaz, Git'e girmez)
- **OASIS-1** (köprü set): https://sites.wustl.edu/oasisbrains/home/oasis-1/ → "Request Access" → indirilen diskleri `D:\veri\oasis1\` gibi klasör dışı bir yere aç. `veri/VERI-SETI.md` §3'teki etiket kuralına bak.
- **ADNI** (ortak set): onay gelince https://ida.loni.usc.edu → ADNI1 1.5T baseline T1 koleksiyonu + `ADNIMERGE.csv`. `veri/VERI-SETI.md` §2.
- `.gitignore` zaten `veri/ham/`, `veri/islenmis/`, `*.nii*`, `*.pth`, `*.onnx` dışlar.

## 6. Kaggle / Colab yolu (GPU yoksa)
1. Bu klasörü zip'le (veri hariç) → Kaggle "Datasets → New Dataset" olarak yükle (özel/private).
2. Yeni Notebook → Settings → Accelerator: **GPU P100** (veya T4 x2) → Add Data ile zip'i ekle.
3. İlk hücre:
   ```python
   !pip -q install monai nibabel SimpleITK onnx onnxruntime
   import sys; sys.path.append('/kaggle/input/<dataset-adı>/tasarim-alzheimer')
   ```
4. Ön işlenmiş tensörleri (`.npy`, 128³ float16) ayrı bir özel Kaggle dataset'i olarak yükle (ADNI DUA: yalnızca kendi hesabın, paylaşma).
5. Eğitim: `uygulama/ortak/egit.py` içindeki `egit()` fonksiyonunu çağır; her kat ~1–2 saat (ResNet-18, 128³, batch 4, AMP, T4).
Colab için aynı adımlar; Drive'ı bağlayıp (`drive.mount`) klasörü oraya koy. Ücretsiz Colab oturumu kesilebilir → `egit.py` **her epoch** `<ad>_son.pth` yazar (model + optimizer + scheduler + AMP scaler + sabır sayacı) ve en iyi doğrulamada `<ad>.pth`; aynı komutu tekrar koşmak kaldığı yerden devam eder, baştan eğitmek için `--sifirdan`.

## 7. Açık kaynak envanteri (rapor kaynakçası için)
| Bileşen | Depo | Lisans | Bizim kullanımımız |
|---|---|---|---|
| PyTorch | pytorch/pytorch | BSD-3 | tüm modeller |
| MONAI | Project-MONAI/MONAI | Apache-2.0 | `resnet18(spatial_dims=3)`, `DenseNet121`, `GradCAM`, dönüşümler |
| MedicalNet (Med3D) | Tencent/MedicalNet | MIT | ResNet-18 ön eğitimli ağırlık (P02) |
| Pytorch-LRP | moboehle/Pytorch-LRP | BSD-3 | LRP katmanları (P06) |
| brain2020 | vkola-lab/brain2020 | MIT | FCN yama modeli ve risk haritası (P11) |
| clinicadl | aramis-lab/clinicadl | MIT | protokol referansı, t1-linear tanımı (P03) |
| gfolego/alzheimers | gfolego/alzheimers | Apache-2.0 | ANTs ön işleme referansı (P04) |
| HD-BET | MIC-DKFZ/HD-BET | Apache-2.0 | kafatası ayıklama |
| SimpleITK | SimpleITK/SimpleITK | Apache-2.0 | N4, afin kayıt |
| nibabel | nipy/nibabel | MIT | NIfTI okuma/yazma |
| TemplateFlow | templateflow/templateflow | Apache-2.0 (şablonlar kendi lisansı) | MNI152NLin2009cAsym |
| dcm2niix | rordenlab/dcm2niix | BSD | DICOM → NIfTI |
| scikit-learn | scikit-learn | BSD-3 | metrikler, StratifiedGroupKFold |
| ONNX / onnxruntime | onnx, microsoft/onnxruntime | Apache-2.0 / MIT | dışa aktarma ve çalıştırma |
**Okunan ama kopyalanmayan:** neuro-ml/resnet_cnn_mri_adni (lisans yok), KVishnuVardhanR/M3T (GPL-3.0), martindyrba/DeepLearningInteractiveVis (MIT ama TF 1.15 — eski).

## 8. Sık sorunlar
- `hd-bet` kurulumu torch ister → önce torch'u (Yol A/B) kur, sonra requirements.
- `antspyx` Windows tekerleği bulunamazsa: gerekmiyor; `onisle.py` varsayılan olarak SimpleITK afin kayıt kullanır (`--kayit sitk`).
- CPU'da HD-BET: `hd-bet -i x.nii.gz -o y.nii.gz -device cpu --disable_tta` (hacim başına ~2 dk, RAM ≥8 GB).
- `templateflow` indirmesi için internet gerekir; kurum ağında proxy varsa `HTTPS_PROXY` ayarla.
- ONNX export hatası (`torch.cat` dinamik eksen) → `onnx_disa_aktar.py` sabit 1×1×128³ ile export eder; `dynamic_axes` kullanma.
