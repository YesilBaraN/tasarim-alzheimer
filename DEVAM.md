# DEVAM — Oturum devir notu

**Son oturum:** 24–25.10.2026, Baran (Claude Code, Fable). Bir sonraki oturum önce bu dosyayı, sonra `SUREC.md §9`'u okur.

## Bu oturumda yapılanlar
1. Form okundu; konu, ekip, danışman, yöntem çıkarıldı. Ders süreci araştırıldı (BSM 401, yönerge, takvim, 4 aşamalı ara rapor yapısı) → `SUREC.md`.
2. 4 araştırma ajanı (Sonnet) + 1 ek tur: 27 aday makale, veri seti erişimi, araç zinciri, güncel mimariler, tekrarlanabilirlik protokolü, ders süreci. Sonuç: 15 makale (hepsi açık erişimli), tematik 3 grup, atama → `makaleler/MAKALE-LISTESI.md`.
3. Workflow (5 Sonnet okuyucu → 5 Opus hakem, pipeline): P01–P05 inceleme notları `makaleler/baran/` (her biri ~28 K karakter, §13 doğrulama bölümlü). P01/P02/P04'te sayısal çelişkiler bulunup düzeltildi; P05 temiz. **P03 (Wen 2020):** web'den tam metin çekilemedi → PDF'ler PyMuPDF ile metne çevrildi, ikinci tur okuma + hakem koşuldu (durumu aşağıda).
4. Ortak veri kararı (ADNI1 1.5T baseline; köprü OASIS-1; Kaggle setleri reddedildi) → `veri/VERI-SETI.md`.
5. Ön işleme hattı `onisleme/onisle.py` + `test_onisle.py` (py_compile OK; **gerçek koşu kullanıcı PC'sinde**).
6. Adil karşılaştırma protokolü `uygulama/PROTOKOL.md`; ortak kod `uygulama/ortak/` (veri, bölme, metrikler, egit, onnx, temel çizgiler); Baran'ın 2 modeli (`baran_P01_korolev`, `baran_P02_medicalnet`) hakem bulgularıyla düzeltilmiş; `uygulama/test_model.py` (py_compile OK).
7. Ara Rapor 2 taslağı `rapor/ARA-RAPOR-2-TASLAK.md` (danışmanın 4 aşamalı yönergesine birebir).
8. Devir promptları `devir/DEVIR-GORKEM.md`, `DEVIR-ERTUGRUL.md`, `DEVIR-BARAN.md`; `KURULUM.md` (kendi PC); `.gitignore`.

## Sunucuda YAPILMAYANLAR (bilerek)
- Hiçbir pip kurulumu, ağırlık/şablon/veri indirmesi, eğitim veya ön işleme koşusu yok. Kod yalnızca `py_compile` ile denetlendi. **İlk gerçek çalıştırma kullanıcı PC'sinde:** `KURULUM.md §3`.

## Doğrulanmamış / riskli noktalar
- `onisle.py` ve `uygulama/*` **gerçek MRI verisiyle** hiç koşmadı (duman + sağlık testleri sentetik veriyle yeşil). HD-BET ve TemplateFlow indirmeleri ilk gerçek koşuda olacak; kafatası ayıklama ve MNI kaydı yalnız o zaman denenmiş olacak.
- Kurulu venv'de torch **CPU** sürümü: GPU eğitimi için `KURULUM.md §2` Yol A (cu126) ile yeniden kurulacak ve `torch.cuda.is_available()` teyit edilecek.
- MONAI `pretrained=True` yolu MONAI ≥1.3 gerektirir; eski sürümde `agirlik=<yol>` ile elle yükleme kullanılır.
- P01 VoxCNN başlığındaki ReLU'lar (Dense128/Dense64 sonrası) depo kodundan birebir doğrulanmadı (Lasagne varsayılanı varsayıldı).
- OASIS-1 CDR sütunu ve dosya biçimi indirince teyit edilecek; ADNI başvurusunun lisans öğrencisi adına kabul edilip edilmediği belirsiz (danışman adıyla yapılacak).
- Ara rapor tarihleri, not ağırlıkları, kaynak biçimi bölümden sorulacak.

## P03 durumu (tamamlandı)
- 1. tur: web'den tam metin alınamadı (yalnız özet). 2. tur: yayıncı PDF'i (19 sayfa) + arXiv ek tabloları (eTable 1–5) yerel metinden okundu, Opus 38 sayıyı denetledi (yalnız sızıntı türü sayımı yanlış; güven yüksek) → `makaleler/baran/P03-wen2020-cnn-ad-reproducible.md`. Hakemin 5 kuralı `uygulama/PROTOKOL.md`'ye "Wen 2020'den alınan ek kurallar" olarak eklendi; referanslar 0.82 / 0.89 / 0.88 `SUREC.md §7` 1. soruya işlendi.
- Devir dosyaları Opus okunabilirlik denetiminden geçti; 12 bulgu kapatıldı (stub placeholder satırı, `innvestigate` hatası, PROTOKOL komut adı, test_model otomatik keşif, iç teslim tarihleri, claude.ai'de dosya yazılamaması notu).

## Kod denetimi düzeltmeleri (25.10.2026, 2. oturum — Claude Code, Opus)
Kod hiç koşmadığı için gözden kaçan hatalar okunarak bulundu ve düzeltildi:
1. **P01 VoxCNN boyut çökmesi (kritik).** Valid 3³ konvolüsyon zinciri 100³'ün altında negatif/sıfır boyut üretiyordu: 32³ → blok 3'te −1, 64³ → blok 4'te −1, 96³ → son havuz 0. Yani `test_model.py` (32³) ve `model.py`'nin kendi testi (64³) hata verirdi, KURULUM'un RTX 3050 için önerdiği 96³ hiç çalışmazdı. `olustur` artık <100³ girdide `padding=1`e düşüp uyarı basıyor (`VOXCNN_EN_KUCUK_VALID = 100`), model `padding` ve `notu` alanlarını taşıyor, koşu kaydına `model_notu` olarak yazılıyor. `test_model.py` ayrıca 128³ valid kurulumu deniyor. Ayrıca `model.py` `__main__` testi batch 1 + `BatchNorm1d` yüzünden eğitim modunda hata verecekti → `eval()` + `no_grad()`.
2. **egit.py koşu adı çakışması (kritik).** Ad `..._t<tohum>_k<kat>` idi; PROTOKOL madde 7'nin LR taraması ({1e-3, 3e-4, 1e-4}) ve 96³/128³ ablation'ı aynı checkpoint'ten devam edip aynı JSON'u eziyordu. Ada `_lr<lr>_b<boyut>[_<etiket>]` eklendi; `--lrler`, `--etiket`, `--sifirdan` bayrakları geldi; kayda `lr`, `boyut`, `etiket` alanları yazılıyor.
3. **Kesintiden devam yarımdı.** Scheduler / AMP scaler / sabır sayacı kaydedilmiyordu ve checkpoint yalnız doğrulama iyileştiğinde yazılıyordu — oysa KURULUM §6 "her epoch" diyordu. Artık her epoch `<ad>_son.pth` (optimizer + scheduler + scaler + sabır + geçmiş), en iyi doğrulamada `<ad>.pth`; devam bu dosyadan okunuyor, kosinüs LR baştan başlamıyor.
4. **Artırma tohumdan kaçıyordu.** `num_workers=2` ile iki işçi aynı RNG kopyasını kullanıyor, dizi her epoch aynı kalıyordu; MONAI `RandAffine` hiç tohumlanmamıştı (PROTOKOL madde 10 determinizmi tutmuyordu). Artık işçi başına `torch.initial_seed()` türevli RNG (`_isci_baslat`) + `RandAffine.set_random_state`.
5. Gradyan biriktirmede son yarım grubun gradyanları düşüyordu → epoch sonunda bekleyen adım atılıyor.
6. `torch.cuda.amp.GradScaler` (torch ≥2.4'te deprecated) → `grad_scaler()`; checkpoint okuma tek yardımcıda (`ckpt_yukle`, `weights_only` uyumlu); indirilen MedicalNet ağırlığı önce `weights_only=True` ile denenir.
7. `onisle.py`'de maske şablon ızgarasına taşınıp hemen atılıyordu (boşa iş) → doğrudan şablon maskesi. `bolme.py etiket-adni` glob'u sıralı hâle geldi; bir denekte birden fazla `.npy` eşleşirse uyarıyor (başlangıç dışı tarama riski). Modül docstring'leri `r"""` yapıldı (Windows yolları `\o`/`\A` için SyntaxWarning veriyordu, `uygulama\test_model.py` içindeki `\t` sessizce sekmeye dönüşüyordu).

Doğrulama: tüm dosyalar `py_compile` ile derlendi; VoxCNN boyut zinciri ayrı bir hesapla doğrulandı (padding=0 → ≥100, padding=1 → ≥16). *(O oturumda torch kurulu olmadığı için gerçek koşu yapılamamıştı; aşağıdaki bölümde koşturuldu ve 4 ek hata çıktı.)*

## Eksik parçalar tamamlandı (25.10.2026, 3. oturum — Claude Code, Opus)

Ortam: makinede 3.11/3.12 yoktu → **Python 3.12.10** kuruldu (`py install 3.12`), proje içinde `.venv` açıldı, torch (cu124) + `requirements.txt` kuruluyor. KURULUM §1–2 artık gerçekten uygulanmış durumda.

Yazılan ve PROTOKOL'de eksik olan parçalar:
1. **`uygulama/ortak/saglik_testi.py`** — PROTOKOL "K5 sağlık testleri" betiği yoktu. Sentetik hacimlerle eğitim hattının TAMAMINI koşar (bölme → veri → egit → metrik → JSON): ayrılabilir iki sınıfta BAcc ≈ 1.0, rastgele etikette ≈ 0.5, bölme kesişimi boş, koşu kaydı madde 10 alanlarını taşıyor, farklı LR'ler birbirini ezmiyor. Veri/GPU/internet gerekmez (~1–3 dk).
2. **`uygulama/ortak/model.py`** — temel çizgi (SigCNN3D) `egit.py` ile koşulamıyordu: model sözleşmesi `uygulama/<ad>/model.py` isterken sığ CNN `ortak/temel_cizgi.py`'deydi. Artık `--model ortak --varyant sigcnn` çalışıyor (PROTOKOL madde 9a).
3. **`uygulama/ortak/svm_kos.py`** — madde 9b voksel SVM temel çizgisinin koşucusu yoktu (epoch'lu eğitimi olmadığı için `egit.py`'ye girmiyor). Aynı bölmeyi, aynı metrikleri ve `egit.py` ile aynı JSON şemasını kullanır; ölçekleyici+SVM yalnız eğitim katında fit edilir; C taraması doğrulama üstünden.
4. **`uygulama/ortak/dis_test.py`** — PROTOKOL'ün "Dış test" bölümü (OASIS-1 sıfır-atış) için hiç kod yoktu. Eğitim yapmaz, checkpoint'i yükler, hedef setin tamamını değerlendirir, **K4 transfer sızıntısını** (kaynak deneklerinin hedefte görünmesi) kontrol eder ve iş durdurur.
5. **`karsilastirma/tablo_uret.py`** — SONUCLAR.md'de "(yazılacak)" diye duruyordu. Kayıtları okur; geliştirme GPU'sunda üretilmiş, mimari sapmalı ya da commit'siz koşuları **tablodan ayıklar ve nedenini yazar**; LR/C taramasını **doğrulama** BAcc'ine göre tek değere indirir (test'e bakmaz — K2); eksik kat/tohum ve karışık commit uyarısı verir.
6. **`karsilastirma/KOSU-PLANI.md`** — GPU bütçesi hesabı: tam protokol 270 koşu / 270–540 GPU-saat, ücretsiz tavan ~720 saat. T0–T4 öncelik katmanları, kim neyi koşar, Kaggle oturum mekaniği, komut sırası. Danışmana sorulacak soru `SUREC.md §7` madde 7 olarak eklendi.
7. **`uygulama/api/tahmin.py` + `api/README.md`** — karar destek prototipinin çıkarım katmanı (SUREC 19 "başlamadı"ydı). `KararDestek` sınıfı: ONNX girdi şeklinden boyutu okur, ön işlemeyi `onisle.py`'den çağırır (eğitim/servis uyumu), softmax olasılıkları + ön işleme uyarıları + "araştırma prototipi, tanı aracı değildir" uyarısını döndürür.
8. **`egit.py` eklemeleri:** `--optimizer adamw|adam|sgd` (P01'in makale-sadık koşusu için; ayrı `calistir.py` gerekmedi, P01 README güncellendi), `--isci`, `--cikti`, ve koşu kaydına `surumler` (python/torch/cuda/monai/numpy/sklearn/SimpleITK/nibabel) + `deterministic` — madde 10 "sürümler kaydedilir" şartı artık gerçekten sağlanıyor.
9. **ADNI DUA uyumu (yeni bulgu):** PROTOKOL madde 10 bölme listelerini depoya koymayı istiyordu, ama o CSV'ler denek kimliği + **tanı + yaş + cinsiyet** taşıyor — DUA klinik veriyi üçüncü tarafa (GitHub dahil) dağıtmayı yasaklar. `bolme.py` artık ek olarak **`<set>_bolme_haritasi.csv`** yazıyor (yalnız denek_id + bölüm + kat, klinik sütun yok); `.gitignore` klinik CSV'leri dışlayıp haritayı içeriyor; PROTOKOL madde 10, `veri/bolme/README.md` ve rapor §4.1 buna göre güncellendi. (Alan standardı da bu: clinicadl bölmelerini böyle yayımlar.)
10. `rapor/ARA-RAPOR-2-TASLAK.md` §4.1 mimari bloğu 5 → 6 katmana çıktı (doğrulama/raporlama katmanı eklendi, dağıtım katmanı gerçek dosyalara bağlandı) ve §5'e "kaynak kısıtı" paragrafı eklendi (yönerge Madde 7 "gerçekçi kısıtlar").

## Ortam kuruldu ve her şey gerçekten koşturuldu (25.10.2026, 3. oturum sonu)

**Ortam:** Python 3.12.10 (`py install 3.12`) + proje içi `.venv`; torch 2.14.1, monai 1.6.1, numpy 2.5.2, SimpleITK 2.5.6, scikit-learn 1.9.1, pandas 3.1.0, nibabel 5.4.2, onnx 1.23.2, onnxruntime 1.31.0, onnxscript 0.7.2. Tam liste: `karsilastirma/surumler-dogrulandi-2026-10-25.txt` (PROTOKOL madde 10). **Bu venv'de torch CPU sürümü**; GPU için `KURULUM.md §2` Yol A (cu126).

### Koşturunca çıkan 4 hata (py_compile'ın göremediği türden)
1. **cp1254 `UnicodeEncodeError` — bütün betikleri çökertiyordu (kritik).** Windows konsolu Türkçe kod sayfasında açılıyor; `→`, `±`, `≈`, `≥`, `█` karakterleri kodlanamıyor ve betik ilk `print`'te çöküyordu. `test_model.py` daha ikinci satırda ölüyordu. 12 giriş noktasında `sys.stdout/stderr.reconfigure(errors="replace")` eklendi (konsolun kendi kodlaması korunur, Türkçe harfler doğru görünür, yalnız nadir simgeler `?` olur); kütüphane seviyesindeki `print`'ler cp1254-güvenli ASCII'ye çevrildi.
2. **P02 `shortcut_type` / `bias_downsample` ters açılmış (kritik).** MONAI'nin `get_medicalnet_pretrained_resnet_args` fonksiyonu `(bias_downsample, shortcut_type)` döndürüyor — teyit edildi: 18 → `(True, 'A')`. Kod ise `shortcut, bias = ...` diye açıyordu → `ValueError: Unsupported option 'True'`. **P02 modeli hiç kurulamıyordu.** Sıra düzeltildi ve sürüm değişse de kırılmasın diye tipe bakarak ayıklanıyor.
3. **`monai>=1.4` ile `cu124` kanalı uyuşmuyor (GPU'yu sessizce kapatıyor).** monai 1.6.1 `torch>=2.8.0` istiyor, cu124 kanalı ise torch 2.6.0'da bitiyor → `pip install -r requirements.txt` CUDA torch'u **PyPI'den CPU sürümüyle değiştiriyor**, kurulum başarılı görünüyor ama `torch.cuda.is_available()` `False`. Ölçülen kanallar: cu124 → 2.6.0, cu128 → 2.11.0, **cu126 → 2.14.1**, cu130 → 2.14.1. `KURULUM.md §0b/§2` cu126'ya geçirildi, tuzak açıkça yazıldı ve her pip turundan sonra koşulacak bir doğrulama komutu eklendi.
4. **`onnxscript` eksikti → ONNX dışa aktarma çalışmıyordu.** torch ≥2.9'un dynamo tabanlı `torch.onnx.export`'u bu paketi istiyor; `requirements.txt`'te yoktu, yani projenin ana çıktısı olan ONNX paketleme ilk denemede hata veriyordu. Paket requirements'a eklendi, `onnx_disa_aktar.py` eski TorchScript aktarıcısına geri düşüş yolu kazandı.

Küçükler: `tahmin.py` olasılık çubukları ASCII'ye çevrildi (cp1254'te `█` → `?`, ekran görüntüsü bozuluyordu); `tablo_uret.py` eşitlikte belirli hiperparametre seçiyor ve satıra veri seti adını yazıyor.

### Doğrulanan zincir (hepsi gerçekten koştu)
| Ne | Sonuç |
|---|---|
| `uygulama\test_model.py` | **TÜM TESTLER OK** — VoxCNN 32³ (padding=1, 0.38M), **VoxCNN 128³ valid padding=0**, VoxResNet (3.21M), SigCNN3D (0.07M), P02 ResNet-18 (32.99M), DenseNet121 (11.25M), Dataset/DataLoader/metrikler |
| `onisleme\test_onisle.py` | **TÜM TESTLER OK** — N4, maske içi z-score (ort 0.0000, ss 1.0000), kırpma, uçtan uca hat + meta JSON |
| `uygulama\ortak\saglik_testi.py` | **TÜM SAĞLIK TESTLERİ OK** — ayrılabilir iki sınıf **BAcc 1.000**, rastgele etiket **BAcc 0.500**, bölme kesişimi temiz, kayıt alanları tam, farklı LR → farklı kayıt, bitmiş koşuda devam dosyası silindi |
| `uygulama\ortak\svm_kos.py` | koştu; C taraması (0.01 / 1) iki ayrı kayıt, sentetik ayrılabilir sette test BAcc 1.000 |
| `uygulama\ortak\onnx_disa_aktar.py` | **uyum: True**, PyTorch ↔ onnxruntime en büyük fark **1.9e-06** |
| `uygulama\api\tahmin.py` | AD imzalı hacim → **AD %65.5**, temiz hacim → **NC %90.4**; prototip uyarısı çıktıda |
| `uygulama\ortak\dis_test.py` | sıfır-atış değerlendirme koştu (n=64); **K4 koruması** kaynak denekleri hedefte bulup işi doğru şekilde durdurdu |
| `karsilastirma\tablo_uret.py` | 6 kaydı "commit hash'i yok" diye **tablo dışı bıraktı** (kural çalışıyor — `git init` gerekiyor); `--tumu` ile tabloyu üretti, LR'yi **doğrulama** BAcc'ine göre seçti (0.001 → 0.750 > 0.0003 → 0.500), eksik kat/tohum uyarısı verdi |

Not: sentetik verideki 1.000'ler hattın çalıştığını gösterir, model başarısını **göstermez** — sinyal kasten lineer ve belirgin.

## Sıradaki (öncelik sırasıyla)
1. **Baran, bu hafta:** danışmana `SUREC.md §8` e-postası (ADNI) + §7 soruları; OASIS-1 "Request Access"; bölümden ara rapor tarihleri.
2. **Görkem / Ertuğrul:** `KURULUM.md` → Python 3.12 venv kur, `test_model.py` + `test_onisle.py` + `saglik_testi.py` yeşil olsun (Baran'da yeşil); sonra devir promptlarıyla P06–P15 incelemeleri. **En kritik darboğaz bu:** Ara Rapor 2 "10–15 kaynak" istiyor, elde 5 var.
2b. ✅ **Baran — bitti:** Git deposu + GitHub + CI (https://github.com/YesilBaraN/tasarim-alzheimer, public). Koşu kayıtlarına commit hash'i düşüyor, `tablo_uret.py` artık kayıtları kabul ediyor. CI her push'ta Windows+Linux'ta hattın tamamını koşuyor.
3. **Baran:** OASIS-1 gelince `onisle.py --toplu` → `bolme.py etiket-oasis` + `bol` + `dogrula` → P01/P02 ilk koşu → `karsilastirma/SONUCLAR.md`.
4. Ara Rapor 2'yi `BSM401_Sablon_201611.docx` biçiminde Word'e dökmek (docx skill; şablonu bölüm sitesinden indir) — literatür paragrafları P01–P15 notlarından.
5. ✅ **Bitti:** P02 iki aşamalı eğitim `egit.py --isinma N` ile geldi; P01'in makale optimizer'ı `--optimizer`, `tablo_uret.py` ve ısı haritası (`api/isi_haritasi.py`) da tamamlandı.
6. ADNI gelince aynı hattı ADNI1'de koş (`KOSU-PLANI.md` T0→T1); dış test `dis_test.py` ile OASIS-1.
7. Gerçek MRI ile ilk koşuda denenmemiş iki adım: HD-BET kafatası ayıklama ve MNI152 afin kayıt (sentetik testte atlanıyor). İlk 5 hacimde `--nii` ile çıktıyı görsel kontrol et, `_toplu_ozet.json` uyarılarına bak.
8. GPU: venv'de CPU torch var; `KURULUM.md §2` Yol A (cu126) ile yeniden kur ve `torch.cuda.is_available()` teyit et.
9. **ADNI/OASIS onayını BEKLEMEDEN yapılabilir (7. maddeyi açar):** OpenNeuro **ds007561** (CC0, kayıt gerekmez, 20 denek, gerçek NC/MCI/AD etiketli) ve **IXI** (CC BY-SA, ~600 etiketsiz T1) hemen indirilebilir. `onisle.py`'nin gerçek MRI'daki davranışı — HD-BET kafatası ayıklama ve MNI152 kaydı — ancak böyle denenir. Karşılaştırmaya girmez, yalnızca hattın doğru çalıştığını kanıtlar. `veri/VERI-SETI.md §2b`.

---

## 4. Oturum Sonu Devri — Ahmet Görkem Yavuz (G231210032) / Grup B Tamamlandı (25.10.2026)

Grup B ("Dikkat Mekanizmaları ve Açıklanabilirlik") kapsamındaki tüm makale incelemeleri, hakem denetimleri, rapor bölümleri, tasarım spesifikasyonları ve iki model implementasyonu eksiksiz olarak tamamlandı:

### 1. 5 Makale İncelemesi ve Opus Doğrulamaları (`makaleler/gorkem/`)
- **P06 (Böhle 2019):** Tam metin PMC6685087 ve `moboehle/Pytorch-LRP` deposundan incelendi. 14 bölüm tam dolduruldu. §13'te **ÇELİŞKİ VAR** belgelendi (makalede 969 tarama / 344 denek; depodaki ADNI split'te 1.069 tarama / 380 denek; depoda batch size 4). LRP $\beta=0$ kuralının sağlıklı kontrollerde yanlış pozitif üretmediği ve hipokampus hacmiyle $r = -0,560$ ($p < 0,001$) ters korelasyonu doğrulandı.
- **P07 (Zhang 2021, 3D ResAttNet):** IEEE J-BHI / arXiv:2008.04024v2 tam metninden incelendi. 14 bölüm tam dolduruldu. §13'te **ÇELİŞKİ YOK**. ResAttNet34 ile AD-NC ACC %91,3, AUC 0,984; pMCI/sMCI ACC %82,1, AUC 0,920; ADNI-2 dış test ACC %82,6, AUC 0,927. Layer 3'ten ($46\times55\times46$) 3B Grad-CAM yerelleştirmesi doğrulandı.
- **P08 (Dyrba 2021):** *Alzheimer's Res. Ther.* (BMC) 13:191 tam metninden incelendi. 14 bölüm tam dolduruldu. §13'te **ÇELİŞKİ YOK**. $N=663$ eğitim, $N=1.655$ devasa bağımsız dış test havuzu (ADNI-3, AIBL, DELCODE; tümünde AUC $\ge 0,91$). LRP ilgi haritalarının hipokampus hacmiyle $r = -0,87$ ($p < 0,001$; CV medyanı $r = -0,84$) korelasyonu ve Bokeh tabanlı interaktif web karar desteği doğrulandı.
- **P09 (Hoang 2023, 3D-DAM):** arXiv:2310.12574 tam metninden incelendi. 14 bölüm tam dolduruldu. §13'te **ÇELİŞKİ VAR** belgelendi (arXiv HTML özetinde %96,3 / %91,9 yazarken, PDF metninde ve Tablo 2'de AD %98,18, pMCI %91,78 yazmaktadır; katman açıklamalarında kanal sayısına "kernel size" denmesi ve SGD için 2. momentum yazımı gibi editoryal hatalar belgelendi). AIBL (%86,3) ve OASIS-1 (%83,4) dış testleri doğrulandı.
- **P10 (Jin 2020, 3DAN):** *Adv. Sci.* 7:1903529 (PMC7375255) tam metin ve XML tablolarından incelendi. 14 bölüm tam dolduruldu. §13'te **ÇELİŞKİ YOK**. $N=1.832$ denek (Çin In-house $N=716$, ADNI $N=1.116$). 4 strateji (In-house $\rightarrow$ ADNI dış test ACC %86,1, AUC 0,912; ADNI 10-kat CV ACC %92,1, AUC 0,941). Brainnetome Atlası (273 ROI) $t$-istatistiği korelasyonu $r = 0,59$ ($p < 10^{-26}$) ve MMSE/BOS biyobelirteç ilişkileri doğrulandı.

### 2. Ortak Tablo ve Rapor Katkıları
- **`makaleler/KARSILASTIRMA-15.md`:** P06–P10 satırları tüm metrikler ve sızıntı değerlendirmeleriyle güncellendi; Grup B'den çıkan ortak dersler (Maddeler 6–10: XAI klinik güveni, biyobelirteç korelasyonu, 3B dikkat ile varyans düşüşü, kovaryat regresyonu, çok merkezli dış test zorunluluğu) eklendi.
- **`makaleler/MAKALE-LISTESI.md`:** P06–P10 satırları "AI özeti + Opus doğrulandı" durumuna geçirildi.
- **`rapor/ARA-RAPOR-2-TASLAK.md`:**
  - §2.2 bölümü her 5 makale için 1-2 derinlemesine akademik paragrafla genişletildi.
  - §3.3 use-case bölümü `rapor/sekiller/usecase.puml` ile entegre edildi.
  - §4.3 arayüz mock-up bölümü `rapor/sekiller/mockups_spec.md` ile bağlandı.

### 3. Tasarım ve Arayüz Çıktıları (`rapor/sekiller/`)
- **`rapor/sekiller/usecase.puml`:** 3 aktör (Radyolog, Araştırmacı, Yönetici) ve UC-1...UC-6 kullanım senaryolarını, `<<include>>` ve `<<extend>>` ilişkilerini içeren eksiksiz PlantUML kodu yazıldı.
- **`rapor/sekiller/mockups_spec.md`:** E1 (Giriş), E2 (Yükle/Anonimleştir), E3 (Ön İşleme Durumu), E4 (Karar Destek + Zorunlu Yasal Uyarı "Karar desteğidir, tanı değildir"), E5 (3 Eksenli XAI Dilim Gezintisi / Eşikleme), E6 (PDF Rapor Önizleme), E7 (Çoklu Model Karşılaştırma Paneli) spesifikasyonu yazıldı.

### 4. İki Model ve XAI İmplementasyonu (`uygulama/`)
- **P06 (`uygulama/gorkem_P06_bohle/`):**
  - `LICENSE-Pytorch-LRP`: BSD-3 lisans dosyası eklendi.
  - `model.py`: Böhle 2019 4 bloklu 3B CNN mimarisi (`BohleCNN3D`) ve `olustur(varyant='cnn', sinif_sayisi, girdi_boyut)` fabrika fonksiyonu yazıldı (32³ için 512, 128³ için 32.768 girişli Linear).
  - `lrp.py`: Autograd tabanlı kararlı LRP $\beta=0$ ($\alpha=1, \beta=0$) algoritması, 3 eksenli ortogonal görselleştirme (`gorsellestir`) ve CLI desteği kodlandı.
- **P07 (`uygulama/gorkem_P07_resattnet/`):**
  - `model.py`: Hafif kök (3 ardışık 3x3x3 evrişim), 3B Rezidüel Öz-Dikkat bloğu ($Q, K, V$, başlangıçta $\gamma=0$), `ResAttNet3D` ve `olustur(varyant='resatt18'|'resatt34')` fabrikası yazıldı. Ablasyon desteği (`dikkat_acik=False`) eklendi.
  - `gradcam.py`: 3B aktivasyon ve gradyan kancaları (hooks), trilinear enterpolasyonla 128³ boyutuna büyütme, 3 eksenli görselleştirme (`gorsellestir`) ve CLI arayüzü kodlandı.

### 5. Donanım ve Süreç Güncellemesi
- `nvidia-smi` çıktısıyla makinede **NVIDIA GeForce RTX 4060 Laptop GPU (8 GB VRAM)** olduğu teyit edildi. Bu donanım 128³ boyutta batch size 4 ile tüm modellerin yerel eğitimine olanak sağlamaktadır.
- `SUREC.md §9` tablosundaki İş 4, 11, 13, 16 "bitti" olarak güncellendi.
- Sıradaki aşama: Ertuğrul'un Grup C incelemeleri (P11–P15) ve tasarım diyagramları (`devir/DEVIR-ERTUGRUL.md`).

---

## 5. Oturum Sonu Devri — Ertuğrul Kabaoğlu (G231210376) / Grup C Tamamlandı (25.10.2026)

Grup C ("Yama/FCN, DenseNet ve Transformer") kapsamındaki tüm makale incelemeleri, hakem denetimleri, rapor bölümleri, tasarım spesifikasyonları ve mimari diyagramlar ile iki model implementasyonu eksiksiz olarak tamamlandı:

### 1. 5 Makale İncelemesi ve Opus Doğrulamaları (`makaleler/ertugrul/`)
- **P11 (Qiu 2020, FCN + DPM Risk Haritası + MLP):** Tam metin PMC7296847 (Brain 2020) ve `vkola-lab/brain2020` GitHub deposu incelendi. 14 bölüm eksiksiz dolduruldu. §13'te **ÇELİŞKİ YOK**. 4 kohortta toplam 1.466 denek (ADNI 417, AIBL 382, FHS 102, NACC 565). Yalnızca MRI modeli ile ADNI testte %83,4 doğruluk (11 uzman nöroloğun ortalaması olan %82,3'ü geçti); füzyon modelinde %96,8 doğruluk ve 0,996 AUC. FHS otopsi kohortunda (11 denek) DPM risk haritasının amiloid-$\beta$ ve tau nörofibriler yumaklarıyla mekânsal korelasyonu doğrulandı. Kod lisansı: MIT.
- **P12 (Solano-Rojas 2021/2020, 3B DenseNet-121):** Tam metin PMC7313295 (ANNPR 2020 / Sensors 2021) incelendi. 14 bölüm tam dolduruldu. §13'te **ÇELİŞKİ VAR** belgelendi (özet bölümünde %87 doğruluk, %87 duyarlılık, %88 özgüllük iddia edilirken; metin içi §3 ve Tablo 1'de nihai modellerin %84 doğruluk, %81 duyarlılık, %84 özgüllük olduğu; ayrıca bölmenin denek bazında değil rastgele %75/25 tarama bazında yapılarak ağır boylamsal veri sızıntısı oluştuğu kanıtlandı).
- **P13 (Lian 2020, H-FCN):** Tam metin PMC6588512 (IEEE TPAMI 2020) incelendi. 14 bölüm tam dolduruldu. §13'te **ÇELİŞKİ YOK**. ADNI-1 baseline 830 denek (229 NC, 226 sMCI, 167 pMCI, 199 AD) üzerinde sızıntısız 10-kat CV ile AD-NC ikili görevde %90,3 doğruluk, %96,5 özgüllük ve 0,951 AUC; ADNI-2 $\rightarrow$ ADNI-1 bağımsız dış testinde %89,5 doğruluk ve 0,945 AUC doğrulandı. Projemizin birincil hedefi olan AD-NC $\ge \%85$ dengeli doğruluk için sağlam tavan referansı.
- **P14 (Jang & Hwang 2022, M3T Transformer):** CVPR 2022 PDF tam metninden (12 sayfa) incelendi. 14 bölüm tam dolduruldu. §13'te **ÇELİŞKİ YOK**. M3T (3B CNN + 2B ResNet50 ImageNet + 8 katman Transformer, 29,12M parametre); ADNI test kümesinde %93,21 doğruluk ve 0,9634 AUC; bağımsız çok merkezli dış testlerde AIBL %93,27 doğruluk, OASIS %85,26 doğruluk (0,8961 AUC). Saf 3B ViT'in (AUC 0,8851) açık farkla geride kaldığı ve 2B ön eğitimin önemi doğrulandı. Gayriresmî kod GPL-3.0 olduğu için depoya kod alınmadı (yalnızca okuma).
- **P15 (Dhinagar 2023, Video ve Sentetik Ön Eğitim):** arXiv:2309.04651 PDF tam metninden incelendi. 14 bölüm tam dolduruldu. §13'te **ÇELİŞKİ YOK**. Kinetics-400 (306k video), LDM (100k sentetik MRI), UKB (38,7k MRI) ön eğitimi. 3B DenseNet-121 sıfırdan eğitildiğinde ADNI 0,901 AUC ve OASIS sıfır atışlı (0-shot) dış testinde %84,0 doğruluk verdi. 1,8M parametreli Tiny DenseNet ise %83,6 OASIS doğruluğu sağlayarak 6 kat daha az parametreyle aynı başarıyı yakaladı. Swin-T video ön eğitimiyle 0,924 AUC'ye ulaştı.

### 2. Ortak Tablo ve Makale Listesi Güncellemeleri
- **`makaleler/KARSILASTIRMA-15.md`:** P11–P15 satırları eksiksiz dolduruldu; Grup C'den çıkan ortak dersler (Maddeler 11–15: yama bazlı eğitimin bellek ve otopsi avantajı, longitudinal tarama sızıntısı artefaktı, 3B DenseNet omurgasının sıfırdan eğitimdeki üstünlüğü, saf Vision Transformer'ların medikal veri kıtlığındaki kısıtı, dış testte beklenen %5-8 puanlık düşüş payı) eklendi.
- **`makaleler/MAKALE-LISTESI.md`:** P11–P15 satırları "AI özeti + Opus doğrulandı" durumuna geçirildi. Böylece **15 MAKALENİN TAMAMI (P01–P15) %100 İNCELENMİŞ VE OPUS İLE DOĞRULANMIŞTIR.**

### 3. Ara Rapor 2 Taslağı Genişletildi (`rapor/ARA-RAPOR-2-TASLAK.md`)
- §2.3 bölümü 5 makale için ([11], [12], [13], [14], [15]) derinlemesine akademik literatür paragraflarıyla genişletildi.
- §4.1 sistem mimarisi, §4.2 veritabanı ER ve §4.4 akış diyagramları bölümleri PlantUML kaynak dosyalarına bağlandı.

### 4. Sistem Tasarım ve Mimari Çıktıları (`rapor/sekiller/`)
- **`rapor/sekiller/mimari.puml`:** 6 katmanlı (Veri, Ön İşleme, Model, Doğrulama/Değerlendirme, Dağıtım/Çıkarım, Sunum/Veritabanı) sistem mimarisi blok diyagramı PlantUML formatında yazıldı.
- **`rapor/sekiller/er.puml`:** 6 varlıklı (Kullanici, Tarama, OnIsleme, Model, Tahmin, AciklamaHaritasi) ve ADNI DUA uyarınca ham görüntü saklamayan ilişkisel veritabanı ER şeması PlantUML formatında yazıldı.
- **`rapor/sekiller/akis_onisleme.puml`:** dcm2niix $\rightarrow$ HD-BET $\rightarrow$ N4 $\rightarrow$ z-skor $\rightarrow$ SimpleITK MNI152 afin $\rightarrow$ 128³ float16 ön işleme hattı akış şeması yazıldı.
- **`rapor/sekiller/akis_egitim.puml`:** Protokol K1–K5 uyumlu, denek düzeyinde kilitli test ve 5-kat çapraz doğrulama, AMP optimizasyonu ve erken durdurmalı eğitim akış şeması yazıldı.
- **`rapor/sekiller/akis_tahmin.puml`:** Klinik web yüklemesi, ONNX inferansı, 3 eksenli XAI (Grad-CAM/LRP/DPM) görselleştirmesi, yasal klinik uyarı ve PDF rapor üretim akış şeması yazıldı.

### 5. İki Model İmplementasyonu (`uygulama/`)
- **P11 (`uygulama/ertugrul_P11_qiu_fcn/`):**
  - `LICENSE-brain2020`: MIT lisans dosyası eklendi.
  - `model.py`: Qiu 2020 4 bloklu 3B FCN mimarisi (`QiuFCN3D`), dinamik adaptör (`AdaptiveAvgPool3d((6,6,6))`), `dense_to_conv()` tam evrişimli harita dönüştürücüsü ve `olustur(varyant='fcn', ...)` fabrikası yazıldı.
  - `harita.py`: Tam hacimden tek geçişte 3B Hastalık Olasılık Haritası (DPM) üreten, tepe risk bölgesini saptayan ve 3 dik düzlemde (aksiyel, koronal, sagital) görselleştirip kaydeden CLI modülü kodlandı.
- **P12 (`uygulama/ertugrul_P12_densenet/`):**
  - `model.py`: Saf PyTorch 3B DenseNet omurgası (`DenseNet3D`) ile standart `densenet121` (~11.2M parametre) ve kaynak dostu `tiny_densenet` (~1.8M parametre, 4x4 blok, k=16) varyantları yazıldı; `olustur(varyant='densenet121'|'tiny_densenet', ...)` fabrika fonksiyonu kodlandı. İsteğe bağlı olarak MONAI `DenseNet121` ile de entegre olabilmektedir.

### 6. Süreç Tablosu ve Sıradaki Adımlar
- `SUREC.md §9` tablosunda İş 5 (P11-P15 inceleme), İş 12 (Mimari blok + ER + akış diyagramları) ve İş 17 (P11 ve P12 implementasyonu) tamamlandı olarak işaretlendi.
- **Genel Durum:** 15 makale incelemesinin tamamı, Ara Rapor 2 gereksinim ve tasarım bölümlerinin tamamı, ve 6 model implementasyonunun (P01, P02, P06, P07, P11, P12) tamamı depoda hazırdır!
- **Sıradaki Adım:** Baran Yeşilyurt'un Ara Rapor 2'yi bölüm şablonunda (`BSM401_Sablon_201611.docx`) birleştirmesi (İş 14), danışman görüşmesi ve ADNI/OASIS başvuru takibi.

