# Status implementasi Classification

Pembaruan: 14 November 2026. Status berikut membedakan fondasi repo dari
pekerjaan analisis yang belum dilakukan.

## Sudah tersedia

| Bagian | Hasil | Batas |
|---|---|---|
| Struktur kerja | Dataset asli Diabetes di Git, profil/kamus data, preprocessing, dua model, baseline, serta evaluasi validasi dan uji | Model tetap lokal; CV dan tuning hiperparameter belum dilakukan |
| Dokumen kelompok | CONTRIBUTING, SECURITY, template issue/PR, pembagian tiga anggota dan kalender Selasa | Pembagian adalah rencana yang disesuaikan dengan beban aktual |
| Python | Acuan 3.12, versi pandas/NumPy/SciPy/scikit-learn/joblib/Matplotlib pada requirements.txt | Dependensi pemodelan tambahan mengikuti kebutuhan eksperimen berikutnya |
| CI | Instalasi requirements, pip check, sintaks .py dan tes perilaku preprocessing/metrik sintetis | Tidak melatih model penuh atau menjalankan dataset di CI; status eksekusi diperiksa pada commit terkait |
| Dependabot | Pembaruan pip/Actions bulanan; alerts dan PR perbaikan keamanan | PR perlu ditinjau; bukan pemindaian rahasia atau audit dataset |
| Pengaturan repo | Private, main, squash merge, hapus branch setelah merge | Auto-merge nonaktif; tidak mengklaim branch protection aktif |

CI pada commit `ace1056` sudah berhasil:
[Python CI](https://github.com/bambangh31/data-mining-classification-kelompok-1/actions/runs/41279203504).
Hasil itu membuktikan fondasi saat commit tersebut dapat dijalankan, bukan
akurasi klasifikasi. Periksa CI pada commit terkait untuk perubahan berikutnya.

## Week 10–11 — hasil lokal

Dataset: 101.766 kunjungan, 50 kolom, 71.518 pasien. Cleaning/cohort menghasilkan
100.114 baris; 1.652 kunjungan berstatus meninggal dikeluarkan. Target awal
`<30=1`, lainnya 0. Train/validation/test: 70.071 / 15.065 / 14.978 baris;
pasien antarset terpisah. Transformer di-fit pada train saja, menghasilkan
1.222 fitur. Kolom weight dibuang karena missing >50% pada train;
acetohexamide, examide dan citoglipton konstan pada train.

Kode: `src/preprocess.py`. Cara menjalankan, pilihan cohort, batasan dan
serah terima ada di [panduan](../preprocessing.md). Bukti eksekusi:
[laporan agregat](../../results/preprocessing/preprocessing_report.md).
Sebelas tes preprocessing/metrik/model lolos lokal; artefak/data tetap lokal.
Week 10 mencakup dataset, kamus, BOD dan pilihan NGBoost/Rotation Forest.
Week 11 memakai baseline prior dan dua model utama dengan adapter SVD 32
komponen + scaling yang sama, seluruh fit pada train. Tidak ada balancing.
AP validation: Dummy_prior 0,1101; NGBoost 0,1993; Rotation_Forest 0,1568.
Threshold 0,5 tanpa tuning atau kalibrasi pascatraining; test tidak dievaluasi.
NGBoost belum memprediksi kelas positif pada threshold ini; Rotation Forest
mengenali 34/1.659 kasus positif. Hasil ini belum memadai untuk penggunaan klinis.
Arsip LR/RF memakai representasi/pembobotan berbeda, bukan pembanding terkontrol.
Rincian ada di [week 10](../week-10/README.md) dan [week 11](../week-11/README.md).

## Week 12 — hasil lokal

Ambang dipilih pada validasi sebelum uji dibaca. Set uji mencakup 14.978
kunjungan dari 10.566 pasien. NGBoost memperoleh AP 0,2068 dan F1 0,2606,
sedangkan Rotation Forest memperoleh AP 0,1573 dan F1 0,2265. Analisis
kesalahan dipisahkan menurut rentang usia dan jumlah rawat inap sebelumnya.
Lihat [Week 12](../week-12/README.md).

## Week 13 sampai 15 dan tindak lanjut

Artikel bahasa Indonesia IMRAD untuk Week 15 sudah disiapkan lebih awal dalam
PDF dan Markdown di [folder artikel](../artikel/README.md). Week 14 belum
dikerjakan; percobaan tambahan mengikuti permintaan dosen pada tahap tersebut.
Eksperimen oversampling yang tersedia merupakan revisi laporan Week 13.
Artikel memisahkan hasil test tahap awal dari hasil validation
revisi, dan tabel numeriknya dicocokkan otomatis terhadap sumber.

Laporan pertama Week 13 sudah tersedia dalam PDF tersendiri dan sumber Markdown
di [Week 13](../week-13/README.md). PDF Week 10 juga diperbarui dengan arti,
jumlah dan perlakuan kode administrasi. Week 10, 11, 12, 13 dipisah dalam
empat folder. Revisi NGBoost + ROS dan penyesuaian ambang dicatat terpisah;
F1 validation sesudah pemilihan ambang adalah 0,2540 (NGBoost) dan 0,2534 (ROS).
Semua 16 tes lulus lokal; ini tidak menyatakan CI pada commit baru sudah lulus.

- Review target/cohort dan penyesuaian format BOD jika dosen memberi template.
- Penyesuaian template artikel jika dosen memberikan format khusus.
- Materi presentasi Week 16 dari hasil nyata.

Undangan collaborator dilakukan setelah setup sesuai permintaan pengguna.
Week 10–13 memiliki laporan terpisah, Week 14 belum dikerjakan, dan artikel
untuk Week 15 sudah disiapkan lebih awal. Pengumpulan ke LMS dan
persetujuan dosen belum diverifikasi.

## Format pembaruan

Untuk tiap capaian, tulis tanggal, commit/versi, cara menjalankan,
pemeriksaan, hasil, tautan bukti, batas, dan pekerjaan yang masih ditunggu.
Bedakan rencana, hasil otomatis, review manual, serta keputusan kelompok.
