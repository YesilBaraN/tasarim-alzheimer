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

Derin öğrenme modellerinin medikal görüntü analizinde, özellikle Alzheimer hastalığının nörodejeneratif evrelerinin saptanmasında klinik rutine girememesinin en kritik engeli "kara kutu" doğalarıdır. Yüksek sınıflandırma doğruluğuna ulaşan bir modelin, kararlarını beyin dışı gürültülere mi yoksa patolojik doku atrofisine mi dayandırdığı şeffafça ortaya konulmalıdır. Bu alt grupta, 3B CNN mimarilerine entegre edilen dikkat mekanizmaları (öz-dikkat, kanal/uzamsal dikkat) ve açıklanabilir yapay zekâ (XAI) yöntemleri (LRP, Grad-CAM, oklüzyon) incelenmiştir:

- **[6] Böhle vd. (2019) — Katman Bazlı İlgi Yayılımı (LRP):** Böhle ve ark. [6], 3B evrişimli sinir ağlarının yapısal MRI üzerindeki sınıflandırma kararlarını piksel/voksel düzeyinde açıklamak amacıyla Katman Bazlı İlgi Yayılımı (Layer-wise Relevance Propagation, LRP) yöntemini uyarlamıştır. ADNI-1 veri tabanından seçilen 969 tarama (344 denek; 193 AD, 151 CN) üzerinde CAT12 ile gri madde yoğunluk haritaları ($193 \times 229 \times 193$) çıkarılmış; 4 bloklu kompakt bir 3D CNN (filtreler: 8-16-32-64, tam bağlantılı katmanlar: 128-2) eğitilmiştir. Denek düzeyinde 10 katlı çapraz doğrulamada AD vs. NC görevinde %81,93 dengeli doğruluk ve 0,880 AUC elde edilmiştir. Çalışmanın temel katkısı, yaygın kullanılan Güdümlü Ters Yayılım (Guided Backpropagation, GB) yöntemi ile LRP'nin sistematik olarak kıyaslanmasıdır. GB yöntemi hem hastalarda hem de sağlıklı kontrollerde yüksek gradyan tepkisi üreterek "yanlış pozitif" şüphe uyandırırken, LRP ($\beta=0$ kuralı ile sadece pozitif katkı sağlayan yönelimler geri yayıldığında) sağlıklı kontrollerde neredeyse sıfır ilgi skoru üretmiş ve AD hastalarında doğrudan hipokampus ve temporal lob atrofisine odaklanmıştır. Ayrıca LRP ilgi skorlarının FreeSurfer hipokampal hacimleri ile istatistiksel olarak anlamlı bir ters korelasyon sergilediği ($r = -0,560, p < 10^{-3}$) kanıtlanmıştır.

- **[7] Zhang vd. (2021) — 3D ResAttNet ve Öz-Dikkat (Self-Attention):** Zhang ve ark. [7], standart 3B ResNet mimarilerine öz-dikkat (Self-Attention) mekanizması ekleyerek hem AD teşhisini hem de patolojik atrofinin yerelleştirilmesini sağlayan 3D ResAttNet modelini önermiştir. Klasik $7\times7\times7$ kök evrişimi yerine 3 adet ardışık $3\times3\times3$ evrişim içeren hafif bir kök katmanı tasarlanmış; rezidüel blokların içine $1\times1\times1$ evrişimlerle sorgu ($Q$), anahtar ($K$) ve değer ($V$) tensörleri üreten 3B Öz-Dikkat katmanı entegre edilmiştir. Çıktı, $y = x + r(x) + \gamma \cdot o(r(x))$ formülüyle rezidüel öğrenmeye bağlanmış; ölçekleyici $\gamma$ katsayısı başlangıçta 0 yapılarak modelin kararlı yakınsaması sağlanmıştır. ADNI-1 kohortunda (817 denek; 188 AD, 400 MCI, 229 NC) yapılan 10 katlı çapraz doğrulamada ResAttNet34; AD vs. NC görevinde %91,3 ± %1,2 doğruluk ve **0,984 ± 0,009 AUC** elde ederek temel ResNet'in standart sapmasını (%14,7'den %1,2'ye) çarpıcı şekilde düşürmüştür. Model ayrıca erken evre pMCI vs. sMCI ayrımında %82,1 doğruluk ve 0,920 AUC başarımı göstermiş; ADNI-2 (3T) harici testinde %82,6 doğruluk ve 0,927 AUC ile çok merkezli genellenebilirliğini kanıtlamıştır. Ağın 3. katmanından ($46\times55\times46$) türetilen 3B Grad-CAM ısı haritaları, son katmanın aşırı bulanık $6\times7\times6$ haritalarına kıyasla hipokampal ve parahipokampal sınırları yüksek anatomik çözünürlükle yerelleştirmiştir.

- **[8] Dyrba vd. (2021) — Etkileşimli İlgi Haritaları ve Biyobelirteç Doğrulaması:** Dyrba ve ark. [8], 3B CNN kararlarının anlaşılabilirliğini artırmak için LRP tabanlı ilgi haritalarını etkileşimli bir web karar destek arayüzü ile birleştirmiştir. ADNI-GO/2 kohortundan $N = 663$ T1 MRI taraması (denek başına tek tarama; 254 CN, 220 MCI, 189 AD) üzerinde eğitilen 3 bloklu 3D CNN (~700 bin parametre), normal yaşlanma etkilerini ayıklamak için sağlıklı kontroller üzerinden doğrusal kovaryat regresyonu (yaş, cinsiyet, TIV, 1.5T/3T alan şiddeti) ile arındırılmış "artık gri madde hacimleri" (residuals) ile beslenmiştir. Model, bugüne kadarki en geniş bağımsız çok merkezli harici test havuzlarından birinde ($N = 1.655$ hasta; ADNI-3: 575, AIBL: 606, DELCODE: 474) sınanmış ve AD vs. CN ayrımında tüm bağımsız kohortlarda **$\text{AUC} \ge 0,91$** ($0,913 - 0,953$, dengeli doğruluk %80,5 - %85,5) korunmuştur. iNNvestigate tabanlı LRP ($\alpha=1, \beta=0$ evrişimde, $\epsilon=10^{-10}$ tam bağlantıda) ile elde edilen ilgi haritaları, AAL atlası hipokampus hacmiyle **$r = -0,87$ ($p < 0,001$)** düzeyinde güçlü bir ters korelasyon sergilemiş; Bokeh tabanlı açık kaynaklı web arayüzü ile klinisyenin 3 eksende dilim gezinimi, AAL anatomik etiketleri ve küme boyut eşikleme yapabilmesi sağlanmıştır.

- **[9] Hoang vd. (2023) — 3D-DAM Çift Dikkat Modülü (CBAM Uyarlaması):** Hoang ve ark. [9], 2B bilgisayarlı görmedeki Convolutional Block Attention Module (CBAM) mekanizmasını 3B medikal tensörlere genişleterek hem dilim/öznitelik düzeyinde kanal ilişkilerini hem de anatomik hacimdeki uzamsal ilişkileri yakalayan 3D-DAM (3D Dual Attention Module) mimarisini önermiştir. Modelde kanal dikkati; 3B ortalama ve maksimum havuzlamanın ardından paylaşımlı bir MLP ile kanallar arası bağıntıyı optimize ederken, uzamsal dikkat kanallar boyunca alınan ortalama ve maksimum haritalarını $3\times3\times3$ evrişimle süzerek kritik vokselleri öne çıkarmaktadır. ADNI veri tabanından seçilen 1.426 denek (403 AD, 653 CN, 165 pMCI, 205 sMCI), Clinica platformunun `t1-linear` boru hattı (N4ITK bias düzeltme + ANTs SyN MNI ICBM2009c afin hizalama) üzerinden BIDS formatına dönüştürülmüştür. 3D-DAM modeli, ADNI test setinde AD vs. CN için **%98,18 ± %0,42** doğruluk (Duyarlılık: %96,73, Özgüllük: %98,97) ve erken evre pMCI vs. sMCI tahmini için **%91,78 ± %0,63** doğruluk (Duyarlılık: %95,06, Özgüllük: %88,62) elde etmiştir. Yöntemin genellenebilirliği AIBL (%86,37 doğruluk) ve OASIS-1 (%83,42 doğruluk) bağımsız veri setlerinde, ayrıca tersine eğitim senaryosunda (AIBL+OASIS eğitim $\rightarrow$ ADNI test: %85,4) kanıtlanmıştır.

- **[10] Jin vd. (2020) — 3DAN ve Nörobilimsel Olarak Yorumlanabilir Biyobelirteçler:** Jin ve ark. [10], 3D ResNet-18 mimarisi üzerine tek bir $3\times3\times3$ evrişim katmanı ile eğitilebilir uzamsal dikkat haritası ($M_i$) ekleyen hafif 3DAN (3D Attention Network) mimarisini geliştirmiştir. Çalışma, 6 farklı hastane ve tarayıcıdan toplanan Çin kurum içi kohortu ($N = 716$; 261 AD, 224 MCI, 231 NC) ile Kuzey Amerika ADNI kohortu ($N = 1.116$; 227 AD, 584 MCI, 305 NC) olmak üzere toplam **$N = 1.832$** denek üzerinde gerçekleştirilmiştir. CAT12 ile $2\text{ mm}$ izotropik voksele ($91 \times 109 \times 91$) getirilen gri madde yoğunlukları üzerinde dört çapraz doğrulama stratejisi yürütülmüştür: Kurum içi $\rightarrow$ ADNI harici testinde %86,1 doğruluk ve 0,912 AUC; ADNI $\rightarrow$ Kurum içi harici testinde %87,0 doğruluk ve 0,913 AUC; merkez dışı bırakmada %90,9 doğruluk; ADNI 10-kat CV'de %92,1 doğruluk ve 0,941 AUC elde edilmiştir. Çalışmanın en özgün yönü, üretilen 3B dikkat haritalarının 273 bölgeli Brainnetome Atlası (BNA) ile eşleştirilerek iki örneklemli $t$-testi gri madde atrofi istatistikleriyle ($r = 0,59, p = 4,75 \times 10^{-27}$), MMSE skorlarıyla, BOS amiloid-$\beta$/tau düzeyleriyle ve APOE $\epsilon4$ genotipleriyle doğrudan nörobiyolojik korelasyonunun kanıtlanmış olmasıdır.


### 2.3 Yama/FCN, DenseNet ve Transformer (Ertuğrul)
- **[11] Qiu vd. (2020) — FCN ile Yama Düzeyi Risk Haritası ve Nörolog Düzeyinde Teşhis:** Qiu ve ark. [11], 3B T1 sMRI verilerinden Alzheimer hastalığı teşhisi koymak ve yüksek çözünürlüklü hastalık olasılık haritaları üretmek amacıyla FCN ve MLP'yi birleştiren iki aşamalı bir mimari geliştirmiştir. Model geliştirme aşamasında $47 \times 47 \times 47$ voksellik yerel 3B yamalar üzerinde 4 evrişim bloklu FCN eğitilmiş; çıkarım evresinde tam bağlantılı katmanlar evrişim çekirdeklerine dönüştürülerek (`dense_to_conv`), kaydırma penceresi döngülerine gerek kalmadan tüm beyin için tek bir ileri geçişte kesintisiz "hastalık olasılık haritası" (Disease Probability Map, DPM) elde edilmiştir. DPM haritasından seçilen en yüksek riskli $K=200$ voksel değeri ile eğitilen nihai MLP sınıflandırıcısı, ADNI test kümesinde yalnızca MRI verisiyle **%83,4 ± 2,0** doğruluk (duyarlılık %76,7, özgüllük %88,9, F1 0,806) elde ederek 11 bağımsız uzman nöroloğun ortalama teşhis başarısını (%82,3 ± 9,4; $\kappa = 0,49$) geride bırakmıştır. Klinik değişkenler (yaş, cinsiyet, MMSE) eklendiğinde doğruluk %96,8'e ve AUC 0,996'ya yükselmiştir. Ayrıca AIBL (%87,0), FHS (%76,6) ve NACC (%81,8) olmak üzere 4 kohortta toplam 1.466 denek üzerinde yüksek genellenebilirlik kanıtlanmış; Framingham Kalp Çalışması'ndan (FHS) otopsi yapılmış 11 hastada modelin işaret ettiği yüksek riskli voksellerin amiloid-$\beta$ ve nörofibriler yumak (tau) histopatolojisiyle mekânsal korelasyonu doğrulanmıştır. Çalışmanın açık kaynaklı PyTorch kodu (`vkola-lab/brain2020`, MIT lisansı), projemizin 5. implementasyon modelinin temelini oluşturmaktadır.
- **[12] Solano-Rojas ve Villalón-Fonseca (2021) — Düşük Maliyetli 3B DenseNet-121:** Solano-Rojas ve ark. [12], gelişmekte olan ülkelerdeki araştırmacıların yüksek maliyetli GPU sunucularına erişim kısıtını aşmak amacıyla, tamamen ücretsiz bulut bilişim kaynakları (Google Colaboratory) üzerinde çalışan bir 3B DenseNet-121 mimarisi önermiştir. ADNI veri tabanından indirilen 5.556 adet 3B T1 MRI taramasından gürültülü olduğu tespit edilen sübjektif "Belirgin Bellek Kaygısı" (SMC) sınıfı elenerek toplam 5.370 tarama ile 5 sınıflı (CN, EMCI, MCI, LMCI, AD) bir evreleme kurgulanmıştır. Voksel aralıkları $1\text{ mm}^3$ ve $256^3$ küboid boyuta getirilen görüntüler üzerinde SGD, momentum (0,9), dropout (0,7) ve batch boyutu 5 ile Colab kesinti sınırlarında (80–110 epoch) mikro-ortalama %84 doğruluk, %81 duyarlılık, %84 özgüllük ve %92 AUROC bildirilmiştir (özette %87 doğruluk). Ancak çalışmada eğitim/test ayrımının denek (RID) düzeyinde değil, tüm taramalar üzerinden rastgele %75 / %25 yapıldığı, aynı hastanın boylamsal vizitlerinin her iki kümeye de dağılarak kritik düzeyde veri sızıntısı (data leakage) yarattığı tespit edilmiştir. Projemizde 3B DenseNet-121, Apache-2.0 lisanslı MONAI omurgası ve hafif `TinyDenseNet` varyantı ile sızıntısız denek bazlı 5-kat çapraz doğrulama altında 6. modelimiz olarak implemente edilmektedir.
- **[13] Lian vd. (2020) — Hiyerarşik FCN (H-FCN) ile Birleşik Atrofi Tespiti ve Teşhis:** Lian ve ark. [13], yapısal MRI görüntülerinde hastalıkla ilişkili yerel beyin atrofisi tespiti ile global Alzheimer teşhisini tek bir uçtan uca mimaride birleştiren Hiyerarşik Tam Evrişimli Ağ (H-FCN) önermiştir. Çok ölçekli yerel yamalardan ($32^3$ ve $64^3$) hiyerarşik öznitelik çıkaran ve her yamanın ayırt ediciliğini ağ içinde otomatik ağırlıklandıran (wH-FCN) model; ADNI-1 başlangıç kohortundaki 830 denek (229 NC, 226 sMCI, 167 pMCI, 199 AD) üzerinde denek düzeyinde 10-kat çapraz doğrulama ile AD vs. NC ikili sınıflandırmasında **%90,3** doğruluk, %82,4 duyarlılık, %96,5 özgüllük ve **0,951** AUC; pMCI vs. sMCI dönüşüm tahmininde ise %80,9 doğruluk ve 0,781 AUC elde etmiştir. Ayrıca model ADNI-2 kohortunda eğitilip ADNI-1 kohortunda bağımsız dış test edildiğinde %89,5 doğruluk ve 0,945 AUC sergileyerek literatürdeki en sağlam sızıntısız başarı referanslarından birini sunmuştur. Bu sonuç, projemizin birincil hedefi olan "AD-NC görevinde $\ge \%85$ dengeli doğruluk" için güçlü bir teorik ve ampirik tavan referansı sağlamaktadır.
- **[14] Jang ve Hwang (2022) — M3T: Çok Düzlemli ve Çok Dilimli Transformer:** Jang ve ark. [14], saf 3B Vision Transformer'ların (ViT) medikal görüntü kıtlığında yaşadığı aşırı uyum ve ağır hesaplama maliyeti sorununu aşmak amacıyla, 3B CNN, 2B CNN ve Transformer bileşenlerini harmanlayan hibrit M3T mimarisini (29,12M parametre) geliştirmiştir. İlk blokta yerel 3B uzamsal ilişkileri yakalayan hafif 3B CNN (32 kanal), ikinci blokta beynin aksiyel, koronal ve sagital düzlemlerinden çıkarılan çoklu 2B dilimleri işleyen ImageNet ön eğitimli ResNet-50 omurgası, son blokta ise düzlemler ve dilimler arası uzun menzilli dikkat ilişkilerini modelleyen 8 katmanlı bir Transformer kodlayıcı ($d=256$, 8 başlık) kullanılmıştır. ADNI'den 4.786 tarama ile eğitilen model; bağımsız ADNI test kümesinde %93,21 doğruluk ve 0,9634 AUC, bağımsız çok merkezli dış test kohortları olan AIBL'de %93,27 doğruluk ve 0,9258 AUC, OASIS'te ise **%85,26** doğruluk ve 0,8961 AUC elde etmiştir. Saf 3B ViT'in (AUC 0,8851) açık ara geride kaldığı çalışma, 3B medikal analizde CNN ön eğitimli hibrit Transformer yapılarının gerekliliğini ve projemizde yürütülecek OASIS-1 dış testinde hedeflenebilecek tavan başarı aralığını (%82–85) ortaya koymaktadır.
- **[15] Dhinagar vd. (2023) — Video ve Sentetik MRI Ön Eğitimi ile ViT ve CNN Karşılaştırması:** Dhinagar ve USC Imaging Genetics Center ekibi [15], 3B nörogörüntüleme analizinde Vision Transformer ve CNN mimarilerinin transfer öğrenme kabiliyetlerini; Kinetics-400 (306.245 doğal insan eylem videosu), LDM ile üretilmiş 100.000 sentetik 3B MRI ve UK Biobank (38.703 gerçek MRI) gibi büyük ölçekli veri kümeleri üzerinden ön eğitime tabi tutarak kıyaslamıştır. Swin-T (27M), ViT-B/16 (8M), 3B DenseNet-121 (11M) ve 3B Tiny DenseNet (1,8M) mimarilerinin ADNI ince ayar ve bağımsız OASIS sıfır atışlı (0-shot) dış test sonuçları; sıfırdan eğitimde 3B DenseNet-121'in (**0,901** AUC, **%84,0** OASIS doğruluk) saf Transformer'ları (0,849 AUC) açık farkla geride bıraktığını, video ön eğitiminin ise Swin-T'yi 0,924 AUC'ye sıçrattığını göstermiştir. En dikkat çekici bulgu, yalnızca 1,8M parametreli hafif 3B Tiny DenseNet'in %83,6 OASIS doğruluğu elde ederek 11M parametreli DenseNet-121 ile neredeyse aynı başarıyı sunmasıdır; bu durum projemizde P12 kapsamında hem standart DenseNet-121 hem de kaynak dostu Tiny DenseNet varyantlarının tasarlanması kararını bilimsel olarak doğrulamaktadır.

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
> **Diyagram Dosyası:** Görkem tarafından hazırlanan PlantUML kaynak dosyası [`rapor/sekiller/usecase.puml`](file:///c:/Users/atomk/OneDrive/Masaüstü/tasarim-alzheimer/rapor/sekiller/usecase.puml) ve rendered diyagramı `rapor/sekiller/usecase.png`.

## 4. TASARIM

### 4.1 Sistem mimarisi (blok diyagram)
Katmanlar, soldan sağa:
1. **Veri katmanı:** ADNI / OASIS-1 ham NIfTI (dış disk, depoya girmez) → `bolme.py` ile RID düzeyi kilitli test + 5 kat → `veri/bolme/`. Klinik sütunlu bölme CSV'leri yerelde kalır; depoya yalnız klinik veri taşımayan `<set>_bolme_haritasi.csv` girer (ADNI DUA).
2. **Ön işleme katmanı (`onisleme/onisle.py`):** dcm2niix → HD-BET → N4 (SimpleITK) → z-score → MNI152 afin (SimpleITK/TemplateFlow) → 128³ float16 `.npy`.
3. **Model katmanı (`uygulama/`):** ortak `veri.py` (Dataset/artırma) + `egit.py` (döngü, AMP, kesintiden devam, LR taraması) + 6 model klasörü (ResNet, MedicalNet-ResNet18, CNN+LRP, ResAttNet, FCN-yama, DenseNet121) + iki temel çizgi (`ortak/model.py` sığ 3B CNN, `svm_kos.py` voksel SVM) → `metrikler.py`.
4. **Doğrulama ve raporlama katmanı:** `saglik_testi.py` (PROTOKOL K5: rastgele etiket ≈ 0.5, ayrılabilir sınıf ≈ 1.0, bölme kesişimi boş), `dis_test.py` (başka sette sıfır-atış, K4 kontrollü), `tablo_uret.py` (kayıt JSON'ları → `karsilastirma/SONUCLAR.md`; protokole uymayan koşuları ayıklar, hiperparametre seçimini doğrulama üstünden yapar).
5. **Dağıtım katmanı:** `onnx_disa_aktar.py` → `model.onnx` (sabit 1×1×128³) → `uygulama/api/tahmin.py` (`KararDestek` sınıfı: ön işleme + onnxruntime + softmax; eğitim/servis uyumu için ön işlemeyi `onisle.py`'den çağırır) → FastAPI sarmalayıcısı (`POST /tahmin`, `GET /saglik`).
6. **Sunum katmanı:** web arayüzü (yükle, sonuç, ısı haritası, PDF) → veritabanı (tahmin kayıtları).
> **Diyagram Dosyası:** Ertuğrul tarafından hazırlanan PlantUML kaynak dosyası [`rapor/sekiller/mimari.puml`](file:///c:/Users/atomk/OneDrive/Masaüstü/tasarim-alzheimer/rapor/sekiller/mimari.puml) ve rendered diyagramı `rapor/sekiller/mimari.png`.

### 4.2 Veritabanı tasarımı (ER)
ADNI/OASIS görüntüleri veritabanına **konmaz** (DUA). Yalnızca meta veri ve tahmin kayıtları tutulur (SQLite ile başlanır, PostgreSQL'e taşınabilir).
| Varlık | Alanlar (PK kalın) | İlişki |
|---|---|---|
| Kullanici | **kullanici_id**, ad, e_posta, rol, parola_hash, olusturma | 1—N Tahmin |
| Tarama | **tarama_id**, kaynak (ADNI/OASIS/klinik), dis_kimlik (RID/OASIS id, anonim), cekim_tarihi, alan_gucu, dosya_hash, yuklenme | 1—N Tahmin, 1—1 OnIsleme |
| OnIsleme | **onisleme_id**, tarama_id, surum, kafatasi_arac, n4, normalizasyon, kayit_sablonu, cikti_boyutu, sure_sn, durum | N—1 Tarama |
| Model | **model_id**, ad (P01…P12), mimari, egitim_veri, protokol_surumu, onnx_yolu, egitim_tarihi, test_bacc, test_auc | 1—N Tahmin |
| Tahmin | **tahmin_id**, tarama_id, model_id, kullanici_id, p_nc, p_mci, p_ad, karar, guven, isi_haritasi_yolu, sure_sn, zaman | N—1 hepsi |
| AciklamaHaritasi | **harita_id**, tahmin_id, yontem (Grad-CAM/LRP/DPM), katman_adi, dosya_yolu, en_yuksek_ilgi_bolgesi, olusturma | N—1 Tahmin |
> **Diyagram Dosyası:** Ertuğrul tarafından hazırlanan 6 varlıklı PlantUML ER şeması [`rapor/sekiller/er.puml`](file:///c:/Users/atomk/OneDrive/Masaüstü/tasarim-alzheimer/rapor/sekiller/er.puml) ve rendered diyagramı `rapor/sekiller/er.png`.

### 4.3 Arayüz prototipleri (mock-up listesi)
Klinik karar destek arayüzümüz hekimin 3 tıklamayla sonuca ve açıklanabilirlik haritasına ulaşmasını hedeflemektedir. Ayrıntılı ekran bileşenleri ve kullanıcı akışları Görkem tarafından [`rapor/sekiller/mockups_spec.md`](file:///c:/Users/atomk/OneDrive/Masaüstü/tasarim-alzheimer/rapor/sekiller/mockups_spec.md) dosyasında tanımlanmıştır:
| Ekran | İçerik ve Klinik İşlev |
|---|---|
| E1 Giriş | Güvenli e-posta/parola girişi, rol seçimi (Radyolog, Araştırmacı, Yönetici), KVKK ve ADNI DUA veri gizliliği bildirimi |
| E2 Yükle | Sürükle-bırak NIfTI/DICOM yükleyici, otomatik anonim protokol kimliği (`SUBJ-xxxx`), meta veri kontrolü (1.5T/3T) |
| E3 İşleniyor | 4 adımlı gerçek zamanlı ilerleme çubuğu (HD-BET → N4ITK → MNI152 afin → ONNX inferansı) ve kalan süre sayacı |
| E4 Sonuç | Olasılık çubukları (NC/MCI/AD), model güven skoru, **zorunlu yasal uyarı ("Karar desteğidir, tanı değildir")**, model sürüm etiketi |
| E5 Isı haritası | Eksenel/koronal/sagittal senkronize 3 düzlem dilim kaydırıcıları, LRP / Grad-CAM şeffaflık ve eşikleme filtreleri, AAL atlası anatomik bölge etiketi |
| E6 Rapor | Kurumsal başlıklı, hipokampus kesitli, sorumluluk reddi beyanlı PDF önizleme ve indirme |
| E7 Model karşılaştırma | Araştırmacı modu: SONUCLAR.md tablosu, interaktif ROC eğrileri, karışıklık matrisleri, OASIS-1 dış test genellenebilirlik grafiği |
> **Mock-up Dosyaları:** Görkem tarafından hazırlanan detaylı spesifikasyon [`rapor/sekiller/mockups_spec.md`](file:///c:/Users/atomk/OneDrive/Masaüstü/tasarim-alzheimer/rapor/sekiller/mockups_spec.md) ve `rapor/sekiller/mockup_E1..E7.png`. Teknoloji: FastAPI + HTML5/CSS3/JS veya Streamlit.

### 4.4 Akış diyagramları
- **A1 Ön işleme akışı:** NIfTI/DICOM → (DICOM ise dcm2niix) → HD-BET maske → N4 → maske içi z-score → MNI152 afin → 128³ kırpma/yeniden örnekleme → kalite kontrol (boş hacim? oryantasyon?) → `.npy` + meta JSON.
- **A2 Eğitim/değerlendirme akışı:** bölme CSV → 5 kat × 3 tohum döngüsü → eğitim (AMP, erken durdurma) → doğrulama metrikleri → test metrikleri → tablo + ROC + karışıklık matrisi → SONUCLAR.md.
- **A3 Tahmin akışı (üretim):** API isteği → doğrulama → ön işleme (A1) → onnxruntime → softmax → karar eşiği → ısı haritası → DB kaydı → JSON/PDF.
> **Diyagram Dosyaları:** Ertuğrul tarafından hazırlanan PlantUML akış diyagramları:
> 1. Ön İşleme Akışı: [`rapor/sekiller/akis_onisleme.puml`](file:///c:/Users/atomk/OneDrive/Masaüstü/tasarim-alzheimer/rapor/sekiller/akis_onisleme.puml) (`akis_onisleme.png`)
> 2. Eğitim & Çapraz Doğrulama Akışı: [`rapor/sekiller/akis_egitim.puml`](file:///c:/Users/atomk/OneDrive/Masaüstü/tasarim-alzheimer/rapor/sekiller/akis_egitim.puml) (`akis_egitim.png`)
> 3. Klinik Tahmin & Karar Destek Akışı: [`rapor/sekiller/akis_tahmin.puml`](file:///c:/Users/atomk/OneDrive/Masaüstü/tasarim-alzheimer/rapor/sekiller/akis_tahmin.puml) (`akis_tahmin.png`)


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
