# SONUÇLAR — Altı modelin ortak veri + ortak protokol karşılaştırması

Kaynak: `karsilastirma/kosu_kayitlari/*.json` (egit.py üretir). Satır biçimi PROTOKOL.md'de. Her hücre **5 kat × 3 tohum ortalama ± ss**; test = kilitli %15 (yalnızca burada açılır). Doldurma: **`python karsilastirma\tablo_uret.py`** — kayıtları okur, PROTOKOL'e uymayan koşuları (etkin batch ya da girdi boyutu protokol değerinden farklı, mimari sapma, commit'siz) tablodan ayıklayıp nedenini yazar, LR/C taramasını **doğrulama** üstünden tek değere indirir ve test metriklerini ortalama ± ss basar. Koşu sırası ve GPU bütçesi: `karsilastirma/KOSU-PLANI.md`.

## A) OASIS (OASIS-1 + OASIS-2, ≥60 yaş) — birincil görev: **AD vs NC**

**Veri (ölçüldü, `veri/VERI-SETI.md §2g`):** 348 denek — **178 AD / 170 sağlıklı**.
Kaynak `radiata-ai/brain-structure`; OASIS-1 ve OASIS-2 **aynı tarayıcıda** çekilmiş
(Siemens Vision 1,5T), dolayısıyla birleştirmek tarayıcı karıştırıcısı yaratmıyor.
Her iki sınıf her iki kohortta var: OASIS-1 100 AD / 98 NC, OASIS-2 78 AD / 72 NC.

**Denek seçimi (Wen 2020 madde 2.2):** veri boylamsal, denek başına tek oturum seçildi —
AD grubuna deneğin **ilk AD tanılı** oturumu, kontrol grubuna **yalnız kararlı NC**
(hiçbir oturumunda AD tanısı almamış) denekler. OASIS-2'de **14 denek NC→AD dönüşüyor**;
bunlar kontrol grubundan çıkarıldı ve AD grubuna kendi AD oturumuyla girdi. Dönüşen bir
deneği "sağlıklı" saymak kontrol grubunu kirletirdi.

**Bölme:** denek düzeyinde, kohort × sınıf dengeli — kilitli test 53 · CV 295 · 5 kat.
Sızıntı kontrolü **TEMİZ (0 kesişim)**.

**Karıştırıcılar — rapora bu üç satır girecek:**
- **Yaş: dengeli.** AD 76,4 ± 7,1 · NC 75,7 ± 8,7 · Welch p = 0,39. Yaş ≥ 60 süzgeci
  olmadan NC ortalaması 51,8'e düşüyor ve model yaşı öğrenirdi; süzgeç bu yüzden var.
- **Cinsiyet: dengesiz.** AD %54 kadın · NC %72 kadın · Fisher p = 0,0009. Eşleştirme
  348 deneği ~210'a düşüreceği için uygulanmadı; yerine **ölçüldü** (aşağıdaki satır).
- **Karıştırıcı tavanı (`altgrup_analiz.py`):** yalnız demografiden AD tahmin eden
  lojistik regresyon aynı test kümesinde **AUC 0,354–0,418** veriyor, yani şans
  seviyesinin *altında*. Modellerin AUC'si bu tavanın belirgin şekilde üzerindeyse
  sonuç beyinden geliyor, cinsiyetten değil.

**⚠ Ön işleme kaynağı:** bu taramalar Radiata'nın hattından geçmiş (CAT12 + FSL FLIRT,
12 DOF afin, hedef `MNI152NLin2009cAsym` — bizim hattımızla **aynı şablon**). Bizim
`onisle.py` hattı `--kafatasi hazir --kayit yok` ile yalnız maske + z-score + 128³
uyguluyor. Afin normalizasyonun ölçülen sonucu: sınır kutusu her denekte 150×187×159 mm
(±2) ve maske hacmi gerçek ICV ile **ilişkisiz** (r = −0,18) — yani **global kafa/beyin
boyutu bir öznitelik olarak kaldırılmış**. Model bölgesel şekil ve yoğunluk örüntülerine
dayanmak zorunda. Bu Wen 2020'nin `t1-linear` hattının bilinen özelliği, ama raporda
kısıt olarak yazılmalı: toplam beyin hacmi kaybı AD'nin güçlü bir işareti ve kısmen
normalize edilmiş durumda.

**⚠ Birincil metrik AUC.** Ölçtük: test kümesi 53 denek olduğu için BAcc'in karar eşiği
doğrulama katından test kümesine taşınmıyor (VoxCNN: doğrulamada seçilen eşik test BAcc'ini
hiç değiştirmiyor, oysa test'te 0,736 veren bir eşik var). AUC eşikten bağımsız olduğu için
bu sorundan etkilenmiyor. BAcc protokolün sabit argmax kuralıyla ve bu kısıt yazılarak
raporlanıyor.

### A) Sonuç tablosu — AD vs NC
| Model | Görev | Ön eğitim | BAcc | AUC | F1-makro | Sens | Spec | Acc | Dış test BAcc | Parametre | Epoch/süre | VRAM | Commit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Temel: SigCNN3D | ikili | hayır | | | | | | | — | | | | |
| Temel: Voksel SVM | ikili | hayır | | | | | | | — | — | — | — | |
| P01 VoxCNN (Baran) | ikili | hayır | | | | | | | — | | | | |
| P01 VoxResNet (Baran) | ikili | hayır | | | | | | | — | | | | |
| P02 ResNet-18 sıfırdan (Baran) | ikili | hayır | | | | | | | — | | | | |
| P02 ResNet-18 MedicalNet (Baran) | ikili | **evet** | | | | | | | — | | | | |
| P06 CNN+LRP (Görkem) | ikili | hayır | | | | | | | — | | | | |
| P07 ResAttNet (Görkem) | ikili | hayır | | | | | | | — | | | | |
| P11 FCN yama (Ertuğrul) | ikili | hayır | | | | | | | — | | | | |
| P12 DenseNet121 (Ertuğrul) | ikili | hayır | | | | | | | — | | | | |

## B) ADNI1 1.5T baseline — ikili görev (AD vs NC) — **hedef BAcc ≥ 0.85**
(aynı satırlar; "Dış test BAcc" = ADNI1'de eğitilen modelin OASIS-1'de sıfır-atış sonucu)

## C) ADNI1 — üç sınıf (NC / MCI / AD) — ikincil görev
(aynı satırlar + her model için karışıklık matrisi `karsilastirma/cm/<model>.png`)

## D) Ablation'lar
| Soru | Karşılaştırma | Sonuç |
|---|---|---|
| Ön eğitim ne kazandırıyor? | P02 sıfırdan vs MedicalNet | |
| Artık bağlantı ne kazandırıyor? | P01 VoxCNN vs VoxResNet | |
| Dikkat ne kazandırıyor? | P07 öz-dikkat var/yok | |
| Derin model sığ CNN'i geçiyor mu? | hepsi vs SigCNN3D | |
| CNN SVM'yi geçiyor mu? (Wen 2020 bulgusu) | hepsi vs voksel SVM | |
| Girdi boyutu | 96³ vs 128³ (**VoxResNet'te**; VoxCNN 96³'te padding'i de değiştirdiği için bu ablation'a uygun değil) | |

## E) Okuma notları
- Sonuç farkı ± ss içindeyse "fark yok" yazılır; üstünlük iddiası için en az 3 tohumda tutarlı fark aranır.
- Sızıntı kontrol listesi (PROTOKOL) işaretlenmemiş koşu tabloya girmez.
