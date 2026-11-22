import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_db

profile_bp = Blueprint("profile", __name__)


def get_user(user_id):
    conn = get_db()
    user = conn.execute(
        "SELECT id, full_name, email, age, gender, contact, role, created_at FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    return user


# view own profile
@profile_bp.route("/profile", methods=["GET"])
@jwt_required()
def view_profile():
    user = get_user(get_jwt_identity())
    if user is None:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"user": dict(user)}), 200


# view someone else's profile: admin, or a doctor whose patient it is
@profile_bp.route("/profile/<int:user_id>", methods=["GET"])
@jwt_required()
def view_other_profile(user_id):
    my_id = get_jwt_identity()
    me = get_user(my_id)

    allowed = str(user_id) == my_id

    if me is not None and me["role"] == "admin":
        allowed = True

    if me is not None and me["role"] == "doctor":
        conn = get_db()
        assigned = conn.execute(
            "SELECT id FROM doctor_patient WHERE doctor_id = ? AND patient_id = ?",
            (my_id, user_id),
        ).fetchone()
        conn.close()
        if assigned:
            allowed = True

    if not allowed:
        return jsonify({"message": "You do not have permission to view this profile"}), 403

    user = get_user(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"user": dict(user)}), 200


# update own profile (email and role cannot be changed here)
@profile_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "No data received"}), 400

    full_name = str(data.get("full_name", "")).strip()
    age = data.get("age")
    gender = str(data.get("gender", "")).strip()
    contact = str(data.get("contact", "")).strip()

    if not full_name or not age or not gender:
        return jsonify({"message": "Name, age and gender are required"}), 400

    if len(full_name) < 3:
        return jsonify({"message": "Name must be at least 3 characters"}), 400

    try:
        age = int(age)
    except (ValueError, TypeError):
        return jsonify({"message": "Age must be a number"}), 400

    if age < 1 or age > 120:
        return jsonify({"message": "Enter a valid age"}), 400

    if gender not in ["Male", "Female", "Other"]:
        return jsonify({"message": "Select a valid gender"}), 400

    if contact and not re.match(r"^\d{10}$", contact):
        return jsonify({"message": "Contact number must be 10 digits"}), 400

    conn = get_db()
    conn.execute(
        "UPDATE users SET full_name = ?, age = ?, gender = ?, contact = ? WHERE id = ?",
        (full_name, age, gender, contact, user_id),
    )
    conn.commit()
    conn.close()

    user = get_user(user_id)
    return jsonify({"message": "Profile updated successfully", "user": dict(user)}), 200
