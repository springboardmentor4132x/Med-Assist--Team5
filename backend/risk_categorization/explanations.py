"""Human-readable text. Wording is driven by the actual decision."""
from typing import List, Optional

from .constants import SCORE_RANGE_TEXT, DeterminingFactor, RiskCategory
from .rules import CategoryDecision

_BASE = {
    RiskCategory.LOW: (
        "The provided risk score and severity level indicate a lower estimated "
        "risk under the project's categorization rules."
    ),
    RiskCategory.MODERATE: (
        "The risk score or severity falls within the moderate range, indicating "
        "that medical evaluation may be appropriate depending on symptoms and "
        "their progression."
    ),
    RiskCategory.HIGH: (
        "The risk score or reported severity indicates a higher estimated risk. "
        "Professional medical evaluation is recommended promptly."
    ),
    RiskCategory.CRITICAL: (
        "The score or severity indicates a critical estimated risk. Immediate "
        "medical evaluation is recommended."
    ),
}

_GUIDANCE = {
    RiskCategory.LOW: (
        "Monitor your symptoms. Consult a healthcare professional if they persist, "
        "worsen, or you are concerned."
    ),
    RiskCategory.MODERATE: (
        "Consider arranging a medical evaluation soon, especially if symptoms "
        "continue or worsen."
    ),
    RiskCategory.HIGH: "Seek prompt medical evaluation from a qualified healthcare professional.",
    RiskCategory.CRITICAL: "Seek immediate medical evaluation from a qualified healthcare professional.",
}

EMERGENCY_ALERT = (
    "A potentially critical warning condition was identified. Seek immediate "
    "emergency medical attention. Do not delay care while waiting for an AI result."
)
_EMERGENCY_GUIDANCE = (
    "Seek immediate emergency medical attention: contact your local emergency "
    "number or go to the nearest emergency department now."
)


def build_emergency_alert(decision: CategoryDecision) -> Optional[str]:
    return EMERGENCY_ALERT if decision.emergency else None


def build_explanation(decision: CategoryDecision, severity_unrecognized: bool = False) -> str:
    if decision.emergency:
        text = (
            EMERGENCY_ALERT
            + " The emergency warning takes priority over the numerical risk score."
        )
    else:
        text = _BASE[decision.category]
        if decision.determining_factor is DeterminingFactor.SEVERITY:
            text += (
                f" The reported severity ({decision.severity_category.value}) set a "
                "higher minimum category than the risk score alone."
            )
    if severity_unrecognized:
        text += " The severity value was not recognized and was not used."
    return text


def build_urgency_guidance(decision: CategoryDecision) -> str:
    return _EMERGENCY_GUIDANCE if decision.emergency else _GUIDANCE[decision.category]


def build_contributing_factors(
    decision: CategoryDecision,
    score: float,
    severity_unrecognized: bool,
    symptoms: List[str],
    risk_factors: List[str],
) -> List[str]:
    f: List[str] = []
    if decision.emergency:
        f.append("Emergency flag was triggered (overrides score and severity)")
    f.append(
        f"Risk score {score:g} is within the {decision.score_category.value.lower()}"
        f"-risk score range ({SCORE_RANGE_TEXT[decision.score_category]})"
    )
    if decision.severity_category is not None:
        f.append(f"Severity level is {decision.severity_category.value}")
    elif severity_unrecognized:
        f.append("Severity level was not recognized and was ignored")
    else:
        f.append("No severity level was provided")
    # Context only: these never change the category.
    if symptoms:
        f.append("Reported symptoms (context only): " + ", ".join(symptoms))
    if risk_factors:
        f.append("Reported risk factors (context only): " + ", ".join(risk_factors))
    return f
