from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import get_db


# use like: @role_required("admin") or @role_required("doctor", "admin")
def role_required(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()

            # role is checked from the database so a changed role works immediately
            conn = get_db()
            user = conn.execute("SELECT role FROM users WHERE id = ?", (user_id,)).fetchone()
            conn.close()

            if user is None or user["role"] not in allowed_roles:
                return jsonify({"message": "You do not have permission to do this"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
