"""Preprocessing UCI Diabetes: python -m src.preprocess --help."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
import zipfile

import joblib
import numpy as np
import pandas as pd
import scipy
from scipy import sparse
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
TARGET = "readmitted"
IDS = ["encounter_id", "patient_nbr"]
NUMERIC = [
    "time_in_hospital", "num_lab_procedures", "num_procedures",
    "num_medications", "number_outpatient", "number_emergency",
    "number_inpatient", "number_diagnoses",
]
# Kode sesuai IDS_mapping.csv. Nilai None pada dua tes LAB bukan missing CSV.
UNKNOWN_CODES = {
    "admission_type_id": ["5", "6", "8"],
    "discharge_disposition_id": ["18", "25", "26"],
    "admission_source_id": ["9", "15", "17", "20", "21"],
}
DEATH_CODES = ["11", "19", "20", "21"]
SOURCE = "https://archive.ics.uci.edu/dataset/296/diabetes-130-us-hospitals-for-years-1999-2008"


def write_json(path: Path, value: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def load_data(source: Path, raw_dir: Path) -> tuple[pd.DataFrame, str]:
    """Salin hanya dua anggota ZIP yang dikenal, tanpa extractall/path traversal."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source) as archive:
            for name in ["diabetic_data.csv", "IDS_mapping.csv"]:
                (raw_dir / name).write_bytes(archive.read(name))
        csv_path = raw_dir / "diabetic_data.csv"
    else:
        csv_path = source
    digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    # Jangan gunakan daftar NA bawaan pandas: string "None" berarti tes tidak dilakukan.
    frame = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    return frame, digest


def clean_data(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    required = IDS + NUMERIC + list(UNKNOWN_CODES) + [TARGET, "gender"]
    if not set(required).issubset(raw.columns):
        raise ValueError(f"Kolom wajib tidak ditemukan: {sorted(set(required) - set(raw.columns))}")
    frame = raw.copy()
    for column in frame:
        frame[column] = frame[column].str.strip()
    frame = frame.replace({"?": np.nan, "": np.nan})
    if frame[IDS].isna().any().any():
        raise ValueError("ID kosong; pembagian pasien tidak dapat dipastikan.")
    duplicated = int(frame.duplicated().sum())
    frame = frame.drop_duplicates().copy()
    if frame.encounter_id.duplicated().any():
        raise ValueError("encounter_id berulang dengan isi berbeda; perlu review manual.")
    valid_target = frame[TARGET].isin(["NO", ">30", "<30"])
    if not valid_target.all():
        raise ValueError("Target hilang/tidak dikenal; perlu review manual.")
    missing_before = frame.isna().sum().to_dict()
    deaths = frame.discharge_disposition_id.isin(DEATH_CODES)
    excluded_deaths = int(deaths.sum())
    frame = frame.loc[~deaths].copy()
    invalid_gender = int(frame.gender.eq("Unknown/Invalid").sum())
    frame["gender"] = frame.gender.replace({"Unknown/Invalid": np.nan})
    unknown_counts = {}
    for column, codes in UNKNOWN_CODES.items():
        unknown_counts[column] = int(frame[column].isin(codes).sum())
        frame[column] = frame[column].replace(dict.fromkeys(codes, np.nan))
    # Kolom kode diagnosis/administrasi tetap kategorikal, meskipun berupa angka.
    for column in NUMERIC:
        converted = pd.to_numeric(frame[column], errors="coerce")
        if (frame[column].notna() & converted.isna()).any():
            raise ValueError(f"Nilai numerik tidak valid pada {column}.")
        if (converted.dropna() < 0).any():
            raise ValueError(f"Nilai negatif pada hitungan {column}.")
        if not converted.dropna().mod(1).eq(0).all():
            raise ValueError(f"Hitungan bukan bilangan bulat pada {column}.")
        frame[column] = converted
    if not frame.time_in_hospital.dropna().between(1, 14).all():
        raise ValueError("time_in_hospital di luar 1-14 hari.")
    frame = frame.reset_index(drop=True)
    return frame, {
        "raw_rows": len(raw), "raw_columns": len(raw.columns),
        "raw_unique_patients": int(raw.patient_nbr.nunique()),
        "exact_duplicates_removed": duplicated,
        "death_discharge_rows_removed": excluded_deaths,
        "invalid_gender_to_missing": invalid_gender,
        "unknown_admin_codes_to_missing": unknown_counts,
        "missing_after_question_mark_normalization": missing_before,
        "clean_rows": len(frame), "clean_unique_patients": int(frame.patient_nbr.nunique()),
        "raw_target_counts": raw[TARGET].value_counts().to_dict(),
        "clean_original_target_counts": frame[TARGET].value_counts().to_dict(),
    }


def make_target(frame: pd.DataFrame, mode: str) -> pd.Series:
    if mode == "binary":
        return frame[TARGET].eq("<30").astype("int8").rename("target")
    return frame[TARGET].map({"NO": 0, ">30": 1, "<30": 2}).astype("int8").rename("target")


def split_patients(frame: pd.DataFrame, seed: int = 42) -> dict[str, np.ndarray]:
    """70/15/15 persen pasien, bukan baris; tidak memilih seed dari skor model."""
    first = GroupShuffleSplit(n_splits=1, test_size=0.30, random_state=seed)
    train, rest = next(first.split(frame, groups=frame.patient_nbr))
    second = GroupShuffleSplit(n_splits=1, test_size=0.50, random_state=seed)
    validation, test = next(second.split(frame.iloc[rest], groups=frame.iloc[rest].patient_nbr))
    splits = {"train": train, "validation": rest[validation], "test": rest[test]}
    patient_sets = [set(frame.iloc[idx].patient_nbr) for idx in splits.values()]
    if any(patient_sets[i] & patient_sets[j] for i in range(3) for j in range(i + 1, 3)):
        raise AssertionError("Pasien bocor antarset.")
    if len(np.unique(np.concatenate(list(splits.values())))) != len(frame):
        raise AssertionError("Baris hilang atau berulang pada pembagian.")
    return splits


def build_transformer(train: pd.DataFrame, min_frequency: int = 10):
    # Semua keputusan berbasis statistik hanya dihitung dari data TRAIN.
    missing_drops = train.columns[train.isna().mean() > 0.50].tolist()
    constant_drops = [c for c in train if c not in missing_drops and train[c].nunique(dropna=False) <= 1]
    retained = [c for c in train if c not in missing_drops + constant_drops]
    numeric = [c for c in retained if c in NUMERIC]
    categorical = [c for c in retained if c not in NUMERIC]
    transformer = ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
            ("scaler", StandardScaler()),
        ]), numeric),
        ("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="constant", fill_value="__MISSING__", keep_empty_features=True)),
            ("encoder", OneHotEncoder(handle_unknown="infrequent_if_exist",
                                      min_frequency=min_frequency, sparse_output=True, dtype=np.float32)),
        ]), categorical),
    ], sparse_threshold=1.0, remainder="drop")
    return transformer, {
        "dropped_over_50_percent_missing_train": missing_drops,
        "dropped_constant_train": constant_drops,
        "numeric_features": numeric, "categorical_features": categorical,
        "retained_features": retained, "rare_category_min_frequency": min_frequency,
    }


def run(source: Path, output: Path, report_dir: Path, mode: str, seed: int) -> dict:
    raw, digest = load_data(source, ROOT / "data/raw")
    frame, quality = clean_data(raw)
    y = make_target(frame, mode)
    splits = split_patients(frame, seed)
    features = frame.drop(columns=IDS + [TARGET])
    transformer, feature_info = build_transformer(features.iloc[splits["train"]])
    transformer.fit(features.iloc[splits["train"]])
    names = transformer.get_feature_names_out().tolist()
    output.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output / "cleaned.csv", index=False)
    split_report = {}
    for name, indices in splits.items():
        subset = features.iloc[indices]
        labels = y.iloc[indices]
        if set(labels) != set(y):
            raise ValueError(f"Kelas tidak lengkap di {name}; tinjau protokol split.")
        encoded = sparse.csr_matrix(transformer.transform(subset), dtype=np.float32)
        if not np.isfinite(encoded.data).all():
            raise AssertionError("Matriks mengandung NaN/Inf.")
        sparse.save_npz(output / f"X_{name}.npz", encoded)
        subset[feature_info["retained_features"]].to_csv(output / f"X_{name}.csv", index=False)
        labels.to_csv(output / f"y_{name}.csv", index=False)
        frame.iloc[indices][IDS].to_csv(output / f"ids_{name}.csv", index=False)
        split_report[name] = {
            "rows": len(indices), "patients": int(frame.iloc[indices].patient_nbr.nunique()),
            "class_counts": {str(k): int(v) for k, v in labels.value_counts().sort_index().items()},
            "class_proportions": {str(k): float(v) for k, v in labels.value_counts(normalize=True).sort_index().items()},
            "encoded_shape": list(encoded.shape), "nonzero_values": int(encoded.nnz),
        }
    joblib.dump(transformer, output / "preprocessor.joblib")
    write_json(output / "feature_names.json", names)
    write_json(output / "feature_schema.json", feature_info)
    metadata = {
        "dataset": "Diabetes 130-US Hospitals for Years 1999-2008", "source": SOURCE,
        "license": "CC BY 4.0", "raw_csv_sha256": digest, "seed": seed,
        "prediction_time": "at discharge", "target_mode": mode,
        "target_mapping": {"NO": 0, ">30": 0, "<30": 1} if mode == "binary" else {"NO": 0, ">30": 1, "<30": 2},
        "split": "GroupShuffleSplit, approximately 70/15/15 percent patients; not stratified or temporal",
        "patient_overlap_between_splits": 0, "fit_on": "train only",
        "quality": quality, "features": feature_info, "splits": split_report,
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "pandas": pd.__version__, "scipy": scipy.__version__,
                     "scikit_learn": sklearn.__version__, "joblib": joblib.__version__},
    }
    write_json(output / "metadata.json", metadata)
    write_json(report_dir / "preprocessing_summary.json", metadata)
    pd.DataFrame({
        "column": raw.columns,
        "missing_raw_question_mark_or_blank": [int(raw[c].str.strip().isin(["?", ""]).sum()) for c in raw],
        "missing_clean": [int(frame[c].isna().sum()) for c in raw],
        "missing_train_fraction": [float(features.iloc[splits["train"]][c].isna().mean()) if c in features else None for c in raw],
    }).to_csv(report_dir / "missing_values.csv", index=False)
    rows = ["# Hasil preprocessing", "", "Dibuat oleh `python -m src.preprocess`.", "",
            f"- Data asli: {len(raw):,} baris, {len(raw.columns)} kolom.",
            f"- Setelah cleaning/cohort: {len(frame):,} baris.",
            f"- Kunjungan berstatus meninggal dikeluarkan: {quality['death_discharge_rows_removed']:,}.",
            f"- Target: `{mode}`; pemetaan: `{metadata['target_mapping']}`.",
            f"- Jumlah fitur setelah encoding: {len(names)}.",
            "- Pasien tumpang tindih antarset: 0; transformer di-fit pada train saja.", "",
            "| Set | Baris | Pasien | Jumlah per kelas |", "|---|---|---|---|"]
    for name, info in split_report.items():
        rows.append(f"| {name} | {info['rows']} | {info['patients']} | {info['class_counts']} |")
    rows += ["", "## Kolom yang dikeluarkan", "",
             f"- ID: {', '.join(IDS)} (hanya metadata/pembagian, bukan fitur).",
             f"- Missing >50% pada train: {feature_info['dropped_over_50_percent_missing_train']}.",
             f"- Konstan pada train: {feature_info['dropped_constant_train']}.", "",
             "Laporan ini hanya preprocessing; percobaan model ada pada laporan week 11. Jangan memilih model/parameter dari test.",
             "Pembagian ini menguji generalisasi ke pasien berbeda, bukan prediksi tahun mendatang.", ""]
    (report_dir / "preprocessing_report.md").write_text("\n".join(rows), encoding="utf-8")
    print(json.dumps({"rows": len(frame), "encoded_features": len(names), "splits": split_report}, indent=2))
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data/raw/diabetic_data.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "data/processed/diabetes")
    parser.add_argument("--reports", type=Path, default=ROOT / "results/preprocessing")
    parser.add_argument("--target", choices=["binary", "multiclass"], default="binary")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    run(args.input, args.output, args.reports, args.target, args.seed)


if __name__ == "__main__":
    main()
