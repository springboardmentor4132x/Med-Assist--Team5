

"""
MedAssist AI - Severity Evaluation Service
Module 4 | Member 1

Educational prototype only.
Rules and thresholds require mentor/clinical review.
This is NOT a medically validated triage system.
"""

# --------------------------------------------------
# PROVISIONAL RULES
# These thresholds are placeholders for software testing.
# They must be reviewed and approved before real-world use.
# --------------------------------------------------

MODERATE_SYMPTOM_COUNT = 3
SEVERE_SYMPTOM_COUNT = 5

MODERATE_DURATION_DAYS = 4
SEVERE_DURATION_DAYS = 7


def evaluate_severity(symptoms, duration_days):
    """
    Evaluate symptoms using provisional demonstration rules.

    Parameters:
        symptoms (list): Patient's reported symptoms.
        duration_days (int): Number of days symptoms have been present.

    Returns:
        dict: Severity level, explanation and notice.
    """

    # 1. Validate the symptoms input
    if not isinstance(symptoms, list):
        raise ValueError("Symptoms must be provided as a list.")

    if not symptoms:
        raise ValueError("At least one symptom is required.")

    # 2. Validate duration
    if not isinstance(duration_days, int) or isinstance(duration_days, bool):
        raise ValueError("Duration must be a whole number of days.")

    if duration_days < 1:
        raise ValueError("Duration must be at least 1 day.")

       # 3. Validate and normalize each symptom
    cleaned_symptoms = []

    for symptom in symptoms:
        if not isinstance(symptom, str):
            raise ValueError("Each symptom must be a string.")

        if not symptom.strip():
            raise ValueError("Symptom names cannot be empty.")

        cleaned_symptoms.append(symptom.strip().lower())

    # 4. Count reported symptoms
    symptom_count = len(set(cleaned_symptoms))

    # 5. Apply provisional evaluation rules
    if (
        symptom_count >= SEVERE_SYMPTOM_COUNT
        or duration_days >= SEVERE_DURATION_DAYS
    ):
        severity_level = "Severe"
        explanation = (
            "The provisional rules flagged the reported symptom count "
            "or duration for further assessment."
        )

    elif (
        symptom_count >= MODERATE_SYMPTOM_COUNT
        or duration_days >= MODERATE_DURATION_DAYS
    ):
        severity_level = "Moderate"
        explanation = (
            "The provisional rules identified multiple symptoms "
            "or a longer reported duration."
        )

    else:
        severity_level = "Mild"
        explanation = (
            "The provisional rules did not flag the symptom count "
            "or duration for a higher category."
        )

    # 6. Return the result
    return {
        "severity_level": severity_level,
        "symptom_count": symptom_count,
        "duration_days": duration_days,
        "severity_explanation": explanation,
        "assessment_notice": (
            "Prototype severity assessment only. "
            "This is not a medical diagnosis or validated triage tool. "
            "Severity rules require review. Emergency assessment "
            "is handled separately."
        )
    }
