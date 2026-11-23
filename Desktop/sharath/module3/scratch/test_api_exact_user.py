from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

response = client.post("/predict", json={
    "patient_name": "Karthikeya",
    "age": 28,
    "gender": "Male",
    "symptoms": [
        "Fever and chills",
        "Fatigue and weakness",
        "Sore throat, headache, or muscle and joint aches",
        "Skin rash or mouth ulcers",
        "Swollen lymph nodes (glands) and night sweats"
    ],
    "duration_days": 10,
    "blood_pressure": "Normal",
    "cholesterol_level": "Normal",
    "severity": "Moderate",
    "onset": "Acute",
    "additional_notes": "Flu-like symptoms persisting for over a week"
})

print("API Status:", response.status_code)
data = response.json()
print("Patient Name:", data.get("patient_name"))
print("Predicted Disease:", data.get("predicted_disease"))
print("Confidence:", data.get("confidence"))
print("Clinical Reason:", data.get("clinical_reason"))
print("Cause:", data.get("cause_of_disease"))
print("Top 3 Predictions:")
for item in data.get("top_predictions", []):
    print(f"  #{item['rank']} {item['disease']} ({item['probability_percent']}) - {item['category']}")
