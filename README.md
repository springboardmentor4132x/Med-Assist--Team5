# MedAssist AI - Module 1: User Management

All 5 functionalities of the module are done: registration, login with JWT, patient profile management, role-based access control (RBAC) and medical history tracking (with admin page and doctor-patient assignment).

## Tech used
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: SQLite
- Password hashing: bcrypt
- Authentication: JWT (Flask-JWT-Extended)

## Folder structure
```
medassist-ai/
  backend/    app.py, config.py, models.py, auth.py, user_profile.py, admin.py,
              history.py, doctor.py, decorators.py, make_admin.py, requirements.txt
  frontend/   index, register, login, dashboard, profile, history, patients, admin,
              privacy, terms (.html)
    css/      style.css, auth.css, dashboard.css
    js/       common.js, register.js, login.js, dashboard.js, profile.js,
              history.js, patients.js, admin.js
```

## How to run

### 1. Backend
```
cd backend
python -m venv venv
venv\Scripts\activate          (Windows)
source venv/bin/activate       (Mac/Linux)
pip install -r requirements.txt
python app.py
```
Backend runs at http://127.0.0.1:5000 and database.db is created automatically.

### 2. Frontend
Open the `frontend` folder in VS Code, right click `index.html` and choose "Open with Live Server".
(It usually opens on http://127.0.0.1:5500)

## API endpoints

| Method | URL | Description | Token needed |
|---|---|---|---|
| POST | /api/register | create new account | No |
| POST | /api/login | login, returns token | No |
| GET | /api/me | get logged in user details | Yes |
| GET | /api/profile | view own profile | Yes |
| PUT | /api/profile | update own profile (name, age, gender, contact) | Yes |
| GET | /api/profile/<id> | view a profile (own, admin, or a doctor whose patient it is) | Yes |
| GET | /api/admin/users | list all users | Admin only |
| GET | /api/admin/stats | user count per role | Admin only |
| PUT | /api/admin/users/<id>/role | change a user's role | Admin only |
| DELETE | /api/admin/users/<id> | delete a user (also deletes his history and assignments) | Admin only |
| GET | /api/admin/assignments | list doctor-patient assignments | Admin only |
| POST | /api/admin/assignments | assign a patient to a doctor | Admin only |
| DELETE | /api/admin/assignments/<id> | remove an assignment | Admin only |
| POST | /api/history | add own medical history entry | Patient only |
| GET | /api/history | view own medical history | Patient only |
| GET | /api/doctor/patients | patients assigned to the logged in doctor | Doctor only |
| GET | /api/history/patient/<id> | history of an assigned patient | Doctor only (assigned patients) |

## Postman tests

**1. Register** - POST http://127.0.0.1:5000/api/register (Body > raw > JSON)
```json
{
  "full_name": "Rahul Kumar",
  "email": "rahul@mail.com",
  "password": "secret123",
  "age": 25,
  "gender": "Male",
  "contact": "9876543210",
  "role": "patient"
}
```
`role` is optional and can be patient, doctor or clinic (the tabs on the register page). Anything else (like admin) gives 400. Expected: 201 "Registration successful". Send the same request again, expected: 409 "Account already exists with this email".

**2. Login** - POST http://127.0.0.1:5000/api/login
```json
{ "email": "rahul@mail.com", "password": "secret123" }
```
Expected: 200 with a token. Wrong password gives 401 "Invalid email or password".

**3. Protected route** - GET http://127.0.0.1:5000/api/me
Add header `Authorization: Bearer <token from login>`. Expected: 200 with user details.
Without token: 401 "Please login to continue".

**4. Update profile** - PUT http://127.0.0.1:5000/api/profile (with token)
```json
{ "full_name": "Rahul K", "age": 31, "gender": "Male", "contact": "9000000001" }
```
Expected: 200 "Profile updated successfully". Age 500 gives 400.

**5. Admin APIs** - GET http://127.0.0.1:5000/api/admin/users
With a patient token: 403 "You do not have permission to do this". With an admin token: 200 with the users list.

**6. Change role** - PUT http://127.0.0.1:5000/api/admin/users/2/role (admin token)
```json
{ "role": "doctor" }
```

**7. Medical history** - POST http://127.0.0.1:5000/api/history (patient token)
```json
{ "condition": "Typhoid fever", "record_date": "2025-03-10", "notes": "Took antibiotics" }
```
Expected: 201. A future date or a doctor token gives 400 / 403. GET /api/history returns your own records.

**8. Assign a patient to a doctor** - POST http://127.0.0.1:5000/api/admin/assignments (admin token)
```json
{ "doctor_id": 3, "patient_id": 2 }
```
Expected: 201. Then GET /api/history/patient/2 with the doctor's token gives 200, and with another doctor's token gives 403.

## Doctor and clinic registration
The register page has Patient, Doctor and Clinic tabs. Nobody can become a doctor, clinic or admin by registering: every new account is created as a patient and the chosen type is saved in the `requested_role` column. The admin sees it in the "Requested" column of the Manage Users page and changes the role if the request is fine.

## How doctor access works
A doctor can see a patient's profile and history only after the admin assigns that patient to him (doctor_patient table). If the role of the doctor or the patient is changed, or a user is deleted, the related assignments are removed automatically.

## How to make the first admin
Nobody can register as admin, so make the first one from the terminal.
1. Register a normal account from the website.
2. In the backend folder run: `python make_admin.py youremail@gmail.com`
3. Logout and login again, the dashboard now shows "Manage Users".

## Roles
| Role | Dashboard links |
|---|---|
| patient | My Profile, Enter Symptoms*, Health Reports*, Medical History |
| doctor | My Profile, My Patients (assigned patients and their history), Health Reports* |
| clinic | My Profile, Clinic Information* |
| admin | My Profile, Manage Users |

*coming soon (these belong to the next modules: symptom analysis and prediction)

The role is checked from the database on every protected admin request (decorators.py), so a changed role works immediately.

## Common errors
- **CORS error / Failed to fetch**: backend is not running, or API_URL in js/common.js is wrong.
- **ModuleNotFoundError**: activate the virtual environment and run pip install again.
- **403 on admin page**: your account is not an admin, run make_admin.py and login again.
- **no such column: requested_role**: old database.db is used, restart the backend once (the column is added automatically) or delete database.db.
- **Token expired**: token is valid for 1 hour (change JWT_EXPIRY in config.py).

---

# Module 2: Symptom Analysis

Module 2 is complete: symptom selection, validation, correlation analysis, medical history integration and the final structured assessment (which Module 3 will use).

## Dataset
`backend/data/Training.csv` is the public disease-symptom dataset (4920 rows, 131 symptom columns, 41 diseases). The symptoms of the dataset are the supported symptoms of the application. A few common names are also supported and mapped to dataset columns: fever (high_fever, mild_fever), body_pain (muscle_pain, joint_pain), sore_throat (throat_irritation), difficulty_breathing (breathlessness). If the team uses a different dataset, replace this file (same format: one 0/1 column per symptom and a prognosis column).

## Part 1: symptom selection and validation
- Page: `symptoms.html` (patients only): common symptoms, search box, multiple selection, remove selected, clear all, submit
- Frontend validation: at least one symptom, no duplicates, only supported symptoms, maximum 20
- Backend validation: request format, empty list, unsupported symptoms, duplicates (removed and reported, not an error), maximum 20, only a logged in patient
- Every submission is saved in the `symptom_assessments` table for the logged in user (the user id is taken from the token, never from the request)

| Method | URL | Description | Token needed |
|---|---|---|---|
| GET | /api/symptoms | list of supported symptoms (key, label, common) | Patient only |
| POST | /api/symptoms/submit | validate, save and analyse the selected symptoms, returns the assessment | Patient only |
| GET | /api/symptoms/assessments | the patient's own assessments, newest first (short list) | Patient only |
| GET | /api/symptoms/assessments/<id> | one full assessment, only the owner can see it (others get 404) | Patient only |

### Postman test
POST http://127.0.0.1:5000/api/symptoms/submit (patient token)
```json
{ "selected_symptoms": ["fever", "headache", "body_pain"] }
```
Expected: 201 with the validated symptoms, an assessment_id and the full `assessment` (see below).

| Request | Result |
|---|---|
| `"selected_symptoms": []` | 400 "Please select at least one symptom." |
| `["fever", "headache", "fever"]` | 201, fever is kept once and shown in removed_duplicates |
| `["fever", "flying_dragon"]` | 400 "Unsupported symptom(s): flying_dragon" |
| `"selected_symptoms": "fever"` | 400 "selected_symptoms must be a list" |
| more than 20 symptoms | 400 "You can select up to 20 symptoms at a time" |
| doctor/admin token | 403 |
| no token | 401 |

Errors have both an `error` key (as in the module document) and a `message` key (used by the frontend).

## Part 2: correlation analysis, history integration, assessment

After the symptoms are validated and saved, the backend builds the assessment and saves it as JSON in `symptom_assessments.result`.

### 2.3 Correlation analysis (backend/correlation.py)
The dataset (4920 rows) is read once when the server starts. A symptom is "present" in a row if its dataset column is 1 (for `fever` it is `high_fever` or `mild_fever`). For every pair of selected symptoms:
- `rows_together`: rows that have both
- `b_given_a` / `a_given_b`: in percent, among the rows with one symptom, how many also have the other
- `score`: phi coefficient (-1 to 1). `strength`: strong (0.5 or more), moderate (0.3), weak (0.1), none (less)
- `strongest_pair`: the pair with the highest score (null when only one symptom is selected)

`related_symptoms`: the top 5 other symptoms in the rows that have all the selected symptoms (if no row has all of them, the rows that have any of them, shown in `related_based_on`). Symptoms of the same kind as a selected one are not suggested (for example high_fever when fever is selected). No disease is predicted.
Limit: the dataset has 4920 rows but only 304 different ones (each disease is repeated about 120 times), so the percentages show how symptoms occur together in this dataset, not in real patients.

### 2.4 Medical history integration (backend/history_integration.py)
The patient's medical history (newest first) is added to the assessment. A record is `relevant` if a selected symptom (for example "fever", or "muscle pain" for body pain) appears in its condition or notes. Patients without history get empty lists.

### The assessment (backend/assessment.py): input for Module 3
`build_assessment(user_id, assessment_id, symptom_keys)` returns:
```
{
  "assessment_id", "created_at",
  "patient": {id, full_name, age, gender},
  "symptoms": [{key, label, dataset_columns}],      # dataset_columns = real csv columns
  "symptom_count",
  "correlation": {dataset_rows, pairs[], strongest_pair, related_symptoms[], related_based_on, rows_used},
  "medical_history": {total_records, relevant_count, relevant_records[], all_records[]},
  "disclaimer",
  "ready_for_prediction": true
}
```
Module 3 can call `build_assessment(...)` or read the saved JSON from `GET /api/symptoms/assessments/<id>`.

### Pages
- `symptoms.html`: after Submit the patient is sent to `assessment.html?id=<number>`
- `assessment.html`: symptoms, relation table, related symptoms with bars, medical history (relevant records highlighted), disclaimer
- `assessments.html`: list of the patient's past assessments (View button), dashboard card "My Assessments"

Old `database.db` files keep working: the `result` column is added automatically, and an old assessment without a result is analysed when it is opened.

## Folder additions
```
backend/symptom_data.py          symptom list, common names, dataset column helpers
backend/symptoms.py              symptom list, submit, assessments APIs
backend/correlation.py           2.3 correlation analysis
backend/history_integration.py   2.4 medical history integration
backend/assessment.py            builds the structured assessment
backend/data/Training.csv        dataset
frontend/symptoms.html, assessment.html, assessments.html
frontend/css/symptoms.css, assessment.css
frontend/js/symptoms.js, assessment.js, assessments.js
```
