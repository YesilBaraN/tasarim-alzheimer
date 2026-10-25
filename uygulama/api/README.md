# API — Karar destek prototipi (çıkarım katmanı)

> **Araştırma prototipidir, tanı aracı değildir.** Çıktı bir model skorudur; klinik karar için tek başına kullanılamaz. Bu uyarı kodda `tahmin.py::UYARI` olarak her çıktıya eklenir ve arayüzde de görünmek zorundadır.

Projenin nihai çıktısı: *en iyi model ONNX olarak paketlenip radyoloji yazılımına eklenebilir bir karar destek prototipine dönüştürülür* (README, proje tanımı). Bu klasör o zincirin çıkarım tarafı.

## Zincir

```
ham T1 (NIfTI / Analyze / DICOM)
   → onisleme/onisle.py          kafatası ayıklama → N4 → maske içi z-score → MNI152 afin → boyut³
   → uygulama/ortak/onnx_disa_aktar.py   eğitilmiş .pth → sabit şekilli .onnx (1×1×B³)
   → uygulama/api/tahmin.py      ONNX çıkarımı → sınıf + olasılıklar (+ ön işleme meta verisi)
```

**Eğitim/servis uyumu kuralı:** `tahmin.py` ön işlemeyi kendisi yazmaz, `onisle.py`'nin fonksiyonlarını çağırır ve boyutu ONNX girdi şeklinden okur. Servise ayrı bir ön işleme yazılırsa modelin gördüğü dağılım kayar ve skor anlamını yitirir.

## Kullanım

```powershell
# 1) eğitilmiş checkpoint'i ONNX'e aktar (sabit 128³, dinamik eksen yok)
python uygulama\ortak\onnx_disa_aktar.py --model baran_P02_medicalnet --varyant resnet18 ^
    --ckpt karsilastirma\kosu_kayitlari\<kosu-adi>.pth --cikti model.onnx --boyut 128

# 2) ham hacim → tahmin (ön işleme dahil; HD-BET ilk çağrıda ağırlık indirir)
python uygulama\api\tahmin.py --onnx model.onnx --girdi D:\hasta\T1.nii.gz

# 2b) zaten onisle.py'den geçmiş hacim
python uygulama\api\tahmin.py --onnx model.onnx --npy D:\veri\adni1\islenmis\RID123.npy

# 2c) hızlı duman denemesi (HD-BET ve MNI kaydı atlanır — SKOR GEÇERSİZ, yalnız boru hattı testi)
python uygulama\api\tahmin.py --onnx model.onnx --girdi T1.nii.gz --kafatasi yok --kayit yok --json
```

Python'dan:

```python
from uygulama.api.tahmin import KararDestek
kd = KararDestek("model.onnx", sinif_adlari=("NC", "AD"))
print(kd.tahmin_nii("T1.nii.gz")["olasiliklar"])
```

## Çıktı alanları

| Alan | Ne |
|---|---|
| `sinif`, `sinif_no`, `guven` | en yüksek olasılıklı sınıf ve olasılığı |
| `olasiliklar` | sınıf adı → softmax olasılığı |
| `logit` | ham çıktı (kalibrasyon çalışması için) |
| `boyut`, `model` | ONNX'ten okunan girdi kenarı ve dosya |
| `onisleme` | uygulanan adımlar, süreler ve **uyarılar** (maske hacmi, kayıt kalitesi) |
| `uyari` | araştırma prototipi uyarısı; ön işleme uyarısı varsa ona da eklenir |

`onisleme.uyarilar` boş değilse skor şüpheli kabul edilmeli: maske hacmi 900–1900 cm³ dışındaysa kafatası ayıklama, Mattes MI sıfıra yakınsa MNI kaydı kötü gitmiş demektir.

## Yapılacaklar (Ara Rapor 3–4)

- [ ] Isı haritası: `monai.visualize.GradCAM` / `OcclusionSensitivity` çıktısını PNG + NIfTI olarak döndür (Görkem'in XAI işiyle birleşir).
- [ ] Basit web arayüzü (yükle → tahmin + ısı haritası). Danışmana sorulacak: bu yeterli mi, DICOM görüntüleyici entegrasyonu mu bekleniyor (SUREC §7 soru 5).
- [ ] Kalibrasyon: güven skoru gerçek olasılığı yansıtıyor mu (reliability diagram, Brier skoru).
- [ ] Toplu mod: klasördeki tüm hacimler → CSV.
- [ ] Reddetme eşiği: güven düşükse "karar verilemedi" döndür (klinik kullanımda yanlış kesinlikten iyidir).
