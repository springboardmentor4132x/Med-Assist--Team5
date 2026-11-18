from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: str
    role_id: int
    is_active: bool
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role_name: str = "Patient"  # Default registration role
