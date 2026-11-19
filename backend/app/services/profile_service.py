from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend.app.models.profile import PatientProfile
from backend.app.schemas.profile import ProfileUpdate


class PatientProfileService:

    @staticmethod
    def get_profile_by_user_id(
        db: Session,
        user_id: int
    ) -> Optional[PatientProfile]:

        return db.query(PatientProfile).filter(
            PatientProfile.user_id == user_id
        ).first()

    @staticmethod
    def get_or_initialize_profile(
        db: Session,
        user_id: int,
        email: str,
        full_name: str
    ) -> PatientProfile:

        profile = PatientProfileService.get_profile_by_user_id(
            db, user_id
        )

        if profile:
            return profile

        new_profile = PatientProfile(
            user_id=user_id,
            email=email,
            full_name=full_name
        )

        try:
            db.add(new_profile)
            db.commit()
            db.refresh(new_profile)
            return new_profile

        except IntegrityError:
            db.rollback()

            existing = PatientProfileService.get_profile_by_user_id(
                db, user_id
            )

            if existing:
                return existing

            raise HTTPException(
                status_code=409,
                detail="Profile already exists or email is already registered."
            )

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def update_profile(
        db: Session,
        user_id: int,
        profile_update: ProfileUpdate
    ) -> PatientProfile:

        profile = PatientProfileService.get_profile_by_user_id(
            db, user_id
        )

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient profile not found."
            )

        update_data = profile_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(profile, field, value)

        try:
            db.commit()
            db.refresh(profile)
            return profile

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Failed to update patient profile."
            )