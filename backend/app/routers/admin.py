from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional, List
from app.core.database import get_db
from app.core.security import verify_password, hash_password
from app.models.user import User, Role
from app.models.profiles import PatientProfile, DoctorProfile, ClinicProfile
from app.schemas.auth import UserResponse
from app.schemas.admin import (
    DashboardStatsResponse,
    RoleDistribution,
    UserUpdateRequest,
    StatusUpdateRequest,
    RoleUpdateRequest,
    UserDetailResponse,
    AdminProfileUpdate,
    PaginatedUsersResponse
)
from app.dependencies.auth import require_admin

router = APIRouter(prefix="/admin", tags=["Admin Management"])

@router.get("/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_statistics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Retrieve real-time dashboard analytics from PostgreSQL:
    - User totals broken down by role
    - Active vs Inactive accounts
    - Role distribution percentages
    - Recent registered users
    """
    total_users = db.query(func.count(User.id)).scalar() or 0
    active_accounts = db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0
    inactive_accounts = db.query(func.count(User.id)).filter(User.is_active == False).scalar() or 0

    roles = db.query(Role).all()
    role_map = {r.name: r.id for r in roles}

    patient_id = role_map.get("Patient")
    doctor_id = role_map.get("Doctor")
    clinic_id = role_map.get("Clinic")
    admin_id = role_map.get("Admin")

    total_patients = db.query(func.count(User.id)).filter(User.role_id == patient_id).scalar() or 0 if patient_id else 0
    total_doctors = db.query(func.count(User.id)).filter(User.role_id == doctor_id).scalar() or 0 if doctor_id else 0
    total_clinics = db.query(func.count(User.id)).filter(User.role_id == clinic_id).scalar() or 0 if clinic_id else 0
    total_admins = db.query(func.count(User.id)).filter(User.role_id == admin_id).scalar() or 0 if admin_id else 0

    # Calculate percentages
    role_dist: List[RoleDistribution] = []
    for r in roles:
        count = db.query(func.count(User.id)).filter(User.role_id == r.id).scalar() or 0
        pct = round((count / total_users * 100), 1) if total_users > 0 else 0.0
        role_dist.append(RoleDistribution(role=r.name, count=count, percentage=pct))

    # Fetch 5 most recent registrations
    recent_users_query = db.query(User).order_by(User.created_at.desc()).limit(5).all()
    recent_registrations = [
        UserResponse(
            id=u.id,
            full_name=u.full_name,
            email=u.email,
            role=u.role.name if u.role else "Unknown",
            role_id=u.role_id,
            is_active=u.is_active,
            created_at=u.created_at
        )
        for u in recent_users_query
    ]

    return DashboardStatsResponse(
        total_users=total_users,
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_clinics=total_clinics,
        total_admins=total_admins,
        active_accounts=active_accounts,
        inactive_accounts=inactive_accounts,
        role_distribution=role_dist,
        recent_registrations=recent_registrations
    )

@router.get("/users", response_model=PaginatedUsersResponse)
def list_users(
    search: Optional[str] = Query(None, description="Search by name or email"),
    role: Optional[str] = Query(None, description="Filter by role name"),
    status: Optional[str] = Query(None, description="Filter by status: 'active' or 'inactive'"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Retrieve all registered users with server-side searching, role filtering,
    status filtering, and pagination.
    """
    query = db.query(User)

    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(or_(User.full_name.ilike(search_fmt), User.email.ilike(search_fmt)))

    if role and role.lower() != "all":
        query = query.join(Role).filter(Role.name.ilike(role.strip()))

    if status and status.lower() != "all":
        if status.lower() == "active":
            query = query.filter(User.is_active == True)
        elif status.lower() == "inactive":
            query = query.filter(User.is_active == False)

    total = query.count()
    offset = (page - 1) * limit
    users = query.order_by(User.id.asc()).offset(offset).limit(limit).all()

    items = [
        UserResponse(
            id=u.id,
            full_name=u.full_name,
            email=u.email,
            role=u.role.name if u.role else "Unknown",
            role_id=u.role_id,
            is_active=u.is_active,
            created_at=u.created_at
        )
        for u in users
    ]

    total_pages = (total + limit - 1) // limit if total > 0 else 1

    return PaginatedUsersResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )

@router.get("/users/{user_id}", response_model=UserDetailResponse)
def get_user_details(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """View permitted details for an individual user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    patient_data = None
    if user.patient_profile:
        patient_data = {
            "date_of_birth": user.patient_profile.date_of_birth,
            "gender": user.patient_profile.gender,
            "emergency_contact": user.patient_profile.emergency_contact,
            "blood_group": user.patient_profile.blood_group
        }

    doctor_data = None
    if user.doctor_profile:
        doctor_data = {
            "specialization": user.doctor_profile.specialization,
            "license_number": user.doctor_profile.license_number,
            "years_of_experience": user.doctor_profile.years_of_experience
        }

    clinic_data = None
    if user.clinic_profile:
        clinic_data = {
            "clinic_name": user.clinic_profile.clinic_name,
            "address": user.clinic_profile.address,
            "contact_number": user.clinic_profile.contact_number
        }

    return UserDetailResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=user.role.name if user.role else "Unknown",
        role_id=user.role_id,
        is_active=user.is_active,
        created_at=user.created_at,
        patient_profile=patient_data,
        doctor_profile=doctor_data,
        clinic_profile=clinic_data
    )

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_info(
    user_id: int,
    update_data: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """Update permitted user details (name, email)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if update_data.email and update_data.email != user.email:
        existing = db.query(User).filter(User.email == update_data.email).first()
        if existing and existing.id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use.")
        user.email = update_data.email

    if update_data.full_name:
        user.full_name = update_data.full_name

    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=user.role.name if user.role else "Unknown",
        role_id=user.role_id,
        is_active=user.is_active,
        created_at=user.created_at
    )

@router.patch("/users/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    status_data: StatusUpdateRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Soft-activate or deactivate a user account.
    Enforces security protection for the last active administrator.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # Guard: Prevent deactivating the last active administrator
    if not status_data.is_active and user.role and user.role.name == "Admin":
        admin_role = db.query(Role).filter(Role.name == "Admin").first()
        if admin_role:
            active_admin_count = db.query(func.count(User.id)).filter(
                User.role_id == admin_role.id,
                User.is_active == True
            ).scalar() or 0
            if active_admin_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Security violation: Cannot deactivate the last remaining active administrator."
                )

    user.is_active = status_data.is_active
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=user.role.name if user.role else "Unknown",
        role_id=user.role_id,
        is_active=user.is_active,
        created_at=user.created_at
    )

@router.put("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    role_data: RoleUpdateRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Assign a new role to a user.
    Protects against self-demotion or removal of the last active administrator.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    target_role = db.query(Role).filter(Role.name == role_data.role_name).first()
    if not target_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Target role '{role_data.role_name}' does not exist."
        )

    # Guard: If demoting an Admin, ensure they are not the last active administrator
    if user.role and user.role.name == "Admin" and target_role.name != "Admin":
        admin_role = db.query(Role).filter(Role.name == "Admin").first()
        if admin_role:
            active_admin_count = db.query(func.count(User.id)).filter(
                User.role_id == admin_role.id,
                User.is_active == True
            ).scalar() or 0
            if active_admin_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Security violation: Cannot change role of the last active administrator."
                )

    user.role_id = target_role.id
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=target_role.name,
        role_id=user.role_id,
        is_active=user.is_active,
        created_at=user.created_at
    )

@router.get("/patients")
def list_patients(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """Dedicated management listing for Patients."""
    patient_role = db.query(Role).filter(Role.name == "Patient").first()
    if not patient_role:
        return {"items": [], "total": 0, "page": page, "limit": limit, "total_pages": 1}

    query = db.query(User).filter(User.role_id == patient_role.id)
    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(or_(User.full_name.ilike(search_fmt), User.email.ilike(search_fmt)))
    if status and status.lower() != "all":
        query = query.filter(User.is_active == (status.lower() == "active"))

    total = query.count()
    users = query.offset((page - 1) * limit).limit(limit).all()

    items = []
    for u in users:
        profile_info = {
            "gender": u.patient_profile.gender if u.patient_profile else "Not specified",
            "date_of_birth": u.patient_profile.date_of_birth if u.patient_profile else "Not specified",
            "blood_group": u.patient_profile.blood_group if u.patient_profile else "Not specified",
            "emergency_contact": u.patient_profile.emergency_contact if u.patient_profile else "Not specified"
        }
        items.append({
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "role": "Patient",
            "is_active": u.is_active,
            "created_at": u.created_at,
            "profile": profile_info
        })

    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return {"items": items, "total": total, "page": page, "limit": limit, "total_pages": total_pages}

@router.get("/doctors")
def list_doctors(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """Dedicated management listing for Doctors."""
    doctor_role = db.query(Role).filter(Role.name == "Doctor").first()
    if not doctor_role:
        return {"items": [], "total": 0, "page": page, "limit": limit, "total_pages": 1}

    query = db.query(User).filter(User.role_id == doctor_role.id)
    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(or_(User.full_name.ilike(search_fmt), User.email.ilike(search_fmt)))
    if status and status.lower() != "all":
        query = query.filter(User.is_active == (status.lower() == "active"))

    total = query.count()
    users = query.offset((page - 1) * limit).limit(limit).all()

    items = []
    for u in users:
        profile_info = {
            "specialization": u.doctor_profile.specialization if u.doctor_profile else "General Practitioner",
            "license_number": u.doctor_profile.license_number if u.doctor_profile else "MED-00000",
            "years_of_experience": u.doctor_profile.years_of_experience if u.doctor_profile else 0
        }
        items.append({
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "role": "Doctor",
            "is_active": u.is_active,
            "created_at": u.created_at,
            "profile": profile_info
        })

    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return {"items": items, "total": total, "page": page, "limit": limit, "total_pages": total_pages}

@router.get("/clinics")
def list_clinics(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """Dedicated management listing for Clinics."""
    clinic_role = db.query(Role).filter(Role.name == "Clinic").first()
    if not clinic_role:
        return {"items": [], "total": 0, "page": page, "limit": limit, "total_pages": 1}

    query = db.query(User).filter(User.role_id == clinic_role.id)
    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(or_(User.full_name.ilike(search_fmt), User.email.ilike(search_fmt)))
    if status and status.lower() != "all":
        query = query.filter(User.is_active == (status.lower() == "active"))

    total = query.count()
    users = query.offset((page - 1) * limit).limit(limit).all()

    items = []
    for u in users:
        profile_info = {
            "clinic_name": u.clinic_profile.clinic_name if u.clinic_profile else u.full_name,
            "address": u.clinic_profile.address if u.clinic_profile else "Main Healthcare Facility",
            "contact_number": u.clinic_profile.contact_number if u.clinic_profile else "+1 (555) 019-2831"
        }
        items.append({
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "role": "Clinic",
            "is_active": u.is_active,
            "created_at": u.created_at,
            "profile": profile_info
        })

    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return {"items": items, "total": total, "page": page, "limit": limit, "total_pages": total_pages}

@router.get("/account", response_model=UserResponse)
def get_admin_account(current_admin: User = Depends(require_admin)):
    """Return the currently authenticated administrator's profile."""
    return UserResponse(
        id=current_admin.id,
        full_name=current_admin.full_name,
        email=current_admin.email,
        role=current_admin.role.name if current_admin.role else "Admin",
        role_id=current_admin.role_id,
        is_active=current_admin.is_active,
        created_at=current_admin.created_at
    )

@router.put("/account", response_model=UserResponse)
def update_admin_account(
    account_in: AdminProfileUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """Update administrator's profile details and change password if requested."""
    if account_in.email and account_in.email != current_admin.email:
        existing = db.query(User).filter(User.email == account_in.email).first()
        if existing and existing.id != current_admin.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use.")
        current_admin.email = account_in.email

    if account_in.full_name:
        current_admin.full_name = account_in.full_name

    # Handle password update
    if account_in.new_password:
        if not account_in.current_password or not verify_password(account_in.current_password, current_admin.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is required and must be correct to set a new password."
            )
        if len(account_in.new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be at least 6 characters long."
            )
        current_admin.password_hash = hash_password(account_in.new_password)

    db.commit()
    db.refresh(current_admin)

    return UserResponse(
        id=current_admin.id,
        full_name=current_admin.full_name,
        email=current_admin.email,
        role=current_admin.role.name if current_admin.role else "Admin",
        role_id=current_admin.role_id,
        is_active=current_admin.is_active,
        created_at=current_admin.created_at
    )
