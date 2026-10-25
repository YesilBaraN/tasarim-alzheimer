# kosu_kayitlari — koşu kayıtları (ortak alan, depoya GİRER)

Her eğitim koşusu buraya iki dosya bırakır:

| Dosya | Depoya girer mi |
|---|---|
| `<kosu-adi>.json` | ✅ **Evet** — PROTOKOL madde 10'un istediği kayıt: ayarlar, tohum, metrikler, süreler, donanım, commit hash'i, kütüphane sürümleri |
| `<kosu-adi>.pth` ve `<kosu-adi>_son.pth` | ❌ Hayır — ağırlık dosyaları, `.gitignore` dışlıyor (yüzlerce MB) |

Koşu adı: `<model>-<varyant>_<set>_<gorev>_t<tohum>_k<kat>_lr<lr>_b<boyut>[_<etiket>]`
lr ve boyut adın içinde olduğu için LR taraması ve ablation koşuları birbirinin kaydını ezmez.

## Ortak alan kuralı

**Üçümüz kendi koşularımızın JSON'larını buraya commit ederiz.** Tablo tek komutla üretilir:

```powershell
python karsilastirma\tablo_uret.py --set adni1 --gorev ikili
```

Üreteç kendiliğinden ayıklar ve nedenini yazar:
- `gpu` alanı geliştirme kartını gösteriyorsa (KURULUM §0b: RTX 3050 yalnız hata ayıklama için),
- `model_notu` mimari sapma bildiriyorsa (ör. VoxCNN padding=1 — PROTOKOL madde 3),
- `commit` yoksa (`git-yok`).

Yani: **koşuyu commit'lenmiş koddan başlat**, yoksa kaydın tabloya girmez.

JSON dosyaları farklı kişilerden geldiği için çakışma olmaz (her koşunun adı tektir) — bu klasörde
`git pull --rebase` sorunsuz çalışır.
