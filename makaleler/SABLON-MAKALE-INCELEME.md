# P0x — <Kısa ad> (<İlk yazar> <yıl>)

> **Durum:** ☐ okunmadı · ☐ AI özeti hazır · ☐ Opus doğrulandı · ☐ insan okudu · ☐ implemente edildi
> **Sorumlu:** <ad> · **Grup:** <A/B/C> · **Tam metin (ücretsiz):** <link> · **Kod:** <link> (<lisans>)

Bu şablon 15 makalenin hepsinde aynı. Başlık numaralarını ve sırasını değiştirme; bir bölüm makalede yoksa "— (makalede yok)" yaz, bölümü silme. Her sayının yanına makaledeki yerini yaz (örn. "Tablo 2", "§3.2", "s. 5"). Emin olmadığın bilgiyi "(doğrulanamadı)" diye işaretle.

## 1. Künye
- Yazarlar, yıl, başlık, yayın yeri, cilt/sayfa, DOI / arXiv
- Atıf sayısı (yaklaşık, kaynağı)

## 2. Tek paragraf özet
Ne yapmışlar, hangi veriyle, ne bulmuşlar — 5–7 cümle, teknik ama sade Türkçe.

## 3. Problem ve katkı
- Çözmeye çalıştıkları problem
- İddia ettikleri 2–4 katkı (madde madde)

## 4. Veri seti ve bölme
- Kaynak (ADNI1/2/3, OASIS, AIBL…), denek sayısı, tarama sayısı, sınıflar ve dağılımı
- Bölme yöntemi: denek (RID) düzeyinde mi, tarama düzeyinde mi, dilim düzeyinde mi? Kaç kat CV? Dış test seti var mı?
- **Sızıntı riski değerlendirmesi:** düşük / orta / yüksek + gerekçe (Wen 2020'nin 4 sızıntı türüne göre: yanlış bölme, geç bölme, taraflı transfer, bağımsız test yok)

## 5. Ön işleme
Adım adım (kafatası ayıklama aracı, bias düzeltme, normalizasyon, hizalama şablonu, kırpma/yeniden boyutlandırma, son hacim boyutu).

## 6. Mimari
| Katman / Blok | Çekirdek | Kanal | Çıktı boyutu | Not |
|---|---|---|---|---|
| … | … | … | … | … |
- Parametre sayısı, girdi boyutu, çıkış (sınıf sayısı)
- Varsa ön eğitim / transfer

## 7. Eğitim ayarları
Optimizer, öğrenme hızı ve takvimi, batch, epoch, kayıp fonksiyonu, veri artırma, erken durdurma, düzenlileştirme, donanım, eğitim süresi.

## 8. Sonuçlar
| Görev | Metrik | Değer | Test seti | Kaynak (tablo/§) |
|---|---|---|---|---|
| AD vs NC | Acc / BAcc / AUC / Sens / Spec / F1 | … | iç / dış | … |
| … | … | … | … | … |
- Karşılaştırdıkları temel çizgiler ve farkı

## 9. Açıklanabilirlik / ek analiz
Grad-CAM, LRP, oklüzyon, ilgi haritaları, biyobelirteç bölgeleri (hipokampus vb.) — varsa.

## 10. Kod ve tekrarlanabilirlik
- Depo, lisans, çerçeve (PyTorch/TF/Keras/Theano/MATLAB), son güncelleme
- Hangi dosyalar doğrudan alınabilir, hangileri yeniden yazılmalı
- Eksikler (ağırlık yok, veri listesi yok, ön işleme betiği yok…)

## 11. Güçlü ve zayıf yönler
- Güçlü: …
- Zayıf: …

## 12. Bizim projeye uyarlama
Kurulumumuz: ADNI1 1.5T başlangıç T1, NC/MCI/AD, HD-BET → N4 → z-score → MNI152 afin → 128³, RID düzeyinde 5-kat CV, birincil görev AD-NC, ikincil 3-sınıf.
- Neyi aynen alıyoruz, neyi değiştiriyoruz (ve neden)
- Beklenen zorluk (1 kolay – 5 zor) ve gerekçe
- Tahminî VRAM / süre (128³, batch 4, T4-16 GB)
- Ortak protokole (uygulama/PROTOKOL.md) uymayan noktalar

## 13. Opus doğrulama
_(Bu bölümü ayrı bir "hakem" turu doldurur: Claude Code'da ikinci ajan, claude.ai'de aynı sohbette "Şimdi hakem ol: §2–§12'deki her sayıyı makaleye karşı kontrol et" komutu. Biçim `baran/P01-*.md §13` gibi:)_
- **Sonuç:** ÇELİŞKİ YOK / ÇELİŞKİ VAR · **Güven:** düşük / orta / yüksek · hakemin okuduğu kaynak
### 13.1 Kontrol edilen sayılar — tablo: İddia | Özetteki değer | Makaledeki değer | Durum (doğru/yanlış/doğrulanamadı) | Yer
### 13.2 Düzeltmeler (özette yanlış/eksik → doğrusu)
### 13.3 Özetin atladığı önemli noktalar
### 13.4 Doğrulanamayanlar
### 13.5 Okuyucunun işaretlediği anahtar sayılar (ham liste)

## 14. Kaynaklar
Bu notta kullanılan tüm linkler (makale, kod, ek kaynaklar).
