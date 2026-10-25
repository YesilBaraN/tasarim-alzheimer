# P01 — Korolev 2017: VoxCNN ve VoxResNet (sıfırdan, PyTorch)

- **Makale:** Residual and Plain Convolutional Neural Networks for 3D Brain MRI Classification, IEEE ISBI 2017, s. 835–838 — https://arxiv.org/abs/1701.06643
- **Orijinal kod:** https://github.com/neuro-ml/resnet_cnn_mri_adni — Theano/Lasagne, **LICENSE dosyası yok** → tek satır kopyalanmadı. Mimari ve hiperparametreler makale + depodaki iki not defteri **okunarak** çıkarıldı ve Opus hakem tarafından doğrulandı (`makaleler/baran/P01…md §13`).
- **Neden bu model:** Formdaki "3D-ResNet"in kökü; düz CNN ile artık ağ aynı kodla karşılaştırılır (ablation: artık bağlantı ne kazandırıyor?).
- **Makaledeki sonuç (dikkat):** 231 görüntü (AD 50 / LMCI 43 / EMCI 77 / NC 61), girdi 110³, AD-NC AUC .88±.08 (VoxCNN) / .87±.07 (ResNet), doğruluk .79 / .80; ara sınıflar şans düzeyine yakın. Model seçimi aynı CV katlarının doğrulama eğrilerinden yapılmış (iyimser). **Bizim ≥%85 hedefi için referans değil, alt sınır.**

## Doğrulanmış mimari ve eğitim ayarları
| | VoxCNN | VoxResNet |
|---|---|---|
| Yapı | 4 blok, filtre 8-16-32-64, 3³ **valid** konv, blok başına 2-2-3-3, MaxPool(2); Dense128 → BN → Dropout 0.7 → Dense64 → Softmax | kök 2×[Conv32 3³ + BN + ReLU] → Conv64 s2 → 2×VoxRes(64) → Conv64 s2 → 2×VoxRes(64) → Conv128 s2 → 2×VoxRes(128) → 7³ havuz → FC128 → Softmax; dropout yok |
| Optimizer | Adam | SGD Nesterov, momentum 0.9 |
| LR | **2.7e-5** (makale "27·10⁻⁶"; özetteki 2e-6 yanlıştı) | 1e-4 (makale) / **1e-3 (depo kodu)** — çelişki, ikisi de denenir |
| Batch / epoch | 5 / 150 | 3 / 70 |
| Yoğunluk | hacim / max (depo) | aynı |
| Bölme | StratifiedKFold 5×5, denek = görüntü (ilk tarama) | aynı |
Bizde girdi 128³ → `AdaptiveAvgPool3d` ile çıkış boyutu sabitlenir (VoxCNN 1³×64, ResNet 2³×128).

## Koşma
**Ana tablo (PROTOKOL: herkes AdamW, eşit bütçe):**
```powershell
python uygulama\ortak\egit.py --model baran_P01_korolev --varyant resnet --set oasis1 --gorev ikili --kat 0 --tohum 2026 --veri D:\veri\oasis1\islenmis
python uygulama\ortak\egit.py --model baran_P01_korolev --varyant voxcnn --set oasis1 --gorev ikili --kat 0 --tohum 2026 --veri D:\veri\oasis1\islenmis
python uygulama\ortak\egit.py --model baran_P01_korolev --varyant resnet --set adni1 --gorev ikili --tum_katlar --tohumlar 2026 2027 2028 --veri D:\veri\adni1\islenmis
python uygulama\ortak\egit.py --model baran_P01_korolev --varyant resnet --set adni1 --gorev uc    --tum_katlar --tohumlar 2026 2027 2028 --veri D:\veri\adni1\islenmis
```
**Makale-sadık sanity check (hakem notu 12.3/10; SONUCLAR'da ayrı "makale ayarı" satırı):** girdiyi 110³'e indir, makale optimizer/LR/batch/epoch ile tek kat koş, AUC ≈ .85+ bandı görülünce 128³ + PROTOKOL ayarlarına geç:
```powershell
python uygulama\ortak\egit.py --model baran_P01_korolev --varyant voxcnn --set adni1 --gorev ikili --kat 0 --tohum 2026 --veri D:\veri\adni1\islenmis --boyut 110 --lr 2.7e-5 --batch 5 --epoch 150
```
`egit.py` varsayılan olarak AdamW kullanır (PROTOKOL madde 7). Makaledeki optimizer'la birebir koşmak için `--optimizer` yeter — ayrı bir sarmalayıcı gerekmiyor; koşu adına optimizer eklendiği için PROTOKOL koşusunun kaydını ezmez:
```powershell
python uygulama\ortak\egit.py --model baran_P01_korolev --varyant voxcnn --set adni1 --gorev ikili --kat 0 --veri D:\veri\adni1\islenmis --boyut 110 --optimizer adam --lr 2.7e-5 --batch 5 --epoch 150 --etiket makale-ayari
python uygulama\ortak\egit.py --model baran_P01_korolev --varyant resnet --set adni1 --gorev ikili --kat 0 --veri D:\veri\adni1\islenmis --boyut 110 --optimizer sgd  --lr 1e-4   --batch 3 --epoch 70  --etiket makale-ayari
```
Hiperparametre değerleri `MAKALE_AYARI` sözlüğünde; `tablo_uret.py` AdamW dışı koşuları ayrı satır olarak işaretler.
128³'te VRAM yetmezse `--batch 2 --accum 2`; `--boyut 96` yalnız herkesle birlikte (PROTOKOL madde 3).

**VoxCNN boyut kısıtı:** valid (padding'siz) 3³ konvolüsyon zinciri 100³'ün altında negatif boyut üretir → `olustur` 100³ altında otomatik `padding=1`e düşer ve uyarı basar. Bu makaledeki mimari değildir: tabloya giren her VoxCNN koşusu **128³** (ya da makale-sadık **110³**) olmalı; 96³ ablation'ını VoxResNet ile yap.

## Yapılacaklar
- [x] ~~`calistir.py` sarmalayıcısı~~ → `egit.py --optimizer adamw|adam|sgd` ile çözüldü (25.10.2026); ayrı dosya gerekmedi.
- [ ] Oklüzyon haritası (makaleyle paralel): `monai.visualize.OcclusionSensitivity(mask_size=7)` + AD sınıfı ortalaması, hipokampüs/ventrikül atlas örtüşmesi.
- [ ] OASIS-1'de ilk koşu → `karsilastirma/SONUCLAR.md`; P01 notu §12'deki farkları raporla.
