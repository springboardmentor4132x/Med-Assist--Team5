from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import SECRET_KEY, JWT_SECRET_KEY, JWT_EXPIRY
from models import create_tables
from auth import auth_bp, bcrypt
from user_profile import profile_bp
from admin import admin_bp
from history import history_bp
from doctor import doctor_bp
from symptoms import symptoms_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_EXPIRY

CORS(app)
bcrypt.init_app(app)
jwt = JWTManager(app)


# error messages for token problems
@jwt.expired_token_loader
def expired_token(jwt_header, jwt_data):
    return jsonify({"message": "Session expired, please login again"}), 401


@jwt.invalid_token_loader
def invalid_token(error):
    return jsonify({"message": "Invalid token, please login again"}), 401


@jwt.unauthorized_loader
def missing_token(error):
    return jsonify({"message": "Please login to continue"}), 401


app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(profile_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api")
app.register_blueprint(history_bp, url_prefix="/api")
app.register_blueprint(doctor_bp, url_prefix="/api")
app.register_blueprint(symptoms_bp, url_prefix="/api")

create_tables()


@app.route("/")
def home():
    return jsonify({"message": "MedAssist AI backend is running"})


if __name__ == "__main__":
    app.run(debug=True)
