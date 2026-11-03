"""Pengujian kebocoran pasien, target, dan statistik transformasi."""

import unittest

import numpy as np
import pandas as pd

from src.preprocess import NUMERIC, build_transformer, clean_data, make_target, split_patients


class PreprocessingTests(unittest.TestCase):
    def test_patient_split_is_disjoint_complete_and_reproducible(self):
        data = pd.DataFrame({"patient_nbr": np.repeat(np.arange(100), 3)})
        splits = split_patients(data)
        repeated = split_patients(data)
        self.assertEqual(sorted(np.concatenate(list(splits.values())).tolist()), list(range(300)))
        groups = {name: set(data.iloc[idx].patient_nbr) for name, idx in splits.items()}
        self.assertFalse(groups["train"] & groups["validation"])
        self.assertFalse(groups["train"] & groups["test"])
        self.assertFalse(groups["validation"] & groups["test"])
        for name in splits:
            np.testing.assert_array_equal(splits[name], repeated[name])

    def test_transform_does_not_learn_from_validation(self):
        train = pd.DataFrame({"num_medications": [1., 3., np.nan],
                              "race": ["A", "B", np.nan], "weight": [np.nan] * 3,
                              "constant": ["No"] * 3})
        transformer, info = build_transformer(train, min_frequency=1)
        transformer.fit(train)
        transformed = transformer.transform(pd.DataFrame({
            "num_medications": [1000., np.nan], "race": ["NEW", "A"],
            "weight": ["heavy", "light"], "constant": ["Yes", "Yes"]}))
        imputer = transformer.named_transformers_["numeric"].named_steps["imputer"]
        self.assertEqual(imputer.statistics_[0], 2.)
        self.assertEqual(info["dropped_over_50_percent_missing_train"], ["weight"])
        self.assertEqual(info["dropped_constant_train"], ["constant"])
        self.assertNotIn("NEW", transformer.named_transformers_["categorical"].named_steps["encoder"].categories_[0])
        self.assertTrue(np.isfinite(transformed.data).all())

    def test_cleaning_preserves_lab_none_and_valid_targets(self):
        raw = pd.DataFrame({name: ["1", "1", "1"] for name in NUMERIC})
        raw = raw.assign(encounter_id=["1", "2", "3"], patient_nbr=["10", "11", "12"],
                         readmitted=["NO", ">30", "<30"], gender=["Male", "Unknown/Invalid", "Female"],
                         admission_type_id=["1", "6", "1"], discharge_disposition_id=["1", "1", "11"],
                         admission_source_id=["7", "17", "7"], race=["?", "Asian", "Asian"],
                         A1Cresult=["None", "Norm", ">8"])
        cleaned, report = clean_data(raw)
        self.assertEqual(len(cleaned), 2)
        self.assertEqual(report["death_discharge_rows_removed"], 1)
        self.assertEqual(cleaned.loc[0, "A1Cresult"], "None")
        self.assertTrue(pd.isna(cleaned.loc[0, "race"]))
        self.assertTrue(pd.isna(cleaned.loc[1, "gender"]))
        self.assertTrue(pd.isna(cleaned.loc[1, "admission_source_id"]))
        self.assertEqual(make_target(cleaned, "binary").tolist(), [0, 0])
        self.assertEqual(make_target(raw, "binary").tolist(), [0, 0, 1])
        self.assertEqual(make_target(raw, "multiclass").tolist(), [0, 1, 2])

    def test_conflicting_encounter_ids_fail_instead_of_arbitrary_drop(self):
        raw = pd.DataFrame({name: ["1", "2"] for name in NUMERIC})
        raw = raw.assign(encounter_id=["1", "1"], patient_nbr=["10", "10"],
                         readmitted=["NO", "<30"], gender=["Male", "Male"],
                         admission_type_id=["1", "1"], discharge_disposition_id=["1", "1"],
                         admission_source_id=["7", "7"])
        with self.assertRaisesRegex(ValueError, "encounter_id"):
            clean_data(raw)


if __name__ == "__main__":
    unittest.main()
