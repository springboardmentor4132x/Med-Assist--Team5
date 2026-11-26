"""Input/output models (Pydantic v2)."""
import math
from datetime import datetime
from typing import Any, List, Literal, Optional, Union

from pydantic import (
    BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, field_validator,
)

from .constants import RiskCategory


class RiskCategorizationInput(BaseModel):
    # Unknown fields from other members' modules are ignored, not fatal.
    model_config = ConfigDict(extra="ignore")

    user_id: Optional[str] = None
    assessment_id: Optional[str] = None
    # Strict numeric: rejects strings ("65") and booleans.
    risk_score: Union[StrictInt, StrictFloat]
    # Raw string; normalized in rules.normalize_severity (unknown -> ignored + noted).
    severity_level: Optional[str] = None
    # Required and strict on purpose: an emergency flag must never be defaulted
    # or inferred from a string like "false"/"yes".
    emergency_flag: StrictBool
    predicted_disease: Optional[str] = None
    symptoms: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    assessment_timestamp: Optional[datetime] = None

    @field_validator("risk_score")
    @classmethod
    def _score_in_range(cls, v: Union[int, float]) -> Union[int, float]:
        if not math.isfinite(v) or not (0 <= v <= 100):
            raise ValueError("risk_score must be a number between 0 and 100")
        return v

    @field_validator("user_id", "assessment_id", "predicted_disease", mode="before")
    @classmethod
    def _clean_text(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        if isinstance(v, bool) or not isinstance(v, (str, int)):
            raise ValueError("must be a string")
        v = str(v).strip()
        return v or None

    @field_validator("severity_level", mode="before")
    @classmethod
    def _clean_severity(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        v = str(getattr(v, "value", v)).strip().upper()
        return v or None

    @field_validator("symptoms", "risk_factors", mode="before")
    @classmethod
    def _clean_list(cls, v: Any) -> List[str]:
        if v is None:
            return []
        if not isinstance(v, (list, tuple)):
            raise ValueError("must be a list of strings")
        out: List[str] = []
        for item in v:
            if not isinstance(item, str):
                raise ValueError("list items must be strings")
            item = " ".join(item.split()).lower()
            if item and item not in out:
                out.append(item)
        return out


class RiskCategorizationResult(BaseModel):
    assessment_id: Optional[str] = None
    user_id: Optional[str] = None
    risk_score: Union[int, float]
    severity_level: Optional[RiskCategory] = None  # None if missing/unrecognized
    risk_category: RiskCategory
    category_label: str
    category_color: str
    category_color_hex: str
    determining_factor: str
    emergency_flag: bool
    emergency_alert: Optional[str] = None
    explanation: str
    contributing_factors: List[str]
    urgency_guidance: str
    is_medical_diagnosis: Literal[False] = False
    thresholds_clinically_validated: Literal[False] = False
    disclaimer: str
