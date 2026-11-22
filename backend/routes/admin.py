from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from backend.database.models import (
    User,
    PatientSymptom,
    DoctorPatientAssignment,
    ClinicDoctorAssignment,
)
from backend.services.security import (
    get_current_user,
    get_db,
    verify_password,
    get_password_hash,
)
from backend.schemas.user_schema import AdminUserCreate
router = APIRouter(prefix="/admin", tags=["Admin Management"])
ALLOWED_ROLES = {"patient", "doctor", "clinic", "admin"}


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if (current_user.role or "").lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access is required.",
        )
    return current_user


def display_role(role: Optional[str]) -> str:
    return (role or "patient").title()


def user_payload(user: User) -> dict:
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": display_role(user.role),
        "role_id": display_role(user.role),
        "is_active": bool(user.is_active),
        "created_at": user.created_at,
    }


def filtered_users(
    db: Session,
    role: Optional[str] = None,
    search: Optional[str] = None,
    account_status: Optional[str] = None,
):
    query = db.query(User)
    if role and role.lower() != "all":
        query = query.filter(func.lower(User.role) == role.strip().lower())
    if search:
        term = f"%{search.strip()}%"
        query = query.filter(or_(User.full_name.ilike(term), User.email.ilike(term)))
    if account_status and account_status.lower() != "all":
        query = query.filter(User.is_active == (account_status.lower() == "active"))
    return query


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    total = db.query(func.count(User.id)).scalar() or 0
    active = db.query(func.count(User.id)).filter(User.is_active.is_(True)).scalar() or 0
    inactive = total - active
    roles = ["Admin", "Doctor", "Clinic", "Patient"]
    distribution = []
    counts = {}
    for role in roles:
        count = db.query(func.count(User.id)).filter(
            func.lower(User.role) == role.lower()
        ).scalar() or 0
        counts[role] = count
        distribution.append({
            "role": role,
            "count": count,
            "percentage": round((count / total * 100), 1) if total else 0.0,
        })
    recent = db.query(User).order_by(User.created_at.desc()).limit(5).all()
    return {
        "total_users": total,
        "total_patients": counts["Patient"],
        "total_doctors": counts["Doctor"],
        "total_clinics": counts["Clinic"],
        "total_admins": counts["Admin"],
        "active_accounts": active,
        "inactive_accounts": inactive,
        "role_distribution": distribution,
        "recent_registrations": [user_payload(user) for user in recent],
    }


@router.get("/users")
def list_users(
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    query = filtered_users(db, role, search, status_filter)
    total = query.count()
    users = query.order_by(User.id.asc()).offset((page - 1) * limit).limit(limit).all()
    return {
        "items": [user_payload(user) for user in users],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": max(1, (total + limit - 1) // limit),
    }


@router.get("/users/{user_id}")
def user_details(
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    data = user_payload(user)
    data.update({
        "patient_profile": None,
        "doctor_profile": None,
        "clinic_profile": None,
    })
    if (user.role or "").lower() == "patient":
        latest = db.query(PatientSymptom).filter(
            PatientSymptom.user_id == user.id
        ).order_by(PatientSymptom.created_at.desc()).first()
        if latest:
            data["patient_profile"] = {
                "gender": latest.gender,
                "latest_record_id": latest.id,
                "latest_record_date": latest.created_at,
            }
    return data


@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    new_name = payload.get("full_name")
    new_email = payload.get("email")
    if new_name:
        user.full_name = str(new_name).strip()
    if new_email and new_email != user.email:
        duplicate = db.query(User).filter(User.email == new_email, User.id != user_id).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Email is already in use.")
        user.email = new_email
    db.commit()
    db.refresh(user)
    return user_payload(user)


@router.patch("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    active = payload.get("is_active")
    if not isinstance(active, bool):
        raise HTTPException(status_code=422, detail="'is_active' must be true or false.")
    if not active and (user.role or "").lower() == "admin":
        active_admins = db.query(func.count(User.id)).filter(
            func.lower(User.role) == "admin",
            User.is_active.is_(True),
        ).scalar() or 0
        if active_admins <= 1:
            raise HTTPException(status_code=400, detail="Cannot deactivate the last active administrator.")
    if user.id == admin.id and not active:
        raise HTTPException(status_code=400, detail="You cannot deactivate your own account.")
    user.is_active = active
    db.commit()
    db.refresh(user)
    return user_payload(user)


@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    target = str(payload.get("role_name", "")).strip().lower()
    if target not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Role must be Patient, Doctor, Clinic, or Admin.")
    if user.role.lower() == "admin" and target != "admin":
        active_admins = db.query(func.count(User.id)).filter(
            func.lower(User.role) == "admin",
            User.is_active.is_(True),
        ).scalar() or 0
        if active_admins <= 1:
            raise HTTPException(status_code=400, detail="Cannot change the role of the last active administrator.")
    if user.id == admin.id and target != "admin":
        raise HTTPException(status_code=400, detail="You cannot remove your own administrator role.")
    user.role = target
    db.commit()
    db.refresh(user)
    return user_payload(user)


def role_listing(
    role: str,
    search: Optional[str],
    account_status: Optional[str],
    page: int,
    limit: int,
    db: Session,
):
    query = filtered_users(db, role, search, account_status)
    total = query.count()
    users = query.order_by(User.id.asc()).offset((page - 1) * limit).limit(limit).all()
    items = []
    for user in users:
        profile = {}
        if role == "patient":
            latest = db.query(PatientSymptom).filter(
                PatientSymptom.user_id == user.id
            ).order_by(PatientSymptom.created_at.desc()).first()
            profile = {
                "gender": latest.gender if latest else "Not specified",
                "date_of_birth": "Not recorded",
                "blood_group": "Not recorded",
                "emergency_contact": "Not recorded",
            }
        elif role == "doctor":
            profile = {
                "specialization": "Not recorded",
                "license_number": "Not recorded",
                "years_of_experience": 0,
            }
        else:
            profile = {
                "clinic_name": user.full_name,
                "address": "Not recorded",
                "contact_number": "Not recorded",
            }
        item = user_payload(user)
        item["profile"] = profile
        items.append(item)
    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": max(1, (total + limit - 1) // limit),
    }


@router.get("/patients")
def list_patients(
    search: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return role_listing("patient", search, status_filter, page, limit, db)


@router.get("/doctors")
def list_doctors(
    search: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return role_listing("doctor", search, status_filter, page, limit, db)


@router.get("/clinics")
def list_clinics(
    search: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return role_listing("clinic", search, status_filter, page, limit, db)


@router.get("/account")
def get_admin_account(admin: User = Depends(require_admin)):
    return user_payload(admin)


@router.put("/account")
def update_admin_account(
    payload: dict,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    name = payload.get("full_name")
    email = payload.get("email")
    current_password = payload.get("current_password")
    new_password = payload.get("new_password")
    if name:
        admin.full_name = str(name).strip()
    if email and email != admin.email:
        duplicate = db.query(User).filter(User.email == email, User.id != admin.id).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Email is already in use.")
        admin.email = email
    if new_password:
        if not current_password or not verify_password(current_password, admin.hashed_password):
            raise HTTPException(status_code=400, detail="Current password is incorrect.")
        if len(new_password) < 8:
            raise HTTPException(status_code=400, detail="New password must contain at least 8 characters.")
        admin.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(admin)
    return user_payload(admin)

# --------------------------------------------------
# DOCTOR-PATIENT ASSIGNMENT MANAGEMENT
# --------------------------------------------------

@router.get("/assignments")
def list_assignments(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    assignments = db.query(DoctorPatientAssignment).order_by(
        DoctorPatientAssignment.assigned_at.desc()
    ).all()

    results = []

    for assignment in assignments:
        doctor = db.query(User).filter(
            User.id == assignment.doctor_id
        ).first()

        patient = db.query(User).filter(
            User.id == assignment.patient_id
        ).first()

        if doctor and patient:
            results.append({
                "id": assignment.id,
                "doctor_id": doctor.id,
                "doctor_name": doctor.full_name,
                "doctor_email": doctor.email,
                "patient_id": patient.id,
                "patient_name": patient.full_name,
                "patient_email": patient.email,
                "assigned_at": assignment.assigned_at,
            })

    return {"items": results, "total": len(results)}


@router.post("/assignments", status_code=201)
def create_assignment(
    payload: dict,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    doctor_id = payload.get("doctor_id")
    patient_id = payload.get("patient_id")

    if (
        not isinstance(doctor_id, int)
        or isinstance(doctor_id, bool)
        or not isinstance(patient_id, int)
        or isinstance(patient_id, bool)
    ):
        raise HTTPException(
            status_code=422,
            detail="Valid doctor_id and patient_id are required.",
        )

    if doctor_id == patient_id:
        raise HTTPException(
            status_code=400,
            detail="A doctor cannot be assigned as their own patient.",
        )

    doctor = db.query(User).filter(User.id == doctor_id).first()
    patient = db.query(User).filter(User.id == patient_id).first()

    if not doctor or (doctor.role or "").lower() != "doctor":
        raise HTTPException(status_code=404, detail="Doctor not found.")

    if not patient or (patient.role or "").lower() != "patient":
        raise HTTPException(status_code=404, detail="Patient not found.")

    if not doctor.is_active:
        raise HTTPException(status_code=400, detail="Doctor account is inactive.")

    if not patient.is_active:
        raise HTTPException(status_code=400, detail="Patient account is inactive.")

    existing = db.query(DoctorPatientAssignment).filter(
        DoctorPatientAssignment.doctor_id == doctor_id,
        DoctorPatientAssignment.patient_id == patient_id,
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="This patient is already assigned to this doctor.",
        )

    assignment = DoctorPatientAssignment(
        doctor_id=doctor_id,
        patient_id=patient_id,
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return {
        "message": "Patient assigned to doctor successfully.",
        "id": assignment.id,
        "doctor_id": doctor.id,
        "doctor_name": doctor.full_name,
        "patient_id": patient.id,
        "patient_name": patient.full_name,
        "assigned_at": assignment.assigned_at,
    }


@router.delete("/assignments/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    assignment = db.query(DoctorPatientAssignment).filter(
        DoctorPatientAssignment.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found.",
        )

    db.delete(assignment)
    db.commit()

    return {"message": "Patient assignment removed successfully."}

# --------------------------------------------------
# CLINIC-DOCTOR ASSOCIATION MANAGEMENT
# --------------------------------------------------

@router.get("/clinic-assignments")
def list_clinic_assignments(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    assignments = db.query(ClinicDoctorAssignment).order_by(
        ClinicDoctorAssignment.assigned_at.desc()
    ).all()

    results = []

    for assignment in assignments:
        clinic = db.query(User).filter(
            User.id == assignment.clinic_id,
            User.role == "clinic",
        ).first()

        doctor = db.query(User).filter(
            User.id == assignment.doctor_id,
            User.role == "doctor",
        ).first()

        if clinic and doctor:
            results.append({
                "id": assignment.id,
                "clinic_id": clinic.id,
                "clinic_name": clinic.full_name,
                "clinic_email": clinic.email,
                "doctor_id": doctor.id,
                "doctor_name": doctor.full_name,
                "doctor_email": doctor.email,
                "assigned_at": assignment.assigned_at,
            })

    return {"items": results, "total": len(results)}


@router.post("/clinic-assignments", status_code=201)
def create_clinic_assignment(
    payload: dict,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    clinic_id = payload.get("clinic_id")
    doctor_id = payload.get("doctor_id")

    if (
        not isinstance(clinic_id, int)
        or isinstance(clinic_id, bool)
        or not isinstance(doctor_id, int)
        or isinstance(doctor_id, bool)
    ):
        raise HTTPException(
            status_code=422,
            detail="Valid clinic_id and doctor_id are required.",
        )

    clinic = db.query(User).filter(
        User.id == clinic_id,
        User.role == "clinic",
    ).first()

    doctor = db.query(User).filter(
        User.id == doctor_id,
        User.role == "doctor",
    ).first()

    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found.")

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found.")

    if not clinic.is_active:
        raise HTTPException(status_code=400, detail="Clinic account is inactive.")

    if not doctor.is_active:
        raise HTTPException(status_code=400, detail="Doctor account is inactive.")

    existing = db.query(ClinicDoctorAssignment).filter(
        ClinicDoctorAssignment.clinic_id == clinic_id,
        ClinicDoctorAssignment.doctor_id == doctor_id,
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="This doctor is already associated with this clinic.",
        )

    assignment = ClinicDoctorAssignment(
        clinic_id=clinic_id,
        doctor_id=doctor_id,
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return {
        "message": "Doctor associated with clinic successfully.",
        "id": assignment.id,
        "clinic_id": clinic.id,
        "clinic_name": clinic.full_name,
        "doctor_id": doctor.id,
        "doctor_name": doctor.full_name,
        "assigned_at": assignment.assigned_at,
    }


@router.delete("/clinic-assignments/{assignment_id}")
def delete_clinic_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    assignment = db.query(ClinicDoctorAssignment).filter(
        ClinicDoctorAssignment.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Clinic-doctor association not found.",
        )

    db.delete(assignment)
    db.commit()

    return {"message": "Doctor removed from clinic successfully."}
# ADMIN: CREATE PATIENT OR DOCTOR
@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: AdminUserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        )

    new_user = User(
        full_name=user_data.full_name,
        email=str(user_data.email),
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role,
        is_active=True,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": f"{user_data.role.title()} account created successfully.",
            "user": {
                "id": new_user.id,
                "full_name": new_user.full_name,
                "email": new_user.email,
                "role": new_user.role,
                "is_active": new_user.is_active,
            },
        }

    except Exception:
        db.rollback()
        raise
    # ADMIN: DELETE PATIENT OR DOCTOR
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    if user.role not in ["patient", "doctor"]:
        raise HTTPException(
            status_code=400,
            detail="Only patient and doctor accounts can be deleted.",
        )

    try:
        if user.role == "patient":
            # Preserve symptom history but detach it from the deleted account
            db.query(PatientSymptom).filter(
                PatientSymptom.user_id == user_id
            ).update(
                {PatientSymptom.user_id: None},
                synchronize_session=False,
            )

            db.query(DoctorPatientAssignment).filter(
                DoctorPatientAssignment.patient_id == user_id
            ).delete(synchronize_session=False)

        elif user.role == "doctor":
            db.query(DoctorPatientAssignment).filter(
                DoctorPatientAssignment.doctor_id == user_id
            ).delete(synchronize_session=False)

            db.query(ClinicDoctorAssignment).filter(
                ClinicDoctorAssignment.doctor_id == user_id
            ).delete(synchronize_session=False)

        db.delete(user)
        db.commit()

        return {
            "message": f"{user.role.title()} account deleted successfully.",
            "deleted_user_id": user_id,
        }

    except Exception:
        db.rollback()
        raise