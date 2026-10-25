# P07 — Zhang 2021: 3D ResAttNet (artık öz-dikkat) + Grad-CAM (Görkem)

- **Makale:** https://arxiv.org/abs/2008.04024 (IEEE JBHI)
- **Resmî kod:** bulunamadı → açık parçalardan kurulur: MONAI `resnet18/34(spatial_dims=3)` (Apache-2.0) + öz-dikkat bloğu (makale §III'teki non-local/self-attention tanımı, kendi kodumuz) + `monai.visualize.GradCAM`.
- **Grad-CAM 3B:** MONAI GradCAM 5B girdiyi destekler (`b, c, *spatial`); hedef katman örn. `layer4`. Çıktıyı 128³'e yeniden örnekleyip MRI üstüne bindir.

## Yapılacaklar
1. `model.py`: `olustur(varyant='resatt18', sinif_sayisi, girdi_boyut)` → MONAI ResNet gövdesi; `layer3`/`layer4` sonrasına öz-dikkat modülü (makaledeki konuma göre).
2. `gradcam.py`: checkpoint + hacim → ısı haritası `.npy` + PNG.
3. Eğitim: `python uygulama\ortak\egit.py --model gorkem_P07_resattnet --varyant resatt18 --set oasis1 --gorev ikili --kat 0 --tohum 2026 --veri <islenmis>`
4. Ablation: öz-dikkat **var/yok** (aynı ResNet) → dikkatin katkısı; P07 notu §12. Ablasyon **ek satırdır**, ana karşılaştırma tablosuna girmez ve PROTOKOL madde 7'deki "fazladan tarama yok" kuralını bozmaz (ana tabloya yalnız "öz-dikkat var" girer).
