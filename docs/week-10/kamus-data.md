# Kamus data

Dihitung dari CSV asli. Missing = tanda ? atau kosong; None pada tes lab dipertahankan.

Arti kode, jumlah tiap kode dan perlakuan cleaning ada pada [rincian kode](kode-kategori.md).

| kolom | peran | tipe_analisis | deskripsi | unik_nonmissing | missing_jumlah | missing_persen | nilai_aktual_atau_contoh |
|---|---|---|---|---|---|---|---|
| encounter_id | ID | kategorikal | ID kunjungan; metadata, bukan prediktor | 101766 | 0 | 0.0 | ID unik; tidak digunakan sebagai fitur |
| patient_nbr | ID | kategorikal | ID pasien; kelompok pembagian data, bukan prediktor | 71518 | 0 | 0.0 | ID unik; tidak digunakan sebagai fitur |
| race | fitur | kategorikal | Kategori ras yang tercatat | 5 | 2273 | 2.234 | AfricanAmerican, Asian, Caucasian, Hispanic, Other |
| gender | fitur | kategorikal | Gender yang tercatat | 3 | 0 | 0.0 | Female, Male, Unknown/Invalid |
| age | fitur | kategorikal | Kelompok usia dalam interval 10 tahun | 10 | 0 | 0.0 | [0-10), [10-20), [20-30), [30-40), [40-50), [50-60), [60-70), [70-80), [80-90), [90-100) |
| weight | fitur | kategorikal | Kelompok berat badan; missing sangat tinggi | 9 | 98569 | 96.858 | >200, [0-25), [100-125), [125-150), [150-175), [175-200), [25-50), [50-75), [75-100) |
| admission_type_id | fitur | kategorikal | Kode jenis masuk; lihat IDS_mapping.csv | 8 | 0 | 0.0 | 1, 2, 3, 4, 5, 6, 7, 8 |
| discharge_disposition_id | fitur | kategorikal | Kode status/tujuan keluar; lihat IDS_mapping.csv | 26 | 0 | 0.0 | 1, 10, 11, 12, 13, 14, 15, 16, 17, 18; ... (contoh, bukan seluruh nilai) |
| admission_source_id | fitur | kategorikal | Kode sumber rujukan; lihat IDS_mapping.csv | 17 | 0 | 0.0 | 1, 10, 11, 13, 14, 17, 2, 20, 22, 25; ... (contoh, bukan seluruh nilai) |
| time_in_hospital | fitur | numerik | Lama rawat, hari (1-14) | 14 | 0 | 0.0 | 1 sampai 14 |
| payer_code | fitur | kategorikal | Kode pembayar/asuransi | 17 | 40256 | 39.557 | BC, CH, CM, CP, DM, FR, HM, MC, MD, MP; ... (contoh, bukan seluruh nilai) |
| medical_specialty | fitur | kategorikal | Spesialisasi dokter yang menerima pasien | 72 | 49949 | 49.082 | AllergyandImmunology, Anesthesiology, Anesthesiology-Pediatric, Cardiology, Cardiology-Pediatric, DCPTEAM, Dentistry, Dermatology, Emergency/Trauma, Endocrinology; ... (contoh, bukan seluruh nilai) |
| num_lab_procedures | fitur | numerik | Jumlah pemeriksaan laboratorium selama kunjungan | 118 | 0 | 0.0 | 1 sampai 132 |
| num_procedures | fitur | numerik | Jumlah prosedur selain pemeriksaan laboratorium | 7 | 0 | 0.0 | 0 sampai 6 |
| num_medications | fitur | numerik | Jumlah obat berbeda selama kunjungan | 75 | 0 | 0.0 | 1 sampai 81 |
| number_outpatient | fitur | numerik | Jumlah kunjungan rawat jalan dalam tahun sebelumnya | 39 | 0 | 0.0 | 0 sampai 42 |
| number_emergency | fitur | numerik | Jumlah kunjungan gawat darurat dalam tahun sebelumnya | 33 | 0 | 0.0 | 0 sampai 76 |
| number_inpatient | fitur | numerik | Jumlah kunjungan rawat inap dalam tahun sebelumnya | 21 | 0 | 0.0 | 0 sampai 21 |
| diag_1 | fitur | kategorikal | Kode diagnosis utama (ICD-9); kategori, bukan angka kontinu | 716 | 21 | 0.021 | 10, 11, 110, 112, 114, 115, 117, 131, 133, 135; ... (contoh, bukan seluruh nilai) |
| diag_2 | fitur | kategorikal | Kode diagnosis kedua (ICD-9) | 748 | 358 | 0.352 | 11, 110, 111, 112, 114, 115, 117, 123, 130, 131; ... (contoh, bukan seluruh nilai) |
| diag_3 | fitur | kategorikal | Kode diagnosis ketiga (ICD-9) | 789 | 1423 | 1.398 | 11, 110, 111, 112, 115, 117, 122, 123, 131, 132; ... (contoh, bukan seluruh nilai) |
| number_diagnoses | fitur | numerik | Jumlah diagnosis yang tercatat | 16 | 0 | 0.0 | 1 sampai 16 |
| max_glu_serum | fitur | kategorikal | Kategori hasil glukosa; None berarti tidak diperiksa | 4 | 0 | 0.0 | >200, >300, None, Norm |
| A1Cresult | fitur | kategorikal | Kategori hasil HbA1c; None berarti tidak diperiksa | 4 | 0 | 0.0 | >7, >8, None, Norm |
| metformin | fitur | kategorikal | Status penggunaan/perubahan dosis obat metformin: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| repaglinide | fitur | kategorikal | Status penggunaan/perubahan dosis obat repaglinide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| nateglinide | fitur | kategorikal | Status penggunaan/perubahan dosis obat nateglinide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| chlorpropamide | fitur | kategorikal | Status penggunaan/perubahan dosis obat chlorpropamide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| glimepiride | fitur | kategorikal | Status penggunaan/perubahan dosis obat glimepiride: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| acetohexamide | fitur | kategorikal | Status penggunaan/perubahan dosis obat acetohexamide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 | No, Steady |
| glipizide | fitur | kategorikal | Status penggunaan/perubahan dosis obat glipizide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| glyburide | fitur | kategorikal | Status penggunaan/perubahan dosis obat glyburide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| tolbutamide | fitur | kategorikal | Status penggunaan/perubahan dosis obat tolbutamide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 | No, Steady |
| pioglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat pioglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| rosiglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat rosiglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| acarbose | fitur | kategorikal | Status penggunaan/perubahan dosis obat acarbose: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| miglitol | fitur | kategorikal | Status penggunaan/perubahan dosis obat miglitol: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| troglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat troglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 | No, Steady |
| tolazamide | fitur | kategorikal | Status penggunaan/perubahan dosis obat tolazamide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 3 | 0 | 0.0 | No, Steady, Up |
| examide | fitur | kategorikal | Status penggunaan/perubahan dosis obat examide: No, Steady, Up, Down (sesuai kategori yang tersedia) | 1 | 0 | 0.0 | No |
| citoglipton | fitur | kategorikal | Status penggunaan/perubahan dosis obat citoglipton: No, Steady, Up, Down (sesuai kategori yang tersedia) | 1 | 0 | 0.0 | No |
| insulin | fitur | kategorikal | Status penggunaan/perubahan dosis obat insulin: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| glyburide-metformin | fitur | kategorikal | Status penggunaan/perubahan dosis obat glyburide-metformin: No, Steady, Up, Down (sesuai kategori yang tersedia) | 4 | 0 | 0.0 | Down, No, Steady, Up |
| glipizide-metformin | fitur | kategorikal | Status penggunaan/perubahan dosis obat glipizide-metformin: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 | No, Steady |
| glimepiride-pioglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat glimepiride-pioglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 | No, Steady |
| metformin-rosiglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat metformin-rosiglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 | No, Steady |
| metformin-pioglitazone | fitur | kategorikal | Status penggunaan/perubahan dosis obat metformin-pioglitazone: No, Steady, Up, Down (sesuai kategori yang tersedia) | 2 | 0 | 0.0 | No, Steady |
| change | fitur | kategorikal | Apakah terdapat perubahan obat diabetes (Ch/No) | 2 | 0 | 0.0 | Ch, No |
| diabetesMed | fitur | kategorikal | Apakah obat diabetes diresepkan (Yes/No) | 2 | 0 | 0.0 | No, Yes |
| readmitted | target | kategorikal | Target asli: NO, >30, <30 | 3 | 0 | 0.0 | <30, >30, NO |
