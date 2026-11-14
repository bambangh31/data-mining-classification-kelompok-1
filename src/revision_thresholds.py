"""Bandingkan ambang NGBoost dari prediksi validation revisi, tanpa training ulang."""

import argparse
import json

import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve

from src.mining import binary_metrics, plt
from src.preprocess import ROOT, write_json
from src.week12 import choose_threshold, formatted_table, sha


MODELS = ("Dummy_prior", "NGBoost", "NGBoost_ROS")


def run(data, output):
    experiment_path = output / "experiment.json"
    experiment = json.loads(experiment_path.read_text(encoding="utf-8"))
    if experiment["evaluation_set"] != "validation" or experiment["test_evaluated"]:
        raise ValueError("Eksperimen sumber harus mengevaluasi validation saja.")
    target_path = data / "y_validation.csv"
    y = pd.read_csv(target_path).target.to_numpy()
    model_dir = data / "models_revision"
    probabilities, choices, rows = {}, {}, []
    hashes = {"experiment.json": sha(experiment_path), "y_validation.csv": sha(target_path)}
    # Pastikan prediksi berasal dari eksperimen yang sama sebelum memilih ambang.
    for name in MODELS:
        path = model_dir / f"validation_predictions_{name}.csv"
        predictions = pd.read_csv(path)
        if not np.array_equal(predictions.y_true.to_numpy(), y):
            raise ValueError(f"Target validation {name} tidak sejajar dengan preprocessing.")
        probability = predictions.probability.to_numpy()
        original = binary_metrics(y, probability)
        expected = experiment["experiments"][name]["metrics"]
        if any(not np.isclose(value, expected[key], atol=1e-10, rtol=1e-8)
               for key, value in original.items()):
            raise ValueError(f"Prediksi {name} berbeda dari eksperimen sumber.")
        probabilities[name] = probability
        hashes[path.name] = sha(path)
        rows.append({"model": name, "set": "validation", "policy": "reference_0_5",
                     "threshold": .5, **original})
        if name == "Dummy_prior":
            continue
        threshold, candidates = choose_threshold(y, probability)
        scores = binary_metrics(y, probability, threshold)
        choices[name] = {"threshold": threshold, "candidate_count": candidates,
                         "validation_at_selected_threshold": scores}
        rows.append({"model": name, "set": "validation", "policy": "selected_on_validation",
                     "threshold": threshold, **scores})
    table = pd.DataFrame(rows)
    table.to_csv(output / "validation_threshold_metrics.csv", index=False)
    write_json(output / "threshold_selection.json", {
        "selected_on": "validation", "evaluated_on": "same validation used for selection",
        "test_evaluated": False, "refit": False,
        "rule": "maximize positive-class F1; prefer highest threshold on ties",
        "baseline_threshold": .5, "input_sha256": hashes, "models": choices,
    })
    selected = table[table.policy == "selected_on_validation"].set_index("model")
    ordinary, balanced = selected.loc["NGBoost"], selected.loc["NGBoost_ROS"]
    report = ["# Perbandingan ambang NGBoost dan NGBoost + oversampling", "",
              "Prediksi validation dari eksperimen revisi digunakan kembali tanpa training ulang. "
              "Target dibandingkan baris per baris dengan y_validation; metrik pada ambang 0,5 "
              "diverifikasi terhadap experiment.json. Fitur/target test tidak dibaca.", "",
              "## Aturan pemilihan", "",
              "Untuk setiap NGBoost, pilih ambang yang memaksimalkan F1 kelas positif pada validation. "
              "Jika F1 seri, pilih ambang tertinggi. Dummy prior tetap pada 0,5. Aturan yang sama "
              "diterapkan pada kedua model; ini bukan penyamaan nilai ambangnya.", "",
              "## Hasil pada validation", "",
              formatted_table(table, ["model", "policy", "threshold", "precision", "recall", "f1",
                                      "average_precision", "roc_auc", "brier_score", "log_loss",
                                      "tp", "fp", "fn", "tn"]), "",
              f"Sesudah pemilihan ambang, NGBoost biasa memperoleh F1 **{ordinary.f1:.4f}**, "
              f"precision **{ordinary.precision:.2%}**, recall **{ordinary.recall:.2%}** pada ambang "
              f"**{ordinary.threshold:.6f}**. NGBoost + ROS memperoleh F1 **{balanced.f1:.4f}**, "
              f"precision **{balanced.precision:.2%}**, recall **{balanced.recall:.2%}** pada ambang "
              f"**{balanced.threshold:.6f}**.", "",
              f"Selisih F1 (ROS dikurangi biasa) adalah **{balanced.f1 - ordinary.f1:+.4f}**. "
              f"NGBoost biasa menghasilkan {int(ordinary.tp):,} true positive dan {int(ordinary.fp):,} "
              f"false positive; ROS menghasilkan {int(balanced.tp):,} true positive dan "
              f"{int(balanced.fp):,} false positive.", "",
              "## Interpretasi dan batas kesimpulan", "",
              "Perubahan threshold mengubah label prediksi, precision, recall dan F1. "
              "AP, ROC-AUC, Brier score dan log loss tidak berubah karena probabilitasnya tetap sama. "
              "Bandingkan efek oversampling setelah kedua model sama-sama diberi kesempatan memilih ambang; "
              "recall 0 pada ambang 0,5 bukan berarti NGBoost biasa tidak mampu mendeteksi kasus positif.", "",
              "Angka selected_on_validation dihitung pada data yang juga dipakai memilih ambang, "
              "sehingga merupakan hasil pemilihan yang dapat optimistis, bukan estimasi uji independen. "
              "Selisih kecil pada satu split tidak membuktikan keunggulan umum atau signifikansi statistik. "
              "Oversampling sebelumnya hanya memberi perubahan AP kecil dan memperburuk Brier/log loss; "
              "pemilihan threshold tidak memperbaiki kalibrasi probabilitas.", "",
              "Ambang yang dipilih beserta hash sumber disimpan di threshold_selection.json. "
              "Data test Week 12 sudah pernah digunakan pada eksperimen terdahulu. "
              "Evaluasi lanjutan yang lebih kuat dapat memakai validasi silang berbasis pasien "
              "dengan pemilihan ambang di dalam fold pelatihan atau data eksternal yang belum digunakan.", "",
              "![Kurva precision–recall dan F1 terhadap ambang](validation_threshold_curves.png)", "",
              "## Reproduksi tanpa training ulang", "", "```powershell",
              ".\\.venv\\Scripts\\python.exe -m src.revision_thresholds", "```", "",
              "Jika prediksi lokal belum tersedia, jalankan python -m src.revision terlebih dahulu. "
              "Runner training tersebut juga menghasilkan perbandingan ambang ini.", "",
              "[Kembali ke laporan revisi](report.md)", ""]
    (output / "threshold_report.md").write_text("\n".join(report), encoding="utf-8")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), layout="constrained")
    axes[0].axhline(y.mean(), color="gray", linestyle="--", label="Prevalensi validation")
    for name in MODELS[1:]:
        probability = probabilities[name]
        precision, recall, thresholds = precision_recall_curve(y, probability)
        f1 = np.divide(2 * precision[:-1] * recall[:-1], precision[:-1] + recall[:-1],
                       out=np.zeros_like(thresholds), where=(precision[:-1] + recall[:-1]) > 0)
        row = selected.loc[name]
        axes[0].step(recall, precision, where="post", label=name)
        axes[0].scatter([row.recall], [row.precision], s=35)
        axes[1].plot(thresholds, f1, label=name)
        axes[1].scatter([row.threshold], [row.f1], s=35)
    axes[0].set(xlabel="Recall", ylabel="Precision", xlim=(0, 1), ylim=(0, 1))
    axes[1].set(xlabel="Threshold", ylabel="F1 kelas positif", xlim=(0, 1), ylim=(0, 1))
    for ax in axes:
        ax.legend(fontsize=8)
    fig.savefig(output / "validation_threshold_curves.png", dpi=160)
    plt.close(fig)
    return table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=type(ROOT), default=ROOT / "data/processed/diabetes")
    parser.add_argument("--output", type=type(ROOT), default=ROOT / "results/revisi-dosen")
    args = parser.parse_args()
    print(run(args.data, args.output)[["model", "policy", "threshold", "precision", "recall", "f1"]].to_string(index=False))


if __name__ == "__main__":
    main()
