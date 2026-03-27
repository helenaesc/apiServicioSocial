from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx
import hashlib

player_auth_bp = Blueprint("player_auth", __name__)

def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@player_auth_bp.post("/api/player/login")
def player_login():
    payload = request.get_json(silent=True) or {}

    enrolment_number = (payload.get("enrolment_number") or "").strip().lower()
    code = (payload.get("code") or "").strip().upper()

    if not enrolment_number or not code:
        return jsonify({"error": "Matrícula y código son obligatorios"}), 400

    code_hash = _sha256(code)

    def tx(conn, cur):
        
        cur.execute(
            "SELECT id FROM users WHERE enrolment_number=%s LIMIT 1",
            [enrolment_number]
        )
        user = cur.fetchone()

        if not user:
            return {"error": "Usuario no encontrado", "status": 404}

        user_id = user["id"]

       
        cur.execute(
            """
            SELECT id
            FROM email_verification_codes
            WHERE id_user = %s
              AND code_hash = %s
              AND used = FALSE
              AND revoked = FALSE
              AND expires_at > NOW()
            LIMIT 1
            """,
            [user_id, code_hash]
        )

        code_row = cur.fetchone()

        if not code_row:
            return {"error": "Código inválido, expirado o ya usado", "status": 400}

        code_id = code_row["id"]

        
        cur.execute(
            """
            UPDATE email_verification_codes
            SET used = TRUE,
                used_at = NOW()
            WHERE id = %s
            """,
            [code_id]
        )

        return {"status": 200}

    try:
        result = execute_tx(tx)

        if result.get("status") != 200:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({"message": "Acceso concedido"}), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500