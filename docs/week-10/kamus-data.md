# Kamus data

Dihitung dari CSV asli. Missing = tanda ? atau kosong; None pada tes lab dipertahankan.

| kolom | peran | tipe_analisis | deskripsi | unik_nonmissing | missing_jumlah | missing_persen |
|---|---|---|---|---|---|---|
| encounter_id | ID | kategorikal | ID kunjungan; metadata, bukan prediktor | 101766 | 0 | 0.0 |
| patient_nbr | ID | kategorikal | ID pasien; kelompok pembagian data, bukan prediktor | 71518 | 0 | 0.0 |
| race | fitur | kategorikal | Kategori ras yang tercatat | 5 | 2273 | 2.234 |
| gender | fitur | kategorikal | Gender yang tercatat | 3 | 0 | 0.0 |
| age | fitur | kategorikal | Kelompok usia dalam interval 10 tahun | 10 | 0 | 0.0 |
| weight | fitur | kategorikal | Kelompok berat badan; missing sangat tinggi | 9 | 98569 | 96.858 |
| admission_type_id | fitur | kategorikal | Kode jenis masuk; lihat IDS_mapping.csv | 8 | 0 | 0.0 |
| discharge_disposition_id | fitur | kategorikal | Kode status/tujuan keluar; lihat IDS_mapping.csv | 26 | 0 | 0.0 |
| admission_source_id | fitur | kategorikal | Kode sumber rujukan; lihat IDS_mapping.csv | 17 | 0 | 0.0 |
| time_in_hospital | fitur | numerik | Lama rawat, hari (1-14) | 14 | 0 | 0.0 |
| payer_code | fitur | kategorikal | Kode pembayar/asuransi | 17 | 40256 | 39.557 |
| medical_specialty | fitur | kategorikal | Spesialisasi dokter yang menerima pasien | 72 | 49949 | 49.082 |
| num_lab_procedures | fitur | numerik | Jumlah pemeriksaan laboratorium selama kunjungan | 118 | 0 | 0.0 |
| num_procedures | fitur | numerik | Jumlah prosedur selain pemeriksaan laboratorium | 7 | 0 | 0.0 |
| num_medications | fitur | numerik | Jumlah obat berbeda selama kunjungan | 75 | 0 | 0.0 |
| number_outpatient | fitur | numerik | Jumlah kunjungan rawat jalan dalam tahun sebelumnya | 39 | 0 | 0.0 |
| number_emergency | fitur | numerik | Jumlah kunjungan gawat darurat dalam tahun sebelumnya | 33 | 0 | 0.0 |
| number_inpatient | fitur | numerik | Jumlah kunjungan rawat inap dalam tahun sebelumnya | 21 | 0 | 0.0 |
| diag_1 | fitur | kategorikal | Kode diagnosis utama (ICD-9); kategori, bukan angka kontinu | 716 | 21 | 0.021 |
| diag_2 | fitur | kategorikal | Kode diagnosis kedua (ICD-9) | 748 | 358 | 0.352 |
| diag_3 | fitur | kategorikal | Kode diagnosis ketiga (ICD-9) | 789 | 1423 | 1.398 |
| number_diagnoses | fitur | numerik | Jumlah diagnosis yang tercatat | 16 | 0 | 0.0 |
| max_glu_serum | fitur | kategorikal | Kategori hasil glukosa; None berarti tidak diperiksa | 4 | 0 | 0.0 |
| A1Cresult | fitur | kategorikal | Kategori hasil HbA1c; None berarti tidak diperiksa | 4 | 0 | 0.0 |
| metformin | fitur | kategorikal | Status penggunaan/perubahan dosis obat metformin: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| repaglinide | fitur | kategorikal | Status penggunaan/perubahan dosis obat repaglinide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| nateglinide | fitur | kategorikal | Status penggunaan/perubahan dosis obat nateglinide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| chlorpropamide | fitur | kategorikal | Status penggunaan/perubahan dosis obat chlorpropamide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| glimepiride | fitur | kategorikal | Status penggunaan/perubahan dosis obat glimepiride: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| acetohexamide | fitur | kategorikal | Status penggunaan/perubahan dosis obat acetohexamide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 |
| glipizide | fitur | kategorikal | Status penggunaan/perubahan dosis obat glipizide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| glyburide | fitur | kategorikal | Status penggunaan/perubahan dosis obat glyburide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| tolbutamide | fitur | kategorikal | Status penggunaan/perubahan dosis obat tolbutamide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 |
| pioglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat pioglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| rosiglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat rosiglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| acarbose | fitur | kategorikal | Status penggunaan/perubahan dosis obat acarbose: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| miglitol | fitur | kategorikal | Status penggunaan/perubahan dosis obat miglitol: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| troglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat troglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 |
| tolazamide | fitur | kategorikal | Status penggunaan/perubahan dosis obat tolazamide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 3 | 0 | 0.0 |
| examide | fitur | kategorikal | Status penggunaan/perubahan dosis obat examide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 1 | 0 | 0.0 |
| citoglipton | fitur | kategorikal | Status penggunaan/perubahan dosis obat citoglipton: No, Steady, Up, Down (sesuai kategori yang tersedia) | 1 | 0 | 0.0 |
| insulin | fitur | kategorikal | Status penggunaan/perubahan dosis obat insulin: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| glyburide-metformin | fitur | kategorikal | Status penggunaan/perubahan dosis obat glyburide-metformin: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 |
| glipizide-metformin | fitur | kategorikal | Status penggunaan/perubahan dosis obat glipizide-metformin: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 |
| glimepiride-pioglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat glimepiride-pioglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 |
| metformin-rosiglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat metformin-rosiglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 |
| metformin-pioglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat metformin-pioglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 |
| change | fitur | kategorikal | Apakah terdapat perubahan obat diabetes (Ch/No) | 2 | 0 | 0.0 |
| diabetesMed | fitur | kategorikal | Apakah obat diabetes diresepkan (Yes/No) | 2 | 0 | 0.0 |
| readmitted | target | kategorikal | Target asli: NO, >30, <30 | 3 | 0 | 0.0 |
