from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models import get_db
from decorators import role_required

admin_bp = Blueprint("admin", __name__)

ROLES = ["patient", "doctor", "clinic", "admin"]


# list of all users
@admin_bp.route("/admin/users", methods=["GET"])
@role_required("admin")
def get_users():
    conn = get_db()
    users = conn.execute(
        "SELECT id, full_name, email, age, gender, contact, role, requested_role, created_at FROM users ORDER BY id"
    ).fetchall()
    conn.close()

    return jsonify({"users": [dict(user) for user in users]}), 200


# number of users in each role, for monitoring
@admin_bp.route("/admin/stats", methods=["GET"])
@role_required("admin")
def get_stats():
    conn = get_db()
    rows = conn.execute("SELECT role, COUNT(*) AS total FROM users GROUP BY role").fetchall()
    conn.close()

    stats = {"total": 0, "patient": 0, "doctor": 0, "clinic": 0, "admin": 0}
    for row in rows:
        stats[row["role"]] = row["total"]
        stats["total"] += row["total"]

    return jsonify(stats), 200


@admin_bp.route("/admin/users/<int:user_id>/role", methods=["PUT"])
@role_required("admin")
def change_role(user_id):
    data = request.get_json(silent=True)
    role = str(data.get("role", "")) if data else ""

    if role not in ROLES:
        return jsonify({"message": "Invalid role"}), 400

    # admin should not remove his own admin access by mistake
    if str(user_id) == get_jwt_identity():
        return jsonify({"message": "You cannot change your own role"}), 400

    conn = get_db()
    user = conn.execute("SELECT id FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        conn.close()
        return jsonify({"message": "User not found"}), 404

    conn.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))

    # old assignments are not valid if the role is changed
    if role != "doctor":
        conn.execute("DELETE FROM doctor_patient WHERE doctor_id = ?", (user_id,))
    if role != "patient":
        conn.execute("DELETE FROM doctor_patient WHERE patient_id = ?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Role updated to " + role}), 200


@admin_bp.route("/admin/users/<int:user_id>", methods=["DELETE"])
@role_required("admin")
def delete_user(user_id):
    if str(user_id) == get_jwt_identity():
        return jsonify({"message": "You cannot delete your own account"}), 400

    conn = get_db()
    user = conn.execute("SELECT id FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        conn.close()
        return jsonify({"message": "User not found"}), 404

    conn.execute("DELETE FROM medical_history WHERE user_id = ?", (user_id,))
    conn.execute("DELETE FROM symptom_assessments WHERE user_id = ?", (user_id,))
    conn.execute("DELETE FROM doctor_patient WHERE doctor_id = ? OR patient_id = ?", (user_id, user_id))
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted"}), 200


# list of doctor-patient assignments
@admin_bp.route("/admin/assignments", methods=["GET"])
@role_required("admin")
def get_assignments():
    conn = get_db()
    rows = conn.execute(
        """SELECT doctor_patient.id, doctor_patient.doctor_id, doctor.full_name AS doctor_name,
                  doctor_patient.patient_id, patient.full_name AS patient_name
           FROM doctor_patient
           JOIN users AS doctor ON doctor.id = doctor_patient.doctor_id
           JOIN users AS patient ON patient.id = doctor_patient.patient_id
           ORDER BY doctor.full_name, patient.full_name"""
    ).fetchall()
    conn.close()

    return jsonify({"assignments": [dict(row) for row in rows]}), 200


# assign a patient to a doctor
@admin_bp.route("/admin/assignments", methods=["POST"])
@role_required("admin")
def add_assignment():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "No data received"}), 400

    try:
        doctor_id = int(data.get("doctor_id"))
        patient_id = int(data.get("patient_id"))
    except (TypeError, ValueError):
        return jsonify({"message": "Select a doctor and a patient"}), 400

    conn = get_db()
    doctor = conn.execute("SELECT role FROM users WHERE id = ?", (doctor_id,)).fetchone()
    patient = conn.execute("SELECT role FROM users WHERE id = ?", (patient_id,)).fetchone()

    if doctor is None or doctor["role"] != "doctor":
        conn.close()
        return jsonify({"message": "Selected user is not a doctor"}), 400

    if patient is None or patient["role"] != "patient":
        conn.close()
        return jsonify({"message": "Selected user is not a patient"}), 400

    existing = conn.execute(
        "SELECT id FROM doctor_patient WHERE doctor_id = ? AND patient_id = ?",
        (doctor_id, patient_id),
    ).fetchone()
    if existing:
        conn.close()
        return jsonify({"message": "This patient is already assigned to this doctor"}), 409

    conn.execute("INSERT INTO doctor_patient (doctor_id, patient_id) VALUES (?, ?)", (doctor_id, patient_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Patient assigned to doctor"}), 201


@admin_bp.route("/admin/assignments/<int:assignment_id>", methods=["DELETE"])
@role_required("admin")
def remove_assignment(assignment_id):
    conn = get_db()
    row = conn.execute("SELECT id FROM doctor_patient WHERE id = ?", (assignment_id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"message": "Assignment not found"}), 404

    conn.execute("DELETE FROM doctor_patient WHERE id = ?", (assignment_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Assignment removed"}), 200
