from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.api.dependencies.auth import get_current_patient, AuthenticatedPatient
from backend.app.schemas.profile import ProfileResponse, ProfileUpdate
from backend.app.services.profile_service import PatientProfileService

router = APIRouter(prefix="/profile", tags=["Patient Profile Management"])


@router.get(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Current Patient Profile",
    description="Retrieve the profile details of the currently authenticated patient derived securely from the JWT token."
)
def get_my_profile(
    current_patient: AuthenticatedPatient = Depends(get_current_patient),
    db: Session = Depends(get_db)
) -> ProfileResponse:
    """
    Retrieve profile for the authenticated patient.
    Guarantees isolation: patient ID is extracted exclusively from the validated JWT token.
    """
    profile = PatientProfileService.get_or_initialize_profile(
        db=db,
        user_id=current_patient.user_id,
        email=current_patient.email
    )
    return profile


@router.patch(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Current Patient Profile",
    description="Update permitted profile fields (age, gender, contact number, address, blood group, emergency contact). Protected fields cannot be altered."
)
def update_my_profile(
    profile_update: ProfileUpdate,
    current_patient: AuthenticatedPatient = Depends(get_current_patient),
    db: Session = Depends(get_db)
) -> ProfileResponse:
    """
    Update permitted profile fields for the authenticated patient.
    Guarantees isolation: patient ID is extracted exclusively from the validated JWT token.
    """
    # Ensure profile exists or is initialized
    PatientProfileService.get_or_initialize_profile(
        db=db,
        user_id=current_patient.user_id,
        email=current_patient.email
    )

    updated_profile = PatientProfileService.update_profile(
        db=db,
        user_id=current_patient.user_id,
        profile_update=profile_update
    )
    return updated_profile
