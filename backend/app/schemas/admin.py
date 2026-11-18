from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.auth import UserResponse

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class StatusUpdateRequest(BaseModel):
    is_active: bool

class RoleUpdateRequest(BaseModel):
    role_name: str

class RoleDistribution(BaseModel):
    role: str
    count: int
    percentage: float

class DashboardStatsResponse(BaseModel):
    total_users: int
    total_patients: int
    total_doctors: int
    total_clinics: int
    total_admins: int
    active_accounts: int
    inactive_accounts: int
    role_distribution: List[RoleDistribution]
    recent_registrations: List[UserResponse]

class UserDetailResponse(UserResponse):
    patient_profile: Optional[Dict[str, Any]] = None
    doctor_profile: Optional[Dict[str, Any]] = None
    clinic_profile: Optional[Dict[str, Any]] = None

class AdminProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None

class PaginatedUsersResponse(BaseModel):
    items: List[UserResponse]
    total: int
    page: int
    limit: int
    total_pages: int
