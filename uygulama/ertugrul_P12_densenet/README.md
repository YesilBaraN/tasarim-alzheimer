# P12 — Solano-Rojas & Villalón-Fonseca 2021: Düşük maliyetli 3B DenseNet (Ertuğrul)

- **Makale:** Sensors 2021 (MDPI, açık erişim); 2020 LNCS sürümü https://pmc.ncbi.nlm.nih.gov/articles/PMC7313295/
- **Kod:** makale kod vermiyor → MONAI `DenseNet121(spatial_dims=3, in_channels=1, out_channels=k)` (Apache-2.0). `pretrained=True` 3B'de yok; sıfırdan.
- **Okurken teyit et:** veri seti (ADNI mi OASIS mi), sınıf tanımı ("5 sınıf" ADNI2'nin CN/SMC/EMCI/LMCI/AD'si olabilir), girdi boyutu, büyüme oranı (growth rate), blok yapısı — P12 notu §4 ve §6.

## Yapılacaklar
1. `model.py`: `olustur(varyant='densenet121'|'densenet169', sinif_sayisi, girdi_boyut)` → MONAI DenseNet; makaledeki "düşük maliyet" ayarı (daha küçük growth rate / blok) ikinci varyant olarak.
2. Eğitim: `python uygulama\ortak\egit.py --model ertugrul_P12_densenet --varyant densenet121 --set oasis1 --gorev ikili --kat 0 --tohum 2026 --veri <islenmis>`
3. VRAM: DenseNet121 128³'te batch 2 bile 16 GB'ı zorlayabilir → `--batch 2 --accum 2`; gerekirse `--boyut 96` (herkesle birlikte).
4. P12 notu §12: makalenin bölme yöntemi denek düzeyinde mi? Değilse sonuçları şişkin say.
