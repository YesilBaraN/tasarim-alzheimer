# 15 Makale — Liste, Gruplama, Atama ve Erişim

Son güncelleme: 25.10.2026 · Hazırlayan: Baran (Claude Code oturumu)

## Neden bu 15?
- Danışman şartı: 3 kişi × 5 makale, her kişi 2 implementasyon, ortak veri seti.
- **Tematik gruplama** seçildi: üç grup birleşince rapor tek bir hikâye anlatır — *düz 3B CNN / ResNet → dikkat ve açıklanabilirlik → yama-FCN, DenseNet ve Transformer* — ve 6 implementasyon farklı mimari aileleri kapsar.
- **Açık erişim ilkesi:** her makalenin tam metni ücretsiz (arXiv / PMC / MDPI / CVF / Frontiers). İmplemente edilenlerin kodu MIT / Apache / BSD lisanslı açık depolardan ya da MONAI'nin hazır sınıflarından kurulur. GPL kod yalnız okunur, kopyalanmaz; lisanssız depo yalnız referans.
- Seçim 24–25.10.2026'da 4 araştırma ajanıyla doğrulandı (27 aday tarandı; DOI, tam metin ve kod depoları tek tek açıldı).

## Grup A — Baran Yeşilyurt (G231210078): "3B CNN temelleri, ResNet omurgası, tekrarlanabilir protokol"
Baran ayrıca ortak veri seti, ön işleme hattı ve karşılaştırma protokolünün sahibi.

| Kod | Makale | Yayın | Tam metin (ücretsiz) | Kod (lisans) | Rol | Durum |
|---|---|---|---|---|---|---|
| P01 | Korolev S. vd. — *Residual and Plain Convolutional Neural Networks for 3D Brain MRI Classification* | IEEE ISBI 2017 | [arXiv:1701.06643](https://arxiv.org/abs/1701.06643) | [neuro-ml/resnet_cnn_mri_adni](https://github.com/neuro-ml/resnet_cnn_mri_adni) (lisans yok, Theano) → yalnız referans | **İMPLEMENTE 1** — 3D-ResNet + VoxCNN, PyTorch/MONAI ile yeniden | AI özeti + Opus doğrulama (bu oturum) |
| P02 | Chen S., Ma K., Zheng Y. — *Med3D: Transfer Learning for 3D Medical Image Analysis* | arXiv 2019 | [arXiv:1904.00625](https://arxiv.org/abs/1904.00625) | [Tencent/MedicalNet](https://github.com/Tencent/MedicalNet) (MIT) | **İMPLEMENTE 2** — MONAI resnet18 + MedicalNet ağırlığı (transfer) | AI özeti + Opus doğrulama (bu oturum) |
| P03 | Wen J. vd. — *Convolutional neural networks for classification of Alzheimer's disease: Overview and reproducible evaluation* | Medical Image Analysis 63 (2020) | [arXiv:1904.07773](https://arxiv.org/abs/1904.07773) | [aramis-lab/clinicadl](https://github.com/aramis-lab/clinicadl) (MIT) | PROTOKOL.md kaynağı; sızıntı türleri; Conv5_FC3 referans | AI özeti + Opus doğrulama (bu oturum) |
| P04 | Folego G. vd. — *Alzheimer's Disease Detection Through Whole-Brain 3D-CNN MRI* | Front. Bioeng. Biotechnol. 8 (2020) | [PMC7661929](https://pmc.ncbi.nlm.nih.gov/articles/PMC7661929/) | [gfolego/alzheimers](https://github.com/gfolego/alzheimers) (Apache-2.0) | Ön işleme zinciri (ANTs → MNI152) + dış test örneği | AI özeti + Opus doğrulama (bu oturum) |
| P05 | Yagis E. vd. — *Effect of data leakage in brain MRI classification using 2D convolutional neural networks* | Scientific Reports 11 (2021) | [Nature OA](https://www.nature.com/articles/s41598-021-01681-w) · [PMC8604922](https://pmc.ncbi.nlm.nih.gov/articles/PMC8604922/) | — | Sızıntı kanıtı → bölme kuralı | AI özeti + Opus doğrulama (bu oturum) |

## Grup B — Ahmet Görkem Yavuz (G231210032): "Dikkat mekanizmaları ve açıklanabilirlik"

| Kod | Makale | Yayın | Tam metin (ücretsiz) | Kod (lisans) | Rol | Durum |
|---|---|---|---|---|---|---|
| P06 | Böhle M. vd. — *Layer-Wise Relevance Propagation for Explaining Deep Neural Network Decisions in MRI-Based Alzheimer's Disease Classification* | Front. Aging Neurosci. 11 (2019) | [PMC6685087](https://pmc.ncbi.nlm.nih.gov/articles/PMC6685087/) | [moboehle/Pytorch-LRP](https://github.com/moboehle/Pytorch-LRP) (BSD-3, PyTorch, ADNI not defterleri) | **İMPLEMENTE** — 3B CNN + LRP ısı haritası | AI özeti + Opus doğrulandı |
| P07 | Zhang X. vd. — *An Explainable 3D Residual Self-Attention Deep Neural Network for Joint Atrophy Localization and Alzheimer's Disease Diagnosis using Structural MRI* (3D ResAttNet) | IEEE J. Biomed. Health Inform. (2021/22) | [arXiv:2008.04024](https://arxiv.org/abs/2008.04024) | resmî kod yok → MONAI ResNet + öz-dikkat bloğu + `monai.visualize.GradCAM` | **İMPLEMENTE** — ResNet + öz-dikkat + Grad-CAM | AI özeti + Opus doğrulandı |
| P08 | Dyrba M. vd. — *Improving 3D convolutional neural network comprehensibility via interactive visualization of relevance maps: evaluation in Alzheimer's disease* | Alzheimer's Res. Ther. (2021) | [arXiv:2012.10294](https://arxiv.org/abs/2012.10294) | [martindyrba/DeepLearningInteractiveVis](https://github.com/martindyrba/DeepLearningInteractiveVis) (MIT, TF 1.15) | okuma — ilgi haritası karşılaştırması | AI özeti + Opus doğrulandı |
| P09 | Hoang G.M. vd. — *A reproducible 3D convolutional neural network with dual attention module (3D-DAM) for Alzheimer's disease classification* | arXiv 2023 | [arXiv:2310.12574](https://arxiv.org/abs/2310.12574) | bulunamadı (PyTorch CBAM türevi) | okuma — dış test (OASIS/AIBL) | AI özeti + Opus doğrulandı |
| P10 | Jin D. vd. — *Generalizable, Reproducible, and Neuroscientifically Interpretable Imaging Biomarkers for Alzheimer's Disease* (3DAN) | Advanced Science (2020) | [PMC7375255](https://pmc.ncbi.nlm.nih.gov/articles/PMC7375255/) | [YongLiuLab](https://github.com/YongLiuLab) (PyTorch 0.3.1) | okuma — 3B dikkat ağı, çok merkezli | AI özeti + Opus doğrulandı |

## Grup C — Ertuğrul Kabaoğlu (G231210376): "Yama/FCN, DenseNet ve Transformer"

| Kod | Makale | Yayın | Tam metin (ücretsiz) | Kod (lisans) | Rol | Durum |
|---|---|---|---|---|---|---|
| P11 | Qiu S. vd. — *Development and validation of an interpretable deep learning framework for Alzheimer's disease classification* | Brain 143 (2020) | [PMC7296847](https://pmc.ncbi.nlm.nih.gov/articles/PMC7296847/) | [vkola-lab/brain2020](https://github.com/vkola-lab/brain2020) (MIT, PyTorch) | **İMPLEMENTE** — FCN yama + risk haritası + MLP | AI özeti + Opus doğrulandı |
| P12 | Solano-Rojas B., Villalón-Fonseca R. — *A Low-Cost Three-Dimensional DenseNet Neural Network for Alzheimer's Disease Early Discovery* | Sensors 21 (2021); 2020 LNCS sürümü [PMC7313295](https://pmc.ncbi.nlm.nih.gov/articles/PMC7313295/) | MDPI açık erişim + PMC | kod yok → `monai.networks.nets.DenseNet121(spatial_dims=3)` (Apache-2.0) | **İMPLEMENTE** — 3B DenseNet121 (veri seti: ADNI, 5 sınıf, tarama sızıntısı analiz edildi) | AI özeti + Opus doğrulandı |
| P13 | Lian C. vd. — *Hierarchical Fully Convolutional Network for Joint Atrophy Localization and Alzheimer's Disease Diagnosis Using Structural MRI* (H-FCN) | IEEE TPAMI 42 (2020) | [PMC6588512](https://pmc.ncbi.nlm.nih.gov/articles/PMC6588512/) | yok (Keras) | okuma — güçlü referans (AD-NC 0.903) | AI özeti + Opus doğrulandı |
| P14 | Jang J., Hwang D. — *M3T: Three-Dimensional Medical Image Classifier Using Multi-Plane and Multi-Slice Transformer* | CVPR 2022 | [CVF açık erişim](https://openaccess.thecvf.com/content/CVPR2022/html/Jang_M3T_Three-Dimensional_Medical_Image_Classifier_Using_Multi-Plane_and_Multi-Slice_Transformer_CVPR_2022_paper.html) | [KVishnuVardhanR/M3T](https://github.com/KVishnuVardhanR/M3T) (GPL-3.0, gayriresmî) → yalnız okunur | okuma — Transformer | AI özeti + Opus doğrulandı |
| P15 | Dhinagar N.J. vd. — *Video and Synthetic MRI Pre-training of 3D Vision Architectures for Neuroimage Analysis* | arXiv 2023 | [arXiv:2309.04651](https://arxiv.org/abs/2309.04651) | yok | okuma — ViT vs CNN, denek bazlı katman protokolü | AI özeti + Opus doğrulandı |

## Altı implementasyon (ortak veri + ortak protokol)
| # | Model | Aile | Kaynak makale | Kim | Açık kod temeli |
|---|---|---|---|---|---|
| 1 | 3D-ResNet + VoxCNN (sıfırdan) | düz 3B CNN / ResNet | P01 | Baran | MONAI blokları, kendi kod |
| 2 | 3D-ResNet-18 (MedicalNet transfer) | transfer öğrenme | P02 | Baran | MONAI resnet18 + MedicalNet (MIT) |
| 3 | 3B CNN + LRP | açıklanabilirlik | P06 | Görkem | Pytorch-LRP (BSD-3) |
| 4 | 3D ResAttNet + Grad-CAM | dikkat | P07 | Görkem | MONAI ResNet + öz-dikkat + MONAI GradCAM |
| 5 | FCN yama + risk haritası | yama / FCN | P11 | Ertuğrul | brain2020 (MIT) |
| 6 | 3D DenseNet121 | DenseNet | P12 | Ertuğrul | MONAI DenseNet121 |

## Yedekler (gerekirse yer değiştirir)
| Makale | Neden yedek | Tam metin | Kod |
|---|---|---|---|
| Ruiz J. vd. 2020 — *3D DenseNet Ensemble in 4-way Classification of AD* (Brain Informatics) | tam metin paywall | Springer | yok |
| Ebrahimi A. vd. 2021 — *CNNs for AD detection on MRI images* (J. Med. Imaging) | kod MATLAB | PubMed "free PMC" | MATLAB File Exchange |
| Yee E. vd. 2021 — *Construction of MRI-Based AD Score Based on Efficient 3D CNN* (JAD) | kod yok | ADNI yayın kopyası | yok |
| Bron E.E. vd. 2021 — *Cross-cohort generalizability of deep and conventional ML for MRI-based AD diagnosis* | SVM vs CNN tartışması | [PMC8203808](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203808/) | GitLab + Zenodo |
| Dhinagar N.J. vd. 2025 — *Parameter Efficient Fine-tuning of Transformer-based MAE…* (SPIE MI) | LoRA fikri | bioRxiv | yok |
| Zhang & Khalvati 2022 — *Introducing ViT for AD classification with 3D input* | "sığ 3B CNN yeter" temel çizgisi | [arXiv:2210.01177](https://arxiv.org/abs/2210.01177) | yok |
| Rumala D.J. 2023 — *How You Split Matters: Data Leakage and Subject Characteristics…* | sızıntı kanıtı (3B) | [arXiv:2309.00350](https://arxiv.org/abs/2309.00350) | yok |
| Dong vd. 2025 — CNN sMRI AD sistematik derleme + meta-analiz (BMC Neurology) | rapor literatür bölümü | [PMC12482330](https://pmc.ncbi.nlm.nih.gov/articles/PMC12482330/) | — |

## Durum sözlüğü
`okunmadı` → `AI özeti hazır` → `Opus doğrulandı` → `insan okudu` → `implemente edildi` (yalnızca implementasyon makaleleri). Durumu değiştiren kişi `SUREC.md` tablosunu da günceller.
