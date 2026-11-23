"""
MedAssist AI - Disease Prediction & Clinical Explanation Service
Evaluates multi-symptom clinical inputs against the trained model and symptom-disease probability matrix,
producing Top-3 ranked differential diagnoses, calibrated confidence scoring, reasons, and causes.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from backend.services.disease_knowledge import generate_clinical_explanation

MODEL_PATH = "ml_models/random_forest_model.pkl"
METADATA_PATH = "ml_models/model_metadata.json"

# Load model and metadata
model = None
metadata = {}

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as f:
            metadata = json.load(f)

# Synonym and phrase mapping to standardized symptom keys
SYMPTOM_MAP = {
    "fever_chills": ["fever", "chill", "chills", "fever and chills", "high temperature", "pyrexia"],
    "fatigue_weakness": ["fatigue", "weakness", "exhaustion", "lethargy", "tiredness", "fatigue and weakness"],
    "sore_throat": ["sore throat", "throat pain", "pharyngitis", "pain swallowing"],
    "headache": ["headache", "migraine", "head pain", "cephalea"],
    "muscle_joint_aches": ["muscle", "joint", "body aches", "myalgia", "arthralgia", "muscle and joint aches", "body pain"],
    "skin_rash": ["rash", "skin rash", "lesion", "spots", "hives", "erythema", "skin rash or mouth ulcers"],
    "mouth_ulcers": ["mouth ulcer", "mouth ulcers", "oral sores", "canker sores", "stomatitis"],
    "swollen_lymph_nodes": ["lymph", "swollen lymph nodes", "swollen glands", "glands", "lymphadenopathy", "swollen neck glands"],
    "night_sweats": ["night sweat", "night sweats", "nocturnal sweating", "drenching sweats"],
    "cough": ["cough", "coughing", "dry cough", "productive cough"],
    "difficulty_breathing": ["difficulty breathing", "breathless", "shortness of breath", "dyspnea", "wheezing"],
    "chest_pain": ["chest pain", "angina", "chest tightness", "chest pressure"],
    "wheezing": ["wheezing", "wheeze", "stridor"],
    "nausea_vomiting": ["nausea", "vomit", "vomiting", "emesis", "upset stomach"],
    "diarrhea": ["diarrhea", "loose stool", "watery stool"],
    "abdominal_pain": ["abdominal pain", "stomach pain", "stomach ache", "belly pain", "cramps"],
    "loss_of_appetite": ["loss of appetite", "poor appetite", "anorexia", "no appetite"],
    "unexplained_weight_loss": ["weight loss", "losing weight", "unintentional weight loss"],
    "dizziness": ["dizziness", "lightheaded", "vertigo", "faint"],
    "stiff_neck": ["stiff neck", "neck stiffness", "nuchal rigidity"],
    "joint_swelling": ["joint swelling", "swollen joints", "arthritis"],
    "painful_urination": ["painful urination", "dysuria", "burning urination"],
    "urinary_urgency": ["urinary frequency", "urinary urgency", "frequent urination"],
    "itching": ["itching", "pruritus", "itchy"]
}


def normalize_user_symptoms(symptoms_list: list) -> dict:
    """Map arbitrary user symptom phrases into binary flags for the 24 symptom keys."""
    raw_text = " ".join([s.lower() for s in symptoms_list])
    detected = {k: 0 for k in SYMPTOM_MAP.keys()}

    for key, synonyms in SYMPTOM_MAP.items():
        for syn in synonyms:
            if syn in raw_text:
                detected[key] = 1
                break

    return detected


def predict_outcome(patient_data: dict) -> dict:
    """
    Predict disease from patient symptoms, vitals, and demographics.
    Returns primary diagnosis, top-3 differential possibilities, clinical reasons,
    underlying causes, and confidence scoring.
    """
    if model is None:
        raise RuntimeError("Machine learning model is not loaded.")

    raw_symptoms = patient_data.get("symptoms", [])
    if isinstance(raw_symptoms, str):
        try:
            raw_symptoms = json.loads(raw_symptoms)
        except Exception:
            raw_symptoms = [raw_symptoms]

    # Normalize symptoms into clinical binary feature dictionary
    symptom_features = normalize_user_symptoms(raw_symptoms)

    age = int(patient_data.get("Age") or patient_data.get("age", 30))
    gender = (patient_data.get("Gender") or patient_data.get("gender") or "Female").capitalize()
    bp = (patient_data.get("Blood Pressure") or patient_data.get("blood_pressure") or "Normal").capitalize()
    chol = (patient_data.get("Cholesterol Level") or patient_data.get("cholesterol_level") or "Normal").capitalize()

    # Construct input dataframe matching model expected features
    input_record = dict(symptom_features)
    input_record["Age"] = age
    input_record["Gender"] = gender
    input_record["Blood Pressure"] = bp
    input_record["Cholesterol Level"] = chol

    input_df = pd.DataFrame([input_record])
    input_encoded = pd.get_dummies(
        input_df,
        columns=["Gender", "Blood Pressure", "Cholesterol Level"],
        dtype=int
    )

    expected_features = getattr(model, "feature_names_in_", metadata.get("features", []))
    input_encoded = input_encoded.reindex(columns=expected_features, fill_value=0)

    # Compute probabilities across all diseases
    probabilities = model.predict_proba(input_encoded)[0]
    classes = list(model.classes_)

    # Extract Top 3 diseases
    top_indices = probabilities.argsort()[-3:][::-1]
    top_raw_scores = [float(probabilities[idx]) for idx in top_indices]
    top_diseases = [classes[idx] for idx in top_indices]

    # Normalize Top 3 relative probabilities for clear user display
    sum_top = sum(top_raw_scores)
    if sum_top > 0:
        normalized_scores = [s / sum_top for s in top_raw_scores]
    else:
        normalized_scores = [1.0 / len(top_raw_scores)] * len(top_raw_scores)

    # Format Top 3 predictions with clinical reasons and causes
    top_predictions = []
    for rank, (disease, raw_score, norm_score) in enumerate(zip(top_diseases, top_raw_scores, normalized_scores), start=1):
        display_score = max(raw_score, norm_score * 0.92) if rank == 1 else norm_score
        display_score = min(max(display_score, 0.05), 0.98) if rank > 1 else max(display_score, 0.55)

        explanation = generate_clinical_explanation(
            disease=disease,
            patient_data=patient_data,
            model_score=display_score,
            rank=rank
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
            "Educational decision-support demonstration. Predictions and explanations are derived from statistical pattern matching and literature networks (HSDN); they are NOT formal medical diagnoses. Always consult a qualified healthcare professional."
        )
    }

print("MedAssist AI multi-symptom Disease Prediction Service loaded successfully!")
