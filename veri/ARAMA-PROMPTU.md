# Açık veri arama promptu

Yeni bir yapay zekâ sohbetine (ya da bir arkadaşa) verilecek hazır istem. Amacı: aynı çıkmaz sokakları
tekrar yürümeden, **bizim işimize yarayacak** açık veri setini aramak.

Aşağıdaki bloğun tamamını kopyala.

---

> Alzheimer sınıflandırması için **3 boyutlu yapısal beyin MRI** veri seti arıyorum. Bir lisans bitirme
> projesi için; sonuçlar bir komisyona savunulacak, bu yüzden **metodolojik olarak savunulabilir** veri lazım.
>
> **ZORUNLU ŞARTLAR** (biri bile sağlanmıyorsa o set elenir, bana getirme):
> 1. **3B hacim** olmalı — NIfTI (`.nii`/`.nii.gz`), DICOM, Analyze (`.img`/`.hdr`) ya da benzeri.
>    **2B dilim görüntüleri (JPG/PNG) işime yaramıyor**; modellerim 3B konvolüsyon kullanıyor ve JPG
>    dönüşümü MRI'ın nicel yoğunluk bilgisini yok ediyor.
> 2. **Denek (hasta) kimliği korunmuş olmalı.** Hangi görüntünün hangi kişiye ait olduğu bilinmeli.
>    Bölmeyi denek düzeyinde yapmak zorundayım; aynı kişinin iki taraması eğitim ve test kümesine
>    dağılırsa doğruluk yapay olarak şişiyor (Yagis 2021 bunu 25–55 puan ölçtü).
> 3. **Tanı etiketi olmalı**: en az sağlıklı kontrol (CN/NC) ve Alzheimer (AD); tercihen MCI de.
>    CDR, MMSE gibi klinik skorlardan türetilmiş etiket de olur, yeter ki belgelenmiş olsun.
> 4. **Erişim yolu açık olmalı**: doğrudan indirme, kayıt, ya da başvuru. Hangisi olduğunu söyle.
> 5. **Artırılmış (augmented) veri olmamalı.** Döndürülmüş/kaydırılmış kopyalar özgünlerle aynı havuzdaysa
>    o set kullanılamaz.
>
> **ZATEN BAKILDI, TEKRAR GETİRME:**
> - OpenNeuro'nun **tamamı** tarandı (2522 veri seti, hepsinin `participants.tsv` dosyası okundu).
>   Tek uygun olanlar: `ds007561` (20 denek) ve `ds007857` (289 denek, ama yalnız 1 AD). İkisi de indirildi.
>   `ds005048` etiketleri iyi ama yalnız EEG, MRI yok.
> - **ADNI**, **OASIS-1/2/3**, **AIBL**, **MIRIAD**, **EPAD**, **NACC**, **PPMI**, **IXI** biliniyor.
>   Bunların başvuru gerektirdiğini de biliyorum; başvuru süreçlerini anlatma, zaten yapılıyor.
> - Kaggle'daki `tourist55/alzheimers-dataset-4-class-of-images` ve ondan türeyen her şey
>   (`uraninjo/augmented-alzheimer-mri-dataset`, `mohiburrahmanrifat/alzheimer`,
>   `ninadaithal/imagesoasis` dahil) **elendi**: 2B JPG, denek kimliği yok, bazıları artırılmış.
>
> **NASIL ARAMANI İSTİYORUM:**
> Arama motoruna güvenme, **kaynağın kendisine bak**. Örneğin bir veri deposu taranacaksa dosya
> listesini/metadata'sını çek ve etiket dosyalarını gerçekten oku. "Muhtemelen vardır" deme; baktığını
> söyle ya da bakamadığını söyle.
>
> Bakmanı istediğim yerler: NITRC, OpenNeuro dışındaki BIDS depoları, Harvard Dataverse, Zenodo, Figshare,
> Synapse, The Cancer Imaging Archive, ulusal biyobankalar, ve yayınların "data availability" bölümleri.
>
> **HER ADAY İÇİN ŞU TABLOYU DOLDUR:**
>
> | Alan | Cevap |
> |---|---|
> | Ad ve bağlantı | |
> | Dosya biçimi | 3B mi, hangi uzantı |
> | Denek sayısı | sınıf dağılımıyla (CN / MCI / AD) |
> | Denek kimliği var mı | evet/hayır — **hayırsa set elenir** |
> | Etiket kaynağı | tanı, CDR, MMSE…? |
> | Lisans | ve yeniden dağıtıma izin veriyor mu |
> | Erişim | doğrudan / kayıt / başvuru + tahmini süre |
> | Boyut | GB |
> | **Nereden doğruladın** | hangi sayfayı/dosyayı gerçekten açtın |
>
> Son satır önemli: doğrulamadığın bir şeyi tabloya yazma, "doğrulanamadı" yaz. Uygun set bulamazsan
> "bulamadım" de — uydurma ya da şartları esnetme. Eksik bir aday, yanlış bir adaydan iyidir.

---

## Neden bu kadar katı

Bu şartlar keyfi değil; her biri `uygulama/PROTOKOL.md`'deki bir maddeden geliyor:

| Şart | Dayanak |
|---|---|
| 3B hacim | Altı modelin hepsi 3B konvolüsyon kullanıyor |
| Denek kimliği | PROTOKOL madde 1 — denek düzeyinde bölme |
| Artırılmış veri yok | PROTOKOL madde 2 / K1 — artırma yalnız eğitim katında |
| Etiket kaynağı belgeli | Rapor yöntem bölümü yazılabilsin diye |
| Lisans | `veri/VERI-SETI.md` — ADNI/OASIS DUA'ları yeniden dağıtımı yasaklıyor |

Ayrıntılı ret gerekçeleri: `veri/VERI-SETI.md` §2b, §2d, §2e.
