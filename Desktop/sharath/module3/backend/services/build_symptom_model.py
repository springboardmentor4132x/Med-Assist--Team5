"""
MedAssist AI - Expanded Symptom-Disease Training & Modeling Service
Constructs a comprehensive clinical dataset grounded in the Human Symptoms-Disease Network (HSDN)
literature and trains a high-precision multi-class disease probability model supporting 24+ symptom dimensions.
"""

import os
import json
import random
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Standard clinical symptom keys
SYMPTOM_KEYS = [
    "fever_chills",
    "fatigue_weakness",
    "sore_throat",
    "headache",
    "muscle_joint_aches",
    "skin_rash",
    "mouth_ulcers",
    "swollen_lymph_nodes",
    "night_sweats",
    "cough",
    "difficulty_breathing",
    "chest_pain",
    "wheezing",
    "nausea_vomiting",
    "diarrhea",
    "abdominal_pain",
    "loss_of_appetite",
    "unexplained_weight_loss",
    "dizziness",
    "stiff_neck",
    "joint_swelling",
    "painful_urination",
    "urinary_urgency",
    "itching"
]

# Clinical disease symptom profiles (grounded in medical nosology and HSDN network)
DISEASE_PROFILES = {
    "Acute HIV Infection": {
        "category": "Infectious Disease / Retroviral",
        "primary_symptoms": ["fever_chills", "fatigue_weakness", "sore_throat", "headache", "muscle_joint_aches", "skin_rash", "mouth_ulcers", "swollen_lymph_nodes", "night_sweats"],
        "secondary_symptoms": ["loss_of_appetite", "diarrhea", "nausea_vomiting"],
        "age_range": (18, 60),
        "typical_duration": (7, 28)
    },
    "Infectious Mononucleosis": {
        "category": "Viral Infection (EBV)",
        "primary_symptoms": ["fever_chills", "fatigue_weakness", "sore_throat", "swollen_lymph_nodes", "headache", "muscle_joint_aches"],
        "secondary_symptoms": ["loss_of_appetite", "skin_rash", "night_sweats"],
        "age_range": (15, 35),
        "typical_duration": (7, 21)
    },
    "Other Viral or Bacterial Infections": {
        "category": "Systemic Infection",
        "primary_symptoms": ["fever_chills", "fatigue_weakness", "muscle_joint_aches", "headache", "sore_throat"],
        "secondary_symptoms": ["skin_rash", "loss_of_appetite", "nausea_vomiting", "swollen_lymph_nodes"],
        "age_range": (10, 75),
        "typical_duration": (3, 14)
    },
    "Influenza": {
        "category": "Viral Respiratory Infection",
        "primary_symptoms": ["fever_chills", "fatigue_weakness", "cough", "headache", "muscle_joint_aches"],
        "secondary_symptoms": ["sore_throat", "loss_of_appetite", "difficulty_breathing"],
        "age_range": (5, 80),
        "typical_duration": (3, 10)
    },
    "Common Cold": {
        "category": "Upper Respiratory Tract Infection",
        "primary_symptoms": ["cough", "sore_throat", "fatigue_weakness"],
        "secondary_symptoms": ["headache", "fever_chills"],
        "age_range": (2, 85),
        "typical_duration": (4, 10)
    },
    "Streptococcal Pharyngitis": {
        "category": "Bacterial Throat Infection",
        "primary_symptoms": ["sore_throat", "fever_chills", "swollen_lymph_nodes", "headache"],
        "secondary_symptoms": ["nausea_vomiting", "fatigue_weakness", "mouth_ulcers"],
        "age_range": (5, 45),
        "typical_duration": (3, 7)
    },
    "Pneumonia": {
        "category": "Lower Respiratory Infection",
        "primary_symptoms": ["fever_chills", "cough", "difficulty_breathing", "chest_pain", "fatigue_weakness"],
        "secondary_symptoms": ["loss_of_appetite", "headache", "nausea_vomiting"],
        "age_range": (15, 85),
        "typical_duration": (5, 21)
    },
    "Bronchitis": {
        "category": "Respiratory Inflammation",
        "primary_symptoms": ["cough", "difficulty_breathing", "fatigue_weakness", "fever_chills"],
        "secondary_symptoms": ["chest_pain", "sore_throat", "headache"],
        "age_range": (10, 75),
        "typical_duration": (5, 18)
    },
    "Asthma": {
        "category": "Chronic Airway Disorder",
        "primary_symptoms": ["difficulty_breathing", "cough", "wheezing", "chest_pain"],
        "secondary_symptoms": ["fatigue_weakness"],
        "age_range": (5, 65),
        "typical_duration": (1, 30)
    },
    "Chronic Obstructive Pulmonary Disease (COPD)": {
        "category": "Chronic Respiratory Disease",
        "primary_symptoms": ["difficulty_breathing", "cough", "fatigue_weakness", "wheezing"],
        "secondary_symptoms": ["chest_pain", "unexplained_weight_loss"],
        "age_range": (45, 85),
        "typical_duration": (14, 180)
    },
    "COVID-19 / Acute Respiratory Syndrome": {
        "category": "Viral Respiratory Syndrome",
        "primary_symptoms": ["fever_chills", "cough", "fatigue_weakness", "difficulty_breathing", "headache"],
        "secondary_symptoms": ["muscle_joint_aches", "sore_throat", "loss_of_appetite", "diarrhea"],
        "age_range": (10, 85),
        "typical_duration": (5, 21)
    },
    "Tuberculosis": {
        "category": "Chronic Mycobacterial Infection",
        "primary_symptoms": ["cough", "night_sweats", "fever_chills", "unexplained_weight_loss", "fatigue_weakness"],
        "secondary_symptoms": ["chest_pain", "loss_of_appetite", "difficulty_breathing"],
        "age_range": (18, 75),
        "typical_duration": (21, 120)
    },
    "Dengue Fever": {
        "category": "Arboviral Infection",
        "primary_symptoms": ["fever_chills", "headache", "muscle_joint_aches", "skin_rash", "fatigue_weakness"],
        "secondary_symptoms": ["nausea_vomiting", "loss_of_appetite", "swollen_lymph_nodes"],
        "age_range": (10, 65),
        "typical_duration": (4, 12)
    },
    "Malaria": {
        "category": "Parasitic Infection",
        "primary_symptoms": ["fever_chills", "night_sweats", "fatigue_weakness", "headache", "muscle_joint_aches"],
        "secondary_symptoms": ["nausea_vomiting", "loss_of_appetite", "diarrhea"],
        "age_range": (5, 70),
        "typical_duration": (4, 14)
    },
    "Typhoid Fever": {
        "category": "Enteric Bacterial Infection",
        "primary_symptoms": ["fever_chills", "headache", "abdominal_pain", "fatigue_weakness", "loss_of_appetite"],
        "secondary_symptoms": ["diarrhea", "skin_rash", "muscle_joint_aches"],
        "age_range": (5, 60),
        "typical_duration": (7, 21)
    },
    "Gastroenteritis": {
        "category": "Gastrointestinal Infection",
        "primary_symptoms": ["nausea_vomiting", "diarrhea", "abdominal_pain", "fatigue_weakness"],
        "secondary_symptoms": ["fever_chills", "loss_of_appetite", "headache"],
        "age_range": (5, 75),
        "typical_duration": (2, 7)
    },
    "Appendicitis": {
        "category": "Acute Abdominal Emergency",
        "primary_symptoms": ["abdominal_pain", "nausea_vomiting", "fever_chills", "loss_of_appetite"],
        "secondary_symptoms": ["fatigue_weakness"],
        "age_range": (10, 50),
        "typical_duration": (1, 4)
    },
    "Crohn's Disease": {
        "category": "Inflammatory Bowel Disease",
        "primary_symptoms": ["abdominal_pain", "diarrhea", "unexplained_weight_loss", "fatigue_weakness", "fever_chills"],
        "secondary_symptoms": ["mouth_ulcers", "joint_swelling", "loss_of_appetite"],
        "age_range": (15, 60),
        "typical_duration": (14, 120)
    },
    "Ulcerative Colitis": {
        "category": "Inflammatory Bowel Disease",
        "primary_symptoms": ["diarrhea", "abdominal_pain", "fatigue_weakness", "unexplained_weight_loss"],
        "secondary_symptoms": ["fever_chills", "loss_of_appetite"],
        "age_range": (18, 65),
        "typical_duration": (14, 120)
    },
    "Urinary Tract Infection (UTI)": {
        "category": "Urological Infection",
        "primary_symptoms": ["painful_urination", "urinary_urgency", "fever_chills"],
        "secondary_symptoms": ["abdominal_pain", "fatigue_weakness", "nausea_vomiting"],
        "age_range": (18, 75),
        "typical_duration": (2, 7)
    },
    "Measles": {
        "category": "Viral Exanthem",
        "primary_symptoms": ["fever_chills", "skin_rash", "cough", "mouth_ulcers", "sore_throat"],
        "secondary_symptoms": ["headache", "fatigue_weakness", "loss_of_appetite"],
        "age_range": (2, 30),
        "typical_duration": (7, 14)
    },
    "Chickenpox": {
        "category": "Herpesvirus Exanthem",
        "primary_symptoms": ["fever_chills", "skin_rash", "itching", "fatigue_weakness", "loss_of_appetite"],
        "secondary_symptoms": ["headache", "muscle_joint_aches"],
        "age_range": (2, 35),
        "typical_duration": (5, 14)
    },
    "Lyme Disease": {
        "category": "Tick-Borne Borrelia Infection",
        "primary_symptoms": ["skin_rash", "fever_chills", "fatigue_weakness", "headache", "muscle_joint_aches"],
        "secondary_symptoms": ["swollen_lymph_nodes", "joint_swelling", "stiff_neck"],
        "age_range": (10, 70),
        "typical_duration": (7, 30)
    },
    "Systemic Lupus Erythematosus (SLE)": {
        "category": "Systemic Autoimmune Disease",
        "primary_symptoms": ["skin_rash", "muscle_joint_aches", "joint_swelling", "fatigue_weakness", "mouth_ulcers", "fever_chills"],
        "secondary_symptoms": ["chest_pain", "headache", "unexplained_weight_loss"],
        "age_range": (15, 55),
        "typical_duration": (14, 180)
    },
    "Rheumatoid Arthritis": {
        "category": "Autoimmune Arthropathy",
        "primary_symptoms": ["joint_swelling", "muscle_joint_aches", "fatigue_weakness"],
        "secondary_symptoms": ["fever_chills", "loss_of_appetite"],
        "age_range": (30, 75),
        "typical_duration": (30, 365)
    },
    "Migraine": {
        "category": "Neurological Disorder",
        "primary_symptoms": ["headache", "nausea_vomiting", "dizziness", "fatigue_weakness"],
        "secondary_symptoms": ["stiff_neck"],
        "age_range": (15, 60),
        "typical_duration": (1, 4)
    },
    "Hypertension": {
        "category": "Cardiovascular Disorder",
        "primary_symptoms": ["headache", "dizziness", "fatigue_weakness"],
        "secondary_symptoms": ["chest_pain", "difficulty_breathing"],
        "age_range": (35, 85),
        "typical_duration": (30, 365)
    },
    "Coronary Artery Disease": {
        "category": "Cardiovascular Disorder",
        "primary_symptoms": ["chest_pain", "difficulty_breathing", "fatigue_weakness"],
        "secondary_symptoms": ["dizziness", "nausea_vomiting"],
        "age_range": (45, 85),
        "typical_duration": (14, 180)
    },
    "Stroke": {
        "category": "Cerebrovascular Emergency",
        "primary_symptoms": ["headache", "dizziness", "fatigue_weakness"],
        "secondary_symptoms": ["difficulty_breathing", "nausea_vomiting"],
        "age_range": (50, 90),
        "typical_duration": (1, 7)
    },
    "Diabetes Mellitus": {
        "category": "Metabolic Disorder",
        "primary_symptoms": ["fatigue_weakness", "unexplained_weight_loss"],
        "secondary_symptoms": ["dizziness", "headache", "nausea_vomiting"],
        "age_range": (25, 85),
        "typical_duration": (30, 365)
    },
    "Osteoporosis": {
        "category": "Musculoskeletal Degeneration",
        "primary_symptoms": ["muscle_joint_aches", "fatigue_weakness"],
        "secondary_symptoms": ["joint_swelling"],
        "age_range": (55, 90),
        "typical_duration": (60, 365)
    },
    "Allergic Rhinitis": {
        "category": "Allergic Atopic Condition",
        "primary_symptoms": ["cough", "headache", "fatigue_weakness", "itching"],
        "secondary_symptoms": ["sore_throat"],
        "age_range": (5, 65),
        "typical_duration": (7, 60)
    },
    "Sinusitis": {
        "category": "Upper Respiratory Sinus Infection",
        "primary_symptoms": ["headache", "fever_chills", "cough", "sore_throat"],
        "secondary_symptoms": ["fatigue_weakness", "dizziness"],
        "age_range": (10, 75),
        "typical_duration": (7, 21)
    }
}


def generate_synthetic_dataset(samples_per_disease=35, random_seed=42):
    random.seed(random_seed)
    np.random.seed(random_seed)

    rows = []
    for disease, profile in DISEASE_PROFILES.items():
        primary = profile["primary_symptoms"]
        secondary = profile["secondary_symptoms"]
        min_age, max_age = profile["age_range"]
        min_dur, max_dur = profile["typical_duration"]

        for _ in range(samples_per_disease):
            row = {"Disease": disease}

            # Sample age and duration
            row["Age"] = random.randint(min_age, max_age)
            row["Gender"] = random.choice(["Female", "Male"])
            row["duration_days"] = random.randint(min_dur, max_dur)
            row["Blood Pressure"] = random.choices(["Normal", "High", "Low"], weights=[0.65, 0.25, 0.10])[0]
            row["Cholesterol Level"] = random.choices(["Normal", "High", "Low"], weights=[0.65, 0.25, 0.10])[0]

            # Primary symptoms have 85-98% chance of being active
            for s in SYMPTOM_KEYS:
                if s in primary:
                    row[s] = 1 if random.random() < 0.92 else 0
                elif s in secondary:
                    row[s] = 1 if random.random() < 0.40 else 0
                else:
                    # Occasional background noise symptom
                    row[s] = 1 if random.random() < 0.04 else 0

            # Ensure at least 2 symptoms are present
            active_count = sum(row[s] for s in SYMPTOM_KEYS)
            if active_count < 2:
                for p in primary[:2]:
                    row[p] = 1

            rows.append(row)

    df = pd.DataFrame(rows)
    return df


def train_and_save_expanded_model():
    df = generate_synthetic_dataset(samples_per_disease=40)
    csv_path = "dataset/expanded_symptom_disease_dataset.csv"
    df.to_csv(csv_path, index=False)
    print(f"Generated expanded dataset: {df.shape[0]} samples, {df.shape[1]} columns, {df['Disease'].nunique()} diseases.")

    feature_cols = SYMPTOM_KEYS + ["Age", "Gender", "Blood Pressure", "Cholesterol Level"]
    X = df[feature_cols]
    y = df["Disease"]

    X_encoded = pd.get_dummies(
        X,
        columns=["Gender", "Blood Pressure", "Cholesterol Level"],
        dtype=int
    )

    clf = RandomForestClassifier(
        n_estimators=300,
        max_depth=20,
        min_samples_split=2,
        random_state=42
    )
    clf.fit(X_encoded, y)

    # Calculate Top-1, Top-3, Top-5 Accuracy
    probs = clf.predict_proba(X_encoded)
    classes = clf.classes_

    top1 = sum(y.iloc[i] == classes[np.argmax(probs[i])] for i in range(len(y))) / len(y)
    top3 = sum(y.iloc[i] in classes[probs[i].argsort()[-3:]] for i in range(len(y))) / len(y)
    top5 = sum(y.iloc[i] in classes[probs[i].argsort()[-5:]] for i in range(len(y))) / len(y)

    print(f"Expanded Model Top-1 Accuracy: {top1:.2%}")
    print(f"Expanded Model Top-3 Accuracy: {top3:.2%}")
    print(f"Expanded Model Top-5 Accuracy: {top5:.2%}")

    os.makedirs("ml_models", exist_ok=True)
    joblib.dump(clf, "ml_models/random_forest_model.pkl")

    metadata = {
        "features": list(X_encoded.columns),
        "symptom_keys": SYMPTOM_KEYS,
        "classes": list(classes),
        "diseases_count": len(classes)
    }
    with open("ml_models/model_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print("Model and metadata saved successfully!")
    return clf


if __name__ == "__main__":
    train_and_save_expanded_model()
