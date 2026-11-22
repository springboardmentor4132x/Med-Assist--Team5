
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class PatientSymptom(Base):
    __tablename__ = "patient_symptoms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(30))
    symptoms = Column(Text, nullable=False)
    duration_days = Column(Integer, nullable=False)
    blood_pressure = Column(String(30), nullable=True)
    cholesterol_level = Column(String(30), nullable=True)
    additional_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="patient", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token_hash = Column(String(64), unique=True, nullable=False)
    revoked_at = Column(DateTime, default=datetime.utcnow)


class DoctorPatientAssignment(Base):
    __tablename__ = "doctor_patient_assignments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    patient_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    assigned_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "patient_id",
            name="uq_doctor_patient_assignment",
        ),
    )

class ClinicDoctorAssignment(Base):
    __tablename__ = "clinic_doctor_assignments"

    id = Column(Integer, primary_key=True, index=True)

    clinic_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    doctor_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    assigned_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "clinic_id",
            "doctor_id",
            name="uq_clinic_doctor_assignment",
        ),
    )
