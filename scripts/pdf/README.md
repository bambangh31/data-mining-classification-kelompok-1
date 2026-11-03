# Pembuatan PDF

Generator PDF week 10 dan week 11 berada di folder ini. Keduanya membaca
data/laporan agregat yang sudah tersedia, tanpa melatih ulang model.

Kebutuhan: Python dengan ReportLab dan pypdf, serta font Arial, Times New Roman
dan Consolas di `C:/Windows/Fonts/`. Generator saat ini ditujukan untuk Windows.
Dependensi PDF terpisah dari environment training model.

```powershell
python -m pip install reportlab pypdf
python scripts/pdf/build_week10.py
python scripts/pdf/build_week11.py
```

Keluaran ada di `output/pdf/` (lokal, diabaikan Git). Salinan PDF final yang
dibagikan lewat repo ada di `docs/week-10/` dan `docs/week-11/`; perbarui
salinannya setelah merevisi dan memeriksa hasil generator. Logo cover berada
di `docs/assets/logo-ukwms.png`.
