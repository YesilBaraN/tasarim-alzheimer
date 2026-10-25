# P11 — Qiu 2020: FCN yama + hastalık olasılık haritası + MLP (Ertuğrul)

- **Makale:** https://pmc.ncbi.nlm.nih.gov/articles/PMC7296847/ (Brain 2020)
- **Açık kod:** https://github.com/vkola-lab/brain2020 — **MIT**, PyTorch (`model.py`, `main.py`, `config.json`). FSL ön işleme kullanıyor; **biz kendi `onisle.py` çıktımızı kullanırız** (PROTOKOL madde 3).
- **Fikir:** 47³ yamalar üzerinde eğitilen FCN tüm hacimde kaydırılarak "hastalık olasılık haritası" üretir; harita + (isteğe bağlı) yaş/cinsiyet/MMSE → MLP. Bizde ilk sürüm yalnızca MRI (MLP girdisi = harita).

## Yapılacaklar
1. Depoyu klonla (klasör dışına), `LICENSE` kopyala. `model.py`'deki FCN sınıfını bu klasöre al (kaynak satırını yorumla belirt).
2. Yama örnekleyici: ortak Dataset'ten 128³ hacim → rastgele 47³ yamalar (eğitim), kaydırmalı tam harita (test). Yama **denek içinde**; bölme yine denek düzeyinde.
3. `model.py`: `olustur(varyant='fcn', ...)` → FCN; `harita.py` → olasılık haritası + PNG.
4. Eğitim: ortak `egit.py` yama modunu desteklemiyor → `calistir.py` ile sarmala ama **aynı bölme CSV, aynı metrikler, aynı bütçe** (PROTOKOL).
5. P11 notu §12: makale 4 kohort (ADNI/AIBL/FHS/NACC) kullanıyor; biz ADNI1 + OASIS-1 dış test.
