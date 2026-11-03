# Panduan kerja kelompok

## Isi folder

| Dokumen | Kegunaan |
|---|---|
| [collaboration-plan.md](collaboration-plan.md) | Pembagian tiga anggota, ketergantungan dan review |
| [timeline.md](timeline.md) | Tahap week 10-16 dengan kalender Selasa |
| [publication-checklist.md](publication-checklist.md) | Pemeriksaan penyerahan dan publikasi jika diperlukan |
| [implementation-status.md](implementation-status.md) | Progres, bukti dan batas implementasi |
| [review-setup.md](review-setup.md) | Pemeriksaan kelengkapan fondasi repo |

## Pembagian kontribusi

Setiap minggu dikerjakan bertiga sesuai peran, tanpa PIC khusus. Week 14
tetap hanya dilakukan jika diminta dosen. Rincian ada di
[pembagian tugas per minggu](collaboration-plan.md#pembagian-tugas-per-minggu).

| Anggota | Kontribusi awal |
|---|---|
| Bambang Herlambang | Tujuan/BOD week 10; preprocessing week 11-12; bagian tujuan/preprocessing laporan week 13; pendahuluan artikel week 15; slide sesuai bagian week 16 |
| Benedictus Erlangga | Pencarian/karakteristik dataset dan rancangan evaluasi week 10; baseline, evaluasi kedua algoritma, grafik dan analisis kesalahan week 11-12; bagian data/evaluasi/hasil laporan week 13 dan artikel week 15; slide sesuai bagian week 16 |
| Robertus Geraldyn Alexandro Gabeler | Kajian/rencana algoritma week 10; implementasi A/B, pengaturan parameter dan pencatatan konfigurasi week 11-12; bagian metode/model laporan week 13 dan artikel week 15; slide sesuai bagian week 16 |

Semua menyumbang bahan pembahasan, kesimpulan, referensi, pemeriksaan hasil,
serta presentasi. Jika satu paket lebih berat, bagi subtugas yang tersisa.
Pencarian dataset dilakukan Benedictus saja; pemilihan akhirnya disepakati bersama.

## Kalender kelas

Kelas setiap Selasa. Week 11 pada 3 November 2026 dikonfirmasi oleh pengguna;
minggu berikutnya dipetakan per Selasa dan mengikuti perubahan jadwal dosen.
Tanggal kelas tidak otomatis menjadi batas waktu pengumpulan.

| Week | Tanggal kelas 2026 | Tahap tugas |
|---|---|---|
| 10 | 27 Oktober (pemetaan mundur) | Dataset, contoh/karakteristik, BOD, rencana algoritma |
| 11 | 3 November | Preprocessing dan pipeline awal |
| 12 | 10 November | Mining dan evaluasi |
| 13 | 17 November | Laporan pertama |
| 14 | 24 November | Percobaan tambahan jika diminta |
| 15 | 1 Desember | Artikel bahasa Indonesia dengan IMRAD |
| 16 | 8 Desember | Presentasi |

Status penyelesaian mengikuti hasil nyata, bukan posisi minggu pada kalender.
BOD mengikuti penjelasan/template dosen. Dataset Diabetes telah diberikan;
Logistic Regression dan Random Forest dipakai sebagai algoritma awal.
[Preprocessing](../preprocessing.md) dan [percobaan week 11](../week-11/README.md)
sudah dijalankan lokal; tuning dan evaluasi final masih menunggu.

## Pencatatan tugas dan keputusan

Gunakan Issues untuk pekerjaan dan masukan dosen. Catat hasil yang diharapkan,
anggota yang mengerjakan, target yang disepakati, kendala, dan tautan bukti.
PR menghubungkan perubahan kode/dokumen dengan issue terkait.

Catat alasan memilih dataset, target, fitur, algoritma, dan protokol evaluasi
pada dokumen tahap terkait; keputusan dicatat bersama sumber atau bukti.
Semua anggota memperbarui bagian dan status pekerjaannya sendiri.

## Pemeriksaan kelengkapan setup

Perbandingan struktur repo contoh telah dilakukan; ringkasannya ada di
[review-setup.md](review-setup.md). Panduan kontribusi ada pada
[CONTRIBUTING.md](../../CONTRIBUTING.md).
