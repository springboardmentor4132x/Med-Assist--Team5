from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from backend.database.models import Base


def utc_now():
    return datetime.now(timezone.utc)


class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
        index=True
    )

    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)

    age = Column(Integer, nullable=True)
    gender = Column(String(30), nullable=True)
    contact_number = Column(String(25), nullable=True)
    address = Column(String(255), nullable=True)
    blood_group = Column(String(10), nullable=True)
    emergency_contact = Column(String(25), nullable=True)

    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    def __repr__(self):
        return f"<PatientProfile(id={self.id}, user_id={self.user_id})>"