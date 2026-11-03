# Rencana kolaborasi Kelompok 1

Topik: Classification. Setiap minggu dikerjakan bertiga sesuai peran, tanpa
PIC khusus. Pembagian subtugas dapat disesuaikan lagi setelah dataset dan
kesulitan pekerjaan diketahui. Week 14 hanya dilakukan jika diminta dosen.

## Anggota

| Nama | NRP |
|---|---|
| Bambang Herlambang | 5803024019 |
| Benedictus Erlangga | 5803024011 |
| Robertus Geraldyn Alexandro Gabeler | 5803024025 |

## Peran teknis

| Anggota | Peran |
|---|---|
| Bambang | Preprocessing: pembersihan, penanganan data kosong, encoding/scaling sesuai kebutuhan, dan pembagian data |
| Benedictus | Pencarian dataset, baseline, evaluasi kedua algoritma, grafik dan analisis kesalahan |
| Robertus Geraldyn | Implementasi algoritma klasifikasi A dan B, pengaturan parameter dan pencatatan konfigurasi percobaan |

Pencarian kandidat dataset dilakukan Benedictus saja; keputusan akhir dataset
tetap disepakati bertiga. Penulisan tujuan/BOD bukan bagian yang otomatis
dipindahkan kepadanya dan tetap dibantu Bambang sesuai tabel mingguan.

## Pembagian tugas per minggu

Tanggal berikut adalah jadwal kelas Selasa tahun 2026, bukan otomatis tenggat
pengumpulan. Week 11 pada 3 November menjadi acuan; week 10 dipetakan mundur.
Status penyelesaian mengikuti pekerjaan nyata, bukan posisi kalender.

| Week / kelas | Pembagian dan hasil |
| --- | --- |
| 10 / 27 Oktober | Benedictus: pencarian kandidat, sumber, contoh, karakteristik, kualitas, distribusi kelas, kamus kolom, ketersediaan label dan rancangan evaluasi. Bambang: masalah, tujuan/BOD, manfaat dan ruang lingkup. Robertus Geraldyn: kajian dan rencana algoritma A/B serta kebutuhan masukan/keluaran. Hasil: bahan week 10. Dataset akhir, algoritma dan rancangan evaluasi disepakati bertiga. |
| 11 / 3 November | Bambang: pemeriksaan/pembersihan, pembagian data dan pipeline transformasi. Benedictus: baseline, fungsi evaluasi dan format rekap. Robertus Geraldyn: kerangka model A/B serta kebutuhan masukan/keluaran. Hasil: pipeline awal yang terhubung. |
| 12 / 10 November | Bambang: menyelesaikan dan memeriksa preprocessing serta menyesuaikan input model. Benedictus: evaluasi kedua algoritma dengan protokol sebanding, grafik dan analisis kesalahan. Robertus Geraldyn: mengimplementasikan algoritma A dan B, mengatur parameter dan mencatat konfigurasi percobaan. Semua mencatat hasil dan penjelasan bagiannya. |
| 13 / 17 November | Bambang menulis masalah, tujuan/BOD dan preprocessing termasuk pembagian/transformasi data. Benedictus menulis sumber/karakteristik dataset, baseline, evaluasi, hasil, grafik dan keterbatasan. Robertus Geraldyn menulis metode/model A/B dan konfigurasi percobaan. Pembahasan, kesimpulan, pustaka, penyatuan format dan pemeriksaan akhir dikerjakan bersama. |
| 14 / 24 November | Jika diminta dosen, bertiga membagi percobaan sesuai peran: Bambang menangani data/preprocessing, Benedictus evaluasi/analisis, dan Robertus Geraldyn model A/B. Detail perubahan mengikuti masukan dosen; hasil dan keputusan diperiksa bersama. Jika tidak diminta, tidak ada percobaan tambahan wajib. |
| 15 / 1 Desember | Bambang: pendahuluan dan metode preprocessing. Benedictus: sumber/karakteristik dataset, baseline, metode evaluasi, hasil dan pembahasan evaluasi. Robertus Geraldyn: metode pemodelan dan pembahasan model. Abstrak, kesimpulan, pustaka dan pemeriksaan akhir bersama; artikel bahasa Indonesia mengikuti IMRAD/template dosen. |
| 16 / 8 Desember | Bambang membuat slide masalah, tujuan/BOD dan preprocessing termasuk pembagian/transformasi data. Benedictus membuat slide sumber/karakteristik dataset, baseline, evaluasi, hasil dan keterbatasan. Robertus Geraldyn membuat slide model A/B dan konfigurasi percobaan. Identitas, alur, kesimpulan dan referensi dirapikan bersama. Semua latihan; pembicara dan durasi mengikuti aturan dosen. |

Dataset Diabetes telah diberikan pada 3 November 2026; preprocessing
dan hasil lokal dijelaskan di [panduan preprocessing](../preprocessing.md).
Algoritma awal A/B adalah NGBoost dan Rotation Forest, dengan baseline
DummyClassifier. Lebih dari satu algoritma disarankan dalam deskripsi tugas.
BOD mengikuti istilah serta format dosen.

## Alasan pembagian

- Benedictus mencari dataset serta menangani baseline dan evaluasi kedua
  algoritma; Bambang menyiapkan tujuan/BOD serta pipeline preprocessing;
  Robertus Geraldyn mengimplementasikan model A/B dan mencatat konfigurasi.
  Beban bergantung pada kondisi data dan kesulitan model. Jika satu bagian
  terlalu berat, anggota lain membantu subtugasnya, termasuk integrasi kode
  dan percobaan.
- Penyusunan slide dibagi bertiga sesuai pekerjaan masing-masing. Setiap
  anggota membuat dan merapikan bagiannya pada materi bersama; alur,
  kesimpulan dan referensi diperiksa bersama.
- Week 15 dikerjakan bertiga karena artikel memerlukan metode, hasil,
  pembahasan, dan referensi yang konsisten.
- Ketiganya berkontribusi setiap minggu sesuai peran. Beban tidak diukur dari
  jumlah berkas atau commit saja; bagi ulang subtugas jika satu bagian berat.

## Bahan sebelum laporan dan slide disusun

Laporan dan slide disusun bertiga, masing-masing sesuai peran. Gunakan satu
dokumen/materi bersama; setiap anggota menulis dan merapikan bagiannya.
Setiap pelaksana menyimpan catatan dan referensi saat coding:

| Bahan | Yang menyiapkan | Kapan tersedia |
|---|---|---|
| Sumber, karakteristik dan rancangan evaluasi | Benedictus | Saat bahan week 10 diselesaikan |
| Kajian dan rencana algoritma A/B | Robertus Geraldyn | Saat bahan week 10 diselesaikan |
| Masalah, tujuan/BOD, manfaat dan ruang lingkup | Bambang | Saat bahan week 10 diselesaikan |
| Pipeline preprocessing, aturan pembersihan, pembagian/transformasi data dan catatan pemeriksaan hasilnya | Bambang | Dikerjakan week 11-12; siap sebelum penyusunan laporan week 13 |
| Algoritma A/B, parameter, prediksi dan penjelasan model | Robertus Geraldyn | Sebelum penyusunan laporan week 13 |
| Baseline, metrik, rekap, grafik dan analisis kesalahan | Benedictus | Sebelum penyusunan laporan week 13 |
| Artikel dan hasil yang sudah diperiksa | Ketiganya sesuai bagian week 15 | Sebelum masing-masing membuat slide week 16 |

Sertakan versi data/kode, cara menjalankan, parameter, jenis set evaluasi,
angka sumber grafik dan keterbatasan. Semua memastikan laporan, artikel,
serta slide memakai angka yang sama. Jika bahan belum siap, pemilik pekerjaan
melengkapinya; anggota lain tidak menanggung pengulangan seluruh eksperimen.

## Urutan teknis dan evaluasi

1. Benedictus menyiapkan kandidat data; Bambang menyusun tujuan/BOD; ketiga
   anggota menyepakati dataset, target, fitur dan protokol evaluasi.
2. Week 11: sepakati masukan/keluaran sejak awal; hubungkan pembersihan,
   transformasi, baseline dan evaluasi.
3. Week 12: bandingkan A/B dengan pembagian dan anggaran percobaan sebanding;
   catat konfigurasi serta hasil.
4. Pilih konfigurasi melalui validasi/CV. Simpan data uji final sampai pilihan
   dibekukan dan jelaskan batas evaluasi jika eksperimen dilanjutkan.
5. Pemeriksaan silang dan bahan siap pakai menjadi dasar laporan/artikel,
   bukan hanya status bahwa kode berhasil dijalankan.

## Review dan pencatatan

Ikuti [CONTRIBUTING.md](../../CONTRIBUTING.md) untuk branch, PR dan CI.
Setelah anggota bergabung, usahakan review anggota lain sebelum merge.
CI sintaks belum membuktikan kebenaran model, metrik, atau kesimpulan.

Gunakan issue atau tracker untuk tugas, target, status, bukti dan kendala.
Catat perubahan data/metode beserta alasan dan eksperimen yang terpengaruh.
Aturan pembagian tidak menggantikan pemeriksaan hasil bersama.

| Tugas / week | Anggota | Hasil | Target | Status | Bukti / kendala |
|---|---|---|---|---|---|
| Diisi saat pembagian | Diisi | Diisi | Disepakati | Sesuai progres nyata | Tautan atau hambatan |

Kalender dan keluaran tahap ada di [timeline.md](timeline.md). Bila laporan,
artikel, atau slide ternyata berat, pecah subtugas tersisa dan bagi kembali.
