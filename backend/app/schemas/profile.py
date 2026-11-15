from datetime import datetime
from typing import Optional
from enum import Enum
import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    PREFER_NOT_TO_SAY = "Prefer not to say"


class BloodGroupEnum(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


PHONE_REGEX = re.compile(r"^\+?[0-9\s\-()]{7,20}$")


class ProfileBase(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="Patient's full legal name")
    email: Optional[EmailStr] = Field(None, description="Patient's primary email address")
    age: Optional[int] = Field(None, ge=0, le=125, description="Patient's age in years (0 - 125)")
    gender: Optional[str] = Field(None, description="Gender (Male, Female, Other, Prefer not to say)")
    contact_number: Optional[str] = Field(None, max_length=25, description="Primary contact phone number")
    address: Optional[str] = Field(None, max_length=255, description="Residential mailing address")
    blood_group: Optional[str] = Field(None, max_length=10, description="Blood type (e.g. A+, O-, etc.)")
    emergency_contact: Optional[str] = Field(None, max_length=25, description="Emergency contact phone number")

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v_clean = v.strip()
        allowed = [g.value for g in GenderEnum]
        if v_clean not in allowed:
            raise ValueError(f"Invalid gender '{v}'. Must be one of: {', '.join(allowed)}")
        return v_clean

    @field_validator("blood_group")
    @classmethod
    def validate_blood_group(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v_clean = v.strip().upper()
        allowed = [bg.value for bg in BloodGroupEnum]
        if v_clean not in allowed:
            raise ValueError(f"Invalid blood group '{v}'. Must be one of: {', '.join(allowed)}")
        return v_clean

    @field_validator("contact_number", "emergency_contact")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v_clean = v.strip()
        if not PHONE_REGEX.match(v_clean):
            raise ValueError(f"Invalid phone number format '{v}'. Must contain 7 to 20 digits with optional + or dashes.")
        return v_clean


class ProfileCreate(ProfileBase):
    """Schema used during initial profile registration/creation."""
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class ProfileUpdate(ProfileBase):
    """
    Schema for PATCH /api/v1/profile/me.
    Only permitted profile fields are present.
    Protected fields such as user_id, role, or id are explicitly forbidden.
    """
    model_config = ConfigDict(extra="forbid")


class ProfileResponse(BaseModel):
    """Schema returned to the frontend representing the patient's profile."""
    id: int
    user_id: int
    full_name: str
    email: EmailStr
    age: Optional[int] = None
    gender: Optional[str] = None
    contact_number: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None
    emergency_contact: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
