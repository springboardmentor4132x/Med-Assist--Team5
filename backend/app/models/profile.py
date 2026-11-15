from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from backend.app.core.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class PatientProfile(Base):
    """
    SQLAlchemy Model representing a Patient's Profile in MedAssist AI.
    Strictly restricted to Patient Profile Management fields.
    (Medical history and disease prediction features are isolated to other team modules).
    """
    __tablename__ = "patient_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)

    # Profile details
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(30), nullable=True)
    contact_number = Column(String(25), nullable=True)
    address = Column(String(255), nullable=True)
    blood_group = Column(String(10), nullable=True)
    emergency_contact = Column(String(25), nullable=True)

    # Auditing timestamps
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    def __repr__(self):
        return f"<PatientProfile(id={self.id}, user_id={self.user_id}, full_name='{self.full_name}')>"
