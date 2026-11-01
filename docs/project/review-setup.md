# Pemeriksaan kelengkapan pengaturan repository

Pemeriksaan pada 1 November 2026 membandingkan struktur rekursif repo
`MelvynFaith/umkm-marketplace`, konfigurasi GitHub, dan isi dasar repo ini.
Tabel ini menilai kebutuhan setup, bukan mengaudit seluruh implementasi
keamanan aplikasi contoh atau menyatakan analisis Data Mining telah selesai.

| Bagian pada contoh | Penerapan untuk Data Mining |
|---|---|
| README dan struktur kode/dokumen | README utama, data, notebooks, src, results, docs |
| CONTRIBUTING.md | Panduan Python, branch/PR, eksperimen, review, dan dokumen |
| SECURITY.md | Kredensial, dataset, keluaran notebook, dan pelaporan pribadi |
| .editorconfig dan .gitattributes | Format teks dan penanganan berkas lintas Windows/Linux |
| .nvmrc dan konfigurasi TypeScript | Diganti acuan Python melalui .python-version dan CI |
| .gitignore | Environment/cache, kredensial, dan file lokal sementara |
| Template issue dan PR | Form masalah/usulan dan template penjelasan perubahan |
| GitHub Actions | CI Python dasar; pemeriksaan eksekusi/model berkembang bersama kode |
| Dependabot | Library Python dan GitHub Actions, pemeriksaan versi bulanan |
| docs/project dan course | Kalender kelas, pembagian kontribusi, tahap tugas, dan pencatatan keputusan |
| Dokumen operasional proyek | collaboration-plan, timeline, publication-checklist, implementation-status |
| Laporan dan bahan presentasi | docs/laporan, docs/artikel, docs/presentasi |
| Kontrak API, layanan, frontend, Postman, infra | Khusus aplikasi Web Service; tidak menjadi kebutuhan proyek klasifikasi saat ini |
| .env.example | Ditambahkan jika kode mulai memakai variabel environment, dengan nilai contoh |
| Konfigurasi lint Markdown | Belum diperlukan; format dokumen diperiksa saat review |
| Pemindaian rahasia dan pengujian perilaku | Belum aktif; CI dasar tidak diklaim memeriksa keduanya |
| Lisensi | Belum ditetapkan; tidak memberi lisensi ulang dataset dari pihak lain |

## Pengaturan GitHub yang sudah diperiksa

- Repo private dengan branch utama `main` dan Issues aktif.
- Squash merge dan penghapusan branch setelah merge aktif; auto-merge nonaktif.
- Dependabot alerts dan PR pembaruan keamanan aktif.
- Izin default workflow read-only; workflow tidak diberi izin menyetujui PR.
- Pilihan akun Git lokal untuk repo ini menggunakan `bambangh31`.
- Undangan collaborator dilakukan terakhir sesuai permintaan pengguna.

## Bagian yang menunggu pengerjaan proyek

Dataset, kamus data aktual, algoritma, library beserta versinya, notebook,
pengujian pipeline/model, hasil evaluasi, laporan, artikel, dan slide diisi
ketika kegiatannya dilakukan. File kosong yang menyerupai hasil jadi tidak
dibuat untuk menggantikan pekerjaan tersebut.

## Keselarasan dengan setup Web Mining

Kedua repo memakai fondasi yang sama: struktur data/kode/dokumen, panduan
kontribusi/keamanan, format file, Python, issue/PR, CI, Dependabot, serta enam
dokumen dalam `docs/project/`. Isi tetap mengikuti mata kuliah masing-masing.
Data Mining memiliki tiga anggota dan kalender Selasa yang sudah diberikan,
perbandingan klasifikasi, serta artikel IMRAD. Panduan anotasi aspek khusus
ABSA tetap berada pada repo Web Mining.

Rencana kolaborasi, timeline dan checklist pada contoh UMKM diadaptasi dengan
fungsi yang sama; status implementasi mencatat fondasi yang benar-benar ada.
Dokumen API, Auth/Gateway, Cloudflare dan implementasi sesi khusus service
tidak disalin sebagai pekerjaan proyek klasifikasi.
