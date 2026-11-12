
import joblib
import pandas as pd

# Load the saved Random Forest model
model = joblib.load("ml_models/random_forest_model.pkl")

# Get the exact feature columns used during training
MODEL_FEATURES = list(model.feature_names_in_)


def predict_outcome(patient_data):

    # Convert patient information into a DataFrame
    input_df = pd.DataFrame([patient_data])

    # Apply categorical encoding
    input_encoded = pd.get_dummies(
        input_df,
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

    # Match the training feature columns
    input_encoded = input_encoded.reindex(
        columns=MODEL_FEATURES,
        fill_value=0
    )

    # Generate prediction
    prediction = model.predict(input_encoded)[0]

    return {
        "prediction": "Positive" if prediction == 1 else "Negative",
        "notice": (
            "Educational demonstration only. "
            "Not a medical diagnosis."
        )
    }


print("MedAssist AI prediction service loaded successfully!")
