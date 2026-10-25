# SONUÇLAR — Altı modelin ortak veri + ortak protokol karşılaştırması

Kaynak: `karsilastirma/kosu_kayitlari/*.json` (egit.py üretir). Satır biçimi PROTOKOL.md'de. Her hücre **5 kat × 3 tohum ortalama ± ss**; test = kilitli %15 (yalnızca burada açılır). Doldurma: **`python karsilastirma\tablo_uret.py`** — kayıtları okur, PROTOKOL/KURULUM'a uymayan koşuları (geliştirme GPU'su, mimari sapma, commit'siz) tablodan ayıklayıp nedenini yazar, LR/C taramasını **doğrulama** üstünden tek değere indirir ve test metriklerini ortalama ± ss basar. Koşu sırası ve GPU bütçesi: `karsilastirma/KOSU-PLANI.md`.

## A) OASIS-1 (köprü set, ≥60 yaş) — ikili görev (NC vs demans)
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
