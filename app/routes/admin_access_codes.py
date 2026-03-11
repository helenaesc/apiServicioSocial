from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx
from ..authz import require_role, ROLE_ADMIN, ROLE_STAFF
import hashlib
import secrets
from datetime import datetime, timedelta

admin_access_bp = Blueprint("admin_access", __name__)

def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def _gen_code():
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    a = "".join(secrets.choice(alphabet) for _ in range(4))
    b = "".join(secrets.choice(alphabet) for _ in range(4))
    return f"{a}-{b}"  

@admin_access_bp.post("/api/admin/access-codes")
def generate_access_code():
    role = require_role(request, {ROLE_ADMIN, ROLE_STAFF})
    if not role:
        return jsonify({"error": "No autorizado (ADMIN o STAFF)"}), 401

    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    hours = payload.get("hours", 24)

    if not email:
        return jsonify({"error": "email es obligatorio"}), 400

    try:
        hours = int(hours)
        if hours < 1 or hours > 168:
            return jsonify({"error": "hours debe estar entre 1 y 168"}), 400
    except:
        return jsonify({"error": "hours debe ser número"}), 400

    def tx(conn, cur):
        cur.execute("SELECT id FROM users WHERE LOWER(email)=LOWER(%s) LIMIT 1", [email])
        user = cur.fetchone()
        if not user:
            return {"error": "Usuario no encontrado", "status": 404}

        code = _gen_code()
        code_hash = _sha256(code)
        expires_at = datetime.now() + timedelta(hours=hours)

        cur.execute(
            """
            INSERT INTO email_verification_codes (id_user, code_hash, expires_at, used)
            VALUES (%s, %s, %s, FALSE)
            """,
            [user["id"], code_hash, expires_at],
        )

        return {
            "status": 201,
            "code": code,
            "expires_at": expires_at.isoformat(sep=" ", timespec="seconds")
        }

    try:
        result = execute_tx(tx)
        if result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]
        return jsonify({"code": result["code"], "expires_at": result["expires_at"]}), 201
    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500