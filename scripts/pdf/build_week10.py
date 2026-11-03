from pathlib import Path
import csv
import json
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from pypdf import PdfReader
from pypdf import PdfWriter
from reportlab.pdfgen import canvas as pdfcanvas
from io import BytesIO

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output/pdf/week-10-data-mining-kelompok-1.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='Arial-Bold')
pdfmetrics.registerFont(TTFont('TimesCover', 'C:/Windows/Fonts/times.ttf'))
pdfmetrics.registerFont(TTFont('TimesCover-Bold', 'C:/Windows/Fonts/timesbd.ttf'))
NAVY = colors.black
TEAL = colors.black
PALE = colors.HexColor('#f2f2f2')
GRAY = colors.HexColor('#444444')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyID', fontName='Arial', fontSize=10, leading=14.4, textColor=NAVY, spaceAfter=8))
styles.add(ParagraphStyle(name='SmallID', fontName='Arial', fontSize=8.5, leading=11.5, textColor=NAVY, spaceAfter=5))
styles.add(ParagraphStyle(name='TitleID', fontName='Arial-Bold', fontSize=25, leading=30, textColor=NAVY, spaceAfter=12))
styles.add(ParagraphStyle(name='HeadingID', fontName='Arial-Bold', fontSize=15, leading=19, textColor=TEAL, spaceBefore=10, spaceAfter=9))
styles.add(ParagraphStyle(name='Kicker', fontName='Arial-Bold', fontSize=9, leading=12, textColor=TEAL, spaceAfter=9))


def p(text, style='BodyID'):
    return Paragraph(escape(str(text)).replace('\n', '<br/>'), styles[style])


def rich(text, style='BodyID'):
    return Paragraph(text, styles[style])


def table(rows, widths, small=False):
    body_style = ParagraphStyle(name='TableBody', parent=styles['SmallID' if small else 'BodyID'],
                                fontSize=8.2 if small else 10, leading=10.5 if small else 14.4, spaceAfter=0)
    header_style = ParagraphStyle(name='TableHeader', parent=body_style, textColor=colors.white, fontName='Arial-Bold')
    data = [[Paragraph(escape(str(value)).replace('\n', '<br/>'), header_style if i == 0 else body_style)
             for value in row] for i, row in enumerate(rows)]
    result = Table(data, colWidths=[value * mm for value in widths], repeatRows=1, hAlign='LEFT')
    result.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PALE]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, 0), .6, NAVY),
        ('LINEBELOW', (0, -1), (-1, -1), .5, colors.HexColor('#cccccc')),
    ]))
    return result


def csv_rows(name):
    with (ROOT / 'results/dataset' / name).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def page(title, subtitle=None):
    if story:
        story.append(PageBreak())
    story.append(p(title, 'TitleID'))
    if subtitle:
        story.append(p(subtitle))


def footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFont('Arial', 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(w/2, 13*mm, str(doc.page))
    canvas.restoreState()


def team_table():
    return table([
        ['Nama anggota', 'NRP'],
        ['Bambang Herlambang', '5803024019'],
        ['Benedictus Erlangga', '5803024011'],
        ['Robertus Geraldyn Alexandro Gabeler', '5803024025'],
    ], [120, 50], small=True)


def add_academic_cover(path, week):
    buffer = BytesIO()
    cover = pdfcanvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    cover.setFillColor(colors.black)
    cover.setFont('TimesCover-Bold', 12)
    cover.drawCentredString(width/2, 263*mm, 'DATA MINING')
    subtitle = ('WEEK 10: DATASET, KARAKTERISTIK DATA, BOD DAN ALGORITMA' if week == 10
                else 'WEEK 11: PREPROCESSING, MINING DAN EVALUASI AWAL')
    cover.drawCentredString(width/2, 248*mm, subtitle)
    cover.drawCentredString(width/2, 240*mm, 'KLASIFIKASI READMISSION PASIEN DIABETES')
    cover.drawImage(str(ROOT/'docs/assets/logo-ukwms.png'), (width-95*mm)/2,
                    137*mm, width=95*mm, height=94*mm,
                    preserveAspectRatio=True, anchor='c', mask='auto')
    cover.drawCentredString(width/2, 123*mm, 'ANGGOTA TIM')
    cover.setFont('TimesCover', 12)
    for i, (name, nrp) in enumerate([
        ('Bambang Herlambang', '5803024019'),
        ('Benedictus Erlangga', '5803024011'),
        ('Robertus Geraldyn Alexandro Gabeler', '5803024025'),
    ]):
        cover.drawString(42*mm, (114-i*6)*mm, name)
        cover.drawString(139*mm, (114-i*6)*mm, nrp)
    cover.setFont('TimesCover-Bold', 12)
    for y, text in [(68,'PROGRAM STUDI INFORMATIKA'), (59,'FAKULTAS TEKNIK'),
                    (50,'UNIVERSITAS KATOLIK WIDYA MANDALA'), (41,'SURABAYA'), (32,'2026')]:
        cover.drawCentredString(width/2, y*mm, text)
    cover.showPage()
    cover.save()
    buffer.seek(0)
    original = PdfReader(path)
    writer = PdfWriter()
    writer.add_page(PdfReader(buffer).pages[0])
    for item in original.pages:
        writer.add_page(item)
    writer.add_metadata({'/Title': f'Week {week} - Data Mining Kelompok 1', '/Author': 'Kelompok 1'})
    final = BytesIO()
    writer.write(final)
    path.write_bytes(final.getvalue())


story = []
story.append(p('01 / Dataset dan sumber', 'HeadingID'))
dataset_url = 'https://archive.ics.uci.edu/dataset/296/diabetes-130-us-hospitals-for-years-1999-2008'
story.append(rich(f'Link dataset: <link href="{dataset_url}"><u>{dataset_url}</u></link>', 'SmallID'))
story.append(p('Dataset memuat catatan kunjungan rawat inap pasien dengan diabetes dari 130 rumah sakit dan jaringan layanan di Amerika Serikat, periode 1999-2008. Sasaran klasifikasi adalah readmission, bukan diagnosis diabetes/non-diabetes.'))
story.append(table([
    ['Komponen', 'Keterangan'],
    ['Sumber', 'UCI Machine Learning Repository, dataset 296'],
    ['Pembuat / tahun', 'Clore, Cios, DeShazo, dan Strack (2014)'],
    ['DOI', '10.24432/C5230J'],
    ['Lisensi', 'Creative Commons Attribution 4.0 (CC BY 4.0)'],
    ['Berkas asli', 'diabetic_data.csv dan IDS_mapping.csv'],
    ['Unit observasi', 'Satu kunjungan rawat inap; satu pasien dapat muncul beberapa kali'],
    ['Jumlah aktual', '101.766 baris, 50 kolom, 71.518 pasien berbeda'],
    ['Struktur kolom', '47 fitur (8 numerik, 39 kategorikal), 2 ID, 1 target'],
], [43, 127]))

page('Contoh dan karakteristik data')
story.append(p('02 / Contoh data aktual', 'HeadingID'))
story.append(p('Enam baris pertama berikut adalah subset kolom data asli sebelum cleaning. ID pasien dan ID kunjungan tidak ditampilkan.'))
preview = csv_rows('data_preview.csv')
story.append(table([['Usia', 'Gender', 'Hari rawat', 'Jumlah obat', 'Rawat inap sebelumnya', 'HbA1c', 'Target']] + [
    [r['age'], r['gender'], r['time_in_hospital'], r['num_medications'], r['number_inpatient'], r['A1Cresult'], r['readmitted']] for r in preview], [24, 23, 22, 22, 31, 22, 26], small=True))
story.append(p('Kelompok usia berupa interval 10 tahun. number_inpatient menghitung rawat inap dalam tahun sebelumnya. None pada HbA1c menunjukkan pemeriksaan tidak dilakukan.', 'SmallID'))
story.append(p('03 / Target dan distribusi kelas', 'HeadingID'))
story.append(table([['Target asli', 'Makna label', 'Jumlah', 'Persen']] + [
    ['NO', 'Tidak tercatat readmission', '54.864', '53,912%'],
    ['>30', 'Readmission lebih dari 30 hari', '35.545', '34,928%'],
    ['<30', 'Readmission kurang dari 30 hari', '11.357', '11,160%'],
], [25, 85, 30, 30]))
story.append(p('Target biner awal: <30 menjadi 1; NO dan >30 menjadi 0. Kelas 0 bukan berarti pasien tidak pernah mengalami readmission. Batas label asli dipertahankan, tanpa menggantinya menjadi <=30 hari.'))
story.append(p('Struktur yang memengaruhi analisis', 'HeadingID'))
story.append(p('Terdapat 30.248 baris di luar kunjungan pertama setiap pasien. Tidak ditemukan duplikasi baris persis maupun duplikasi ID kunjungan. Pasien berulang tetap dipertahankan, tetapi seluruh kunjungan seorang pasien harus berada di set yang sama.'))
story.append(p('Fitur meliputi demografi, administrasi masuk/keluar, hitungan layanan, diagnosis, hasil lab dan obat. Kode diagnosis serta administrasi diperlakukan sebagai kategori, bukan angka kontinu.'))

page('Kualitas data dan implikasinya')
story.append(p('04 / Missing value dan ketidakseimbangan kelas', 'HeadingID'))
story.append(Image(str(ROOT/'results/dataset/dataset_overview.png'), width=170*mm, height=68*mm))
story.append(p('Gambar 1. Distribusi target dan missing pada data asli. Missing di grafik dihitung dari tanda ? atau string kosong; kategori None pada tes lab tidak dihitung sebagai missing.', 'SmallID'))
missing = csv_rows('missing_summary.csv')
story.append(table([['Kolom', 'Jumlah missing', 'Persen']] + [[r['kolom'], f"{int(r['missing_jumlah']):,}".replace(',', '.'), f"{float(r['missing_persen']):.3f}%".replace('.', ',')] for r in missing], [90, 40, 40], small=True))
story.append(p('Keputusan awal penanganan', 'HeadingID'))
for text in [
    'Tidak menghapus seluruh baris yang memiliki missing karena akan menghilangkan banyak data. Kolom missing >50% pada train dikeluarkan; fitur lainnya diimputasi sesuai tipe.',
    'Tanda ? dan kosong menjadi missing. Gender Unknown/Invalid (3 baris) dan kode administrasi tidak diketahui dinormalisasi menjadi missing. None pada hasil lab tetap kategori tes tidak dilakukan.',
    'Kelas <30 hanya sekitar 11,16% data asli. Akurasi saja tidak memadai; average precision, precision, recall dan F1 perlu diperiksa.',
    'ID dipakai untuk audit dan split, bukan prediktor. Statistik seleksi kolom, imputasi, scaling dan encoding dipelajari hanya dari train.',
]:
    story.append(p('- ' + text))

page('BOD: masalah dan tujuan')
story.append(p('05 / Rumusan BOD', 'HeadingID'))
story.append(p('Bagian ini memuat bahan rumusan masalah dan tujuan. Kepanjangan istilah BOD dan format akhir mengikuti penjelasan dosen.'))
story.append(table([
    ['Komponen', 'Rumusan proyek'],
    ['Masalah', 'Readmission dini ingin dikenali dari karakteristik kunjungan pasien diabetes.'],
    ['Pertanyaan', 'Apakah suatu kunjungan akan diikuti readmission yang tercatat dalam kurang dari 30 hari?'],
    ['Tujuan', 'Membangun dan membandingkan dua algoritma klasifikasi dengan preprocessing dan split yang sama.'],
    ['Target operasional', '1 untuk <30; 0 untuk NO atau >30. Unit prediksi adalah satu kunjungan.'],
    ['Waktu prediksi', 'Saat keluar rumah sakit; informasi selama kunjungan boleh digunakan.'],
    ['Manfaat', 'Memahami pola data dan trade-off deteksi readmission dini sebagai kajian akademik.'],
    ['Ruang lingkup', 'Data historis AS; pengujian generalisasi ke pasien berbeda melalui pembagian berbasis pasien.'],
    ['Evaluasi utama', 'Average precision pada validation, dibandingkan baseline mayoritas.'],
    ['Evaluasi pelengkap', 'Precision, recall, F1, ROC-AUC, balanced accuracy dan confusion matrix.'],
    ['Keberhasilan awal', 'Pipeline berjalan tanpa overlap pasien; model nontrivial melampaui AP baseline pada validation. Skor bukan bukti manfaat klinis.'],
], [39, 131]))
story.append(p('Cohort dan keterbatasan', 'HeadingID'))
story.append(p('Kunjungan dengan status keluar meninggal (kode 11, 19, 20, 21 menurut IDS_mapping.csv) dikeluarkan sebagai keputusan cohort awal, bukan aturan wajib UCI. Status hospice/transfer lain dipertahankan.'))
story.append(p('Data historis, bias representasi dan tidak adanya validasi eksternal membatasi generalisasi. Hasil tidak menunjukkan sebab-akibat atau kesiapan penggunaan klinis, dan tidak otomatis berlaku pada rumah sakit Indonesia.'))

page('Algoritma klasifikasi')
story.append(p('06 / Dua algoritma dan baseline', 'HeadingID'))
story.append(table([
    ['Algoritma', 'Alasan pemilihan', 'Konfigurasi awal'],
    ['Logistic Regression', 'Model linier probabilistik, relatif mudah dijelaskan. Menggunakan scaling numerik dan one-hot kategori.', 'solver=liblinear; C=1; max_iter=1000; class_weight=balanced; seed=42'],
    ['Random Forest', 'Ensemble pohon untuk menangkap hubungan nonlinier dan interaksi antarfitur.', '150 pohon; max_depth=16; min_samples_leaf=5; max_features=sqrt; class_weight=balanced_subsample; seed=42'],
    ['DummyClassifier', 'Baseline selalu memprediksi kelas mayoritas untuk menguji apakah model memberi nilai tambah.', 'strategy=most_frequent; bukan pengganti dua algoritma utama'],
], [35, 67, 68]))
story.append(p('Prinsip perbandingan', 'HeadingID'))
for text in [
    'Kedua model menggunakan target, cohort, train dan validation yang sama. Parameter awal ditetapkan sebelum melihat skor validation; belum merupakan hasil tuning.',
    'Threshold awal 0,5. Bobot kelas dihitung dari label train. Pembobotan kelas perlu dibaca bersama perubahan precision/recall dan tidak membuktikan probabilitas terkalibrasi.',
    'Average precision (AP) dihitung dari probabilitas dan merangkum kurva precision-recall. AP tidak sama dengan integrasi trapezoid PR-AUC.',
    'Precision, recall dan F1 mengacu kelas positif <30. Confusion matrix menunjukkan false positive dan false negative, sehingga akurasi tinggi pada kelas mayoritas tidak menutupi kegagalan mendeteksi readmission dini.',
    'Hasil eksperimen validation awal dibahas pada week 11, tidak dimasukkan sebagai hasil akhir week 10. Test tetap disimpan untuk evaluasi final.',
]:
    story.append(p('- ' + text))

page('Rencana coding dan referensi')
story.append(p('07 / Alur week 11-12', 'HeadingID'))
story.append(table([
    ['Tahap', 'Rencana pelaksanaan'],
    ['Preprocessing', 'Normalisasi missing/kode tidak diketahui, validasi tipe/ID, keputusan cohort dan pemisahan target.'],
    ['Pembagian data', 'GroupShuffleSplit, seed 42: sekitar 70% pasien train, 15% validation, 15% test. Proporsi baris dapat berbeda.'],
    ['Transformasi', 'Fit pada train saja: seleksi kolom missing/konstan, imputasi, scaling dan one-hot encoding. Validation/test hanya transform.'],
    ['Mining awal', 'Latih baseline, Logistic Regression dan Random Forest pada train dengan konfigurasi awal.'],
    ['Evaluasi awal', 'Nilai pada validation menggunakan AP dan metrik pelengkap; tidak memakai test untuk pemilihan model.'],
    ['Lanjutan week 12', 'Tuning, CV berbasis pasien dan analisis kesalahan. Setiap fold mempelajari preprocessing ulang dari bagian latihnya sendiri.'],
], [37, 133]))
story.append(p('Split ini tidak stratified dan bukan temporal. Distribusi kelas diperiksa per set; ID kunjungan tidak dianggap tanggal. Evaluasi menilai pasien berbeda, bukan prediksi tahun mendatang.', 'SmallID'))
story.append(p('08 / Referensi dan keterlacakan', 'HeadingID'))
references = [
    ('Dataset UCI - Clore dkk. (2014), DOI 10.24432/C5230J', 'https://doi.org/10.24432/C5230J'),
    ('Dokumentasi Logistic Regression, scikit-learn 1.7', 'https://scikit-learn.org/1.7/modules/generated/sklearn.linear_model.LogisticRegression.html'),
    ('Dokumentasi Random Forest, scikit-learn 1.7', 'https://scikit-learn.org/1.7/modules/generated/sklearn.ensemble.RandomForestClassifier.html'),
    ('Dokumentasi average precision, scikit-learn 1.7', 'https://scikit-learn.org/1.7/modules/generated/sklearn.metrics.average_precision_score.html'),
]
for title, link in references:
    story.append(rich(f'<link href="{link}" color="#000000">{escape(title)}</link>', 'SmallID'))
story.append(p('Sumber lokal: data/raw/diabetic_data.csv dan IDS_mapping.csv. Statistik dibuat dengan python -m src.profile_data; kode ada di src/profile_data.py. Versi library tercatat pada requirements.txt dan metadata preprocessing.', 'SmallID'))
story.append(p('SHA-256 CSV asli:\n0689e7ec031237dc63031b938805c48377748761a3b26acab621567afa24df97', 'SmallID'))
story.append(p('Lampiran berikut berisi kamus seluruh 50 kolom. Missing dihitung dari ? atau kosong pada data asli; kode tidak diketahui dan gender invalid ditangani terpisah saat preprocessing.', 'SmallID'))

dictionary = csv_rows('data_dictionary.csv')
for number, start in enumerate(range(0, len(dictionary), 13), 1):
    subset = dictionary[start:start+13]
    page(f'Lampiran: kamus data ({number}/4)', f'Kolom {start+1}-{start+len(subset)} dari 50 kolom CSV asli.')
    rows = [['Kolom / peran', 'Deskripsi dan tipe analisis', 'Unik*', 'Missing*']]
    for row in subset:
        description = row['deskripsi']
        if 'Status penggunaan/perubahan dosis obat' in description:
            description = 'Status obat: No (tidak), Steady (tetap), Up (naik), Down (turun).'
        rows.append([row['kolom'] + '\n' + row['peran'], description + '\nTipe: ' + row['tipe_analisis'], row['unik_nonmissing'], row['missing_jumlah'] + '\n' + row['missing_persen'] + '%'])
    story.append(table(rows, [45, 90, 15, 20], small=True))
    story.append(Spacer(1, 4*mm))
    story.append(p('* Unik = jumlah nilai unik nonmissing. Missing = tanda ? atau kosong. None pada hasil lab adalah kategori tes tidak dilakukan. ID disimpan sebagai metadata, bukan fitur.', 'SmallID'))

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=20*mm, leftMargin=20*mm,
                        topMargin=18*mm, bottomMargin=24*mm,
                        title='Week 10 - Data Mining Kelompok 1', author='Kelompok 1',
                        subject='Dataset, karakteristik, BOD dan algoritma klasifikasi readmission')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
add_academic_cover(OUT, 10)
reader = PdfReader(OUT)
print(f'PDF: {OUT}; pages={len(reader.pages)}')
for i, item in enumerate(reader.pages, 1):
    text = item.extract_text()
    print(f'page {i}: {len(text)} characters')
    assert len(text) > 200
first_page = reader.pages[0].extract_text()
assert all(value in first_page for value in ['Bambang Herlambang', '5803024019', 'Benedictus Erlangga', '5803024011', 'Robertus Geraldyn Alexandro Gabeler', '5803024025'])
