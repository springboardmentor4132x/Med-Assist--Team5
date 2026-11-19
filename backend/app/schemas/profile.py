from datetime import datetime
from typing import Optional
from enum import Enum
import re

from pydantic import BaseModel, Field, field_validator, ConfigDict


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


class ProfileUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=125)
    gender: Optional[str] = None
    contact_number: Optional[str] = Field(None, max_length=25)
    address: Optional[str] = Field(None, max_length=255)
    blood_group: Optional[str] = Field(None, max_length=10)
    emergency_contact: Optional[str] = Field(None, max_length=25)

    model_config = ConfigDict(extra="forbid")

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value):
        if value is not None:
            value = value.strip()
            if value not in [item.value for item in GenderEnum]:
                raise ValueError("Invalid gender")
        return value

    @field_validator("blood_group")
    @classmethod
    def validate_blood_group(cls, value):
        if value is not None:
            value = value.strip().upper()
            if value not in [item.value for item in BloodGroupEnum]:
                raise ValueError("Invalid blood group")
        return value

    @field_validator("contact_number", "emergency_contact")
    @classmethod
    def validate_phone(cls, value):
        if value is not None:
            value = value.strip()
            if not PHONE_REGEX.fullmatch(value):
                raise ValueError("Invalid phone number")
        return value


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    email: str
    age: Optional[int] = None
    gender: Optional[str] = None
    contact_number: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None
    emergency_contact: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)