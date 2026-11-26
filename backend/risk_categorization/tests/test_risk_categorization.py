"""Service/schema tests. Require pydantic v2 + pytest."""
import pytest

pytest.importorskip("pydantic")
from pydantic import ValidationError  # noqa: E402

from risk_categorization.service import categorize_risk  # noqa: E402

BASE = {"risk_score": 65, "severity_level": "HIGH", "emergency_flag": False}


def run(**over):
    return categorize_risk({**BASE, **over})


def test_example_high():
    r = run(assessment_id="A1", symptoms=["Fever", " fever ", "Headache"])
    assert r.risk_category == "HIGH" and r.category_label == "High Risk"
    assert r.emergency_alert is None and r.is_medical_diagnosis is False
    assert "emergency" not in r.explanation.lower()
    assert any("fever, headache" in f for f in r.contributing_factors)


def test_emergency_overrides_low_score():
    r = run(risk_score=10, severity_level="LOW", emergency_flag=True)
    assert r.risk_category == "CRITICAL" and r.emergency_flag and r.emergency_alert
    assert r.determining_factor == "EMERGENCY"


def test_missing_and_unknown_severity():
    assert run(severity_level=None).risk_category == "HIGH"
    r = run(risk_score=20, severity_level="banana")
    assert r.risk_category == "LOW" and r.severity_level is None
    assert any("not recognized" in f for f in r.contributing_factors)


def test_disease_does_not_change_category():
    a = run(predicted_disease="Cancer", risk_score=10, severity_level="LOW")
    assert a.risk_category == "LOW"


@pytest.mark.parametrize("bad", [-1, 101, "65", True, None, float("nan")])
def test_bad_scores_rejected(bad):
    with pytest.raises(ValidationError):
        run(risk_score=bad)


@pytest.mark.parametrize("bad", ["false", "yes", 1, None])
def test_emergency_must_be_bool(bad):
    with pytest.raises(ValidationError):
        run(emergency_flag=bad)


def test_missing_emergency_flag_rejected():
    with pytest.raises(ValidationError):
        categorize_risk({"risk_score": 5})


def test_extra_fields_ignored_and_optionals_missing():
    r = categorize_risk({"risk_score": 5, "emergency_flag": False, "other_module_field": 1})
    assert r.risk_category == "LOW"
