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

---

## 7. GERÇEKLEŞEN: OASIS AD vs NC koşusu (25.10.2026, RTX 3050 4 GB)

Bu bölüm **ölçülmüş** sürelerdir, tahmin değil. Kendi makinenizde planlarken bunları ölçek alın.

### 7.1 Komut sırası
```powershell
# 0) Veri (bir kez, ~1,6 GB indirme + 2 dk işleme)
python veri\indir_radiata.py --hedef D:\veri --kohort OASIS-1 OASIS-2
python onisleme\onisle.py --girdi D:\veri\radiata\ham --cikti D:\veri\radiata\islenmis ^
    --toplu --kafatasi hazir --kayit yok --boyut 128
python uygulama\ortak\bolme.py etiket-radiata --metadata D:\veri\radiata\radiata_metadata.csv ^
    --veri D:\veri\radiata\islenmis --kohort OASIS-1 OASIS-2 --min_yas 60 --cikti veri\oasis_etiket.csv
python uygulama\ortak\bolme.py bol --etiket veri\oasis_etiket.csv --set oasis --cikti veri\bolme
python uygulama\ortak\bolme.py dogrula --set oasis --bolme veri\bolme

# 1) Kat kat koş (kos_oasis.py batch boyutlarını ölçülmüş değerlerden alır)
python karsilastirma\kos_oasis.py --veri D:\veri\radiata\islenmis --kat 0
python karsilastirma\kos_oasis.py --veri D:\veri\radiata\islenmis --kat 1
#  ... kat 2, 3, 4

# 2) Analiz
python karsilastirma\tablo_uret.py --set oasis --gorev ikili
python karsilastirma\altgrup_analiz.py --hepsi --set oasis --veri D:\veri\radiata\islenmis ^
    --cikti karsilastirma\ALTGRUP.md
python karsilastirma\uyum_analiz.py --set oasis --veri D:\veri\radiata\islenmis ^
    --cikti karsilastirma\UYUM.md
```

### 7.2 Ölçülen süreler (kat 0, RTX 3050 Laptop 4 GB)
| Model | Batch | Epoch | Süre | VRAM |
|---|---|---|---|---|
| Temel SigCNN3D | 4 | 40 | 19,5 dk | 0,9 GB |
| P01 VoxCNN | 4 | 60 | 31,6 dk | 0,8 GB |
| P02 MedicalNet (ön eğitimli) | 4 | 22 | 11,0 dk | 1,4 GB |
| P02 sıfırdan | 4 | 27 | 13,5 dk | 1,4 GB |
| P06 CNN+LRP | 4 | 13 | 6,4 dk | 0,7 GB |
| P12 DenseNet121 | 4 | — | 23,8 dk | 2,2 GB |
| P01 VoxResNet | **2 × accum 2** | — | — | 1,8 GB |
| P11 FCN-yama | **2 × accum 2** | — | — | 2,4 GB |
| P07 ResAttNet | **2 × accum 2** | — | — | 3,1 GB |

**Kat başına kaba toplam ~2–3 saat** → 5 kat × 1 tohum ≈ **12–15 saat**.
PROTOKOL madde 5'in istediği 5 kat × 3 tohum ≈ **40–45 saat**; tohum tekrarı öne çıkan
modellere ayrılabilir, ama bu bir **sapmadır ve raporda yazılmalıdır**.

### 7.3 ⚠ Sessiz yavaşlama tuzağı — bunu bir kez yaşadık
VoxResNet batch 4'te `vram_olc.py`'ye göre 3,59 GB istiyor ve araç **"OK"** diyor; kart 4,0 GB.
Gerçek koşuda epoch süresi 32 saniyeden **7 dakikaya** çıktı. Neden: Windows WDDM, kalan belleği
sistem RAM'ine taşıyor — program çökmüyor, **13 kat yavaşlıyor**. 60 epoch o hızda 7 saat demekti.

**Kural: "sığdı" demek yetmiyor. Eşik kartın kapasitesi değil, kapasitenin ~%75'i.**
4 GB kartta hedef **≤ 3,0 GB**. Aşan model `--batch 2 --accum 2` ile koşar; etkin batch
4'te sabit kaldığı için karşılaştırma bozulmaz (PROTOKOL madde 7).

`kos_oasis.py` ayrıca `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` koyuyor: dar VRAM'de
parçalanma tek başına yüzlerce MB yiyor.

**Nasıl fark edilir:** epoch süresi beklenenin 3 katından fazlaysa `nvidia-smi` ile bellek
kullanımına bakın. Kartın %85'inin üzerindeyse batch'i yarıya indirip accum'u iki katına çıkarın.
