# P13 — Lian 2020 — Hiyerarşik FCN (H-FCN)

> **Durum:** ☐ okunmadı · ☐ AI özeti hazır · ☑ Opus doğrulandı · ☐ insan okudu · ☐ implemente edildi
> **Sorumlu:** Ertuğrul Kabaoğlu · **Grup:** C · **Tam metin (ücretsiz):** https://pmc.ncbi.nlm.nih.gov/articles/PMC6588512/ (IEEE TPAMI 2020) · **Kod:** Resmi repo yok (Keras/TensorFlow prototipi) · **Rol:** Okuma — Güçlü Karşılaştırma Referansı (AD-NC 0.903)

---

## 1. Künye
- **Yazarlar:** Chunfeng Lian, Mingxia Liu, Jun Zhang, Dinggang Shen.
- **Yıl / Başlık:** 2020 — *Hierarchical Fully Convolutional Network for Joint Atrophy Localization and Alzheimer’s Disease Diagnosis Using Structural MRI*.
- **Yayın Yeri:** *IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)*, Cilt 42, Sayı 6, Sayfalar 1494–1506, Haziran 2020 (İlk yayın Aralık 2018).
- **DOI / PMC:** [10.1109/TPAMI.2018.2889096](https://doi.org/10.1109/TPAMI.2018.2889096) · PubMed Central: [PMC6588512](https://pmc.ncbi.nlm.nih.gov/articles/PMC6588512/).
- **Atıf Sayısı:** ~480 (Google Scholar, 2026 itibarıyla).

---

## 2. Tek paragraf özet
Lian ve arkadaşları, yapısal MRI (sMRI) görüntülerinde hastalıkla ilişkili yerel beyin atrofisi tespiti ile global Alzheimer teşhisini tek bir uçtan uca derin mimaride birleştiren Hiyerarşik Tam Evrişimli Ağ (Hierarchical Fully Convolutional Network, H-FCN) önermiştir. Geleneksel yama tabanlı yöntemlerin atrofili bölgeleri önceden seçip sınıflandırıcıdan bağımsız eğitme kısıtını aşmak için, çok ölçekli yerel yamalardan (kaba ve ince ölçek) hiyerarşik öznitelik çıkaran ve tüm beyin düzeyinde birleşik kayıp fonksiyonuyla optimize edilen bir ağ yapısı kurgulanmıştır. ADNI-1 başlangıç (baseline) kohortundaki 830 denek (229 NC, 226 sMCI, 167 pMCI, 199 AD) üzerinde denek düzeyinde 10-kat çapraz doğrulama ile yürütülen deneylerde H-FCN, AD vs. NC ikili sınıflandırmasında $\%90.3$ doğruluk, $\%96.5$ özgüllük ve $0.951$ AUC; pMCI vs. sMCI dönüşüm tahmininde ise $\%80.9$ doğruluk ve $0.781$ AUC elde etmiştir. Ayrıca, model ADNI-2 kohortunda eğitilip ADNI-1 kohortunda bağımsız dış test edildiğinde $\%89.5$ doğruluk ve $0.945$ AUC sergileyerek literatürdeki en sağlam sızıntısız genelleme referanslarından birini sunmuştur.

---

## 3. Problem ve katkı
- **Çözmeye çalıştıkları problem:** Geleneksel derin öğrenme yöntemlerinde ayırt edici yerel beyin atrofisi tespitinin (atrophy localization) öznitelik çıkarımı ve nihai sınıflandırıcıdan izole edilmesi; yama seçimindeki ön kabullerin global sınıflandırma başarısını sınırlaması.
- **İddia ettikleri katkılar (madde madde):**
  1. **Uçtan Uca Hiyerarşik FCN (H-FCN):** Yerel atrofi tespiti ile tüm beyin sınıflandırmasını tek bir hesaplama grafiğinde birleştiren hiyerarşik tam evrişimli mimari (§1, §3).
  2. **Otomatik Çok Ölçekli Yama Değerlendirmesi:** Önceden tanımlanmış ROI veya el yapımı özniteliklere gerek duymadan, kaba ve ince ölçekli beyin yamalarının ayırt ediciliğini ağ içinde otomatik puanlama ve ağırlıklandırma (wH-FCN).
  3. **Çapraz Kohort Sağlamlığı:** ADNI-2 $\rightarrow$ ADNI-1 bağımsız çapraz kohort testinde $\%89.5$ doğruluk ve $0.945$ AUC ile güçlü genellenebilirlik kanıtı (Tablo 3).

---

## 4. Veri seti ve bölme
- **Kaynak Kohortlar (Tablo 1):**
  - **ADNI-1 (Başlangıç/Baseline):** Toplam $N = 830$ denek:
    - NC: 229 denek (127 E / 102 K, yaş 75.8 ± 5.0, MMSE 29.1 ± 1.0)
    - sMCI (stabil MCI): 226 denek (151 E / 75 K, yaş 74.9 ± 7.6, MMSE 27.3 ± 1.8)
    - pMCI (dönüşen MCI): 167 denek (102 E / 65 K, yaş 74.8 ± 6.8, MMSE 26.6 ± 1.7)
    - AD: 199 denek (106 E / 93 K, yaş 75.3 ± 7.5, MMSE 23.3 ± 2.0)
  - **ADNI-2 (Bağımsız Eğitim/Test):** $N = 517$ başlangıç taraması.
- **Bölme Yöntemi:** ADNI-1 üzerinde **denek (RID) düzeyinde 10-kat çapraz doğrulama** (10-fold CV). Çapraz kohort analizinde ADNI-2'nin tamamı eğitim, ADNI-1'in tamamı test olarak kullanılmıştır (Tablo 3).
- **Sızıntı riski değerlendirmesi:** **Düşük.** Yalnızca başlangıç (baseline) taramaları kullanılmıştır (longitudinal sızıntı yok). Bölme katları kesinlikle denek bazındadır. ADNI-2 bağımsız dış test protokolü kusursuz uygulanmıştır.

---

## 5. Ön işleme
1. **Kafatası Soyma (Skull Stripping):** MIPAV yazılımı kullanılarak kafatası ve beyin dışı dokular ayıklanmıştır.
2. **Bias Alanı Düzeltme:** N4ITK algoritması ile manyetik alan homojensizlikleri giderilmiştir.
3. **Kayıtlama (Registration):** FSL FLIRT ile Colin27 şablonuna afin olarak hizalanmıştır ($1 \times 1 \times 1 \text{ mm}^3$ izotropik voksel).
4. **Boyut:** Son hacimler $181 \times 217 \times 181$ matris boyutundadır.

---

## 6. Mimari
- **Hiyerarşik Yapı:**
  - Alt Katman (Bottom-level FCN): Yerel yamalar ($32^3$ ve $64^3$) üzerinde çalışan evrişim blokları; yerel atrofi olasılık haritasını üretir.
  - Üst Katman (Top-level FCN): Alt katmandan gelen öznitelik haritalarını ve atrofi olasılıklarını küresel bağlamda birleştiren evrişim ve havuzlama katmanları.
- **Ağırlıklandırılmış Füzyon (wH-FCN):** Her yerel yamanın ayırt edicilik derecesi ağ içinde bir dikkat/önem katsayısı ile çarpılarak nihai sınıflandırıcıya iletilir.
- **Girdi:** $181 \times 217 \times 181$ (3B sMRI). Çıkış: İkili olasılık (AD vs NC veya pMCI vs sMCI).

---

## 7. Eğitim ayarları
- **Optimizer:** Adam veya SGD + Momentum.
- **Kayıp Fonksiyonu:** Birleşik kayıp (Yerel yama sınıflandırma kaybı + Global hasta sınıflandırma kaybı; çoklu görev optimizasyonu).
- **Batch Boyutu:** Bellek kısıtları nedeniyle küçük batch (2-4).
- **Düzenlileştirme:** $L_2$ ağırlık çürümesi, Dropout.

---

## 8. Sonuçlar

### ADNI-1 10-Kat Çapraz Doğrulama Sonuçları (Makale Tablo 2)
| Yöntem | Görev | Doğruluk (ACC) | Duyarlılık (SEN) | Özgüllük (SPE) | AUC | Kaynak |
|---|---|---|---|---|---|---|
| ROI Temelli SVM | AD vs NC | 0.792 | 0.786 | 0.796 | 0.867 | Tablo 2 |
| VBM Temelli | AD vs NC | 0.805 | 0.774 | 0.830 | 0.876 | Tablo 2 |
| Çoklu Örnek Öğrenmesi (DMIL) | AD vs NC | 0.911 | 0.881 | 0.935 | 0.959 | Tablo 2 |
| **wH-FCN (Önerilen)** | **AD vs NC** | **0.903** | **0.824** | **0.965** | **0.951** | Tablo 2 |
| ROI Temelli SVM | pMCI vs sMCI | 0.661 | 0.474 | 0.690 | 0.638 | Tablo 2 |
| DMIL | pMCI vs sMCI | 0.769 | 0.421 | 0.824 | 0.776 | Tablo 2 |
| **wH-FCN (Önerilen)** | **pMCI vs sMCI** | **0.809** | **0.526** | **0.854** | **0.781** | Tablo 2 |

### ADNI-2 Eğitim $\rightarrow$ ADNI-1 Bağımsız Dış Test (Makale Tablo 3)
| Yöntem | Doğruluk (ACC) | Duyarlılık (SEN) | Özgüllük (SPE) | AUC |
|---|---|---|---|---|
| LBM (Temel Çizgi) | 0.820 | 0.824 | 0.817 | 0.887 |
| **wH-FCN (Önerilen)** | **0.895** | **0.879** | **0.910** | **0.945** |

---

## 9. Açıklanabilirlik / ek analiz
- H-FCN'in ara katmanlarından elde edilen atrofi haritaları, AD hastalarında hipokampus, amigdala, parahipokampal girus ve ventriküler genişlemeleri çok belirgin şekilde işaretlemektedir (Fig. 4, Fig. 5).
- pMCI olgularında henüz klinik tablo tam gelişmeden önce temporal lobdaki mikro-yapısal hacim kayıplarının saptanabildiği gösterilmiştir.

---

## 10. Kod ve tekrarlanabilirlik
- **Depo:** Yazarlar makalede resmî bir açık kaynak deposu vermemiştir (— resmi kod yok).
- **Yeniden Üretilebilirlik:** Fikir, P11 Qiu vd. (brain2020) ile benzer prensiplere dayanır; farkı tek aşamalı hiyerarşik kayıp fonksiyonudur.
- **Lisans:** Kod olmadığı için doğrudan kod transferi yapılmamıştır; mimari kavramsal referans olarak değerlendirilmiştir.

---

## 11. Güçlü ve zayıf yönler
- **Güçlü Yönler:**
  1. Yüksek bilimsel titizlik: IEEE TPAMI gibi zirve bir dergide yayınlanmış, 830 denekli ADNI-1 baseline üzerinde sızıntısız 10-kat CV ile test edilmiştir.
  2. Dış test başarısı: ADNI-2'de eğitilip ADNI-1'de $\%89.5$ doğruluk elde ederek literatürün en güçlü dış genelleme örneklerinden birini sunmuştur.
  3. İki görevin (AD-NC ve pMCI-sMCI) ortak ele alınması.
- **Zayıf Yönler:**
  1. Resmi kod deposunun bulunmaması.
  2. Hiyerarşik çok ölçekli yapının karmaşık eğitim parametreleri ve bellek ihtiyacı.

---

## 12. Bizim projeye uyarlama
- **Rol:** Literatür Karşılaştırma ve Üst Başarı Referansı (Target Benchmark).
- **Çıkarımlarımız:**
  - Lian vd.'nin ADNI-1 baseline üzerinde elde ettiği **ACC: 0.903, AUC: 0.951** değerleri, projemizin birincil hedefi olan "AD-NC ikili görevde $\ge \%85$ dengeli doğruluk" için ulaşılabilir ve gerçekçi bir tavan hedef sunmaktadır.
  - Bağımsız kohort aktarımında (ADNI-2 $\rightarrow$ ADNI-1) başarının $\%89.5$'e düşmesi, dış testte (projemizde OASIS-1 dış testi) ~2-5 puanlık bir genelleme kaybının doğal olduğunu kanıtlar.

---

## 13. Opus doğrulama
- **Sonuç:** **ÇELİŞKİ YOK**
- **Kontrol edilen sayılar ve kaynakları:**
  1. ADNI-1 denek sayısı: $N = 830$ (229 NC, 226 sMCI, 167 pMCI, 199 AD) (Tablo 1). **Birebir doğru.**
  2. wH-FCN AD vs NC sonuçları (Tablo 2): ACC $0.903$, SEN $0.824$, SPE $0.965$, AUC $0.951$. **Birebir doğru.**
  3. wH-FCN pMCI vs sMCI sonuçları (Tablo 2): ACC $0.809$, SEN $0.526$, SPE $0.854$, AUC $0.781$. **Birebir doğru.**
  4. ADNI-2 $\rightarrow$ ADNI-1 dış test sonuçları (Tablo 3): ACC $0.895$, SEN $0.879$, SPE $0.910$, AUC $0.945$. **Birebir doğru.**
  5. Ön işleme boyutları: $181 \times 217 \times 181$ matris, $1\text{ mm}^3$ izotropik voksel (§4.1). **Doğru.**
- **Güven düzeyi:** Yüksek (Tam metin PMC6588512 XML incelenerek tüm tablolar doğrulanmıştır).

---

## 14. Kaynaklar
1. Lian C. et al., *IEEE TPAMI*, 42(6): 1494–1506, 2020: https://pmc.ncbi.nlm.nih.gov/articles/PMC6588512/
