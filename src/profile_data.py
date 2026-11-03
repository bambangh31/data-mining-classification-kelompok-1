"""Profil week 10: python -m src.profile_data."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.preprocess import IDS, NUMERIC, ROOT, TARGET


DESCRIPTIONS = {
    "encounter_id": "ID kunjungan; metadata, bukan prediktor",
    "patient_nbr": "ID pasien; kelompok pembagian data, bukan prediktor",
    "race": "Kategori ras yang tercatat",
    "gender": "Gender yang tercatat",
    "age": "Kelompok usia dalam interval 10 tahun",
    "weight": "Kelompok berat badan; missing sangat tinggi",
    "admission_type_id": "Kode jenis masuk; lihat IDS_mapping.csv",
    "discharge_disposition_id": "Kode status/tujuan keluar; lihat IDS_mapping.csv",
    "admission_source_id": "Kode sumber rujukan; lihat IDS_mapping.csv",
    "time_in_hospital": "Lama rawat, hari (1-14)",
    "payer_code": "Kode pembayar/asuransi",
    "medical_specialty": "Spesialisasi dokter yang menerima pasien",
    "num_lab_procedures": "Jumlah pemeriksaan laboratorium selama kunjungan",
    "num_procedures": "Jumlah prosedur selain pemeriksaan laboratorium",
    "num_medications": "Jumlah obat berbeda selama kunjungan",
    "number_outpatient": "Jumlah kunjungan rawat jalan dalam tahun sebelumnya",
    "number_emergency": "Jumlah kunjungan gawat darurat dalam tahun sebelumnya",
    "number_inpatient": "Jumlah kunjungan rawat inap dalam tahun sebelumnya",
    "diag_1": "Kode diagnosis utama (ICD-9); kategori, bukan angka kontinu",
    "diag_2": "Kode diagnosis kedua (ICD-9)",
    "diag_3": "Kode diagnosis ketiga (ICD-9)",
    "number_diagnoses": "Jumlah diagnosis yang tercatat",
    "max_glu_serum": "Kategori hasil glukosa; None berarti tidak diperiksa",
    "A1Cresult": "Kategori hasil HbA1c; None berarti tidak diperiksa",
    "change": "Apakah terdapat perubahan obat diabetes (Ch/No)",
    "diabetesMed": "Apakah obat diabetes diresepkan (Yes/No)",
    "readmitted": "Target asli: NO, >30, <30",
}


def md_table(frame):
    def safe(value):
        return str(value).replace("|", "/").replace("\n", " ")
    rows = ["| " + " | ".join(map(safe, frame.columns)) + " |",
            "|" + "---|" * len(frame.columns)]
    rows += ["| " + " | ".join(map(safe, row)) + " |" for row in frame.itertuples(index=False, name=None)]
    return "\n".join(rows)


def main():
    raw = pd.read_csv(ROOT / "data/raw/diabetic_data.csv", dtype=str, keep_default_na=False)
    clean = raw.apply(lambda col: col.str.strip()).replace({"?": np.nan, "": np.nan})
    output = ROOT / "results/dataset"
    output.mkdir(parents=True, exist_ok=True)
    docs = ROOT / "docs/week-10"
    docs.mkdir(parents=True, exist_ok=True)
    dictionary = []
    for column in raw:
        role = "ID" if column in IDS else "target" if column == TARGET else "fitur"
        desc = DESCRIPTIONS.get(column, f"Status penggunaan/perubahan dosis obat {column}: No, Steady, Up, Down (sesuai kategori yang tersedia)")
        dictionary.append({"kolom": column, "peran": role,
                           "tipe_analisis": "numerik" if column in NUMERIC else "kategorikal",
                           "deskripsi": desc, "unik_nonmissing": clean[column].nunique(),
                           "missing_jumlah": int(clean[column].isna().sum()),
                           "missing_persen": round(float(clean[column].isna().mean() * 100), 3)})
    dictionary = pd.DataFrame(dictionary)
    dictionary.to_csv(output / "data_dictionary.csv", index=False)
    (docs / "kamus-data.md").write_text("# Kamus data\n\nDihitung dari CSV asli. Missing = tanda ? atau kosong; None pada tes lab dipertahankan.\n\n" + md_table(dictionary) + "\n", encoding="utf-8")
    # Contoh aktual subset kolom; ID pasien/kunjungan sengaja tidak ditampilkan.
    preview_columns = ["age", "gender", "time_in_hospital", "num_medications", "number_inpatient", "A1Cresult", "readmitted"]
    preview = raw[preview_columns].head(6)
    preview.to_csv(output / "data_preview.csv", index=False)
    (docs / "contoh-data.md").write_text("# Contoh data aktual\n\nEnam baris pertama, hanya sebagian kolom. ID tidak ditampilkan. Ini data asli sebelum cleaning, bukan contoh sintetis.\n\n" + md_table(preview) + "\n", encoding="utf-8")
    numeric = clean[NUMERIC].apply(pd.to_numeric)
    numeric.describe().T.to_csv(output / "numeric_summary.csv", index_label="feature")
    counts = raw[TARGET].value_counts().reindex(["NO", ">30", "<30"])
    target_table = pd.DataFrame({"kelas": counts.index, "jumlah": counts.values,
                                 "persen": (counts.values / len(raw) * 100).round(3)})
    target_table.to_csv(output / "target_distribution.csv", index=False)
    missing = dictionary.loc[dictionary.missing_jumlah > 0, ["kolom", "missing_jumlah", "missing_persen"]].sort_values("missing_persen", ascending=False)
    missing.to_csv(output / "missing_summary.csv", index=False)
    summary = {"rows": len(raw), "columns": len(raw.columns), "patients": int(raw.patient_nbr.nunique()),
               "repeated_patient_rows_beyond_first": int(raw.patient_nbr.duplicated().sum()),
               "duplicate_rows": int(raw.duplicated().sum()), "duplicate_encounter_ids": int(raw.encounter_id.duplicated().sum()),
               "numeric_features": len(NUMERIC), "categorical_features": len(raw.columns) - len(NUMERIC) - 3,
               "original_target_counts": counts.to_dict(), "positive_prevalence_raw": float(raw.readmitted.eq("<30").mean()),
               "lab_none_counts": {c:int(raw[c].eq("None").sum()) for c in ["max_glu_serum", "A1Cresult"]}}
    (output / "dataset_profile.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), layout="constrained")
    bars = axes[0].bar(target_table.kelas, target_table.jumlah, color=["#547c9e", "#67a6a1", "#c86c49"])
    axes[0].bar_label(bars, labels=[f"{v:,}" for v in target_table.jumlah], padding=4)
    axes[0].set(title="Distribusi target asli", xlabel="readmitted", ylabel="Jumlah kunjungan")
    axes[0].set_ylim(0, counts.max() * 1.18)
    axes[1].barh(missing.kolom[::-1], missing.missing_persen[::-1], color="#547c9e")
    axes[1].set(title="Missing (? atau kosong)", xlabel="Persen baris", xlim=(0, 105))
    fig.savefig(output / "dataset_overview.png", dpi=160)
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
