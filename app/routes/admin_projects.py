from flask import Blueprint, jsonify, request, session
from mysql.connector import Error
from ..database import execute_tx, fetch_all, fetch_one
from ..authz import require_role, ROLE_ADMIN

admin_projects_bp = Blueprint("admin_projects", __name__)


def _get_current_admin_role(req):
    session_role = session.get("admin_user_role")
    if session_role == ROLE_ADMIN:
        return session_role

    legacy_role = require_role(req, {ROLE_ADMIN})
    if legacy_role:
        return legacy_role

    return None


def _to_nullable_str(value):
    value = str(value).strip() if value is not None else ""
    return value or None


def _to_required_str(value, field_name: str):
    value = str(value).strip() if value is not None else ""
    if not value:
        raise ValueError(f"{field_name} es obligatorio")
    return value


def _to_required_int(value, field_name: str, min_value=None, max_value=None):
    try:
        n = int(value)
    except:
        raise ValueError(f"{field_name} debe ser numérico")

    if min_value is not None and n < min_value:
        raise ValueError(f"{field_name} debe ser >= {min_value}")

    if max_value is not None and n > max_value:
        raise ValueError(f"{field_name} debe ser <= {max_value}")

    return n


@admin_projects_bp.get("/api/admin/projects")
def list_admin_projects():
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    q = (request.args.get("q") or "").strip()

    where = []
    params = []

    if q:
        where.append("""
            (
                p.general_name LIKE %s
                OR p.name LIKE %s
                OR p.schedule_description LIKE %s
                OR p.team_owners LIKE %s
                OR p.clave LIKE %s
                OR pa.name LIKE %s
            )
        """)
        like = f"%{q}%"
        params.extend([like, like, like, like, like, like])

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    sql = f"""
        SELECT
            p.id,
            p.general_name,
            p.name,
            p.id_partner,
            p.id_modality,
            p.id_week_days,
            p.id_schedule,
            p.slots,
            p.schedule_description,
            p.team_owners,
            p.objectives,
            p.activities,
            p.clave,
            p.competencies,
            p.location,
            p.duration,
            p.audience,
            p.max_hours,
            p.comments,

            pa.name AS partner_name,
            m.name AS modality_name,
            wd.name AS week_days_name,
            sc.name AS schedule_name

        FROM project p
        LEFT JOIN partner pa ON pa.id = p.id_partner
        LEFT JOIN modality m ON m.id = p.id_modality
        LEFT JOIN week_days wd ON wd.id = p.id_week_days
        LEFT JOIN schedule sc ON sc.id = p.id_schedule
        {where_sql}
        ORDER BY p.general_name, p.name, p.id DESC
    """

    rows = fetch_all(sql, params)
    return jsonify(rows), 200


@admin_projects_bp.post("/api/admin/projects")
def create_admin_project():
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}

    try:
        general_name = _to_required_str(payload.get("general_name"), "general_name")
        name = _to_required_str(payload.get("name"), "name")

        id_partner = _to_required_int(payload.get("id_partner"), "id_partner", min_value=1)
        id_modality = _to_required_int(payload.get("id_modality"), "id_modality", min_value=1)
        id_week_days = _to_required_int(payload.get("id_week_days"), "id_week_days", min_value=1)
        id_schedule = _to_required_int(payload.get("id_schedule"), "id_schedule", min_value=1)

        slots = _to_required_int(payload.get("slots", 0), "slots", min_value=0, max_value=5000)

        schedule_description = _to_nullable_str(payload.get("schedule_description"))
        team_owners = _to_nullable_str(payload.get("team_owners"))
        objectives = _to_nullable_str(payload.get("objectives"))
        activities = _to_nullable_str(payload.get("activities"))
        clave = _to_nullable_str(payload.get("clave"))
        competencies = _to_nullable_str(payload.get("competencies"))
        location = _to_nullable_str(payload.get("location"))
        duration = _to_nullable_str(payload.get("duration"))
        audience = _to_nullable_str(payload.get("audience"))
        max_hours = _to_nullable_str(payload.get("max_hours"))
        comments = _to_nullable_str(payload.get("comments"))

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    def tx(conn, cur):
        # Validar catálogos
        cur.execute("SELECT id FROM partner WHERE id = %s LIMIT 1", [id_partner])
        if not cur.fetchone():
            return {"error": "partner no encontrado", "status": 404}

        cur.execute("SELECT id FROM modality WHERE id = %s LIMIT 1", [id_modality])
        if not cur.fetchone():
            return {"error": "modality no encontrada", "status": 404}

        cur.execute("SELECT id FROM week_days WHERE id = %s LIMIT 1", [id_week_days])
        if not cur.fetchone():
            return {"error": "week_days no encontrado", "status": 404}

        cur.execute("SELECT id FROM schedule WHERE id = %s LIMIT 1", [id_schedule])
        if not cur.fetchone():
            return {"error": "schedule no encontrado", "status": 404}

        # Evitar duplicado muy obvio
        cur.execute(
            """
            SELECT id
            FROM project
            WHERE general_name = %s
              AND name = %s
              AND id_partner = %s
              AND id_modality = %s
              AND id_week_days = %s
              AND id_schedule = %s
            LIMIT 1
            FOR UPDATE
            """,
            [general_name, name, id_partner, id_modality, id_week_days, id_schedule]
        )
        existing = cur.fetchone()
        if existing:
            return {
                "error": "Ya existe un proyecto base con esa combinación principal",
                "status": 409
            }

        cur.execute(
            """
            INSERT INTO project
            (
                general_name,
                name,
                id_partner,
                id_modality,
                id_week_days,
                id_schedule,
                slots,
                schedule_description,
                team_owners,
                objectives,
                activities,
                clave,
                competencies,
                location,
                duration,
                audience,
                max_hours,
                comments
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """,
            [
                general_name,
                name,
                id_partner,
                id_modality,
                id_week_days,
                id_schedule,
                slots,
                schedule_description,
                team_owners,
                objectives,
                activities,
                clave,
                competencies,
                location,
                duration,
                audience,
                max_hours,
                comments
            ]
        )

        project_id = cur.lastrowid

        cur.execute(
            """
            SELECT
                p.id,
                p.general_name,
                p.name,
                p.id_partner,
                p.id_modality,
                p.id_week_days,
                p.id_schedule,
                p.slots,
                p.schedule_description,
                p.team_owners,
                p.objectives,
                p.activities,
                p.clave,
                p.competencies,
                p.location,
                p.duration,
                p.audience,
                p.max_hours,
                p.comments,

                pa.name AS partner_name,
                m.name AS modality_name,
                wd.name AS week_days_name,
                sc.name AS schedule_name
            FROM project p
            LEFT JOIN partner pa ON pa.id = p.id_partner
            LEFT JOIN modality m ON m.id = p.id_modality
            LEFT JOIN week_days wd ON wd.id = p.id_week_days
            LEFT JOIN schedule sc ON sc.id = p.id_schedule
            WHERE p.id = %s
            LIMIT 1
            """,
            [project_id]
        )
        row = cur.fetchone()

        return {
            "status": 201,
            "message": "Proyecto base creado",
            "project": row
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


@admin_projects_bp.route("/api/admin/projects/<int:project_id>/slots", methods=["PATCH"])
def update_project_slots(project_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}
    new_slots = payload.get("slots")

    try:
        new_slots = int(new_slots)
        if new_slots < 0 or new_slots > 5000:
            return jsonify({"error": "slots debe estar entre 0 y 5000"}), 400
    except:
        return jsonify({"error": "slots debe ser número"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            SELECT id, slots
            FROM project
            WHERE id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [project_id]
        )
        proj = cur.fetchone()
        if not proj:
            return {"error": "Proyecto no encontrado", "status": 404}

        # Si todavía usas la lógica vieja de tokens por project base
        # la respetamos para no romper nada.
        cur.execute(
            """
            SELECT COUNT(*) AS c
            FROM token
            WHERE id_project = %s
              AND used = TRUE
            """,
            [project_id]
        )
        used_count = int(cur.fetchone()["c"])

        cur.execute(
            """
            SELECT COUNT(*) AS c
            FROM token
            WHERE id_project = %s
              AND used = FALSE
              AND revoked = FALSE
              AND (expires_at IS NULL OR expires_at > NOW())
            """,
            [project_id]
        )
        open_active = int(cur.fetchone()["c"])

        min_needed = used_count + open_active
        if new_slots < min_needed:
            return {
                "error": (
                    f"No puedes bajar slots a {new_slots}. "
                    f"Mínimo requerido: {min_needed} "
                    f"(usados={used_count}, abiertos={open_active})."
                ),
                "status": 409
            }

        cur.execute(
            "UPDATE project SET slots = %s WHERE id = %s",
            [new_slots, project_id]
        )

        return {
            "message": "Cupo actualizado",
            "slots": new_slots,
            "status": 200
        }

    try:
        result = execute_tx(tx)
        if result.get("status") != 200:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({
            "message": result["message"],
            "slots": result["slots"]
        }), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500