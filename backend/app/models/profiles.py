from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    date_of_birth = Column(String(50), nullable=True)
    gender = Column(String(20), nullable=True)
    emergency_contact = Column(String(50), nullable=True)
    blood_group = Column(String(10), nullable=True)

    user = relationship("User", back_populates="patient_profile")
    medical_histories = relationship("MedicalHistory", back_populates="patient", cascade="all, delete-orphan")

class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    specialization = Column(String(100), nullable=True)
    license_number = Column(String(100), nullable=True)
    years_of_experience = Column(Integer, default=0)

    user = relationship("User", back_populates="doctor_profile")

class ClinicProfile(Base):
    __tablename__ = "clinic_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    clinic_name = Column(String(150), nullable=True)
    address = Column(String(255), nullable=True)
    contact_number = Column(String(50), nullable=True)

    user = relationship("User", back_populates="clinic_profile")

class MedicalHistory(Base):
    __tablename__ = "medical_histories"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    diagnosis = Column(String(255), nullable=False)
    treatment_plan = Column(Text, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("PatientProfile", back_populates="medical_histories")
