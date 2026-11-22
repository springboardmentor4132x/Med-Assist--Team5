import re
import sqlite3
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import get_db

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "No data received"}), 400

    full_name = str(data.get("full_name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    age = data.get("age")
    gender = str(data.get("gender", "")).strip()
    contact = str(data.get("contact", "")).strip()
    requested_role = str(data.get("role", "patient")).strip()

    # validation
    if not full_name or not email or not password or not age or not gender:
        return jsonify({"message": "Please fill all the required fields"}), 400

    if len(full_name) < 3:
        return jsonify({"message": "Name must be at least 3 characters"}), 400

    if not re.match(EMAIL_PATTERN, email):
        return jsonify({"message": "Enter a valid email address"}), 400

    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters"}), 400

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

    # admin cannot be chosen while registering
    if requested_role not in ["patient", "doctor", "clinic"]:
        return jsonify({"message": "Select a valid account type"}), 400

    conn = get_db()

    # check if email is already registered
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return jsonify({"message": "Account already exists with this email"}), 409

    # never store the plain password, only the hash
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    try:
        conn.execute(
            "INSERT INTO users (full_name, email, password, age, gender, contact, requested_role) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (full_name, email, hashed_password, age, gender, contact, requested_role),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"message": "Account already exists with this email"}), 409

    conn.close()

    # everyone starts as a patient, doctor and clinic accounts need admin approval
    if requested_role != "patient":
        return jsonify({"message": "Registration successful. Your account is a patient account until the admin approves your " + requested_role + " request."}), 201

    return jsonify({"message": "Registration successful. Please login."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "No data received"}), 400

    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    # same message for both cases so we don't tell which one is wrong
    if user is None or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_access_token(
        identity=str(user["id"]),
        additional_claims={"role": user["role"]},
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"],
        },
    }), 200


# protected route, works only with a valid token
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()

    conn = get_db()
    user = conn.execute(
        "SELECT id, full_name, email, age, gender, contact, role, created_at FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"user": dict(user)}), 200
