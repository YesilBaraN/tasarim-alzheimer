# 2. ARA RAPOR — Analiz ve Tasarım (TASLAK)

Danışmanın verdiği `Tasarim_ara_raporlar.docx` yapısı birebir izlenmiştir. Biçim: `BSM401_Sablon_201611.docx` (Times New Roman, başlık 14 pt). Kaynak gösterme: IEEE (danışman aksini söylerse APA). Bu md, Word'e aktarılacak **içerik taslağıdır**; `[…]` içindekiler doldurulacak yerlerdir.

---

## KAPAK
**Proje adı:** Alzheimer Hastalığının Erken Teşhisi İçin 3B Derin Öğrenme Tabanlı Karar Destek Sistemi Geliştirilmesi
**Öğrenciler:** Ahmet Görkem Yavuz (G231210032) · Ertuğrul Kabaoğlu (G231210376) · Baran Yeşilyurt (G231210078)
**Danışman:** Dr. Öğr. Üyesi Can Yüzkollar
**Ders:** BSM 401 Bilgisayar Mühendisliği Tasarımı — 2026-2027 Güz
**Teslim tarihi:** [bölümden öğrenilecek]

---

## 1. GİRİŞ — Birinci ara rapordan bu yana yapılanlar
- Konu ve danışman formu teslim edildi (24.10.2026).
- Literatürde 27 aday makale tarandı; açık erişim ve açık kod ölçütüyle 15 makale seçildi, üç tematik gruba ayrıldı ve ekip üyelerine atandı (`makaleler/MAKALE-LISTESI.md`).
- Ortak veri seti kararı verildi: ADNI1 1.5T T1 başlangıç taramaları (NC/MCI/AD); ADNI başvurusu danışman adıyla başlatıldı; köprü veri seti olarak OASIS-1 seçildi.
- Ön işleme hattı, adil karşılaştırma protokolü ve ortak eğitim altyapısı tasarlandı (`onisleme/`, `uygulama/PROTOKOL.md`, `uygulama/ortak/`).
- [Danışman görüşmesi sonucu: hedef metrik kararı (AD-NC ≥%85 birincil, üç sınıf ikincil)]

## 2. DETAYLI LİTERATÜR TARAMASI (15 kaynak)
> Her alt bölüm, ilgili `makaleler/<kişi>/P..md` notunun §2 (özet), §8 (sonuçlar) ve §11 (güçlü/zayıf) bölümlerinden 1–2 paragraf olarak yazılır. Sonunda tek bir karşılaştırma tablosu (`makaleler/KARSILASTIRMA-15.md`) verilir.

### 2.1 Üç boyutlu CNN temelleri ve ResNet omurgası (Baran)
- **[1] Korolev vd. 2017** — VoxCNN ve 3B ResNet'in ADNI'de karşılaştırılması; küçük veri (231 denek) ve AD-NC ≈ %80. [P01 notundan]
- **[2] Chen vd. 2019 (Med3D/MedicalNet)** — 23 veri setinde ön eğitilmiş 3B ResNet; transfer öğrenmeyle hızlı yakınsama. [P02]
- **[3] Wen vd. 2020** — 32 çalışmanın derlemesi, 4 veri sızıntısı türü, 3B denek/ROI/yama/2B karşılaştırması; sızıntısız AD-CN dengeli doğruluk 0.76–0.89. [P03]
- **[4] Folego vd. 2020** — Tüm beyin 3B CNN (ADNet), ANTs→MNI152 ön işleme, dış test CADDementia'da üç sınıf %52. [P04]
- **[5] Yagis vd. 2021** — Dilim düzeyi bölmenin doğruluğu %29–55 şişirdiğinin deneysel kanıtı. [P05]

### 2.2 Dikkat mekanizmaları ve açıklanabilirlik (Görkem)
- **[6] Böhle vd. 2019** — LRP ile 3B CNN kararlarının açıklanması. [P06]
- **[7] Zhang vd. 2021** — 3D ResAttNet: artık öz-dikkat + Grad-CAM ile atrofi yerelleştirme. [P07]
- **[8] Dyrba vd. 2021** — İlgi haritalarının etkileşimli görselleştirilmesi; [sonuç değerleri P08 incelemesinde doğrulanacak]. [P08]
- **[9] Hoang vd. 2023** — Çift dikkat modüllü tekrarlanabilir 3B CNN; dış test OASIS/AIBL. [P09]
- **[10] Jin vd. 2020** — 3DAN: genellenebilir ve nörobilimsel olarak yorumlanabilir biyobelirteçler. [P10]

### 2.3 Yama/FCN, DenseNet ve Transformer (Ertuğrul)
- **[11] Qiu vd. 2020** — FCN ile yama düzeyi risk haritası + MLP; dört kohortta doğrulama. [P11]
- **[12] Solano-Rojas & Villalón-Fonseca 2021** — Düşük maliyetli 3B DenseNet. [P12]
- **[13] Lian vd. 2020** — H-FCN: hiyerarşik tam evrişimli ağ, ADNI-1→ADNI-2 AD-NC 0.903. [P13]
- **[14] Jang & Hwang 2022** — M3T: 3B CNN + 2B CNN + Transformer; çok merkezli doğrulama. [P14]
- **[15] Dhinagar vd. 2023** — Video/sentetik MRI ön eğitimi; ViT ve CNN karşılaştırması; denek bazlı katmanlar. [P15]

### 2.4 Literatürden çıkan tasarım kararları
1. Bölme **denek (RID) düzeyinde** yapılır; aksi hâlde sonuçlar %30'a varan oranda şişer [3], [5].
2. ≥%85 doğruluk hedefi **AD vs NC** görevinde gerçekçidir; üç sınıf ikincil görev olarak raporlanır [3], [4].
3. Altı mimari **aynı ön işleme ve aynı protokolle** karşılaştırılır (`uygulama/PROTOKOL.md`); bu, literatürde eksik olan "ortak protokolle yan yana karşılaştırma" boşluğunu doldurur.
4. Açıklanabilirlik (LRP/Grad-CAM) karar destek sisteminin parçasıdır [6], [7], [8].

## 3. GEREKSİNİM ANALİZİ

### 3.1 İşlevsel gereksinimler
| No | Gereksinim | Öncelik |
|---|---|---|
| FR-1 | Sistem, T1 ağırlıklı 3B MRI'ı NIfTI (.nii/.nii.gz) veya DICOM klasörü olarak kabul eder | Zorunlu |
| FR-2 | Ön işleme hattı (kafatası ayıklama, N4, normalizasyon, MNI152 hizalama, 128³ yeniden boyutlandırma) otomatik çalışır ve her adımın çıktısı kaydedilir | Zorunlu |
| FR-3 | Eğitilmiş model için AD / MCI / NC olasılıkları ve ikili AD-NC kararı üretilir | Zorunlu |
| FR-4 | Karar için açıklanabilirlik haritası (Grad-CAM veya LRP) üretilir ve MRI üzerine bindirilerek gösterilir | Zorunlu |
| FR-5 | Altı model aynı veri ve protokolle eğitilip sonuçları tek tabloda karşılaştırılır | Zorunlu |
| FR-6 | En iyi model ONNX olarak dışa aktarılır ve onnxruntime ile PyTorch'suz çalıştırılır | Zorunlu |
| FR-7 | REST API (`POST /tahmin`) ile görüntü gönderilip JSON sonuç alınır | Zorunlu |
| FR-8 | Web arayüzü: görüntü yükle → sonuç + ısı haritası + güven skoru + rapor indir (PDF) | İstenen |
| FR-9 | Tahmin kayıtları (meta veri, sonuç, model sürümü, zaman) veritabanında saklanır | İstenen |
| FR-10 | Kullanıcı girişi ve rol (radyolog / araştırmacı / yönetici) | İsteğe bağlı |

### 3.2 İşlevsel olmayan gereksinimler
| No | Gereksinim | Ölçüt |
|---|---|---|
| NFR-1 | **Performans (model):** AD-NC testinde doğruluk ≥%85, AUC ≥0.90; üç sınıfta dengeli doğruluk raporlanır | PROTOKOL ile ölçülür |
| NFR-2 | **Yanıt süresi:** tek görüntü için ön işleme + tahmin ≤ 5 dk CPU'da, ≤ 30 sn GPU'da | ölçülecek |
| NFR-3 | **Tekrarlanabilirlik:** sabit tohum, kayıtlı bölme listeleri, sürüm sabitlenmiş `requirements.txt` | kontrol listesi |
| NFR-4 | **Güvenlik / gizlilik:** ADNI DUA'ya uyum; ham görüntü sunucuda kalıcı saklanmaz; kimlik bilgisi tutulmaz; HTTPS | tasarım kararı |
| NFR-5 | **Taşınabilirlik:** Windows/Linux, GPU'lu veya GPU'suz; ONNX ile çerçeveden bağımsız | test |
| NFR-6 | **Açık kaynak:** yalnızca MIT/Apache/BSD bileşenler; GPL kod türetilmez | envanter tablosu |
| NFR-7 | **Kullanılabilirlik:** radyolog 3 tıkla sonuç alır; sonuç ekranı "karar desteği, tanı değildir" uyarısı taşır | kullanıcı testi |
| NFR-8 | **Bakım:** modüler kod (ortak veri/metrik/eğitim), her model ayrı klasörde, Git ile sürüm | yapı |

### 3.3 Kullanım senaryoları (use-case)
**Aktörler:** Radyolog/klinisyen (birincil), Araştırmacı (model eğitimi/karşılaştırma), Sistem yöneticisi.
| UC | Ad | Aktör | Özet akış |
|---|---|---|---|
| UC-1 | MRI yükle ve tahmin al | Radyolog | NIfTI/DICOM seç → ön işleme → model → olasılıklar + karar |
| UC-2 | Açıklama haritasını incele | Radyolog | UC-1 sonrası ısı haritası katmanını aç/kapat, dilimler arasında gez |
| UC-3 | Rapor üret | Radyolog | Sonuç + harita + model sürümü → PDF |
| UC-4 | Modelleri eğit ve karşılaştır | Araştırmacı | veri seti seç → protokol → 6 model → SONUCLAR tablosu |
| UC-5 | Model yayınla | Araştırmacı | en iyi modeli ONNX'e aktar → API'ye bağla |
| UC-6 | Kullanıcı/rol yönet | Yönetici | kullanıcı ekle, rol ata |
> **Diyagram:** UC-1…UC-6 ile üç aktörü gösteren tek use-case diyagramı (Görkem çizer; draw.io veya PlantUML, PNG olarak `rapor/sekiller/usecase.png`).

## 4. TASARIM

### 4.1 Sistem mimarisi (blok diyagram)
Katmanlar, soldan sağa:
1. **Veri katmanı:** ADNI / OASIS-1 ham NIfTI (dış disk, depoya girmez) → `bolme.py` ile RID düzeyi kilitli test + 5 kat → `veri/bolme/`. Klinik sütunlu bölme CSV'leri yerelde kalır; depoya yalnız klinik veri taşımayan `<set>_bolme_haritasi.csv` girer (ADNI DUA).
2. **Ön işleme katmanı (`onisleme/onisle.py`):** dcm2niix → HD-BET → N4 (SimpleITK) → z-score → MNI152 afin (SimpleITK/TemplateFlow) → 128³ float16 `.npy`.
3. **Model katmanı (`uygulama/`):** ortak `veri.py` (Dataset/artırma) + `egit.py` (döngü, AMP, kesintiden devam, LR taraması) + 6 model klasörü (ResNet, MedicalNet-ResNet18, CNN+LRP, ResAttNet, FCN-yama, DenseNet121) + iki temel çizgi (`ortak/model.py` sığ 3B CNN, `svm_kos.py` voksel SVM) → `metrikler.py`.
4. **Doğrulama ve raporlama katmanı:** `saglik_testi.py` (PROTOKOL K5: rastgele etiket ≈ 0.5, ayrılabilir sınıf ≈ 1.0, bölme kesişimi boş), `dis_test.py` (başka sette sıfır-atış, K4 kontrollü), `tablo_uret.py` (kayıt JSON'ları → `karsilastirma/SONUCLAR.md`; protokole uymayan koşuları ayıklar, hiperparametre seçimini doğrulama üstünden yapar).
5. **Dağıtım katmanı:** `onnx_disa_aktar.py` → `model.onnx` (sabit 1×1×128³) → `uygulama/api/tahmin.py` (`KararDestek` sınıfı: ön işleme + onnxruntime + softmax; eğitim/servis uyumu için ön işlemeyi `onisle.py`'den çağırır) → FastAPI sarmalayıcısı (`POST /tahmin`, `GET /saglik`).
6. **Sunum katmanı:** web arayüzü (yükle, sonuç, ısı haritası, PDF) → veritabanı (tahmin kayıtları).
> **Diyagram:** 6 blok + oklar + yanında kullanılan teknoloji etiketi (Ertuğrul çizer; `rapor/sekiller/mimari.png`).

### 4.2 Veritabanı tasarımı (ER)
ADNI/OASIS görüntüleri veritabanına **konmaz** (DUA). Yalnızca meta veri ve tahmin kayıtları tutulur (SQLite ile başlanır, PostgreSQL'e taşınabilir).
| Varlık | Alanlar (PK kalın) | İlişki |
|---|---|---|
| Kullanici | **kullanici_id**, ad, e_posta, rol, parola_hash, olusturma | 1—N Tahmin |
| Tarama | **tarama_id**, kaynak (ADNI/OASIS/klinik), dis_kimlik (RID/OASIS id, anonim), cekim_tarihi, alan_gucu, dosya_hash, yuklenme | 1—N Tahmin, 1—1 OnIsleme |
| OnIsleme | **onisleme_id**, tarama_id, surum, kafatasi_arac, n4, normalizasyon, kayit_sablonu, cikti_boyutu, sure_sn, durum | N—1 Tarama |
| Model | **model_id**, ad (P01…P12), mimari, egitim_veri, protokol_surumu, onnx_yolu, egitim_tarihi, test_bacc, test_auc | 1—N Tahmin |
| Tahmin | **tahmin_id**, tarama_id, model_id, kullanici_id, p_nc, p_mci, p_ad, karar, guven, isi_haritasi_yolu, sure_sn, zaman | N—1 hepsi |
| Rapor | **rapor_id**, tahmin_id, pdf_yolu, olusturma | 1—1 Tahmin |
> **Diyagram:** 6 varlıklı ER (Ertuğrul; `rapor/sekiller/er.png`).

### 4.3 Arayüz prototipleri (mock-up listesi)
| Ekran | İçerik |
|---|---|
| E1 Giriş | e-posta/parola, rol |
| E2 Yükle | sürükle-bırak NIfTI/DICOM, hasta kimliği (anonim), "Analiz et" |
| E3 İşleniyor | adım adım ilerleme (ayıklama → N4 → kayıt → tahmin) |
| E4 Sonuç | olasılık çubukları (NC/MCI/AD), ikili karar + güven, **"Karar desteğidir, tanı değildir"** uyarısı, model sürümü |
| E5 Isı haritası | eksenel/koronal/sagittal dilim kaydırıcı, Grad-CAM/LRP katmanı şeffaflık ayarı |
| E6 Rapor | PDF önizleme, indir |
| E7 Model karşılaştırma (araştırmacı) | SONUCLAR tablosu, ROC eğrileri, karışıklık matrisleri |
> Görkem çizer (Figma/Balsamiq/draw.io, PNG). Teknoloji: ilk sürümde Streamlit veya basit HTML+FastAPI (açık kaynak, hızlı).

### 4.4 Akış diyagramları
- **A1 Ön işleme akışı:** NIfTI/DICOM → (DICOM ise dcm2niix) → HD-BET maske → N4 → maske içi z-score → MNI152 afin → 128³ kırpma/yeniden örnekleme → kalite kontrol (boş hacim? oryantasyon?) → `.npy` + meta JSON.
- **A2 Eğitim/değerlendirme akışı:** bölme CSV → 5 kat × 3 tohum döngüsü → eğitim (AMP, erken durdurma) → doğrulama metrikleri → test metrikleri → tablo + ROC + karışıklık matrisi → SONUCLAR.md.
- **A3 Tahmin akışı (üretim):** API isteği → doğrulama → ön işleme (A1) → onnxruntime → softmax → karar eşiği → ısı haritası → DB kaydı → JSON/PDF.
> Ertuğrul çizer (`rapor/sekiller/akis_*.png`).

## 5. GÜNCELLENMİŞ ZAMAN ÇİZELGESİ (Gantt)
| İş | H5 | H6 | H7 | H8 | H9 | H10 | H11 | H12 | H13 | H14 |
|---|---|---|---|---|---|---|---|---|---|---|
| ADNI/OASIS başvuru | █ | █ | | | | | | | | |
| 15 makale incelemesi | | █ | █ | | | | | | | |
| Gereksinim + use-case | | █ | █ | | | | | | | |
| Mimari + ER + akış + mock-up | | | █ | █ | | | | | | |
| **Ara Rapor 2** | | | | █ | | | | | | |
| Ön işleme hattı (OASIS→ADNI) | | | █ | █ | █ | | | | | |
| 6 model eğitimi + karşılaştırma (T0→T4, `karsilastirma/KOSU-PLANI.md`) | | | | █ | █ | █ | | | | |
| XAI + ONNX + API + arayüz | | | | | | █ | █ | | | |
| **Ara Rapor 3** | | | | | | | █ | | | |
| Rapor + poster + final | | | | | | | | █ | █ | █ |
Haftalar: H5 = 24–30 Eki 2026 … H14 = 26–28 Ara 2026 (28 Aralık son teslim). Ayrıntı `SUREC.md §5`.

**Kaynak kısıtı (gerçekçi kısıt — yönerge Madde 7):** tam protokol (9 model × 2 görev × 5 kat × 3 tohum = 270 koşu, 270–540 GPU-saat) ücretsiz hesaplama bütçesine (Kaggle ~30 GPU-saat/hafta/hesap, 3 hesap) sığmaz. Bu yüzden koşular T0–T4 öncelik katmanlarına bölündü: birincil görevde (AD-NC) 5 kat × 3 tohum korunur, ikincil üç sınıf görevinde 5 kat × 1 tohum koşulur ve bu raporda açıkça belirtilir. Hesap ve komut sırası `karsilastirma/KOSU-PLANI.md`'de.

## KAYNAKLAR (IEEE — 15 makale, `MAKALE-LISTESI.md` sırasıyla)
[1] S. Korolev, A. Safiullin, M. Belyaev, Y. Dodonova, "Residual and plain convolutional neural networks for 3D brain MRI classification," *IEEE ISBI*, 2017.
[2] S. Chen, K. Ma, Y. Zheng, "Med3D: Transfer learning for 3D medical image analysis," arXiv:1904.00625, 2019.
[3] J. Wen et al., "Convolutional neural networks for classification of Alzheimer's disease: Overview and reproducible evaluation," *Med. Image Anal.*, vol. 63, 2020.
[4] G. Folego et al., "Alzheimer's disease detection through whole-brain 3D-CNN MRI," *Front. Bioeng. Biotechnol.*, vol. 8, 2020.
[5] E. Yagis et al., "Effect of data leakage in brain MRI classification using 2D convolutional neural networks," *Sci. Rep.*, vol. 11, 2021.
[6] M. Böhle et al., "Layer-wise relevance propagation for explaining deep neural network decisions in MRI-based Alzheimer's disease classification," *Front. Aging Neurosci.*, vol. 11, 2019.
[7] X. Zhang et al., "An explainable 3D residual self-attention deep neural network for joint atrophy localization and Alzheimer's disease diagnosis using structural MRI," *IEEE J. Biomed. Health Inform.*, 2021.
[8] M. Dyrba et al., "Improving 3D convolutional neural network comprehensibility via interactive visualization of relevance maps: evaluation in Alzheimer's disease," *Alzheimer's Res. Ther.*, 2021.
[9] G. M. Hoang et al., "A reproducible 3D convolutional neural network with dual attention module (3D-DAM) for Alzheimer's disease classification," arXiv:2310.12574, 2023.
[10] D. Jin et al., "Generalizable, reproducible, and neuroscientifically interpretable imaging biomarkers for Alzheimer's disease," *Adv. Sci.*, 2020.
[11] S. Qiu et al., "Development and validation of an interpretable deep learning framework for Alzheimer's disease classification," *Brain*, vol. 143, 2020.
[12] B. Solano-Rojas, R. Villalón-Fonseca, "A low-cost three-dimensional DenseNet neural network for Alzheimer's disease early discovery," *Sensors*, vol. 21, 2021.
[13] C. Lian et al., "Hierarchical fully convolutional network for joint atrophy localization and Alzheimer's disease diagnosis using structural MRI," *IEEE TPAMI*, vol. 42, 2020.
[14] J. Jang, D. Hwang, "M3T: Three-dimensional medical image classifier using multi-plane and multi-slice transformer," *CVPR*, 2022.
[15] N. J. Dhinagar et al., "Video and synthetic MRI pre-training of 3D vision architectures for neuroimage analysis," arXiv:2309.04651, 2023.
[16] ADNI, "Alzheimer's Disease Neuroimaging Initiative — Data Use Agreement," https://adni.loni.usc.edu
[17] D. S. Marcus et al., "Open Access Series of Imaging Studies (OASIS): Cross-sectional MRI data in young, middle aged, nondemented, and demented older adults," *J. Cogn. Neurosci.*, 2007.
[18] M. J. Cardoso et al., "MONAI: An open-source framework for deep learning in healthcare," arXiv:2211.02701, 2022.
[19] F. Isensee et al., "Automated brain extraction of multisequence MRI using artificial neural networks," *Hum. Brain Mapp.*, 2019. (HD-BET)
[20] N. J. Tustison et al., "N4ITK: Improved N3 bias correction," *IEEE TMI*, 2010.
