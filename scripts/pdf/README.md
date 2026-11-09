# Pembuatan PDF

Generator PDF Week 10, Week 11, dan Week 12 berada di folder ini. Ketiganya membaca
data/laporan agregat yang sudah tersedia, tanpa melatih ulang model.

Kebutuhan: Python dengan ReportLab dan pypdf, serta font Arial, Times New Roman
dan Consolas di `C:/Windows/Fonts/`. Generator saat ini ditujukan untuk Windows.
Dependensi PDF terpisah dari environment training model.

```powershell
python -m pip install reportlab pypdf
python scripts/pdf/build_week10.py
python scripts/pdf/build_week11.py
python scripts/pdf/build_week12.py
```

Keluaran ada di `output/pdf/` (lokal, diabaikan Git). Salinan PDF final yang
dibagikan lewat repo ada di `docs/week-10/`, `docs/week-11/`, dan `docs/week-12/`. Perbarui
salinannya setelah merevisi dan memeriksa hasil generator. Logo cover berada
di `docs/assets/logo-ukwms.png`.
