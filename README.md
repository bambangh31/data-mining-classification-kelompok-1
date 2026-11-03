# Data Mining — Classification Kelompok 1

Proyek mata kuliah Data Mining: preprocessing,
perbandingan algoritma klasifikasi, evaluasi,
dan artikel berbahasa Indonesia dengan struktur IMRAD.

## Anggota

| Nama | NRP |
|---|---|
| Bambang Herlambang | 5803024019 |
| Benedictus Erlangga | 5803024011 |
| Robertus Geraldyn Alexandro Gabeler | 5803024025 |

## Rencana Pengerjaan

- Week 10: dataset, karakteristik data, BOD, dan rencana algoritma.
- Week 11–12: preprocessing, klasifikasi, dan evaluasi.
- Week 13: laporan pertama.
- Week 14: percobaan tambahan jika diminta.
- Week 15: artikel bahasa Indonesia dengan struktur IMRAD.
- Week 16: presentasi.

## Dataset

**Diabetes 130-US Hospitals for Years 1999-2008**, dari
[UCI](https://archive.ics.uci.edu/dataset/296/diabetes-130-us-hospitals-for-years-1999-2008).
Data asli berisi 101.766 kunjungan, 50 kolom dan 71.518 pasien.
Target awal: rawat inap ulang `<30` hari (biner); opsi tiga kelas tersedia.
Data disiapkan untuk prediksi pada saat keluar rumah sakit.
Sumber dan lisensi ada di [data/README.md](data/README.md).

## Algoritma

NGBoost dan Rotation Forest, dengan DummyClassifier(strategy="prior") sebagai baseline.
Percobaan awal sudah dijalankan pada validation; test belum dievaluasi.
Alasan pemilihan dan batas klaim kebaruan ada pada
[penelusuran algoritma](docs/algorithm-review.md). Hasil Logistic Regression/
Random Forest sebelumnya tersedia di results/archive/week-11-lr-rf.
Lihat [bahan week 10](docs/week-10/README.md) dan [hasil week 11](docs/week-11/README.md).

## Cara Menjalankan

Dokumen PDF: [week 10](docs/week-10/week-10-data-mining-kelompok-1.pdf) dan
[week 11](docs/week-11/week-11-data-mining-kelompok-1.pdf).

Gunakan Python 3.12, dari root repo:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.preprocess
.\.venv\Scripts\python.exe -m src.profile_data
.\.venv\Scripts\python.exe -m src.mining
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Dataset asli sudah disertakan di `data/raw/`, sehingga tidak perlu unduh ulang.
Opsi `--input "lokasi.zip"` tetap tersedia untuk ZIP asli UCI.
Lihat [panduan preprocessing](docs/preprocessing.md) dan
[hasil eksekusi](results/preprocessing/preprocessing_report.md).
Tuning, analisis kesalahan lanjutan dan evaluasi final menjadi tahap berikutnya.

## Struktur Repository

```text
.
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── .editorconfig
├── .gitattributes
├── .python-version
├── .gitignore
├── requirements.txt
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   │   └── ci.yml
│   ├── dependabot.yml
│   └── pull_request_template.md
├── data/
│   ├── README.md
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── results/
│   ├── metrics/
│   └── figures/
└── docs/
    ├── project/
    ├── week-10/
    ├── laporan/
    ├── artikel/
    └── presentasi/
```

`src/preprocess.py` dan notebook preprocessing sudah tersedia. Library beserta
versi yang dipakai tercantum di `requirements.txt`. Data/artefak hasil bersifat
lokal dan dapat dibuat ulang; laporan agregat ada di `results/preprocessing/`.

Sumber dan petunjuk dataset ada di [data/README.md](data/README.md).
Data besar atau yang distribusinya dibatasi dapat disertakan melalui tautan
dan petunjuk pengambilan.

## Kontribusi

Ikuti [panduan kontribusi](CONTRIBUTING.md) untuk lingkungan Python, alur PR,
pemeriksaan, dan pencatatan eksperimen. Penanganan kredensial dan data
tercantum di [panduan keamanan](SECURITY.md).

Kalender kelas dan pembagian kontribusi ada di
[panduan kerja kelompok](docs/project/README.md). Hasil pemeriksaan
kelengkapan setup ada di [review setup](docs/project/review-setup.md).

Gunakan **Issues → New issue** untuk memilih form laporan masalah atau usulan
perubahan. Issue kosong tetap tersedia untuk catatan atau tugas lainnya.

Saat membuat pull request, isi template ringkasan perubahan dan pemeriksaan.

## Python, CI, dan Dependabot

Proyek menggunakan Python. CI memakai Python 3.12 dan berjalan saat push ke
`main`, saat pull request, atau secara manual dari tab **Actions**.

Pemeriksaan awal mencakup pemasangan `requirements.txt`, kompatibilitas
dependensi, sintaks `.py`, serta pengujian perilaku preprocessing dengan data
sintetis, termasuk pemeriksaan metrik. CI tidak menjalankan dataset penuh,
notebook, atau training model.

Dependabot memeriksa library Python di `requirements.txt` dan GitHub Actions
setiap bulan. Pembaruan diajukan melalui pull request untuk diperiksa sebelum
digabung. Pemeriksaan library mulai bermanfaat setelah dependensi ditambahkan.
