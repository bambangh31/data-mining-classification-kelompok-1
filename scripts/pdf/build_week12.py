"""Bangun PDF Week 12 dari hasil agregat yang sudah tersimpan."""
from pathlib import Path

# Ikuti cara pemakaian gaya bersama pada generator Week 11.
style_source = Path(__file__).with_name("build_week10.py").read_text(encoding="utf-8")
exec(compile(style_source.split("story = []")[0], "<shared-pdf-styles>", "exec"))


OUT = ROOT / "output/pdf/week-12-data-mining-kelompok-1.pdf"
RESULTS = ROOT / "results/week-12"
TEST = RESULTS / "test"
protocol = json.loads((RESULTS / "protocol.json").read_text(encoding="utf-8"))
evaluation = json.loads((TEST / "evaluation.json").read_text(encoding="utf-8"))
labels = {"Dummy_prior": "Baseline prior", "NGBoost": "NGBoost", "Rotation_Forest": "Rotation Forest"}
models = list(labels)


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def integer(value):
    return f"{int(value):,}".replace(",", ".")


def decimal(value):
    return f"{float(value):.4f}".replace(".", ",")


def percent(value):
    return f"{float(value):.2%}".replace(".", ",")


def chart(filename, aspect_ratio):
    return Image(str(TEST / filename), width=165 * mm, height=165 * mm / aspect_ratio)


metrics = {(row["model"], row["policy"]): row for row in read_csv(TEST / "metrics.csv")}
locked = {name: metrics[name, "locked"] for name in models}
groups = read_csv(TEST / "error_groups.csv")
positive = evaluation["positives"]
total = evaluation["encounters"]
primary = protocol["primary_model"]
main = locked[primary]
other_name = next(name for name in models[1:] if name != primary)
other = locked[other_name]

story = []
story.append(p("01 / Protokol evaluasi", "HeadingID"))
story.append(p("Week 12 melanjutkan klasifikasi rawat inap ulang dalam waktu kurang dari 30 hari pada dataset Diabetes 130-US Hospitals for Years 1999-2008. Satu baris mewakili satu kunjungan. Pasien yang sama dapat menyumbang beberapa kunjungan di set yang sama."))
story.append(table([
    ["Bagian", "Keputusan"],
    ["Target", "<30 hari = positif. NO dan >30 = negatif."],
    ["Pelatihan", "Pakai model Week 11. Preprocessing, SVD 32 komponen, dan scaling dipelajari dari set latih."],
    ["Validasi", "Pilih ambang yang memberi F1 kelas positif tertinggi. Jika seri, gunakan ambang lebih tinggi. Baseline prior tetap 0,5."],
    ["Model utama", f"{labels[primary]} dipilih berdasarkan Average Precision (AP) tertinggi pada validasi."],
    ["Uji", f"{integer(total)} kunjungan dari {integer(evaluation['patients'])} pasien. "
     f"Ada {integer(positive)} kasus positif ({percent(positive / total)}). Pasien antarset terpisah."],
], [34, 130]))
story.append(p("02 / Ambang yang dikunci dari validasi", "HeadingID"))
rows = [["Model", "Ambang", "F1 pada 0,5", "F1 terpilih", "AP validasi"]]
for name in models:
    choice = protocol["models"][name]
    before = choice["validation_at_0_5"]
    after = choice["validation_at_locked_threshold"]
    rows.append([labels[name], decimal(choice["threshold"]), decimal(before["f1"]),
                 decimal(after["f1"]), decimal(after["average_precision"])])
story.append(table(rows, [40, 28, 32, 32, 32], small=True))
story.append(p("Protokol dan hash artefak disimpan sebelum set uji dibaca. Pencarian hanya mengubah ambang klasifikasi. Konfigurasi model Week 11 tetap digunakan.", "SmallID"))

page("Hasil pada set uji")
story.append(p("03 / Perbandingan pada ambang terkunci", "HeadingID"))
metrics_names = [
    ("accuracy", "Akurasi"), ("balanced_accuracy", "Balanced accuracy"),
    ("precision", "Precision positif"), ("recall", "Recall positif"), ("f1", "F1 positif"),
    ("average_precision", "Average Precision"), ("roc_auc", "ROC-AUC"),
    ("brier_score", "Brier score"), ("log_loss", "Log loss"),
]
story.append(table([["Metrik", *labels.values()]] + [
    [label, *[decimal(locked[name][key]) for name in models]] for key, label in metrics_names
], [50, 36, 37, 41]))
story.append(p("04 / Dampak pemilihan ambang", "HeadingID"))
story.append(table([["Model", "F1 pada 0,5", "F1 terkunci", "Recall pada 0,5", "Recall terkunci"]] + [
    [labels[name], decimal(metrics[name, "reference_0_5"]["f1"]), decimal(locked[name]["f1"]),
     percent(metrics[name, "reference_0_5"]["recall"]), percent(locked[name]["recall"])]
    for name in models[1:]
], [39, 27, 29, 34, 35], small=True))
story.append(p("Ambang mengubah keputusan kelas sehingga precision, recall dan F1 dapat berubah. AP, ROC-AUC, Brier score dan log loss dihitung dari probabilitas yang sama pada kedua ambang. Akurasi baseline yang tinggi berasal dari prediksi kelas mayoritas."))

page("Kesalahan prediksi")
story.append(p("05 / Matriks kebingungan pada set uji", "HeadingID"))
story.append(chart("test_confusion_matrices.png", 12 / 3.8))
story.append(p("Baris menunjukkan kelas aktual dan kolom menunjukkan prediksi. Positif berarti rawat inap ulang kurang dari 30 hari.", "SmallID"))
story.append(table([["Model", "TN", "FP", "FN", "TP"]] + [
    [labels[name], *[integer(locked[name][key]) for key in ("tn", "fp", "fn", "tp")]]
    for name in models
], [48, 29, 29, 29, 29]))
story.append(p(f"{labels[primary]} mendeteksi {integer(main['tp'])} dari {integer(positive)} kasus positif. "
               f"Sebanyak {integer(main['fn'])} kasus positif terlewat dan {integer(main['fp'])} prediksi positif keliru. "
               f"{labels[other_name]} mendeteksi {integer(other['tp'])} kasus positif dengan {integer(other['fp'])} prediksi positif keliru."))
story.append(p("06 / Riwayat rawat inap sebelumnya", "HeadingID"))
prior = [row for row in groups if row["variable"] == "number_inpatient"]
story.append(table([["Model", "Rawat inap", "Kunjungan", "Positif", "FP", "FN", "Recall"]] + [
    [labels[row["model"]], row["group"], *[integer(row[key]) for key in ("n", "positives", "fp", "fn")],
     percent(row["recall"]) if row["recall"] else "-"] for row in prior
], [34, 23, 23, 20, 19, 19, 26], small=True))
main_prior = {row["group"]: row for row in prior if row["model"] == primary}
story.append(p(f"Pada {labels[primary]}, recall kelompok tanpa riwayat rawat inap sebesar "
               f"{percent(main_prior['0']['recall'])} dan kelompok dua atau lebih sebesar "
               f"{percent(main_prior['2+']['recall'])}. Sebanyak {integer(main_prior['0']['fn'])} kasus "
               "positif yang terlewat berasal dari kelompok tanpa riwayat rawat inap.", "SmallID"))

page("Diskriminasi dan reliabilitas")
story.append(p("07 / Precision-recall dan kalibrasi", "HeadingID"))
story.append(chart("test_pr_and_calibration.png", 11 / 4.4))
story.append(p("Kiri: garis putus-putus menunjukkan prevalensi positif pada set uji. Kanan: garis diagonal menunjukkan kalibrasi ideal. Setiap titik merangkum kelompok probabilitas dengan lebar bin yang sama.", "SmallID"))
story.append(p(f"AP {labels[primary]} sebesar {decimal(main['average_precision'])}, sedangkan "
               f"{labels[other_name]} sebesar {decimal(other['average_precision'])} dan baseline prior "
               f"sebesar {decimal(locked['Dummy_prior']['average_precision'])}. AP merangkum kemampuan model "
               "menempatkan kasus positif pada peringkat risiko yang lebih tinggi."))
story.append(p(f"{labels[primary]} memperoleh Brier score {decimal(main['brier_score'])} dan log loss "
               f"{decimal(main['log_loss'])}. Kedua nilai lebih rendah dari baseline prior pada set uji ini. "
               "Diagram reliabilitas menunjukkan selisih antara probabilitas prediksi dan proporsi positif aktual. "
               "Jumlah kunjungan per bin tersedia di calibration.csv agar titik dengan sedikit data dapat ditafsirkan dengan hati-hati."))
story.append(p("08 / Batas interpretasi", "HeadingID"))
story.append(p("Hasil berasal dari satu pembagian berbasis pasien. Evaluasi dihitung per kunjungan. Pemisahan waktu, validasi lintas rumah sakit, dan penggunaan klinis belum diuji. Analisis berdasarkan usia dan riwayat rawat inap bersifat deskriptif."))

page("Reproduksi dan kesimpulan")
story.append(p("09 / Urutan menjalankan evaluasi", "HeadingID"))
story.append(p("Dengan model Week 11 yang sudah tersedia, jalankan perintah dari akar repo. Gunakan folder keluaran baru untuk setiap reproduksi. Jika model perlu dilatih ulang, ikuti langkah lengkap pada docs/week-12/README.md."))
story.append(table([
    ["Tahap", "Perintah"],
    ["Kunci protokol", "python -m src.week12 freeze --output tmp/week12-repro"],
    ["Evaluasi set uji", "python -m src.week12 evaluate --output tmp/week12-repro"],
    ["Jalankan tes", "python -m unittest discover -s tests -v"],
], [39, 125], small=True))
story.append(p("10 / Bukti yang disimpan", "HeadingID"))
story.append(table([
    ["Berkas di results/week-12/", "Isi"],
    ["protocol.json", "Aturan pemilihan model dan ambang dari validasi serta hash artefak."],
    ["test/metrics.csv", "Metrik pada ambang terkunci dan pembanding tetap 0,5."],
    ["test/error_groups.csv", "Ringkasan kesalahan per rentang usia dan jumlah rawat inap sebelumnya."],
    ["test/calibration.csv dan test/evaluation.json", "Statistik per bin dan metadata set uji serta hash."],
    ["test/report.md dan grafik PNG", "Ringkasan hasil, matriks kebingungan, kurva precision-recall dan reliabilitas."],
], [70, 94], small=True))
story.append(p("11 / Kesimpulan", "HeadingID"))
story.append(p(f"{labels[primary]} memperoleh AP {decimal(main['average_precision'])} dan F1 {decimal(main['f1'])} "
               f"pada set uji. {labels[other_name]} memiliki recall lebih tinggi dengan lebih banyak prediksi positif keliru. "
               "Hasil ini menjadi bahan laporan Week 13."))
story.append(rich('Sumber dataset: <link href="https://doi.org/10.24432/C5230J"><u>UCI, DOI 10.24432/C5230J</u></link>. '
                  'Sumber angka: protokol dan hasil agregat Week 12.', "SmallID"))

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm,
                        topMargin=18 * mm, bottomMargin=24 * mm,
                        title="Week 12 - Data Mining Kelompok 1", author="Kelompok 1")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
add_academic_cover(OUT, 12)
assert len(PdfReader(OUT).pages) == 6
print(OUT)
