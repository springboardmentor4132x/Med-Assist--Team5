# MedAssist AI - Symptom Analyzer

def analyze_symptoms(symptoms):

    possible_conditions = []

    # Convert symptoms to lowercase
    symptoms = [symptom.lower().strip() for symptom in symptoms]

    # Example symptom patterns for demonstration only
    if "fever" in symptoms and "headache" in symptoms:
        possible_conditions.append("Fever with headache - needs clinical assessment")

    if "cough" in symptoms and "sore throat" in symptoms:
        possible_conditions.append("Respiratory symptoms - needs clinical assessment")

    if "vomiting" in symptoms and "diarrhea" in symptoms:
        possible_conditions.append("Gastrointestinal symptoms - needs clinical assessment")

    if not possible_conditions:
        possible_conditions.append(
            "No matching demonstration pattern found. Consult a healthcare professional."
        )

    return {
        "possible_conditions": possible_conditions,
        "notice": "This is an educational demonstration, not a medical diagnosis."
    }
