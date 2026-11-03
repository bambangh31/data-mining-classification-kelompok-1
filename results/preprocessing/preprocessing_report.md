# Hasil preprocessing

Dibuat oleh `python -m src.preprocess`.

- Data asli: 101,766 baris, 50 kolom.
- Setelah cleaning/cohort: 100,114 baris.
- Kunjungan berstatus meninggal dikeluarkan: 1,652.
- Target: `binary`; pemetaan: `{'NO': 0, '>30': 0, '<30': 1}`.
- Jumlah fitur setelah encoding: 1222.
- Pasien tumpang tindih antarset: 0; transformer di-fit pada train saja.

| Set | Baris | Pasien | Jumlah per kelas |
|---|---|---|---|
| train | 70071 | 49307 | {'0': 62104, '1': 7967} |
| validation | 15065 | 10566 | {'0': 13406, '1': 1659} |
| test | 14978 | 10566 | {'0': 13247, '1': 1731} |

## Kolom yang dikeluarkan

- ID: encounter_id, patient_nbr (hanya metadata/pembagian, bukan fitur).
- Missing >50% pada train: ['weight'].
- Konstan pada train: ['acetohexamide', 'examide', 'citoglipton'].

Laporan ini hanya preprocessing; percobaan model ada pada laporan week 11. Jangan memilih model/parameter dari test.
Pembagian ini menguji generalisasi ke pasien berbeda, bukan prediksi tahun mendatang.
