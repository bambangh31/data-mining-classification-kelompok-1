# Arti kode dan kategori data

Sumber kode: [IDS_mapping.csv](../../data/raw/IDS_mapping.csv) dari arsip [UCI](https://archive.ics.uci.edu/dataset/296/diabetes-130-us-hospitals-for-years-1999-2008). Arti sumber dipertahankan; jumlah dihitung dari seluruh CSV asli sebelum cleaning. Kode dengan jumlah 0 tetap dicantumkan karena tersedia dalam mapping.

## Status meninggal dan pemilihan cohort

`discharge_disposition_id`: **11 = Expired (meninggal)**; **19 = meninggal di rumah, Medicaid/hospice**; **20 = meninggal di fasilitas medis, Medicaid/hospice**; **21 = meninggal, lokasi tidak diketahui, Medicaid/hospice**. Keempat kode mengecualikan kunjungan tersebut karena sasaran adalah readmission setelah keluar hidup. Kunjungan terdahulu pasien tetap dipertahankan. Kode 13/14 berarti hospice, tidak otomatis meninggal.

Kode berlaku per kolom: kode 20 pada admission_source_id berarti Not Mapped, bukan meninggal. Kode administrasi merupakan kategori nominal, bukan angka berurutan.

## admission_type_id

| kode | arti_sumber | jumlah_data_asli | perlakuan |
|---|---|---|---|
| 1 | Emergency | 53990 | Dipertahankan sebagai kategori |
| 2 | Urgent | 18480 | Dipertahankan sebagai kategori |
| 3 | Elective | 18869 | Dipertahankan sebagai kategori |
| 4 | Newborn | 10 | Dipertahankan sebagai kategori |
| 5 | Not Available | 4785 | Diubah menjadi missing |
| 6 | NULL | 5291 | Diubah menjadi missing |
| 7 | Trauma Center | 21 | Dipertahankan sebagai kategori |
| 8 | Not Mapped | 320 | Diubah menjadi missing |

## discharge_disposition_id

| kode | arti_sumber | jumlah_data_asli | perlakuan |
|---|---|---|---|
| 1 | Discharged to home | 60234 | Dipertahankan sebagai kategori |
| 2 | Discharged/transferred to another short term hospital | 2128 | Dipertahankan sebagai kategori |
| 3 | Discharged/transferred to SNF | 13954 | Dipertahankan sebagai kategori |
| 4 | Discharged/transferred to ICF | 815 | Dipertahankan sebagai kategori |
| 5 | Discharged/transferred to another type of inpatient care institution | 1184 | Dipertahankan sebagai kategori |
| 6 | Discharged/transferred to home with home health service | 12902 | Dipertahankan sebagai kategori |
| 7 | Left AMA | 623 | Dipertahankan sebagai kategori |
| 8 | Discharged/transferred to home under care of Home IV provider | 108 | Dipertahankan sebagai kategori |
| 9 | Admitted as an inpatient to this hospital | 21 | Dipertahankan sebagai kategori |
| 10 | Neonate discharged to another hospital for neonatal aftercare | 6 | Dipertahankan sebagai kategori |
| 11 | Expired | 1642 | Kunjungan dikeluarkan: meninggal |
| 12 | Still patient or expected to return for outpatient services | 3 | Dipertahankan sebagai kategori |
| 13 | Hospice / home | 399 | Dipertahankan sebagai kategori |
| 14 | Hospice / medical facility | 372 | Dipertahankan sebagai kategori |
| 15 | Discharged/transferred within this institution to Medicare approved swing bed | 63 | Dipertahankan sebagai kategori |
| 16 | Discharged/transferred/referred another institution for outpatient services | 11 | Dipertahankan sebagai kategori |
| 17 | Discharged/transferred/referred to this institution for outpatient services | 14 | Dipertahankan sebagai kategori |
| 18 | NULL | 3691 | Diubah menjadi missing |
| 19 | Expired at home. Medicaid only, hospice. | 8 | Kunjungan dikeluarkan: meninggal |
| 20 | Expired in a medical facility. Medicaid only, hospice. | 2 | Kunjungan dikeluarkan: meninggal |
| 21 | Expired, place unknown. Medicaid only, hospice. | 0 | Kunjungan dikeluarkan: meninggal |
| 22 | Discharged/transferred to another rehab fac including rehab units of a hospital . | 1993 | Dipertahankan sebagai kategori |
| 23 | Discharged/transferred to a long term care hospital. | 412 | Dipertahankan sebagai kategori |
| 24 | Discharged/transferred to a nursing facility certified under Medicaid but not certified under Medicare. | 48 | Dipertahankan sebagai kategori |
| 25 | Not Mapped | 989 | Diubah menjadi missing |
| 26 | Unknown/Invalid | 0 | Diubah menjadi missing |
| 30 | Discharged/transferred to another Type of Health Care Institution not Defined Elsewhere | 0 | Dipertahankan sebagai kategori |
| 27 | Discharged/transferred to a federal health care facility. | 5 | Dipertahankan sebagai kategori |
| 28 | Discharged/transferred/referred to a psychiatric hospital of psychiatric distinct part unit of a hospital | 139 | Dipertahankan sebagai kategori |
| 29 | Discharged/transferred to a Critical Access Hospital (CAH). | 0 | Dipertahankan sebagai kategori |

## admission_source_id

| kode | arti_sumber | jumlah_data_asli | perlakuan |
|---|---|---|---|
| 1 | Physician Referral | 29565 | Dipertahankan sebagai kategori |
| 2 | Clinic Referral | 1104 | Dipertahankan sebagai kategori |
| 3 | HMO Referral | 187 | Dipertahankan sebagai kategori |
| 4 | Transfer from a hospital | 3187 | Dipertahankan sebagai kategori |
| 5 | Transfer from a Skilled Nursing Facility (SNF) | 855 | Dipertahankan sebagai kategori |
| 6 | Transfer from another health care facility | 2264 | Dipertahankan sebagai kategori |
| 7 | Emergency Room | 57494 | Dipertahankan sebagai kategori |
| 8 | Court/Law Enforcement | 16 | Dipertahankan sebagai kategori |
| 9 | Not Available | 125 | Diubah menjadi missing |
| 10 | Transfer from critial access hospital | 8 | Dipertahankan sebagai kategori |
| 11 | Normal Delivery | 2 | Dipertahankan sebagai kategori |
| 12 | Premature Delivery | 0 | Dipertahankan sebagai kategori |
| 13 | Sick Baby | 1 | Dipertahankan sebagai kategori |
| 14 | Extramural Birth | 2 | Dipertahankan sebagai kategori |
| 15 | Not Available | 0 | Diubah menjadi missing |
| 17 | NULL | 6781 | Diubah menjadi missing |
| 18 | Transfer From Another Home Health Agency | 0 | Dipertahankan sebagai kategori |
| 19 | Readmission to Same Home Health Agency | 0 | Dipertahankan sebagai kategori |
| 20 | Not Mapped | 161 | Diubah menjadi missing |
| 21 | Unknown/Invalid | 0 | Diubah menjadi missing |
| 22 | Transfer from hospital inpt/same fac reslt in a sep claim | 12 | Dipertahankan sebagai kategori |
| 23 | Born inside this hospital | 0 | Dipertahankan sebagai kategori |
| 24 | Born outside this hospital | 0 | Dipertahankan sebagai kategori |
| 25 | Transfer from Ambulatory Surgery Center | 2 | Dipertahankan sebagai kategori |
| 26 | Transfer from Hospice | 0 | Dipertahankan sebagai kategori |

## Kategori lain dan target

- `readmitted`: NO = tidak tercatat rawat inap ulang; >30 = rawat inap ulang lebih dari 30 hari; <30 = kurang dari 30 hari. Target biner: <30 menjadi 1; NO dan >30 menjadi 0. Kelas 0 bukan berarti tidak pernah rawat inap ulang. Label sumber dipertahankan apa adanya.
- Status obat: No = tidak diresepkan; Steady = dosis tetap; Up = dosis dinaikkan; Down = dosis diturunkan. Tidak semua obat memiliki keempat kategori dalam CSV.
- `change`: Ch = ada perubahan terapi diabetes; No = tidak ada. `diabetesMed`: Yes = obat diabetes diresepkan; No = tidak.
- `max_glu_serum`: None = tidak diperiksa; Norm = kategori normal; >200 dan >300 = kategori hasil glukosa sesuai label sumber (mg/dL). `A1Cresult`: None = tidak diperiksa; Norm = kategori normal; >7 dan >8 = kategori HbA1c sesuai label sumber (%). None bukan missing CSV.
- `age`: interval tahun [a,b) mencakup a sampai sebelum b, misalnya [70-80). `weight`: kelompok berat dalam pound; kolom ini dikeluarkan karena missing >50% pada train.
- `gender`: Male, Female, Unknown/Invalid; yang terakhir menjadi missing. `race`: Caucasian, AfricanAmerican, Asian, Hispanic, Other; ? menjadi missing.
- `diag_1/2/3`: kode ICD-9 diagnosis utama/kedua/ketiga; angka dan kode E/V diperlakukan sebagai kategori. `payer_code` dan `medical_specialty` juga kategori; mapping administrasi tidak menjelaskan semua singkatan pembayar.
- Delapan fitur numerik berisi hitungan kecuali time_in_hospital (hari). Rentang aktual dan contoh kategori per kolom tersedia di [kamus data](kamus-data.md).
