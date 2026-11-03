"""Percobaan awal week 11, hanya train dan validation; test tidak dibaca."""

import argparse
import json
import time
import warnings

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score, balanced_accuracy_score,
                             confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score)

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
            "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}


def run(data_dir, output, seed=42):
    meta = json.loads((data_dir / "metadata.json").read_text(encoding="utf-8"))
    if meta["target_mode"] != "binary":
        raise ValueError("Percobaan week 11 menggunakan target binary. Buat preprocessing binary terlebih dahulu.")
    x_train = sparse.load_npz(data_dir / "X_train.npz")
    x_val = sparse.load_npz(data_dir / "X_validation.npz")
    y_train = pd.read_csv(data_dir / "y_train.csv").target.to_numpy()
    y_val = pd.read_csv(data_dir / "y_validation.csv").target.to_numpy()
    train_ids = pd.read_csv(data_dir / "ids_train.csv", dtype=str)
    val_ids = pd.read_csv(data_dir / "ids_validation.csv", dtype=str)
    if set(train_ids.patient_nbr) & set(val_ids.patient_nbr):
        raise ValueError("Pasien overlap train/validation.")
    if x_train.shape[0] != len(y_train) or x_val.shape[0] != len(y_val) or x_train.shape[1] != x_val.shape[1]:
        raise ValueError("Dimensi X/y tidak konsisten.")
    models = {
        "Dummy_most_frequent": DummyClassifier(strategy="most_frequent"),
        "Logistic_Regression": LogisticRegression(solver="liblinear", C=1.0, max_iter=1000,
                                                   class_weight="balanced", random_state=seed),
        "Random_Forest": RandomForestClassifier(n_estimators=150, max_depth=16, min_samples_leaf=5,
                                                 max_features="sqrt", class_weight="balanced_subsample",
                                                 random_state=seed, n_jobs=2),
    }
    output.mkdir(parents=True, exist_ok=True)
    model_dir = data_dir / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    rows, details = [], {}
    for name, model in models.items():
        start = time.perf_counter()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ConvergenceWarning)
            model.fit(x_train, y_train)
        if any(issubclass(item.category, ConvergenceWarning) for item in caught):
            raise RuntimeError(f"{name} belum konvergen; jangan gunakan hasilnya sebagai hasil final.")
        probability = model.predict_proba(x_val)[:, list(model.classes_).index(1)]
        scores = binary_metrics(y_val, probability)
        rows.append({"model": name, "set": "validation", **scores})
        details[name] = {"parameters": model.get_params(), "seconds_fit_and_predict": time.perf_counter() - start,
                         "warnings": [str(item.message) for item in caught], "metrics": scores}
        pd.DataFrame({"y_true": y_val, "probability": probability,
                      "y_pred": (probability >= 0.5).astype(int)}).to_csv(model_dir / f"validation_predictions_{name}.csv", index=False)
        joblib.dump(model, model_dir / f"{name}.joblib")
        print(f"{name}: AP={scores['average_precision']:.4f}, F1={scores['f1']:.4f}", flush=True)
    table = pd.DataFrame(rows)
    table.to_csv(output / "validation_metrics.csv", index=False)
    write_json(output / "experiment.json", {
        "stage": "week-11 initial experiment", "evaluation_set": "validation", "test_evaluated": False,
        "seed": seed, "threshold": 0.5, "threshold_tuned": False,
        "raw_csv_sha256": meta["raw_csv_sha256"], "preprocessing": meta,
        "primary_ranking_metric": "average_precision", "experiments": details,
    })
    display = table[["model", "accuracy", "balanced_accuracy", "precision", "recall", "f1", "roc_auc", "average_precision"]].copy()
    for col in display.columns[1:]:
        display[col] = display[col].map(lambda value: f"{value:.4f}")
    best = table.loc[table.average_precision.idxmax(), "model"]
    report = ["# Percobaan awal week 11", "", "Evaluasi pada validation; tidak membaca X_test/y_test.", "",
              md_table(display), "", "## Interpretasi", "",
              f"- Average precision tertinggi pada percobaan ini: **{best}**.",
              f"- Prevalensi kelas positif validation: {y_val.mean():.4f}; ini acuan AP prediktor skor konstan.",
              "- Dummy mayoritas dapat memiliki akurasi tinggi sambil tidak mengenali kasus positif.",
              "- Threshold 0,5 tetap; pembobotan kelas membuat precision/recall perlu dibaca bersama.",
              "- Average precision adalah ringkasan kurva precision-recall, bukan integrasi trapezoid PR-AUC.",
              "- Skor ini dari satu split dan konfigurasi awal, bukan hasil tuning, CV atau uji final.",
              "- Week 12 dapat menambah validasi berbasis pasien, tuning dan analisis kesalahan; test tetap disimpan.", "",
              "![Confusion matrix validation](validation_confusion_matrices.png)", ""]
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
    return table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=type(ROOT), default=ROOT / "data/processed/diabetes")
    parser.add_argument("--output", type=type(ROOT), default=ROOT / "results/archive/week-11-lr-rf")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    run(args.data, args.output, args.seed)


if __name__ == "__main__":
    main()
