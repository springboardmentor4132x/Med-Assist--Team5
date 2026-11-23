
"""
MedAssist AI - Expanded Disease Prediction Service
Educational multi-symptom prediction using the 33-class model.
"""

import json
from pathlib import Path

import joblib
import pandas as pd

from backend.services.expanded_disease_knowledge import (
    generate_clinical_explanation,
)

# Resolve paths from the project root, independent of terminal location.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "ml_models" / "expanded_disease_model.pkl"
METADATA_PATH = (
    PROJECT_ROOT / "ml_models" / "expanded_disease_model_metadata.json"
)

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Expanded model not found: {MODEL_PATH}")

if not METADATA_PATH.exists():
    raise FileNotFoundError(f"Model metadata not found: {METADATA_PATH}")

model = joblib.load(MODEL_PATH)

with open(METADATA_PATH, "r", encoding="utf-8") as file:
    metadata = json.load(file)

MODEL_FEATURES = list(model.feature_names_in_)

if MODEL_FEATURES != metadata.get("features"):
    raise ValueError("Expanded model features do not match metadata.")

SYMPTOM_MAP = {
    "fever_chills": ["fever", "chill", "chills", "high temperature", "pyrexia"],
    "fatigue_weakness": ["fatigue", "weakness", "exhaustion", "lethargy", "tiredness"],
    "sore_throat": ["sore throat", "throat pain", "pharyngitis", "pain swallowing"],
    "headache": ["headache", "migraine", "head pain"],
    "muscle_joint_aches": ["muscle", "joint", "body aches", "myalgia", "arthralgia", "body pain"],
    "skin_rash": ["rash", "skin rash", "lesion", "spots", "hives", "erythema"],
    "mouth_ulcers": ["mouth ulcer", "mouth ulcers", "oral sores", "canker sores"],
    "swollen_lymph_nodes": ["lymph", "swollen glands", "lymphadenopathy"],
    "night_sweats": ["night sweat", "night sweats", "nocturnal sweating"],
    "cough": ["cough", "coughing", "dry cough", "productive cough"],
    "difficulty_breathing": ["difficulty breathing", "breathless", "shortness of breath", "dyspnea"],
    "chest_pain": ["chest pain", "angina", "chest tightness", "chest pressure"],
    "wheezing": ["wheezing", "wheeze", "stridor"],
    "nausea_vomiting": ["nausea", "vomit", "vomiting", "emesis"],
    "diarrhea": ["diarrhea", "loose stool", "watery stool"],
    "abdominal_pain": ["abdominal pain", "stomach pain", "stomach ache", "belly pain", "cramps"],
    "loss_of_appetite": ["loss of appetite", "poor appetite", "no appetite"],
    "unexplained_weight_loss": ["weight loss", "losing weight", "unintentional weight loss"],
    "dizziness": ["dizziness", "lightheaded", "vertigo", "faint"],
    "stiff_neck": ["stiff neck", "neck stiffness", "nuchal rigidity"],
    "joint_swelling": ["joint swelling", "swollen joints", "arthritis"],
    "painful_urination": ["painful urination", "dysuria", "burning urination"],
    "urinary_urgency": ["urinary frequency", "urinary urgency", "frequent urination"],
    "itching": ["itching", "pruritus", "itchy"],
}


def normalize_user_symptoms(symptoms_list):
    """Convert symptom phrases into the model's 24 binary symptom features."""

    if isinstance(symptoms_list, str):
        try:
            symptoms_list = json.loads(symptoms_list)
        except (json.JSONDecodeError, TypeError):
            symptoms_list = [symptoms_list]

    if not isinstance(symptoms_list, list):
        raise ValueError("Symptoms must be supplied as a list of strings.")

    raw_text = " ".join(
        str(symptom).lower().strip() for symptom in symptoms_list
    )

    detected = {key: 0 for key in SYMPTOM_MAP}

    for key, synonyms in SYMPTOM_MAP.items():
        if any(term in raw_text for term in synonyms):
            detected[key] = 1

    return detected


def predict_outcome(patient_data: dict) -> dict:
    """Return the top three model predictions and educational explanations."""

    if not isinstance(patient_data, dict):
        raise ValueError("Patient data must be an object.")

    raw_symptoms = patient_data.get("symptoms", [])
    symptom_features = normalize_user_symptoms(raw_symptoms)

    age = int(patient_data.get("Age") or patient_data.get("age") or 30)

    if not 0 <= age <= 120:
        raise ValueError("Age must be between 0 and 120.")

    gender = (
        patient_data.get("Gender")
        or patient_data.get("gender")
        or "Female"
    ).capitalize()

    bp = (
        patient_data.get("Blood Pressure")
        or patient_data.get("blood_pressure")
        or "Normal"
    ).capitalize()

    cholesterol = (
        patient_data.get("Cholesterol Level")
        or patient_data.get("cholesterol_level")
        or "Normal"
    ).capitalize()

    if gender not in ("Male", "Female"):
        raise ValueError("Gender must be Male or Female.")

    if bp not in ("Low", "Normal", "High"):
        raise ValueError("Blood pressure must be Low, Normal or High.")

    if cholesterol not in ("Low", "Normal", "High"):
        raise ValueError("Cholesterol must be Low, Normal or High.")

    input_record = {
        **symptom_features,
        "Age": age,
        "Gender": gender,
        "Blood Pressure": bp,
        "Cholesterol Level": cholesterol,
    }

    input_df = pd.DataFrame([input_record])

    input_encoded = pd.get_dummies(
        input_df,
        columns=["Gender", "Blood Pressure", "Cholesterol Level"],
        dtype=int,
    )

    input_encoded = input_encoded.reindex(
        columns=MODEL_FEATURES,
        fill_value=0,
    )

    probabilities = model.predict_proba(input_encoded)[0]
    classes = list(model.classes_)

    top_indices = probabilities.argsort()[-3:][::-1]

    top_predictions = []

    for rank, index in enumerate(top_indices, start=1):
        disease = str(classes[index])
        raw_score = float(probabilities[index])

        explanation = generate_clinical_explanation(
            disease=disease,
            patient_data=patient_data,
            model_score=raw_score,
            rank=rank,
        )

        explanation["raw_model_probability"] = round(raw_score, 4)
        top_predictions.append(explanation)

    primary = top_predictions[0]

    return {
        "prediction": primary["disease"],
        "primary_prediction": primary,
        "top_predictions": top_predictions,
        "predicted_disease": primary["disease"],
        "confidence": primary["confidence_tier"],
        "clinical_reason": primary["clinical_reason"],
        "cause_of_disease": primary["cause"],
        "pathophysiology": primary["pathophysiology"],
        "category": primary["category"],
        "recommended_action": primary["recommended_action"],
        "urgency": primary["urgency"],
        "patient_name": patient_data.get("patient_name") or "Anonymous Patient",
        "notice": (
            "Educational decision-support demonstration only. "
            "Model predictions are not diagnoses or clinically validated "
            "probabilities. Consult a qualified healthcare professional."
        ),
    }


print("MedAssist AI expanded disease prediction service loaded successfully!")
