# P02 — Med3D / MedicalNet: 3B ResNet-18 transfer öğrenme

- **Makale:** Chen, Ma, Zheng — Med3D: Transfer Learning for 3D Medical Image Analysis, arXiv:1904.00625 — https://arxiv.org/abs/1904.00625
- **Kod/ağırlık:** https://github.com/Tencent/MedicalNet — **MIT** (Tencent 2019; içinde Kensho Hara 3D-ResNets-PyTorch, MIT). Ağırlıklar: `resnet_18.pth` (makaledeki 8 kümeli 3DSeg-8) ve `resnet_18_23dataset.pth` (23 kümeli, 2019-07 güncellemesi); HF aynası https://huggingface.co/TencentMedicalNet/MedicalNet-Resnet18
- **Model:** MONAI `resnet18(spatial_dims=3, n_input_channels=1, feed_forward=False, shortcut_type='A', bias_downsample=True, conv1_t_size=7, conv1_t_stride=2, pretrained=True)` + bizim baş (Dropout 0.3 + Linear 512→C) → `model.py`. Opus hakem doğrulaması: `makaleler/baran/P02…md §13`.
- **Makale bulgusu:** ön eğitim ile akciğer Dice 87.26 (TFS 75.22, Kinetics 83.21), nodül doğruluğu 88.89 (TFS 80.80); yakınsama 2× (Kinetics'e göre) / 10× (sıfırdan) hızlı. **Uyarı:** derin ağlarda uyumsuz alan (Kinetics) transferi sıfırdan eğitimin altına düşebiliyor → **sıfırdan (TFS) temel çizgisi zorunlu**. Ön eğitim verisinde dejeneratif hastalık / tüm-beyin T1 yok → kazanç bize taşınmayabilir; çoğunlukla hızlı/kararlı yakınsama beklenir.

## Üç ağırlık seçeneği (`--agirlik`)
| `--agirlik` | Ne olur | Tablo sütunu |
|---|---|---|
| (yok) | sıfırdan (TFS) | ön eğitim: hayır |
| `monai` | MONAI HF Hub'dan `resnet_18_23dataset.pth` indirir (otomatik) | ön eğitim: evet (23 küme) |
| `<yol>\resnet_18.pth` | makaledeki 8 kümeli ağırlık elle yüklenir (`module.` ayıklanır, `conv_seg` atlanır) | ön eğitim: evet (8 küme) |
Ağırlık dosyasının adı ve SHA-256'sı koşu JSON'una yazılır (hakem notu 12.3/9). MedicalNet'in 23 kümesinde ADNI/OASIS olup olmadığı README'de yazmıyor → **PROTOKOL sızıntı listesi için "bilinmiyor"** olarak raporlanır; 8 kümeli sürümde (BraTS, Hippo, akciğer, karaciğer…) ADNI yok.

## Koşma
```powershell
# (i) sıfırdan, (ii) 23 kümeli, (iii) 8 kümeli — hepsi aynı bölme/tohum
python uygulama\ortak\egit.py --model baran_P02_medicalnet --varyant resnet18 --set oasis1 --gorev ikili --kat 0 --tohum 2026 --veri D:\veri\oasis1\islenmis
python uygulama\ortak\egit.py --model baran_P02_medicalnet --varyant resnet18 --agirlik monai --set oasis1 --gorev ikili --kat 0 --tohum 2026 --veri D:\veri\oasis1\islenmis --lr 1e-4
python uygulama\ortak\egit.py --model baran_P02_medicalnet --varyant resnet18 --agirlik uygulama\baran_P02_medicalnet\agirliklar\resnet_18.pth --set oasis1 --gorev ikili --kat 0 --tohum 2026 --veri D:\veri\oasis1\islenmis --lr 1e-4
```
Hızlı kontrol (ağırlık gerçekten oturdu mu):
```powershell
python -c "import sys; sys.path.insert(0,'.'); from uygulama.baran_P02_medicalnet.model import olustur; olustur('resnet18', 2, 128, agirlik='monai')"
```
Elle yüklemede "eksik 0" (bas.* hariç) görmelisin.

## Hakem notlarından uygulama kararları
- Omurga LR 1e-4, baş 1e-3 (makale ince ayar Adam 1e-3, TFS 1e-2); ilk 3–5 epoch yalnız baş + BN (`dondur=True`, sonra `coz()`), sonra tamamı.
- Artırma: küçük afin (±5°, ölçek 0.8–1.2 makaledeki aralık; MNI'ye kayıtlı veride daha dar tut), hafif yoğunluk kaydırma; ortak `veri.py` ile aynı.
- Ablation (b): MedicalNet `models/resnet.py` (MIT) dilation'lı gövde + GAP/FC — 128³'te VRAM ölç; MONAI stride'lı gövdeyle karşılaştır.
- ONNX: `python uygulama\ortak\onnx_disa_aktar.py --model baran_P02_medicalnet --varyant resnet18 --ckpt <pth>`.

## Yapılacaklar
- [ ] `calistir.py`: ısınma (dondur) → çöz iki aşamalı eğitim sarmalayıcısı.
- [ ] Ağırlık SHA-256 kaydı ve 8/23 küme içerik notu.
- [ ] (i)/(ii)/(iii) × 5 kat × 3 tohum; kazancı kat×tohum eşleştirilmiş farkla raporla.
