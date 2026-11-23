from backend.services.predict import predict_outcome

user_input_symptoms = [
    "Fever and chills",
    "Fatigue and weakness",
    "Sore throat, headache, or muscle and joint aches",
    "Skin rash or mouth ulcers",
    "Swollen lymph nodes (glands) and night sweats"
]

res = predict_outcome({
    "patient_name": "Karthikeya",
    "symptoms": user_input_symptoms,
    "Age": 28,
    "Gender": "Male",
    "Blood Pressure": "Normal",
    "Cholesterol Level": "Normal",
    "duration_days": 10
})

print("Patient Name:", res.get("patient_name"))
print("Primary Disease:", res["primary_prediction"]["disease"])
print("Probability:", res["primary_prediction"]["probability_percent"])
print("Confidence:", res["primary_prediction"]["confidence_tier"])
print("Clinical Reason:", res["primary_prediction"]["clinical_reason"])
print("Cause of Disease:", res["primary_prediction"]["cause"])
print("\nDifferential Diagnoses (Top 3):")
for p in res["top_predictions"]:
    print(f" #{p['rank']}: {p['disease']} ({p['probability_percent']}) | Category: {p['category']}")
