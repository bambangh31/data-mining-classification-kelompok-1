import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
from scipy import sparse

from src.mining import binary_metrics, make_feature_adapter, calibration_bins, positive_probability


class BinaryMetricsTests(unittest.TestCase):
    def test_perfect_ranking_and_classification(self):
        scores = binary_metrics([0, 1, 0, 1], [0.1, 0.8, 0.2, 0.9])
        for key in ["accuracy", "precision", "recall", "f1", "roc_auc", "average_precision"]:
            self.assertEqual(scores[key], 1.)
        self.assertEqual((scores["tn"], scores["fp"], scores["fn"], scores["tp"]), (2, 0, 0, 2))
        self.assertAlmostEqual(scores["brier_score"], 0.025)
        self.assertGreater(scores["log_loss"], 0)

    def test_majority_accuracy_is_not_positive_class_performance(self):
        scores = binary_metrics([0, 0, 0, 1], [0., 0., 0., 0.])
        self.assertEqual(scores["accuracy"], 0.75)
        self.assertEqual(scores["recall"], 0.)
        self.assertEqual(scores["f1"], 0.)
        self.assertEqual(scores["average_precision"], 0.25)
        self.assertEqual(scores["roc_auc"], 0.5)

    def test_invalid_probabilities_are_rejected(self):
        for scores in [[0.1], [0.1, float("nan")], [0.1, 1.1]]:
            with self.assertRaises(ValueError):
                binary_metrics([0, 1], scores)

    def test_adapter_does_not_refit_on_validation(self):
        x = sparse.csr_matrix(np.random.default_rng(42).normal(size=(30, 8)))
        adapter = make_feature_adapter(x, components=3)
        components = adapter[0].components_.copy()
        mean = adapter[1].mean_.copy()
        actual = adapter.transform(sparse.csr_matrix(np.ones((5, 8)) * 100))
        self.assertEqual(actual.shape, (5, 3))
        np.testing.assert_array_equal(components, adapter[0].components_)
        np.testing.assert_array_equal(mean, adapter[1].mean_)
        self.assertTrue(np.isfinite(actual).all())

    def test_calibration_bins_keep_zero_and_one_and_counts(self):
        bins = calibration_bins([0, 0, 1, 1], [0., .05, .9, 1.])
        self.assertEqual(sum(row["count"] for row in bins), 4)
        self.assertEqual(bins[0]["count"], 2)
        self.assertEqual(bins[-1]["count"], 2)
        self.assertEqual(bins[-1]["positive_fraction"], 1.)

    def test_new_models_produce_valid_binary_probabilities(self):
        from sklearn.datasets import make_classification
        from src.mining import make_models
        x, y = make_classification(n_samples=80, n_features=6, n_informative=3, random_state=42)
        for name, model in make_models().items():
            if name != "Dummy_prior":
                model.set_params(n_estimators=2)
            if name == "Rotation_Forest":
                model.set_params(n_jobs=1)
            model.fit(x[:60], y[:60])
            probability = positive_probability(model, x[60:])
            self.assertEqual(probability.shape, (20,))
            self.assertTrue(np.isfinite(probability).all())
            self.assertTrue(((probability >= 0) & (probability <= 1)).all())

    def test_complete_run_exports_metrics_without_any_test_files(self):
        from sklearn.datasets import make_classification
        from src.mining import make_models, run
        x, y = make_classification(n_samples=80, n_features=8, n_informative=4, random_state=42)
        models = make_models()
        for name, model in models.items():
            if name != "Dummy_prior":
                model.set_params(n_estimators=2)
            if name == "Rotation_Forest":
                model.set_params(n_jobs=1)
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            data.mkdir()
            for name, start, end in [("train", 0, 60), ("validation", 60, 80)]:
                sparse.save_npz(data / f"X_{name}.npz", sparse.csr_matrix(x[start:end]))
                pd.DataFrame({"target": y[start:end]}).to_csv(data / f"y_{name}.csv", index=False)
                pd.DataFrame({"patient_nbr": range(start, end)}).to_csv(data / f"ids_{name}.csv", index=False)
            (data / "metadata.json").write_text(json.dumps({"target_mode": "binary", "raw_csv_sha256": "synthetic"}))
            with patch("src.mining.make_models", return_value=models):
                table = run(data, Path(tmp) / "reports")
            self.assertEqual(set(table.model), {"Dummy_prior", "NGBoost", "Rotation_Forest"})
            report = json.loads((Path(tmp) / "reports/experiment.json").read_text())
            self.assertIs(report["test_evaluated"], False)
            self.assertTrue((Path(tmp) / "reports/validation_calibration.png").exists())


if __name__ == "__main__":
    unittest.main()
