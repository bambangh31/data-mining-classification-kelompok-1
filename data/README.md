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

Unduh ZIP dari sumber, lalu jalankan `python -m src.preprocess --input "lokasi.zip"`.
Pipeline menyalin dua file asli ke raw tanpa mengubah isi byte, serta mencatat
SHA-256 CSV pada metadata/laporan. Data asli/hasil diabaikan Git; tidak perlu
LFS untuk alur ini. Lihat [panduan preprocessing](../docs/preprocessing.md).

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
