import unittest

from src.mining import binary_metrics


class BinaryMetricsTests(unittest.TestCase):
    def test_perfect_ranking_and_classification(self):
        scores = binary_metrics([0, 1, 0, 1], [0.1, 0.8, 0.2, 0.9])
        for key in ["accuracy", "precision", "recall", "f1", "roc_auc", "average_precision"]:
            self.assertEqual(scores[key], 1.)
        self.assertEqual((scores["tn"], scores["fp"], scores["fn"], scores["tp"]), (2, 0, 0, 2))

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


if __name__ == "__main__":
    unittest.main()
