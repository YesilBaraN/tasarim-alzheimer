# -*- coding: utf-8 -*-
r"""
model.py — Ortak temel çizgilerin model sözleşmesi girişi (PROTOKOL madde 9).

`egit.py` modelleri `uygulama/<klasor>/model.py` içindeki `olustur(...)` ile kurar. Sığ 3B CNN temel çizgisi
`temel_cizgi.py`'de yaşadığı için ortak eğitim döngüsünden çağrılabilsin diye burada yeniden dışa verilir:

  python uygulama\ortak\egit.py --model ortak --varyant sigcnn --set oasis1 --gorev ikili ...

Voksel tabanlı lineer SVM temel çizgisi epoch'lu eğitim kullanmaz; onun koşucusu `svm_kos.py`.
"""
from uygulama.ortak.temel_cizgi import SigCNN3D, olustur  # noqa: F401

__all__ = ["olustur", "SigCNN3D"]
