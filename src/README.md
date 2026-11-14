# Fungsi bersama

Simpan fungsi yang digunakan lebih dari satu notebook, misalnya pembacaan
data, preprocessing, atau evaluasi. Buat modul ketika dibutuhkan oleh kode.

`preprocess.py` berisi cleaning, split pasien, transformasi dan ekspor hasil
Diabetes. Jalankan `python -m src.preprocess --help` dari root repo.
Lihat [panduan preprocessing](../docs/preprocessing.md).

`profile_data.py` menghasilkan bahan karakteristik week 10. `mining.py`
menjalankan baseline dan NGBoost/Rotation Forest, mengevaluasi validation saja.
Jalankan `python -m src.profile_data` lalu `python -m src.mining` dari root repo.

`revision.py` menjalankan perbandingan terkontrol NGBoost tanpa oversampling dan
NGBoost + RandomOverSampler (train saja). Jalankan `python -m src.revision`;
hasil di `results/revisi-dosen/`, model lokal di
`data/processed/diabetes/models_revision/`. Runner tidak membaca fitur/target
test dan tidak mengganti artefak Week 11/12.

`revision_thresholds.py` memilih ambang F1 maksimum untuk kedua NGBoost dari
prediksi validation revisi. Jalankan `python -m src.revision_thresholds` tanpa
training ulang. Runner memverifikasi target dan metrik sumber, menyimpan ambang,
hash input, tabel metrik dan grafik. Hasilnya adalah evaluasi pada validation
yang juga dipakai memilih ambang, bukan estimasi uji independen.
