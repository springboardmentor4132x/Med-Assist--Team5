
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.services.security import get_current_user, get_db
from backend.database.models import (
    User,
    PatientSymptom,
    DoctorPatientAssignment
)
from backend.app.models.profile import PatientProfile


router = APIRouter(
    prefix="/doctor",
    tags=["Doctor Dashboard"]
)


def require_doctor(current_user: User):
    if (current_user.role or "").lower() != "doctor":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Doctor account required."
        )


@router.get("/patients")
def get_assigned_patients(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_doctor(current_user)

    assignments = db.query(DoctorPatientAssignment).filter(
        DoctorPatientAssignment.doctor_id == current_user.id
    ).all()

    patients = []

    for assignment in assignments:
        patient = db.query(User).filter(
            User.id == assignment.patient_id,
            User.role.ilike("patient"),
            User.is_active.is_(True)
        ).first()

        if not patient:
            continue

        profile = db.query(PatientProfile).filter(
            PatientProfile.user_id == patient.id
        ).first()

        record_count = db.query(PatientSymptom).filter(
            PatientSymptom.user_id == patient.id
        ).count()

        patients.append({
            "patient_id": patient.id,
            "full_name": patient.full_name,
            "email": patient.email,
            "profile": {
                "age": profile.age,
                "gender": profile.gender,
                "contact_number": profile.contact_number,
                "address": profile.address,
                "blood_group": profile.blood_group,
                "emergency_contact": profile.emergency_contact
            } if profile else None,
            "records_count": record_count,
            "assigned_at": assignment.assigned_at
        })

    return {
        "total": len(patients),
        "patients": patients
    }


@router.get("/patients/{patient_id}")
def get_assigned_patient_details(
    patient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_doctor(current_user)

    assignment = db.query(DoctorPatientAssignment).filter(
        DoctorPatientAssignment.doctor_id == current_user.id,
        DoctorPatientAssignment.patient_id == patient_id
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this patient."
        )

    patient = db.query(User).filter(
        User.id == patient_id,
        User.role.ilike("patient"),
        User.is_active.is_(True)
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    profile = db.query(PatientProfile).filter(
        PatientProfile.user_id == patient.id
    ).first()

    records = db.query(PatientSymptom).filter(
        PatientSymptom.user_id == patient.id
    ).order_by(
        PatientSymptom.created_at.desc()
    ).all()

    return {
        "patient": {
            "id": patient.id,
            "full_name": patient.full_name,
            "email": patient.email
        },
        "profile": {
            "age": profile.age,
            "gender": profile.gender,
            "contact_number": profile.contact_number,
            "address": profile.address,
            "blood_group": profile.blood_group,
            "emergency_contact": profile.emergency_contact
        } if profile else None,
        "records_count": len(records),
        "clinical_records": [
            {
                "id": record.id,
                "age": record.age,
                "gender": record.gender,
                "symptoms": record.symptoms,
                "duration_days": record.duration_days,
                "blood_pressure": record.blood_pressure,
                "cholesterol_level": record.cholesterol_level,
                "additional_notes": record.additional_notes,
                "created_at": record.created_at
            }
            for record in records
        ]
    }
