# P06 — Böhle 2019: 3B CNN + Layer-wise Relevance Propagation (Görkem)

- **Makale:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6685087/ (Front. Aging Neurosci. 2019)
- **Açık kod:** https://github.com/moboehle/Pytorch-LRP — **BSD-3**, PyTorch, ADNI eğitim ve LRP not defterleri içinde → doğrudan kullanılabilir.
- **Ne alınır:** Pytorch-LRP deposundaki LRP katman sarmalayıcıları (PyTorch; `innvestigate` DEĞİL, o Keras/TF kütüphanesidir) + makaledeki 3B CNN tanımı. Veri yükleme **alınmaz**; ortak `uygulama/ortak/veri.py` kullanılır.

## Yapılacaklar
1. Depoyu klonla (bu klasörün dışına), LICENSE dosyasını buraya kopyala (`LICENSE-Pytorch-LRP`).
2. `model.py` yaz: `olustur(varyant, sinif_sayisi, girdi_boyut, **kw)` → makaledeki 3B CNN (`nn.Module`). Sözleşme `uygulama/ortak/egit.py` başlığında.
3. `lrp.py`: eğitilmiş checkpoint + bir hacim → LRP ilgi haritası (`.npy`) + eksenel/koronal/sagittal PNG (matplotlib).
4. Eğitim: `python uygulama\ortak\egit.py --model gorkem_P06_bohle --varyant cnn --set oasis1 --gorev ikili --kat 0 --tohum 2026 --veri <islenmis>`
5. P06 inceleme notu §12'ye makale ayarları ile PROTOKOL farklarını yaz.
