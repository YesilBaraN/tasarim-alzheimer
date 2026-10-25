# dis_test — dış test (sıfır-atış) sonuçları, depoya GİRER

`uygulama/ortak/dis_test.py` üretir: bir sette eğitilmiş modelin BAŞKA sette, hiç eğitim görmeden
(zero-shot) sonucu. PROTOKOL "Dış test" bölümü bunu zorunlu kılıyor; genelleme düşüşü (iç − dış)
tartışma bölümünün ana konusu.

Dosya adı: `<kosu-adi>_dis-<hedef-set>.json` · `tablo_uret.py` bunları "Dış test BAcc" sütununa koyar.

```powershell
python uygulama\ortak\dis_test.py --model baran_P02_medicalnet --tum_ckpt "*adni1_ikili*" ^
    --dis_set oasis1 --etiket veri\oasis1_etiket.csv --veri D:\veri\oasis1\islenmis ^
    --kaynak_etiket veri\adni1_etiket.csv
```

`--kaynak_etiket` vermeyi ihmal etme: K4 transfer sızıntısı kontrolünü o yapıyor (kaynak setin
denekleri hedef sette görünüyorsa iş durur).
