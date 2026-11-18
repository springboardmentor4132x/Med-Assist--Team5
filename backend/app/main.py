from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.core.security import hash_password
from app.models.user import Role, User
from app.models.profiles import PatientProfile, DoctorProfile, ClinicProfile
from app.routers.auth import router as auth_router
from app.routers.admin import router as admin_router

def seed_database():
    """Ensure essential roles and initial system accounts exist."""
    db: Session = SessionLocal()
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)

        # 1. Seed Roles
        roles_data = [
            ("Admin", "Full administrative control and user governance"),
            ("Doctor", "Licensed healthcare medical practitioner"),
            ("Clinic", "Clinical center, hospital or health organization"),
            ("Patient", "Registered healthcare recipient / patient")
        ]
        role_objs = {}
        for role_name, desc in roles_data:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(name=role_name, description=desc)
                db.add(role)
                db.commit()
                db.refresh(role)
            role_objs[role_name] = role

        # 2. Seed Default Accounts if empty
        default_users = [
            {
                "full_name": "Dr. Sarah Admin",
                "email": "admin@medassist.ai",
                "password": "Admin@123",
                "role": "Admin",
                "is_active": True
            },
            {
                "full_name": "Dr. Robert Vance",
                "email": "doctor@medassist.ai",
                "password": "Doctor@123",
                "role": "Doctor",
                "is_active": True,
                "specialization": "Cardiology",
                "license": "MD-84920",
                "exp": 12
            },
            {
                "full_name": "Dr. Emily Chen",
                "email": "emily.chen@medassist.ai",
                "password": "Doctor@123",
                "role": "Doctor",
                "is_active": True,
                "specialization": "Neurology",
                "license": "MD-39102",
                "exp": 8
            },
            {
                "full_name": "Metro Health Clinic",
                "email": "clinic@medassist.ai",
                "password": "Clinic@123",
                "role": "Clinic",
                "is_active": True,
                "clinic_name": "Metro Health Wellness Center",
                "address": "742 Evergreen Terrace, Medical District",
                "phone": "+1 (555) 019-4820"
            },
            {
                "full_name": "John Doe",
                "email": "patient@medassist.ai",
                "password": "Patient@123",
                "role": "Patient",
                "is_active": True,
                "dob": "1990-05-14",
                "gender": "Male",
                "blood_group": "O+",
                "emergency": "+1 (555) 432-1098"
            },
            {
                "full_name": "Jane Smith",
                "email": "jane.smith@medassist.ai",
                "password": "Patient@123",
                "role": "Patient",
                "is_active": True,
                "dob": "1985-11-23",
                "gender": "Female",
                "blood_group": "A-",
                "emergency": "+1 (555) 765-4321"
            },
            {
                "full_name": "Michael Brown",
                "email": "michael.b@medassist.ai",
                "password": "Patient@123",
                "role": "Patient",
                "is_active": False,  # Demo deactivated account
                "dob": "1998-02-17",
                "gender": "Male",
                "blood_group": "B+",
                "emergency": "+1 (555) 998-7766"
            }
        ]

        for u_data in default_users:
            existing = db.query(User).filter(User.email == u_data["email"]).first()
            if not existing:
                role = role_objs[u_data["role"]]
                new_user = User(
                    full_name=u_data["full_name"],
                    email=u_data["email"],
                    password_hash=hash_password(u_data["password"]),
                    role_id=role.id,
                    is_active=u_data["is_active"]
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)

                # Attach respective profile
                if u_data["role"] == "Patient":
                    p_prof = PatientProfile(
                        user_id=new_user.id,
                        date_of_birth=u_data.get("dob"),
                        gender=u_data.get("gender"),
                        blood_group=u_data.get("blood_group"),
                        emergency_contact=u_data.get("emergency")
                    )
                    db.add(p_prof)
                elif u_data["role"] == "Doctor":
                    d_prof = DoctorProfile(
                        user_id=new_user.id,
                        specialization=u_data.get("specialization"),
                        license_number=u_data.get("license"),
                        years_of_experience=u_data.get("exp", 0)
                    )
                    db.add(d_prof)
                elif u_data["role"] == "Clinic":
                    c_prof = ClinicProfile(
                        user_id=new_user.id,
                        clinic_name=u_data.get("clinic_name"),
                        address=u_data.get("address"),
                        contact_number=u_data.get("phone")
                    )
                    db.add(c_prof)
                db.commit()

    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: seed database tables and roles
    seed_database()
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="MedAssist AI Healthcare Management Backend - Member 5 Module",
    lifespan=lifespan
)

# CORS configuration for modern React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include core routers under /api/v1 and root prefixes for seamless compatibility
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "MedAssist AI API",
        "version": "1.0.0",
        "module": "Member 5: Admin & User Account Management"
    }
