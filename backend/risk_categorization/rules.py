"""Pure, dependency-free categorization rules (no Pydantic, no I/O)."""
from dataclasses import dataclass
from typing import Any, Optional

from .constants import (
    CATEGORY_PRIORITY,
    SCORE_UPPER_BOUNDS,
    SEVERITY_ALIASES,
    SEVERITY_MINIMUM_CATEGORY,
    DeterminingFactor,
    RiskCategory,
)


@dataclass(frozen=True)
class CategoryDecision:
    category: RiskCategory
    score_category: RiskCategory
    severity_category: Optional[RiskCategory]  # None if missing/unrecognized
    emergency: bool
    determining_factor: DeterminingFactor


def score_to_category(score: float) -> RiskCategory:
    """Map a 0-100 score to its band. Raises ValueError if out of range/NaN."""
    if not (0 <= score <= 100):  # also False for NaN
        raise ValueError(f"risk score must be between 0 and 100, got {score!r}")
    for upper, category in SCORE_UPPER_BOUNDS:
        if score <= upper:
            return category
    raise ValueError(f"no category for score {score!r}")  # unreachable


def normalize_severity(raw: Any) -> Optional[RiskCategory]:
    """Normalize a severity value. Returns None if missing or unrecognized.

    The caller can tell the two apart (raw is None/empty vs. not).
    """
    if raw is None:
        return None
    text = str(getattr(raw, "value", raw)).strip().upper()
    if not text:
        return None
    text = SEVERITY_ALIASES.get(text, text)
    try:
        return RiskCategory(text)
    except ValueError:
        return None


def highest(*categories: Optional[RiskCategory]) -> RiskCategory:
    """Highest-priority category among those given (None ignored)."""
    present = [c for c in categories if c is not None]
    return max(present, key=lambda c: CATEGORY_PRIORITY[c])


def determine_category(
    score: float, severity: Optional[RiskCategory], emergency: bool
) -> CategoryDecision:
    """Final category = highest required by emergency, severity, score.

    The result is never lower than any individual rule's requirement.
    """
    score_cat = score_to_category(score)
    sev_cat = SEVERITY_MINIMUM_CATEGORY[severity] if severity is not None else None

    if emergency is True:
        final = RiskCategory.CRITICAL
        factor = DeterminingFactor.EMERGENCY
    else:
        final = highest(score_cat, sev_cat)
        sev_p = CATEGORY_PRIORITY[sev_cat] if sev_cat is not None else -1
        score_p = CATEGORY_PRIORITY[score_cat]
        if sev_p > score_p:
            factor = DeterminingFactor.SEVERITY
        elif sev_p == score_p:
            factor = DeterminingFactor.RISK_SCORE_AND_SEVERITY
        else:
            factor = DeterminingFactor.RISK_SCORE

    return CategoryDecision(final, score_cat, sev_cat, emergency is True, factor)
