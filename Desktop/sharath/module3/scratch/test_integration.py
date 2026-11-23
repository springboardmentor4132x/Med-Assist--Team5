from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

cases = [
    {
        "name": "Respiratory Case",
        "payload": {
            "age": 28,
            "gender": "Female",
            "symptoms": ["cough", "difficulty breathing"],
            "duration_days": 4,
            "blood_pressure": "Normal",
            "cholesterol_level": "Normal",
            "additional_notes": "Nighttime wheezing"
        }
    },
    {
        "name": "Febrile Viral Case",
        "payload": {
            "age": 35,
            "gender": "Male",
            "symptoms": ["fever", "fatigue"],
            "duration_days": 3,
            "blood_pressure": "Normal",
            "cholesterol_level": "Normal"
        }
    },
    {
        "name": "Cardiovascular / Senior Case",
        "payload": {
            "age": 68,
            "gender": "Male",
            "symptoms": ["fatigue"],
            "duration_days": 14,
            "blood_pressure": "High",
            "cholesterol_level": "High"
        }
    }
]

print("=== RUNNING MEDASSIST AI END-TO-END PREDICTION INTEGRATION TESTS ===\n")
all_passed = True

for case in cases:
    print(f"--- Test Case: {case['name']} ---")
    resp = client.post("/predict", json=case["payload"])
    if resp.status_code != 200:
        print(f"FAILED with status {resp.status_code}: {resp.text}")
        all_passed = False
        continue

    data = resp.json()
    disease = data.get("predicted_disease")
    confidence = data.get("confidence")
    reason = data.get("clinical_reason")
    cause = data.get("cause_of_disease")
    top3 = data.get("top_predictions", [])

    print(f"Status: {resp.status_code} OK")
    print(f"Predicted Disease: {disease}")
    print(f"Confidence Tier: {confidence}")
    print(f"Clinical Reason: {reason}")
    print(f"Underlying Cause: {cause}")
    print("Differential Diagnoses (Top 3):")
    for item in top3:
        print(f"  #{item['rank']} {item['disease']} ({item['probability_percent']}) - {item['category']}")

    # Validation checks
    assert disease is not None, "Disease must not be None"
    assert reason is not None and len(reason) > 10, "Clinical reason must be populated"
    assert cause is not None and len(cause) > 10, "Cause must be populated"
    assert len(top3) == 3, "Top 3 predictions must have exactly 3 items"
    print("All assertions passed!\n")

if all_passed:
    print(">>> ALL 3 INTEGRATION TEST CASES PASSED SUCCESSFULLY! <<<")
else:
    print(">>> SOME TESTS FAILED <<<")
