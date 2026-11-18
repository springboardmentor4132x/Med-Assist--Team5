from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, hash_password, create_access_token
from app.models.user import User, Role
from app.models.profiles import PatientProfile
from app.schemas.auth import LoginRequest, TokenResponse, UserRegister, UserResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Common login endpoint for Patient, Doctor, Clinic, and Administrator roles.
    Verifies credentials, checks active status, and returns JWT with role details.
    """
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Check account active status
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated. Please contact an administrator."
        )

    role_name = user.role.name if user.role else "Patient"
    
    # Generate JWT
    token_payload = {
        "sub": user.email,
        "user_id": user.id,
        "role": role_name
    }
    access_token = create_access_token(data=token_payload)

    user_response = UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=role_name,
        role_id=user.role_id,
        is_active=user.is_active,
        created_at=user.created_at
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account (defaults to Patient role)."""
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    role = db.query(Role).filter(Role.name == user_in.role_name).first()
    if not role:
        role = db.query(Role).filter(Role.name == "Patient").first()
        if not role:
            role = Role(name="Patient", description="General Patient")
            db.add(role)
            db.commit()
            db.refresh(role)

    new_user = User(
        full_name=user_in.full_name,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        role_id=role.id,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Automatically create patient profile if role is Patient
    if role.name == "Patient":
        patient_profile = PatientProfile(user_id=new_user.id)
        db.add(patient_profile)
        db.commit()

    return UserResponse(
        id=new_user.id,
        full_name=new_user.full_name,
        email=new_user.email,
        role=role.name,
        role_id=role.id,
        is_active=new_user.is_active,
        created_at=new_user.created_at
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return UserResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        role=current_user.role.name if current_user.role else "User",
        role_id=current_user.role_id,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )
