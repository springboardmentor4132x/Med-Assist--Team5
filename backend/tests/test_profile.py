import os
import pytest
from datetime import timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.core.database import Base, get_db
from backend.app.core.security import create_access_token

# Test database setup (in-memory SQLite for deterministic, fast unit/integration testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def setup_test_db():
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# Fixtures for JWT tokens
@pytest.fixture
def patient1_token():
    return create_access_token(
        subject="101",
        email="patient1@medassist.org",
        role="patient",
        expires_delta=timedelta(minutes=30)
    )


@pytest.fixture
def patient2_token():
    return create_access_token(
        subject="202",
        email="patient2@medassist.org",
        role="patient",
        expires_delta=timedelta(minutes=30)
    )


@pytest.fixture
def expired_token():
    return create_access_token(
        subject="101",
        email="patient1@medassist.org",
        role="patient",
        expires_delta=timedelta(minutes=-10)  # Expired 10 minutes ago
    )


# -------------------------------------------------------------
# Test Cases
# -------------------------------------------------------------

def test_get_profile_missing_token():
    """GET /api/v1/profile/me without token must return 401 Unauthorized."""
    response = client.get("/api/v1/profile/me")
    assert response.status_code == 401
    assert "detail" in response.json()
    assert "missing" in response.json()["detail"].lower()


def test_get_profile_invalid_token():
    """GET /api/v1/profile/me with malformed token must return 401 Unauthorized."""
    headers = {"Authorization": "Bearer invalid_gibberish_token_string"}
    response = client.get("/api/v1/profile/me", headers=headers)
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_get_profile_expired_token(expired_token):
    """GET /api/v1/profile/me with expired token must return 401 Unauthorized."""
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/v1/profile/me", headers=headers)
    assert response.status_code == 401
    assert "expired" in response.json()["detail"].lower()


def test_get_profile_success(patient1_token):
    """GET /api/v1/profile/me with valid token returns the authenticated patient's profile."""
    headers = {"Authorization": f"Bearer {patient1_token}"}
    response = client.get("/api/v1/profile/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 101
    assert data["email"] == "patient1@medassist.org"
    assert "full_name" in data


def test_patch_profile_success(patient1_token):
    """PATCH /api/v1/profile/me updates permitted profile fields."""
    headers = {"Authorization": f"Bearer {patient1_token}"}
    update_payload = {
        "full_name": "Jane Doe",
        "age": 32,
        "gender": "Female",
        "contact_number": "+1-555-0199",
        "address": "456 Wellness Blvd, Suite 12",
        "blood_group": "A+",
        "emergency_contact": "+1-555-0188"
    }
    response = client.patch("/api/v1/profile/me", json=update_payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jane Doe"
    assert data["age"] == 32
    assert data["gender"] == "Female"
    assert data["contact_number"] == "+1-555-0199"
    assert data["address"] == "456 Wellness Blvd, Suite 12"
    assert data["blood_group"] == "A+"
    assert data["emergency_contact"] == "+1-555-0188"

    # Confirm persistence with a subsequent GET
    get_res = client.get("/api/v1/profile/me", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["age"] == 32
    assert get_res.json()["blood_group"] == "A+"


def test_patch_profile_invalid_age(patient1_token):
    """PATCH /api/v1/profile/me rejects invalid age (< 0 or > 125)."""
    headers = {"Authorization": f"Bearer {patient1_token}"}
    response = client.patch("/api/v1/profile/me", json={"age": -5}, headers=headers)
    assert response.status_code == 422

    response_high = client.patch("/api/v1/profile/me", json={"age": 180}, headers=headers)
    assert response_high.status_code == 422


def test_patch_profile_invalid_gender(patient1_token):
    """PATCH /api/v1/profile/me rejects unauthorized gender string."""
    headers = {"Authorization": f"Bearer {patient1_token}"}
    response = client.patch("/api/v1/profile/me", json={"gender": "Alien"}, headers=headers)
    assert response.status_code == 422


def test_patch_profile_invalid_blood_group(patient1_token):
    """PATCH /api/v1/profile/me rejects invalid blood group."""
    headers = {"Authorization": f"Bearer {patient1_token}"}
    response = client.patch("/api/v1/profile/me", json={"blood_group": "XYZ+"}, headers=headers)
    assert response.status_code == 422


def test_patch_profile_invalid_phone_number(patient1_token):
    """PATCH /api/v1/profile/me rejects letters in phone number."""
    headers = {"Authorization": f"Bearer {patient1_token}"}
    response = client.patch("/api/v1/profile/me", json={"contact_number": "not-a-number"}, headers=headers)
    assert response.status_code == 422


def test_patch_profile_rejects_protected_fields(patient1_token):
    """PATCH /api/v1/profile/me forbids modifying protected fields (user_id, role, id)."""
    headers = {"Authorization": f"Bearer {patient1_token}"}
    malicious_payload = {
        "user_id": 9999,
        "role": "admin",
        "age": 40
    }
    response = client.patch("/api/v1/profile/me", json=malicious_payload, headers=headers)
    # Extra forbidden fields must return 422
    assert response.status_code == 422


def test_patient_isolation(patient1_token, patient2_token):
    """Ensure patient 1 and patient 2 have strictly isolated profiles."""
    headers1 = {"Authorization": f"Bearer {patient1_token}"}
    headers2 = {"Authorization": f"Bearer {patient2_token}"}

    # Patient 1 updates their profile
    client.patch("/api/v1/profile/me", json={"full_name": "Alice Patient", "age": 25}, headers=headers1)

    # Patient 2 updates their profile
    client.patch("/api/v1/profile/me", json={"full_name": "Bob Patient", "age": 45}, headers=headers2)

    # Patient 1 reads their profile
    res1 = client.get("/api/v1/profile/me", headers=headers1)
    assert res1.json()["user_id"] == 101
    assert res1.json()["full_name"] == "Alice Patient"
    assert res1.json()["age"] == 25

    # Patient 2 reads their profile
    res2 = client.get("/api/v1/profile/me", headers=headers2)
    assert res2.json()["user_id"] == 202
    assert res2.json()["full_name"] == "Bob Patient"
    assert res2.json()["age"] == 45
