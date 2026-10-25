# SÜREÇ — Ders, Takvim, İş Bölümü ve "Nerede Kaldık"

Son güncelleme: 25.10.2026 (Baran, Claude Code oturumu). Bu dosya ekibin tek "süreç" kaynağıdır; her iş bitince en alttaki tabloyu güncelleyin.

## 1. Dersin resmî çerçevesi (kaynaklı)
- **Ders:** BSM 401 Bilgisayar Mühendisliği Tasarımı (0+2, 5 AKTS), SAÜ Bilgisayar ve Bilişim Bilimleri Fakültesi, Bilgisayar Mühendisliği.
- **Bölüm sayfası (rapor yazım ilkeleri + şablonlar):** https://cs.sakarya.edu.tr/tr/icerik/24805/83709/tasarim-ve-bitirme
  - Rapor şablonu: `BSM401_Sablon_201611.docx` (Times New Roman; büyük başlık 14 pt kalın; kapak biçimi bozulmaz; sıra: Önsöz → İçindekiler → Simgeler ve Kısaltmalar → Şekiller → Tablolar → Özet → Bölüm 1 Giriş …).
  - Poster şablonu: `Poster_Formati22.pptx` · Dergi özeti biçimi: `Dergi_Ozet_Bicimi21.docx`.
  - İçerik ilkeleri: Özet geçmiş zaman + edilgen; Giriş = konu tanımı + önceki çalışmalar + yöntemler; Sonuç = hedefe ulaşma derecesi + güçlü/zayıf yönler.
- **Üniversite Bitirme Projeleri Yönergesi (Senato, 02.11.2023):** https://ogrdek.sakarya.edu.tr/sites/ogrdek.sakarya.edu.tr/file/Bitirme_Projeleri_Yonergesi_02.11_.2023_.pdf
  - Konu: karmaşık bir problemin çözümü / sistem tasarımı, yenilikçi yaklaşım, gerçekçi kısıtlar, takım çalışması (Madde 7).
  - Proje türü: TÜBİTAK 2209-A/B, AB, TÜSEB, bakanlık, Ar-Ge merkezli firma işbirliği türlerinden birine uygunluk aranır (Madde 8) → **danışmana sorulacak**.
  - Teslim: en geç yarıyıl sonu sınavlarının başladığı gün; geç teslim = proje yapılmamış sayılır (GR) (Madde 10).
  - Değerlendirme: en az 3 öğretim elemanlı komisyon önünde sözlü; ölçütler = dönem içi izlemeler, rapor biçimi, içerik niteliği (Madde 11). **Yüzdesel ağırlıklar yayında yok.**

## 2. Dört aşamalı ara rapor yapısı (danışmanın verdiği `Tasarim_ara_raporlar.docx`)
| Aşama | Ad | İçermesi gerekenler | Bizim durumumuz |
|---|---|---|---|
| 1 | **Proje Önerisi ve Planlama** | kapak · proje tanımı (amaç, kapsam, önem) · literatür özeti (5–10 kaynak) · teknik altyapı · zaman çizelgesi (Gantt) · beklenen sonuçlar | ✅ Konu formu teslim edildi (24.10.2026) |
| 2 | **Analiz ve Tasarım** ← **BURADAYIZ** | kapak · giriş (1. rapordan bu yana özet) · **detaylı literatür (10–15 kaynak)** · **gereksinim analizi** (işlevsel, işlevsel olmayan, use-case) · **tasarım** (sistem mimarisi blok diyagramı, veritabanı ER, arayüz mock-up, akış diyagramları) · güncellenmiş zaman çizelgesi | 🔄 Taslak: `rapor/ARA-RAPOR-2-TASLAK.md` |
| 3 | **Uygulama ve Geliştirme** | giriş · geliştirme ortamı · kod yapısı · algoritma/pseudocode · ekran görüntüleri · ön test sonuçları · problemler/çözümler · mühendislik standartları · değişiklik yönetimi · güncel plan | ⏳ 6 implementasyon + ortak protokol |
| 4 | **Sonuçlandırma ve Değerlendirme** | nihai mimari · yazılım yapısı · kapsamlı test/değerlendirme · sonuç/öneriler · kaynakça (APA/IEEE) · ekler | ⏳ Karşılaştırma tablosu + ONNX prototip |

**15 makale incelemesi = 2. aşamanın "detaylı literatür taraması" bölümü.** Her inceleme notu (`makaleler/<kişi>/P..md`) rapora doğrudan paragraf olarak girer.

## 3. Danışmanın sözlü şartları
1. 3 kişi × 5 makale = 15 makale incelenir (yapay zekâ ile yorumlatıp anlamak kabul).
2. Her kişi 2 makaleyi implemente eder (6 uygulama).
3. Tüm uygulamalar **ortak bir veri setinde** çalıştırılır ve aradaki fark raporlanır.

## 4. Resmî takvim 2026-2027 Güz (Öğrenci İşleri PDF'inden)
| Olay | Tarih |
|---|---|
| Güz öğretim başlangıcı | 21 Eylül 2026 |
| Ara sınavlar | 9–15 Kasım 2026 |
| Yarıyıl sonu | **27 Aralık 2026** |
| Final sınavları (rapor için yönergedeki en geç teslim = ilk gün) | **28 Aralık 2026 – 10 Ocak 2027** |
| Bütünleme | 18–24 Ocak 2027 |

**Bölümden / danışmandan öğrenilecek (yayında yok):** 2. ara rapor teslim tarihi · 3. ve 4. ara rapor tarihleri · sunum/poster günü · not ağırlıkları · benzerlik (intihal) sınırı · kaynak biçimi (IEEE mi APA mı) · sayfa sınırı · Madde 8 proje türü uygunluğu.

## 5. Haftalık iş takvimi (bugün 5. hafta; "varsayım" olanlar bölüm tarihiyle güncellenir)
| Hafta | Tarih | İş | Kim | Teslim/kilometre taşı |
|---|---|---|---|---|
| 5 | 24–30 Eki | Konu formu teslimi ✅ · ADNI başvurusu (danışman adıyla) · OASIS-1 erişim isteği · bölüme soru listesi · KURULUM.md ile ortam kurulumu | Baran (ADNI/OASIS), herkes (kurulum) | ADNI başvurusu gönderildi |
| 6 | 31 Eki – 6 Kas | 15 makale incelemesi (herkes kendi 5'i, şablonla) · gereksinim analizi taslağı | herkes | `makaleler/*/P..md` dolu |
| 7 | 7–13 Kas | Ön işleme hattı OASIS-1'de ayağa kalkar · RID düzeyi bölme dosyaları · Ara sınav haftası: hafif | Baran (hat), Görkem (use-case + arayüz mock-up), Ertuğrul (ER + akış diyagramları) | `onisleme/` çalışır |
| 8 | 14–20 Kas | **Ara Rapor 2** son hali (literatür + gereksinim + tasarım + takvim) · ortak eğitim harness'i | herkes / Baran | 📄 Ara Rapor 2 (tarih bölümden) |
| 9 | 21–27 Kas | ADNI geldiyse ön işleme ADNI'de · Baran'ın 2 modeli ilk sonuç · diğerleri kendi depolarını OASIS-1'de koşturur | herkes | ilk sonuç tablosu |
| 10 | 28 Kas – 4 Ara | 6 modelin tamamı ortak protokolde · XAI (LRP/Grad-CAM) çıktıları | herkes | `karsilastirma/SONUCLAR.md` dolu |
| 11 | 5–11 Ara | **Ara Rapor 3** (uygulama) · ONNX export + API prototipi · test senaryoları | Baran (ONNX/API), herkes (rapor) | 📄 Ara Rapor 3 (varsayım) |
| 12 | 12–18 Ara | Rapor taslağı BSM401 şablonunda · poster taslağı · danışman geri bildirimi | herkes | taslak |
| 13 | 19–25 Ara | **Ara Rapor 4 / final rapor** son hali · benzerlik kontrolü · danışman onayı | herkes | 📄 Final rapor |
| 14 | 26–28 Ara | Teslim (**28 Aralık son gün**) | Baran | ✅ teslim |
| Final | 28 Ara – 10 Oca | Komisyon önünde sunum (gün bölümden) | herkes | sunum |

## 6. İş bölümü
| Kişi | Grup / tema | Makaleler | İmplemente | Ek sorumluluk |
|---|---|---|---|---|
| **Baran Yeşilyurt** | A — 3B CNN temelleri, ResNet, tekrarlanabilir protokol | P01–P05 | P01 (ResNet/VoxCNN), P02 (MedicalNet ResNet-18) | ortak veri seti, ADNI/OASIS başvurusu, ön işleme hattı, PROTOKOL, ortak eğitim kodu, ONNX/API, Git deposu |
| **Ahmet Görkem Yavuz** | B — dikkat ve açıklanabilirlik | P06–P10 | P06 (CNN+LRP), P07 (ResAttNet+Grad-CAM) | gereksinim analizi, use-case diyagramı, arayüz mock-up'ları, XAI görselleri |
| **Ertuğrul Kabaoğlu** | C — yama/FCN, DenseNet, Transformer | P11–P15 | P11 (FCN yama), P12 (DenseNet121) | sistem mimarisi blok diyagramı, veritabanı ER tasarımı, akış diyagramları, Gantt |

Rapor bölümleri: Giriş (Baran) · Literatür (herkes, kendi 5'i) · Gereksinim (Görkem) · Tasarım (Ertuğrul + Görkem) · Takvim (Ertuğrul) · Birleştirme ve biçim (Baran).

## 7. Danışmana sorulacaklar (ilk görüşmede, sırayla)
1. **Hedef metrik:** Literatürde sızıntısız sonuçlarda ≥%85 yalnızca **AD vs NC** ikili görevde gerçekçi; üç sınıf (NC/MCI/AD) sMRI ile çok daha düşük (dış testte ~%50–60, Folego 2020). Wen 2020'de (en sıkı protokol) tek 3B CNN + başlangıç görüntüsü ADNI testte **0.82**, hipokampüs ROI **0.89**, doğrusal SVM **0.88** dengeli doğruluk. Öneri: birincil hedef AD-NC ≥%85 (dengeli doğruluk), üç sınıf ikincil ve dürüst raporlanır; hedefe ulaşmak için 6 modele ek olarak hipokampüs-ROI kolu ve SVM temel çizgisi de koşulur. Kabul eder mi?
2. ADNI başvurusunu danışman adıyla yapabilir miyiz (kurumsal e-posta, üç öğrenci ekip üyesi)? Taslak aşağıda.
3. 2., 3., 4. ara rapor ve sunum/poster tarihleri; kaynak biçimi (IEEE öneriyoruz); sayfa sınırı; benzerlik sınırı.
4. Yönerge Madde 8 proje türü: TÜBİTAK 2209-A başvurusu yapmamızı ister mi?
5. Karar destek "prototipi" beklentisi: basit web arayüzü (yükle → tahmin + ısı haritası) yeterli mi, yoksa DICOM görüntüleyici entegrasyonu mu?
6. Ortak veri setinin ekip içinde paylaşımı: DUA gereği ham veri dağıtılamıyor; herkes kendi IDA hesabıyla mı indirsin, yoksa ön işlenmiş tensörler mi paylaşılsın (ADNI'ye sorulacak)?
7. **Hesaplama bütçesi (kritik):** tam protokol 9 model × 2 görev × 5 kat × 3 tohum = **270 koşu ≈ 270–540 GPU-saat**; elimizdeki ücretsiz bütçe 3 hesap × ~30 GPU-saat/hafta × 8 hafta ≈ 720 saat tavan, hata payı yok. Öneri: birincil görevde (AD-NC) 5 kat × 3 tohum korunur, **ikincil üç sınıf görevinde 5 kat × 1 tohum** koşulur ve raporda açıkça yazılır; LR taraması yalnız kat 0'da yapılır. Kabul eder mi? Bölümün GPU sunucusu/kümesi kullanıma açık mı? Hesap ve öncelik katmanları: `karsilastirma/KOSU-PLANI.md`.

## 8. ADNI başvurusu için danışmana e-posta taslağı
> Sayın Hocam,
>
> BSM 401 Tasarım dersi kapsamında "Alzheimer Hastalığının Erken Teşhisi İçin 3B Derin Öğrenme Tabanlı Karar Destek Sistemi" projemiz için ADNI (Alzheimer's Disease Neuroimaging Initiative) verisine erişim gerekiyor. ADNI, başvuruda kurumsal bağlılık ve araştırma amacı aradığı için başvurunun sizin adınıza (kurumsal e-posta ile) yapılması, bizim de ekip üyesi olarak eklenmemiz en güvenli yol görünüyor. İnceleme süresi yaklaşık iki hafta olduğundan bu hafta göndermeyi hedefliyoruz.
>
> Adımlar: (1) https://ida.loni.usc.edu adresinde hesap açılır, (2) "ADNI" için Data Use Agreement kabul edilir, (3) başvuru formunda amaç olarak lisans tasarım projesi, kullanılacak veri olarak "ADNI1 1.5T T1 sMRI başlangıç taramaları ve NC/MCI/AD tanı etiketleri (ADNIMERGE)" yazılır, (4) ekip üyeleri: Ahmet Görkem Yavuz, Ertuğrul Kabaoğlu, Baran Yeşilyurt.
>
> Onay beklerken boru hattımızı OASIS-1 açık veri setiyle kuruyoruz. Uygun görürseniz başvuru metnini birlikte doldurabiliriz.
>
> Saygılarımla, Baran Yeşilyurt (G231210078)

## 9. NEREDE KALDIK (her iş bitince güncelle)
| # | İş | Kim | Durum | Son güncelleme | Not |
|---|---|---|---|---|---|
| 1 | Konu formu | ekip | ✅ bitti | 24.10 | form Baran.Deneme'de |
| 2 | 15 makale seçimi + gruplama | Baran (Claude) | ✅ bitti | 25.10 | `makaleler/MAKALE-LISTESI.md` |
| 3 | P01–P05 inceleme (AI + Opus doğrulama) | Baran (Claude) | ✅ bitti (insan okuması ☐) | 25.10 | `makaleler/baran/` 5 not, §13 doğrulamalı; P03 PDF'den okundu |
| 4 | P06–P10 inceleme | Görkem | ☐ başlamadı | — | `devir/DEVIR-GORKEM.md` |
| 5 | P11–P15 inceleme | Ertuğrul | ☐ başlamadı | — | `devir/DEVIR-ERTUGRUL.md` |
| 6 | ADNI başvurusu | Baran + danışman | ☐ başlamadı | — | e-posta taslağı §8 |
| 7 | OASIS-1 erişim isteği (**her üye kendi adına**, kurumsal e-posta + araştırma açıklaması) | herkes | ☐ başlamadı | — | https://sites.wustl.edu/oasisbrains/home/access/ · DUA paylaşımı yasaklar |
| 7b | ADNI'ye Baran'ın kendi başvurusu (danışmanınkiyle paralel) + OpenNeuro ds007561 kontrolü + IXI indirme (kod testi) | Baran | ☐ başlamadı | — | `veri/VERI-SETI.md §2b` |
| 8 | Ortam kurulumu (kendi PC) | herkes | 🔄 Baran: ✅ kuruldu, 3 test takımı yeşil (CPU torch) | 25.10 | `KURULUM.md` · GPU için cu126 ile yeniden kurulacak · **Görkem/Ertuğrul henüz kurmadı** |
| 8b | Git deposu + GitHub + CI | Baran | ✅ bitti | 25.10 | https://github.com/YesilBaraN/tasarim-alzheimer (public) · her push'ta Windows+Linux uçtan uca test, iki koşu da yeşil · koşu kayıtlarına commit hash'i düşüyor |
| 9 | Ön işleme hattı (OASIS-1'de) | Baran | ☐ kod hazır, **duman testi yeşil** (sentetik) | 25.10 | `onisleme/onisle.py` · gerçek MRI, HD-BET ve MNI kaydı henüz denenmedi |
| 10 | PROTOKOL + ortak eğitim kodu | Baran | ✅ kod hazır ve **uçtan uca koştu** (7 denetim + 4 çalışma zamanı hatası düzeltildi) | 25.10 | `uygulama/ortak/` · düzeltmeler ve doğrulama tablosu `DEVAM.md` |
| 11 | Gereksinim analizi + use-case | Görkem | ☐ taslak var | 25.10 | `rapor/ARA-RAPOR-2-TASLAK.md §3` |
| 12 | Mimari blok + ER + akış diyagramları | Ertuğrul | ☐ taslak var | 25.10 | `rapor/ARA-RAPOR-2-TASLAK.md §4` |
| 13 | Arayüz mock-up'ları | Görkem | ☐ başlamadı | — | §4.3 ekran listesi |
| 14 | Ara Rapor 2 birleştirme | Baran | ☐ başlamadı | — | BSM401 şablonu |
| 15 | Baran implementasyonu P01, P02 | Baran | ☐ iskelet hazır | 25.10 | `uygulama/baran_*` |
| 16 | Görkem implementasyonu P06, P07 | Görkem | ☐ başlamadı | — | |
| 17 | Ertuğrul implementasyonu P11, P12 | Ertuğrul | ☐ başlamadı | — | |
| 18 | Karşılaştırma tablosu | ekip | ☐ şablon + üreteci hazır | 25.10 | `karsilastirma/SONUCLAR.md` · üreteç `tablo_uret.py` (protokole uymayan koşuyu ayıklar) |
| 18b | Koşu planı / GPU bütçesi | Baran | ✅ plan hazır, danışman onayı bekliyor | 25.10 | `karsilastirma/KOSU-PLANI.md` · §7 soru 7 |
| 18c | Sağlık testleri (PROTOKOL K5) | Baran | ✅ koştu, yeşil | 25.10 | `uygulama/ortak/saglik_testi.py` — ayrılabilir 1.000 / rastgele 0.500 |
| 18d | Dış test + SVM temel çizgisi koşucuları | Baran | ✅ ikisi de koştu (sentetik) | 25.10 | `uygulama/ortak/dis_test.py` (K4 koruması dahil), `svm_kos.py` |
| 19 | ONNX + API prototipi | Baran | 🔄 çıkarım zinciri **uçtan uca çalıştı** (sentetik modelle) | 25.10 | `onnx_disa_aktar.py` (uyum True, fark 1.9e-06) + `api/tahmin.py` · FastAPI, ısı haritası, kalibrasyon yapılacak |
| 20 | Danışman soruları (§7) | Baran | ☐ başlamadı | — | ilk görüşme |
