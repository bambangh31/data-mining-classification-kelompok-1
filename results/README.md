# Hasil eksperimen

- `dataset/`: profil asli, kamus, contoh subset data dan grafik karakteristik.
- `week-11/`: baseline prior, NGBoost/Rotation Forest, metrik diskriminasi dan kalibrasi validation.
- `revisi-dosen/`: perbandingan NGBoost sebelum/sesudah random oversampling pada train,
  metrik validation, distribusi kelas, dan jawaban pemakaian data train.
- `archive/week-11-lr-rf/`: hasil eksperimen lama LR/RF dengan pipeline berbeda; bukan perbandingan terkontrol.

- `metrics/`: tabel metrik dan konfigurasi percobaan.
- `figures/`: grafik dan confusion matrix.
- `preprocessing/`: laporan agregat, missing value dan metadata preprocessing,
  bukan skor model. Dataset/matriks berada lokal di data/processed.

Setiap hasil perlu menyebutkan versi data/kode, algoritma, parameter, dan
jenis set evaluasi (validasi, CV, atau uji final). Isi hanya dari eksekusi nyata.
