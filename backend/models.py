import sqlite3
from config import DATABASE


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            contact TEXT,
            role TEXT NOT NULL DEFAULT 'patient',
            requested_role TEXT NOT NULL DEFAULT 'patient',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # old database.db files do not have requested_role, so add it
    columns = [col["name"] for col in conn.execute("PRAGMA table_info(users)").fetchall()]
    if "requested_role" not in columns:
        conn.execute("ALTER TABLE users ADD COLUMN requested_role TEXT NOT NULL DEFAULT 'patient'")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS medical_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            condition TEXT NOT NULL,
            notes TEXT,
            record_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # admin assigns patients to doctors, only then the doctor can see the patient data
    conn.execute("""
        CREATE TABLE IF NOT EXISTS doctor_patient (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            UNIQUE (doctor_id, patient_id)
        )
    """)


    # every symptom submission of a patient is saved here
    conn.execute("""
        CREATE TABLE IF NOT EXISTS symptom_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symptoms TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            result TEXT
        )
    """)

    # old database.db files do not have the result column, so add it
    columns = [col["name"] for col in conn.execute("PRAGMA table_info(symptom_assessments)").fetchall()]
    if "result" not in columns:
        conn.execute("ALTER TABLE symptom_assessments ADD COLUMN result TEXT")

    conn.commit()
    conn.close()
