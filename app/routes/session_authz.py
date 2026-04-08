from functools import wraps
from flask import session, jsonify

ROLE_ADMIN = "ADMIN"
ROLE_STAFF = "STAFF"


def session_login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin_user_id"):
            return jsonify({"error": "Sesión no iniciada"}), 401
        return fn(*args, **kwargs)
    return wrapper


def session_role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role = session.get("admin_user_role")
            if not role:
                return jsonify({"error": "Sesión no iniciada"}), 401
            if role not in allowed_roles:
                return jsonify({"error": "No autorizado"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator