# PROVA RAPORU — hattın gerçek veride uçtan uca sınanması

**Tarih:** 25.10.2026 · **Koşan:** Baran · **Durum:** tamamlandı

> ⚠ **Bu rapor `SONUCLAR.md` değildir ve oradaki tabloya girmez.** Görev projenin birincil görevi
> (AD vs NC) değil; veri de ortak veri seti değil. Amaç **hattın çalıştığını kanıtlamak**, model
> başarısı ölçmek değil.

## 1. Neden bu prova yapıldı

Kod yazılmıştı ama gerçek MRI üzerinde hiç koşmamıştı. Sentetik testler HD-BET ve MNI kaydını
atlıyordu, yani hattın en kırılgan iki adımı denenmemişti. ADNI onayı beklenirken açık veriyle
tüm zinciri (indirme → ön işleme → etiket → bölme → eğitim → metrik → tablo) uçtan uca koşturduk.

## 2. Veri

| | |
|---|---|
| Kaynak | OpenNeuro `ds007561` + `ds007857` (ikisi de CC0) |
| Görev | **NC vs MCI** (`ikili-mci`) — AD denek sayısı 2 olduğu için AD vs NC yapılamadı |
| Denek | 142 (88 NC · 54 MCI), iki kohorttan |
| Ön işleme | HD-BET → N4 → MNI152 afin → maske içi z-score → 128³ |
| Bölme | denek düzeyinde, kohort × sınıf dengeli, kilitli test 22 · CV 120 · 5 kat |
| Sızıntı kontrolü | **TEMİZ (0 kesişim)** |
| Koşu | kat 0, tohum 2026, 40 epoch (sabır 10), RTX 3050 4 GB |

ds007857'de MCI grubu anlamlı olarak daha yaşlıydı (74,1 vs 71,3 · p = 0,0014). Yaş/cinsiyet
eşleştirmesi uygulandı; sonrasında p = 0,76 oldu.

## 3. Sonuçlar

| Model | Parametre | Test BAcc | Test AUC | Duyarlılık | Özgüllük | Epoch | Süre |
|---|---|---|---|---|---|---|---|
| Temel: SigCNN3D | 0,07M | 0,500 | 0,641 | 1,000 | 0,000 | 11 | 4,8 dk |
| P01 VoxCNN | 0,38M | 0,500 | 0,479 | 1,000 | 0,000 | 11 | 5,1 dk |
| P01 VoxResNet | 3,21M | **0,611** | 0,641 | 0,222 | 1,000 | 12 | 11,7 dk |
| P02 ResNet-18 (sıfırdan) | 32,99M | **0,611** | **0,846** | 0,222 | 1,000 | 14 | 6,5 dk |

## 4. Bu sayıların gerçekte söylediği

**Dört modelin hiçbiri öğrenmedi — ikisi her şeye "MCI", ikisi her şeye "sağlıklı" dedi.**
Duyarlılık/özgüllük çiftlerine bakmak yeterli: `1,000 / 0,000` ve `0,222 / 1,000` çökmüş çözümlerdir.
BAcc 0,611 yüksek görünüyor ama çoğunluk sınıfını söylemekten geliyor, ayırt etmekten değil.

**Tek anlamlı işaret: P02 ResNet-18'in AUC'si 0,846.** AUC eşikten bağımsızdır; model karar eşiğini
bulamamış ama **sıralaması** iki sınıfı ayırıyor. Dört model içinde belirgin şekilde en yüksek olan bu.
Daha derin mimarinin az veriden daha fazla sinyal çıkardığına işaret ediyor — ama 22 kişilik test
kümesinde bu tek başına kanıt değil.

**Neden öğrenemediler:**
1. **96 eğitim deneği** — 2 milyon vokselli hacimlerle 3B CNN eğitmek için çok az.
2. **MCI vs sağlıklı zaten zor.** Literatürde binlerce denekle bile %65–75 bandında; AD vs sağlıklıdan
   belirgin şekilde zor, çünkü MCI'de atrofi silik.
3. **Test kümesi 22 kişi.** Tek bir deneğin yeri değişince BAcc ~%4,5 oynuyor. Tablodaki `±0,000`
   yanıltıcıdır: tek koşu olduğu için sapma hesaplanamamıştır, sıfır değildir.

## 5. Asıl kazanç: hat çalışıyor ve beş hata bulundu

Prova sonuç üretmedi ama **sentetik testlerin göremediği beş gerçek hatayı** ortaya çıkardı:

| # | Hata | Nasıl bulundu |
|---|---|---|
| 1 | ASCII olmayan yolda SimpleITK dosya açamıyor | Türkçe kullanıcı klasöründe ilk gerçek hacim |
| 2 | `hd-bet` venv aktive edilmeden bulunamıyor | ilk gerçek çağrı |
| 3 | HD-BET 2.x `-device 0` kabul etmiyor (`cuda:0` gerekiyor) | GPU'ya geçince; GPU kullanımı %0'dı |
| 4 | MNI kaydı her hacimde çöküyor (MOMENTS + yanlış adım sırası) | ilk gerçek kayıt denemesi |
| 5 | VRAM tahmini on kat yanlış ("ResNet-18 128³ sığmaz" → gerçekte 1,58 GB) | `vram_olc.py` ile ölçüm |

Ayrıca ön işleme kalitesi 143 hacmin **143'ünde** temiz çıktı: maske hacimleri 1108–1578 cm³,
kayıt metrikleri −0,53 ile −0,46 arasında, tek uyarı yok.

## 6. Sırada

Prova bitti; **asıl görev (AD vs NC)** için `radiata-ai/brain-structure` koleksiyonunun OASIS alt kümesi
indiriliyor: yaş ≥ 60 süzgeciyle **165 AD + 183 sağlıklı**, yaş zaten dengeli (p = 0,84).
Ayrıntı: `veri/VERI-SETI.md §2g`.

Bu prova o koşunun provasıdır: aynı komutlar, aynı protokol, yalnız veri ve görev değişiyor.
