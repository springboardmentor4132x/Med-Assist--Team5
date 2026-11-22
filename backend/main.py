
from backend.services.symptom_analyzer import analyze_symptoms
from backend.services.predict import predict_outcome
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import json

from backend.database.models import PatientSymptom, User
from backend.services.security import get_current_user
from backend.routes.auth import router as auth_router


# Load database settings
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

# Create database connection
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Create FastAPI application
app = FastAPI(
    title="MedAssist AI",
    description="Medical Symptom Analysis System",
    version="1.0.0"
)
app.include_router(auth_router)
# Enable communication between React and FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Patient symptom input model
class SymptomRequest(BaseModel):
    age: int = Field(ge=0, le=120)

    gender: Optional[str] = Field(
        default=None,
        max_length=30
    )

    symptoms: list[str] = Field(min_length=1)

    duration_days: int = Field(ge=1, le=365)

    blood_pressure: str = "Normal"

    cholesterol_level: str = "Normal"

    additional_notes: Optional[str] = Field(
        default=None,
        max_length=500
    )


# Home API
@app.get("/")
def home():
    return {
        "message": "Welcome to MedAssist AI",
        "status": "Backend is running successfully"
    }


# Health check API
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Patient symptom submission API
@app.post("/symptoms")
def submit_symptoms(
    patient: SymptomRequest,
    current_user: User = Depends(get_current_user)
):

    db = SessionLocal()

    try:
        new_patient = PatientSymptom(
            user_id=current_user.id,
            age=patient.age,
            gender=patient.gender,
            symptoms=json.dumps(patient.symptoms),
            duration_days=patient.duration_days,
            blood_pressure=patient.blood_pressure,
            cholesterol_level=patient.cholesterol_level,
            additional_notes=patient.additional_notes
            
          )

        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)

        return {
            "message": "Symptoms saved successfully",
            "patient_id": new_patient.id,
            "patient_details": {
                "age": new_patient.age,
                "gender": new_patient.gender,
                "symptoms": patient.symptoms,
                "duration_days": new_patient.duration_days,
                "additional_notes": new_patient.additional_notes
            },
            "analysis_status": "Ready for future analysis"
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to save symptoms to the database"
        )

    finally:
        db.close()
        # Get all patient symptom records
@app.get("/patients")
def get_patients(
    current_user: User = Depends(get_current_user)
):

    db = SessionLocal()

    try:
        patients = db.query(PatientSymptom).filter(
    PatientSymptom.user_id == current_user.id
).order_by(
    PatientSymptom.id.desc()
).all()

        return {
            "total_records": len(patients),
            "patients": [
                {
                    "id": patient.id,
                    "age": patient.age,
                    "gender": patient.gender,
                    "symptoms": json.loads(patient.symptoms),
                    "duration_days": patient.duration_days,
                    "blood_pressure": patient.blood_pressure,
                    "cholesterol_level": patient.cholesterol_level,
                    "additional_notes": patient.additional_notes
                }
                for patient in patients
            ]
        }

    finally:
        db.close()
        # Get one patient using patient ID

@app.get("/patients/{patient_id}")
def get_patient_by_id(
    patient_id: int,
    current_user: User = Depends(get_current_user)
):

    db = SessionLocal()

    try:
        patient = db.query(PatientSymptom).filter(
            PatientSymptom.id == patient_id,
            PatientSymptom.user_id == current_user.id
        ).first()

        if patient is None:
            raise HTTPException(
                status_code=404,
                detail="Patient record not found"
            )

        return {
            "id": patient.id,
            "age": patient.age,
            "gender": patient.gender,
            "symptoms": json.loads(patient.symptoms),
            "duration_days": patient.duration_days,
            "additional_notes": patient.additional_notes
        }

    finally:
        db.close()

        # Update patient information

@app.put("/patients/{patient_id}")
def update_patient(
    patient_id: int,
    updated_data: SymptomRequest,
    current_user: User = Depends(get_current_user)
):

    db = SessionLocal()

    try:
        patient = db.query(PatientSymptom).filter(
            PatientSymptom.id == patient_id,
            PatientSymptom.user_id == current_user.id
        ).first()

        if patient is None:
            raise HTTPException(
                status_code=404,
                detail="Patient record not found"
            )

        patient.age = updated_data.age
        patient.gender = updated_data.gender
        patient.symptoms = json.dumps(updated_data.symptoms)
        patient.duration_days = updated_data.duration_days
        patient.additional_notes = updated_data.additional_notes

        db.commit()
        db.refresh(patient)

        return {
            "message": "Patient record updated successfully",
            "patient_id": patient.id
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update patient record"
        )

    finally:
        db.close()

        # Delete patient record

@app.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: int,
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()

    try:
        patient = db.query(PatientSymptom).filter(
            PatientSymptom.id == patient_id,
            PatientSymptom.user_id == current_user.id
        ).first()

        if patient is None:
            raise HTTPException(
                status_code=404,
                detail="Patient record not found"
            )

        db.delete(patient)
        db.commit()

        return {
            "message": "Patient record deleted successfully",
            "patient_id": patient_id
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to delete patient record"
        )

    finally:
        db.close()

        # Analyze patient symptoms
@app.post("/analyze-symptoms")
def analyze_patient_symptoms(patient: SymptomRequest):

    analysis = analyze_symptoms(patient.symptoms)

    return {
        "message": "Symptom analysis completed",
        "age": patient.age,
        "symptoms": patient.symptoms,
        "duration_days": patient.duration_days,
        "analysis": analysis
    }
@app.post("/predict")
def predict_patient_outcome(patient: SymptomRequest):

    # 1. Convert submitted symptoms into model features
    symptoms = [
        symptom.lower().strip()
        for symptom in patient.symptoms
    ]

    # 2. Validate and normalize gender
    gender = (patient.gender or "").strip().lower()

    if gender not in ["female", "male"]:
        raise HTTPException(
            status_code=422,
            detail="Gender must be Female or Male."
        )

    gender = gender.capitalize()

    # 3. Validate blood pressure
    blood_pressure = patient.blood_pressure.strip().capitalize()

    if blood_pressure not in ["Low", "Normal", "High"]:
        raise HTTPException(
            status_code=422,
            detail="Blood pressure must be Low, Normal, or High."
        )

    # 4. Validate cholesterol
    cholesterol = patient.cholesterol_level.strip().capitalize()

    if cholesterol not in ["Low", "Normal", "High"]:
        raise HTTPException(
            status_code=422,
            detail="Cholesterol level must be Low, Normal, or High."
        )

    # 5. Prepare patient data for prediction
    patient_data = {
        "Fever": "Yes" if "fever" in symptoms else "No",
        "Cough": "Yes" if "cough" in symptoms else "No",
        "Fatigue": "Yes" if "fatigue" in symptoms else "No",
        "Difficulty Breathing": (
            "Yes" if "difficulty breathing" in symptoms else "No"
        ),
        "Age": patient.age,
        "Gender": gender,
        "Blood Pressure": blood_pressure,
        "Cholesterol Level": cholesterol
    }

    # 6. Generate prediction
    result = predict_outcome(patient_data)

    # 7. Return response
    return {
        "message": "Prediction completed",
        "patient_age": patient.age,
        "gender": gender,
        "symptoms": patient.symptoms,
        "blood_pressure": blood_pressure,
        "cholesterol_level": cholesterol,
        "prediction_result": result,
        "notice": (
            "Educational demonstration only. "
            "Not a medical diagnosis."
        )
    }
