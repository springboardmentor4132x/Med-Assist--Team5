import pytest
from fastapi.testclient import TestClient
from app.main import app, seed_database
from app.core.database import SessionLocal
from app.models.user import User

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    seed_database()

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_admin_login_success():
    response = client.post("/auth/login", json={
        "email": "admin@medassist.ai",
        "password": "Admin@123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "Admin"
    assert data["user"]["email"] == "admin@medassist.ai"

def test_doctor_login_success():
    response = client.post("/auth/login", json={
        "email": "doctor@medassist.ai",
        "password": "Doctor@123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["role"] == "Doctor"

def test_invalid_credentials():
    response = client.post("/auth/login", json={
        "email": "admin@medassist.ai",
        "password": "WrongPassword999"
    })
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_deactivated_account_login_blocked():
    # michael.b@medassist.ai is seeded as is_active=False
    response = client.post("/auth/login", json={
        "email": "michael.b@medassist.ai",
        "password": "Patient@123"
    })
    assert response.status_code == 403
    assert "deactivated" in response.json()["detail"].lower()

def test_admin_dashboard_statistics():
    # Login as admin
    login_res = client.post("/auth/login", json={
        "email": "admin@medassist.ai",
        "password": "Admin@123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch dashboard stats
    dash_res = client.get("/admin/dashboard", headers=headers)
    assert dash_res.status_code == 200
    stats = dash_res.json()
    assert stats["total_users"] >= 7
    assert stats["total_admins"] >= 1
    assert stats["total_patients"] >= 3
    assert stats["active_accounts"] >= 6
    assert len(stats["role_distribution"]) == 4
    assert len(stats["recent_registrations"]) > 0

def test_role_authorization_rejection():
    # Login as patient
    login_res = client.post("/auth/login", json={
        "email": "patient@medassist.ai",
        "password": "Patient@123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Patient tries to access admin dashboard
    dash_res = client.get("/admin/dashboard", headers=headers)
    assert dash_res.status_code == 403
    assert "Access denied" in dash_res.json()["detail"]

def test_unauthenticated_rejection():
    dash_res = client.get("/admin/dashboard")
    assert dash_res.status_code == 401

def test_last_active_admin_protection():
    login_res = client.post("/auth/login", json={
        "email": "admin@medassist.ai",
        "password": "Admin@123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    admin_id = login_res.json()["user"]["id"]

    # Try to deactivate the only active admin
    deactivate_res = client.patch(
        f"/admin/users/{admin_id}/status",
        json={"is_active": False},
        headers=headers
    )
    assert deactivate_res.status_code == 400
    assert "Cannot deactivate the last remaining active administrator" in deactivate_res.json()["detail"]
