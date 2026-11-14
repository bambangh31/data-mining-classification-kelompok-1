# Week 13 Laporan pertama

Laporan pertama sudah disusun dari hasil nyata Week 10-12 serta revisi dosen.
Pembaruan: 14 November 2026. Dokumen ini terpisah dari laporan tiap minggu.

- [PDF laporan pertama](week-13-data-mining-kelompok-1.pdf)
- [Sumber isi yang dapat diedit](laporan-pertama.md)
- [Generator PDF dan Markdown](../../scripts/pdf/build_week13.py)

Cakupan: tujuan/BOD, dataset dan kode kategori, preprocessing, split pasien,
NGBoost/Rotation Forest/baseline, hasil validation Week 11, hasil uji historis
Week 12, percobaan oversampling dan pemilihan ambang pada validation, pembahasan,
keterbatasan, kesimpulan serta reproduksi.

Setelah pemilihan ambang F1 maksimum, NGBoost biasa memperoleh F1 0,2540
dan NGBoost + ROS 0,2534 pada validation. Oversampling belum menunjukkan
keunggulan yang jelas pada percobaan ini. Angka tersebut dihitung pada set
yang juga dipakai memilih ambang; bukan hasil uji independen.

Hasil test Week 12 berasal dari model historis, bukan model revisi.
Artikel bahasa Indonesia dengan struktur IMRAD dan slide presentasi belum dibuat.
Laporan tersedia di repository; ini tidak menyatakan pengumpulan ke LMS atau
persetujuan dosen sudah dilakukan.

## Pemisahan berkas pengumpulan

| Minggu | Keluaran | Lokasi PDF |
|---|---|---|
| 10 | Dataset, karakteristik, BOD dan algoritma | [Week 10](../week-10/week-10-data-mining-kelompok-1.pdf) |
| 11 | Preprocessing, mining dan evaluasi awal | [Week 11](../week-11/week-11-data-mining-kelompok-1.pdf) |
| 12 | Pemilihan ambang, evaluasi uji dan analisis kesalahan | [Week 12](../week-12/week-12-data-mining-kelompok-1.pdf) |
| 13 | Laporan pertama yang menyatukan hasil dan revisi | [Week 13](week-13-data-mining-kelompok-1.pdf) |

## Membuat ulang

Jalankan generator setelah semua hasil agregat tersedia. Gunakan environment
PDF dengan ReportLab dan pypdf, terpisah dari environment training.

```powershell
python scripts/pdf/build_week13.py
```

PDF dibuat di `output/pdf/`; setelah render dan pemeriksaan visual, salin
hasil final ke folder ini. Markdown dibuat langsung di folder ini.
