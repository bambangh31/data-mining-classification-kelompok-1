# Preprocessing Diabetes

Implementasi dan eksekusi lokal: 3 November 2026. Cakupan: cleaning, pembagian
data dan transformasi. Modul ini tidak melatih model; percobaan dan evaluasi
awal terpisah pada [week 11](week-11/README.md).

## Masalah dan tujuan/BOD awal

Pertanyaan: apakah kunjungan pasien diabetes akan diikuti rawat inap ulang dalam
kurang dari 30 hari? Unit observasi adalah kunjungan, bukan satu pasien.
Tujuannya menyiapkan data untuk membandingkan dua algoritma klasifikasi.
Prediksi dirancang pada waktu pasien keluar rumah sakit, sehingga informasi
selama kunjungan boleh digunakan. Dataset ini bukan diagnosis diabetes/non-diabetes.
Rumusan BOD awal mengikuti istilah/template dosen saat difinalisasi.
Manfaat akademiknya mempelajari pola readmission; data historis AS tidak otomatis
mewakili kondisi rumah sakit Indonesia.

Sumber: [UCI](https://archive.ics.uci.edu/dataset/296/diabetes-130-us-hospitals-for-years-1999-2008),
Clore, Cios, DeShazo, dan Strack (2014), DOI `10.24432/C5230J`, CC BY 4.0.
Kode administrasi mengikuti `IDS_mapping.csv` pada arsip asli.

## Target dan cohort awal

- Default binary: `<30=1`, `NO=0`, `>30=0`. Kelas 0 berarti tidak tercatat
  readmission kurang dari 30 hari, bukan tidak pernah readmission. Batas label
  asli dipertahankan, tidak diganti menjadi <=30.
- Opsi multiclass: `NO=0`, `>30=1`, `<30=2`. Simpan pada folder eksperimen terpisah.
- Kunjungan dengan discharge meninggal (`11,19,20,21`) dikeluarkan berdasarkan
  mapping. Ini keputusan cohort awal, bukan aturan wajib UCI. Kunjungan sebelumnya
  dari pasien tersebut tetap dipertahankan. Status hospice/transfer lain tetap ada
  dan menjadi keterbatasan cohort. Target/cohort perlu disepakati kelompok.
- Semua kunjungan lain dipertahankan. Pasien berulang tidak boleh masuk set berbeda.

## Cleaning

1. Baca string dengan `keep_default_na=False`, trim spasi, ubah `?` dan kosong
   menjadi missing. `None` pada `max_glu_serum`/`A1Cresult` tetap kategori
   tes tidak dilakukan, bukan missing CSV.
2. Hapus baris duplikat persis bila ada. ID kosong, ID kunjungan konflik atau
   target tidak dikenal menghentikan proses untuk review manual.
3. `Unknown/Invalid` pada gender menjadi missing tanpa menghapus barisnya.
4. Kode administrasi tidak diketahui menjadi missing: admission type `5,6,8`;
   discharge `18,25,26`; admission source `9,15,17,20,21`.
5. Delapan fitur hitungan menjadi numerik. Hitungan negatif/non-integer atau
   lama rawat di luar 1–14 hari menghentikan proses. Nilai ekstrem yang valid
   tidak dibuang otomatis. Diagnosis tetap kategori, termasuk kode V/E.
6. `encounter_id`, `patient_nbr`, dan target asli tidak masuk fitur model.

## Split dan transformasi

`GroupShuffleSplit`, seed 42: sekitar 70% pasien train, 15% validation, 15% test.
Persentase baris dapat berbeda karena jumlah kunjungan per pasien berbeda.
Split tidak stratified; distribusi kelas dicatat. Semua kelas wajib tersedia
dan overlap pasien antarset wajib nol. Pembagian bukan temporal; ID kunjungan
tidak dianggap tanggal. Hasil menilai pasien berbeda, bukan prediksi masa depan.

Hanya dari train: keluarkan kolom missing >50% dan kolom konstan; imputasi fitur
numerik dengan median lalu StandardScaler; imputasi kategori dengan
`__MISSING__`, lalu one-hot encoding. Kategori berfrekuensi <10 pada train
digabung sebagai infrequent. Kategori baru memakai kelompok tersebut jika ada,
atau semua nol jika tidak ada. Validation/test hanya di-transform, tidak di-fit.
Scaling disediakan untuk model yang membutuhkannya. Tidak ada oversampling
sebelum split. Untuk CV, split pasien dan fit ulang transformer pada setiap fold.
Jangan memakai matriks yang telah di-fit seluruh train untuk mengklaim CV tanpa
kebocoran. Fitur usia/ras/gender masih dipertahankan; evaluasi bias belum dilakukan.

## Menjalankan dari root repo (Python 3.12)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.preprocess --input "C:\lokasi\diabetes+130-us+hospitals+for+years+1999-2008.zip"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Sesudah ekstraksi, jalankan tanpa `--input` untuk membaca `data/raw/diabetic_data.csv`.
Untuk tiga kelas, gunakan output/laporan berbeda:

```powershell
.\.venv\Scripts\python.exe -m src.preprocess --target multiclass --output data/processed/diabetes_multiclass --reports results/preprocessing_multiclass
```

## Penggunaan hasil untuk pemodelan dan evaluasi

Semua berkas berikut berada di `data/processed/diabetes/` dan diabaikan Git:

| Berkas | Isi |
|---|---|
| `cleaned.csv` | Data setelah cleaning, masih dengan ID/target asli; jangan langsung dipakai sebagai X |
| `X_train.npz`, `X_validation.npz`, `X_test.npz` | Matriks sparse siap model, dibaca `scipy.sparse.load_npz` |
| `y_train.csv`, `y_validation.csv`, `y_test.csv` | Target, urutan baris sama dengan X |
| `X_train.csv`, `X_validation.csv`, `X_test.csv` | Fitur sebelum imputasi/encoding, tanpa ID/target; missing masih boleh ada |
| `ids_train.csv`, `ids_validation.csv`, `ids_test.csv` | Metadata ID untuk pelacakan/CV kelompok, bukan fitur |
| `feature_names.json`, `feature_schema.json` | Nama fitur encoded dan keputusan kolom |
| `preprocessor.joblib` | Transformer yang di-fit pada train; muat hanya artefak tepercaya |
| `metadata.json` | Hash CSV asli, versi library, seed, target, konfigurasi dan distribusi |

Model dilatih pada train dan parameter dipilih lewat validation.
Perbandingan model memakai set yang sama. Test disimpan untuk evaluasi final
sesudah konfigurasi dibekukan. Jangan memilih model berdasarkan skor test.

## Bukti eksekusi

- [Laporan hasil otomatis](../results/preprocessing/preprocessing_report.md).
- [Ringkasan dan konfigurasi](../results/preprocessing/preprocessing_summary.json).
- [Rekap missing value](../results/preprocessing/missing_values.csv).

Kode memeriksa fitur konsisten, matriks bebas NaN/Inf dan pasien terpisah antarset.
Tes perilaku mencakup arti None, target, kode tidak diketahui, ID konflik,
split reproducible dan statistik transformasi yang tidak belajar dari validation.
Skor model awal tersedia pada laporan week 11, bukan evaluasi final atau kesimpulan klinis.
