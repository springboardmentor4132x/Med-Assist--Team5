from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from backend.app.core.security import decode_access_token

"""
Authentication Dependency Module for MedAssist AI:
--------------------------------------------------
This module defines the secure JWT bearer token validation dependency.
It interfaces cleanly with Member 1's Authentication Module.

Expected JWT Token Payload Specification:
{
    "sub": "101",                     # Unique Patient User ID (integer as string)
    "email": "patient@example.com",   # Registered patient email address
    "role": "patient",                # User authorization role
    "exp": 1731337200                 # Expiration UNIX timestamp
}

Production Security Guarantee:
- The patient ID is STRICTLY derived from the cryptographically verified JWT payload.
- No client-provided query or body parameters can override this ID.
- No insecure authentication bypass is permitted.
"""

security_bearer = HTTPBearer(auto_error=False)


class AuthenticatedPatient:
    """Represents the authenticated identity extracted from a valid JWT."""
    def __init__(self, user_id: int, email: str, role: str = "patient"):
        self.user_id = user_id
        self.email = email
        self.role = role

    def __repr__(self):
        return f"<AuthenticatedPatient(user_id={self.user_id}, email='{self.email}', role='{self.role}')>"


async def get_current_patient(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)
) -> AuthenticatedPatient:
    """
    FastAPI Dependency to retrieve and verify the current logged-in patient.
    Raises HTTPException(401) on missing, expired, or invalid bearer token.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing. Please provide a Bearer token in the Authorization header.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        payload: Dict[str, Any] = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or malformed authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract subject (user_id) from token
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is missing subject claim ('sub').",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(sub)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token subject ('sub') must be a valid integer user ID.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get("email", "")
    role = payload.get("role", "patient")

    return AuthenticatedPatient(user_id=user_id, email=email, role=role)
