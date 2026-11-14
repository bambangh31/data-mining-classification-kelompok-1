# Artikel Week 15

Artikel bahasa Indonesia sudah disusun dengan struktur IMRAD, abstrak,
kata kunci, kesimpulan, ketersediaan data/kode, serta delapan referensi.
Judul: **Klasifikasi Rawat Inap Ulang Pasien Diabetes Menggunakan NGBoost dan
Rotation Forest serta Evaluasi Random Oversampling**.

- [PDF artikel](week-15-artikel-imrad-kelompok-1.pdf)
- [Sumber Markdown yang dapat diedit](artikel-imrad.md)
- [Hash sumber angka dan catatan pemeriksaan tabel](sumber-angka.json)
- [Percobaan tambahan Week 14](../week-14/README.md)

Artikel menggunakan hasil nyata yang sudah tersimpan; tidak menambahkan
hasil training, CV, signifikansi, atau test yang belum dilakukan. Hasil test
tahap awal dibedakan dari hasil validation revisi oversampling. Hasil ambang
optimal revisi diukur pada validation yang juga dipakai memilih ambang,
sehingga tidak diklaim sebagai evaluasi independen.

Format saat ini adalah artikel akademik satu kolom tanpa cover laporan,
dengan abstrak dan paragraf isi rata kanan-kiri (justify).
Template jurnal/dosen, batas halaman, dan gaya sitasi khusus belum diberikan;
penyesuaian format dapat dilakukan jika ada ketentuan tambahan. Isi IMRAD
sudah lengkap, tetapi belum menyatakan persetujuan dosen atau pengumpulan LMS.

## Reproduksi dan pemeriksaan

Gunakan Python dengan ReportLab dan pypdf pada environment PDF.

```powershell
python scripts/pdf/build_article.py
```

Generator memeriksa tabel numerik 1 dan 3-7 terhadap metadata/CSV sumber,
menulis manifest hash, lalu menghasilkan PDF artikel dan Week 14 ke
`output/pdf/`. Tabel 2 berisi parameter yang diperiksa terhadap kode mining.
Sumber utama isi adalah Markdown di folder ini; perubahan isi dilakukan
di sana, kemudian PDF dibuat dan diperiksa kembali. Salinan PDF final di
folder dokumen diperbarui setelah pemeriksaan visual.

Percobaan dasar berada pada commit `2c2e594`; hash setiap sumber data dicatat
di manifest. Hash teks memakai UTF-8 dengan newline LF agar dapat diperiksa
lintas sistem operasi; hash PNG memakai byte asli. Presentasi Week 16 belum dibuat.
