"""Percobaan awal week 11, hanya train dan validation; test tidak dibaca."""

import argparse
import json
import time
import warnings
from importlib.metadata import version

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.dummy import DummyClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.exceptions import ConvergenceWarning
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import (accuracy_score, average_precision_score, balanced_accuracy_score,
                             confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score,
                             brier_score_loss, log_loss)

from src.preprocess import ROOT, write_json
from src.profile_data import md_table


def binary_metrics(y_true, probability, threshold=0.5):
    y_true = np.asarray(y_true)
    probability = np.asarray(probability)
    if len(y_true) != len(probability) or probability.ndim != 1:
        raise ValueError("Target dan probabilitas harus berupa vektor sejajar.")
    if set(np.unique(y_true)) != {0, 1}:
        raise ValueError("Evaluasi awal mensyaratkan dua kelas 0 dan 1.")
    if not np.isfinite(probability).all() or ((probability < 0) | (probability > 1)).any():
        raise ValueError("Probabilitas harus finite dalam rentang 0-1.")
    prediction = (probability >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, prediction, labels=[0, 1]).ravel()
    return {"accuracy": accuracy_score(y_true, prediction),
            "balanced_accuracy": balanced_accuracy_score(y_true, prediction),
            "precision": precision_score(y_true, prediction, zero_division=0),
            "recall": recall_score(y_true, prediction, zero_division=0),
            "f1": f1_score(y_true, prediction, zero_division=0),
            "roc_auc": roc_auc_score(y_true, probability),
            "average_precision": average_precision_score(y_true, probability),
            "brier_score": brier_score_loss(y_true, probability),
            "log_loss": log_loss(y_true, probability, labels=[0, 1]),
            "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}


def make_feature_adapter(x_train, seed=42, components=32):
    """Representasi kontinu bersama, di-fit hanya pada train; menerima sparse."""
    count = min(components, x_train.shape[0] - 1, x_train.shape[1] - 1)
    if count < 1:
        raise ValueError("Data terlalu kecil untuk adapter SVD.")
    adapter = make_pipeline(TruncatedSVD(n_components=count, n_iter=5, random_state=seed), StandardScaler())
    adapter.fit(x_train)
    return adapter


def make_models(seed=42):
    # Import saat training agar tes metrik/adapter tidak memuat numba.
    from aeon.classification.sklearn import RotationForestClassifier
    from ngboost import NGBClassifier
    from ngboost.distns import Bernoulli
    return {
        "Dummy_prior": DummyClassifier(strategy="prior"),
        "NGBoost": NGBClassifier(Dist=Bernoulli,
            Base=DecisionTreeRegressor(max_depth=3, min_samples_leaf=20, random_state=seed),
            n_estimators=150, learning_rate=0.03, minibatch_frac=0.75,
            random_state=seed, verbose=False),
        "Rotation_Forest": RotationForestClassifier(n_estimators=20, n_jobs=2, random_state=seed),
    }


def calibration_bins(y_true, probability, bins=10):
    """Bin sama lebar; bin kosong tidak ditampilkan."""
    groups = np.minimum((np.asarray(probability) * bins).astype(int), bins - 1)
    return [{"bin": int(i), "count": int((groups == i).sum()),
             "mean_probability": float(np.asarray(probability)[groups == i].mean()),
             "positive_fraction": float(np.asarray(y_true)[groups == i].mean())}
            for i in range(bins) if (groups == i).any()]


def positive_probability(model, x):
    probability = model.predict_proba(x)
    if hasattr(model, "classes_"):
        index = list(model.classes_).index(1)
    elif model.__class__.__module__.startswith("ngboost"):
        # NGBClassifier Bernoulli mensyaratkan label 0/1, tetapi tidak punya classes_.
        index = 1
    else:
        raise ValueError("Urutan kelas estimator tidak diketahui.")
    return probability[:, index]


def run(data_dir, output, seed=42):
    meta = json.loads((data_dir / "metadata.json").read_text(encoding="utf-8"))
    if meta["target_mode"] != "binary":
        raise ValueError("Percobaan week 11 menggunakan target binary. Buat preprocessing binary terlebih dahulu.")
    x_train = sparse.load_npz(data_dir / "X_train.npz")
    x_val = sparse.load_npz(data_dir / "X_validation.npz")
    y_train = pd.read_csv(data_dir / "y_train.csv").target.to_numpy()
    y_val = pd.read_csv(data_dir / "y_validation.csv").target.to_numpy()
    if set(np.unique(y_train)) != {0, 1}:
        raise ValueError("Train harus memuat label biner 0 dan 1.")
    train_ids = pd.read_csv(data_dir / "ids_train.csv", dtype=str)
    val_ids = pd.read_csv(data_dir / "ids_validation.csv", dtype=str)
    if set(train_ids.patient_nbr) & set(val_ids.patient_nbr):
        raise ValueError("Pasien overlap train/validation.")
    if x_train.shape[0] != len(y_train) or x_val.shape[0] != len(y_val) or x_train.shape[1] != x_val.shape[1]:
        raise ValueError("Dimensi X/y tidak konsisten.")
    if len(train_ids) != len(y_train) or len(val_ids) != len(y_val):
        raise ValueError("Metadata ID dan target tidak sejajar.")
    print("Fit adapter SVD 32 + scaling pada train...", flush=True)
    adapter = make_feature_adapter(x_train, seed=seed)
    x_train = adapter.transform(x_train).astype(np.float32)
    x_val = adapter.transform(x_val).astype(np.float32)
    models = make_models(seed)
    output.mkdir(parents=True, exist_ok=True)
    model_dir = data_dir / "models_paper"
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(adapter, model_dir / "feature_adapter.joblib")
    rows, details = [], {}
    calibration = []
    for name, model in models.items():
        start = time.perf_counter()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ConvergenceWarning)
            model.fit(x_train, y_train)
        if any(issubclass(item.category, ConvergenceWarning) for item in caught):
            raise RuntimeError(f"{name} belum konvergen; jangan gunakan hasilnya sebagai hasil final.")
        joblib.dump(model, model_dir / f"{name}.joblib")
        probability = positive_probability(model, x_val)
        scores = binary_metrics(y_val, probability)
        rows.append({"model": name, "set": "validation", **scores})
        params = json.loads(json.dumps(model.get_params(), default=repr))
        details[name] = {"parameters": params, "seconds_fit_and_predict": time.perf_counter() - start,
                         "warnings": [str(item.message) for item in caught], "metrics": scores}
        calibration.extend({"model": name, **row} for row in calibration_bins(y_val, probability))
        pd.DataFrame({"y_true": y_val, "probability": probability,
                      "y_pred": (probability >= 0.5).astype(int)}).to_csv(model_dir / f"validation_predictions_{name}.csv", index=False)
        joblib.dump(model, model_dir / f"{name}.joblib")
        print(f"{name}: AP={scores['average_precision']:.4f}, F1={scores['f1']:.4f}", flush=True)
    table = pd.DataFrame(rows)
    table.to_csv(output / "validation_metrics.csv", index=False)
    calibration_table = pd.DataFrame(calibration)
    calibration_table.to_csv(output / "validation_calibration.csv", index=False)
    write_json(output / "experiment.json", {
        "stage": "week-11 initial experiment", "evaluation_set": "validation", "test_evaluated": False,
        "seed": seed, "threshold": 0.5, "threshold_tuned": False,
        "raw_csv_sha256": meta["raw_csv_sha256"], "preprocessing": meta,
        "primary_ranking_metric": "average_precision", "experiments": details,
        "algorithm_revision": "NGBoost and Rotation Forest; prior LR/RF run archived",
        "versions": {package: version(package) for package in ["numpy", "pandas", "scipy", "scikit-learn", "ngboost", "aeon"]},
        "feature_adapter": {"method": "TruncatedSVD + StandardScaler, fit train only",
                            "components": int(x_train.shape[1]), "random_state": seed,
                            "explained_variance_ratio_sum": float(adapter[0].explained_variance_ratio_.sum())},
        "class_reweighting": False, "probability_calibration_fitted": False,
    })
    display = table[["model", "accuracy", "precision", "recall", "f1", "roc_auc", "average_precision", "brier_score", "log_loss"]].copy()
    for col in display.columns[1:]:
        display[col] = display[col].map(lambda value: f"{value:.4f}")
    best = table.loc[table.average_precision.idxmax(), "model"]
    report = ["# Percobaan awal week 11", "", "Evaluasi pada validation; tidak membaca X_test/y_test.", "",
              md_table(display), "", "## Interpretasi", "",
              f"- Average precision tertinggi pada percobaan ini: **{best}**.",
              f"- Prevalensi kelas positif validation: {y_val.mean():.4f}; ini acuan AP prediktor skor konstan.",
              "- Dummy mayoritas dapat memiliki akurasi tinggi sambil tidak mengenali kasus positif.",
              "- Threshold 0,5 tetap; tidak ada class weighting atau oversampling. Baca precision/recall bersama.",
              "- Dummy_prior memprediksi probabilitas prevalensi train, bukan selalu probabilitas nol.",
              "- Kedua algoritma memakai adapter SVD 32 komponen + scaling yang sama, di-fit hanya pada train.",
              "- Brier score dan log loss lebih kecil lebih baik; model probabilistik tidak otomatis terkalibrasi.",
              "- Hasil LR/RF lama menggunakan representasi dan pembobotan berbeda; bukan perbandingan terkontrol dengan eksperimen ini.",
              "- Average precision adalah ringkasan kurva precision-recall, bukan integrasi trapezoid PR-AUC.",
              "- Skor ini dari satu split dan konfigurasi awal, bukan hasil tuning, CV atau uji final.",
              "- Week 12 dapat menambah validasi berbasis pasien, tuning dan analisis kesalahan; test tetap disimpan.", "",
              "![Confusion matrix validation](validation_confusion_matrices.png)", ""]
    report += ["![Kurva kalibrasi validation](validation_calibration.png)", ""]
    (output / "report.md").write_text("\n".join(report), encoding="utf-8")
    fig, axes = plt.subplots(1, len(rows), figsize=(12, 3.8), layout="constrained")
    for ax, row in zip(axes, rows):
        matrix = np.array([[row["tn"], row["fp"]], [row["fn"], row["tp"]]])
        ax.imshow(matrix, cmap="Blues")
        for (i, j), count in np.ndenumerate(matrix):
            ax.text(j, i, f"{count:,}", ha="center", va="center",
                    color="white" if count > matrix.max() / 2 else "black")
        ax.set(xticks=[0, 1], yticks=[0, 1], xticklabels=["Lainnya", "<30"], yticklabels=["Lainnya", "<30"],
               title=row["model"].replace("_", " "), xlabel="Prediksi", ylabel="Aktual")
    fig.savefig(output / "validation_confusion_matrices.png", dpi=160)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(6, 4.5), layout="constrained")
    ax.plot([0, 1], [0, 1], "--", color="gray", label="Kalibrasi ideal")
    for name, group in calibration_table.groupby("model", sort=False):
        ax.plot(group.mean_probability, group.positive_fraction, marker="o", label=name.replace("_", " "))
    ax.set(xlabel="Rata-rata probabilitas (bin)", ylabel="Proporsi positif aktual", xlim=(0, 1), ylim=(0, 1))
    ax.legend(fontsize=8)
    fig.savefig(output / "validation_calibration.png", dpi=160)
    plt.close(fig)
    return table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=type(ROOT), default=ROOT / "data/processed/diabetes")
    parser.add_argument("--output", type=type(ROOT), default=ROOT / "results/week-11")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    run(args.data, args.output, args.seed)


if __name__ == "__main__":
    main()
