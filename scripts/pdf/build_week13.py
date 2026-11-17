"""Bangun laporan pertama Week 13 dalam PDF dan Markdown dari hasil tersimpan."""
from pathlib import Path
import hashlib
from reportlab.platypus import KeepTogether
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus.tableofcontents import TableOfContents, drawPageNumbers
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderSVG

style_source = Path(__file__).with_name("build_week10.py").read_text(encoding="utf-8")
exec(compile(style_source.split("story = []")[0], "<shared-pdf-styles>", "exec"))

OUT = ROOT / "output/pdf/week-13-data-mining-kelompok-1.pdf"
DEST = ROOT / "docs/week-13"
DEST.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('TimesBody', 'C:/Windows/Fonts/times.ttf'))
pdfmetrics.registerFont(TTFont('TimesBody-Bold', 'C:/Windows/Fonts/timesbd.ttf'))
pdfmetrics.registerFontFamily('TimesBody', normal='TimesBody', bold='TimesBody-Bold')
for name in ('BodyID', 'SmallID', 'TitleID', 'HeadingID'):
    styles[name].fontName = 'TimesBody-Bold' if name in ('TitleID', 'HeadingID') else 'TimesBody'
styles['BodyID'].fontSize = 12
styles['BodyID'].leading = 18
styles['BodyID'].alignment = TA_JUSTIFY
styles['BodyID'].firstLineIndent = 10*mm
styles['BodyID'].allowWidows = 0
styles['BodyID'].allowOrphans = 0
styles['SmallID'].fontSize = 10
styles['SmallID'].leading = 13
styles['TitleID'].fontSize = 16
styles['TitleID'].leading = 21
styles['TitleID'].spaceAfter = 12
styles['TitleID'].keepWithNext = True
styles['HeadingID'].fontSize = 13
styles['HeadingID'].leading = 17
styles['HeadingID'].keepWithNext = True


def table(rows, widths, small=False):
    body = ParagraphStyle('ReportCell', parent=styles['SmallID'], fontSize=10, leading=13,
                          alignment=TA_LEFT, firstLineIndent=0, spaceAfter=0)
    head = ParagraphStyle('ReportCellHead', parent=body, fontName='TimesBody-Bold')
    data = [[Paragraph(escape(str(v)).replace('\n', '<br/>'), head if i == 0 else body)
             for v in row] for i, row in enumerate(rows)]
    result = Table(data, colWidths=[v*mm for v in widths], repeatRows=1, hAlign='LEFT', spaceAfter=10)
    result.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), .4, colors.HexColor('#b9b9b9')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return result


class ReportDoc(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ('TitleID', 'HeadingID'):
            title = flowable.getPlainText()
            key = 'section-' + hashlib.sha256(title.encode()).hexdigest()[:12]
            self.canv.bookmarkPage(key)
            level = 0 if flowable.style.name == 'TitleID' else 1
            self.notify('TOCEntry', (level, title, self.page - 1, key))


class ReportTOC(TableOfContents):
    """Compact hierarchy with continuous dot leaders in each entry's font."""

    def wrap(self, availWidth, availHeight):
        entries = self._lastEntries or [(0, 'Daftar isi', 0, None)]
        rows = []
        for index, (level, text, number, key) in enumerate(entries):
            style = self.getLevelStyle(level)
            callback = f'reportTOCEntry{index}'

            def draw_end(canvas, kind, label, style=style, number=number, key=key):
                drawPageNumbers(canvas, style, [(number, key)], availWidth, availHeight, dot='.')

            self.canv.setNamedCB(callback, draw_end)
            text = escape(text)
            if key:
                text = f'<a href="#{key}">{text}</a>'
            if style.spaceBefore:
                rows.append([Spacer(1, style.spaceBefore)])
            rows.append([Paragraph(f'{text}<onDraw name="{callback}"/>', style)])
        self._table = Table(rows, colWidths=[availWidth], style=TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        self.width, self.height = self._table.wrapOn(self.canv, availWidth, availHeight)
        return self.width, self.height


def report_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('TimesBody', 10)
    canvas.drawCentredString(A4[0]/2, 13*mm, 'i' if doc.page == 1 else str(doc.page-1))
    canvas.restoreState()


def flow_diagram():
    drawing = Drawing(464, 420)
    boxes = [
        ('Data asli', '101.766 kunjungan, 50 kolom, 71.518 pasien'),
        ('Cleaning dan cohort', '1.652 kunjungan meninggal dikeluarkan; tersisa 100.114'),
        ('Split berbasis pasien, seed 42', 'Train 70.071 | Validasi 15.065 | Test 14.978; overlap pasien 0'),
        ('Transformasi dipelajari pada train asli', 'Imputasi, one-hot 1.222 fitur, SVD 32, scaling'),
        ('Pelatihan dan pemilihan', 'Awal: baseline, NGBoost, Rotation Forest | Revisi: NGBoost dan ROS'),
    ]
    for i, (title, detail) in enumerate(boxes):
        y = 365 - i*66
        drawing.add(Rect(10, y, 444, 48, rx=5, ry=5, fillColor=colors.HexColor('#f0f2f5'), strokeColor=colors.HexColor('#666666')))
        drawing.add(String(232, y+29, title, fontName='TimesBody-Bold', fontSize=12, textAnchor='middle'))
        drawing.add(String(232, y+12, detail, fontName='TimesBody', fontSize=10, textAnchor='middle'))
        if i < 4:
            drawing.add(Line(232, y, 232, y-13, strokeColor=colors.black))
            drawing.add(Polygon([228,y-12,236,y-12,232,y-18], fillColor=colors.black))
    for x, title, detail in [(10,'Evaluasi awal Week 12','Ambang dari validasi, lalu test historis'),
                             (244,'Evaluasi revisi Week 13','ROS train saja; skor pada validasi')]:
        drawing.add(Line(232,101,x+105,78,strokeColor=colors.black))
        drawing.add(Rect(x, 19, 210, 59, rx=5, ry=5, fillColor=colors.HexColor('#fafafa'), strokeColor=colors.HexColor('#666666')))
        drawing.add(String(x+105, 54, title, fontName='TimesBody-Bold', fontSize=11, textAnchor='middle'))
        drawing.add(String(x+105, 35, detail, fontName='TimesBody', fontSize=10, textAnchor='middle'))
    renderSVG.drawToFile(drawing, str(DEST/'alur-penelitian.svg'))
    return drawing


def read_csv(relative):
    with (ROOT / relative).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def dec(value):
    return f"{float(value):.4f}".replace(".", ",")


def count(value):
    return f"{int(value):,}".replace(",", ".")


toc = ReportTOC()
toc.levelStyles = [
    ParagraphStyle('ReportTOCChapter', fontName='TimesBody-Bold', fontSize=11, leading=13,
                   leftIndent=0, firstLineIndent=0, spaceBefore=4),
    ParagraphStyle('ReportTOCSection', fontName='TimesBody', fontSize=11, leading=13,
                   leftIndent=6*mm, firstLineIndent=0, spaceBefore=0),
]
styles.add(ParagraphStyle('TOCTitle', parent=styles['TitleID'], alignment=TA_CENTER,
                          fontSize=14, leading=18, spaceAfter=14))
story = [p('DAFTAR ISI', 'TOCTitle'), toc]
markdown = ["# Laporan pertama Week 13", "", "Klasifikasi rawat inap ulang pasien diabetes", "",
    "Kelompok 1 | Data Mining | Pembaruan 17 November 2026", "",
    "| Anggota | NRP |", "|---|---|",
    "| Bambang Herlambang | 5803024019 |", "| Benedictus Erlangga | 5803024011 |",
    "| Robertus Geraldyn Alexandro Gabeler | 5803024025 |", ""]


chapter_index = 0
subsection_index = 0


def section(title):
    global chapter_index, subsection_index
    subsection_index = 0
    original = title
    if not title.startswith('Ringkasan'):
        chapter_index += 1
        title = f'{chapter_index}. {title}'
    if original in ('Ringkasan laporan pertama', 'Pendahuluan', 'Daftar pustaka'):
        page(title)
    else:
        story.append(Spacer(1, 5*mm))
        story.append(p(title, 'TitleID'))
    markdown.extend(["## " + title, ""])


def paragraph(text, small=False):
    story.append(p(text, "SmallID" if small else "BodyID"))
    markdown.extend([text, ""])


def heading(text):
    global subsection_index
    subsection_index += 1
    text = f'{chapter_index}.{subsection_index} {text}'
    story.append(p(text, "HeadingID"))
    markdown.extend(["### " + text, ""])


table_titles = [
    'Tujuan dan kriteria keberhasilan', 'Risiko dan keputusan penanganan',
    'Karakteristik dataset', 'Contoh aktual sebelum cleaning', 'Kode status meninggal',
    'Pembagian kunjungan dan pasien', 'Konfigurasi model awal', 'Validasi masukan dan pencegahan kebocoran',
    'Definisi metrik evaluasi', 'Hasil validation awal pada ambang 0,5',
    'Hasil test awal pada ambang dari validation', 'Recall test menurut riwayat rawat inap',
    'Hasil validation revisi pada ambang 0,5', 'Hasil validation revisi setelah memilih ambang',
    'Jawaban rumusan masalah', 'Pembagian tanggung jawab kelompok', 'Status keluaran tugas',
    'Bukti pemeriksaan', 'Berkas implementasi', 'Perintah reproduksi',
]
table_index = 0
styles.add(ParagraphStyle('CaptionID', parent=styles['SmallID'], keepWithNext=True, spaceBefore=5, spaceAfter=6))


def tab(rows, widths, small=True):
    global table_index
    caption = f'Tabel {table_index+1}. {table_titles[table_index]}'
    table_index += 1
    story.append(p(caption,'CaptionID'))
    markdown.extend([caption, ''])
    story.append(table(rows, widths, small=small))
    markdown.append("| " + " | ".join(rows[0]) + " |")
    markdown.append("|" + "---|" * len(rows[0]))
    markdown.extend("| " + " | ".join(str(v).replace("\n", " ").replace("|", "/") for v in row) + " |" for row in rows[1:])
    markdown.append("")


def figure(relative, caption, ratio):
    story.append(KeepTogether([Image(str(ROOT / relative), width=164*mm, height=164*mm/ratio),
                              p(caption, "SmallID")]))
    markdown.extend([f"![{caption}](../../{relative})", ""])


meta = json.loads((ROOT / "results/preprocessing/preprocessing_summary.json").read_text(encoding="utf-8"))
old_validation = read_csv("results/week-11/validation_metrics.csv")
test = [r for r in read_csv("results/week-12/test/metrics.csv") if r["policy"] == "locked"]
revision = read_csv("results/revisi-dosen/validation_metrics.csv")
tuned = [r for r in read_csv("results/revisi-dosen/validation_threshold_metrics.csv") if r["policy"] == "selected_on_validation"]
labels = {"Dummy_prior": "Baseline prior", "NGBoost": "NGBoost", "NGBoost_ROS": "NGBoost + ROS", "Rotation_Forest": "Rotation Forest"}

section("Ringkasan laporan pertama")
paragraph("Laporan pertama ini menyatukan pekerjaan Week 10 sampai Week 12 dan percobaan revisi dosen: pelengkapan karakteristik kode, NGBoost dengan random oversampling, serta penjelasan data pelatihan. Dua algoritma utama adalah NGBoost dan Rotation Forest, dengan DummyClassifier sebagai baseline. Artikel IMRAD Week 15 dan presentasi Week 16 belum menjadi keluaran laporan ini.")
paragraph("Pada uji historis Week 12, NGBoost memperoleh AP 0,2068 dan F1 0,2606. Pada percobaan revisi yang dievaluasi di validation, F1 NGBoost biasa dan NGBoost dengan oversampling hampir sama setelah masing-masing ambang dipilih: 0,2540 dan 0,2534. Hasil tersebut belum menunjukkan keunggulan yang jelas dari oversampling. Skor uji historis dan validasi revisi tidak dibandingkan sebagai eksperimen pada set yang sama.")
section("Pendahuluan")
heading("Latar belakang")
paragraph("Sasaran proyek adalah mengenali kunjungan pasien diabetes yang tercatat diikuti rawat inap ulang dalam kurang dari 30 hari. Unit observasi adalah kunjungan, bukan satu pasien. Proyek ini mempelajari klasifikasi readmission, bukan diagnosis diabetes dan bukan hubungan sebab akibat.")
paragraph("Ketidakseimbangan target membuat akurasi tinggi dapat dicapai hanya dengan memilih kelas mayoritas. Di sisi lain, satu pasien dapat muncul beberapa kali sehingga pengacakan kunjungan tanpa memperhatikan pasien berisiko menempatkan riwayat pasien yang sama pada train dan test. Penelitian ini menempatkan pemisahan pasien dan pembacaan metrik positif sebagai dasar evaluasi.")
heading("Rumusan masalah")
paragraph("RQ1: Bagaimana karakteristik dataset, makna kode administrasi, missing value, dan pengulangan pasien memengaruhi keputusan preprocessing dan pembagian data?")
paragraph("RQ2: Bagaimana perbandingan NGBoost dan Rotation Forest pada representasi dan split pasien yang sama, menurut AP, precision, recall, F1, serta kualitas probabilitas?")
paragraph("RQ3: Apakah penambahan random oversampling pada NGBoost masih memperlihatkan keuntungan setelah ambang kedua model dipilih dengan aturan F1 maksimum yang sama pada validation?")
heading("Tujuan dan batasan")
paragraph("Tujuan laporan adalah menyediakan alur yang dapat diperiksa dari sumber data sampai evaluasi, membandingkan dua konfigurasi klasifikasi, dan menjawab revisi dosen dengan bukti eksperimen. Pembahasan terbatas pada target biner <30, satu pembagian pasien, informasi saat keluar rumah sakit, serta data historis AS. Tidak dilakukan penerapan pada layanan rumah sakit atau pengujian efektivitas intervensi.")
paragraph("Revisi yang sudah dilaksanakan meliputi kamus kode yang lebih lengkap, percobaan NGBoost + ROS, dan penjelasan penggunaan seluruh kumpulan train. Revisi tersebut tetap merupakan bagian laporan Week 13; bukan keluaran Week 14.")

section("Business objective dan tujuan data mining")
paragraph("Bagian BOD menghubungkan masalah pemantauan readmission dengan sasaran teknis klasifikasi. Calon pembaca hasil adalah pihak akademik yang mempelajari pemilahan risiko kunjungan. Pengelola layanan dapat menjadi pemangku kepentingan konseptual, tetapi laporan ini belum menetapkan kebijakan klinis, biaya kesalahan, atau target operasional rumah sakit.")
heading("Tujuan dan kriteria keberhasilan")
tab([["Komponen", "Rumusan"],
     ["Pertanyaan", "Apakah kunjungan pasien akan diikuti rawat inap ulang tercatat kurang dari 30 hari?"],
     ["Tujuan", "Membandingkan dua algoritma dengan target, split pasien, dan preprocessing yang sama."],
     ["Waktu prediksi", "Saat pasien keluar rumah sakit; informasi selama kunjungan dapat dipakai."],
     ["Manfaat akademik", "Memahami pola readmission dan hubungan precision, recall, threshold serta imbalance."],
     ["Kriteria awal", "Pipeline tanpa overlap pasien dan AP model di atas baseline pada validation."],
], [35, 129])
paragraph("Kriteria keberhasilan dibatasi pada bukti akademik yang dapat diperiksa: tidak ada overlap pasien, proses dapat diulang, hasil dibedakan menurut set evaluasi, dan model nontrivial memiliki AP validation di atas baseline. Tidak ditetapkan target penurunan readmission, penghematan biaya, atau manfaat klinis karena data eksperimen belum mengukur hasil tersebut.")
heading("Situasi, risiko, dan penanganan")
tab([["Risiko atau kendala", "Keputusan penanganan"],
     ["Kelas positif sedikit", "Periksa AP, precision, recall dan F1; bandingkan dengan prior. ROS hanya untuk train."],
     ["Pasien muncul berulang", "GroupShuffleSplit berdasarkan patient_nbr; overlap pasien antarset harus nol."],
     ["Missing dan kategori nominal", "Seleksi/imputasi dipelajari di train; kode administrasi tidak diperlakukan sebagai besaran."],
     ["Dimensi one-hot besar", "Adapter SVD 32 komponen bersama; hasil dibatasi pada representasi ini."],
     ["Pemilihan model dari test", "Gunakan validasi untuk model/ambang; protokol awal dicatat sebelum evaluasi uji."],
     ["Perubahan tahap eksperimen", "Pisahkan model awal dan revisi; jangan memberi skor test lama kepada model revisi."],
], [49,115])
paragraph("Sumber daya yang dibuktikan adalah dataset lokal, implementasi Python, library yang dipin versinya, repository Git, serta laporan agregat. Spesifikasi perangkat keras, biaya komputasi dan durasi kerja tiap anggota tidak dilaporkan karena belum dicatat secara konsisten.")

section("Dataset dan karakteristik data")
paragraph("Dataset Diabetes 130-US Hospitals for Years 1999-2008 berasal dari UCI, DOI 10.24432/C5230J, dengan lisensi CC BY 4.0. Data mencakup 130 rumah sakit dan jaringan layanan di Amerika Serikat pada 1999-2008. CSV memuat 101.766 kunjungan, 71.518 pasien, dan 50 kolom: 47 calon fitur, dua ID, serta satu target.")
tab([["Kelompok", "Karakteristik"],
     ["Delapan numerik", "Lama rawat 1-14 hari dan tujuh hitungan layanan/diagnosis. Kode administrasi dan diagnosis tetap kategorikal."],
     ["Demografi", "Kelompok usia interval 10 tahun, gender, ras, dan kelompok berat dalam pound."],
     ["Missing", "Tanda ? atau kosong; weight 96,858%, medical_specialty 49,082%, payer_code 39,557%. None pada lab berarti tes tidak dilakukan."],
     ["Target asli", "NO: 54.864; >30: 35.545; <30: 11.357 (11,160%). Target biner <30 = 1, lainnya = 0."],
     ["Pengulangan", "30.248 kunjungan di luar kunjungan pertama pasien. Tidak ada duplikasi baris persis atau ID kunjungan."],
], [34, 130])
heading("Contoh data aktual")
preview = read_csv('results/dataset/data_preview.csv')
tab([["Usia", "Gender", "Hari", "Obat", "Rawat inap terdahulu", "HbA1c", "Target"]] + [
    [r['age'],r['gender'],r['time_in_hospital'],r['num_medications'],r['number_inpatient'],r['A1Cresult'],r['readmitted']]
    for r in preview[:4]], [25,24,17,17,35,24,22])
paragraph("Empat baris tersebut diambil dari data asli sebelum cleaning. ID pasien dan kunjungan tidak ditampilkan. number_inpatient menghitung rawat inap pada tahun sebelum kunjungan, bukan jumlah rawat pada masa depan.", True)
figure('results/dataset/dataset_overview.png', 'Gambar 1. Distribusi target dan missing pada data asli', 11/4.4)
paragraph("Missing pada grafik dihitung dari ? atau kosong. Selain weight, missing medical_specialty dan payer_code cukup besar, tetapi keputusan drop tetap dihitung dari train. None pada tes laboratorium tidak dimasukkan sebagai missing. Persentase label positif setelah cohort dan per split dapat berbeda dari prevalensi data asli.")
heading("Arti kode meninggal dan kategori lain")
tab([["Kode discharge", "Arti", "Jumlah"], ["11", "Expired atau meninggal", "1.642"],
     ["19", "Meninggal di rumah; Medicaid/hospice", "8"],
     ["20", "Meninggal di fasilitas medis; Medicaid/hospice", "2"],
     ["21", "Meninggal, tempat tidak diketahui; Medicaid/hospice", "0"]], [30, 109, 25])
paragraph("Kode ini hanya berlaku pada discharge_disposition_id. Kode 20 pada admission_source_id berarti Not Mapped. Hospice 13/14 tidak otomatis menunjukkan meninggal. Status obat No/Steady/Up/Down berarti tidak diresepkan/dosis tetap/naik/turun; change Ch/No menunjukkan perubahan terapi. HbA1c dan glukosa memiliki kategori hasil serta None untuk tes tidak dilakukan. Rincian seluruh kode dan frekuensinya dipisahkan pada docs/week-10/kode-kategori.md serta lampiran PDF Week 10.", True)

section("Rancangan metode dan algoritma")
paragraph("Penelitian memakai supervised binary classification. Dua algoritma dengan mekanisme berbeda dipilih untuk perbandingan awal, lalu dilakukan ablation sederhana penambahan ROS pada NGBoost. Semua tahap yang mempelajari statistik fitur menggunakan train saja. Alur berikut membedakan jalur uji awal dari jalur validasi revisi.")
story.append(KeepTogether([flow_diagram(),p("Gambar 2. Alur penelitian dan pemisahan evaluasi awal dari evaluasi revisi", 'SmallID')]))
markdown.extend(['Gambar 2. Alur penelitian dan pemisahan evaluasi awal dari evaluasi revisi', ''])
markdown.extend(['![Alur penelitian](alur-penelitian.svg)', ''])
heading("NGBoost")
paragraph("NGBoost membangun prediksi probabilistik melalui natural gradient boosting (Duan dkk., 2020). Implementasi tugas memakai NGBClassifier dengan distribusi Bernoulli untuk label 0/1 dan decision tree sebagai base learner. Probabilitas kelas 1 dipakai untuk ranking dan evaluasi; label prediksi diperoleh dengan menerapkan ambang keputusan. Model probabilistik tidak otomatis berarti probabilitasnya telah terkalibrasi pada data evaluasi.")
heading("Rotation Forest dan baseline")
paragraph("Rotation Forest membentuk ensemble dengan rotasi fitur melalui PCA pada kelompok fitur (Rodriguez, Kuncheva dan Alonso, 2006). Dalam proyek ini, Rotation Forest menerima representasi SVD yang sama dengan NGBoost. Baseline DummyClassifier strategy prior menghasilkan probabilitas konstan sesuai prevalensi train dan memprediksi kelas mayoritas pada ambang 0,5. Baseline menguji apakah model memberi nilai tambah terhadap prediktor sederhana.")
paragraph("Pemakaian SVD bersama mengendalikan representasi masukan, tetapi dapat memengaruhi performa kedua algoritma. Belum ada pengujian tanpa SVD. Jumlah estimator kedua model juga berbeda, sehingga hasil tidak diklaim sebagai perbandingan hasil tuning dengan anggaran komputasi setara.")

section("Implementasi preprocessing dan pembagian data")
paragraph("CSV dibaca sebagai string agar None pada lab tidak berubah menjadi missing. Cleaning mencakup normalisasi spasi dan ?, validasi ID/target/numerik, serta perubahan kode administrasi tidak diketahui dan gender invalid menjadi missing. Kunjungan meninggal dikeluarkan sebagai keputusan cohort untuk prediksi setelah keluar hidup; kunjungan terdahulu pasien tetap dipertahankan. Tersisa 100.114 kunjungan.")
tab([["Set", "Kunjungan", "Pasien", "Kelas 0", "Kelas 1"]] + [
    [name, count(info["rows"]), count(info["patients"]), count(info["class_counts"]["0"]), count(info["class_counts"]["1"])]
    for name, info in meta["splits"].items()], [32, 33, 33, 33, 33])
paragraph("Pembagian GroupShuffleSplit seed 42 memakai sekitar 70/15/15 persen pasien. Tidak ada pasien antarset yang tumpang tindih. Seluruh 70.071 kunjungan train menjadi kumpulan pelatihan; validation untuk pemilihan dan test untuk evaluasi sesudah protokol ditetapkan. NGBoost memakai minibatch_frac 0,75 sehingga setiap iterasi mengambil sampel acak 75% dari kumpulan train, tanpa membuang subset secara permanen.")
paragraph("Keputusan berbasis statistik dipelajari pada train: weight dikeluarkan karena missing lebih dari 50%; acetohexamide, examide dan citoglipton konstan. Tersisa 43 kolom fitur. Numerik diimputasi median dan diskalakan; kategori diimputasi dan di-one-hot, menghasilkan 1.222 fitur. Adapter bersama TruncatedSVD 32 komponen dan StandardScaler juga di-fit pada train saja.")
tab([["Model", "Konfigurasi"],
     ["NGBoost", "Bernoulli; 150 estimator; learning rate 0,03; minibatch 0,75; base tree depth 3; min leaf 20; seed 42."],
     ["Rotation Forest", "20 estimator; min/max group 3; remove proportion 0,5; n_jobs 2; seed 42."],
     ["Baseline prior", "DummyClassifier strategy prior; probabilitas mengikuti prevalensi train asli."],
], [35, 129])
paragraph("AP adalah metrik ranking utama, didampingi precision, recall, F1, ROC-AUC, balanced accuracy dan confusion matrix. Brier score dan log loss lebih kecil lebih baik. AP berbeda dari integrasi trapezoid PR-AUC.", True)
heading("Aturan validasi masukan dan pencegahan kebocoran")
tab([["Bagian", "Pelaksanaan"],
     ["Validasi baris", "Target hanya NO/>30/<30; ID tidak kosong; konflik encounter_id menghentikan proses."],
     ["Validasi numerik", "Hitungan harus bilangan bulat nonnegatif; time_in_hospital dalam 1-14 hari."],
     ["Penggunaan ID", "patient_nbr untuk split; encounter_id untuk audit; keduanya tidak masuk prediktor."],
     ["Fit transformer", "Seleksi kolom, median, encoder, scaling dan SVD dipelajari di train asli."],
     ["Kategori baru", "Encoder menangani kategori yang tidak dikenal tanpa fit ulang pada validasi/test."],
     ["Oversampling", "Diterapkan setelah transformasi train; tidak menyeimbangkan validasi/test."],
], [40,124])
paragraph("Data uji memuat pasien yang tidak berada di train atau validation. Namun, split ini tidak menjamin urutan waktu, pemisahan rumah sakit, atau independensi setiap kunjungan dalam pasien yang sama. Hasil menilai pasien berbeda pada cohort yang ditentukan, bukan prediksi tahun mendatang.")

section("Implementasi mining dan rancangan evaluasi")
paragraph("Modul src/mining.py membaca train dan validation untuk eksperimen awal. Adapter dan model disimpan lokal pada models_paper; hasil agregat memuat parameter, versi library, metrik serta prediksi validasi. Tidak ada fit menggunakan test pada tahap tersebut. Parameter model awal ditentukan sebelum melihat skor validasi dan belum merupakan hasil pencarian hiperparameter.")
paragraph("Modul src/week12.py memisahkan freeze dan evaluate. Tahap freeze memilih ambang F1 pada validasi, mempertahankan baseline 0,5, memilih model utama dari AP validasi, serta mencatat hash input dan model. Tahap evaluate memeriksa kesesuaian artefak sebelum memprediksi test. Protokol awal tersimpan pada results/week-12/protocol.json.")
tab([["Ukuran", "Definisi atau kegunaan"],
     ["Precision", "TP/(TP+FP): proporsi prediksi positif yang benar."],
     ["Recall", "TP/(TP+FN): proporsi kasus positif yang berhasil ditemukan."],
     ["F1 positif", "2 x precision x recall / (precision+recall); kompromi keduanya."],
     ["Average precision", "Ringkasan precision dengan bobot peningkatan recall; tidak memerlukan satu threshold."],
     ["ROC-AUC", "Ranking positif terhadap negatif pada rentang ambang."],
     ["Brier dan log loss", "Kesalahan probabilitas; nilai lebih rendah lebih baik."],
     ["Confusion matrix", "TN, FP, FN, TP menunjukkan jumlah kunjungan pada setiap jenis keputusan."],
], [40,124])
paragraph("Unit hitung metrik adalah kunjungan. Pemilihan ambang mengubah label prediksi dan F1, tetapi tidak mengubah AP, ROC-AUC, Brier atau log loss dari probabilitas yang sama. Analisis per kelompok memakai ambang model yang sama, tanpa memilih ambang berbeda dari skor kelompok test.")

section("Hasil Week 11 dan Week 12")
heading("Week 11 pada validation dengan ambang 0,5")
tab([["Model", "AP", "Precision", "Recall", "F1"]] + [
    [labels[r["model"]], *[dec(r[k]) for k in ["average_precision", "precision", "recall", "f1"]]] for r in old_validation], [40, 31, 31, 31, 31])
paragraph("Baseline menghasilkan akurasi tinggi karena kelas 0 dominan. NGBoost memiliki AP tertinggi tetapi belum memprediksi positif pada ambang 0,5. Rotation Forest menangkap 34 dari 1.659 kasus positif. Akurasi dan threshold 0,5 saja belum cukup menilai model.")
heading("Week 12 pada set uji historis")
paragraph("Model Week 11 dipertahankan. Ambang dipilih untuk memaksimalkan F1 pada validation, dengan ambang lebih tinggi saat seri; NGBoost dipilih berdasarkan AP validation. Protokol dan hash artefak dicatat sebelum set uji dibaca. Set uji berisi 14.978 kunjungan dari 10.566 pasien, dengan 1.731 kasus positif.")
tab([["Model", "Ambang", "AP uji", "Precision", "Recall", "F1"]] + [
    [labels[r["model"]], *[dec(r[k]) for k in ["threshold", "average_precision", "precision", "recall", "f1"]]] for r in test], [36, 26, 25, 26, 25, 26])
paragraph("NGBoost menangkap 540 kasus positif dengan 1.874 false positive; Rotation Forest menangkap 628 dengan 3.186 false positive. Recall Rotation Forest lebih tinggi, sedangkan F1 dan AP NGBoost lebih tinggi pada set uji ini. Analisis kesalahan menurut usia dan jumlah rawat inap terdahulu tersedia di hasil Week 12.")
paragraph("Hasil di atas adalah riwayat evaluasi sebelum percobaan revisi. Model revisi dilatih ulang dan disimpan terpisah; perubahan kecil AP NGBoost validation (0,1993 menjadi 0,1994) dicatat sebagai hasil run berbeda. Skor test model lama tidak dipakai sebagai skor test untuk model revisi.", True)
figure('results/week-12/test/test_confusion_matrices.png', 'Gambar 3. Confusion matrix pada test awal dengan ambang dari validation', 12/3.8)
heading("Analisis kesalahan menurut riwayat rawat inap")
groups = read_csv('results/week-12/test/error_groups.csv')
group_rows = []
for group in ('0','1','2+'):
    pair = {r['model']:r for r in groups if r['variable']=='number_inpatient' and r['group']==group}
    ng = pair['NGBoost']
    group_rows.append([group, count(ng['n']), count(ng['positives']), dec(ng['recall']), dec(pair['Rotation_Forest']['recall'])])
tab([['Rawat inap terdahulu','Kunjungan','Positif','Recall NGBoost','Recall Rotation Forest']] + group_rows, [32,29,25,37,41])
paragraph("Recall NGBoost hanya 3,28% pada kelompok tanpa riwayat rawat inap dan 85,23% pada kelompok dengan dua atau lebih rawat inap dalam tahun sebelumnya. Sebanyak 825 dari 1.191 kasus positif yang terlewat berasal dari kelompok tanpa riwayat. Hasil ini memperlihatkan bahwa metrik agregat belum menjamin deteksi yang merata antar kelompok; perbandingan tersebut deskriptif dan tidak membuktikan penyebab kesalahan.")
figure('results/week-12/test/test_pr_and_calibration.png', 'Gambar 4. Precision-recall dan diagram reliabilitas probabilitas pada test awal', 11/4.4)
paragraph("AP mengukur ranking, sedangkan diagram reliabilitas membandingkan rata-rata probabilitas dengan proporsi positif aktual dalam bin. Model tidak otomatis terkalibrasi hanya karena menghasilkan probabilitas. Brier score test awal NGBoost 0,0987 dan log loss 0,3424 lebih rendah daripada baseline 0,1022 dan 0,3580 pada set ini. Hasil tersebut tidak dipindahkan menjadi klaim kalibrasi model revisi.")

section("Revisi dosen dan oversampling")
paragraph("Percobaan tambahan membandingkan NGBoost tanpa oversampling dan NGBoost dengan RandomOverSampler (ROS). Parameter, seed, split dan adapter dibuat sama. ROS diterapkan pada train setelah adapter di-fit pada train asli; validation/test tidak di-resample. Metode ini menggandakan sampel minoritas tanpa membuat interpolasi kategori diagnosis dan obat.")
figure("results/revisi-dosen/class_balance.png", "Gambar 5. Distribusi kelas train sebelum dan sesudah random oversampling", 9/4)
paragraph("Train asli terdiri dari 62.104 kelas 0 dan 7.967 kelas 1. Sesudah ROS, masing-masing menjadi 62.104, total 124.208 baris. Tambahan 54.137 baris adalah duplikasi sampel minoritas, bukan pasien atau kunjungan baru.")
tab([["Model", "AP", "Precision", "Recall", "F1", "Brier"]] + [
    [labels[r["model"]], *[dec(r[k]) for k in ["average_precision", "precision", "recall", "f1", "brier_score"]]]
    for r in revision], [36, 25, 26, 26, 25, 26])
paragraph("Tabel memakai validation dengan ambang 0,5. ROS menangkap 869 kasus positif dan menghasilkan 4.597 false positive, sedangkan NGBoost biasa belum memprediksi positif. Namun AP hanya berubah dari 0,1994 menjadi 0,2001. Brier score memburuk dari 0,0948 menjadi 0,2255 dan log loss dari 0,3329 menjadi 0,6434. Penyeimbangan train mengubah prior dan dapat menggeser probabilitas; model belum dikalibrasi ulang.")

section("Perbandingan setelah memilih ambang")
paragraph("Untuk membandingkan kedua model dengan aturan yang sama, ambang masing-masing dipilih agar F1 kelas positif maksimum pada validation. Jika seri, dipilih ambang tertinggi. Prediksi validation yang tersimpan dipakai kembali tanpa training ulang; target dan metrik sumber diperiksa sebelum pemilihan.")
tab([["Model", "Ambang", "Precision", "Recall", "F1"]] + [
    [labels[r["model"]], *[dec(r[k]) for k in ["threshold", "precision", "recall", "f1"]]] for r in tuned], [40, 31, 31, 31, 31])
paragraph("NGBoost biasa menangkap 571 kasus positif dengan 2.266 false positive; ROS menangkap 576 dengan 2.312 false positive. Selisih F1 ROS dikurangi NGBoost biasa adalah -0,0006. Pada split ini hasilnya hampir sama, sehingga oversampling belum menunjukkan keunggulan yang jelas setelah kedua model diberi kesempatan menyesuaikan ambang.")
figure("results/revisi-dosen/validation_threshold_curves.png", "Gambar 6. Kurva precision-recall dan F1 terhadap ambang pada validation", 11/4.5)
paragraph("Perubahan ambang tidak mengubah AP, ROC-AUC, Brier score atau log loss karena probabilitasnya tetap. F1 di halaman ini dihitung pada validation yang juga dipakai memilih ambang, sehingga dapat optimistis dan bukan estimasi uji independen. Tidak dilakukan uji signifikansi; selisih kecil tidak membuktikan keunggulan umum.")

section("Pembahasan")
paragraph("Revisi dosen sudah ditindaklanjuti melalui kamus kode yang lebih rinci, percobaan NGBoost dengan oversampling train, dan penjelasan pembagian data. Seluruh bagian train tersedia untuk pembelajaran, sedangkan validation/test dipisahkan berdasarkan pasien. Dua algoritma utama dan baseline telah dijalankan; oversampling diperlakukan sebagai percobaan tambahan pada NGBoost.")
paragraph("Pada uji historis Week 12, NGBoost mempunyai AP dan F1 lebih tinggi daripada Rotation Forest pada konfigurasi yang dicoba. Pada validasi revisi, keuntungan recall ROS pada ambang 0,5 hampir hilang setelah ambang kedua model dipilih dengan aturan F1 yang sama. Karena itu, laporan tidak menyimpulkan bahwa oversampling selalu meningkatkan performa atau bahwa data seimbang menjamin model lebih baik.")
heading("Keterbatasan dan tindak lanjut")
paragraph("Hasil berasal dari satu split berbasis pasien, bukan temporal atau lintas rumah sakit. Kunjungan berulang dalam pasien yang sama membuat observasi tidak sepenuhnya independen. Data historis AS belum mewakili rumah sakit Indonesia; variabel demografi juga memerlukan pemeriksaan bias. Hospice/transfer tetap dipertahankan dan cohort hanya mengecualikan kunjungan berstatus meninggal.")
paragraph("CV berbasis pasien, tuning hiperparameter, ablasi SVD, kalibrasi probabilitas, validasi eksternal dan signifikansi statistik belum dilakukan. Test Week 12 sudah pernah dilihat pada eksperimen terdahulu, sehingga tidak dipresentasikan sebagai holdout baru untuk model revisi. Jika eksperimen dilanjutkan, preprocessing dan ROS harus di-fit ulang pada training fold saja, dengan pemilihan ambang di dalam proses pelatihan.")
heading("Jawaban rumusan masalah")
tab([['Pertanyaan','Jawaban berdasarkan hasil'],
     ['RQ1','Kode nominal, missing, kelas positif kecil dan pengulangan pasien mendasari cleaning, imputasi train saja dan split pasien.'],
     ['RQ2','Pada test awal, NGBoost lebih tinggi dalam AP/F1; Rotation Forest lebih tinggi dalam recall pada konfigurasi yang dicoba.'],
     ['RQ3','F1 validation setelah pemilihan ambang hampir sama. Penyeimbangan train belum menunjukkan keunggulan yang jelas.'],
], [27,137])

section("Pembagian tugas dan status pekerjaan")
paragraph("Pembagian berikut mengikuti rencana kolaborasi kelompok. Peran merupakan pembagian tanggung jawab, bukan bukti bahwa setiap bagian sudah ditulis atau ditinjau sendiri oleh anggota yang disebut. Pemeriksaan akhir dan keputusan penyerahan tetap menjadi tanggung jawab kelompok.")
tab([['Anggota dan NRP','Fokus tanggung jawab'],
     ['Bambang Herlambang\n5803024019','Tujuan/BOD, preprocessing, pembagian pasien, transformasi dan penjelasan pipeline.'],
     ['Benedictus Erlangga\n5803024011','Sumber/karakteristik data, baseline, evaluasi model, grafik dan analisis kesalahan.'],
     ['Robertus Geraldyn Alexandro Gabeler\n5803024025','Implementasi NGBoost/Rotation Forest, parameter dan konfigurasi eksperimen.'],
], [71,93])
paragraph("Pembahasan, kesimpulan, referensi, konsistensi angka serta peninjauan format dikerjakan bersama sesuai rencana. Laporan ini menggunakan hasil tersimpan dan tidak menambahkan eksperimen baru hanya untuk memperpanjang dokumen.")
heading("Pemenuhan ketentuan Week 10 sampai 13")
tab([["Minggu", "Keluaran dan status"],
     ["10", "Dataset, contoh, karakteristik, BOD dan algoritma; PDF tersendiri diperbarui dengan kode."],
     ["11", "Kode preprocessing/mining dan evaluasi validation; PDF tersendiri."],
     ["12", "Protokol ambang, evaluasi test historis dan analisis kesalahan; PDF tersendiri."],
     ["13", "Laporan pertama ini, merangkum pekerjaan dan revisi dosen; PDF tersendiri."],
     ["14", "Belum dikerjakan; percobaan tambahan mengikuti permintaan dosen pada tahap tersebut."],
     ["15", "Artikel IMRAD sudah disiapkan lebih awal dari hasil tersedia; terpisah dari laporan Week 13."],
     ["16", "Presentasi belum dibuat."],
], [23, 141])
paragraph("PDF pengumpulan Week 10-13 berada pada docs/laporan/ sebagai empat file terpisah. Sumber laporan dan bahan tiap minggu tetap di folder masing-masing. Status ini menunjukkan ketersediaan berkas; pengumpulan ke LMS dan persetujuan dosen belum diverifikasi.", True)

section("Pengujian dan reproduksi")
heading("Bukti pemeriksaan")
paragraph("Suite lokal memuat 16 tes perilaku preprocessing, evaluasi, model kecil, dan revisi. Pemeriksaan meliputi pasien terpisah, preservasi kategori None, penolakan ID konflik, transformasi yang tidak belajar dari validasi, metrik biner, pemilihan threshold ketika skor seri, serta oversampling train saja. Tes sintetis tidak menggantikan eksekusi dataset penuh atau membuktikan kesimpulan ilmiah.")
tab([['Pemeriksaan','Bukti atau lingkup'],
     ['Preprocessing penuh','preprocessing_summary.json mencatat split, fitur, kualitas dan hash CSV asli.'],
     ['Test tahap awal','protocol.json dan evaluation.json mencatat pilihan ambang, input serta hasil uji.'],
     ['Revisi dosen','experiment.json mencatat kelas sebelum/sesudah ROS, parameter, seed dan metrik validation.'],
     ['Pemilihan ambang','threshold_selection.json menyimpan aturan dan hash prediksi/target sumber.'],
     ['Konsistensi laporan','Tabel dibaca dari sumber CSV; model test lama dan model revisi diberi label terpisah.'],
], [46,118])
heading("Berkas implementasi dan keluaran")
tab([['Lokasi','Isi'],
     ['src/preprocess.py','Cleaning, target, split pasien dan transformer train.'],
     ['src/profile_data.py','Kamus, frekuensi kode, contoh data dan profil dataset.'],
     ['src/mining.py','Baseline, adapter bersama, NGBoost/Rotation Forest serta evaluasi validation awal.'],
     ['src/week12.py','Freeze protokol lalu evaluasi test dengan verifikasi artefak.'],
     ['src/revision.py','Perbandingan NGBoost tanpa/dengan ROS pada validation.'],
     ['src/revision_thresholds.py','Verifikasi prediksi dan pemilihan ambang revisi tanpa training ulang.'],
], [62,102])
heading("Cara menjalankan kembali")
paragraph("Kode, dataset asli, laporan agregat dan generator PDF disimpan pada repository kelompok. Model joblib serta matriks hasil preprocessing tetap lokal dan dapat dibentuk ulang. Versi library training terkunci pada requirements.txt; dependensi PDF dipisahkan dari training.")
tab([["Tahap", "Perintah dari root repo"],
     ["Preprocessing", "python -m src.preprocess"], ["Karakteristik", "python -m src.profile_data"],
     ["Week 11", "python -m src.mining"],
     ["Week 12", "Ikuti docs/week-12/README.md dengan folder output baru; hasil lama dipertahankan."],
     ["Revisi dosen", "python -m src.revision"],
     ["Ambang revisi", "python -m src.revision_thresholds (tanpa training ulang)"],
     ["Pemeriksaan", "python -m unittest discover -s tests -v"],
     ["PDF laporan", "python scripts/pdf/build_week13.py (environment PDF)"],
], [36, 128])
paragraph("Bukti angka: results/preprocessing/preprocessing_summary.json; results/week-11/validation_metrics.csv; results/week-12/protocol.json dan test/metrics.csv; results/revisi-dosen/experiment.json, validation_metrics.csv, validation_threshold_metrics.csv serta threshold_selection.json. Hash input pemilihan ambang disimpan untuk keterlacakan.", True)
section("Kesimpulan")
paragraph("Pekerjaan Week 10-12 telah disatukan menjadi laporan pertama dengan dataset, karakteristik kode, tujuan, preprocessing, implementasi mining, serta evaluasi. Train, validation dan test dipisahkan berdasarkan pasien. Seluruh kumpulan train digunakan untuk pembelajaran, dengan mekanisme minibatch pada NGBoost; oversampling hanya diterapkan pada train revisi.")
paragraph("Pada test tahap awal, NGBoost memperoleh AP 0,2068 dan F1 0,2606, sedangkan Rotation Forest memperoleh AP 0,1573 dan F1 0,2265. Pada validation revisi, F1 maksimum NGBoost tanpa dan dengan ROS hampir sama, yaitu 0,2540 dan 0,2534. Dengan demikian, laporan tidak menyimpulkan bahwa oversampling selalu meningkatkan performa. Peningkatan recall pada ambang 0,5 perlu dibaca bersama false positive, ranking dan kualitas probabilitas.")
paragraph("Keterbatasan utama adalah satu split, evaluasi per kunjungan, representasi SVD bersama, belum adanya tuning/CV serta belum ada validasi eksternal. Hasil pemilihan ambang pada validation bukan estimasi independen. Week 14 tetap belum dikerjakan; artikel sudah disiapkan lebih awal dan tidak menggantikan kebutuhan penilaian atau persetujuan dosen.")

section("Daftar pustaka")
for text in [
    "Clore, Cios, DeShazo dan Strack (2014). Diabetes 130-US Hospitals for Years 1999-2008. UCI. DOI https://doi.org/10.24432/C5230J. Mapping administrasi: IDS_mapping.csv pada arsip dataset.",
    "Duan dkk. (2020). NGBoost Natural Gradient Boosting for Probabilistic Prediction. ICML. https://proceedings.mlr.press/v119/duan20a.html",
    "Rodriguez, Kuncheva dan Alonso (2006). Rotation Forest A New Classifier Ensemble Method. https://www.lucykuncheva.co.uk/papers/jrlkcatpami06.pdf",
    "Dokumentasi scikit-learn 1.7. Average precision dan precision-recall. https://scikit-learn.org/1.7/modules/generated/sklearn.metrics.average_precision_score.html",
    "Dokumentasi imbalanced-learn. RandomOverSampler. https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.RandomOverSampler.html",
]:
    paragraph(text, True)

assert table_index == len(table_titles)
doc = ReportDoc(str(OUT), pagesize=A4, rightMargin=23*mm, leftMargin=23*mm,
                        topMargin=20*mm, bottomMargin=22*mm,
                        title="Laporan pertama Week 13 Data Mining Kelompok 1", author="Kelompok 1")
doc.multiBuild(story, onFirstPage=report_footer, onLaterPages=report_footer)
# Cover khusus laporan lengkap; cover laporan minggu lain tetap terpisah.
cover_buffer = BytesIO()
cover_canvas = pdfcanvas.Canvas(cover_buffer, pagesize=A4)
for y, text in [(265,'LAPORAN PERTAMA WEEK 13'),(254,'DATASET BOD METODE IMPLEMENTASI DAN EVALUASI'),
                (244,'KLASIFIKASI READMISSION PASIEN DIABETES')]:
    cover_canvas.setFont('TimesBody-Bold', 12)
    cover_canvas.drawCentredString(A4[0]/2,y*mm,text)
cover_canvas.setFont('TimesBody',12)
cover_canvas.drawCentredString(A4[0]/2,232*mm,'Mata Kuliah Data Mining')
cover_canvas.drawImage(str(ROOT/'docs/assets/logo-ukwms.png'),(A4[0]-75*mm)/2,148*mm,
                       width=75*mm,height=75*mm,preserveAspectRatio=True,mask='auto')
cover_canvas.drawCentredString(A4[0]/2,137*mm,'Dosen pengampu')
cover_canvas.drawCentredString(A4[0]/2,130*mm,'Ir. Devi Dwi Purwanto, S.Kom., M.Kom., CQAI., IPM.')
cover_canvas.setFont('TimesBody-Bold',12)
cover_canvas.drawCentredString(A4[0]/2,116*mm,'Disusun oleh Kelompok 1')
cover_canvas.setFont('TimesBody',12)
for i,(name,nrp) in enumerate([('Bambang Herlambang','5803024019'),('Benedictus Erlangga','5803024011'),
                              ('Robertus Geraldyn Alexandro Gabeler','5803024025')]):
    cover_canvas.drawString(33*mm,(106-i*7)*mm,name)
    cover_canvas.drawString(146*mm,(106-i*7)*mm,nrp)
cover_canvas.setFont('TimesBody-Bold',12)
for y,text in [(58,'PROGRAM STUDI INFORMATIKA'),(51,'FAKULTAS TEKNIK'),
               (44,'UNIVERSITAS KATOLIK WIDYA MANDALA SURABAYA'),(37,'2026')]:
    cover_canvas.drawCentredString(A4[0]/2,y*mm,text)
cover_canvas.save()
cover_buffer.seek(0)
final_reader = PdfReader(OUT)
writer = PdfWriter()
writer.append(PdfReader(cover_buffer))
writer.append(final_reader)
writer.add_metadata({'/Title':'Laporan pertama Week 13 Data Mining Kelompok 1','/Author':'Kelompok 1'})
with OUT.open('wb') as stream:
    writer.write(stream)
(DEST / "laporan-pertama.md").write_text("\n".join(markdown), encoding="utf-8")
reader = PdfReader(OUT)
assert all(len(page.extract_text()) > 200 for page in reader.pages)
print(f"PDF: {OUT}; pages={len(reader.pages)}")
