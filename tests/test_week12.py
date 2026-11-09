import tempfile
import unittest
from pathlib import Path

from src.week12 import choose_threshold, evaluate


class Week12Tests(unittest.TestCase):
    def test_uses_highest_threshold_when_f1_ties(self):
        # Predicting four positives (two correct) ties predicting one correct positive.
        threshold, candidates = choose_threshold([1, 0, 0, 1], [0.9, 0.8, 0.7, 0.6])
        self.assertEqual(threshold, 0.9)
        self.assertEqual(candidates, 4)

    def test_keeps_equal_scores_together(self):
        threshold, candidates = choose_threshold([1, 0, 1, 0], [0.2, 0.2, 0.2, 0.1])
        self.assertEqual(threshold, 0.2)
        self.assertEqual(candidates, 2)

    def test_evaluate_requires_lock_before_loading_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(FileNotFoundError) as raised:
                evaluate(root / "absent_data", root / "output")
            self.assertEqual(Path(raised.exception.filename).name, "protocol.json")
