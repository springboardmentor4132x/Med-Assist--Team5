
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class PatientSymptom(Base):
    __tablename__ = "patient_symptoms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
    Integer,
    ForeignKey("users.id"),
    nullable=True
)
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
    created_at = Column(DateTime, default=datetime.utcnow)


class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token_hash = Column(String(64), unique=True, nullable=False)
    revoked_at = Column(DateTime, default=datetime.utcnow)
