from datetime import datetime, date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models import get_db
from decorators import role_required

history_bp = Blueprint("history", __name__)


# patient adds an entry to his own history
@history_bp.route("/history", methods=["POST"])
@role_required("patient")
def add_history():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "No data received"}), 400

    condition = str(data.get("condition", "")).strip()
    notes = str(data.get("notes", "")).strip()
    record_date = str(data.get("record_date", "")).strip()

    if not condition or not record_date:
        return jsonify({"message": "Condition and date are required"}), 400

    if len(condition) < 3 or len(condition) > 200:
        return jsonify({"message": "Condition must be 3 to 200 characters"}), 400

    if len(notes) > 1000:
        return jsonify({"message": "Notes can be 1000 characters at most"}), 400

    try:
        entered_date = datetime.strptime(record_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Enter a valid date"}), 400

    if entered_date > date.today():
        return jsonify({"message": "Date cannot be in the future"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO medical_history (user_id, condition, notes, record_date) VALUES (?, ?, ?, ?)",
        (get_jwt_identity(), condition, notes, record_date),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "History added successfully"}), 201


# patient views his own history
@history_bp.route("/history", methods=["GET"])
@role_required("patient")
def my_history():
    conn = get_db()
    rows = conn.execute(
        "SELECT id, condition, notes, record_date FROM medical_history WHERE user_id = ? ORDER BY record_date DESC, id DESC",
        (get_jwt_identity(),),
    ).fetchall()
    conn.close()

    return jsonify({"history": [dict(row) for row in rows]}), 200


# doctor views history of a patient, only if admin assigned that patient to him
@history_bp.route("/history/patient/<int:patient_id>", methods=["GET"])
@role_required("doctor")
def patient_history(patient_id):
    doctor_id = get_jwt_identity()

    conn = get_db()
    assigned = conn.execute(
        "SELECT id FROM doctor_patient WHERE doctor_id = ? AND patient_id = ?",
        (doctor_id, patient_id),
    ).fetchone()

    if assigned is None:
        conn.close()
        return jsonify({"message": "This patient is not assigned to you"}), 403

    rows = conn.execute(
        "SELECT id, condition, notes, record_date FROM medical_history WHERE user_id = ? ORDER BY record_date DESC, id DESC",
        (patient_id,),
    ).fetchall()
    conn.close()

    return jsonify({"history": [dict(row) for row in rows]}), 200
