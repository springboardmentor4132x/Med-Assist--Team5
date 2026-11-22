from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity
from models import get_db
from decorators import role_required

doctor_bp = Blueprint("doctor", __name__)


# patients that admin assigned to this doctor
@doctor_bp.route("/doctor/patients", methods=["GET"])
@role_required("doctor")
def my_patients():
    conn = get_db()
    patients = conn.execute(
        """SELECT users.id, users.full_name, users.email, users.age, users.gender, users.contact
           FROM doctor_patient
           JOIN users ON users.id = doctor_patient.patient_id
           WHERE doctor_patient.doctor_id = ?
           ORDER BY users.full_name""",
        (get_jwt_identity(),),
    ).fetchall()
    conn.close()

    return jsonify({"patients": [dict(patient) for patient in patients]}), 200
