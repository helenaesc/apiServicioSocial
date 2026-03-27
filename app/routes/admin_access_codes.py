from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx, fetch_one
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


def _get_access_ttl_minutes():
    row = fetch_one("SELECT v FROM app_settings WHERE k='ACCESS_CODE_TTL_MINUTES' LIMIT 1")
    if not row or not row.get("v"):
        return 5
    try:
        return int(row["v"])
    except:
        return 5




@admin_access_bp.put("/api/admin/access-code-ttl")
def update_access_ttl():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}
    minutes = payload.get("minutes")

    try:
        minutes = int(minutes)
        if minutes < 1 or minutes > 15:
            return jsonify({"error": "minutes debe estar entre 1 y 15"}), 400
    except:
        return jsonify({"error": "minutes debe ser número"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            INSERT INTO app_settings (k, v)
            VALUES ('ACCESS_CODE_TTL_MINUTES', %s)
            ON DUPLICATE KEY UPDATE v = VALUES(v)
            """,
            [str(minutes)]
        )
        return {"status": 200}

    execute_tx(tx)
    return jsonify({"message": "TTL actualizado", "minutes": minutes})




@admin_access_bp.post("/api/admin/access-codes")
def generate_access_code():
    role = require_role(request, {ROLE_ADMIN, ROLE_STAFF})
    if not role:
        return jsonify({"error": "No autorizado (ADMIN o STAFF)"}), 401

    payload = request.get_json(silent=True) or {}
    enrolment_number = (payload.get("enrolment_number") or "").strip().lower()

    if not enrolment_number:
        return jsonify({"error": "Matrícula es obligatoria"}), 400

    ttl_minutes = _get_access_ttl_minutes()

    def tx(conn, cur):
        
        cur.execute(
            "SELECT id, first_name, p_last_name FROM users WHERE enrolment_number=%s LIMIT 1",
            [enrolment_number]
        )
        user = cur.fetchone()

        if not user:
            return {"error": "Usuario no encontrado", "status": 404}

        user_id = user["id"]

    
        cur.execute(
            """
            UPDATE email_verification_codes
            SET revoked = TRUE
            WHERE id_user = %s
              AND used = FALSE
              AND revoked = FALSE
              AND expires_at > NOW()
            """,
            [user_id]
        )

       
        code = _gen_code()
        code_hash = _sha256(code)
        expires_at = datetime.now() + timedelta(minutes=ttl_minutes)

        
        cur.execute(
            """
            INSERT INTO email_verification_codes
            (id_user, code_hash, expires_at, used, revoked)
            VALUES (%s, %s, %s, FALSE, FALSE)
            """,
            [user_id, code_hash, expires_at],
        )

        return {
            "status": 201,
            "code": code,
            "expires_at": expires_at.isoformat(sep=" ", timespec="seconds"),
            "user_name": f"{user['first_name']} {user['p_last_name']}"
        }

    try:
        result = execute_tx(tx)
        if result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({
            "code": result["code"],
            "expires_at": result["expires_at"],
            "user_name": result["user_name"]
        }), 201

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500