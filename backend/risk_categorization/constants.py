"""Configuration for risk categorization.

IMPORTANT: thresholds are project DEMONSTRATION values, not clinically validated.
Change them here only; no other file hard-codes them.
"""
from enum import Enum
from typing import Dict, Tuple


class RiskCategory(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class DeterminingFactor(str, Enum):
    EMERGENCY = "EMERGENCY"
    SEVERITY = "SEVERITY"
    RISK_SCORE = "RISK_SCORE"
    RISK_SCORE_AND_SEVERITY = "RISK_SCORE_AND_SEVERITY"


# Higher number = higher risk. Final category is the max over all rules.
CATEGORY_PRIORITY: Dict[RiskCategory, int] = {
    RiskCategory.LOW: 0,
    RiskCategory.MODERATE: 1,
    RiskCategory.HIGH: 2,
    RiskCategory.CRITICAL: 3,
}

# Inclusive upper bounds, checked in order. 0-30 LOW, 31-60 MODERATE,
# 61-80 HIGH, 81-100 CRITICAL. Fractional scores (e.g. 30.5) fall into the
# next band up, so a score is never rounded down into a lower category.
SCORE_UPPER_BOUNDS: Tuple[Tuple[float, RiskCategory], ...] = (
    (30.0, RiskCategory.LOW),
    (60.0, RiskCategory.MODERATE),
    (80.0, RiskCategory.HIGH),
    (100.0, RiskCategory.CRITICAL),
)

SCORE_RANGE_TEXT: Dict[RiskCategory, str] = {
    RiskCategory.LOW: "0-30",
    RiskCategory.MODERATE: "31-60",
    RiskCategory.HIGH: "61-80",
    RiskCategory.CRITICAL: "81-100",
}

# Minimum final category implied by each severity level.
SEVERITY_MINIMUM_CATEGORY: Dict[RiskCategory, RiskCategory] = {
    RiskCategory.LOW: RiskCategory.LOW,
    RiskCategory.MODERATE: RiskCategory.MODERATE,
    RiskCategory.HIGH: RiskCategory.HIGH,
    RiskCategory.CRITICAL: RiskCategory.CRITICAL,
}

SEVERITY_ALIASES: Dict[str, str] = {"MEDIUM": "MODERATE"}

# Frontend metadata. Colour must not be the only cue: always show the label too.
CATEGORY_METADATA: Dict[RiskCategory, Dict[str, str]] = {
    RiskCategory.LOW: {"label": "Low Risk", "color": "green", "color_hex": "#2E7D32"},
    RiskCategory.MODERATE: {"label": "Moderate Risk", "color": "yellow", "color_hex": "#F9A825"},
    RiskCategory.HIGH: {"label": "High Risk", "color": "orange", "color_hex": "#EF6C00"},
    RiskCategory.CRITICAL: {"label": "Critical Risk", "color": "red", "color_hex": "#C62828"},
}

DISCLAIMER = (
    "This is an automated preliminary risk categorization and is not a medical "
    "diagnosis. Thresholds are project demonstration values and are not "
    "clinically validated."
)
