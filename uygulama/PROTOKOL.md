# PROTOKOL — Altı implementasyonu adil karşılaştırma kuralları (BAĞLAYICI)

Bu kurallara uymayan sonuç `karsilastirma/SONUCLAR.md` tablosuna girmez. Dayanak: Wen 2020 [P03], Yagis 2021 [P05], Rumala 2023, Dhinagar 2023 [P15].

## 10 kural
| # | Kural | Nasıl sağlanır |
|---|---|---|
| 1 | **Denek düzeyinde bölme.** Aynı deneğin (RID / OASIS ID) hiçbir taraması, tekrarı veya dilimi farklı katlara düşmez. | `uygulama/ortak/bolme.py` → `StratifiedGroupKFold(groups=denek)`; bölme CSV'leri `veri/bolme/` |
| 2 | **Bölme önce, bir kez.** Veri artırma, normalizasyon istatistiği, özellik seçimi, ön eğitim yalnızca eğitim katında; test seti hiperparametre seçiminde hiç kullanılmaz. | Kilitli test %15 tohum 2026; CV yalnızca kalan %85'te |
| 3 | **Aynı ön işleme.** Altı model aynı `onisle.py` çıktısını (128³ float16, MNI152, z-score) kullanır; mimari başına özel ön işleme yok. Girdi boyutunu küçültmek gerekiyorsa (ör. 96³) **herkes** küçültür. | `uygulama/ortak/veri.py` tek Dataset sınıfı |
| 4 | **Aynı görevler.** Birincil: **AD vs NC** (ikili). İkincil: **NC / MCI / AD** (üç sınıf). İsteğe bağlı: sMCI vs pMCI. Her model her iki görevi koşar. | `egit.py --gorev ikili|uc` |
| 5 | **5-kat CV × 3 tohum.** (Ücretsiz GPU bütçesi tam protokole yetmiyor; indirgeme ve öncelik katmanları `karsilastirma/KOSU-PLANI.md`, danışman onayına sunulacak.) Katlar denek düzeyinde ve sınıf dengeli; tohumlar 2026, 2027, 2028 — hepsinde aynı. Ortalama ± standart sapma raporlanır. | `egit.py --tohum` |
| 6 | **Metrikler.** Dengeli doğruluk (BAcc), AUC (ikili: ROC-AUC; üç sınıf: makro OvR), F1-makro, duyarlılık, özgüllük, doğruluk; üç sınıfta karışıklık matrisi. Yalnız "doğruluk" raporlanmaz. | `uygulama/ortak/metrikler.py` |
| 7 | **Eşit bütçe.** Her model: en fazla 100 epoch, erken durdurma (doğrulama BAcc, sabır 15), AdamW, aynı LR taraması {1e-3, 3e-4, 1e-4} ve aynı batch (4; VRAM yetmezse gradient accumulation ile etkin 4). Model başına fazladan hiperparametre taraması yok. | `egit.py` varsayılanları; tarama `egit.py --lrler 1e-3 3e-4 1e-4` (her LR kendi koşu adı ve kaydı) |
| 8 | **Ön eğitim ayrı sütun.** Dış veriyle ön eğitilmiş modeller (MedicalNet, ImageNet-2B) tabloda "ön eğitim: evet" olarak işaretlenir; sıfırdan eğitilenlerle aynı satırda yarışmaz, yan yana gösterilir. | SONUCLAR.md sütunu |
| 9 | **Temel çizgiler.** Aynı veride (a) sığ 3B CNN (4 blok, Zhang & Khalvati 2022) ve (b) voksel tabanlı lineer SVM (Wen 2020) koşulur. Karmaşık modeller bunları geçmiyorsa raporda açıkça yazılır. | `uygulama/ortak/temel_cizgi.py`; koşucular: `egit.py --model ortak --varyant sigcnn` ve `svm_kos.py` (Baran) |
| 10 | **Şeffaf raporlama.** Bölme bilgisi (`<set>_bolme_haritasi.csv` — yalnız denek kimliği + kat/bölüm; tanı/yaş/cinsiyet taşıyan CSV'ler **ADNI DUA gereği depoya girmez**, yerelde kalır), ayarlar, tohumlar, sürümler (`pip freeze`), donanım, eğitim süresi ve `deterministic` ayarları depoya konur; her sonuç satırının yanında commit hash'i bulunur. | `karsilastirma/kosu_kayitlari/<model>-<varyant>_<set>_<gorev>_t<tohum>_k<kat>_lr<lr>_b<boyut>[_<etiket>].json` (egit.py üretir; lr ve boyut adın içinde olduğu için tarama ve ablation koşuları birbirini ezmez) |

## Wen 2020'den alınan ek kurallar (P03 hakem notu, 25.10.2026)
- **K1 Geç bölme yasağı:** normalizasyon istatistiği, öznitelik seçimi, artırma ve (varsa) otokodlayıcı ön eğitimi bölmeden **sonra** ve yalnız eğitim katında.
- **K2 Kilitli test:** `bolme.py` başta %15 denek düzeyi, sınıf dengeli test ayırır; mimari/hiperparametre seçimi yalnız CV katlarında; test **dondurulmuş** final modelde **bir kez** koşulur. Hiperparametreler aynı katlarda seçilip aynı katlarda raporlanırsa bu Wen'in "bağımsız test yokluğu" sızıntısıdır.
- **K3 Sabit katlar:** kat atamaları sabit tohumla bir kez üretilir, CSV'ye yazılır, tüm deneyler (6 model, temel çizgiler, ablation) aynısını kullanır. "3 tohum" = başlatma/karıştırma tohumu; bölme sabit.
- **K4 Transfer sızıntısı:** AD-NC'de eğitilen modelin MCI görevlerine aktarımında kaynak görev eğitim denekleri hedef test kümesinde bulunamaz.
- **K5 Sağlık testleri:** (a) rastgele etiket → BAcc ≈ 0.5, (b) sentetik ayrılabilir iki sınıf → BAcc ≈ 1.0, (c) RID kesişimi boş (`bolme.py dogrula`). Üçü birden: **`python uygulama\ortak\saglik_testi.py`** (sentetik hacimlerle, veri/GPU gerekmez, ~1–3 dk) — her gerçek koşu turundan önce yeşil olmalı. Her raporda Wen 2020 referansları yan yana: 3B denek baseline **0.82**, hipokampüs ROI **0.89**, doğrusal SVM **0.88** (ADNI test BAcc).
- **Test sonucu tanımı:** Wen'de test BAcc = 5 kat modelinin test sonuçlarının ortalaması (topluluk değil). Bizde de aynı: her kat × tohum modeli testte ayrı koşulur, ortalama ± ss raporlanır.
- **Yoğunluk ölçekleme zorunlu:** ölçeklemesiz eğitim 0.50'de çöker (Wen Exp1); maske içi z-score + arka plan sabit.

## Dış test (ADNI geldikten sonra)
Koşucu: **`uygulama/ortak/dis_test.py`** (eğitim yok, yalnız çıkarım; hedef setin tamamı değerlendirilir, K4 denek kesişimi kontrol edilir). ADNI1'de eğitilen her modelin ikili görevde **OASIS-1 (≥60 yaş)** üzerinde sıfır-atış (zero-shot) sonucu ayrı sütunda raporlanır. Genelleme düşüşü (iç − dış) tartışma bölümünün ana konusudur (Wen 2020, Bron 2021).

## Sonuç satırı biçimi
`model | görev | ön eğitim | BAcc ortalama±ss | AUC | F1-makro | Sens | Spec | Acc | dış test BAcc | parametre sayısı | epoch/süre | VRAM | commit`

## Sızıntı kontrol listesi (her koşudan önce işaretle)
- [ ] `python uygulama\ortak\saglik_testi.py` → "TÜM SAĞLIK TESTLERİ OK" (K5 a/b/c + kayıt alanları)
- [ ] Katlardaki denek kümeleri kesişmiyor (`python uygulama\ortak\bolme.py dogrula --set <set>` çıktısı "TEMİZ (0 kesişim)")
- [ ] Test seti dosyaları eğitim/doğrulama yükleyicisinde yok
- [ ] Normalizasyon per-hacim (z-score) — veri seti geneli istatistik yok
- [ ] Artırma yalnızca `egitim=True` iken
- [ ] Ön eğitimli ağırlık ADNI/OASIS içermiyor (MedicalNet'in 23 seti arasında ADNI yok — doğrulanacak)
- [ ] Tohum sabit; `torch.backends.cudnn.deterministic=True`
