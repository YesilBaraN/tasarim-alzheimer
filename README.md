# Alzheimer Erken Teşhisi — 3B Derin Öğrenme Karar Destek Sistemi

[![testler](https://github.com/YesilBaraN/tasarim-alzheimer/actions/workflows/testler.yml/badge.svg)](https://github.com/YesilBaraN/tasarim-alzheimer/actions/workflows/testler.yml)

**Depo:** https://github.com/YesilBaraN/tasarim-alzheimer
**Ders:** BSM 401 Bilgisayar Mühendisliği Tasarımı · Sakarya Üniversitesi, Bilgisayar Mühendisliği · 2026-2027 Güz
**Danışman:** Dr. Öğr. Üyesi Can Yüzkollar
**Ekip:** Ahmet Görkem Yavuz (G231210032) · Ertuğrul Kabaoğlu (G231210376) · Baran Yeşilyurt (G231210078)

## Tek paragrafta proje
ADNI veri tabanından T1 ağırlıklı 3B yapısal MRI (sMRI) ve NC / MCI / AD klinik etiketleriyle ortak bir veri seti kurulur; görüntülere kafatası ayıklama, N4 bias düzeltme, yoğunluk normalizasyonu ve MNI152 hizalama uygulanır; 3D-ResNet başta olmak üzere altı farklı 3B derin öğrenme mimarisi aynı veri ve aynı protokolle eğitilip karşılaştırılır; en iyi model ONNX / Python API olarak paketlenip radyoloji yazılımına eklenebilir bir karar destek prototipine dönüştürülür.

## Danışmanın şartı
- Her öğrenci **5 makale** inceler (toplam 15), **2'sini implemente eder** (toplam 6).
- Altı uygulama **aynı ortak veri setinde** karşılaştırılır; aradaki fark raporlanır.
- Makaleleri yapay zekâ ile yorumlatarak anlamak kabul edilir; önemli olan anlamak ve uygulamak.

## Klasör haritası
| Yol | Ne var |
|---|---|
| `SUREC.md` | Dersin resmî süreci, takvim, danışmana sorulacaklar, iş bölümü, **NEREDE KALDIK** tablosu |
| `KURULUM.md` | Kendi bilgisayarında ortam kurulumu (GPU'lu / GPU'suz), ilk 10 dakikada ne koşulur, açık kaynak lisans tablosu |
| `DEVAM.md` | Son oturumun devir notu (en son ne yapıldı, sıradaki iş) |
| `makaleler/MAKALE-LISTESI.md` | 15 makale: kim, hangi grup, tam metin linki, kod deposu ve lisansı, durum |
| `makaleler/SABLON-MAKALE-INCELEME.md` | Herkesin kullandığı tek inceleme şablonu |
| `makaleler/baran/`, `gorkem/`, `ertugrul/` | Kişi başına 5 inceleme notu (P01–P15) |
| `makaleler/KARSILASTIRMA-15.md` | 15 makalenin tek tabloda özeti |
| `veri/VERI-SETI.md` | Ortak veri seti kararı, ADNI başvurusu, OASIS-1 köprü seti, etiket ve bölme kuralları |
| `onisleme/` | Ön işleme hattı tanımı ve betiği (`onisle.py`) |
| `uygulama/PROTOKOL.md` | Altı modeli **adil** karşılaştırma kuralları — herkes için bağlayıcı |
| `uygulama/ortak/` | Ortak veri yükleyici, bölme, metrik, eğitim döngüsü, ONNX dışa aktarma |
| `uygulama/ortak/saglik_testi.py` | PROTOKOL K5 sağlık testleri — eğitim hattını sentetik veriyle uçtan uca koşar (veri/GPU gerekmez) |
| `uygulama/ortak/svm_kos.py` | Voksel tabanlı lineer SVM temel çizgisi (madde 9b), `egit.py` ile aynı JSON şeması |
| `uygulama/ortak/dis_test.py` | Dış test: başka sette sıfır-atış değerlendirme (K4 sızıntı kontrollü) |
| `uygulama/api/tahmin.py` | Karar destek çıkarımı: ön işleme + ONNX → sınıf ve olasılıklar |
| `uygulama/api/isi_haritasi.py` | Açıklanabilirlik: Grad-CAM ve oklüzyon haritaları (.npy + 3 kesitli .png) |
| `uygulama/<kişi>_P<no>_<model>/` | Her implementasyonun kendi klasörü |
| `karsilastirma/SONUCLAR.md` | Altı modelin sonuç tablosu (şablon) |
| `karsilastirma/KOSU-PLANI.md` | GPU bütçesi hesabı, indirgenmiş plan, T0–T4 öncelik katmanları, komut sırası |
| `karsilastirma/tablo_uret.py` | Koşu kayıtları → SONUCLAR satırı; uymayan koşuları ayıklar, taramayı doğrulama üstünden seçer |
| `devir/DEVIR-<ad>.md` | Her arkadaşın kendi Claude sohbetine yapıştıracağı devir promptu |

## Takım: GitHub'dan nasıl devam edilir

Depo: **https://github.com/YesilBaraN/tasarim-alzheimer**

### 1. Kur (bir kez, ~15 dk)
```powershell
git clone https://github.com/YesilBaraN/tasarim-alzheimer.git
cd tasarim-alzheimer
py install 3.12                 # Python 3.12 yoksa; olmazsa python.org/downloads (3.11 veya 3.12)
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r onisleme\requirements.txt
```
GPU'n varsa CPU satırı yerine `KURULUM.md §2` Yol A'yı izle — **cu124 kullanma**, orada açıklanan tuzağa düşersin.

### 2. Yeşil olduğunu gör (~3 dk)
```powershell
python uygulama\test_model.py
python onisleme\test_onisle.py
python uygulama\ortak\saglik_testi.py
```
Üçünde de `OK` satırları ve sonda `TÜM ... OK` görmelisin. Görmezsen kod değiştirmeden önce bunu çöz.

### 2b. Açık veriyi indir (herkes aynı dosyaları alsın)
```powershell
python veri\indir.py --hedef D:\veri             # D: yoksa Desktop\veri de olur
python veri\indir.py --hedef D:\veri --dogrula   # indirme, eldekini sına
```
İki CC0 veri seti iner — **ds007561** (20 denek, 284 MB) ve **ds007857** (287 denek, 2,6 GB).

**Veri depoya girmez**; betik hedefi depo içinde seçersen reddeder. Sebep hukuki değil (CC0 yeniden dağıtıma izin verir), teknik: 2,9 GB ikili dosya herkesin klonunu şişirir, GitHub 1 GB üstü depolarda uyarır, Git LFS'in ücretsiz katmanı 1 GB — ve veri zaten tek komutla iniyor. Paylaştığımız şey veri değil, **onu birebir aynı indiren betik**; böylece üçümüzde de aynı dosyalar olur.

ADNI ve OASIS bu betikle **inmez**: başvuru ve Data Use Agreement isterler (`veri/VERI-SETI.md §2`).

### 2c. İşlenmiş veriyi al (3,5 saat kazandırır)
Ham veriyi indirmek dakikalar sürer; **ön işlemek ~3,5 saat** (143 hacim × ~75–95 sn, GPU'da).
Üçümüz ayrı ayrı yaparsak 10 saat boşa gider. İki yol var:

**a) Hazırını indir (önerilen).** İşlenmiş hacimler (`128³ float16 .npy`, ~600 MB) depo **Releases**
bölümünden iner. Git geçmişine girmez, klonu şişirmez. Kaynak setler CC0 olduğu için paylaşımı serbest.

**b) Kendin üret (birebir aynı çıkar).** Zincirin tamamı tohuma bağlı ve belirli:
```powershell
python veri\indir.py --hedef D:\veri
python uygulama\ortak\bolme.py etiket-bids --katilimcilar D:\veri\ds007857\ham\participants.tsv --veri D:\veri\ds007857\ham --cikti veri\ds007857_etiket.csv
python uygulama\ortak\eslestir.py --etiket veri\ds007857_etiket.csv --cikti veri\ds007857_eslesmis.csv --oran 1.5 --kaliper 3
python onisleme\onisle.py --girdi D:\veri\ds007857\ham --cikti D:\veri\ds007857\islenmis --toplu --liste veri\ds007857_eslesmis.csv --cihaz 0
```
Aynı tohumla aynı denekler seçilir, aynı bölme çıkar. Depodaki `veri\ds007857_eslesmis.csv` ile
karşılaştırarak doğrulayabilirsin — fark varsa tohum ya da etiket CSV'si farklıdır.

**Etiket dosyaları depoda:** `veri/ds007561_etiket.csv`, `veri/ds007857_etiket.csv`,
`veri/ds007857_eslesmis.csv`. Bunlar CC0 setlerin tanı/yaş/cinsiyet bilgisi olduğu için paylaşılabilir.
**ADNI/OASIS etiketleri asla girmez** (DUA) — onları herkes kendi indirmesinden üretir.

### 3. Nerede kaldığımızı oku
`SUREC.md` → **§9 NEREDE KALDIK** tablosunda kendi satırlarını bul. Sonra `DEVAM.md` (son oturumda ne yapıldı, ne bozuktu, ne düzeltildi) ve `uygulama/PROTOKOL.md` (bağlayıcı kurallar).

### 4. Çalış ve geri gönder
`devir/DEVIR-<adın>.md` dosyasının **A bölümünü** kendi Claude sohbetine yapıştır. İki yol var:

- **Claude Code ile (önerilir):** klasörü açtır, dosyaları doğrudan düzenlesin, sonra
  ```powershell
  git pull --rebase
  git add -A
  git commit -m "Gorkem: P06 inceleme notu"
  git push
  ```
- **claude.ai sohbetiyle:** sohbette dosya sistemi yok; değiştirdiği dosyaları tam içerikle indir, klasöre koy, yukarıdaki dört komutu koş. İstersen GitHub web arayüzünden de yükleyebilirsin (dosyayı aç → kalem simgesi → yapıştır → Commit).

> **PR açmanız gerekmiyor — doğrudan `main`'e push edin.** Üçünüz de yazma yetkisine sahipsiniz
> ve `main` dalında koruma yok; yukarıdaki dört komut yeterli, kimsenin onayını beklemenize gerek yok.
> Pull request yalnızca **isteyerek** kullanılır: büyük bir değişikliği göstermek ya da CI'ı
> `main`'e dokunmadan koşturmak istiyorsanız. Yoksa normal yol doğrudan push.

**Push öncesi her zaman `git pull --rebase`.** Çakışma çıkarsa dosyayı aç, `<<<<<<<` işaretlerini temizle, `git add` + `git rebase --continue`.

### Yetkiler
| Kişi | Rol | Yapabildiği |
|---|---|---|
| Baran (`YesilBaraN`) | admin / sahip | her şey + depo ayarları, yetki verme, görünürlük |
| Görkem (`ahmtgrkem`) | write | **doğrudan `main`'e push**, dal açma, PR açma/birleştirme, issue, Actions |
| Ertuğrul (`Wujin0`) | write | aynısı |

Write yetkisi günlük işin **tamamını** kapsıyor: kod yazmak, push etmek, PR birleştirmek, issue açmak.
Yalnızca depo ayarları (görünürlük, silme, yeni kişi ekleme) sahibe özel.

⚠ **Admin yetkisi kişisel hesaptaki depoda paylaşılamıyor** — GitHub kişisel depolarda collaborator'a
`admin` atanmasına izin vermiyor (API `422: Cannot assign … permission of admin` dönüyor). Üçümüzün de
admin olması gerekirse depoyu ücretsiz bir **GitHub Organization**'a taşımak gerekir; iş akışı için
gerekli değil, çünkü write zaten her şeyi kapsıyor.

### Çakışmayı önleyen tek kural
Kendi klasörlerin sende: `makaleler/<adın>/`, `uygulama/<adın>_*`. **Ortak dosyalarda (`SUREC.md`, `DEVAM.md`, `KARSILASTIRMA-15.md`, `MAKALE-LISTESI.md`, `rapor/`) yalnız kendi satırını/bölümünü düzenle.** Başkasının satırına dokunma; aynı satırı iki kişi değiştirirse rebase çakışır.

### Depoya ASLA girmeyecekler
ADNI/OASIS görüntüleri, `.npy`/`.pth`/`.onnx` dosyaları, klinik sütunlu bölme CSV'leri, `.venv`. `.gitignore` bunları dışlıyor — **`git add -f` ile zorlamayın**, DUA ihlali olur. Veriyi herkes kendi hesabıyla indirir (`veri/VERI-SETI.md`).

### Ortak alanın üç kuralı

**1. Rozet yeşil kalır.** Her push'ta GitHub Actions üç test takımını + ONNX dışa aktarmayı + çıkarım katmanını Windows ve Linux'ta koşar (`.github/workflows/testler.yml`). Rozet kırmızıya dönerse **önce onu düzelt**, üstüne yeni iş yığma — kırmızı CI'a alışan ekip CI'ı olmayan ekiptir. Koşuları depoda [Actions](https://github.com/YesilBaraN/tasarim-alzheimer/actions) sekmesinden görürsün.

`uygulama/<adın>_*/model.py` dosyasını yazdığın anda CI onu kendiliğinden bulur ve `olustur(varyant, sinif_sayisi, girdi_boyut)` sözleşmesiyle 32³ rastgele hacimde ileri/geri geçirir. Sözleşmeye uymazsa rozet kırmızıya döner — eksik bir pip paketi yüzünden atlanırsa logda `ATLA` olarak yazar, sessizce geçmez.

**2. Koşu kayıtları depoya girer, ağırlıklar girmez.** Her eğitim koşusunun JSON kaydını `karsilastirma/kosu_kayitlari/` altına commit et (`.pth` dosyaları `.gitignore`'da). Tablo kimsenin elle doldurmasına gerek kalmadan üretilir:
```powershell
python karsilastirma	ablo_uret.py --set adni1 --gorev ikili
```
Koşuyu **commit'lenmiş koddan** başlat: `tablo_uret.py`, commit hash'i olmayan kaydı tabloya almaz (PROTOKOL madde 10).

**3. Durum tek yerde tutulur.** İşin bitince `SUREC.md §9` tablosundaki **kendi satırını** ve gerekiyorsa `DEVAM.md`'yi güncelle. Bir sonraki kişi (ya da bir sonraki Claude sohbeti) oraya bakarak nerede kaldığımızı anlıyor; güncellenmezse herkes baştan keşif yapar.

## Bağlayıcı ilkeler
- **Açık erişim:** tüm makaleler ücretsiz tam metinli; tüm kod MIT/Apache/BSD lisanslı açık depolardan veya MONAI'den; araçlar pip ile ücretsiz; hesaplama Kaggle/Colab ücretsiz katman.
- **Veri gizliliği:** ADNI verisi yeniden dağıtılamaz (DUA). Ham veri Drive/GitHub'a konmaz; herkes kendi hesabından indirir.
- **Adil karşılaştırma:** `uygulama/PROTOKOL.md` dışına çıkan sonuç tabloya girmez.
- **Sızıntı yok:** bölme her zaman denek (RID) düzeyinde; aynı deneğin iki taraması farklı katlara düşmez.
