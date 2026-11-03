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
labels = {'Dummy_prior':'Baseline prior', 'NGBoost':'NGBoost', 'Rotation_Forest':'Rotation Forest'}
by_name = {row['model']:row for row in metrics}


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
    ['Model awal', 'NGBoost dan Rotation Forest; DummyClassifier prior sebagai baseline'],
    ['Set evaluasi', 'Validation saja, 15.065 baris; modul mining tidak membaca X_test/y_test'],
    ['Status hasil', 'Percobaan satu split dan parameter awal; belum tuning, CV atau uji final'],
], [38, 132]))
story.append(p('Ringkasan hasil', 'HeadingID'))
story.append(p('Data asli terdiri dari 101.766 kunjungan. Setelah cleaning/cohort, 100.114 kunjungan dipertahankan. Pasien antarset tidak tumpang tindih. Preprocessing menghasilkan 1.222 fitur; adapter SVD menghasilkan 32 fitur kontinu untuk model.'))
story.append(p('Average precision validation: ' + '; '.join(labels[row['model']] + ' ' + decimal(row['average_precision']) for row in metrics) + '. Hasil satu split awal, bukan bukti kebaruan atau kesiapan klinis.'))

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
    ['Keluaran', 'Matriks sparse preprocessing 1.222 kolom. Adapter SVD 32 + scaling dipelajari dari train, lalu menghasilkan fitur kontinu yang sama untuk NGBoost/Rotation Forest. Validation hanya transform.'],
], [35, 135], small=True))

page('Mining: dua algoritma utama')
story.append(p('05 / Konfigurasi awal', 'HeadingID'))
story.append(table([
    ['Model', 'Konfigurasi'],
    ['Baseline prior', 'DummyClassifier(strategy=prior). Probabilitas sama dengan prevalensi train; label prediksi tetap kelas mayoritas.'],
    ['NGBoost', 'Bernoulli; 150 estimator; learning_rate=0,03; minibatch_frac=0,75; base DecisionTreeRegressor depth=3, min_samples_leaf=20; seed=42.'],
    ['Rotation Forest', '20 estimator; min_group=max_group=3; remove_proportion=0,5; n_jobs=2; seed=42.'],
], [43,127]))
story.append(p('Kedua algoritma menggunakan SVD 32 komponen dan scaling yang sama. Adapter di-fit hanya pada 70.071 baris train, bukan validation. Tidak ada pembobotan kelas atau oversampling.'))
story.append(code('adapter = make_feature_adapter(X_train, seed=42)\nx_train = adapter.transform(X_train)\nx_val = adapter.transform(X_validation)\nmodel.fit(x_train, y_train)\nprobability = model.predict_proba(x_val)[:, 1]\nscores = binary_metrics(y_val, probability)'))
story.append(p('Ruang lingkup pembandingan', 'HeadingID'))
story.append(p('SVD menyediakan masukan kontinu dan membatasi biaya komputasi. Ia dapat membuang sinyal penting; jumlah komponen dan ablasi adapter masih perlu diperiksa. Hasil LR/RF lama disimpan dalam arsip, dengan representasi serta pembobotan berbeda, sehingga bukan pembanding terkontrol.'))
story.append(p('Kebaruan penerapan NGBoost/Rotation Forest pada dataset ini belum dibuktikan. Kontribusi yang diuji adalah diskriminasi dan kalibrasi dengan protokol pasien; bukan penciptaan algoritma baru.'))

page('Evaluasi pada validation')
story.append(p('06 / Hasil eksekusi terbaru', 'HeadingID'))
metric_labels = [('accuracy','Accuracy'),('balanced_accuracy','Balanced accuracy'),('precision','Precision positif'),('recall','Recall positif'),('f1','F1 positif'),('roc_auc','ROC-AUC'),('average_precision','Average precision'),('brier_score','Brier score'),('log_loss','Log loss')]
rows = [['Metrik','Baseline prior','NGBoost','Rotation Forest']]
for key,label in metric_labels:
    rows.append([label]+[decimal(row[key]) for row in metrics])
story.append(table(rows,[53,37,40,40]))
story.append(p('Validation: 15.065 baris, 1.659 positif <30 (11,012%). Threshold 0,5 tetap; parameter belum dituning. Precision/recall/F1 mengacu kelas positif. Test belum dievaluasi.', 'SmallID'))
story.append(p('Interpretasi', 'HeadingID'))
best=max(metrics,key=lambda row:float(row['average_precision']))
story.append(p('AP tertinggi pada percobaan ini: '+labels[best['model']]+' ('+decimal(best['average_precision'])+'). AP/ROC-AUC lebih besar lebih baik; Brier score/log loss lebih kecil lebih baik. Metrik harus dibaca bersama.'))
story.append(p('Model dapat meranking risiko lebih baik daripada baseline tetapi tetap jarang memprediksi positif pada threshold 0,5. Periksa TP/FN dan jangan menyamakan akurasi mayoritas dengan deteksi readmission dini. Threshold operasional belum dipilih.'))
story.append(p('Hasil ini satu split awal, bukan hasil CV, uji final atau validasi eksternal. Model probabilistik tidak otomatis menghasilkan probabilitas terkalibrasi.'))

page('Confusion matrix validation')
story.append(p('07 / Kesalahan prediksi', 'HeadingID'))
story.append(Image(str(ROOT/'results/week-11/validation_confusion_matrices.png'),width=170*mm,height=(170*3.8/12)*mm))
story.append(p('Baris = aktual; kolom = prediksi. Lainnya adalah NO dan >30. Tiap matriks memuat 15.065 kunjungan.', 'SmallID'))
story.append(table([['Model','TN','FP','FN','TP']]+[[labels[row['model']],*[number(row[k]) for k in ['tn','fp','fn','tp']]] for row in metrics],[58,28,28,28,28],small=True))
for row in metrics[1:]:
    story.append(p(labels[row['model']]+' mengenali '+number(row['tp'])+' kasus positif dan melewatkan '+number(row['fn'])+', dengan '+number(row['fp'])+' false positive pada threshold 0,5.'))
story.append(p('Analisis lebih rinci menurut usia/riwayat rawat inap dan evaluasi trade-off threshold dapat dilanjutkan. Gunakan validation atau CV yang benar, bukan memilih threshold dari test.'))

page('Kalibrasi probabilitas')
story.append(p('08 / Reliability diagram', 'HeadingID'))
story.append(Image(str(ROOT/'results/week-11/validation_calibration.png'),width=150*mm,height=112.5*mm))
story.append(p('Sepuluh bin probabilitas sama lebar; bin kosong tidak ditampilkan. Garis diagonal menunjukkan kalibrasi ideal. Jumlah sampel setiap bin dicatat di validation_calibration.csv.', 'SmallID'))
story.append(p('Kurva menunjukkan kesesuaian rata-rata probabilitas dengan proporsi positif aktual pada validation. Bin kecil dapat tidak stabil; kurva saja bukan bukti model sudah terkalibrasi. Belum dilakukan kalibrasi pascatraining.'))
story.append(p('SVD menjelaskan '+f"{exp['feature_adapter']['explained_variance_ratio_sum']*100:.2f}"+'% variasi fitur train. Angka ini bukan persentase informasi target yang dipertahankan atau bukti kualitas model.'))

page('Reproduksibilitas dan keluaran')
story.append(p('09 / Menjalankan dari root repo', 'HeadingID'))
story.append(code('python -m venv .venv\n.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt\n# Isi path ZIP sesuai lokasi unduhan\n.\\.venv\\Scripts\\python.exe -m src.preprocess --input "lokasi.zip"\n.\\.venv\\Scripts\\python.exe -m src.profile_data\n.\\.venv\\Scripts\\python.exe -m src.mining\n.\\.venv\\Scripts\\python.exe -m unittest discover -s tests -v'))
story.append(p('Setelah ekstraksi pertama, preprocessing dapat dijalankan tanpa --input. Notebook pendamping: notebooks/01_preprocessing.ipynb dan notebooks/02_week11_mining.ipynb. Pilih kernel environment proyek; CLI tidak membutuhkan Jupyter.'))
story.append(table([
    ['Lokasi / berkas', 'Kegunaan'],
    ['data/raw/', 'CSV dan mapping asli; tidak diubah oleh cleaning.'],
    ['data/processed/diabetes/', 'cleaned.csv, X/y/ID tiap set, matriks NPZ, transformer joblib, schema dan metadata.'],
    ['data/processed/diabetes/models_paper/', 'Model joblib, feature_adapter.joblib dan prediksi validation; urutan sama dengan y_validation dan ids_validation.'],
    ['results/preprocessing/', 'Laporan cleaning, missing dan ringkasan transformasi.'],
    ['results/week-11/', 'validation_metrics.csv, experiment.json, report.md dan grafik confusion matrix.'],
], [71,99], small=True))
story.append(p('CSV asli dan mapping disertakan di repo melalui Git biasa. Matriks, transformer, model dan prediksi per baris tetap lokal pada data/processed/ dan diabaikan Git. Setelah clone, jalankan preprocessing tanpa --input. Jangan memakai ID sebagai prediktor; muat joblib hanya dari sumber tepercaya.', 'SmallID'))
story.append(p('Versi runtime', 'HeadingID'))
versions = pre['versions']
story.append(p('; '.join(f'{key} {value}' for key,value in versions.items()) + '; Matplotlib 3.10.7; ngboost 0.5.11; aeon 1.6.0.', 'SmallID'))
story.append(p('Hash CSV asli (SHA-256):\n' + pre['raw_csv_sha256'], 'SmallID'))

page('Verifikasi dan tindak lanjut')
story.append(p('10 / Pemeriksaan yang telah lolos', 'HeadingID'))
story.append(table([
    ['Pemeriksaan', 'Hasil'],
    ['Tes perilaku preprocessing', '4 tes: target/arti None/kode unknown; ID konflik; split pasien lengkap dan reproducible; statistik transformasi tidak belajar dari validation.'],
    ['Tes metrik/model', '7 tes: metrik sempurna/mayoritas, input invalid, bin kalibrasi, adapter train-only, probabilitas model baru dan alur lengkap tanpa file test. Total dengan preprocessing: 11 tes.'],
    ['Pemeriksaan artefak', 'Matriks finite, dimensi fitur/label sejajar, pasien antarset terpisah dan isi data asli sama dengan arsip.'],
    ['Notebook dan angka', 'Dua notebook berhasil dijalankan dalam mode membaca hasil. Metrik dihitung ulang dari prediksi tersimpan dan cocok dengan laporan.'],
    ['Dependensi / sintaks', 'pip check dan compileall lolos lokal. CI menguji preprocessing, metrik dan model kecil sintetis, bukan training dataset penuh. Status CI mengikuti commit di GitHub.'],
], [47,123], small=True))
story.append(p('11 / Batas hasil dan rencana week 12', 'HeadingID'))
for text in [
    'Satu split pasien, belum CV atau tuning; threshold tetap 0,5. Hasil awal bukan evaluasi final.',
    'CV harus berbasis pasien dan mempelajari seleksi kolom/imputasi/encoding ulang dari bagian latih pada setiap fold. Jangan CV dari matriks yang sudah di-fit pada seluruh train.',
    'Lanjutkan variasi parameter, ablasi adapter SVD, kalibrasi dan analisis kesalahan. Test tetap disimpan sampai pilihan dibekukan; tidak memilih model atau threshold berdasarkan test.',
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
