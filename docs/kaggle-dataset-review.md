# Analisis sumber Kaggle dan kesesuaian dengan dataset proyek

Pemeriksaan: 3 November 2026. Kaggle:
[brandao/diabetes](https://www.kaggle.com/datasets/brandao/diabetes), versi 1.
Nama: Diabetes 130 US hospitals for years 1999-2008, diunggah oleh Humberto
Brandao. Deskripsi Kaggle merujuk dataset UCI sebagai sumber asli.

## Kesamaan CSV dibuktikan langsung

CSV dari ZIP Kaggle versi 1 diunduh dan dibandingkan dengan data/raw/diabetic_data.csv
yang berasal dari ZIP UCI. Hasilnya identik byte demi byte, bukan hanya sama nama,
ukuran atau jumlah baris. Keduanya berukuran 19.159.383 byte dan memiliki SHA-256:

`0689e7ec031237dc63031b938805c48377748761a3b26acab621567afa24df97`

Bukti mesin: [kaggle_source_verification.json](../results/dataset/kaggle_source_verification.json).
Tidak ada perubahan data, preprocessing, hasil model atau PDF pada pemeriksaan ini.
Training tidak perlu diulang hanya karena menambahkan tautan Kaggle.

## Karakteristik yang berlaku pada kedua salinan

| Bagian | Hasil aktual |
|---|---|
| Unit observasi | Kunjungan rawat inap pasien dengan diabetes |
| Baris / kolom | 101.766 / 50 |
| Pasien berbeda | 71.518 |
| Fitur | 47, di luar 2 ID dan 1 target |
| Target NO | 54.864 baris |
| Target >30 | 35.545 baris |
| Target <30 | 11.357 baris (sekitar 11,16%) |
| Duplikasi baris / encounter_id | 0 / 0 |
| Missing penting | weight 98.569; medical_specialty 49.949; payer_code 40.256 |

Dataset mengukur readmission, bukan diabetes/non-diabetes. Target asli memiliki
tiga kelas. Pembentukan `<30=1`, lainnya 0 adalah keputusan proyek yang sesuai
dengan fokus readmission dini, bukan label biner yang sudah disediakan Kaggle.

Pasien dapat muncul dalam beberapa kunjungan, sehingga split harus berbasis
patient_nbr. Kolom ID tidak menjadi prediktor. None pada hasil lab tetap berarti
tes tidak dilakukan; tidak dibaca sebagai missing otomatis. Kelas positif sedikit,
sehingga akurasi saja tidak cukup. Tidak ada tanggal kunjungan dan pengenal rumah
sakit eksplisit pada CSV ini untuk langsung mengklaim validasi temporal/site.
Hubungan fitur dengan readmission bukan bukti penyebab atau kegagalan terapi.

## Perbedaan paket dan metadata

| Bagian | Kaggle versi 1 | Paket UCI yang dipakai proyek |
|---|---|---|
| CSV | diabetic_data.csv; identik | diabetic_data.csv; identik |
| Berkas pendukung | description.pdf (1.492.915 byte) | IDS_mapping.csv (2.547 byte) |
| Label lisensi sumber | CC0: Public Domain | CC BY 4.0 |

Label lisensi diambil dari metadata resmi Kaggle dan halaman UCI, bukan
disimpulkan dari kesamaan hash. Catat keduanya; atribusi dataset asli dan DOI
UCI tetap dipertahankan pada paper/proyek. Tidak menyatakan pengunggah Kaggle
sebagai pencipta asli data klinis.

Loader ZIP saat ini mengharapkan diabetic_data.csv dan IDS_mapping.csv dari
paket UCI. Karena ZIP Kaggle tidak berisi mapping, jangan memasukkan ZIP Kaggle
langsung ke loader ini tanpa penyesuaian. Untuk alur saat ini gunakan ZIP UCI
atau CSV lokal yang sudah diverifikasi; IDS_mapping.csv UCI tetap rujukan kode.

## Implikasi untuk penelitian

Kaggle adalah lokasi distribusi alternatif untuk CSV yang sama. Berpindah tautan
tidak menghasilkan dataset baru atau kebaruan paper. Eksperimen NGBoost/Rotation
Forest yang ada tetap memakai data yang sesuai, tetapi hasil threshold 0,5 masih
lemah dan perlu pengembangan metodologis seperti yang dicatat pada week 11.
Pertahankan source/version, hash, target, cohort dan split yang sama agar dapat
direproduksi. Bila sumber Kaggle ditambahkan ke PDF, tampilkan sebagai sumber
unduhan alternatif dan tetap cantumkan rujukan asli UCI.

## Sumber pemeriksaan

- [Halaman Kaggle](https://www.kaggle.com/datasets/brandao/diabetes).
- [Metadata resmi Kaggle](https://www.kaggle.com/api/v1/datasets/view/brandao/diabetes).
- [Daftar berkas resmi Kaggle](https://www.kaggle.com/api/v1/datasets/list/brandao/diabetes).
- [Dataset asli UCI](https://archive.ics.uci.edu/dataset/296/diabetes-130-us-hospitals-for-years-1999-2008),
  DOI [10.24432/C5230J](https://doi.org/10.24432/C5230J).
