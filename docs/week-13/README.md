# Week 13 Laporan pertama

Laporan pertama sudah disusun dari hasil nyata Week 10-12 serta revisi dosen.
Pembaruan: 17 November 2026. Dokumen ini terpisah dari laporan tiap minggu.
Versi lengkap terdiri atas 20 halaman: cover, daftar isi otomatis, ringkasan,
14 bab, 20 tabel bernomor, dan 6 gambar termasuk diagram alur penelitian.
Paragraf isi menggunakan Times New Roman 12 dengan rata kanan-kiri.

- [PDF laporan pertama](../laporan/week-13-data-mining-kelompok-1.pdf)
- [Sumber isi yang dapat diedit](laporan-pertama.md)
- [Generator PDF dan Markdown](../../scripts/pdf/build_week13.py)

Cakupan: pendahuluan dan rumusan masalah, tujuan/BOD, risiko dan kriteria
keberhasilan, dataset dan kode kategori, metode, preprocessing, split pasien,
NGBoost/Rotation Forest/baseline, hasil validation Week 11, hasil uji historis
Week 12, percobaan oversampling dan pemilihan ambang pada validation, pembahasan,
keterbatasan, pembagian tugas, bukti pengujian, kesimpulan serta reproduksi.
Struktur laporan dikembangkan mengikuti contoh format yang diberikan pengguna;
isi dan angka tetap berasal dari proyek Data Mining ini.

Setelah pemilihan ambang F1 maksimum, NGBoost biasa memperoleh F1 0,2540
dan NGBoost + ROS 0,2534 pada validation. Oversampling belum menunjukkan
keunggulan yang jelas pada percobaan ini. Angka tersebut dihitung pada set
yang juga dipakai memilih ambang; bukan hasil uji independen.

Hasil test Week 12 berasal dari model historis, bukan model revisi.
Laporan pertama memuat hasil dan revisi dosen untuk tahap Week 13.
Status terbaru: [artikel IMRAD untuk Week 15](../artikel/README.md) sudah disiapkan
lebih awal. Week 14 belum dikerjakan; eksperimen oversampling yang tersedia
merupakan revisi laporan Week 13. Slide presentasi belum dibuat.
Laporan tersedia di repository; ini tidak menyatakan pengumpulan ke LMS atau
persetujuan dosen sudah dilakukan.

## Pemisahan berkas pengumpulan

| Minggu | Keluaran | Lokasi PDF |
|---|---|---|
| 10 | Dataset, karakteristik, BOD dan algoritma | [Week 10](../laporan/week-10-data-mining-kelompok-1.pdf) |
| 11 | Preprocessing, mining dan evaluasi awal | [Week 11](../laporan/week-11-data-mining-kelompok-1.pdf) |
| 12 | Pemilihan ambang, evaluasi uji dan analisis kesalahan | [Week 12](../laporan/week-12-data-mining-kelompok-1.pdf) |
| 13 | Laporan pertama yang menyatukan hasil dan revisi | [Week 13](../laporan/week-13-data-mining-kelompok-1.pdf) |

## Membuat ulang

Jalankan generator setelah semua hasil agregat tersedia. Gunakan environment
PDF dengan ReportLab dan pypdf, terpisah dari environment training.

```powershell
python scripts/pdf/build_week13.py
```

PDF dibuat di `output/pdf/`; setelah render dan pemeriksaan visual, salin
hasil final ke `docs/laporan/`. Markdown dibuat langsung di folder ini.
