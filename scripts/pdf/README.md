# Pembuatan PDF

Generator PDF Week 10, Week 11, Week 12, dan Week 13 berada di folder ini. Semuanya membaca
data/laporan agregat yang sudah tersedia, tanpa melatih ulang model.

Kebutuhan: Python dengan ReportLab dan pypdf, serta font Arial, Times New Roman
dan Consolas di `C:/Windows/Fonts/`. Generator saat ini ditujukan untuk Windows.
Dependensi PDF terpisah dari environment training model.

```powershell
python -m pip install reportlab pypdf
python scripts/pdf/build_week10.py
python scripts/pdf/build_week11.py
python scripts/pdf/build_week12.py
python scripts/pdf/build_week13.py
```

Keluaran ada di `output/pdf/` (lokal, diabaikan Git). Salinan PDF final yang
dibagikan lewat repo ada di `docs/week-10/`, `docs/week-11/`, `docs/week-12/`, dan `docs/week-13/`. Perbarui
salinannya setelah merevisi dan memeriksa hasil generator. Logo cover berada
di `docs/assets/logo-ukwms.png`.

Week 10 memuat lampiran kode administrasi lengkap. Generator Week 13 juga
menulis `docs/week-13/laporan-pertama.md` dari konten yang sama dengan PDF.
Jika perlu mengubah isi laporan, edit generator agar PDF dan Markdown konsisten.

Artikel Week 15 dan rekap percobaan Week 14 memakai sumber Markdown:

```powershell
python scripts/pdf/build_article.py
```

Generator ini memeriksa tabel artikel terhadap metadata/CSV dan mencatat hash
sumber di `docs/artikel/sumber-angka.json`. Hasil final setelah pemeriksaan
visual disalin dari `output/pdf/` ke `docs/artikel/` dan `docs/week-14/`.
