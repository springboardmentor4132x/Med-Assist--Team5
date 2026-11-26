import unittest

from backend.services.severity_evaluator import evaluate_severity


class TestSeverityEvaluator(unittest.TestCase):

    def test_non_string_symptom_raises_error(self):
        with self.assertRaises(ValueError):
            evaluate_severity(["fever", 123], 1)

    def test_blank_symptom_raises_error(self):
        with self.assertRaises(ValueError):
            evaluate_severity(["fever", "   "], 1)

    def test_mild_severity(self):
        result = evaluate_severity(["fever"], 1)
        self.assertEqual(result["severity_level"], "Mild")

    def test_moderate_by_symptom_count(self):
        result = evaluate_severity(
            ["fever", "cough", "headache"], 2
        )
        self.assertEqual(result["severity_level"], "Moderate")

    def test_severe_by_symptom_count(self):
        result = evaluate_severity(
            ["fever", "cough", "headache", "fatigue", "nausea"], 2
        )
        self.assertEqual(result["severity_level"], "Severe")

    def test_moderate_by_duration(self):
        result = evaluate_severity(["fever"], 4)
        self.assertEqual(result["severity_level"], "Moderate")

    def test_severe_by_duration(self):
        result = evaluate_severity(["fever"], 7)
        self.assertEqual(result["severity_level"], "Severe")

    def test_empty_symptoms_raises_error(self):
        with self.assertRaises(ValueError):
            evaluate_severity([], 1)

    def test_zero_duration_raises_error(self):
        with self.assertRaises(ValueError):
            evaluate_severity(["fever"], 0)

    def test_duplicate_symptoms_count_once(self):
        result = evaluate_severity(["fever", "fever"], 1)
        self.assertEqual(result["symptom_count"], 1)
        self.assertEqual(result["severity_level"], "Mild")

    def test_symptom_names_are_normalized(self):
        result = evaluate_severity(
            [" Fever ", "fever", "COUGH"], 1
        )
        self.assertEqual(result["symptom_count"], 2)

    def test_non_list_symptoms_raises_error(self):
        with self.assertRaises(ValueError):
            evaluate_severity("fever", 1)

    def test_invalid_duration_type_raises_error(self):
        with self.assertRaises(ValueError):
            evaluate_severity(["fever"], "two")


if __name__ == "__main__":
    unittest.main()