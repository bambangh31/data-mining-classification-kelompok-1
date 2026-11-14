"""Revisi dosen: NGBoost sebelum/sesudah oversampling; evaluasi validation saja."""

import argparse
import json
import time
from importlib.metadata import version

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from scipy import sparse
from sklearn.base import clone

from src.mining import (binary_metrics, calibration_bins, make_feature_adapter,
                        make_models, plt, positive_probability)
from src.preprocess import ROOT, write_json
from src.profile_data import md_table
from src.revision_thresholds import run as compare_thresholds


def class_counts(y):
    labels, counts = np.unique(y, return_counts=True)
    return {str(int(label)): int(count) for label, count in zip(labels, counts)}


def run(data, output, seed=42):
    meta = json.loads((data / "metadata.json").read_text(encoding="utf-8"))
    if meta["target_mode"] != "binary":
        raise ValueError("Eksperimen ini membutuhkan target binary.")
    matrices, targets, ids = {}, {}, {}
    for split in ("train", "validation"):
        matrices[split] = sparse.load_npz(data / f"X_{split}.npz")
        targets[split] = pd.read_csv(data / f"y_{split}.csv").target.to_numpy()
        ids[split] = pd.read_csv(data / f"ids_{split}.csv", dtype=str)
        if matrices[split].shape[0] != len(targets[split]) or len(ids[split]) != len(targets[split]):
            raise ValueError("X, y dan ID tidak sejajar.")
        if set(np.unique(targets[split])) != {0, 1}:
            raise ValueError("Setiap set harus memiliki kelas 0 dan 1.")
    if set(ids["train"].patient_nbr) & set(ids["validation"].patient_nbr):
        raise ValueError("Pasien overlap train/validation.")
    if matrices["train"].shape[1] != matrices["validation"].shape[1]:
        raise ValueError("Jumlah fitur antarset berbeda.")
    # Fit representasi pada seluruh train asli sebelum duplikasi kelas minoritas.
    adapter = make_feature_adapter(matrices["train"], seed=seed)
    x_train = adapter.transform(matrices["train"]).astype(np.float32)
    x_val = adapter.transform(matrices["validation"]).astype(np.float32)
    y_train, y_val = targets["train"], targets["validation"]
    sampler = RandomOverSampler(sampling_strategy="minority", random_state=seed)
    x_balanced, y_balanced = sampler.fit_resample(x_train, y_train)
    models = make_models(seed)
    experiments = {
        "Dummy_prior": (models["Dummy_prior"], x_train, y_train),
        "NGBoost": (models["NGBoost"], x_train, y_train),
        "NGBoost_ROS": (clone(models["NGBoost"]), x_balanced, y_balanced),
    }
    output.mkdir(parents=True, exist_ok=True)
    # Artefak baru terpisah agar model dan protokol Week 11/12 tetap bisa direproduksi.
    model_dir = data / "models_revision"
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(adapter, model_dir / "feature_adapter.joblib")
    joblib.dump(sampler, model_dir / "oversampler.joblib")
    rows, details, calibration = [], {}, []
    for name, (model, features, labels) in experiments.items():
        print(f"Training {name}: {len(labels):,} baris, {class_counts(labels)}", flush=True)
        start = time.perf_counter()
        model.fit(features, labels)
        probability = positive_probability(model, x_val)
        scores = binary_metrics(y_val, probability)
        rows.append({"model": name, "set": "validation", "threshold": 0.5, **scores})
        details[name] = {"train_class_counts": class_counts(labels), "training_rows": len(labels),
                         "parameters": json.loads(json.dumps(model.get_params(), default=repr)),
                         "seconds_fit_and_predict": time.perf_counter() - start, "metrics": scores}
        joblib.dump(model, model_dir / f"{name}.joblib")
        pd.DataFrame({"y_true": y_val, "probability": probability,
                      "y_pred": (probability >= .5).astype(int)}).to_csv(
                          model_dir / f"validation_predictions_{name}.csv", index=False)
        calibration.extend({"model": name, **row} for row in calibration_bins(y_val, probability))
        print(f"{name}: AP={scores['average_precision']:.4f}, recall={scores['recall']:.4f}, F1={scores['f1']:.4f}", flush=True)
    table = pd.DataFrame(rows)
    table.to_csv(output / "validation_metrics.csv", index=False)
    pd.DataFrame(calibration).to_csv(output / "validation_calibration.csv", index=False)
    write_json(output / "experiment.json", {
        "stage": "lecturer revision: NGBoost oversampling ablation", "seed": seed,
        "evaluation_set": "validation", "test_evaluated": False, "threshold": .5,
        "threshold_tuned": False, "preprocessing": meta, "experiments": details,
        "oversampling": {"method": "RandomOverSampler", "sampling_strategy": "minority",
                         "fit_on": "train only, after original-train SVD/scaling",
                         "before": class_counts(y_train), "after": class_counts(y_balanced),
                         "added_rows": len(y_balanced) - len(y_train),
                         "new_patients": 0, "validation_resampled": False, "test_resampled": False},
        "feature_adapter": {"fit_on": "original train only", "components": x_train.shape[1]},
        "versions": {name: version(name) for name in
                     ("numpy", "pandas", "scipy", "scikit-learn", "ngboost", "imbalanced-learn")},
    })
    view = table[["model", "accuracy", "balanced_accuracy", "precision", "recall", "f1",
                  "average_precision", "roc_auc", "brier_score", "log_loss"]].copy()
    for col in view.columns[1:]:
        view[col] = view[col].map(lambda value: f"{value:.4f}")
    before, after = table.set_index("model").loc[["NGBoost", "NGBoost_ROS"]].to_dict("records")
    split_rows = [{"set": name, "kunjungan": info["rows"], "pasien": info["patients"],
                   "kelas_0": info["class_counts"]["0"], "kelas_1": info["class_counts"]["1"]}
                  for name, info in meta.get("splits", {}).items()]
    quality = meta.get("quality", {})
    cohort = (f"Data asli memiliki {quality['raw_rows']:,} kunjungan dan {quality['raw_columns']} kolom. "
              f"Sebanyak {quality['death_discharge_rows_removed']:,} kunjungan "
              "berstatus meninggal (discharge 11/19/20/21) dikeluarkan, "
              f"sehingga tersisa {quality['clean_rows']:,} kunjungan. "
              if quality else "Ukuran cohort asli tidak tersedia dalam metadata eksperimen ini. ")
    report = ["# Revisi dosen — NGBoost dan oversampling", "",
              "## Apakah seluruh data digunakan untuk train?", "",
              "Tidak. " + cohort +
              "Pembagian sekitar 70%/15%/15% berdasarkan pasien, bukan pengacakan baris. "
              f"Seluruh {len(y_train):,} kunjungan pada train tersedia untuk pelatihan. "
              "Validation untuk evaluasi/pemilihan; test untuk evaluasi sesudah konfigurasi dikunci.", ""]
    if split_rows:
        report += [md_table(pd.DataFrame(split_rows)), ""]
    report += ["NGBoost memakai minibatch_frac=0,75: seluruh train menjadi kumpulan data pelatihan, "
               "tetapi setiap iterasi boosting mengambil sampel acak 75% dari kumpulan tersebut. "
               "Pada varian ROS, kumpulannya adalah train setelah oversampling. "
               "Ini berbeda dari membuang sebagian train secara permanen.", ""]
    report += ["Angka tabel split berasal dari metadata preprocessing; runner ini hanya membaca fitur/target "
               "train dan validation. Data test tidak dibaca. Pasien antarset terpisah. "
               "ID pasien/kunjungan dan readmitted tidak masuk fitur. "
               f"Representasi masukan memiliki {matrices['train'].shape[1]:,} fitur hasil preprocessing, "
               f"lalu SVD menjadi {x_train.shape[1]} komponen. "
               "Pada dataset penuh seed 42, dari 47 kandidat fitur, weight dan tiga kolom konstan "
               "dikeluarkan berdasarkan train; tersisa 43 kolom sebelum one-hot.", "",
               "## Percobaan terkontrol", "",
               f"Train asli: {class_counts(y_train)}. Sesudah RandomOverSampler: {class_counts(y_balanced)}; "
               f"tambahan {len(y_balanced) - len(y_train):,} baris merupakan duplikasi acak kelas minoritas, "
               "bukan pasien baru. Kedua NGBoost memakai parameter, seed, split dan adapter yang sama. "
               "Dummy prior dilatih pada train asli sebagai baseline prevalensi.", "",
               "Imputasi, encoding, SVD dan scaling di-fit pada train asli. Oversampling hanya setelah "
               "transformasi train. Validation dan test mempertahankan distribusi kelas asli. "
               "Random oversampling dipilih agar tidak membuat interpolasi kategori obat/diagnosis. "
               "Jika kelak memakai CV, fit preprocessing dan oversampling harus diulang pada training fold saja.", "",
               "## Hasil validation (threshold 0,5)", "", md_table(view), "",
               f"Recall berubah dari {before['recall']:.4f} ke {after['recall']:.4f}; "
               f"precision dari {before['precision']:.4f} ke {after['precision']:.4f}; "
               f"F1 dari {before['f1']:.4f} ke {after['f1']:.4f}; "
               f"AP dari {before['average_precision']:.4f} ke {after['average_precision']:.4f}.", "",
               f"NGBoost_ROS menangkap {int(after['tp']):,} kasus positif, melewatkan {int(after['fn']):,}, "
               f"dan menghasilkan {int(after['fp']):,} prediksi positif yang salah. "
               "Bandingkan metrik ranking dan kualitas probabilitas secara terpisah dari deteksi pada threshold 0,5.", "",
               "Oversampling menyeimbangkan train, tetapi tidak menjamin semua metrik membaik. "
               "AP menilai ranking tanpa threshold; F1/recall/precision di atas memakai 0,5 yang sama. "
               "Perubahan prior train dapat menggeser probabilitas; baca Brier/log loss dan kalibrasi. "
               "Probabilitas belum dikalibrasi ulang. Hasil ini satu split validation, bukan skor test baru "
               "atau bukti keunggulan umum. Test Week 12 sudah pernah dievaluasi pada eksperimen terdahulu; "
               "jangan menyebutnya holdout yang belum pernah dilihat untuk klaim lanjutan.", "",
               "![Distribusi train sebelum dan sesudah oversampling](class_balance.png)", "",
               "## Perbandingan setelah memilih ambang", "",
               "Kedua model juga dibandingkan dengan ambang yang memaksimalkan F1 pada validation. "
               "Lihat [hasil pemilihan ambang dan batas interpretasi](threshold_report.md).", "",
               "## Reproduksi", "", "```powershell",
               ".\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt",
               ".\\.venv\\Scripts\\python.exe -m src.preprocess",
               ".\\.venv\\Scripts\\python.exe -m src.profile_data",
               ".\\.venv\\Scripts\\python.exe -m src.revision", "```", "",
               "Hasil lama Week 11/12 dipertahankan sebagai riwayat. Artefak model revisi: "
               "data/processed/diabetes/models_revision (lokal). "
               "Arti kode lengkap: [kode kategori](../../docs/week-10/kode-kategori.md).", "",
               "Referensi: [RandomOverSampler](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.RandomOverSampler.html), "
               "[NGBoost](https://proceedings.mlr.press/v119/duan20a.html).", ""]
    (output / "report.md").write_text("\n".join(report), encoding="utf-8")
    fig, axes = plt.subplots(1, 2, figsize=(9, 4), layout="constrained")
    for ax, title, labels in zip(axes, ("Train asli", "Train setelah ROS"), (y_train, y_balanced)):
        counts = class_counts(labels)
        bars = ax.bar(["0: NO / >30", "1: <30"], [counts["0"], counts["1"]], color=["#547c9e", "#c86c49"])
        ax.bar_label(bars, padding=3)
        ax.set(title=title, ylabel="Jumlah baris", ylim=(0, max(class_counts(y_balanced).values()) * 1.15))
    fig.savefig(output / "class_balance.png", dpi=160)
    plt.close(fig)
    compare_thresholds(data, output)
    return table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=type(ROOT), default=ROOT / "data/processed/diabetes")
    parser.add_argument("--output", type=type(ROOT), default=ROOT / "results/revisi-dosen")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    run(args.data, args.output, args.seed)


if __name__ == "__main__":
    main()
