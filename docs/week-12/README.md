# Week 12 — Tuning ambang dan evaluasi uji

Week 12 menggunakan preprocessing dan model terlatih Week 11. Target positif
adalah rawat inap ulang dalam waktu kurang dari 30 hari. Ambang dipilih dengan
F1 kelas positif pada validasi. NGBoost ditetapkan sebagai model utama
berdasarkan Average Precision (AP) validasi sebelum melihat set uji.

| Model | Ambang | AP uji | F1 uji | Precision uji | Recall uji |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dummy prior | 0,5000 | 0,1156 | 0,0000 | 0,0000 | 0,0000 |
| NGBoost | 0,1438 | 0,2068 | 0,2606 | 0,2237 | 0,3120 |
| Rotation Forest | 0,2000 | 0,1573 | 0,2265 | 0,1647 | 0,3628 |

Set uji mencakup 14.978 kunjungan dari 10.566 pasien dan 1.731 kasus positif.
NGBoost mendeteksi 540 kasus positif dengan 1.874 peringatan salah. Rotation
Forest mendeteksi 628 kasus positif dengan 3.186 peringatan salah. Angka
tersebut menggambarkan trade-off pada ambang yang dipilih di validasi.
Set ini sudah digunakan untuk penilaian. Jika konfigurasi kelak dipilih dari
temuan uji ini, penilaian independen membutuhkan set uji lain.

- [Laporan Week 12 dalam PDF](week-12-data-mining-kelompok-1.pdf)
- [Protokol dan ambang lengkap](../../results/week-12/protocol.json)
- [Laporan, analisis kesalahan, dan grafik](../../results/week-12/test/report.md)
- [Tabel metrik uji](../../results/week-12/test/metrics.csv)

## Reproduksi

Dengan Python 3.12 dan dependensi proyek. Bila artefak lokal belum ada,
jalankan preprocessing dan Week 11 terlebih dahulu. Simpan hasil Week 11
reproduksi di folder terpisah agar pembanding validasi cocok dengan model
yang baru dilatih.

```powershell
.\.venv\Scripts\python.exe -m src.preprocess
.\.venv\Scripts\python.exe -m src.mining --output tmp/week11-repro
.\.venv\Scripts\python.exe -m src.week12 freeze --week11 tmp/week11-repro --output tmp/week12-repro
.\.venv\Scripts\python.exe -m src.week12 evaluate --output tmp/week12-repro
```

Jika artefak Week 11 asli masih ada, cukup jalankan dua perintah terakhir
dengan menghapus opsi `--week11 tmp/week11-repro`. Pilih folder output baru
untuk setiap reproduksi. `freeze` memeriksa hasil validasi terhadap Week 11
dan menyimpan hash artefak tanpa membuka set uji. `evaluate` memeriksa hash
dan pemisahan pasien, lalu menulis hasil agregat. ID pasien, prediksi per
baris, dan model tidak disertakan pada hasil yang dilacak Git.
