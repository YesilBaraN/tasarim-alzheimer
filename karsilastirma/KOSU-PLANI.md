# KOŞU PLANI — GPU bütçesi ve öncelik katmanları

Son güncelleme: 25.10.2026 · Sahibi: Baran · Dayanak: `uygulama/PROTOKOL.md`, `KURULUM.md §6`

## 1. Neden bu dosya var

PROTOKOL'ü harfiyen uygulamak ücretsiz GPU bütçesine **sığmıyor**. Sayılar:

| | Hesap | Sonuç |
|---|---|---|
| Tabloda GPU ile eğitilen satır | 2 temel çizgi (SigCNN3D) + P01 ×2 + P02 ×2 + P06 + P07 + P11 + P12 | **9 model** (SVM ayrı, CPU) |
| Görev | ikili (AD-NC) + üç sınıf | **2** |
| Koşu / model / görev | 5 kat × 3 tohum (madde 5) | **15** |
| **Tam protokol** | 9 × 2 × 15 | **270 koşu** |
| Koşu süresi | KURULUM §6: ResNet-18, 128³, batch 4, AMP, T4 → 1–2 sa/kat | **270–540 GPU-saat** |
| + LR taraması (madde 7, 3 değer) | ×3 | **810–1620 GPU-saat** |
| **Eldeki bütçe** | Kaggle ücretsiz ~30 GPU-sa/hafta/hesap × 3 üye × 8 hafta (6–13. hafta) | **~720 GPU-saat tavan** |

Yani: tam protokol + LR taraması **imkânsız**; tarama olmadan tam protokol tavanın %40–75'ini yiyor ve hata ayıklama, çöken oturum, yeniden koşma için **hiç pay bırakmıyor**. Aşağıdaki indirgeme PROTOKOL'ün sızıntı ve adillik kurallarının **hiçbirinden** ödün vermez; yalnızca tekrar sayısını azaltır ve bunu raporda açıkça yazar.

## 2. İndirgenmiş plan (danışman onayına sunulacak)

| Değişiklik | PROTOKOL maddesi | Gerekçe | Maliyet |
|---|---|---|---|
| LR taraması yalnız **kat 0 / tohum 2026 / ikili**, epoch 30 + sabır 8 ile; seçilen LR model başına sabitlenir | madde 7 | LR sıralaması 30 epoch'ta belli olur; tarama her katta tekrarlanırsa bütçenin yarısı gider | 9 model × 3 LR ≈ **8–16 sa** |
| **Birincil görev (AD-NC) tam**: 5 kat × 3 tohum | madde 5 değişmez | Hedef metrik bu; ±ss burada gerçekten gerekli | 135 koşu ≈ **135–270 sa** |
| **Üç sınıf: 5 kat × 1 tohum (2026)** | madde 5'ten sapma | İkincil görev; sMRI ile üç sınıf zaten düşük, tohum tekrarının bilgi değeri az. Raporda "tek tohum" yazılır | 45 koşu ≈ **45–90 sa** |
| Dış test (OASIS-1 sıfır-atış) | değişmez | Yalnız çıkarım, eğitim yok | **dakikalar** |
| Voksel SVM | madde 9 | CPU; GPU bütçesinden yemez | **0 sa** |
| **Toplam** | | | **~190–380 GPU-saat** |

720 saatlik tavanın içinde, hata payıyla.

## 3. Öncelik katmanları — darlık olursa bu sırayla kes

Kural: **önce tablo tamamlansın, sonra derinleşsin.** Bir modeli 15 koşuyla bitirip diğerini boş bırakmak, hepsini 5 koşuyla bitirmekten kötüdür — karşılaştırma tablosu projenin ana çıktısı.

| Katman | İçerik | Koşu | Tahmini | Ne verir |
|---|---|---|---|---|
| **T0** | OASIS-1 köprü seti, ikili, kat 0, tek tohum, 9 model | 9 | 3–5 sa | Hat ayakta mı, hangi model çöküyor |
| **T0b** | LR taraması (kat 0 / tohum 2026, epoch 30) | 27 | 8–16 sa | Model başına LR sabitlenir |
| **T1** | ADNI1 ikili, **5 kat × 1 tohum**, 9 model | 45 | 45–90 sa | **Tam karşılaştırma tablosu + kat varyansı** |
| **T2** | ADNI1 ikili, tohum 2027 ve 2028 | 90 | 90–180 sa | ±ss gerçek, "fark var mı" sorusu yanıtlanır |
| **T3** | ADNI1 üç sınıf, 5 kat × 1 tohum | 45 | 45–90 sa | İkincil görev |
| **T4** | Ablation'lar (ön eğitim, artık bağlantı, dikkat, boyut) | ~20 | 20–40 sa | SONUCLAR §D |

**Ara Rapor 3 (11. hafta) için T1 bitmiş olmalı.** T2 bitmezse tablo "tek tohum, 5 kat" olarak raporlanır ve bu dürüstçe yazılır.

## 4. Kim neyi koşar (kendi Kaggle kotasından)

| Kişi | Modeller | Haftalık ~30 GPU-sa'de |
|---|---|---|
| Baran | temel SigCNN3D, SVM (CPU), P01 VoxCNN, P01 VoxResNet, P02 sıfırdan, P02 MedicalNet | ~15–25 koşu |
| Görkem | P06 CNN+LRP, P07 ResAttNet | ~15–25 koşu |
| Ertuğrul | P11 FCN yama, P12 DenseNet121 | ~15–25 koşu |

Herkes kendi koşularının JSON kayıtlarını `karsilastirma/kosu_kayitlari/` altına commit eder (`.pth` girmez, `.gitignore` zaten dışlıyor). Tabloyu `python karsilastirma\tablo_uret.py` üretir.

## 5. Kaggle oturum mekaniği

- Oturum sınırı ~9 saat; haftalık kota ~30 GPU-saat (Pazartesi sıfırlanır).
- Bir kat 9 saati aşarsa: `egit.py` her epoch `<ad>_son.pth` yazar → **aynı komutu yeni oturumda tekrar koş**, kaldığı epoch'tan, aynı optimizer/scheduler/scaler durumuyla devam eder. Checkpoint'i Kaggle çıktısından kalıcı bir dataset'e ya da Drive'a kopyala, yoksa oturumla silinir.
- Baştan eğitmek gerekirse `--sifirdan`.
- `--isci 2` Kaggle'da iyi; Windows'ta hata ayıklarken `--isci 0` daha hızlı başlar.
- RTX 3050'de üretilen koşular tabloya **girmez** (KURULUM §0b); `tablo_uret.py` bunları otomatik ayıklayıp neden ayıkladığını yazar.

## 6. Komut sırası (T0 → T1)

Ön koşul: `veri/bolme/` dosyaları üretilmiş (`bolme.py bol`) ve `dogrula` çıktısı "TEMİZ".

```powershell
# T0 — OASIS-1 köprüde tek kat, 9 model ayakta mı
python uygulama\ortak\egit.py --model ortak              --varyant sigcnn    --set oasis1 --gorev ikili --kat 0 --veri D:\veri\oasis1\islenmis
python uygulama\ortak\egit.py --model baran_P01_korolev  --varyant voxcnn    --set oasis1 --gorev ikili --kat 0 --veri D:\veri\oasis1\islenmis
python uygulama\ortak\egit.py --model baran_P01_korolev  --varyant resnet    --set oasis1 --gorev ikili --kat 0 --veri D:\veri\oasis1\islenmis
python uygulama\ortak\egit.py --model baran_P02_medicalnet --varyant resnet18 --set oasis1 --gorev ikili --kat 0 --veri D:\veri\oasis1\islenmis
python uygulama\ortak\egit.py --model baran_P02_medicalnet --varyant resnet18 --agirlik monai --set oasis1 --gorev ikili --kat 0 --veri D:\veri\oasis1\islenmis
python uygulama\ortak\svm_kos.py --set oasis1 --gorev ikili --kat 0 --veri D:\veri\oasis1\islenmis

# T0b — LR taraması (kısa; seçilen LR'yi not et, sonraki katmanlarda --lr ile sabitle)
python uygulama\ortak\egit.py --model baran_P02_medicalnet --varyant resnet18 --agirlik monai --set adni1 --gorev ikili --kat 0 --tohum 2026 --epoch 30 --sabir 8 --lrler 1e-3 3e-4 1e-4 --veri D:\veri\adni1\islenmis

# T1 — ADNI1 ikili, 5 kat, tek tohum, seçilen LR
python uygulama\ortak\egit.py --model baran_P02_medicalnet --varyant resnet18 --agirlik monai --set adni1 --gorev ikili --tum_katlar --tohum 2026 --lr 3e-4 --veri D:\veri\adni1\islenmis

# Dış test (ADNI'de eğitilen model → OASIS-1 sıfır-atış)
python uygulama\ortak\dis_test.py --model baran_P02_medicalnet --tum_ckpt "*adni1_ikili*" --dis_set oasis1 --etiket veri\oasis1_etiket.csv --veri D:\veri\oasis1\islenmis --kaynak_etiket veri\adni1_etiket.csv

# Tablo
python karsilastirma\tablo_uret.py --set adni1 --gorev ikili --yaz karsilastirma\TABLO-URETILDI.md
```

## 7. Danışmana sorulacak (SUREC §7'ye ek)

7. Üç sınıf görevini **5 kat × 1 tohum** koşmamız kabul edilir mi? Ücretsiz GPU bütçesi (Kaggle ~30 sa/hafta/hesap) tam protokolün (270 koşu, 270–540 GPU-saat) üçte birini bile karşılamıyor; birincil görevde 3 tohumu koruyup ikincil görevde tek tohuma inmeyi öneriyoruz, raporda açıkça belirtilerek. Alternatif: bölümün GPU sunucusu/kümesi kullanıma açık mı?
