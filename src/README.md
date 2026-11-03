# Fungsi bersama

Simpan fungsi yang digunakan lebih dari satu notebook, misalnya pembacaan
data, preprocessing, atau evaluasi. Buat modul ketika dibutuhkan oleh kode.

`preprocess.py` berisi cleaning, split pasien, transformasi dan ekspor hasil
Diabetes. Jalankan `python -m src.preprocess --help` dari root repo.
Lihat [panduan preprocessing](../docs/preprocessing.md).

`profile_data.py` menghasilkan bahan karakteristik week 10. `mining.py`
menjalankan baseline dan NGBoost/Rotation Forest, mengevaluasi validation saja.
Jalankan `python -m src.profile_data` lalu `python -m src.mining` dari root repo.
