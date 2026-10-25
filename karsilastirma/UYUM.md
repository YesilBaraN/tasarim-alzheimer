# Model uyum analizi — oasis

Test kümesi: 53 denek (26 NC / 27 AD) · 4 koşu

⚠ **Analiz dışı 1 çökmüş koşu:** `P06_bohle:cnn` (tek sınıf tahmin ediyor)

Tek sınıf tahmin eden bir model üç ölçümü de bozar: kappa'sı tanımı gereği 0,000 çıkar, her karşı-sınıf deneğini yanlış bildiği için ayrışma sayısını yapay şişirir, olasılıkları bilgi taşımadığı için topluluğu sulandırır.

## (a) İkili uyum

Ham uyum yüzdesi yanıltıcı olabilir (iki model de çoğunluk sınıfını söylerse yüksek çıkar); **kappa** şansı düzeltir. Kappa 1 = birebir aynı kararlar, 0 = şans düzeyinde ilişki.

| Model A | Model B | Uyum | Kappa | Olasılık korelasyonu |
|---|---|---|---|---|
| P01_korolev:voxcnn | P02_medicalnet:resnet18+ön | 62% | +0.292 | +0.685 |
| P01_korolev:voxcnn | P02_medicalnet:resnet18[sifirdan-ablation] | 81% | +0.579 | +0.808 |
| P01_korolev:voxcnn | ortak:sigcnn | 66% | +0.300 | +0.598 |
| P02_medicalnet:resnet18+ön | P02_medicalnet:resnet18[sifirdan-ablation] | 66% | +0.363 | +0.622 |
| P02_medicalnet:resnet18+ön | ortak:sigcnn | 74% | +0.482 | +0.787 |
| P02_medicalnet:resnet18[sifirdan-ablation] | ortak:sigcnn | 77% | +0.533 | +0.696 |

**Ortalama uyum 71% · ortalama kappa +0.425**

## (b) İndirgenemez çekirdek

- **Hiçbir model doğru bilemedi: 6/53 denek (11%)**
- Her model doğru bildi: 19/53 (36%)
- Modellerin ayrıştığı: 28/53

Hiçbir modelin bilemediği deneklerin demografisi:

- sınıf: AD 2 · NC 4
- yaş: 80.7 (tüm test: 76.0)
- kadın oranı: 50% (tüm test: 72%)
- kohort: {'OASIS-1': np.int64(4), 'OASIS-2': np.int64(2)}

## (c) Topluluk tavanı

| | AUC |
|---|---|
| P01_korolev:voxcnn | 0.758 |
| P02_medicalnet:resnet18+ön | 0.758 |
| P02_medicalnet:resnet18[sifirdan-ablation] | 0.738 |
| ortak:sigcnn | 0.654 |
| **Topluluk (olasılık ortalaması)** | **0.762** |

Topluluk, en iyi tek modelden (P01_korolev:voxcnn, 0.758) **+0.004** farklı.

→ Topluluk kayda değer bir şey eklemiyor: modeller büyük ölçüde **aynı sinyali** görüyor.

**(b) ile (c) birlikte okunmalı ve ilginç olan şu:** modeller deneklerin yarısında ayrışıyor (28/53), ama ortalamaları hiçbir şey kazandırmıyor. Eğer bu ayrışma **tamamlayıcı** olsaydı (her model verinin farklı ama geçerli bir yönünü görseydi) ortalama kazandırırdı. Kazandırmadığına göre ayrışma **gürültü**: her model aynı karar yüzeyinden gürültülü bir çekiliş. 236 eğitim deneğiyle kayıp yüzeyi düz olduğu için her koşu farklı bir rastgele köşeye oturuyor.

---

⚠ **Kapsam:** bu analiz 4 koşu ve **tek kat** (kat 0) üzerinden, 53 deneklik test kümesinde yapıldı. Yukarıdaki yorum bir **ön işaret**, sonuç değil — mimari hakkında kesin bir şey söylemek için 5 kat bitmeli ve koşular birbirinden bağımsız mimarilerle çeşitlenmeli (şu an koşuların bir kısmı aynı mimarinin varyantı). Beş kat bitince bu betik yeniden koşturulmalı.
