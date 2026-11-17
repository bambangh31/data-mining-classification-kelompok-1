"""Pembahasan rinci Week 13; angka dibaca dari artefak eksperimen tersimpan.

Tidak melakukan pelatihan, pemilihan parameter, atau evaluasi test baru.
"""


def add_details(chapter, context):
    p = context['paragraph']
    h = context['heading']
    read = context['read_csv']
    meta = context['meta']
    dec = context['dec']
    count = context['count']
    labels = context['labels']

    def table(title, rows, widths):
        context['tab'](rows, widths, title=title)

    def paragraphs(*texts):
        for text in texts:
            p(text)

    if chapter == 'Pendahuluan':
        h('Definisi masalah klasifikasi dan waktu prediksi')
        paragraphs(
            'Masukan model adalah karakteristik satu kunjungan rawat inap yang telah tersedia pada akhir perawatan. Keluaran berupa probabilitas label readmitted <30. Waktu prediksi ditetapkan saat pasien keluar karena lama rawat, jumlah prosedur, hasil pemeriksaan, perubahan obat dan status keluar baru lengkap pada tahap tersebut. Apabila tujuan diubah menjadi prediksi saat masuk rumah sakit, fitur-fitur yang baru diketahui saat keluar perlu ditinjau dan eksperimen harus diulang.',
            'Penelitian menggunakan label pada CSV sumber secara langsung. Kelas positif bukan semua kejadian readmission: kunjungan yang diikuti rawat inap ulang >30 masuk kelas negatif bersama NO. Karena itu, istilah negatif pada laporan berarti tidak memiliki label <30 dalam dataset, bukan pernyataan bahwa pasien tidak pernah dirawat lagi. Dataset tidak digunakan untuk menyimpulkan bahwa terapi tertentu menyebabkan atau mencegah readmission.',
            'Terdapat dua unit yang perlu dibedakan. Unit observasi dan perhitungan metrik adalah kunjungan, sedangkan unit pembagian data adalah pasien. Seluruh kunjungan seorang pasien harus berada pada set yang sama. Satu pasien dapat menyumbang lebih dari satu kesalahan prediksi; jumlah kesalahan kunjungan tidak boleh langsung disebut jumlah pasien yang salah diprediksi.'
        )
        h('Hubungan laporan dengan tahapan tugas')
        table('Pemetaan kebutuhan tugas ke bukti pekerjaan', [
            ['Tahap', 'Pertanyaan yang dijawab', 'Bukti yang digunakan'],
            ['Week 10', 'Data apa, makna kolom/kode, tujuan dan algoritma?', 'CSV asli, mapping administrasi, profil dan kamus data.'],
            ['Week 11', 'Bagaimana data dibersihkan dan model dipelajari?', 'Kode preprocessing/mining, metadata dan metrik validation awal.'],
            ['Week 12', 'Bagaimana ambang dipilih dan hasil uji dibaca?', 'Protokol beku, metrik test historis, kelompok kesalahan.'],
            ['Week 13', 'Apa hasil sementara dan tindak lanjut revisi?', 'Sintesis hasil dan eksperimen NGBoost tanpa/dengan ROS pada validation.'],
        ], [22,65,77])
        p('Laporan pertama menyajikan pekerjaan yang telah tersedia sampai revisi Week 13. Penambahan uraian pada versi ini bertujuan membuat hubungan antara keputusan metode, implementasi dan angka hasil dapat diperiksa. Rincian yang belum dikerjakan tetap ditulis sebagai keterbatasan atau rencana, sehingga pembaca dapat membedakan hasil pengamatan dari usulan penelitian berikutnya.')

    elif chapter == 'Business objective dan tujuan data mining':
        h('Pengguna hasil dan keputusan yang didukung')
        paragraphs(
            'Dalam skenario pembelajaran, hasil klasifikasi dapat menjadi bahan simulasi penyusunan prioritas peninjauan kunjungan setelah pasien keluar. Pengguna hipotetisnya adalah tim yang meninjau kebutuhan tindak lanjut, sedangkan keputusan yang disimulasikan ialah kunjungan mana yang lebih dahulu diperiksa. Proyek tidak mencakup integrasi sistem rumah sakit, intervensi kepada pasien, atau pengukuran manfaat klinis.',
            'Tujuan bisnis perlu diterjemahkan menjadi keluaran yang bisa dinilai pada data. Model yang hanya mengeluarkan kelas mayoritas dapat mencapai akurasi tinggi tetapi tidak membantu menemukan label <30. Karena itu, keberhasilan teknis dinilai dari kemampuan ranking di atas baseline, jangkauan kelas positif, dan beban false positive. Tidak ditetapkan klaim penghematan biaya karena tidak tersedia nilai biaya, kapasitas layanan atau hasil intervensi.'
        )
        h('Konsekuensi false positive dan false negative')
        table('Makna keputusan pada skenario peninjauan', [
            ['Keadaan', 'Makna pada data', 'Implikasi dalam simulasi'],
            ['True positive', 'Label <30 dan diprediksi positif.', 'Kasus target masuk daftar peninjauan.'],
            ['False positive', 'Label NO/>30 tetapi diprediksi positif.', 'Daftar peninjauan bertambah tanpa label target <30.'],
            ['False negative', 'Label <30 tetapi diprediksi negatif.', 'Kasus target tidak masuk daftar pada ambang tersebut.'],
            ['True negative', 'Label NO/>30 dan diprediksi negatif.', 'Kunjungan dikeluarkan dari daftar sesuai label biner.'],
        ], [30,66,68])
        paragraphs(
            'Menurunkan ambang dapat menambah true positive sekaligus false positive. Tanpa informasi kapasitas dan biaya, tidak ada dasar untuk menyatakan satu ambang sebagai pilihan operasional terbaik. Aturan maksimum F1 dipakai sebagai aturan eksperimen yang dapat direproduksi, bukan sebagai keputusan layanan yang telah disepakati pengguna rumah sakit.',
            'Kriteria keberhasilan laporan juga mencakup keterlacakan. Sumber data, definisi label, aturan pengecualian, pemisahan pasien dan batas penggunaan test harus dinyatakan. Hasil yang tidak lebih baik setelah oversampling tetap merupakan temuan yang perlu dilaporkan. Keberhasilan menyelesaikan tugas tidak sama dengan keberhasilan model mencapai kelayakan penggunaan nyata.'
        )
        h('Keterbatasan sumber daya dan ruang lingkup')
        p('Percobaan menggunakan konfigurasi awal yang tetap, satu pembagian pasien, dan representasi fitur bersama. Tidak dilakukan grid search atau pencarian banyak seed untuk mendapatkan skor tertinggi. Pilihan ini menjaga percobaan tetap terbatas dan mudah ditelusuri, tetapi tidak cukup untuk menentukan algoritma terbaik secara umum. Perbandingan hanya berlaku pada cohort, fitur, parameter dan protokol yang dijelaskan dalam laporan.')

    elif chapter == 'Dataset dan karakteristik data':
        h('Asal berkas, skema, dan lingkup statistik')
        paragraphs(
            'Dua berkas sumber utama adalah diabetic_data.csv dan IDS_mapping.csv. CSV observasi mempunyai 50 kolom: dua ID, satu target dan 47 kandidat prediktor. Jadi, angka 50 kolom pada berkas dan 47 fitur pada deskripsi dataset tidak bertentangan. Setelah keputusan berbasis train diterapkan, jumlah kolom prediktor berubah menjadi 43; sesudah encoding jumlah dimensi berubah lagi menjadi 1.222.',
            'Statistik pada subbagian ini dihitung dari CSV asli sebelum pengecualian cohort, kecuali dinyatakan lain. Profil awal dipakai untuk memahami bentuk data, sedangkan keputusan median, kategori langka, scaling dan penghapusan kolom dipelajari dari train. Pemisahan lingkup tersebut mencegah angka deskriptif seluruh data dianggap sebagai statistik yang boleh dipakai melatih transformer.'
        )
        profile = context['json'].loads((context['ROOT']/'results/dataset/dataset_profile.json').read_text(encoding='utf-8'))
        p(f"Data memuat {count(profile['repeated_patient_rows_beyond_first'])} baris kunjungan di luar kemunculan pertama tiap pasien. Angka ini bukan jumlah pasien yang berulang, melainkan jumlah baris tambahan. Tidak ditemukan duplikasi seluruh baris maupun encounter_id pada profil sumber. Kunjungan berulang pasien dipertahankan karena merupakan observasi berbeda, lalu diikat dalam kelompok pasien saat pembagian data.")
        h('Kamus seluruh kolom: identitas dan karakteristik kunjungan')
        dictionary = read('results/dataset/data_dictionary.csv')
        groups = [dictionary[:13], dictionary[13:24], dictionary[24:37], dictionary[37:]]
        titles = ['Identitas, demografi, dan administrasi', 'Layanan, diagnosis, dan pemeriksaan',
                  'Status obat bagian pertama', 'Status obat bagian kedua dan target']
        for index, (title, rows) in enumerate(zip(titles, groups)):
            if index:
                h('Kamus seluruh kolom: ' + title.lower())
            table('Kamus data - ' + title.lower(), [
                ['Kolom', 'Peran/tipe', 'Arti dan nilai pada data asli'],
                *[[r['kolom'], r['peran']+'; '+r['tipe_analisis'],
                   r['deskripsi']+'\nNilai/contoh: '+r['nilai_aktual_atau_contoh']]
                  for r in rows],
            ], [39,26,99])
        paragraphs(
            'Delapan kolom numerik berisi hitungan layanan atau lama rawat. Kode diagnosis dan administrasi tetap kategorikal walaupun sebagian ditulis dengan angka. Tidak tepat mengartikan selisih kode 1 dan 2 sebagai jarak klinis yang sama dengan selisih kode 2 dan 3. Usia juga dipertahankan sebagai kelompok interval, tanpa menganggap titik tengah interval sebagai umur sebenarnya.',
            'Status obat membedakan No, Steady, Up dan Down sesuai kategori yang benar-benar muncul pada obat tersebut. No berarti tidak diresepkan pada catatan ini; nilainya berbeda dari ? yang menunjukkan missing. Perubahan dosis menunjukkan status tercatat selama kunjungan, bukan efek kausal obat terhadap readmission. Beberapa obat sangat jarang atau konstan sehingga keberadaan nama kolom belum menjamin informasi prediktif yang bervariasi.'
        )
        h('Statistik delapan variabel numerik')
        table('Statistik numerik pada seluruh CSV asli', [
            ['Variabel', 'Min', 'Q1', 'Median', 'Q3', 'Maks', 'Rerata'],
            *[[r['feature'], *[f"{float(r[k]):.2f}".replace('.',',') for k in ['min','25%','50%','75%','max','mean']]]
              for r in read('results/dataset/numeric_summary.csv')],
        ], [43,17,18,22,18,18,28])
        paragraphs(
            'Median number_outpatient dan number_emergency sama-sama 0, sedangkan maksimum masing-masing 42 dan 76. Perbedaan ini menunjukkan banyak kunjungan tanpa riwayat layanan tersebut dan sebagian kecil dengan hitungan tinggi. Laporan tidak menghapus nilai tinggi hanya karena jauh dari median: pipeline memeriksa validitas bilangan nonnegatif, bukan menerapkan pemotongan outlier berdasarkan perkiraan visual.',
            'Rerata lama rawat sekitar 4,40 hari dengan median 4 hari dan rentang 1-14 hari. Jumlah obat mempunyai median 15 dan maksimum 81. Besaran antarvariabel berbeda, sehingga pipeline numerik menggunakan standardisasi setelah imputasi. Ringkasan ini tidak memuat uji hubungan dengan target dan tidak menunjukkan variabel mana yang paling penting bagi model.'
        )
        h('Missing value dan kategori yang tampak serupa')
        table('Missing awal sebelum perubahan kode administrasi', [
            ['Kolom', 'Baris missing', 'Persen data asli'],
            *[[r['kolom'],count(r['missing_jumlah']),r['missing_persen'].replace('.',',')+'%']
              for r in read('results/dataset/missing_summary.csv')],
        ], [70,47,47])
        paragraphs(
            'Missing awal di tabel berarti tanda ? atau string kosong setelah normalisasi. Kode administrasi yang bermakna tidak diketahui ditangani sesudahnya, sehingga kolom yang tampak tidak memiliki missing pada CSV dapat mempunyai missing setelah cleaning. Persentase pada seluruh CSV juga dapat berbeda sedikit dari persentase train karena cohort dan keanggotaan set berbeda.',
            f"String None pada max_glu_serum muncul {count(profile['lab_none_counts']['max_glu_serum'])} kali dan pada A1Cresult {count(profile['lab_none_counts']['A1Cresult'])} kali. Pada dua kolom ini None berarti tes tidak dilakukan, sehingga dipertahankan sebagai kategori. Mengubah semua string None menjadi NaN akan menyatukan dua makna yang berbeda dan mengubah informasi pemeriksaan yang diterima encoder."
        )
        h('Kamus lengkap kode jenis masuk')
        admin = read('results/dataset/admin_code_dictionary.csv')
        for index, field in enumerate(['admission_type_id','discharge_disposition_id','admission_source_id']):
            if index:
                h('Kamus lengkap kode ' + ('status keluar' if index == 1 else 'sumber masuk'))
            rows = [r for r in admin if r['kolom'] == field]
            table('Mapping ' + field + ' dan frekuensi asli', [
                ['Kode', 'Arti pada IDS_mapping.csv', 'Jumlah', 'Perlakuan'],
                *[[r['kode'],r['arti_sumber'],count(r['jumlah_data_asli']),r['perlakuan']] for r in rows],
            ], [13,88,23,40])
            p('Arti berbahasa Inggris dipertahankan dari mapping sumber agar kode mudah dicocokkan kembali. Frekuensi dihitung sebelum cleaning pada seluruh CSV asli. Kode dengan jumlah 0 tetap dicantumkan karena tersedia dalam mapping; keberadaan kode pada kamus tidak berarti kode tersebut muncul pada data pelatihan.')
        paragraphs(
            'Kode harus selalu dibaca bersama nama kolomnya. Misalnya, kode 20 pada status keluar berarti meninggal di fasilitas medis, sedangkan pada sumber masuk berarti Not Mapped. Aturan cleaning menggunakan pasangan kolom dan kode, bukan menghapus setiap sel bernilai 20. Kode hospice 13 dan 14 pada status keluar tidak secara otomatis berarti meninggal dan tetap dipertahankan pada cohort yang digunakan.',
            'Payer_code dan medical_specialty mempunyai banyak kategori serta missing yang cukup besar. Laporan tidak menebak kepanjangan setiap singkatan pembayar yang tidak dijelaskan mapping administrasi. Nilainya dipertahankan sebagai kategori sumber. Hal yang sama berlaku untuk kode diagnosis ICD-9: pipeline tidak mengubahnya menjadi kelompok penyakit buatan atau angka kontinu.'
        )
        h('Perubahan populasi setelah pengecualian meninggal')
        quality = meta['quality']
        table('Distribusi target sebelum dan sesudah pemilihan cohort', [
            ['Target asli', 'CSV asli', 'Setelah cohort', 'Label biner'],
            *[[label,count(quality['raw_target_counts'][label]),count(quality['clean_original_target_counts'][label]),'1' if label=='<30' else '0']
              for label in ['NO','>30','<30']],
        ], [41,41,41,41])
        p('Pada data ini seluruh 1.652 kunjungan yang dikeluarkan berlabel NO. Jumlah <30 dan >30 tidak berubah. Akibatnya prevalensi positif cohort sedikit lebih tinggi daripada data asli. Pengecualian tidak dilakukan untuk mengejar skor, melainkan untuk menyelaraskan populasi dengan prediksi setelah keluar hidup. Hal ini membatasi penerapan hasil pada cohort yang sama dan perlu disebut ketika membandingkan dengan penelitian yang memakai aturan pengecualian berbeda.')

    elif chapter == 'Rancangan metode dan algoritma':
        h('Pemetaan variabel masukan ke prediksi')
        paragraphs(
            'Secara konseptual, tiap kunjungan diwakili vektor x dan label y dalam {0,1}. Model mempelajari fungsi p(x) untuk memperkirakan peluang label 1. Keputusan biner dibuat dengan aturan y_pred = 1 bila p(x) >= t dan 0 jika lebih kecil. Nilai t adalah ambang yang dipilih pada validation. Dengan p(x) yang sama, perubahan t dapat mengubah jumlah prediksi positif tanpa memperbaiki urutan ranking probabilitas.',
            'Representasi x tidak langsung memakai ID dan readmitted. Setelah seleksi, 43 kolom ditransformasikan menjadi matriks sparse 1.222 dimensi. Adapter mengubah matriks menjadi 32 komponen kontinu agar kedua model utama menerima bentuk masukan yang sama. Jadi, hasil merupakan penilaian atas rangkaian preprocessing, adapter dan model, bukan kemampuan algoritma pada 47 kolom mentah.'
        )
        h('Mekanisme pembelajaran NGBoost pada implementasi')
        paragraphs(
            'Model menggunakan NGBClassifier dengan Bernoulli dan LogScore. Untuk sebuah label y dan probabilitas p, log loss biner adalah -[y log(p) + (1-y) log(1-p)]. Kontribusi kesalahan lebih besar ketika model memberi probabilitas tinggi pada label yang salah. Parameter distribusi diperbarui secara bertahap dengan natural gradient, sedangkan pohon regresi menjadi pembelajar dasar untuk arah pembaruan (Duan dkk., 2020).',
            'Konfigurasi proyek membatasi pohon pada kedalaman 3 dan minimum 20 sampel per daun. Learning rate 0,03 membatasi besar langkah pembaruan, sementara 150 estimator menjadi batas jumlah iterasi. Minibatch_frac 0,75 memilih sebagian baris dari kumpulan train pada tiap iterasi. Nilai-nilai tersebut adalah konfigurasi percobaan; laporan belum membuktikan bahwa konfigurasi itu optimal.'
        )
        h('Mekanisme Rotation Forest dan pembanding prior')
        paragraphs(
            'Rotation Forest membangun keragaman pohon melalui transformasi PCA pada kelompok fitur. Implementasi aeon yang digunakan menerima atribut kontinu; proyek memasukkan hasil adapter 32 dimensi dan memakai 20 estimator, min_group/max_group 3 serta remove_proportion 0,5. Transformasi di dalam ensemble berbeda dari SVD bersama sebelum model: keduanya terjadi pada tahap yang berbeda (Rodriguez dkk., 2006; dokumentasi aeon 1.6.0).',
            'Baseline prior mengestimasi proporsi kelas dari train asli. Semua kunjungan evaluasi menerima probabilitas positif yang sama, sekitar 0,1137. Pada ambang 0,5 seluruh prediksi menjadi negatif. Baseline diperlukan agar akurasi sekitar 89% tidak keliru dibaca sebagai bukti model kuat. Karena ranking baseline konstan, ROC-AUC bernilai 0,5 dan AP mengikuti prevalensi positif pada set evaluasi.'
        )
        h('Alasan representasi bersama dan batas perbandingan')
        table('Komponen yang disamakan dan yang berbeda', [
            ['Komponen', 'Pelaksanaan', 'Konsekuensi interpretasi'],
            ['Cohort dan split', 'Sama untuk model awal dan revisi.', 'Perbedaan skor tidak berasal dari pembagian pasien baru.'],
            ['Adapter', 'SVD 32 + scaler; fit train asli.', 'Masukan kontinu sebanding; belum menguji tanpa SVD.'],
            ['Model awal', 'NGBoost 150 dan Rotation Forest 20 estimator.', 'Jumlah estimator dan biaya komputasi tidak disetarakan.'],
            ['Ablasi ROS', 'NGBoost dengan parameter tetap; ROS menjadi perbedaan utama.', 'Mengamati penambahan ROS pada konfigurasi ini.'],
            ['Pemilihan ambang', 'Maksimum F1 pada validation.', 'Hasil validation terpilih dapat optimistis.'],
        ], [31,64,69])
        p('Tidak dilakukan klaim bahwa SVD 32 adalah jumlah komponen terbaik. Metadata eksperimen awal mencatat jumlah explained variance ratio sekitar 0,7610, yang menjelaskan representasi input pada train, bukan persentase akurasi dan bukan persentase informasi target yang berhasil dipertahankan. Evaluasi tanpa SVD atau dengan jumlah komponen lain memerlukan eksperimen terpisah.')

    elif chapter == 'Implementasi preprocessing dan pembagian data':
        h('Urutan cleaning yang dapat ditelusuri')
        table('Urutan operasi dalam clean_data', [
            ['Urutan', 'Operasi', 'Alasan'],
            ['1', 'Periksa kolom wajib dan hilangkan spasi tepi.', 'Mencegah perbedaan format dibaca sebagai nilai berbeda.'],
            ['2', 'Ubah ? dan kosong menjadi missing.', 'Menyamakan penanda kehilangan data tanpa mengubah None lab.'],
            ['3', 'Periksa ID dan hapus duplikasi identik.', 'Menjaga kunjungan dapat diaudit dan dibagi berdasarkan pasien.'],
            ['4', 'Tolak encounter_id konflik dan target tidak dikenal.', 'Menghentikan proses ketika makna observasi tidak dapat dipastikan.'],
            ['5', 'Keluarkan status meninggal; ubah kode unknown/gender invalid.', 'Menetapkan cohort dan membedakan unknown dari kategori valid.'],
            ['6', 'Konversi dan validasi delapan numerik.', 'Menolak teks tidak numerik, negatif dan hitungan pecahan.'],
            ['7', 'Bentuk target dan split pasien sebelum fit.', 'Membatasi pembelajaran statistik pada train.'],
        ], [17,80,67])
        paragraphs(
            'Normalisasi deterministik berdasarkan skema dan arti kode tidak sama dengan belajar dari statistik seluruh data. Daftar kode unknown dan kode meninggal ditentukan dari mapping sumber. Sebaliknya, penentuan kolom dengan missing >50%, kolom konstan, median dan kategori langka bergantung pada isi train sehingga baru dijalankan setelah split.',
            'Pipeline tidak menghapus kunjungan berulang pasien, tidak menyeimbangkan seluruh cohort sebelum split, dan tidak memasukkan ID menjadi prediktor. Jika encounter_id muncul lagi dengan isi berbeda, proses berhenti untuk pemeriksaan manual. Pada data yang tersedia, jumlah duplikasi identik 0 sehingga pembersihan duplikasi tidak mengubah ukuran cohort.'
        )
        h('Rincian split dan jawaban penggunaan seluruh data train')
        table('Peran setiap kumpulan data dalam eksperimen', [
            ['Kumpulan', 'Boleh dipelajari', 'Tidak dipakai untuk'],
            ['Train asli', 'Seleksi fitur, imputasi, encoder, scaler, SVD, parameter model.', 'Pelaporan performa generalisasi sebagai hasil independen.'],
            ['Train setelah ROS', 'Fit NGBoost_ROS; hanya turunan dari train asli.', 'Membentuk pasien baru atau mengganti distribusi validation/test.'],
            ['Validation', 'Membandingkan hasil dan memilih ambang.', 'Fit ulang median, kategori, SVD atau model.'],
            ['Test historis', 'Evaluasi model awal setelah protokol dibekukan.', 'Memilih ambang revisi atau mengklaim holdout baru.'],
        ], [32,68,64])
        paragraphs(
            'Pembagian pertama memilih sekitar 70% pasien sebagai train dan 30% sisanya sebagai kumpulan sementara. Pembagian kedua membagi kumpulan sementara menjadi validation dan test dengan proporsi setengah-setengah. Kedua GroupShuffleSplit memakai seed 42. Ukuran test_size merujuk jumlah kelompok pasien, sehingga proporsi kunjungan tidak harus tepat 70/15/15 (dokumentasi scikit-learn 1.7).',
            'Jawaban atas pertanyaan dosen adalah: seluruh dataset tidak dipakai untuk train. Namun, seluruh 70.071 kunjungan yang ditetapkan sebagai train menjadi kumpulan pelatihan. NGBoost mengambil minibatch acak 75% per iterasi dari kumpulan itu; pada varian ROS kumpulannya berukuran 124.208. Minibatch adalah cara menghitung pembaruan model, sedangkan split menentukan data mana yang boleh ikut belajar.'
        )
        h('Seleksi kolom dan perubahan missing pada train')
        missing = read('results/preprocessing/missing_values.csv')
        selected = [r for r in missing if r['missing_train_fraction'] and float(r['missing_train_fraction'])>0]
        table('Missing setelah cleaning dan proporsi pada train', [
            ['Kolom', 'Missing cohort', 'Missing train (%)', 'Keputusan'],
            *[[r['column'],count(r['missing_clean']),f"{100*float(r['missing_train_fraction']):.3f}".replace('.',','),
               'Dikeluarkan' if r['column']=='weight' else 'Dipertahankan; kategori missing'] for r in selected],
        ], [45,36,37,46])
        paragraphs(
            'Ambang penghapusan missing menggunakan lebih dari 50% pada train. Weight berada di atas ambang dan dikeluarkan. Medical_specialty mendekati 49% pada train sehingga tetap dipertahankan; payer_code juga tetap masuk. Keputusan ini mengikuti aturan yang sama, bukan memilih kolom setelah melihat skor validasi. Tiga kolom konstan pada train tidak mempunyai variasi yang dapat dipelajari sehingga dikeluarkan.',
            'Sesudah dua ID dan target dilepas, terdapat 47 kandidat fitur. Penghapusan weight dan tiga kolom konstan menyisakan 43: delapan numerik dan 35 kategorikal. Tidak ada imputasi terhadap target. Nilai target yang tidak dikenal menyebabkan penghentian proses, karena memberi label buatan akan mengubah masalah klasifikasi yang dievaluasi.'
        )
        h('Imputasi, one-hot encoding, dan standardisasi')
        paragraphs(
            'Jalur numerik menggunakan SimpleImputer strategi median dan StandardScaler. Untuk nilai x, standardisasi mengikuti bentuk z = (x - rerata_train)/simpangan_baku_train. Rerata dan simpangan baku dipelajari sesudah imputasi train; validation/test hanya ditransformasikan. Walaupun numerik pada CSV yang tersedia tidak missing, aturan imputasi membuat pipeline tetap memiliki perilaku yang jelas terhadap masukan kosong yang valid.',
            'Jalur kategori mengganti missing dengan token __MISSING__. OneHotEncoder memakai min_frequency 10 dan handle_unknown infrequent_if_exist. Kategori dengan frekuensi train di bawah batas dikelompokkan sebagai infrequent; kategori baru diarahkan ke kelompok itu bila tersedia, dan ditangani menurut perilaku encoder bila tidak tersedia. Validation/test tidak dipakai menambah daftar kategori atau menghitung ulang frekuensi (dokumentasi scikit-learn 1.7).',
            'One-hot menghindari pemberian urutan numerik buatan pada diagnosis, obat dan kode administrasi. Matriks sparse menyimpan terutama posisi yang bernilai nonnol, karena banyak indikator kategori bernilai nol. Jumlah 1.222 adalah dimensi keluaran transformer, bukan jumlah variabel klinis asli. Nama fitur dan skema disimpan agar hubungan antara keluaran dan kolom sumber dapat diperiksa.'
        )
        h('Adapter SVD dan artefak hasil preprocessing')
        table('Ukuran representasi pada tiap set', [
            ['Set', 'Baris', 'Dimensi encoded', 'Elemen nonnol', 'Dimensi adapter'],
            *[[name,count(info['rows']),str(info['encoded_shape'][1]),count(info['nonzero_values']),'32']
              for name,info in meta['splits'].items()],
        ], [30,31,36,36,31])
        paragraphs(
            'TruncatedSVD memproyeksikan matriks sparse menjadi komponen kontinu tanpa memusatkan seluruh matriks sparse. Komponen yang digunakan berjumlah 32, n_iter 5 dan random_state 42. StandardScaler berikutnya bekerja pada hasil proyeksi. Adapter di-fit pada train asli, kemudian objek yang sama mentransformasikan validation/test (dokumentasi scikit-learn 1.7).',
            'Artefak yang disimpan mencakup cleaned.csv, X dan y tiap set, ID audit, feature_schema.json, feature_names.json, preprocessor.joblib serta metadata.json. File ID tidak dimasukkan ke model. Metadata mencatat hash CSV sumber, seed, versi library, keputusan kolom, jumlah baris, jumlah pasien dan jumlah kelas sehingga hasil dapat dicocokkan dengan eksperimen berikutnya.'
        )

    elif chapter == 'Implementasi mining dan rancangan evaluasi':
        h('Kontrak input, probabilitas, dan keluaran model')
        paragraphs(
            'Runner awal memastikan target preprocessing adalah biner sebelum memuat matriks train dan validation. Adapter di-fit sekali pada train dan dipakai untuk seluruh model awal. Fungsi positive_probability memilih kolom probabilitas kelas 1 berdasarkan classes_ bila tersedia; untuk NGBClassifier Bernoulli digunakan urutan label 0/1 yang disyaratkan model. Dengan demikian, probabilitas kelas negatif tidak keliru dipakai sebagai skor kelas positif.',
            'Fungsi binary_metrics memeriksa panjang target dan probabilitas, keberadaan dua kelas, serta probabilitas finite dalam rentang 0-1. Label prediksi dihitung dengan perbandingan >= threshold. Confusion matrix menggunakan urutan label [0,1]. Jika tidak ada prediksi positif, precision dan F1 dikembalikan 0 melalui zero_division=0; hasil itu tidak diartikan sebagai nilai precision yang terukur dari sampel positif.'
        )
        h('Makna metrik dan contoh perhitungan dari hasil nyata')
        paragraphs(
            'Pada test historis NGBoost, TP=540, FP=1.874, FN=1.191 dan TN=11.373. Precision = 540/(540+1.874) = 0,2237; recall = 540/(540+1.191) = 0,3120. F1 = 2TP/(2TP+FP+FN) = 0,2606. Accuracy = (TP+TN)/14.978 = 0,7954. Contoh ini menggunakan hasil tersimpan, bukan observasi sintetis.',
            'Balanced accuracy merata-ratakan recall kelas positif dan spesifisitas kelas negatif. Ukuran ini memberi bobot yang sama kepada kedua kelas, sehingga prediktor semua negatif memperoleh 0,5 meskipun accuracy tinggi. F1 berfokus pada precision dan recall positif serta tidak memasukkan true negative secara langsung. Pemilihan metrik menentukan aspek kesalahan mana yang diperhatikan.'
        )
        table('Tiga kelompok ukuran evaluasi', [
            ['Kelompok', 'Metrik', 'Pertanyaan yang dijawab'],
            ['Keputusan biner', 'Precision, recall, F1, accuracy, balanced accuracy, confusion matrix.', 'Apa akibat memilih ambang tertentu?'],
            ['Ranking', 'AP dan ROC-AUC.', 'Seberapa baik skor mengurutkan kunjungan positif dan negatif?'],
            ['Probabilitas', 'Brier score, log loss, diagram reliabilitas.', 'Seberapa dekat probabilitas terhadap label/proporsi aktual?'],
        ], [31,68,65])
        paragraphs(
            'AP dihitung sebagai penjumlahan precision pada titik kenaikan recall dengan bobot besar kenaikan tersebut. Implementasi menggunakan average_precision_score, bukan luas trapezoid kurva precision-recall. AP tidak memerlukan satu threshold tetap; karena itu, model dengan F1 nol pada ambang 0,5 masih dapat mempunyai AP di atas baseline (dokumentasi scikit-learn 1.7).',
            'Brier score adalah rerata (p-y)^2. Log loss memberi penalti kuat pada prediksi sangat yakin yang salah. Keduanya lebih kecil lebih baik dan tetap sama ketika hanya threshold label diubah. Diagram reliabilitas membandingkan rerata probabilitas dengan proporsi positif per bin; bin dengan sedikit observasi lebih mudah berubah. Laporan tidak melakukan fitting kalibrasi tambahan.'
        )
        h('Pembekuan protokol dan batas penggunaan test')
        table('Urutan pemilihan dan evaluasi Week 12', [
            ['Tahap', 'Data yang dipakai', 'Keputusan/hasil'],
            ['Reproduksi validation', 'Model awal dan validation.', 'Cocokkan metrik dengan eksperimen Week 11.'],
            ['Pilih threshold', 'Skor dan label validation.', 'Maksimum F1 positif; threshold lebih tinggi bila seri.'],
            ['Pilih model utama', 'AP validation kedua model.', 'NGBoost dipilih; baseline tetap threshold 0,5.'],
            ['Simpan protokol', 'Metadata dan artefak lokal.', 'Hash dan konfigurasi dikunci sebelum evaluasi test tahap awal.'],
            ['Evaluate', 'Model/protokol yang cocok dan test.', 'Simpan metrik, diagram dan analisis kelompok.'],
        ], [35,54,75])
        p('Protokol membatasi keputusan pada evaluasi awal yang tersimpan. Setelah hasil test diketahui, test tersebut tidak lagi diperlakukan sebagai sumber informasi yang belum pernah dilihat untuk eksperimen baru. Karena itu, percobaan ROS revisi hanya dilaporkan pada validation dan tidak menerima angka test milik model lama. Hash memeriksa konsistensi berkas, tetapi bukan bukti bahwa keseluruhan proses bebas dari semua bentuk bias penelitian.')

    elif chapter == 'Hasil Week 11 dan Week 12':
        h('Metrik tambahan dan jumlah kesalahan pada validation awal')
        table('Confusion matrix validation awal pada ambang 0,5', [
            ['Model', 'TN', 'FP', 'FN', 'TP', 'Balanced acc.'],
            *[[labels[r['model']],*[count(r[k]) for k in ['tn','fp','fn','tp']],dec(r['balanced_accuracy'])]
              for r in context['old_validation']],
        ], [39,25,24,26,23,27])
        paragraphs(
            'NGBoost dan baseline mempunyai confusion matrix yang sama pada ambang 0,5, tetapi probabilitasnya berbeda. AP NGBoost 0,1993 melebihi AP baseline 0,1101, sehingga ranking kunjungannya lebih informatif pada validation ini. Kesimpulan yang tepat adalah threshold 0,5 belum menghasilkan deteksi positif, bukan bahwa NGBoost sama persis dengan baseline pada semua ukuran.',
            'Rotation Forest menghasilkan 103 prediksi positif: 34 benar dan 69 salah. Precision sekitar 0,3301 lebih tinggi daripada hasilnya setelah threshold diperkecil pada evaluasi test, tetapi recall validation hanya 0,0205. Angka precision tidak cukup dibaca sendiri ketika hampir semua kasus positif terlewat. Perbandingan antarset juga harus memperhatikan perubahan threshold dan komposisi kasus.'
        )
        h('Confusion matrix dan kualitas probabilitas pada test historis')
        table('Jumlah prediksi test pada threshold terkunci', [
            ['Model', 'TN', 'FP', 'FN', 'TP', 'Prediksi +'],
            *[[labels[r['model']],*[count(r[k]) for k in ['tn','fp','fn','tp']],count(int(r['tp'])+int(r['fp']))]
              for r in context['test']],
        ], [39,25,25,25,25,25])
        table('Ranking dan probabilitas test historis', [
            ['Model', 'ROC-AUC', 'AP', 'Brier', 'Log loss', 'Bal. acc.'],
            *[[labels[r['model']],*[dec(r[k]) for k in ['roc_auc','average_precision','brier_score','log_loss','balanced_accuracy']]]
              for r in context['test']],
        ], [39,25,25,25,25,25])
        paragraphs(
            'NGBoost mengeluarkan 2.414 prediksi positif pada test historis dan 540 di antaranya benar berlabel <30. Rotation Forest mengeluarkan 3.814 prediksi positif dan menangkap 628 kasus. Tambahan 88 true positive pada Rotation Forest disertai tambahan 1.312 false positive dibanding NGBoost. Ini menunjukkan perbedaan beban peninjauan, bukan bukti langsung tentang manfaat atau biaya layanan.',
            'Baseline semua negatif mempunyai accuracy 0,8844, lebih tinggi daripada kedua model pada threshold terpilih. Namun, baseline melewatkan seluruh 1.731 kasus positif. NGBoost memiliki AP dan F1 lebih tinggi daripada Rotation Forest pada konfigurasi ini, sedangkan Rotation Forest memiliki recall lebih tinggi. Tidak ada satu angka accuracy yang merangkum seluruh kompromi tersebut.'
        )
        h('Hasil menurut kelompok usia')
        groups = read('results/week-12/test/error_groups.csv')
        rows = []
        for ng in [r for r in groups if r['variable']=='age' and r['model']=='NGBoost']:
            rf = next(r for r in groups if r['variable']=='age' and r['model']=='Rotation_Forest' and r['group']==ng['group'])
            rows.append([ng['group'],count(ng['n']),count(ng['positives']),
                         dec(ng['recall']) if ng['recall'] else 'Tidak terdefinisi',
                         dec(rf['recall']) if rf['recall'] else 'Tidak terdefinisi'])
        table('Recall menurut kelompok usia pada test historis', [
            ['Usia', 'Kunjungan', 'Positif', 'Recall NGBoost', 'Recall RotF'], *rows,
        ], [29,30,25,40,40])
        paragraphs(
            'Kelompok [0-10) mempunyai 26 kunjungan tanpa label positif sehingga recall tidak terdefinisi, bukan bernilai nol. Beberapa kelompok muda juga mempunyai sedikit kasus positif. Perubahan beberapa true positive saja dapat menggeser recall kelompok kecil secara besar; karena itu, perbandingan angka usia tidak cukup untuk menyimpulkan diskriminasi atau penyebab perbedaan model.',
            'Pada kelompok usia [70-80) terdapat 3.922 kunjungan dan 472 kasus positif. NGBoost menangkap 148 dan Rotation Forest 156. Kedua model masih melewatkan banyak kasus pada kelompok dengan kontribusi observasi besar ini. Analisis usia bersifat deskriptif pada threshold global yang sama untuk semua usia; tidak dipilih threshold per usia dari test.'
        )
        h('Rincian kasus terlewat menurut riwayat rawat inap')
        table('False negative menurut riwayat rawat inap, test historis', [
            ['Riwayat', 'Positif', 'TP NGBoost', 'FN NGBoost', 'TP RotF', 'FN RotF'],
            *[[ng['group'],count(ng['positives']),count(ng['tp']),count(ng['fn']),count(rf['tp']),count(rf['fn'])]
              for ng in groups if ng['variable']=='number_inpatient' and ng['model']=='NGBoost'
              for rf in groups if rf['variable']=='number_inpatient' and rf['model']=='Rotation_Forest' and rf['group']==ng['group']],
        ], [24,28,28,28,28,28])
        p('Perbedaan recall antarriwayat adalah indikasi lokasi kelemahan model untuk diteliti lebih lanjut. Laporan tidak melakukan feature importance atau SHAP sehingga tidak menyatakan bahwa number_inpatient menjadi penyebab kesalahan atau fitur terpenting. Pengelompokan menggunakan nilai variabel pada test dan prediksi yang sudah terkunci, tanpa melatih ulang model untuk kelompok tertentu.')
        h('Pembacaan bin reliabilitas NGBoost')
        table('Bin probabilitas NGBoost pada test historis', [
            ['Bin', 'Jumlah', 'Rerata probabilitas', 'Proporsi positif'],
            *[[r['bin'],count(r['count']),dec(r['mean_probability']),dec(r['positive_fraction'])]
              for r in read('results/week-12/test/calibration.csv') if r['model']=='NGBoost'],
        ], [20,36,54,54])
        p('Pada bin 0 terdapat 7.648 kunjungan dengan rerata probabilitas 0,0751 dan proporsi positif 0,0737. Pada bin 3 terdapat 113 kunjungan dengan rerata probabilitas 0,3346 dan proporsi positif 0,4248. Bin 4 hanya berisi 13 kunjungan sehingga tidak dapat dijadikan dasar kuat untuk klaim kalibrasi pada rentang tinggi. Tidak ada hasil untuk bin kosong; ketiadaan titik tidak berarti model akurat pada rentang itu.')

    elif chapter == 'Revisi dosen dan oversampling':
        h('Pemetaan masukan dosen ke perubahan nyata')
        table('Tindak lanjut tiga masukan dosen', [
            ['Masukan', 'Tindakan', 'Bukti'],
            ['Lengkapi karakteristik/kode.', 'Kamus 50 kolom, seluruh mapping administrasi dan frekuensinya; kematian 11/19/20/21.', 'data_dictionary.csv dan admin_code_dictionary.csv.'],
            ['Coba NGBoost dan oversampling.', 'Bandingkan NGBoost tanpa/dengan ROS pada split dan parameter tetap.', 'experiment.json serta validation_metrics.csv revisi.'],
            ['Apakah semua data dipakai train?', 'Jelaskan cohort, split pasien, jumlah train dan arti minibatch.', 'preprocessing_summary.json dan penjelasan metode.'],
        ], [39,78,47])
        h('Prosedur resampling yang dipakai')
        paragraphs(
            'RandomOverSampler memilih ulang sampel minoritas secara acak dengan pengembalian. Konfigurasi proyek memakai sampling_strategy minority, random_state 42 dan tidak memakai smoothed bootstrap. Setiap baris tambahan merupakan salinan contoh train yang sudah ada. Metode ini tidak memerlukan interpolasi kombinasi diagnosis atau status obat (dokumentasi imbalanced-learn).',
            'Urutannya adalah fit transformer dan adapter pada train asli, transform train dan validation, lalu fit_resample hanya pada representasi train. NGBoost tanpa ROS memakai train asli; NGBoost_ROS memakai hasil resampling. Kedua model menerima adapter yang sama. RandomOverSampler dan model revisi disimpan di models_revision, terpisah dari models_paper agar model historis tidak tertimpa.'
        )
        table('Perubahan ukuran kumpulan train karena ROS', [
            ['Ukuran', 'Sebelum', 'Sesudah'],
            ['Kelas 0', '62.104', '62.104'], ['Kelas 1', '7.967', '62.104'],
            ['Total baris', '70.071', '124.208'],
            ['Proporsi kelas 1', '11,3699%', '50,0000%'],
            ['Baris tambahan', '0', '54.137 duplikasi minoritas'],
            ['Pasien baru', '0', '0'],
        ], [62,43,59])
        paragraphs(
            'Penyeimbangan tidak menambah keragaman observasi minoritas yang sesungguhnya. Satu kunjungan dapat muncul berulang dalam kumpulan training yang telah di-resample. Karena itu, jumlah 124.208 tidak boleh disebut ukuran dataset pasien baru. Dalam evaluasi tetap digunakan 15.065 kunjungan validation dengan 1.659 positif, sehingga prior pada evaluasi tetap sekitar 11%.',
            'Bila ROS diterapkan sebelum split, salinan suatu kunjungan dapat masuk ke set yang berbeda dan mengakibatkan kebocoran. Prosedur proyek menghindari hal itu dengan memisahkan pasien terlebih dahulu. Apabila nanti dilakukan cross-validation, preprocessing, adapter dan ROS harus dibangun ulang pada masing-masing training fold; objek yang sudah di-fit pada seluruh train tidak langsung dipakai untuk menilai fold internal.'
        )
        h('Confusion matrix revisi pada ambang 0,5')
        table('Prediksi validation revisi sebelum pemilihan ambang', [
            ['Model', 'TN', 'FP', 'FN', 'TP', 'Prediksi +'],
            *[[labels[r['model']],*[count(r[k]) for k in ['tn','fp','fn','tp']],count(int(r['tp'])+int(r['fp']))]
              for r in context['revision']],
        ], [39,25,25,25,25,25])
        paragraphs(
            'NGBoost_ROS menghasilkan 5.466 prediksi positif: 869 benar dan 4.597 salah. Recall 0,5238 berarti sekitar separuh label positif terdeteksi, tetapi precision 0,1590 berarti sebagian besar prediksi positif tidak berlabel <30. Accuracy turun menjadi 0,6424, sedangkan balanced accuracy menjadi 0,5905. Perubahan ini harus dibaca sebagai pergeseran keputusan pada threshold 0,5.',
            'AP hanya naik sekitar 0,0006 dan ROC-AUC sekitar 0,0011 antara kedua NGBoost revisi. Pada saat yang sama Brier dan log loss memburuk. Pola ini konsisten dengan perubahan skala probabilitas setelah prior train diseimbangkan, tetapi percobaan ini tidak mengisolasi seluruh mekanisme penyebabnya. Tidak dilakukan koreksi prior, kalibrasi ulang, atau uji signifikansi untuk memisahkan pengaruh tersebut.'
        )
        h('Waktu komputasi yang tercatat dan batas pengukurannya')
        experiment = context['json'].loads((context['ROOT']/'results/revisi-dosen/experiment.json').read_text(encoding='utf-8'))
        table('Durasi fit dan prediksi validation pada run revisi', [
            ['Model', 'Baris training', 'Detik fit + prediksi'],
            *[[labels[name],count(info['training_rows']),f"{info['seconds_fit_and_predict']:.2f}".replace('.',',')]
              for name,info in experiment['experiments'].items()],
        ], [57,48,59])
        p('Durasi berasal dari satu run pada lingkungan lokal dan hanya mencakup blok fit model serta prediksi validation yang diukur runner. Waktu pembacaan data, fitting adapter dan resampling berada di luar blok ini. Angka tidak diperlakukan sebagai benchmark kecepatan umum, tidak mencakup pengulangan pengukuran, dan dapat berubah mengikuti perangkat maupun beban sistem.')

    elif chapter == 'Perbandingan setelah memilih ambang':
        h('Cara memilih threshold dari probabilitas validation')
        paragraphs(
            'Fungsi choose_threshold membentuk precision-recall curve dari skor validation, menghitung F1 pada kandidat threshold, lalu mengambil F1 maksimum. Jika beberapa kandidat sama dalam toleransi numerik 1e-12, dipilih threshold lebih tinggi. Pemilihan itu menggunakan label validation secara eksplisit, sehingga skor pada threshold terpilih adalah skor hasil seleksi dan bukan hasil independen.',
            'Runner revisi memakai kembali file prediksi tersimpan dan memeriksa kesesuaian target serta metrik sebelum pemilihan threshold. Model tidak di-fit ulang pada tahap ini. NGBoost tanpa ROS memperoleh threshold sekitar 0,137382, sedangkan NGBoost_ROS sekitar 0,560540. Perbedaan threshold mencerminkan skala skor kedua model yang berbeda; nilai threshold tidak dapat dibandingkan sebagai ukuran kekuatan model.'
        )
        table('Confusion matrix revisi pada threshold F1 terpilih', [
            ['Model', 'TN', 'FP', 'FN', 'TP', 'Prediksi +'],
            *[[labels[r['model']],*[count(r[k]) for k in ['tn','fp','fn','tp']],count(int(r['tp'])+int(r['fp']))]
              for r in context['tuned']],
        ], [39,25,25,25,25,25])
        h('Apa yang berubah dan apa yang tetap')
        table('Efek perubahan threshold pada validation revisi', [
            ['Model', 'Threshold', 'Recall', 'Precision', 'F1'],
            *[[labels[r['model']],dec(r['threshold']),dec(r['recall']),dec(r['precision']),dec(r['f1'])]
              for r in read('results/revisi-dosen/validation_threshold_metrics.csv') if r['model']!='Dummy_prior'],
        ], [44,30,30,30,30])
        paragraphs(
            'Setelah threshold masing-masing disesuaikan, ROS menangkap lima true positive lebih banyak tetapi menambah 46 false positive dibanding NGBoost biasa. F1 ROS sedikit lebih rendah, 0,2534 dibanding 0,2540. Keuntungan besar recall ROS pada threshold bersama 0,5 tidak otomatis menjadi keunggulan ketika kedua model diberi kesempatan memilih threshold dengan aturan sama.',
            'AP, ROC-AUC, Brier dan log loss tidak berubah pada penyesuaian ini, karena skor probabilitas tidak diubah. Threshold menentukan pemetaan skor ke label, sedangkan kalibrasi akan mengubah probabilitas itu sendiri. Laporan tidak menyebut pemilihan threshold sebagai kalibrasi dan tidak memakai threshold validation revisi untuk mengklaim hasil test yang belum dihitung.'
        )
        h('Implikasi untuk kesimpulan eksperimen')
        p('Temuan mendukung kesimpulan terbatas bahwa random oversampling belum menunjukkan peningkatan F1 yang jelas pada konfigurasi dan split ini setelah threshold dipilih. Temuan tidak membuktikan bahwa ROS selalu tidak berguna, karena belum ada pengulangan seed, variasi rasio sampling, tuning, ataupun estimasi ketidakpastian berbasis pasien. Selisih kecil juga belum dapat disebut signifikan secara statistik.')

    elif chapter == 'Pembahasan':
        h('Sintesis hasil menurut tiga rumusan masalah')
        paragraphs(
            'Untuk RQ1, karakteristik paling menentukan rancangan adalah kunjungan berulang pasien, ketidakseimbangan label, kode nominal dan missing dengan makna berbeda. Konsekuensinya, pasien dipisah antarset, ID dikeluarkan dari prediktor, kode unknown dinormalisasi, dan None lab dipertahankan. Kode meninggal memperjelas cohort. Jadi, karakteristik data tidak berhenti sebagai daftar tipe kolom, melainkan menjadi dasar keputusan pipeline.',
            'Untuk RQ2, NGBoost mengungguli Rotation Forest dalam AP dan F1 pada uji historis konfigurasi awal, sedangkan recall Rotation Forest lebih tinggi pada threshold yang dipilih. Hasil menggambarkan kompromi ranking, ketepatan dan cakupan. Tidak ada tuning setara atau uji banyak dataset, sehingga tidak disimpulkan bahwa NGBoost selalu lebih unggul untuk klasifikasi readmission.',
            'Untuk RQ3, ROS menambah recall pada threshold 0,5 tetapi juga meningkatkan false positive dan kesalahan probabilitas. Pada threshold F1 masing-masing, hasil kedua model hampir sama. Karena itu, laporan menilai oversampling dengan beberapa ukuran dan aturan threshold yang sama, bukan hanya membandingkan recall sebelum dan sesudah penyeimbangan.'
        )
        h('Validitas internal, eksternal, dan konstruk')
        table('Ancaman validitas dan dampaknya terhadap klaim', [
            ['Aspek', 'Batas pada proyek', 'Dampak'],
            ['Internal', 'Satu split, satu seed dan konfigurasi tetap.', 'Selisih kecil mungkin berubah pada pembagian atau parameter lain.'],
            ['Representasi', 'SVD digunakan untuk kedua algoritma.', 'Belum diketahui apakah perbedaan berasal dari interaksi adapter dan model.'],
            ['Seleksi', 'Threshold dipilih dan dinilai pada validation yang sama.', 'F1 validation terpilih cenderung optimistis.'],
            ['Eksternal', 'Data AS 1999-2008; tidak ada validasi rumah sakit Indonesia.', 'Hasil tidak langsung mewakili kondisi layanan sekarang/lokasi lain.'],
            ['Konstruk', 'Label <30 bersumber dari catatan dataset.', 'Negatif bukan jaminan tidak pernah readmission; tidak mengukur manfaat intervensi.'],
            ['Dependensi', 'Beberapa kunjungan per pasien.', 'Unit kunjungan tidak seluruhnya independen untuk inferensi statistik.'],
        ], [29,69,66])
        h('Interpretasi fitur, demografi, dan etika pelaporan')
        paragraphs(
            'Model memanfaatkan variabel demografi yang tersedia, tetapi belum dilakukan audit fairness menurut ras atau gender. Analisis usia dan riwayat layanan hanya menunjukkan pola kesalahan per kelompok yang dihitung. Perbedaan itu tidak cukup untuk menyatakan ketidakadilan, menjelaskan sebab klinis, ataupun membenarkan penghapusan suatu kelompok. Setiap penggunaan lanjutan memerlukan definisi tujuan dan pemeriksaan yang sesuai.',
            'Tidak dilakukan analisis koefisien asli, feature importance yang dipetakan kembali, atau SHAP. Setelah proyeksi SVD, komponen merupakan gabungan banyak indikator, sehingga menamai satu kolom sebagai faktor risiko terpenting tanpa analisis tambahan akan melampaui bukti. Laporan menampilkan contoh observasi tanpa ID untuk memperlihatkan struktur, bukan untuk mengidentifikasi individu.'
        )
        h('Rencana percobaan lanjutan yang belum dilaksanakan')
        table('Usulan tindak lanjut dan cara menjaga evaluasi', [
            ['Usulan', 'Tujuan', 'Syarat rancangan'],
            ['CV berbasis pasien', 'Memeriksa kestabilan hasil antar pembagian.', 'Fit preprocessing/ROS pada training fold; pemilihan di dalam loop.'],
            ['Ablasi adapter', 'Bandingkan tanpa SVD atau jumlah komponen lain.', 'Tetapkan ruang pencarian sebelum menilai evaluasi akhir.'],
            ['Kalibrasi probabilitas', 'Periksa dampak ROS terhadap probabilitas.', 'Gunakan data pemilihan/kalibrasi yang terpisah secara tepat.'],
            ['Rasio sampling lain', 'Periksa kompromi deteksi dan false positive.', 'Rasio dipilih pada validation internal; test tidak diseimbangkan.'],
            ['Validasi eksternal', 'Uji generalisasi ke waktu atau rumah sakit lain.', 'Perlu data baru dan definisi cohort/label yang sebanding.'],
        ], [34,61,69])
        p('Daftar di atas merupakan rencana dan tidak diberi skor hasil seolah-olah sudah dijalankan. Week 14 tetap belum dikerjakan. Jika dosen meminta percobaan tambahan, pertanyaan eksperimen dan protokol perlu ditentukan terlebih dahulu, lalu hasil baru disimpan terpisah dari hasil historis agar perkembangan proyek dapat ditelusuri.')

    elif chapter == 'Pembagian tugas dan status pekerjaan':
        h('Pemeriksaan bersama sebelum penyerahan')
        table('Hal yang perlu diperiksa kelompok pada naskah akhir', [
            ['Bagian', 'Pemeriksaan isi'],
            ['Identitas', 'Nama, NRP, kelompok, mata kuliah dan judul sesuai.'],
            ['Dataset', 'Sumber tercantum; angka asli/cohort/split diberi lingkup.'],
            ['Metode', 'Tidak menyatakan seluruh dataset untuk train; ROS hanya train.'],
            ['Hasil', 'Model awal/test historis dipisah dari validation model revisi.'],
            ['Kesimpulan', 'Tidak melebihkan selisih kecil atau mengklaim eksperimen rencana.'],
            ['Berkas', 'PDF dapat dibuka, daftar isi cocok, file tiap minggu tersedia.'],
        ], [35,129])
        p('Pemeriksaan ini menjadi panduan peninjauan oleh anggota kelompok, bukan pernyataan bahwa dosen telah menyetujui hasil atau bahwa berkas telah dikumpulkan. Laporan Week 13 menyatukan isi pekerjaan sebelumnya dalam satu alur, sedangkan PDF Week 10, Week 11 dan Week 12 tetap dipisahkan sebagai keluaran tahap masing-masing. Artikel IMRAD berada pada berkas lain dan tidak dimasukkan sebagai bab laporan pertama.')

    elif chapter == 'Pengujian dan reproduksi':
        h('Lingkungan perangkat lunak yang tercatat')
        requirements = (context['ROOT']/'requirements.txt').read_text(encoding='utf-8').splitlines()
        table('Dependensi training yang dikunci pada repository', [
            ['Paket', 'Versi'], *[line.split('==') for line in requirements if '==' in line],
        ], [90,74])
        paragraphs(
            'Metadata preprocessing mencatat Python 3.12.14 pada run sumber. Versi training dipisahkan dari dependensi penulisan laporan seperti ReportLab dan pypdf. Reproduksi angka model memerlukan data, konfigurasi, seed dan dependensi training yang cocok; mengubah library dapat mengubah detail numerik meskipun kode dan seed sama.',
            'Artefak model joblib hanya dimuat dari hasil lokal yang dibuat pipeline sendiri. Repository menyimpan kode dan ringkasan agregat; sebagian matriks dan model besar berada lokal atau dibentuk ulang. Karena itu, mengunduh repository belum tentu langsung menyediakan semua model siap prediksi. Urutan menjalankan kembali harus dimulai dari tahap yang artefaknya belum tersedia.'
        )
        h('Keterlacakan angka laporan dan sumber hasil')
        table('Sumber angka menurut lingkup analisis', [
            ['Sumber', 'Isi yang dirujuk laporan'],
            ['results/dataset/', 'Kamus 50 kolom, kode administrasi, missing, statistik numerik dan profil asli.'],
            ['results/preprocessing/', 'Cohort, split, jumlah kelas, jumlah fitur serta missing setelah cleaning.'],
            ['results/week-11/', 'Parameter dan metrik validation awal pada threshold 0,5.'],
            ['results/week-12/', 'Protokol pilihan validation; test/ memuat evaluasi historis dan kelompok kesalahan.'],
            ['results/revisi-dosen/', 'NGBoost tanpa/dengan ROS, ambang revisi dan hasil validation.'],
        ], [59,105])
        paragraphs(
            'Tabel numerik pada laporan dibentuk dari CSV/JSON tersimpan, sedangkan interpretasi ditulis dengan lingkup set dan tahap eksperimen yang jelas. Manifest sumber laporan menyimpan hash teks berkas sumber agar perubahan angka dapat ditelusuri. Hash teks dinormalisasi dari perbedaan akhir baris Windows dan Unix supaya perbedaan format akhir baris tidak dianggap perubahan isi.',
            'Pemeriksaan konsistensi mencakup penjumlahan kelas tiap set, kesesuaian total confusion matrix dengan jumlah kunjungan evaluasi, dan hubungan precision/recall/F1 dengan TP/FP/FN. Pemeriksaan dokumen mencakup tujuan tautan daftar isi, nomor halaman, tabel yang terpotong dan keterbacaan grafik. Pemeriksaan ini mendukung ketepatan laporan, tetapi tidak menggantikan validasi ilmiah pada data independen.'
        )
        h('Urutan reproduksi yang menjaga hasil historis')
        paragraphs(
            'Pertama, cocokkan CSV asli dan mapping; jalankan profil data serta preprocessing biner seed 42. Kedua, jalankan model awal untuk mendapatkan model dan prediksi validation yang konsisten. Ketiga, ikuti prosedur freeze lalu evaluate Week 12 pada direktori output baru. Keempat, jalankan revisi ROS pada folder model terpisah dan pilih ambang dari prediksi validation revisi. Terakhir, bangun PDF setelah seluruh sumber agregat cocok.',
            'Perintah yang dapat menimpa hasil lama sebaiknya diarahkan ke folder run baru sesuai opsi modul. Khusus protokol Week 12, file dibuat dengan mode eksklusif agar protokol lama tidak diam-diam ditulis ulang. Laporan ini sendiri tidak menjalankan eksperimen baru ketika diperluas; semua angka evaluasi berasal dari hasil yang sudah tersedia.'
        )

    elif chapter == 'Kesimpulan':
        h('Rekomendasi berdasarkan bukti sementara')
        paragraphs(
            'Untuk pelaporan tugas, NGBoost awal dapat dipakai sebagai model utama yang dipilih dari AP validation, dengan Rotation Forest sebagai pembanding dan baseline prior sebagai acuan minimum. Pada bagian revisi, hasil ROS harus ditampilkan bersama model tanpa ROS dan threshold masing-masing. Rekomendasi ini menyangkut penyajian eksperimen yang tersedia, bukan persetujuan penggunaan model untuk keputusan klinis.',
            'Prioritas perbaikan berikutnya adalah memeriksa kestabilan pada pembagian pasien lain dan kualitas probabilitas, kemudian menilai interaksi preprocessing serta konfigurasi model melalui protokol yang ditetapkan lebih dahulu. Tanpa evaluasi tersebut, hasil terbaik yang dapat dinyatakan adalah hasil pada satu rancangan percobaan ini. Semua langkah yang belum dilaksanakan tetap dicatat sebagai rencana, termasuk tahapan Week 14.'
        )
