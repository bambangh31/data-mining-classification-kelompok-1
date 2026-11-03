# Kandidat algoritma untuk arah paper

Penelusuran dan revisi: 3 November 2026. NGBoost dan Rotation Forest dipilih
untuk eksperimen utama berikutnya. Ini bukan klaim metode pertama pada dataset.
Hasil Logistic Regression/Random Forest diarsipkan di results/archive/week-11-lr-rf.
PDF week 10-11 mengikuti revisi algoritma dan hasil eksekusi terbaru.

## Kesimpulan awal

NGBoost dan Rotation Forest menjadi dua algoritma utama di luar daftar yang diberikan.
Keduanya algoritma yang sudah dipublikasikan; potensi kontribusi adalah evaluasi
aplikasi/protokol pada dataset, bukan penciptaan algoritma baru.

Dalam pencarian web terarah di bawah, belum ditemukan bukti langsung penerapan
NGBoost atau Rotation Forest standar pada target <30 dataset Diabetes 130-US
Hospitals. Ketidaktemuan ini bukan bukti bahwa tidak ada paper tersebut.
Full text, referensi silang dan basis bibliografi perlu diperiksa sebelum
membuat klaim kebaruan. Tidak dilakukan pencarian menyeluruh di Scopus/WoS.

## Kandidat

| Kandidat | Alasan | Batas dan kebutuhan eksperimen |
|---|---|---|
| NGBoost / NGBClassifier | Natural-gradient boosting dengan distribusi Bernoulli untuk klasifikasi biner; menarik untuk menilai kualitas probabilitas risiko | Tambahkan log loss, Brier score dan kurva kalibrasi selain AP. Bernoulli tidak otomatis memberi ketidakpastian epistemik atau jaminan kalibrasi. Perlu menguji runtime, kompatibilitas input dan memori sebelum memilih konfigurasi |
| Rotation Forest | Ensemble yang menggunakan PCA pada kelompok fitur untuk meningkatkan keragaman model; berbeda dari Random Forest | Implementasi aeon membutuhkan fitur kontinu. Representasi numerik/one-hot dan biaya komputasi perlu diuji; jangan menganggap kode kategori ordinal sebagai besaran kontinu. Variannya sudah pernah dipakai untuk readmission pada dataset lain |

Sumber algoritma dan implementasi:

- [NGBoost, ICML 2020](https://proceedings.mlr.press/v119/duan20a.html).
- [Dokumentasi NGBClassifier dan Bernoulli](https://stanfordmlgroup.github.io/ngboost/useage/).
- [Rotation Forest, artikel penulis 2006](https://www.lucykuncheva.co.uk/papers/jrlkcatpami06.pdf).
- [RotationForestClassifier pada aeon](https://www.aeon-toolkit.org/en/stable/api_reference/auto_generated/aeon.classification.sklearn.RotationForestClassifier.html).
- [AHERF untuk readmission 72 jam, dataset rumah sakit di Chile](https://www.vicomtech.org/en/rdi-tangible/publications/publication/using-anticipative-hybrid-extreme-rotation-forest-to-predict-emergency-service-readmission-risk).

## Alternatif yang tidak otomatis memberi kebaruan

- SVM, KNN, Naive Bayes, J48 dan LDA sudah digunakan untuk profil readmission
  diabetes dalam [studi 2019](https://link.springer.com/article/10.1186/s12911-019-0990-x).
- EasyEnsemble sudah diteliti pada catatan diabetes dari 130 rumah sakit periode
  1999-2008: [Xiang dkk., 2021](https://vuir.vu.edu.au/49252/),
  [teks lengkap](https://vuir.vu.edu.au/49252/1/predictive_modeling_of_30_day_readmission_risk_of.6.pdf).
- EBM, RuleFit dan LightGBM tercantum pada eksperimen Diabetes 130-US dalam
  [SAFIRE, 2026, tabel 10](https://www.mdpi.com/2227-7390/14/13/2255).
  Tabel ditemukan pada hasil indeks; akses halaman penuh dibatasi 429 ketika
  dicek, sehingga detail protokol belum diaudit.
- RUSBoost relevan untuk imbalance, tetapi literatur readmission juga sudah
  memakainya. Ia bukan pilihan yang aman untuk diklaim baru hanya karena tidak
  ada pada daftar awal. [Implementasi resmi](https://imbalanced-learn.org/stable/references/generated/imblearn.ensemble.RUSBoostClassifier.html).

## Rancangan kontribusi yang disarankan

Pertanyaan penelitian: bagaimana NGBoost dibanding model pembanding dalam
diskriminasi dan kalibrasi risiko readmission <30 pada pasien yang tidak
tumpang tindih antarset?

1. Pertahankan cohort/target dan ID pasien yang sama untuk perbandingan.
2. Gunakan CV berbasis pasien, fit ulang preprocessing di tiap fold, dan
   anggaran tuning yang sebanding. Test tetap ditutup sampai keputusan dibekukan.
3. Ukur AP, ROC-AUC, precision/recall/F1, Brier score, log loss dan kurva kalibrasi.
4. Bila melakukan kalibrasi atau memilih threshold, gunakan data validasi
   yang benar; jangan mengoptimalkan dari data uji final.
5. Hitung interval ketidakpastian metrik dengan resampling pada tingkat pasien,
   bukan menganggap seluruh kunjungan sebagai observasi independen.
6. Bandingkan kontribusi/protokol dengan paper terdahulu, bukan mengklaim
   patient-level split atau kalibrasi sebagai hal baru tanpa pemeriksaan literatur.

Judul kerja: "Evaluasi Diskriminasi dan Kalibrasi NGBoost untuk Prediksi
Readmission Pasien Diabetes dengan Validasi Berbasis Pasien".

## Cakupan pencarian

Kombinasi istilah NGBoost / natural gradient boosting / Rotation Forest /
RUSBoost dengan diabetes, diabetic, readmission, Diabetes 130-US Hospitals,
130 dan diabetic_data. Pencarian kandidat interpretabilitas juga mencakup
EBM, RuleFit dan FIGS; pencarian ensemble mencakup EasyEnsemble dan TabPFN.
Tidak semua hasil telah dibaca penuh. Status kandidat tidak menyatakan bahwa
semua algoritma tersebut baru, lebih akurat, atau layak publikasi tanpa eksperimen.
