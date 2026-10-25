# Baran — yeni Claude Code oturumuna devir

## A) Yeni oturuma yapıştırılacak prompt

> Ben Baran Yeşilyurt (G231210078). BSM 401 tasarım projesi "Alzheimer Hastalığının Erken Teşhisi İçin 3B Derin Öğrenme Tabanlı Karar Destek Sistemi" — klasör `tasarim-alzheimer\`. Önce `DEVAM.md` ve `SUREC.md §9` (nerede kaldık) oku; sonra `README.md`, `makaleler/MAKALE-LISTESI.md`, `uygulama/PROTOKOL.md`.
>
> Benim grubum A (P01–P05) incelendi ve Opus'la doğrulandı (`makaleler/baran/`). İmplementasyonlarım: P01 Korolev VoxCNN/VoxResNet (`uygulama/baran_P01_korolev`) ve P02 MedicalNet ResNet-18 (`uygulama/baran_P02_medicalnet`); ortak altyapı `uygulama/ortak/`, ön işleme `onisleme/`. Ortak veri/protokol sahibi benim.
>
> Kurallar: bu makinede (sunucu) kurulum/indirme/eğitim yapma — kod iskeleti ve md üret, kendi PC'mde koşarım. Yalnız açık erişimli makale ve MIT/Apache/BSD kod. ADNI verisi paylaşılmaz. Bölme RID düzeyinde.
>
> Sıradaki işler (`DEVAM.md` "Sıradaki" bölümü): [oturumda güncellenir]

## B) Bu oturumda yazdığım istemler
1. Form + "3 kişiyiz, 5'er makale, 2 implementasyon, ortak veri seti; 15 makale belirle, 5'erli grupla, süreci incele, ben Baran'ım, md yap, Sonnet/Opus workflow".
2. "Sunucuyu sıkıştırma; planı ve her şeyi hazırla, gerisini kendi PC'mde yapayım."
3. "Açık kaynaklı kod kullan, erişimi kolay olsun, öğrenciyiz."
4. `Tasarim_ara_raporlar.docx` + "ikinci aşamadayız, buna göre ilerle."

## C) Bulunan sonuçlar
- Plan, 15 makale, atama, veri kararı, ders süreci, Ara Rapor 2 taslağı, ön işleme + ortak eğitim kodu, 2 model iskeleti, devir dosyaları yazıldı (ayrıntı `DEVAM.md`).
- P01–P05: 5 Sonnet okuyucu + 5 Opus hakem; P01, P02, P04'te sayısal çelişkiler bulundu ve §13'te düzeltildi; P05 temiz; P03 (Wen 2020) PDF'den ikinci tur okundu.
- Kritik uyarı danışmana: ≥%85 yalnız AD-NC'de gerçekçi (SUREC.md §7 madde 1).
