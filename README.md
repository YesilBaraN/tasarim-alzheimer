# Alzheimer Erken Teşhisi — 3B Derin Öğrenme Karar Destek Sistemi

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
| `uygulama/<kişi>_P<no>_<model>/` | Her implementasyonun kendi klasörü |
| `karsilastirma/SONUCLAR.md` | Altı modelin sonuç tablosu (şablon) |
| `karsilastirma/KOSU-PLANI.md` | GPU bütçesi hesabı, indirgenmiş plan, T0–T4 öncelik katmanları, komut sırası |
| `karsilastirma/tablo_uret.py` | Koşu kayıtları → SONUCLAR satırı; uymayan koşuları ayıklar, taramayı doğrulama üstünden seçer |
| `devir/DEVIR-<ad>.md` | Her arkadaşın kendi Claude sohbetine yapıştıracağı devir promptu |

## Nasıl devam edilir (3 adım)
1. `SUREC.md` → "NEREDE KALDIK" tablosuna bak; kendi satırını bul.
2. `devir/DEVIR-<adın>.md` dosyasının **A bölümünü** kendi Claude sohbetine yapıştır, klasörü (zip) sohbete yükle.
3. İşin bitince `SUREC.md` tablosundaki durumunu ve `DEVAM.md`'yi güncelle.

## Bağlayıcı ilkeler
- **Açık erişim:** tüm makaleler ücretsiz tam metinli; tüm kod MIT/Apache/BSD lisanslı açık depolardan veya MONAI'den; araçlar pip ile ücretsiz; hesaplama Kaggle/Colab ücretsiz katman.
- **Veri gizliliği:** ADNI verisi yeniden dağıtılamaz (DUA). Ham veri Drive/GitHub'a konmaz; herkes kendi hesabından indirir.
- **Adil karşılaştırma:** `uygulama/PROTOKOL.md` dışına çıkan sonuç tabloya girmez.
- **Sızıntı yok:** bölme her zaman denek (RID) düzeyinde; aynı deneğin iki taraması farklı katlara düşmez.
