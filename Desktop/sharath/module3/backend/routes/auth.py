
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database.connection import SessionLocal
from backend.database.models import User, RevokedToken
from backend.schemas.user_schema import UserRegister, UserLogin
from backend.services.security import (
    verify_password,
    create_access_token,
    get_db,
    get_current_user,
    security,
    hash_token
)
from pwdlib import PasswordHash


router = APIRouter(prefix="/auth", tags=["Authentication"])

password_hash = PasswordHash.recommended()


# USER REGISTRATION
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):

    db: Session = SessionLocal()

    try:
        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email is already registered"
            )

        hashed_password = password_hash.hash(user.password)

        new_user = User(
            full_name=user.full_name,
            email=user.email,
            hashed_password=hashed_password,
            role="patient"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "full_name": new_user.full_name,
                "email": new_user.email,
                "role": new_user.role
            }
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    finally:
        db.close()


# USER LOGIN
@router.post("/login")
def login_user(user: UserLogin):

    db: Session = SessionLocal()

    try:
        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        if not existing_user or not verify_password(
            user.password,
            existing_user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            data={
                "sub": str(existing_user.id),
                "role": existing_user.role
            }
        )

        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": existing_user.id,
                "full_name": existing_user.full_name,
                "email": existing_user.email,
                "role": existing_user.role
            }
        }

    finally:
        db.close()


# USER LOGOUT
@router.post("/logout")
def logout_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    token = credentials.credentials

    # Hash JWT before storing it
    token_hash = hash_token(token)

    revoked_token = RevokedToken(
        token_hash=token_hash
    )

    db.add(revoked_token)
    db.commit()

    return {
        "message": "Logout successful"
    }
