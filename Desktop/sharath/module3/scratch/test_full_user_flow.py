from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

print("=== TESTING COMPLETE MEDASSIST AI WORKFLOW ===\n")

# 1. Register / Login user
login_resp = client.post("/auth/login", json={
    "email": "testuser@medassist.ai",
    "password": "Password123!"
})

if login_resp.status_code != 200:
    # Register if not existing
    reg_resp = client.post("/auth/register", json={
        "full_name": "Karthikeya",
        "email": "testuser@medassist.ai",
        "password": "Password123!"
    })
    print("Registration Status:", reg_resp.status_code)
    login_resp = client.post("/auth/login", json={
        "email": "testuser@medassist.ai",
        "password": "Password123!"
    })

token = login_resp.json().get("access_token")
print("Login successful! Token acquired.")

# 2. Submit symptoms with Patient Name & Multi-Symptom Constellation
user_symptoms = [
    "Fever and chills",
    "Fatigue and weakness",
    "Sore throat, headache, or muscle and joint aches",
    "Skin rash or mouth ulcers",
    "Swollen lymph nodes (glands) and night sweats"
]

save_payload = {
    "patient_name": "Karthikeya",
    "age": 28,
    "gender": "Male",
    "symptoms": user_symptoms,
    "duration_days": 10,
    "blood_pressure": "Normal",
    "cholesterol_level": "Normal",
    "severity": "Moderate",
    "onset": "Acute",
    "additional_notes": "Night sweats, swollen lymph nodes in neck, mouth ulcers"
}

save_resp = client.post("/symptoms", json=save_payload, headers={"Authorization": f"Bearer {token}"})
print("\nSubmit Symptoms Status:", save_resp.status_code)
assert save_resp.status_code == 200, "Saving symptoms must succeed"
saved_data = save_resp.json()
print("Saved Patient ID:", saved_data.get("patient_id"))
print("Saved Patient Name:", saved_data.get("patient_details", {}).get("patient_name"))

# 3. Retrieve Patient Records
records_resp = client.get("/patients", headers={"Authorization": f"Bearer {token}"})
print("\nGet Patients Status:", records_resp.status_code)
assert records_resp.status_code == 200
records = records_resp.json().get("patients", [])
print(f"Total Patient Records for User: {len(records)}")
latest = records[0]
print(f"Latest Record: #{latest['id']} - Name: {latest.get('patient_name')}")
print(f"Symptoms Count in Record: {len(latest.get('symptoms', []))}")

# 4. Predict Disease using the Exact User Constellation
predict_resp = client.post("/predict", json=save_payload)
print("\nPrediction Status:", predict_resp.status_code)
assert predict_resp.status_code == 200
pred_data = predict_resp.json()

print("\n--- PREDICTION OUTPUT ---")
print("Patient Name:", pred_data.get("patient_name"))
print("Primary Disease:", pred_data.get("predicted_disease"))
print("Confidence:", pred_data.get("confidence"))
print("Clinical Reason:", pred_data.get("clinical_reason"))
print("Cause of Disease:", pred_data.get("cause_of_disease"))
print("\nTop 3 Differential Diagnoses:")
for p in pred_data.get("top_predictions", []):
    print(f"  Rank #{p['rank']}: {p['disease']} ({p['probability_percent']}) | Category: {p['category']}")

# Verification assertions
assert pred_data.get("predicted_disease") in ["Acute HIV Infection", "Infectious Mononucleosis", "Other Viral or Bacterial Infections"], "Primary disease must match expected differential"
diff_diseases = [p["disease"] for p in pred_data.get("top_predictions", [])]
print("\nDifferential includes:")
for d in diff_diseases:
    print(f" - {d}")

print("\n>>> ALL TESTS PASSED WITH 100% SUCCESS! <<<")
