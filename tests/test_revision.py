import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import joblib
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from ngboost import NGBClassifier

from src.profile_data import admin_code_dictionary
from src.revision import run
from src.revision_thresholds import run as compare_thresholds


class RevisionTests(unittest.TestCase):
    def test_mapping_keeps_column_specific_codes_and_zero_counts(self):
        raw = pd.DataFrame({"admission_type_id": ["1", "6"],
                            "discharge_disposition_id": ["11", "13"],
                            "admission_source_id": ["20", "7"]})
        mapping = Path(__file__).resolve().parents[1] / "data/raw/IDS_mapping.csv"
        table = admin_code_dictionary(raw, mapping).set_index(["kolom", "kode"])
        self.assertIn("meninggal", table.loc[("discharge_disposition_id", "20"), "perlakuan"])
        self.assertEqual(table.loc[("discharge_disposition_id", "20"), "jumlah_data_asli"], 0)
        self.assertEqual(table.loc[("admission_source_id", "20"), "perlakuan"], "Diubah menjadi missing")
        self.assertEqual(table.loc[("admission_type_id", "6"), "arti_sumber"], "NULL")
        self.assertEqual(table.loc[("discharge_disposition_id", "13"), "perlakuan"], "Dipertahankan sebagai kategori")

    def test_full_run_balances_only_train_without_test_files(self):
        x, y = make_classification(n_samples=100, n_features=8, n_informative=4,
                                   weights=[.8, .2], random_state=42)
        with tempfile.TemporaryDirectory() as temporary:
            data, output = Path(temporary) / "data", Path(temporary) / "results"
            data.mkdir()
            for name, start, end in [("train", 0, 75), ("validation", 75, 100)]:
                sparse.save_npz(data / f"X_{name}.npz", sparse.csr_matrix(x[start:end]))
                pd.DataFrame({"target": y[start:end]}).to_csv(data / f"y_{name}.csv", index=False)
                pd.DataFrame({"patient_nbr": range(start, end)}).to_csv(data / f"ids_{name}.csv", index=False)
            original_validation = (data / "X_validation.npz").read_bytes()
            (data / "metadata.json").write_text(json.dumps({"target_mode": "binary"}))
            models = {"Dummy_prior": DummyClassifier(strategy="prior"),
                      "NGBoost": NGBClassifier(n_estimators=2, random_state=42, verbose=False)}
            with patch("src.revision.make_models", return_value=models):
                table = run(data, output)
            experiment = json.loads((output / "experiment.json").read_text(encoding="utf-8"))
            self.assertFalse(experiment["test_evaluated"])
            counts = experiment["oversampling"]["after"]
            self.assertEqual(counts["0"], counts["1"])
            self.assertEqual(experiment["experiments"]["NGBoost"]["training_rows"], 75)
            self.assertFalse((data / "models_paper").exists())
            self.assertEqual(original_validation, (data / "X_validation.npz").read_bytes())
            self.assertEqual(set(table.model), {"Dummy_prior", "NGBoost", "NGBoost_ROS"})
            self.assertTrue((output / "class_balance.png").exists())
            sampler = joblib.load(data / "models_revision/oversampler.joblib")
            self.assertTrue((sampler.sample_indices_ < 75).all())
            self.assertEqual(len(np.unique(sampler.sample_indices_)), 75)
            predictions = pd.read_csv(data / "models_revision/validation_predictions_NGBoost_ROS.csv")
            self.assertEqual(len(predictions), 25)
            np.testing.assert_array_equal(predictions.y_true, y[75:])
            thresholds = pd.read_csv(output / "validation_threshold_metrics.csv")
            for name in ("NGBoost", "NGBoost_ROS"):
                pair = thresholds[thresholds.model == name].set_index("policy")
                self.assertGreaterEqual(pair.loc["selected_on_validation", "f1"],
                                        pair.loc["reference_0_5", "f1"])
                for metric in ("average_precision", "roc_auc", "brier_score", "log_loss"):
                    self.assertEqual(pair.loc["selected_on_validation", metric],
                                     pair.loc["reference_0_5", metric])
            selection = json.loads((output / "threshold_selection.json").read_text(encoding="utf-8"))
            self.assertFalse(selection["test_evaluated"])
            self.assertFalse(selection["refit"])
            self.assertEqual(selection["selected_on"], "validation")
            self.assertTrue((output / "threshold_report.md").exists())
            # Menolak prediksi yang bergeser terhadap target asli.
            predictions.loc[0, "y_true"] = 1 - predictions.loc[0, "y_true"]
            path = data / "models_revision/validation_predictions_NGBoost_ROS.csv"
            predictions.to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "tidak sejajar"):
                compare_thresholds(data, output)
            # Menolak skor lama yang tidak cocok dengan eksperimen sumber.
            predictions.loc[0, "y_true"] = y[75]
            predictions["probability"] = .99
            predictions.to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "berbeda dari eksperimen"):
                compare_thresholds(data, output)


if __name__ == "__main__":
    unittest.main()
