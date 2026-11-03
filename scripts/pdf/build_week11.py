"""PDF laporan week 11, memakai gaya visual yang sama dengan week 10."""
from pathlib import Path

# Muat hanya definisi gaya/helper, tanpa menjalankan authoring PDF week 10.
style_source = Path(__file__).with_name('build_week10.py').read_text(encoding='utf-8')
exec(compile(style_source.split('story = []')[0], '<shared-pdf-styles>', 'exec'))
from reportlab.platypus import Preformatted
pdfmetrics.registerFont(TTFont('Consolas', 'C:/Windows/Fonts/consola.ttf'))

OUT = ROOT / 'output/pdf/week-11-data-mining-kelompok-1.pdf'
pre = json.loads((ROOT/'results/preprocessing/preprocessing_summary.json').read_text(encoding='utf-8'))
exp = json.loads((ROOT/'results/week-11/experiment.json').read_text(encoding='utf-8'))
with (ROOT/'results/week-11/validation_metrics.csv').open(encoding='utf-8', newline='') as stream:
    metrics = list(csv.DictReader(stream))
assert exp['test_evaluated'] is False


def number(value):
    return f'{int(value):,}'.replace(',', '.')


def decimal(value):
    return f'{float(value):.4f}'.replace('.', ',')


def code(text):
    style = ParagraphStyle(name='Code', fontName='Consolas', fontSize=8.5, leading=11.5, textColor=NAVY,
                           backColor=PALE, borderPadding=8, spaceBefore=6, spaceAfter=12)
    return Preformatted(text, style)


def footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFont('Arial', 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(w/2, 13*mm, str(doc.page))
    canvas.restoreState()


story = []
story.append(p('01 / Tujuan dan cakupan', 'HeadingID'))
story.append(p('Menghubungkan pembacaan data, cleaning, pembagian pasien, transformasi fitur, pelatihan baseline dan dua algoritma, serta evaluasi awal. Dataset yang digunakan adalah Diabetes 130-US Hospitals for Years 1999-2008.'))
story.append(table([
    ['Komponen', 'Keputusan eksperimen'],
    ['Unit analisis', 'Satu kunjungan rawat inap; pasien yang sama dapat memiliki banyak kunjungan'],
    ['Target awal', '<30 = 1; NO dan >30 = 0. Sasaran adalah readmission dini, bukan diagnosis diabetes'],
    ['Waktu prediksi', 'Saat keluar rumah sakit, menggunakan informasi kunjungan yang sudah tersedia'],
    ['Pembagian', 'Train, validation dan test berbasis pasien, seed 42'],
    ['Model awal', 'Logistic Regression dan Random Forest; DummyClassifier sebagai baseline mayoritas'],
    ['Set evaluasi', 'Validation saja, 15.065 baris; modul mining tidak membaca X_test/y_test'],
    ['Status hasil', 'Percobaan satu split dan parameter awal; belum tuning, CV atau uji final'],
], [38, 132]))
story.append(p('Ringkasan hasil', 'HeadingID'))
story.append(p('Data asli terdiri dari 101.766 kunjungan. Setelah cleaning/cohort, 100.114 kunjungan dipertahankan. Tidak ada pasien yang tumpang tindih antarset. Transformasi menghasilkan 1.222 fitur numerik siap model.'))
story.append(p('Average precision validation: baseline 0,1101; Logistic Regression 0,2102; Random Forest 0,2014. Hasil ini merupakan pembandingan awal, bukan bukti kesiapan penggunaan klinis.'))

page('Cleaning dan keputusan cohort')
story.append(p('02 / Aturan yang diterapkan', 'HeadingID'))
story.append(table([
    ['Langkah', 'Aturan dan alasan'],
    ['Pembacaan CSV', 'dtype=str, keep_default_na=False. Trim spasi; ? dan kosong menjadi missing. None pada hasil lab dipertahankan sebagai kategori tes tidak dilakukan.'],
    ['Validasi identitas', 'ID kosong, target tidak dikenal, atau ID kunjungan berulang dengan isi berbeda menghentikan proses untuk review manual.'],
    ['Duplikasi', 'Hapus baris duplikat persis bila ditemukan; pada dataset ini jumlahnya 0.'],
    ['Cohort', 'Keluarkan kunjungan berstatus meninggal: discharge 11, 19, 20, 21 menurut IDS_mapping.csv. Ini keputusan awal proyek, bukan aturan wajib UCI.'],
    ['Nilai tidak diketahui', 'Gender Unknown/Invalid menjadi missing. Kode administrasi tidak diketahui dinormalisasi sesuai mapping.'],
    ['Fitur hitungan', 'Delapan fitur dikonversi numerik. Nilai negatif, non-integer atau time_in_hospital di luar 1-14 hari menghentikan proses.'],
    ['Prediktor', 'ID pasien/kunjungan dan target asli tidak masuk X. Diagnosis dan kode administrasi tetap kategori. Nilai ekstrem valid tidak dibuang otomatis.'],
], [36, 134], small=True))
story.append(p('Dampak cleaning aktual', 'HeadingID'))
q = pre['quality']
story.append(table([
    ['Pemeriksaan', 'Hasil'],
    ['Data asli / setelah cleaning', f"{number(q['raw_rows'])} / {number(q['clean_rows'])} baris"],
    ['Kunjungan meninggal dikeluarkan', number(q['death_discharge_rows_removed'])],
    ['Gender invalid menjadi missing', number(q['invalid_gender_to_missing'])],
    ['Kode admission type / discharge / source menjadi missing', '10.237 / 4.680 / 6.929 baris'],
    ['Pasien berbeda setelah cleaning/cohort', number(q['clean_unique_patients'])],
], [108, 62], small=True))
story.append(p('Status hospice/transfer lain tetap dipertahankan. Kunjungan terdahulu pasien yang kemudian meninggal tidak otomatis dibuang. Perubahan cohort ini perlu dicatat saat menafsirkan hasil.', 'SmallID'))

page('Split pasien dan transformasi')
story.append(p('03 / Pembagian tanpa overlap pasien', 'HeadingID'))
rows = [['Set', 'Baris', 'Pasien', 'Positif <30', 'Proporsi positif']]
for name, info in pre['splits'].items():
    rows.append([name, number(info['rows']), number(info['patients']), number(info['class_counts']['1']),
                 f"{info['class_proportions']['1']*100:.3f}%".replace('.', ',')])
story.append(table(rows, [31, 31, 31, 36, 41], small=True))
story.append(p('GroupShuffleSplit membagi sekitar 70/15/15 persen pasien, bukan jumlah baris. Split tidak stratified dan tidak temporal. Seluruh kelas tersedia pada tiap set dan overlap pasien antarset adalah 0.'))
story.append(code('first = GroupShuffleSplit(\n    n_splits=1, test_size=0.30, random_state=42)\ntrain, rest = next(first.split(\n    frame, groups=frame.patient_nbr))\nsecond = GroupShuffleSplit(\n    n_splits=1, test_size=0.50, random_state=42)\nvalidation, test = next(second.split(\n    frame.iloc[rest],\n    groups=frame.iloc[rest].patient_nbr))'))
story.append(p('04 / Fit hanya pada train', 'HeadingID'))
story.append(table([
    ['Bagian', 'Perlakuan'],
    ['Seleksi kolom', 'weight dibuang karena missing >50% train. acetohexamide, examide, citoglipton konstan pada train. Fitur tersisa: 43.'],
    ['Numerik', 'Imputasi median train, kemudian StandardScaler.'],
    ['Kategorikal', 'Imputasi __MISSING__, one-hot encoding; kategori frekuensi <10 di train digabung sebagai infrequent.'],
    ['Kategori baru', 'Masuk kelompok infrequent jika ada, atau seluruh nol jika kelompok tersebut tidak terbentuk.'],
    ['Keluaran', 'Matriks sparse 1.222 kolom. Validation/test hanya transform; tidak mempelajari statistik baru.'],
], [35, 135], small=True))

page('Mining: baseline dan dua model')
story.append(p('05 / Konfigurasi awal', 'HeadingID'))
story.append(table([
    ['Model', 'Konfigurasi'],
    ['DummyClassifier', 'strategy=most_frequent; selalu memprediksi kelas mayoritas.'],
    ['Logistic Regression', 'solver=liblinear; C=1,0; max_iter=1000; class_weight=balanced; random_state=42.'],
    ['Random Forest', 'n_estimators=150; max_depth=16; min_samples_leaf=5; max_features=sqrt; class_weight=balanced_subsample; random_state=42; n_jobs=2.'],
], [43, 127]))
story.append(p('Semua model di-fit pada 70.071 baris train dengan fitur yang sama. Parameter dan threshold 0,5 ditetapkan sebelum membaca skor validation, bukan hasil tuning. Tidak ada oversampling sebelum split.'))
story.append(p('Inti pelatihan dan prediksi', 'HeadingID'))
story.append(code('model.fit(x_train, y_train)\npositive_index = list(model.classes_).index(1)\nprobability = model.predict_proba(x_val)[:, positive_index]\nprediction = (probability >= 0.5).astype(int)\nscores = binary_metrics(y_val, probability)'))
story.append(p('Kode lengkap dan pemeriksaan', 'HeadingID'))
for text in [
    'src/mining.py memuat baseline, kedua estimator, ekspor model/prediksi dan laporan evaluasi. Source code pada PDF berupa cuplikan; modul di repo menjadi rujukan lengkap.',
    'Pelatihan Logistic Regression diperiksa terhadap ConvergenceWarning; proses dihentikan bila belum konvergen. Eksekusi yang dilaporkan selesai tanpa peringatan konvergensi.',
    'Transformasi, parameter model, seed, target dan hash data asli dicatat pada experiment.json. Model disimpan terpisah dari laporan agregat.',
    'Bobot kelas seimbang dapat mengubah trade-off precision/recall. Probabilitasnya belum dikalibrasi dan threshold ini belum merupakan threshold operasional.',
]:
    story.append(p('- ' + text))

page('Evaluasi pada validation')
story.append(p('06 / Metrik hasil eksekusi', 'HeadingID'))
metric_labels = [('accuracy','Accuracy'), ('balanced_accuracy','Balanced accuracy'), ('precision','Precision positif'),
                 ('recall','Recall positif'), ('f1','F1 positif'), ('roc_auc','ROC-AUC'), ('average_precision','Average precision (AP)')]
rows = [['Metrik', 'Baseline', 'Logistic Regression', 'Random Forest']]
for key, label in metric_labels:
    rows.append([label] + [decimal(row[key]) for row in metrics])
story.append(table(rows, [53, 32, 45, 40]))
story.append(p('Validation: 15.065 kunjungan, termasuk 1.659 positif <30 (11,012%). Precision, recall dan F1 mengacu kelas positif. AP/ROC-AUC memakai probabilitas, sedangkan metrik label memakai threshold 0,5.', 'SmallID'))
story.append(p('Interpretasi hasil', 'HeadingID'))
for text in [
    'Baseline mencapai akurasi 88,99%, tetapi recall dan F1 positif bernilai 0 karena tidak memprediksi satu pun readmission dini. Akurasi saja menyesatkan pada data ini.',
    'Logistic Regression memiliki AP tertinggi pada percobaan awal, 0,2102, dibanding baseline 0,1101. Random Forest mencapai 0,2014. Ini belum membuktikan keunggulan stabil antar-split.',
    'Random Forest memiliki F1 sedikit lebih tinggi (0,2694 vs 0,2681), sedangkan Logistic Regression memiliki recall sedikit lebih tinggi (0,5654 vs 0,5461). Urutan model bergantung pada metrik.',
    'Precision sekitar 17-18% menunjukkan banyak prediksi positif masih salah. Meningkatnya recall belum berarti model siap digunakan dalam keputusan layanan.',
    'AP merangkum precision-recall dari skor probabilitas dan bukan integrasi trapezoid PR-AUC. Skor validation ini bukan skor test atau hasil validasi eksternal.',
]:
    story.append(p('- ' + text))

page('Confusion matrix dan kesalahan')
story.append(p('07 / Kesalahan prediksi awal', 'HeadingID'))
image_path = ROOT/'results/week-11/validation_confusion_matrices.png'
story.append(Image(str(image_path), width=170*mm, height=(170*3.8/12)*mm))
story.append(p('Gambar 1. Confusion matrix validation. Baris = aktual, kolom = prediksi. Lainnya merupakan gabungan NO dan >30. Jumlah tiap matriks = 15.065.', 'SmallID'))
story.append(table([['Model', 'TN', 'FP', 'FN', 'TP']] + [[
    {'Dummy_most_frequent':'Baseline', 'Logistic_Regression':'Logistic Regression', 'Random_Forest':'Random Forest'}[row['model']],
    *[number(row[key]) for key in ['tn','fp','fn','tp']]] for row in metrics], [58,28,28,28,28], small=True))
story.append(p('Arti hasil', 'HeadingID'))
story.append(p('TN: kelas lainnya diprediksi lainnya. FP: kelas lainnya diprediksi <30. FN: kelas <30 terlewat. TP: kelas <30 dikenali dengan benar.'))
story.append(p('Logistic Regression mengenali 938 dari 1.659 kasus positif dan melewatkan 721, dengan 4.400 false positive. Random Forest mengenali 906 dan melewatkan 753, dengan 4.160 false positive.'))
story.append(p('Kedua model mengurangi kasus positif yang terlewat dibanding baseline, tetapi menghasilkan false positive yang besar. Trade-off ini perlu dianalisis lebih lanjut sebelum menetapkan threshold atau penggunaan praktis.'))
story.append(p('Analisis ini baru agregat. Week 12 dapat memeriksa pola kesalahan menurut kelompok usia, riwayat rawat inap dan kelompok lainnya, disertai ukuran sampel. Jangan menyatakan perbedaan kecil antarmodel sebagai bukti signifikansi tanpa pengujian yang sesuai.'))

page('Reproduksibilitas dan keluaran')
story.append(p('08 / Menjalankan dari root repo', 'HeadingID'))
story.append(code('python -m venv .venv\n.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt\n# Isi path ZIP sesuai lokasi unduhan\n.\\.venv\\Scripts\\python.exe -m src.preprocess --input "lokasi.zip"\n.\\.venv\\Scripts\\python.exe -m src.profile_data\n.\\.venv\\Scripts\\python.exe -m src.mining\n.\\.venv\\Scripts\\python.exe -m unittest discover -s tests -v'))
story.append(p('Setelah ekstraksi pertama, preprocessing dapat dijalankan tanpa --input. Notebook pendamping: notebooks/01_preprocessing.ipynb dan notebooks/02_week11_mining.ipynb. Pilih kernel environment proyek; CLI tidak membutuhkan Jupyter.'))
story.append(table([
    ['Lokasi / berkas', 'Kegunaan'],
    ['data/raw/', 'CSV dan mapping asli; tidak diubah oleh cleaning.'],
    ['data/processed/diabetes/', 'cleaned.csv, X/y/ID tiap set, matriks NPZ, transformer joblib, schema dan metadata.'],
    ['data/processed/diabetes/models/', 'Model joblib dan prediksi validation per baris; urutannya sama dengan y_validation dan ids_validation.'],
    ['results/preprocessing/', 'Laporan cleaning, missing dan ringkasan transformasi.'],
    ['results/week-11/', 'validation_metrics.csv, experiment.json, report.md dan grafik confusion matrix.'],
], [71,99], small=True))
story.append(p('Data dan artefak disimpan lokal serta diabaikan Git; kode, dokumentasi dan laporan agregat dapat disimpan di repo. Jangan memakai ID sebagai prediktor. Muat joblib hanya dari sumber tepercaya.', 'SmallID'))
story.append(p('Versi runtime', 'HeadingID'))
versions = pre['versions']
story.append(p('; '.join(f'{key} {value}' for key,value in versions.items()) + '; Matplotlib 3.10.7.', 'SmallID'))
story.append(p('Hash CSV asli (SHA-256):\n' + pre['raw_csv_sha256'], 'SmallID'))

page('Verifikasi dan tindak lanjut')
story.append(p('09 / Pemeriksaan yang telah lolos', 'HeadingID'))
story.append(table([
    ['Pemeriksaan', 'Hasil'],
    ['Tes perilaku preprocessing', '4 tes: target/arti None/kode unknown; ID konflik; split pasien lengkap dan reproducible; statistik transformasi tidak belajar dari validation.'],
    ['Tes metrik', '3 tes: prediksi sempurna; baseline mayoritas tetap gagal pada positif; probabilitas invalid ditolak.'],
    ['Pemeriksaan artefak', 'Matriks finite, dimensi fitur/label sejajar, pasien antarset terpisah dan isi data asli sama dengan arsip.'],
    ['Notebook dan angka', 'Dua notebook berhasil dijalankan dalam mode membaca hasil. Metrik dihitung ulang dari prediksi tersimpan dan cocok dengan laporan.'],
    ['Dependensi / sintaks', 'pip check dan compileall lolos lokal. CI diperbarui untuk tes sintetis; belum dipush atau dijalankan di GitHub untuk perubahan ini.'],
], [47,123], small=True))
story.append(p('10 / Batas hasil dan rencana week 12', 'HeadingID'))
for text in [
    'Satu split pasien, belum CV atau tuning; threshold tetap 0,5. Hasil awal bukan evaluasi final.',
    'CV harus berbasis pasien dan mempelajari seleksi kolom/imputasi/encoding ulang dari bagian latih pada setiap fold. Jangan CV dari matriks yang sudah di-fit pada seluruh train.',
    'Lanjutkan variasi parameter dan analisis kesalahan. Test tetap disimpan sampai pilihan dibekukan; tidak memilih model atau threshold berdasarkan test.',
    'Split tidak temporal dan tidak menguji rumah sakit baru. Cohort masih memuat hospice/transfer lain. Fitur demografi dipertahankan; evaluasi bias dan generalisasi eksternal belum dilakukan.',
]:
    story.append(p('- ' + text))
story.append(p('Referensi dan sumber hasil', 'HeadingID'))
for label, link in [
    ('Dataset UCI, DOI 10.24432/C5230J', 'https://doi.org/10.24432/C5230J'),
    ('Dokumentasi scikit-learn 1.7: model dan metrik', 'https://scikit-learn.org/1.7/'),
]:
    story.append(rich(f'<link href="{link}" color="#000000">{label}</link>', 'SmallID'))
story.append(p('Sumber lokal: docs/week-11/README.md, docs/preprocessing.md, results/preprocessing/preprocessing_summary.json, results/week-11/validation_metrics.csv dan experiment.json. Grafik diambil dari keluaran eksekusi aktual.', 'SmallID'))

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=20*mm,leftMargin=20*mm,
                        topMargin=18*mm,bottomMargin=24*mm,title='Week 11 - Data Mining Kelompok 1',
                        author='Kelompok 1',subject='Preprocessing, mining dan evaluasi validation awal')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
add_academic_cover(OUT, 11)
reader = PdfReader(OUT)
print(f'PDF: {OUT}; pages={len(reader.pages)}')
for i,item in enumerate(reader.pages,1):
    text = item.extract_text()
    print(f'page {i}: {len(text)} characters')
    assert len(text)>300
all_text = ''.join(item.extract_text() for item in reader.pages)
first_page = reader.pages[0].extract_text()
assert all(value in first_page for value in ['Bambang Herlambang', '5803024019', 'Benedictus Erlangga', '5803024011', 'Robertus Geraldyn Alexandro Gabeler', '5803024025'])
