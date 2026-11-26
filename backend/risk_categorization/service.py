"""Main entry point. No database or network access."""
from typing import Any, Dict, Mapping, Union

from .constants import CATEGORY_METADATA, DISCLAIMER
from .explanations import (
    build_contributing_factors, build_emergency_alert,
    build_explanation, build_urgency_guidance,
)
from .rules import determine_category, normalize_severity
from .schemas import RiskCategorizationInput, RiskCategorizationResult


def categorize_risk(
    assessment_input: Union[RiskCategorizationInput, Mapping[str, Any]],
) -> RiskCategorizationResult:
    """Categorize risk from Member 1 (severity), 2 (score), 3 (emergency) outputs.

    Accepts a validated model or a plain dict. Raises pydantic.ValidationError
    on invalid input (FastAPI turns this into HTTP 422).
    """
    data = (
        assessment_input
        if isinstance(assessment_input, RiskCategorizationInput)
        else RiskCategorizationInput.model_validate(assessment_input)
    )

    severity = normalize_severity(data.severity_level)
    severity_unrecognized = data.severity_level is not None and severity is None
    decision = determine_category(data.risk_score, severity, data.emergency_flag)
    meta = CATEGORY_METADATA[decision.category]

    return RiskCategorizationResult(
        assessment_id=data.assessment_id,
        user_id=data.user_id,
        risk_score=data.risk_score,
        severity_level=severity,
        risk_category=decision.category,
        category_label=meta["label"],
        category_color=meta["color"],
        category_color_hex=meta["color_hex"],
        determining_factor=decision.determining_factor.value,
        emergency_flag=decision.emergency,
        emergency_alert=build_emergency_alert(decision),
        explanation=build_explanation(decision, severity_unrecognized),
        contributing_factors=build_contributing_factors(
            decision, data.risk_score, severity_unrecognized,
            data.symptoms, data.risk_factors,
        ),
        urgency_guidance=build_urgency_guidance(decision),
        disclaimer=DISCLAIMER,
    )


def categorize_risk_as_dict(assessment_input: Union[RiskCategorizationInput, Mapping[str, Any]]) -> Dict[str, Any]:
    """JSON-ready dict version for non-FastAPI callers."""
    return categorize_risk(assessment_input).model_dump(mode="json")
