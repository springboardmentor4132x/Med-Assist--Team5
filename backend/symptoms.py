import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models import get_db
from decorators import role_required
from symptom_data import SYMPTOMS, QUICK_SYMPTOMS, MAX_SYMPTOMS, make_label
from assessment import build_assessment

symptoms_bp = Blueprint("symptoms", __name__)


# the error response has both keys, "error" is the one given in the module document
def error(text, code=400, **extra):
    data = {"error": text, "message": text}
    data.update(extra)
    return jsonify(data), code


def get_label(key):
    return SYMPTOMS.get(key, make_label(key))


# list of symptoms for the selection page
@symptoms_bp.route("/symptoms", methods=["GET"])
@role_required("patient")
def get_symptoms():
    symptoms = []
    for key, label in SYMPTOMS.items():
        symptoms.append({"key": key, "label": label, "common": key in QUICK_SYMPTOMS})

    symptoms.sort(key=lambda symptom: symptom["label"])
    return jsonify({"symptoms": symptoms}), 200


# receive the selected symptoms, validate them, save them and analyse them
@symptoms_bp.route("/symptoms/submit", methods=["POST"])
@role_required("patient")
def submit_symptoms():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "selected_symptoms" not in data:
        return error("Request must contain selected_symptoms")

    selected = data["selected_symptoms"]

    if not isinstance(selected, list):
        return error("selected_symptoms must be a list")

    if len(selected) == 0:
        return error("Please select at least one symptom.")

    clean = []
    duplicates = []
    invalid = []

    for item in selected:
        if not isinstance(item, str):
            return error("Each symptom must be text")

        # "Body Pain" and "body_pain" are the same symptom
        name = item.strip().lower().replace(" ", "_")

        if name not in SYMPTOMS:
            invalid.append(item.strip()[:50] or "(empty)")
        elif name in clean:
            if name not in duplicates:
                duplicates.append(name)
        else:
            clean.append(name)

    if invalid:
        return error("Unsupported symptom(s): " + ", ".join(invalid), invalid_symptoms=invalid)

    if len(clean) > MAX_SYMPTOMS:
        return error("You can select up to " + str(MAX_SYMPTOMS) + " symptoms at a time")

    user_id = get_jwt_identity()

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO symptom_assessments (user_id, symptoms) VALUES (?, ?)",
        (user_id, json.dumps(clean)),
    )
    conn.commit()
    assessment_id = cursor.lastrowid
    conn.close()

    # correlation analysis + medical history, saved with the assessment
    assessment = build_assessment(user_id, assessment_id, clean)
    save_result(assessment_id, assessment)

    return jsonify({
        "message": "Symptoms submitted successfully",
        "assessment_id": assessment_id,
        "symptoms": [{"key": key, "label": SYMPTOMS[key]} for key in clean],
        "removed_duplicates": duplicates,
        "assessment": assessment,
    }), 201


def save_result(assessment_id, assessment):
    conn = get_db()
    conn.execute(
        "UPDATE symptom_assessments SET result = ? WHERE id = ?",
        (json.dumps(assessment), assessment_id),
    )
    conn.commit()
    conn.close()


# short list of the patient's own assessments, newest first
@symptoms_bp.route("/symptoms/assessments", methods=["GET"])
@role_required("patient")
def my_assessments():
    conn = get_db()
    rows = conn.execute(
        "SELECT id, symptoms, created_at FROM symptom_assessments WHERE user_id = ? ORDER BY id DESC",
        (get_jwt_identity(),),
    ).fetchall()
    conn.close()

    assessments = []
    for row in rows:
        keys = json.loads(row["symptoms"])
        assessments.append({
            "id": row["id"],
            "created_at": row["created_at"],
            "symptom_count": len(keys),
            "symptoms": [{"key": key, "label": get_label(key)} for key in keys],
        })

    return jsonify({"assessments": assessments}), 200


# one full assessment, only the owner can see it
@symptoms_bp.route("/symptoms/assessments/<int:assessment_id>", methods=["GET"])
@role_required("patient")
def get_assessment(assessment_id):
    user_id = get_jwt_identity()

    conn = get_db()
    row = conn.execute(
        "SELECT id, symptoms, result FROM symptom_assessments WHERE id = ? AND user_id = ?",
        (assessment_id, user_id),
    ).fetchone()
    conn.close()

    # same message if it does not exist or belongs to someone else
    if row is None:
        return error("Assessment not found", 404)

    # assessments saved before the analysis was added have no result yet
    if row["result"] is None:
        assessment = build_assessment(user_id, assessment_id, json.loads(row["symptoms"]))
        save_result(assessment_id, assessment)
    else:
        assessment = json.loads(row["result"])

    return jsonify({"assessment": assessment}), 200
