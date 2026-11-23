"""
MedAssist AI - Disease Prediction Model Training Service
Trains a multi-class Random Forest Classifier to predict Disease from clinical symptoms and patient profiles,
evaluated on Top-1, Top-3, and Top-5 accuracy in alignment with differential medical diagnosis workflows.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def train_disease_model():
    dataset_path = "dataset/cleaned_disease_dataset.csv"
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")

    df = pd.read_csv(dataset_path)
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    feature_cols = [
        "Fever",
        "Cough",
        "Fatigue",
        "Difficulty Breathing",
        "Age",
        "Gender",
        "Blood Pressure",
        "Cholesterol Level"
    ]

    X = df[feature_cols]
    y_disease = df["Disease"]
    y_outcome = df["Outcome Variable"]

    # One-hot encode categorical features
    X_encoded = pd.get_dummies(
        X,
        columns=[
            "Fever",
            "Cough",
            "Fatigue",
            "Difficulty Breathing",
            "Gender",
            "Blood Pressure",
            "Cholesterol Level"
        ],
        dtype=int
    )

    print(f"Total encoded features: {X_encoded.shape[1]}")
    print(f"Total unique disease classes: {y_disease.nunique()}")

    # 1. Train Multi-class Disease Prediction Model
    print("\n--- Training Disease Multi-Class Classifier ---")
    disease_model = RandomForestClassifier(
        n_estimators=300,
        max_depth=16,
        min_samples_split=2,
        random_state=42
    )
    disease_model.fit(X_encoded, y_disease)

    # Evaluate Top-1, Top-3, and Top-5 Accuracy
    probs = disease_model.predict_proba(X_encoded)
    classes = disease_model.classes_

    top1_correct = 0
    top3_correct = 0
    top5_correct = 0

    for i, true_label in enumerate(y_disease):
        top1_pred = classes[np.argmax(probs[i])]
        top3_preds = classes[probs[i].argsort()[-3:]]
        top5_preds = classes[probs[i].argsort()[-5:]]

        if true_label == top1_pred:
            top1_correct += 1
        if true_label in top3_preds:
            top3_correct += 1
        if true_label in top5_preds:
            top5_correct += 1

    n_samples = len(y_disease)
    print(f"Top-1 Accuracy: {top1_correct / n_samples:.2%}")
    print(f"Top-3 Accuracy: {top3_correct / n_samples:.2%}")
    print(f"Top-5 Accuracy: {top5_correct / n_samples:.2%}")

    # 2. Also train binary outcome model (for secondary risk score)
    print("\n--- Training Secondary Binary Outcome Classifier ---")
    binary_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    y_outcome_encoded = y_outcome.map({"Negative": 0, "Positive": 1})
    binary_model.fit(X_encoded, y_outcome_encoded)
    print(f"Binary Outcome Accuracy: {binary_model.score(X_encoded, y_outcome_encoded):.2%}")

    # Ensure ml_models directory exists
    os.makedirs("ml_models", exist_ok=True)

    # Save primary disease prediction model
    joblib.dump(disease_model, "ml_models/random_forest_model.pkl")
    joblib.dump(binary_model, "ml_models/binary_outcome_model.pkl")

    print("\nModels successfully saved:")
    print(" - ml_models/random_forest_model.pkl (Primary Disease Classifier)")
    print(" - ml_models/binary_outcome_model.pkl (Secondary Binary Classifier)")

if __name__ == "__main__":
    train_disease_model()
