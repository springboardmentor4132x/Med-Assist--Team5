from models import get_db
from symptom_data import SYMPTOMS, get_dataset_columns
from correlation import analyse_correlation
from history_integration import get_history_info

DISCLAIMER = (
    "This analysis only shows how the selected symptoms occur together in the dataset. "
    "It is not a medical diagnosis. Please consult a doctor for medical advice."
)


# builds the structured assessment, Module 3 (disease prediction) will use this
def build_assessment(user_id, assessment_id, symptom_keys):
    conn = get_db()
    patient = conn.execute(
        "SELECT id, full_name, age, gender FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    saved = conn.execute(
        "SELECT created_at FROM symptom_assessments WHERE id = ?", (assessment_id,)
    ).fetchone()
    conn.close()

    symptoms = []
    for key in symptom_keys:
        symptoms.append({
            "key": key,
            "label": SYMPTOMS[key],
            "dataset_columns": get_dataset_columns(key),
        })

    return {
        "assessment_id": assessment_id,
        "created_at": saved["created_at"] if saved else None,
        "patient": dict(patient) if patient else None,
        "symptoms": symptoms,
        "symptom_count": len(symptoms),
        "correlation": analyse_correlation(symptom_keys),
        "medical_history": get_history_info(user_id, symptom_keys),
        "disclaimer": DISCLAIMER,
        "ready_for_prediction": True,
    }
