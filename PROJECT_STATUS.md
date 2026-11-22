# MedAssist AI: Project Status

Student team project. Keep the code simple and beginner-like (short casual comments, no emojis, plain CSS, no frameworks, HTML/CSS/JS in separate files, no inline JS, addEventListener).

## Overall
- Module 1 (User Management): COMPLETE
- Module 2 (Symptom Analysis): COMPLETE (2.1 selection, 2.2 validation, 2.3 correlation, 2.4 history integration, structured assessment)
- Module 3 (Disease Prediction): not started. It will take the structured assessment of Module 2 as its input

## Stack and decisions
Frontend: HTML, CSS, JS. Backend: Flask + Blueprints, sqlite3 (get_db in models.py), Flask-Bcrypt, Flask-JWT-Extended, Flask-CORS. Frontend on Live Server (5500), backend on 5000.
The team document for Module 2 mentions FastAPI, but the project stays on Flask (one backend and one login for all modules). If the team lead insists on FastAPI the whole backend has to be ported.

## Module 1 (done, tested)
- Registration (frontend + backend validation, unique email, bcrypt). Users can request a role (patient/doctor/clinic) while registering, but everyone starts as patient and the admin approves (requested_role column). Privacy and terms pages exist
- Login with JWT (identity = str(user id)), /api/me, logout, protected pages
- Profile: GET/PUT /api/profile, GET /api/profile/<id> (own, admin, or a doctor with that patient assigned)
- RBAC: decorators.py role_required(*roles) checks the role in the DATABASE and returns 403
- Admin: users list, stats, change role, delete user (also deletes history, assignments, symptom assessments), doctor-patient assignments
- make_admin.py (first admin): python make_admin.py email
- Medical history: patient adds/views own, doctor sees assigned patients only (doctor_patient table)
- common.js helpers: API_URL, saveToken, getToken, logout, checkLogin, showMessage, hideMessage, authFetch(path, options)
- user_profile.py is named so on purpose (profile.py clashes with a Python built-in module)

## Module 2 Part 1 (done, tested)
- backend/symptom_data.py (data) and backend/symptoms.py (routes): SYMPTOMS (key -> label, 135 selectable = 131 dataset symptoms + 4 common names), DATASET_COLUMNS (clean name -> real csv column name), COMMON_SYMPTOMS (fever -> high_fever + mild_fever, body_pain -> muscle_pain + joint_pain, sore_throat -> throat_irritation, difficulty_breathing -> breathlessness), get_dataset_columns(key)
- GET /api/symptoms and POST /api/symptoms/submit (patient only). Validation: format, empty list, unsupported symptoms (400 with invalid_symptoms), duplicates (removed and reported in removed_duplicates), max 20, input normalised ("Body Pain" = body_pain). Errors have "error" and "message" keys
- symptom_assessments table (id, user_id, symptoms JSON list of keys, created_at). user id comes from the token only
- backend/data/Training.csv (4920 rows, 0/1 symptom columns, prognosis; only 304 unique rows). Source: public disease-symptom dataset. Ask the team lead if they use a different dataset (same format needed)
- frontend: symptoms.html, css/symptoms.css, js/symptoms.js (common symptoms, search, multi-select, chips, remove, clear, duplicate prevention, submit, validated result box). Dashboard patient card "Enter Symptoms" links to it
- Note: the dataset has 131 unique symptom names (the column fluid_overload appears twice in the file)

## Module 2 Part 2 (done, tested: 70 API checks, 36 browser checks, plus regressions of Module 1 and Part 1)
- backend/symptom_data.py now holds the symptom data and helpers (moved out of symptoms.py to avoid circular imports; symptoms.py only has the routes)
- backend/correlation.py: dataset loaded once; pairwise rows_together, b_given_a, a_given_b, phi score, strength label; strongest pair; top 5 related symptoms (rows with all selected, else any selected); same-family symptoms are not suggested; no disease is predicted. Numbers were cross-checked with an independent pandas calculation
- backend/history_integration.py: the patient's history, records marked relevant when a selected symptom appears in condition or notes
- backend/assessment.py: build_assessment(user_id, assessment_id, symptom_keys) returns the structured assessment (format in README.md). Module 3 should use this
- symptom_assessments has a result TEXT column (JSON of the assessment), added automatically to old databases. Old rows without a result are rebuilt when opened
- APIs (patient only, own data only): POST /api/symptoms/submit (now also returns "assessment"), GET /api/symptoms/assessments, GET /api/symptoms/assessments/<id> (other patients get 404)
- Frontend: assessment.html, assessments.html, js/assessment.js, js/assessments.js, css/assessment.css. symptoms.js redirects to assessment.html?id=N after submit. Dashboard patient card "My Assessments". "Health Reports" stays "Coming soon" (Module 3)
- Dataset limit: 4920 rows but only 304 different ones, so percentages describe the dataset only

## Notes for Module 3 (Disease Prediction)
Input: build_assessment(...) output (symptoms with dataset_columns, correlation, medical_history). The dataset file backend/data/Training.csv has the prognosis column (41 diseases) for training. The "Health Reports" cards (patient and doctor) are waiting for Module 3.

## Possible improvements (optional)
Delete/edit own history entry, password change/reset, doctors viewing symptom assessments of assigned patients.
