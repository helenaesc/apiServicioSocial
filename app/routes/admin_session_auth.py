from flask import Blueprint, jsonify, request, session
from mysql.connector import Error
from werkzeug.security import check_password_hash
from ..database import fetch_one, execute_tx

admin_session_auth_bp = Blueprint("admin_session_auth", __name__)

ROLE_ADMIN = "ADMIN"
ROLE_STAFF = "STAFF"


def _build_auth_user_payload(row: dict) -> dict:
    return {
        "id": row["id"],
        "full_name": row["full_name"],
        "email": row["email"],
        "role": row["role"],
        "status": row["status"],
        "last_login_at": row["last_login_at"],
    }


@admin_session_auth_bp.post("/api/admin-auth/login")
def login():
    payload = request.get_json(silent=True) or {}

    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email:
        return jsonify({"error": "email es obligatorio"}), 400

    if not password:
        return jsonify({"error": "password es obligatorio"}), 400

    user = fetch_one(
        """
        SELECT
            id,
            full_name,
            email,
            password_hash,
            role,
            status,
            last_login_at
        FROM admin_users
        WHERE email = %s
        LIMIT 1
        """,
        [email]
    )

    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 401

    if user["status"] != "ACTIVE":
        return jsonify({"error": "Cuenta deshabilitada"}), 403

    if not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    def tx(conn, cur):
        cur.execute(
            """
            UPDATE admin_users
            SET last_login_at = NOW()
            WHERE id = %s
            """,
            [user["id"]]
        )

        cur.execute(
            """
            SELECT
                id,
                full_name,
                email,
                role,
                status,
                last_login_at
            FROM admin_users
            WHERE id = %s
            LIMIT 1
            """,
            [user["id"]]
        )
        final_user = cur.fetchone()

        return {"status": 200, "user": final_user}

    try:
        result = execute_tx(tx)

        auth_user = result["user"]

        session.clear()
        session["admin_user_id"] = auth_user["id"]
        session["admin_user_role"] = auth_user["role"]
        session["admin_user_email"] = auth_user["email"]
        session["admin_user_name"] = auth_user["full_name"]

        return jsonify({
            "message": "Login correcto",
            "user": _build_auth_user_payload(auth_user)
        }), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_session_auth_bp.post("/api/admin-auth/logout")
def logout():
    session.clear()
    return jsonify({"message": "Sesión cerrada"}), 200


@admin_session_auth_bp.get("/api/admin-auth/me")
def me():
    user_id = session.get("admin_user_id")
    role = session.get("admin_user_role")
    email = session.get("admin_user_email")
    full_name = session.get("admin_user_name")

    if not user_id or not role:
        return jsonify({"error": "Sesión no iniciada"}), 401

    row = fetch_one(
        """
        SELECT
            id,
            full_name,
            email,
            role,
            status,
            last_login_at
        FROM admin_users
        WHERE id = %s
        LIMIT 1
        """,
        [user_id]
    )

    if not row:
        session.clear()
        return jsonify({"error": "Sesión inválida"}), 401

    if row["status"] != "ACTIVE":
        session.clear()
        return jsonify({"error": "Cuenta deshabilitada"}), 403

    return jsonify({
        "user": _build_auth_user_payload(row)
    }), 200