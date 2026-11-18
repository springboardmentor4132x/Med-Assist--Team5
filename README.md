# MedAssist AI – Healthcare Administration Platform
## Member 5: Admin Login, Admin Dashboard & User Account Management

An enterprise-grade, responsive healthcare administration and account governance system built with **React.js**, **FastAPI**, and **PostgreSQL** (with zero-config SQLite development fallback).

---

## 1. Module Overview & Responsibilities

The User Management Module is split across 5 specialized roles:
* **Member 1 – Authentication & Registration:** Password hashing (Bcrypt), JWT access tokens.
* **Member 2 – Patient Profile Management:** Patient demographics & contacts.
* **Member 3 – Role-Based Access Control (RBAC):** Role enforcement across Patient, Doctor, Clinic, Admin.
* **Member 4 – Medical History Management:** Clinical diagnoses and treatment records.
* **Member 5 – Admin & User Account Management (This Module):**
  * Common split-screen login interface with backend-driven role redirection.
  * Real-time administrative dashboard with PostgreSQL statistics.
  * User Directory & Account Governance (search, filter by role/status, pagination).
  * Dedicated management views for Patients, Doctors, and Clinics.
  * Role Management & RBAC Governance with protection for the last active administrator.
  * Soft account activation/deactivation (immediately revokes access to protected APIs).
  * Administrator Account Settings & credential modification.

---

## 2. Technology Stack

* **Frontend:** React 18, Vite, React Router v6, Axios, Custom Healthcare CSS Design System.
* **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2, PyJWT, Bcrypt.
* **Database:** PostgreSQL (production-ready) / SQLite (seamless local dev fallback).
* **Testing:** Pytest, HTTPX, FastAPI TestClient.
* **Version Control:** Git on branch `feature/admin-management`.

---

## 3. Pre-Seeded Credentials for Testing

The application automatically seeds standard test accounts on first startup:

| Role | Email Address | Password | Permissions / Landing Page |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@medassist.ai` | `Admin@123` | Full Admin Dashboard & User Governance (`/admin-dashboard`) |
| **Doctor** | `doctor@medassist.ai` | `Doctor@123` | Clinical Workspace (`/doctor-dashboard`) |
| **Clinic** | `clinic@medassist.ai` | `Clinic@123` | Facility Portal (`/clinic-dashboard`) |
| **Patient** | `patient@medassist.ai` | `Patient@123` | Patient Health Portal (`/patient-dashboard`) |
| **Inactive Patient**| `michael.b@medassist.ai` | `Patient@123` | Account Deactivated (Login blocked with HTTP 403) |

---

## 4. Setup & Running Instructions

### Step 1: Clone & Switch to Feature Branch
```bash
git checkout feature/admin-management
```

### Step 2: Backend Setup & Execution
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Activate the Python virtual environment:
   * **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **Linux / macOS:**
     ```bash
     source venv/bin/activate
     ```
3. (Optional) Configure PostgreSQL in `backend/.env`:
   ```env
   DATABASE_URL="postgresql://postgres:postgres@localhost:5432/medassist_db"
   ```
   *Note: If PostgreSQL is not running, the application automatically uses SQLite (`sqlite:///./medassist.db`) for immediate out-of-the-box local testing.*
4. Start the FastAPI server:
   ```bash
   venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
   ```
   * The API will be live at `http://localhost:8000`
   * Interactive Swagger docs at `http://localhost:8000/docs`

### Step 3: Frontend Setup & Execution
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Start the Vite development server:
   ```bash
   npm run dev
   ```
3. Open your browser and navigate to:
   ```text
   http://localhost:5173
   ```

---

## 5. Administrative API Endpoints

### Authentication
* `POST /api/v1/auth/login`: Authenticates user credentials and returns JWT bearer token + actual user role.
* `POST /api/v1/auth/register`: Registers a new account.
* `GET /api/v1/auth/me`: Retrieves current authenticated user profile.

### Admin Governance (Protected with `require_admin`)
* `GET /api/v1/admin/dashboard`: Live database statistics (total users, counts per role, active/inactive counts, role distribution percentages, recent registrations).
* `GET /api/v1/admin/users`: Server-side searchable, role-filterable, status-filterable, and paginated user list.
* `GET /api/v1/admin/users/{id}`: Detailed user account inspector including attached profile data.
* `PUT /api/v1/admin/users/{id}`: Edit permitted user details (name, email).
* `PATCH /api/v1/admin/users/{id}/status`: Soft-activate or deactivate an account (enforces last active admin protection).
* `PUT /api/v1/admin/users/{id}/role`: Assign a new role (enforces last active admin protection and role validation).
* `GET /api/v1/admin/patients`: Dedicated patient directory.
* `GET /api/v1/admin/doctors`: Dedicated doctor registry.
* `GET /api/v1/admin/clinics`: Dedicated clinic directory.
* `GET /api/v1/admin/account`: Administrator profile settings.
* `PUT /api/v1/admin/account`: Update administrator profile and change password.

---

## 6. Running Automated Tests

Run the full backend integration and security test suite:
```bash
$env:PYTHONPATH="backend"
backend/venv/Scripts/python -m pytest backend/tests/test_member5.py -v
```

Test coverage includes:
1. Health check endpoint.
2. Admin login & JWT verification.
3. Doctor login & role verification.
4. Invalid credentials rejection (HTTP 401).
5. Deactivated account rejection (HTTP 403).
6. Live dashboard analytics compilation from database.
7. Role authorization denial for non-admin accounts (HTTP 403).
8. Unauthenticated access denial (HTTP 401).
9. Security guard preventing deactivation of the last active administrator (HTTP 400).

---

## 7. Git Workflow & Submitting Changes

```bash
# Verify current branch is feature/admin-management
git status

# Stage all files
git add .

# Commit changes
git commit -m "Implement admin dashboard, user management, and common login for Member 5"

# Push to remote feature branch
git push origin feature/admin-management
```
Then, open GitHub and create a Pull Request from `feature/admin-management` into `main`.
