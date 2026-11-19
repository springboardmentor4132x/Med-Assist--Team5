from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.services.security import get_current_user, get_db
from backend.database.models import User

from backend.app.schemas.profile import ProfileResponse, ProfileUpdate
from backend.app.services.profile_service import PatientProfileService


router = APIRouter(
    prefix="/profile",
    tags=["Patient Profile Management"]
)


@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = PatientProfileService.get_or_initialize_profile(
        db=db,
        user_id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name
    )

    return profile


@router.patch("/me", response_model=ProfileResponse)
def update_my_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    PatientProfileService.get_or_initialize_profile(
        db=db,
        user_id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name
    )

    updated_profile = PatientProfileService.update_profile(
        db=db,
        user_id=current_user.id,
        profile_update=profile_update
    )

    return updated_profile