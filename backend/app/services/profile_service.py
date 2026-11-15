from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from backend.app.models.profile import PatientProfile
from backend.app.schemas.profile import ProfileUpdate, ProfileCreate


class PatientProfileService:
    """
    Business logic layer for Patient Profile Management.
    Ensures safe database transactions, input processing, and strict isolation.
    """

    @staticmethod
    def get_profile_by_user_id(db: Session, user_id: int) -> Optional[PatientProfile]:
        """
        Retrieves the profile record belonging strictly to user_id.
        """
        return db.query(PatientProfile).filter(PatientProfile.user_id == user_id).first()

    @staticmethod
    def get_or_initialize_profile(
        db: Session,
        user_id: int,
        email: str,
        full_name: Optional[str] = None
    ) -> PatientProfile:
        """
        Retrieves the existing patient profile.
        If no profile exists yet for this authenticated user (e.g. freshly registered via Member 1's auth),
        safely initializes a base profile for them using their token identity.
        """
        profile = PatientProfileService.get_profile_by_user_id(db, user_id)
        if profile:
            return profile

        # Initialize base profile
        initial_name = full_name if full_name else (email.split("@")[0].title() if email else "Patient User")
        new_profile = PatientProfile(
            user_id=user_id,
            email=email if email else f"patient_{user_id}@medassist.local",
            full_name=initial_name
        )
        try:
            db.add(new_profile)
            db.commit()
            db.refresh(new_profile)
            return new_profile
        except IntegrityError:
            db.rollback()
            # If created concurrently, return the existing one
            return PatientProfileService.get_profile_by_user_id(db, user_id)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to initialize patient profile: {str(e)}"
            )

    @staticmethod
    def update_profile(
        db: Session,
        user_id: int,
        profile_update: ProfileUpdate
    ) -> PatientProfile:
        """
        Updates permissible fields on the patient's own profile.
        Strictly prevents modifying user_id, id, role, or other patients' profiles.
        """
        profile = PatientProfileService.get_profile_by_user_id(db, user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient profile not found. Please ensure your account has an initialized profile."
            )

        update_data = profile_update.model_dump(exclude_unset=True)

        if not update_data:
            # Nothing to update, return existing profile
            return profile

        # Check unique constraint if email is being updated
        new_email = update_data.get("email")
        if new_email and new_email != profile.email:
            existing_email = db.query(PatientProfile).filter(
                PatientProfile.email == new_email,
                PatientProfile.user_id != user_id
            ).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Email address '{new_email}' is already in use by another account."
                )

        # Apply updates to permissible fields only
        for field, value in update_data.items():
            setattr(profile, field, value)

        try:
            db.commit()
            db.refresh(profile)
            return profile
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity violation while updating profile."
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error while saving profile updates: {str(e)}"
            )
