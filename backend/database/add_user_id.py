from sqlalchemy import text
from backend.database.connection import engine

with engine.begin() as connection:
    connection.execute(text("""
        ALTER TABLE patient_symptoms
        ADD COLUMN IF NOT EXISTS user_id INTEGER
        REFERENCES users(id)
    """))

print("Patient user_id column added successfully!")