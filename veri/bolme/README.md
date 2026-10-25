# veri/bolme — bölme dosyaları

`bolme.py bol` burada iki tür dosya üretir. **Hangisinin depoya girdiğine dikkat:**

| Dosya | İçerik | Depoya girer mi |
|---|---|---|
| `<set>_test.csv`, `<set>_kat0..4.csv` | denek_id, dosya, **sinif (tanı)**, **yas**, **cinsiyet**, bolum | ❌ **Hayır** — ADNI/OASIS DUA klinik veriyi üçüncü tarafa dağıtmayı yasaklar, GitHub da üçüncü taraftır. `.gitignore` bunları dışlar; herkes kendi hesabıyla indirip **aynı tohumla** yeniden üretir. |
| `<set>_bolme_haritasi.csv` | denek_id, bolum, kat — **klinik sütun yok** | ✅ **Evet** — PROTOKOL madde 10'un istediği tekrarlanabilirlik bilgisi budur; alan standardı da böyle (clinicadl bölmelerini bu biçimde yayımlar). |

Bölme **bir kez** üretilir ve değiştirilmez: 6 model, iki temel çizgi ve tüm ablation'lar aynı dosyaları kullanır (PROTOKOL K3). Tohum farklıysa sonuçlar karşılaştırılamaz.

## Üretme ve doğrulama

```powershell
python uygulama\ortak\bolme.py etiket-oasis --csv D:\veri\oasis1\oasis_cross-sectional.csv --islenmis D:\veri\oasis1\islenmis --cikti veri\oasis1_etiket.csv
python uygulama\ortak\bolme.py bol --etiket veri\oasis1_etiket.csv --set oasis1 --cikti veri\bolme --tohum 2026
python uygulama\ortak\bolme.py dogrula --set oasis1 --bolme veri\bolme
```

ADNI için: `etiket-adni --adnimerge D:\veri\adni1\ADNIMERGE.csv --islenmis D:\veri\adni1\islenmis --cikti veri\adni1_etiket.csv`.

Son komut **"SIZINTI KONTROLÜ: TEMİZ (0 kesişim)"** yazmazsa hiçbir koşu başlatılmaz (PROTOKOL madde 1–2, K2–K3). Kontrol ettiği üç şey: kat içinde eğitim ∩ doğrulama boş, CV ∩ kilitli test boş, katların doğrulama kümeleri birbirinden ayrık.

## Ekip içi tutarlılık

Herkes bölmeyi kendi bilgisayarında üretir, ama **aynı bölmeye düşmek zorunlu**. Kendi ürettiğin haritayı depodakiyle karşılaştır: `git status veri/bolme/` çıktısında `*_bolme_haritasi.csv` **değişmiş görünmemeli**. Değişmiş görünüyorsa sebep ya farklı tohum ya farklı etiket CSV'sidir (ör. işlenmiş hacim sayısı farklı, bir denek atlanmış). Çözülmeden koşulan sonuçlar aynı tabloya giremez.
