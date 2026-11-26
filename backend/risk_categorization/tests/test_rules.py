"""Pure-rule tests (unittest; no Pydantic needed)."""
import math
import unittest

from risk_categorization.constants import RiskCategory as C, DeterminingFactor as F
from risk_categorization.rules import determine_category, normalize_severity, score_to_category


class ScoreBands(unittest.TestCase):
    def test_boundaries(self):
        cases = {0: C.LOW, 30: C.LOW, 30.5: C.MODERATE, 31: C.MODERATE, 60: C.MODERATE,
                 61: C.HIGH, 80: C.HIGH, 81: C.CRITICAL, 100: C.CRITICAL}
        for score, cat in cases.items():
            self.assertEqual(score_to_category(score), cat, score)

    def test_invalid(self):
        for bad in (-1, 100.1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                score_to_category(bad)


class Severity(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize_severity(" high "), C.HIGH)
        self.assertEqual(normalize_severity("medium"), C.MODERATE)
        for v in (None, "", "  ", "banana", 5):
            self.assertIsNone(normalize_severity(v))


class Decisions(unittest.TestCase):
    def test_spec_examples(self):
        d = determine_category(25, C.LOW, True)
        self.assertEqual((d.category, d.emergency, d.determining_factor), (C.CRITICAL, True, F.EMERGENCY))
        self.assertEqual(determine_category(25, C.HIGH, False).category, C.HIGH)
        self.assertEqual(determine_category(50, C.LOW, False).category, C.MODERATE)
        self.assertEqual(determine_category(90, C.LOW, False).category, C.CRITICAL)

    def test_emergency_with_tiny_score(self):
        self.assertEqual(determine_category(10, None, True).category, C.CRITICAL)

    def test_severity_floors(self):
        self.assertEqual(determine_category(0, C.CRITICAL, False).category, C.CRITICAL)
        self.assertEqual(determine_category(5, C.MODERATE, False).category, C.MODERATE)
        self.assertEqual(determine_category(70, C.MODERATE, False).category, C.HIGH)  # never reduced

    def test_never_below_any_rule(self):
        order = list(C)
        for score in range(0, 101, 5):
            for sev in [None, *C]:
                for em in (True, False):
                    d = determine_category(score, sev, em)
                    floor = max(order.index(score_to_category(score)),
                                order.index(sev) if sev else 0,
                                3 if em else 0)
                    self.assertGreaterEqual(order.index(d.category), floor)

    def test_missing_severity_uses_score(self):
        d = determine_category(65, None, False)
        self.assertEqual((d.category, d.determining_factor), (C.HIGH, F.RISK_SCORE))


if __name__ == "__main__":
    unittest.main()
