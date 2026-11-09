"""Bekukan ambang pada validation, lalu evaluasi model Week 11 pada holdout."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import joblib
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics import precision_recall_curve

from src.mining import binary_metrics, calibration_bins, plt, positive_probability
from src.preprocess import ROOT, write_json
from src.profile_data import md_table


MODELS = ("Dummy_prior", "NGBoost", "Rotation_Forest")
BASELINE = MODELS[0]


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def artifact_hashes(data):
    names = ["metadata.json", "ids_train.csv", "ids_validation.csv",
             "X_validation.npz", "y_validation.csv",
             "models_paper/feature_adapter.joblib"]
    names.extend(f"models_paper/{name}.joblib" for name in MODELS)
    return {name: sha(data / name) for name in names}


def predict(data, split):
    matrix = sparse.load_npz(data / f"X_{split}.npz")
    model_dir = data / "models_paper"
    # Only load artifacts created locally by the Week 11 pipeline.
    adapter = joblib.load(model_dir / "feature_adapter.joblib")
    features = adapter.transform(matrix).astype(np.float32)
    return {name: positive_probability(joblib.load(model_dir / f"{name}.joblib"), features)
            for name in MODELS}


def choose_threshold(y, probability):
    """Maximize F1 over the validation score cutoffs; prefer higher cutoff in a tie."""
    precision, recall, thresholds = precision_recall_curve(y, probability)
    p, r = precision[:-1], recall[:-1]
    f1 = np.divide(2 * p * r, p + r, out=np.zeros_like(p), where=(p + r) > 0)
    best = np.flatnonzero(np.isclose(f1, f1.max(), atol=1e-12, rtol=0))[-1]
    return float(thresholds[best]), len(thresholds)


def freeze(data, output, week11):
    meta = json.loads((data / "metadata.json").read_text(encoding="utf-8"))
    previous = json.loads((week11 / "experiment.json").read_text(encoding="utf-8"))
    if meta["target_mode"] != "binary" or previous["preprocessing"] != meta:
        raise ValueError("Preprocessing tidak cocok dengan eksperimen biner Week 11.")
    y = pd.read_csv(data / "y_validation.csv").target.to_numpy()
    probabilities = predict(data, "validation")
    choices = {}
    for name, probability in probabilities.items():
        original = binary_metrics(y, probability)
        expected = previous["experiments"][name]["metrics"]
        if any(not np.isclose(value, expected[key], atol=1e-8, rtol=1e-7)
               for key, value in original.items()):
            raise ValueError(f"Prediksi validation {name} tidak cocok dengan hasil Week 11.")
        threshold, candidates = (0.5, 0) if name == BASELINE else choose_threshold(y, probability)
        choices[name] = {"threshold": threshold, "candidate_count": candidates,
                         "validation_at_0_5": original,
                         "validation_at_locked_threshold": binary_metrics(y, probability, threshold)}
    primary = max(MODELS[1:], key=lambda name: choices[name]["validation_at_0_5"]["average_precision"])
    protocol = {
        "locked_utc": datetime.now(timezone.utc).isoformat(),
        "selected_on": "validation", "test_read_during_selection": False,
        "threshold_rule": "maximize positive-class F1 over unique validation scores; higher threshold on ties",
        "primary_model_rule": "highest validation average precision among the two trained models",
        "primary_model": primary, "baseline_keeps_threshold": 0.5,
        "raw_csv_sha256": meta["raw_csv_sha256"], "week11_experiment_sha256": sha(week11 / "experiment.json"),
        "artifact_hashes": artifact_hashes(data), "models": choices,
    }
    output.mkdir(parents=True, exist_ok=True)
    with (output / "protocol.json").open("x", encoding="utf-8") as stream:
        json.dump(protocol, stream, indent=2)
        stream.write("\n")
    return protocol


def error_groups(frame, y, probabilities, choices):
    prior = pd.cut(frame.number_inpatient, [-1, 0, 1, np.inf], labels=["0", "1", "2+"])
    rows = []
    for field, groups in [("age", frame.age), ("number_inpatient", prior)]:
        for group in sorted(groups.dropna().unique()):
            mask = np.asarray(groups == group)
            actual = y[mask] == 1
            for name in MODELS[1:]:
                predicted = probabilities[name][mask] >= choices[name]["threshold"]
                tp = int((actual & predicted).sum())
                fn = int((actual & ~predicted).sum())
                fp = int((~actual & predicted).sum())
                tn = int((~actual & ~predicted).sum())
                rows.append({"model": name, "variable": field, "group": str(group), "n": int(mask.sum()),
                             "positives": tp + fn, "tn": tn, "fp": fp, "fn": fn, "tp": tp,
                             "recall": tp / (tp + fn) if tp + fn else None,
                             "precision": tp / (tp + fp) if tp + fp else None})
    return pd.DataFrame(rows)


def plot_results(directory, scores, y, probabilities, choices):
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), layout="constrained")
    for ax, name in zip(axes, MODELS):
        row = scores[(scores.model == name) & (scores.policy == "locked")].iloc[0]
        matrix = np.array([[row.tn, row.fp], [row.fn, row.tp]])
        ax.imshow(matrix, cmap="Blues", vmin=0, vmax=len(y))
        for (i, j), count in np.ndenumerate(matrix):
            ax.text(j, i, f"{count:,}", ha="center", va="center",
                    color="white" if count > len(y) / 2 else "black")
        ax.set(xticks=[0, 1], yticks=[0, 1], xticklabels=["Lainnya", "<30"], yticklabels=["Lainnya", "<30"],
               title=f"{name.replace('_', ' ')} | ambang {choices[name]['threshold']:.4f}",
               xlabel="Prediksi", ylabel="Aktual")
    fig.savefig(directory / "test_confusion_matrices.png", dpi=160)
    plt.close(fig)

    fig, (pr, cal) = plt.subplots(1, 2, figsize=(11, 4.4), layout="constrained")
    pr.axhline(y.mean(), color="gray", linestyle="--", label="Prevalensi uji")
    cal.plot([0, 1], [0, 1], "--", color="gray", label="Ideal")
    for name, probability in probabilities.items():
        label = name.replace("_", " ")
        if name != BASELINE:
            precision, recall, _ = precision_recall_curve(y, probability)
            ap = scores.loc[scores.model == name, "average_precision"].iloc[0]
            pr.step(recall, precision, where="post", label=f"{label} (AP {ap:.3f})")
        bins = calibration_bins(y, probability)
        cal.plot([row["mean_probability"] for row in bins],
                 [row["positive_fraction"] for row in bins], marker="o", label=label)
    pr.set(xlabel="Recall", ylabel="Precision", xlim=(0, 1), ylim=(0, 1), title="Precision–recall")
    cal.set(xlabel="Rata-rata probabilitas", ylabel="Proporsi positif aktual",
            xlim=(0, 1), ylim=(0, 1), title="Reliabilitas probabilitas")
    for ax in (pr, cal):
        ax.legend(fontsize=8)
    fig.savefig(directory / "test_pr_and_calibration.png", dpi=160)
    plt.close(fig)


def formatted_table(frame, columns):
    view = frame[columns].copy()
    for column in view.select_dtypes(include="floating"):
        view[column] = view[column].map(lambda value: f"{value:.4f}" if pd.notna(value) else "—")
    return md_table(view)


def evaluate(data, output):
    lock = output / "protocol.json"
    protocol = json.loads(lock.read_text(encoding="utf-8"))
    if protocol["artifact_hashes"] != artifact_hashes(data):
        raise ValueError("Artefak Week 11 berubah setelah protokol dikunci.")
    target = output / "test"
    if target.exists():
        raise FileExistsError(f"Hasil uji sudah tersimpan di {target}. Gunakan output baru untuk reproduksi.")
    choices = protocol["models"]
    ids = {name: pd.read_csv(data / f"ids_{name}.csv", dtype=str)
           for name in ("train", "validation", "test")}
    patients = {name: set(frame.patient_nbr) for name, frame in ids.items()}
    if (patients["test"] & (patients["train"] | patients["validation"])
            or patients["train"] & patients["validation"]):
        raise ValueError("Pasien tumpang tindih antarset.")
    y = pd.read_csv(data / "y_test.csv").target.to_numpy()
    frame = pd.read_csv(data / "X_test.csv", usecols=["age", "number_inpatient"])
    if len(y) != len(ids["test"]) or len(y) != len(frame) or not ids["test"].encounter_id.is_unique:
        raise ValueError("ID, target, dan fitur uji tidak sejajar.")
    probabilities = predict(data, "test")
    scores = pd.DataFrame([
        {"model": name, "policy": policy, "threshold": threshold, **binary_metrics(y, probability, threshold)}
        for name, probability in probabilities.items()
        for policy, threshold in ([("locked", choices[name]["threshold"])] if name == BASELINE
                                  else [("locked", choices[name]["threshold"]), ("reference_0_5", 0.5)])
    ])
    errors = error_groups(frame, y, probabilities, choices)
    prior = errors[errors.variable == "number_inpatient"]
    if any(int(group.n.sum()) != len(y) for _, group in prior.groupby("model")):
        raise ValueError("Kelompok riwayat rawat inap tidak mencakup seluruh set uji.")
    validation = pd.DataFrame([{"model": name, "threshold": info["threshold"],
                                "f1_at_0_5": info["validation_at_0_5"]["f1"],
                                **info["validation_at_locked_threshold"]} for name, info in choices.items()])
    selected = scores[(scores.model == protocol["primary_model"]) & (scores.policy == "locked")].iloc[0]
    other = scores[(scores.model != protocol["primary_model"]) & (scores.model != BASELINE)
                   & (scores.policy == "locked")].iloc[0]
    prior_selected = prior[prior.model == protocol["primary_model"]].set_index("group")
    group_summary = []
    if {"0", "2+"} <= set(prior_selected.index) and prior_selected.loc[["0", "2+"], "recall"].notna().all():
        group_summary = [
            f"Recall {selected.model} adalah **{prior_selected.loc['0', 'recall']:.2%}** pada kelompok tanpa "
            f"riwayat rawat inap dan **{prior_selected.loc['2+', 'recall']:.2%}** pada kelompok dengan dua atau lebih. "
            f"Kelompok tanpa riwayat menyumbang **{prior_selected.loc['0', 'fn']:,}** dari "
            f"**{selected.fn:,}** kasus positif yang terlewat.", "",
        ]
    with TemporaryDirectory(dir=output, prefix=".test-") as temporary:
        staged = Path(temporary) / "test"
        staged.mkdir()
        scores.to_csv(staged / "metrics.csv", index=False)
        errors.to_csv(staged / "error_groups.csv", index=False)
        pd.DataFrame([{"model": name, **row} for name, probability in probabilities.items()
                      for row in calibration_bins(y, probability)]).to_csv(staged / "calibration.csv", index=False)
        write_json(staged / "evaluation.json", {
            "set": "test", "encounters": len(y), "patients": len(patients["test"]),
            "positives": int(y.sum()), "patient_overlap": 0, "protocol_sha256": sha(lock),
            "input_hashes": {name: sha(data / name) for name in ("X_test.npz", "X_test.csv", "y_test.csv", "ids_test.csv")},
        })
        plot_results(staged, scores, y, probabilities, choices)
        report = [
            "# Week 12 — Evaluasi pada set uji", "",
            f"Target positif: rawat inap ulang dalam <30 hari. Set uji memuat {len(y):,} kunjungan dari "
            f"{len(patients['test']):,} pasien, dengan {int(y.sum()):,} kasus positif ({y.mean():.2%}). "
            "Tidak ada pasien yang tumpang tindih antarset.", "",
            "## Pemilihan pada validation", "",
            "Model dan preprocessing Week 11 dipertahankan. Ambang kedua model dipilih untuk "
            "memaksimalkan F1 kelas positif pada validation. Jika seri, dipilih ambang tertinggi. "
            "Dummy prior tetap pada 0,5. Tidak ada fit ulang atau tuning hiperparameter.", "",
            formatted_table(validation, ["model", "threshold", "f1_at_0_5", "f1", "precision", "recall", "average_precision"]), "",
            f"Model utama ditetapkan dari AP validation: **{protocol['primary_model']}**. "
            "Pilihan dan hash artefak disimpan di [protokol](../protocol.json) sebelum set uji dibaca.", "",
            "## Hasil pada set uji", "",
            "`locked` memakai ambang dari validation. `reference_0_5` adalah pembanding tetap Week 11. "
            "Perubahan ambang memengaruhi label prediksi, sementara AP, ROC-AUC, Brier dan log loss memakai probabilitas yang sama.", "",
            formatted_table(scores, ["model", "policy", "threshold", "precision", "recall", "f1", "average_precision", "roc_auc", "brier_score", "log_loss"]), "",
            f"Pada ambang terkunci, model utama menangkap **{selected.tp:,} dari {int(y.sum()):,}** kasus positif "
            f"dan menghasilkan **{selected.fp:,}** peringatan salah. Sebanyak **{selected.fn:,}** kasus positif terlewat.", "",
            f"{other.model} menangkap **{other.tp:,}** kasus positif dan menghasilkan **{other.fp:,}** "
            "peringatan salah.", "",
            "![Matriks kebingungan set uji](test_confusion_matrices.png)", "",
            "![Kurva precision–recall dan reliabilitas probabilitas](test_pr_and_calibration.png)", "",
            "## Analisis kesalahan", "",
            "Kelompok berikut memakai jumlah rawat inap dalam tahun sebelum kunjungan indeks. "
            "Perbandingan deskriptif per kelompok memakai ambang yang sama untuk tiap model.", "",
            formatted_table(prior, ["model", "group", "n", "positives", "fp", "fn", "recall", "precision"]), "",
            *group_summary,
            "Rincian per rentang usia dan riwayat rawat inap tersedia di [CSV analisis](error_groups.csv). "
            "Kelompok kecil memiliki estimasi yang mudah berubah. Hasil berasal dari satu pembagian pasien, "
            "dihitung per kunjungan, dan belum mengukur performa lintas rumah sakit, waktu, atau pemakaian klinis.", "",
        ]
        (staged / "report.md").write_text("\n".join(report), encoding="utf-8")
        staged.rename(target)
    return scores


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["freeze", "evaluate"])
    parser.add_argument("--data", type=Path, default=ROOT / "data/processed/diabetes")
    parser.add_argument("--week11", type=Path, default=ROOT / "results/week-11")
    parser.add_argument("--output", type=Path, default=ROOT / "results/week-12")
    args = parser.parse_args()
    if args.stage == "freeze":
        result = freeze(args.data, args.output, args.week11)
        print("Protokol terkunci:", result["primary_model"])
    else:
        print(evaluate(args.data, args.output)[["model", "policy", "threshold", "f1", "average_precision"]].to_string(index=False))


if __name__ == "__main__":
    main()
