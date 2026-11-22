
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.services.security import get_current_user, get_db
from backend.database.models import (
    User,
    PatientSymptom,
    DoctorPatientAssignment,
    ClinicDoctorAssignment,
)

router = APIRouter(prefix="/clinic", tags=["Clinic Management"])


# Verify that the logged-in account is a clinic
def get_current_clinic(
    current_user: User = Depends(get_current_user),
):
    if current_user.role.lower() != "clinic":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clinic access only",
        )
    return current_user


# 1. Clinic Dashboard Overview
@router.get("/dashboard")
def clinic_dashboard(
    db: Session = Depends(get_db),
    clinic: User = Depends(get_current_clinic),
):
    doctor_ids = db.query(
        ClinicDoctorAssignment.doctor_id
    ).filter(
        ClinicDoctorAssignment.clinic_id == clinic.id
    ).subquery()

    total_doctors = db.query(
        func.count(func.distinct(ClinicDoctorAssignment.doctor_id))
    ).filter(
        ClinicDoctorAssignment.clinic_id == clinic.id
    ).scalar() or 0

    total_patients = db.query(
        func.count(func.distinct(DoctorPatientAssignment.patient_id))
    ).join(
        ClinicDoctorAssignment,
        ClinicDoctorAssignment.doctor_id
        == DoctorPatientAssignment.doctor_id,
    ).filter(
        ClinicDoctorAssignment.clinic_id == clinic.id
    ).scalar() or 0

    return {
        "clinic": {
            "id": clinic.id,
            "name": clinic.full_name,
            "email": clinic.email,
        },
        "total_doctors": total_doctors,
        "total_patients": total_patients,
    }


# 2. Doctors associated with this clinic
@router.get("/doctors")
def clinic_doctors(
    db: Session = Depends(get_db),
    clinic: User = Depends(get_current_clinic),
):
    doctors = db.query(User).join(
        ClinicDoctorAssignment,
        ClinicDoctorAssignment.doctor_id == User.id,
    ).filter(
        ClinicDoctorAssignment.clinic_id == clinic.id,
        User.role == "doctor",
    ).order_by(User.id.desc()).all()

    return {
        "items": [
            {
                "id": doctor.id,
                "full_name": doctor.full_name,
                "email": doctor.email,
                "is_active": doctor.is_active,
                "created_at": doctor.created_at,
            }
            for doctor in doctors
        ],
        "total": len(doctors),
    }


# 3. Patients assigned to doctors of this clinic
@router.get("/patients")
def clinic_patients(
    db: Session = Depends(get_db),
    clinic: User = Depends(get_current_clinic),
):
    patients = db.query(
        User,
        DoctorPatientAssignment.doctor_id,
    ).join(
        DoctorPatientAssignment,
        DoctorPatientAssignment.patient_id == User.id,
    ).join(
        ClinicDoctorAssignment,
        ClinicDoctorAssignment.doctor_id
        == DoctorPatientAssignment.doctor_id,
    ).filter(
        ClinicDoctorAssignment.clinic_id == clinic.id,
        User.role == "patient",
    ).order_by(User.id.desc()).all()

    items = []
    seen = set()

    for patient, doctor_id in patients:
        if patient.id in seen:
            continue

        seen.add(patient.id)

        doctor = db.query(User).filter(
            User.id == doctor_id,
            User.role == "doctor",
        ).first()

        items.append({
            "id": patient.id,
            "full_name": patient.full_name,
            "email": patient.email,
            "is_active": patient.is_active,
            "assigned_doctor_id": doctor_id,
            "assigned_doctor_name": doctor.full_name if doctor else None,
        })

    return {
        "items": items,
        "total": len(items),
    }


# 4. Patient details – only within this clinic
@router.get("/patients/{patient_id}")
def clinic_patient_details(
    patient_id: int,
    db: Session = Depends(get_db),
    clinic: User = Depends(get_current_clinic),
):
    assignment = db.query(
        DoctorPatientAssignment
    ).join(
        ClinicDoctorAssignment,
        ClinicDoctorAssignment.doctor_id
        == DoctorPatientAssignment.doctor_id,
    ).filter(
        ClinicDoctorAssignment.clinic_id == clinic.id,
        DoctorPatientAssignment.patient_id == patient_id,
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Patient not found in this clinic",
        )

    patient = db.query(User).filter(
        User.id == patient_id,
        User.role == "patient",
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    doctor = db.query(User).filter(
        User.id == assignment.doctor_id,
        User.role == "doctor",
    ).first()

    records = db.query(PatientSymptom).filter(
        PatientSymptom.user_id == patient_id
    ).order_by(
        PatientSymptom.created_at.desc()
    ).all()

    return {
        "patient": {
            "id": patient.id,
            "full_name": patient.full_name,
            "email": patient.email,
            "is_active": patient.is_active,
        },
        "assigned_doctor": {
            "id": doctor.id,
            "full_name": doctor.full_name,
        } if doctor else None,
        "symptom_records": [
            {
                "id": record.id,
                "age": record.age,
                "gender": record.gender,
                "symptoms": record.symptoms,
                "duration_days": record.duration_days,
                "blood_pressure": record.blood_pressure,
                "cholesterol_level": record.cholesterol_level,
                "additional_notes": record.additional_notes,
                "created_at": record.created_at,
            }
            for record in records
        ],
    }


# 5. Clinic Profile
@router.get("/profile")
def clinic_profile(
    clinic: User = Depends(get_current_clinic),
):
    return {
        "id": clinic.id,
        "full_name": clinic.full_name,
        "email": clinic.email,
        "role": clinic.role,
        "is_active": clinic.is_active,
        "created_at": clinic.created_at,
    }

