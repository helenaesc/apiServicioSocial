from flask import Blueprint, jsonify, request, session
from mysql.connector import Error
from werkzeug.security import generate_password_hash
from ..database import execute_tx, fetch_all, fetch_one
from ..authz import require_role, ROLE_ADMIN

admin_users_management_bp = Blueprint("admin_users_management", __name__)

VALID_STATUSES = {"ACTIVE", "DISABLED"}


def _get_current_admin_role(req):
    """
    Prioridad:
    1) sesión real
    2) compatibilidad temporal con X-ADMIN-KEY
    """
    session_role = session.get("admin_user_role")
    if session_role == ROLE_ADMIN:
        return session_role

    legacy_role = require_role(req, {ROLE_ADMIN})
    if legacy_role:
        return legacy_role

    return None


@admin_users_management_bp.get("/api/admin/staff")
def list_staff():
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    status = (request.args.get("status") or "").strip().upper()

    where = ["role = 'STAFF'"]
    params = []

    if status:
        if status not in VALID_STATUSES:
            return jsonify({"error": "status inválido (ACTIVE/DISABLED)"}), 400
        where.append("status = %s")
        params.append(status)

    sql = f"""
        SELECT
            id,
            full_name,
            email,
            role,
            status,
            created_at,
            updated_at,
            last_login_at
        FROM admin_users
        WHERE {' AND '.join(where)}
        ORDER BY status ASC, full_name ASC, id DESC
    """

    rows = fetch_all(sql, params)

    return jsonify({
        "performed_by": {
            "role": role
        },
        "items": rows
    }), 200


@admin_users_management_bp.post("/api/admin/staff")
def create_staff():
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}

    full_name = (payload.get("full_name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not full_name:
        return jsonify({"error": "full_name es obligatorio"}), 400

    if not email:
        return jsonify({"error": "email es obligatorio"}), 400

    if not password:
        return jsonify({"error": "password es obligatorio"}), 400

    if len(password) < 8:
        return jsonify({"error": "password debe tener al menos 8 caracteres"}), 400

    password_hash = generate_password_hash(password)

    def tx(conn, cur):
        cur.execute(
            """
            SELECT id
            FROM admin_users
            WHERE email = %s
            LIMIT 1
            FOR UPDATE
            """,
            [email]
        )
        if cur.fetchone():
            return {"error": "Ya existe una cuenta con ese email", "status": 409}

        cur.execute(
            """
            INSERT INTO admin_users
            (
                full_name,
                email,
                password_hash,
                role,
                status
            )
            VALUES (%s, %s, %s, 'STAFF', 'ACTIVE')
            """,
            [full_name, email, password_hash]
        )

        staff_id = cur.lastrowid

        cur.execute(
            """
            SELECT
                id,
                full_name,
                email,
                role,
                status,
                created_at,
                updated_at,
                last_login_at
            FROM admin_users
            WHERE id = %s
            LIMIT 1
            """,
            [staff_id]
        )
        staff_row = cur.fetchone()

        return {
            "status": 201,
            "message": "Staff creado",
            "performed_by": {
                "role": role
            },
            "staff": staff_row
        }

    try:
        result = execute_tx(tx)

        if result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify(result), 201

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_users_management_bp.patch("/api/admin/staff/<int:user_id>/status")
def update_staff_status(user_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}

    status = (payload.get("status") or "").strip().upper()
    if status not in VALID_STATUSES:
        return jsonify({"error": "status inválido (ACTIVE/DISABLED)"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            SELECT
                id,
                full_name,
                email,
                role,
                status,
                created_at,
                updated_at,
                last_login_at
            FROM admin_users
            WHERE id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [user_id]
        )
        row = cur.fetchone()

        if not row:
            return {"error": "Cuenta no encontrada", "status": 404}

        if row["role"] != "STAFF":
            return {"error": "Solo se puede modificar cuentas STAFF desde este endpoint", "status": 409}

        cur.execute(
            """
            UPDATE admin_users
            SET status = %s
            WHERE id = %s
            """,
            [status, user_id]
        )

        cur.execute(
            """
            SELECT
                id,
                full_name,
                email,
                role,
                status,
                created_at,
                updated_at,
                last_login_at
            FROM admin_users
            WHERE id = %s
            LIMIT 1
            """,
            [user_id]
        )
        final_row = cur.fetchone()

        return {
            "status": 200,
            "message": "Estado de staff actualizado",
            "performed_by": {
                "role": role
            },
            "staff": final_row
        }

    try:
        result = execute_tx(tx)

        if result.get("status") != 200:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify(result), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500