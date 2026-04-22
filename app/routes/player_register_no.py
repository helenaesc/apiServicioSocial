from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx
import secrets
import hashlib

player_register_bp = Blueprint("player_register", __name__)

def _make_temp_salt(length: int = 10) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))

def _make_temp_password_hash() -> tuple[str, str]:
    """
    Como el flujo actual del evento no usa password real del jugador,
    generamos un salt y un hash temporales para cumplir con la tabla users.
    """
    temp_plain = secrets.token_urlsafe(16)
    salt = _make_temp_salt(10)
    password_hash = hashlib.sha256((temp_plain + salt).encode("utf-8")).hexdigest()
    return password_hash, salt

@player_register_bp.post("/api/player/register")
def player_register():
    payload = request.get_json(silent=True) or {}

    first_name = (payload.get("first_name") or "").strip()
    second_name = (payload.get("second_name") or "").strip() or None
    p_last_name = (payload.get("p_last_name") or "").strip()
    m_last_name = (payload.get("m_last_name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    enrolment_number = (payload.get("enrolment_number") or "").strip().lower()
    phone_number = (payload.get("phone_number") or "").strip() or None
    degree = (payload.get("degree") or "").strip() or None
    semester = payload.get("semester")

    
    if not first_name:
        return jsonify({"error": "Nombre es obligatorio"}), 400
    if not p_last_name:
        return jsonify({"error": "Apellido paterno es obligatorio"}), 400
    if not m_last_name:
        return jsonify({"error": "Apellido materno es obligatorio"}), 400
    if not email:
        return jsonify({"error": "Correo es obligatorio"}), 400
    if not enrolment_number:
        return jsonify({"error": "Matrícula es obligatoria"}), 400

    if len(enrolment_number) > 10:
        return jsonify({"error": "La matrícula no puede exceder 10 caracteres"}), 400

    if semester not in (None, ""):
        try:
            semester = int(semester)
            if semester < 1 or semester > 20:
                return jsonify({"error": "semester debe estar entre 1 y 20"}), 400
        except:
            return jsonify({"error": "semester debe ser número"}), 400
    else:
        semester = None

    password_hash, salt = _make_temp_password_hash()

    def tx(conn, cur):
        # Verificar matrícula duplicada
        cur.execute(
            "SELECT id FROM users WHERE enrolment_number=%s LIMIT 1",
            [enrolment_number]
        )
        if cur.fetchone():
            return {"error": "Ya existe un jugador con esa matrícula", "status": 409}

        # Verificar correo duplicado
        cur.execute(
            "SELECT id FROM users WHERE email=%s LIMIT 1",
            [email]
        )
        if cur.fetchone():
            return {"error": "Ya existe un jugador con ese correo", "status": 409}

        cur.execute(
            """
            INSERT INTO users
            (
                first_name, second_name, p_last_name, m_last_name,
                email, enrolment_number, phone_number,
                password, salt, admin, degree, semester
            )
            VALUES (%s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, FALSE, %s, %s)
            """,
            [
                first_name, second_name, p_last_name, m_last_name,
                email, enrolment_number, phone_number,
                password_hash, salt, degree, semester
            ]
        )

        new_id = cur.lastrowid

        return {
            "status": 201,
            "id": new_id,
            "first_name": first_name,
            "p_last_name": p_last_name,
            "m_last_name": m_last_name,
            "email": email,
            "enrolment_number": enrolment_number
        }

    try:
        result = execute_tx(tx)

        if result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({
            "message": "Jugador registrado",
            "id": result["id"],
            "first_name": result["first_name"],
            "p_last_name": result["p_last_name"],
            "m_last_name": result["m_last_name"],
            "email": result["email"],
            "enrolment_number": result["enrolment_number"]
        }), 201

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500