# Week 11 — pipeline awal preprocessing, mining dan evaluasi

Dokumen siap baca: [PDF week 11](week-11-data-mining-kelompok-1.pdf).

Tanggal kelas dan eksekusi lokal: 3 November 2026. Tahap ini menghubungkan
pipeline awal untuk tugas coding week 11–12; tuning dan evaluasi final bukan
klaim penyelesaian pada dokumen ini.

## Alur yang sudah dijalankan

1. Membaca data asli dan memvalidasi struktur, ID serta target.
2. Menormalkan missing dan kode tidak diketahui; mengecualikan discharge
   meninggal sesuai pilihan cohort yang didokumentasikan.
3. Membagi pasien train/validation/test dengan seed 42 tanpa overlap pasien.
4. Menentukan kolom missing tinggi/konstan, imputasi, scaling dan encoding
   berdasarkan train saja; validation/test memakai transformer yang sama.
5. Fit adapter SVD 32 komponen dan scaling pada train; representasi yang sama
   digunakan baseline prior, NGBoost dan Rotation Forest.
6. Menghitung metrik dan confusion matrix pada validation saja, threshold 0,5.

## Hasil preprocessing

| Hasil | Nilai |
|---|---|
| Baris asli | 101.766 |
| Kunjungan meninggal dikeluarkan | 1.652 |
| Baris setelah cleaning/cohort | 100.114 |
| Train / validation / test | 70.071 / 15.065 / 14.978 baris |
| Pasien train / validation / test | 49.307 / 10.566 / 10.566 |
| Overlap pasien antarset | 0 |
| Fitur awal / setelah seleksi train | 47 / 43 |
| Fitur setelah encoding | 1.222 |
| Fitur kontinu setelah adapter SVD | 32, adapter fit hanya pada train |
| Kolom missing >50% train | weight |
| Kolom konstan pada train | acetohexamide, examide, citoglipton |

Rincian missing dan aturan cleaning ada di [panduan preprocessing](../preprocessing.md)
dan [laporan otomatis](../../results/preprocessing/preprocessing_report.md).

## Mining dan evaluasi awal

Hasil angka aktual, interpretasi dan confusion matrix tersedia pada
[laporan percobaan week 11](../../results/week-11/report.md).
Tabel mesin: [validation_metrics.csv](../../results/week-11/validation_metrics.csv).
Parameter, seed, versi preprocessing, waktu proses dan pernyataan test tidak
dievaluasi: [experiment.json](../../results/week-11/experiment.json).

Metrik: average precision (utama), Brier score, log loss, kurva kalibrasi,
ROC-AUC, precision, recall, F1, accuracy,
balanced accuracy dan TN/FP/FN/TP. Nilai precision/recall/F1 mengacu kelas
positif `<30`, bukan rata-rata kedua kelas. AP dihitung dari probabilitas;
threshold 0,5 hanya untuk prediksi label. Parameter dan threshold belum dituning. Semua model memakai adapter kontinu
TruncatedSVD 32 komponen dan StandardScaler yang sama, fit train saja. SVD dapat
membuang informasi penting; ablasi jumlah komponen menjadi pekerjaan berikutnya.
Baseline prior memberi probabilitas prevalensi train. Tidak ada pembobotan kelas.
Hasil lama LR/RF dan source reproduksinya tersedia di results/archive/week-11-lr-rf
dan src/mining_legacy.py; representasi serta pembobotannya berbeda.

## Cara menjalankan dari root repo

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.preprocess --input "C:\lokasi\diabetes+130-us+hospitals+for+years+1999-2008.zip"
.\.venv\Scripts\python.exe -m src.profile_data
.\.venv\Scripts\python.exe -m src.mining
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Sesudah ekstraksi, preprocessing dapat dijalankan tanpa `--input`.
Notebook pendamping: [preprocessing](../../notebooks/01_preprocessing.ipynb)
dan [pipeline awal week 11](../../notebooks/02_week11_mining.ipynb).
Jupyter/ipykernel diinstal terpisah bila memakai notebook; CLI tidak membutuhkannya.

## Berkas hasil

Kode di `src/` dan dokumentasi/hasil agregat dapat disimpan di repo.
Data asli, matriks, transformer, model joblib dan prediksi per baris berada
lokal di `data/` yang diabaikan Git. Model dan prediksi validation ada di
`data/processed/diabetes/models_paper/`. Urutan prediksi sama dengan y_validation.csv
dan ids_validation.csv. Jangan memasukkan ID sebagai prediktor.

## Batas hasil dan tindak lanjut week 12

- Satu split pasien, tanpa CV/tuning; hasil validation bukan uji final.
- Tidak ada pembobotan/oversampling dan tidak ada kalibrasi pascatraining; threshold operasional
  membutuhkan kajian terpisah. Tidak memilih threshold dari test.
- CV berikutnya harus split berbasis pasien dan refit semua preprocessing pada
  setiap fold, dari data sebelum seleksi/transformasi berbasis statistik.
- Analisis kesalahan lebih rinci, variasi parameter dan pemeriksaan performa
  antar kelompok demografi dapat dilanjutkan pada week 12.
- Split tidak temporal dan tidak menguji rumah sakit baru. Test tetap disimpan
  untuk evaluasi final setelah pilihan dibekukan.

## Revisi algoritma untuk arah paper

NGBoost dan Rotation Forest adalah pilihan eksperimen utama, bukan klaim
pertama pada dataset. Penelusuran awal dan keterbatasannya ada pada
[catatan literatur](../algorithm-review.md). Tidak ada skor uji final.
Adapter SVD dapat memengaruhi sinyal diagnosis langka; ablasi dan CV berbasis
pasien masih diperlukan. Kualitas probabilitas dinilai pada prevalensi asli
validation, tanpa balancing atau kalibrasi pascatraining.

## Ringkasan revisi hasil

| Model | AP | Brier score | Log loss | Recall pada 0,5 |
|---|---|---|---|---|
| Dummy_prior | 0.1101 | 0.0980 | 0.3468 | 0.0000 |
| NGBoost | 0.1993 | 0.0948 | 0.3329 | 0.0000 |
| Rotation_Forest | 0.1568 | 0.1010 | 0.6968 | 0.0205 |

AP lebih tinggi lebih baik; Brier/log loss lebih rendah lebih baik.
NGBoost tidak memprediksi kelas positif pada threshold 0,5. Rotation Forest
mengenali 34 dari 1.659 kasus positif. Ini hasil awal tanpa tuning, bukan hasil
akhir yang siap digunakan. SVD menjelaskan 76,10% variasi fitur train; angka ini
bukan jumlah informasi target yang dipertahankan.
