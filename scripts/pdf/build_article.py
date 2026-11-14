"""Render sumber Markdown artikel IMRAD tanpa training ulang."""

import csv
import hashlib
import json
import re
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph,
                               SimpleDocTemplate, Spacer, Table, TableStyle)
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
WIDTH = 164 * mm


def read_csv(relative):
    with (ROOT / relative).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def decimal(value):
    return f"{float(value):.4f}".replace(".", ",")


def integer(value):
    return f"{int(value):,}".replace(",", ".")


def check_article_tables():
    """Periksa seluruh tabel numerik artikel terhadap artefak eksperimen."""
    text = (ROOT / "docs/artikel/artikel-imrad.md").read_text(encoding="utf-8")
    tables = {}
    for match in re.finditer(r"Tabel (\d+)\.[^\n]+\n\n((?:\|[^\n]+\n)+)", text):
        rows = [[cell.strip() for cell in line.strip().strip("|").split("|")]
                for line in match[2].strip().splitlines()]
        tables[int(match[1])] = rows[2:]
    if set(tables) != set(range(1, 8)):
        raise ValueError("Artikel harus memiliki tujuh tabel bernomor.")
    meta = json.loads((ROOT / "results/preprocessing/preprocessing_summary.json").read_text(encoding="utf-8"))
    labels = {"Dummy_prior": "Baseline prior", "NGBoost": "NGBoost", "NGBoost_ROS": "NGBoost + ROS", "Rotation_Forest": "Rotation Forest"}
    expected = [[name, integer(meta["splits"][key]["rows"]), integer(meta["splits"][key]["patients"]),
                 *[integer(meta["splits"][key]["class_counts"][c]) for c in ("0", "1")]]
                for name, key in (("Latih", "train"), ("Validasi", "validation"), ("Uji", "test"))]
    if tables[1] != expected:
        raise ValueError("Tabel split artikel berbeda dari metadata.")
    sources = {
        3: ("results/week-11/validation_metrics.csv", ["average_precision", "precision", "recall", "f1"]),
        4: ("results/week-12/test/metrics.csv", ["threshold", "average_precision", "precision", "recall", "f1"]),
        5: ("results/revisi-dosen/validation_metrics.csv", ["average_precision", "precision", "recall", "f1", "brier_score", "log_loss"]),
        6: ("results/revisi-dosen/validation_threshold_metrics.csv", ["threshold", "precision", "recall", "f1"]),
    }
    for number, (path, metrics) in sources.items():
        rows = read_csv(path)
        if number == 4:
            rows = [r for r in rows if r["policy"] == "locked"]
        elif number == 5:
            rows = [r for r in rows if r["model"] != "Dummy_prior"]
        elif number == 6:
            rows = [r for r in rows if r["policy"] == "selected_on_validation"]
        expected = [[labels[r["model"]], *[decimal(r[k]) for k in metrics]] for r in rows]
        if tables[number] != expected:
            raise ValueError(f"Tabel {number} berbeda dari {path}.")
    groups = read_csv("results/week-12/test/error_groups.csv")
    expected = []
    for group in ("0", "1", "2+"):
        pairs = {r["model"]: r for r in groups if r["variable"] == "number_inpatient" and r["group"] == group}
        r = pairs["NGBoost"]
        expected.append([group, integer(r["n"]), integer(r["positives"]), decimal(r["recall"]), decimal(pairs["Rotation_Forest"]["recall"])])
    if tables[7] != expected:
        raise ValueError("Tabel kelompok kesalahan berbeda dari sumber.")
    # Konfigurasi Tabel 2 ditinjau bersama src/mining.py; tabel 1 dan 3-7 diperiksa otomatis.
    paths = ["docs/artikel/artikel-imrad.md", "src/mining.py", "src/preprocess.py", "src/revision.py",
             "src/revision_thresholds.py", "requirements.txt", "results/preprocessing/preprocessing_summary.json",
             "results/week-12/protocol.json", "results/week-12/test/error_groups.csv",
             "results/revisi-dosen/experiment.json", "results/revisi-dosen/threshold_selection.json",
             "results/revisi-dosen/class_balance.png", "results/revisi-dosen/validation_threshold_curves.png"]
    paths += [v[0] for v in sources.values()]
    hashes = {path: hashlib.sha256((ROOT / path).read_bytes() if path.endswith(".png") else
                                  (ROOT / path).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
              for path in paths}
    manifest = {"data_as_of": "2026-11-14", "experiment_base_commit": "2c2e59414a1e8496e36280821d790b02c2402f8b",
                "table_checks": "tables 1 and 3-7 match stored metadata/CSV after four-decimal formatting",
                "hash_policy": "UTF-8 text with universal newlines normalized to LF; PNG files use raw bytes",
                "test_evaluated_during_article_creation": False, "sha256": hashes}
    (ROOT / "docs/artikel/sumber-angka.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Article tables verified against source artifacts")


def render_markdown(source, destination):
    pdfmetrics.registerFont(TTFont("ArticleArial", "C:/Windows/Fonts/arial.ttf"))
    pdfmetrics.registerFont(TTFont("ArticleArialBold", "C:/Windows/Fonts/arialbd.ttf"))
    body = ParagraphStyle("ArticleBody", fontName="ArticleArial", fontSize=10.5, leading=15,
                          spaceAfter=8, textColor=colors.black, allowWidows=0, allowOrphans=0,
                          alignment=TA_JUSTIFY)
    title = ParagraphStyle("ArticleTitle", parent=body, fontName="ArticleArialBold", fontSize=17,
                           leading=22, alignment=TA_CENTER, spaceAfter=14, keepWithNext=True)
    heading = ParagraphStyle("ArticleHeading", parent=body, fontName="ArticleArialBold", fontSize=13,
                             leading=17, spaceBefore=12, spaceAfter=8, keepWithNext=True,
                             alignment=TA_LEFT)
    subheading = ParagraphStyle("ArticleSubheading", parent=heading, fontSize=11, leading=15, spaceBefore=9)
    small = ParagraphStyle("ArticleSmall", parent=body, fontSize=9, leading=12, spaceAfter=7,
                           alignment=TA_LEFT)
    caption = ParagraphStyle("ArticleCaption", parent=small, keepWithNext=True, spaceBefore=6, spaceAfter=6)
    author = ParagraphStyle("ArticleAuthor", parent=small, alignment=TA_CENTER, keepWithNext=True)
    cell = ParagraphStyle("ArticleCell", parent=small, fontSize=8.5, leading=11.5, spaceAfter=0)
    cell_head = ParagraphStyle("ArticleCellHead", parent=cell, fontName="ArticleArialBold")

    def paragraph(text, style=body):
        return Paragraph(escape(text), style)

    def make_table(lines):
        rows = [[v.strip() for v in line.strip().strip("|").split("|")] for line in lines]
        rows = [rows[0], *rows[2:]]
        n = len(rows[0])
        if n == 2:
            widths = [36, 128]
        elif n == 7:
            widths = [38, 21, 21, 21, 21, 21, 21]
        elif n == 5 and rows[0][0] == "Riwayat rawat inap":
            widths = [34, 26, 22, 39, 43]
        else:
            widths = [36] + [128/(n-1)]*(n-1)
        data = [[paragraph(v, cell_head if i == 0 else cell) for v in row] for i, row in enumerate(rows)]
        result = Table(data, colWidths=[v*mm for v in widths], repeatRows=1, hAlign="LEFT", spaceAfter=9)
        result.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#d9d9d9")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e9ed")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f8fa")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        return result

    lines = source.read_text(encoding="utf-8").splitlines()
    story, index = [], 0
    while index < len(lines):
        line = lines[index].strip()
        index += 1
        if not line:
            continue
        if line.startswith("# "):
            story.append(paragraph(line[2:], title))
        elif line.startswith("## "):
            if line == "## Daftar pustaka":
                story.append(PageBreak())
            story.append(paragraph(line[3:], heading))
        elif line.startswith("### "):
            story.append(paragraph(line[4:], subheading))
        elif line.startswith("|"):
            table_lines = [line]
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1
            story.append(make_table(table_lines))
        elif line.startswith("!["):
            match = re.fullmatch(r"!\[(.*?)\]\((.*?)\)", line)
            if not match:
                raise ValueError(f"Gambar tidak valid: {line}")
            image = Image(str((source.parent / match[2]).resolve()))
            height = WIDTH * image.imageHeight / image.imageWidth
            image.drawWidth, image.drawHeight = WIDTH, height
            story.append(KeepTogether([Spacer(1, 4), image, paragraph(match[1], small)]))
        else:
            while index < len(lines) and lines[index].strip() and not lines[index].startswith(("#", "|", "![")):
                line += " " + lines[index].strip()
                index += 1
            style = caption if line.startswith("Tabel ") else small if re.match(r"\[\d+\]", line) else body
            if line.startswith(("Bambang Herlambang", "Program Studi")):
                style = author
            if style is body and "https://" in line:
                # URL panjang pada baris sendiri mencegah celah kata besar saat justify.
                for part in re.split(r"(https?://\S+)", line):
                    if part.strip():
                        story.append(paragraph(part.strip(), small if part.startswith("http") else body))
            else:
                story.append(paragraph(line, style))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("ArticleArial", 8)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawCentredString(A4[0]/2, 13*mm, str(doc.page))
        canvas.restoreState()

    destination.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(destination), pagesize=A4, leftMargin=23*mm, rightMargin=23*mm,
                            topMargin=20*mm, bottomMargin=22*mm,
                            title=lines[0].removeprefix("# "), author="Bambang Herlambang; Benedictus Erlangga; Robertus Geraldyn Alexandro Gabeler")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    reader = PdfReader(destination)
    assert all(len(page.extract_text()) > 150 for page in reader.pages)
    print(f"PDF: {destination}; pages={len(reader.pages)}")


if __name__ == "__main__":
    check_article_tables()
    render_markdown(ROOT / "docs/artikel/artikel-imrad.md", ROOT / "output/pdf/week-15-artikel-imrad-kelompok-1.pdf")
