# Status implementasi Classification

Catatan awal: 1 November 2026. Status berikut membedakan fondasi repo dari
pekerjaan analisis yang belum dilakukan.

## Sudah tersedia

| Bagian | Hasil | Batas |
|---|---|---|
| Struktur kerja | data/raw dan processed; notebooks; src; results; docs | Berisi petunjuk; belum ada dataset dan kode klasifikasi |
| Dokumen kelompok | CONTRIBUTING, SECURITY, template issue/PR, pembagian tiga anggota dan kalender Selasa | Pembagian adalah rencana yang disesuaikan dengan beban aktual |
| Python | Versi acuan 3.12, requirements.txt, format file dan ignore | Dependensi proyek belum ditentukan |
| CI | Instalasi requirements, pip check, sintaks .py dalam src | Belum menjalankan notebook atau menguji hasil model/metrik |
| Dependabot | Pembaruan pip/Actions bulanan; alerts dan PR perbaikan keamanan | PR perlu ditinjau; bukan pemindaian rahasia atau audit dataset |
| Pengaturan repo | Private, main, squash merge, hapus branch setelah merge | Auto-merge nonaktif; tidak mengklaim branch protection aktif |

CI pada commit `ace1056` sudah berhasil:
[Python CI](https://github.com/bambangh31/data-mining-classification-kelompok-1/actions/runs/41279203504).
Hasil itu membuktikan fondasi saat commit tersebut dapat dijalankan, bukan
akurasi klasifikasi. Periksa CI pada commit terkait untuk perubahan berikutnya.

## Menunggu pengerjaan

- Pemilihan dataset, tujuan/BOD final, kamus data dan karakteristik aktual.
- Pemilihan algoritma A/B, fitur, metrik, dan protokol pembagian/validasi.
- Dependensi, kode preprocessing, baseline, model dan evaluasi.
- Hasil eksperimen, analisis kesalahan dan keterbatasan.
- Laporan pertama, artikel IMRAD dan materi presentasi dari hasil nyata.

Undangan collaborator dilakukan setelah setup sesuai permintaan pengguna.
Belum ada klaim bahwa dataset, eksperimen, atau laporan sudah selesai.

## Format pembaruan

Untuk tiap capaian, tulis tanggal, commit/versi, cara menjalankan,
pemeriksaan, hasil, tautan bukti, batas, dan pekerjaan yang masih ditunggu.
Bedakan rencana, hasil otomatis, review manual, serta keputusan kelompok.
