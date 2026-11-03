# Arsip eksperimen awal LR/RF

Hasil ini berasal dari Logistic Regression dan Random Forest pada fitur one-hot
1.222 kolom, dengan pembobotan kelas. Hasil dipertahankan untuk keterlacakan.
Jalankan `python -m src.mining_legacy` untuk membuat ulang arsip ini.

Eksperimen utama terbaru berada di `results/week-11/`, menggunakan NGBoost,
Rotation Forest, adapter SVD 32 + scaling dan tanpa pembobotan kelas. Perbedaan
representasi dan pembobotan membuat kedua run bukan perbandingan terkontrol.
Tidak menyimpulkan keunggulan algoritma dari perbedaan skor antar-run tersebut.
