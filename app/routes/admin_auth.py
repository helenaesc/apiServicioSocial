from flask import Blueprint, jsonify, request, session
from mysql.connector import Error
from werkzeug.security import check_password_hash
from ..database import fetch_one, execute_tx

admin_auth_bp = Blueprint("admin_auth", __name__)


@admin_auth_bp.post("/api/admin-auth/login")
def admin_login():
    payload = request.get_json(silent=True) or {}

    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email:
        return jsonify({"error": "email es obligatorio"}), 400

    if not password:
        return jsonify({"error": "password es obligatorio"}), 400

    try:
        row = fetch_one(
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

        if not row:
            return jsonify({"error": "Credenciales inválidas"}), 401

        if row["status"] != "ACTIVE":
            return jsonify({"error": "Cuenta inactiva o deshabilitada"}), 403

        password_hash = row.get("password_hash") or ""
        if not check_password_hash(password_hash, password):
            return jsonify({"error": "Credenciales inválidas"}), 401

        def tx(conn, cur):
            cur.execute(
                """
                UPDATE admin_users
                SET last_login_at = NOW()
                WHERE id = %s
                """,
                [row["id"]]
            )
            return {"status": 200}

        execute_tx(tx)

        session.clear()
        session["admin_user_id"] = row["id"]
        session["admin_user_role"] = row["role"]
        session["admin_user_email"] = row["email"]
        session["admin_user_full_name"] = row["full_name"]

        return jsonify({
            "message": "Login correcto",
            "user": {
                "id": row["id"],
                "full_name": row["full_name"],
                "email": row["email"],
                "role": row["role"],
                "status": row["status"]
            }
        }), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_auth_bp.post("/api/admin-auth/logout")
def admin_logout():
    session.clear()
    return jsonify({"message": "Sesión cerrada"}), 200


@admin_auth_bp.get("/api/admin-auth/me")
def admin_me():
    admin_user_id = session.get("admin_user_id")
    admin_user_role = session.get("admin_user_role")

    if not admin_user_id or not admin_user_role:
        return jsonify({"error": "No autenticado"}), 401

    try:
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
            [admin_user_id]
        )

        if not row:
            session.clear()
            return jsonify({"error": "Sesión inválida"}), 401

        if row["status"] != "ACTIVE":
            session.clear()
            return jsonify({"error": "Cuenta inactiva o deshabilitada"}), 403

        return jsonify({
            "user": {
                "id": row["id"],
                "full_name": row["full_name"],
                "email": row["email"],
                "role": row["role"],
                "status": row["status"],
                "last_login_at": row["last_login_at"]
            }
        }), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500