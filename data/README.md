# Dataset

Dataset dipilih: **Diabetes 130-US Hospitals for Years 1999-2008**.
ZIP diberikan pengguna pada 3 November 2026; waktu unduh asli tidak diketahui.
Sumber: [UCI](https://archive.ics.uci.edu/dataset/296/diabetes-130-us-hospitals-for-years-1999-2008).
Pembuat: Clore, Cios, DeShazo, dan Strack (2014), DOI `10.24432/C5230J`, CC BY 4.0.
Arsip berisi `diabetic_data.csv` dan `IDS_mapping.csv`.

CSV aktual memiliki 101.766 baris, 50 kolom dan 71.518 pasien. Satu baris adalah
kunjungan rawat inap. Angka 47 fitur pada UCI tidak termasuk dua ID dan target.
Target asli `readmitted`: `NO`, `>30`, `<30`; default pipeline `<30=1`, lainnya 0.
Sumber dan lisensi wajib diatribusikan jika membagikan ulang.

Data asli sekarang disertakan di GitHub: `raw/diabetic_data.csv` (19.159.383 byte,
sekitar 19,16 MB) dan `raw/IDS_mapping.csv` (2.547 byte). Setelah clone dan
instalasi dependensi, jalankan `python -m src.preprocess` tanpa mengunduh ulang.
Keduanya memakai Git biasa; Git LFS tidak diperlukan untuk ukuran ini.
Hasil terolah, matriks dan model tetap lokal serta diabaikan Git.

Untuk memperoleh ulang dari sumber, jalankan
`python -m src.preprocess --input "lokasi.zip"` dengan ZIP UCI. Pipeline
menyalin file asli tanpa mengubah isi byte. `.gitattributes` menonaktifkan
konversi line ending untuk kedua CSV agar hash sumber tetap sama:
`0689e7ec031237dc63031b938805c48377748761a3b26acab621567afa24df97`
untuk diabetic_data.csv. Lihat [panduan preprocessing](../docs/preprocessing.md).

Salinan CSV identik juga tersedia di [Kaggle](https://www.kaggle.com/datasets/brandao/diabetes).
Pemeriksaan kesamaannya ada di [analisis sumber](../docs/kaggle-dataset-review.md).

Catatan dataset yang dilengkapi bersama kelompok:

- Nama, pembuat, dan tautan sumber asli.
- Tanggal pengambilan, versi, dan cara mengunduhnya.
- Izin penggunaan dan pembagian ulang.
- Jumlah baris/kolom, unit observasi, target, dan distribusi kelas.
- Kamus kolom, tipe data, satuan, dan keterbatasan.

`raw/` menyimpan data asli; `processed/` menyimpan hasil preprocessing.
Untuk data besar atau yang tidak boleh dibagikan ulang, sertakan tautan dan
petunjuk pengambilan alih-alih mengunggah berkasnya. Tentukan penggunaan
Git LFS setelah ukuran dataset diketahui.
