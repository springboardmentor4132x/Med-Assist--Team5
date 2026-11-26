"""Risk Categorization (Module 4, Member 4) - MedAssist AI.

Usage:  from risk_categorization import categorize_risk
Imports are lazy so the pure rules (constants/rules) work without Pydantic.
"""
__all__ = ["categorize_risk", "RiskCategorizationInput", "RiskCategorizationResult"]


def __getattr__(name):
    if name == "categorize_risk":
        from .service import categorize_risk
        return categorize_risk
    if name in ("RiskCategorizationInput", "RiskCategorizationResult"):
        from . import schemas
        return getattr(schemas, name)
    raise AttributeError(name)
