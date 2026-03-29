from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx, fetch_all, fetch_one
from ..authz import require_role, ROLE_ADMIN

admin_master_projects_bp = Blueprint("admin_master_projects", __name__)


@admin_master_projects_bp.get("/api/admin/projects")
def list_master_projects():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    q = (request.args.get("q") or "").strip()

    where = []
    params = []

    if q:
        where.append("""
            (
              p.name LIKE %s
              OR p.team_owners LIKE %s
              OR p.objectives LIKE %s
              OR p.activities LIKE %s
              OR p.clave LIKE %s
            )
        """)
        like = f"%{q}%"
        params.extend([like, like, like, like, like])

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    sql = f"""
        SELECT
            p.id,
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
            p.season,
            pa.name AS partner_name,
            m.name AS modality_name,
            wd.name AS week_days_name,
            sc.name AS schedule_name
        FROM project p
        JOIN partner pa ON pa.id = p.id_partner
        JOIN modality m ON m.id = p.id_modality
        JOIN week_days wd ON wd.id = p.id_week_days
        JOIN schedule sc ON sc.id = p.id_schedule
        {where_sql}
        ORDER BY pa.name, p.name
    """

    rows = fetch_all(sql, params)
    return jsonify(rows), 200


@admin_master_projects_bp.get("/api/admin/projects/<int:project_id>")
def get_master_project(project_id: int):
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    sql = """
        SELECT
            p.id,
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
            p.season,
            pa.name AS partner_name,
            m.name AS modality_name,
            wd.name AS week_days_name,
            sc.name AS schedule_name
        FROM project p
        JOIN partner pa ON pa.id = p.id_partner
        JOIN modality m ON m.id = p.id_modality
        JOIN week_days wd ON wd.id = p.id_week_days
        JOIN schedule sc ON sc.id = p.id_schedule
        WHERE p.id = %s
        LIMIT 1
    """
    row = fetch_one(sql, [project_id])

    if not row:
        return jsonify({"error": "Proyecto no encontrado"}), 404

    return jsonify(row), 200


@admin_master_projects_bp.post("/api/admin/projects")
def create_master_project():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}

    name = (payload.get("name") or "").strip()
    id_partner = payload.get("id_partner")
    id_modality = payload.get("id_modality")
    id_week_days = payload.get("id_week_days")
    id_schedule = payload.get("id_schedule")
    slots = payload.get("slots", 0)

    schedule_description = (payload.get("schedule_description") or "").strip() or None
    team_owners = (payload.get("team_owners") or "").strip() or None
    objectives = (payload.get("objectives") or "").strip() or None
    activities = (payload.get("activities") or "").strip() or None
    clave = (payload.get("clave") or "").strip() or None
    competencies = (payload.get("competencies") or "").strip() or None
    location = (payload.get("location") or "").strip() or None
    duration = (payload.get("duration") or "").strip() or None
    audience = (payload.get("audience") or "").strip() or None
    max_hours = payload.get("max_hours")
    comments = (payload.get("comments") or "").strip() or None

    if not name:
        return jsonify({"error": "name es obligatorio"}), 400

    try:
        id_partner = int(id_partner)
        id_modality = int(id_modality)
        id_week_days = int(id_week_days)
        id_schedule = int(id_schedule)
        slots = int(slots)
        if slots < 0:
            return jsonify({"error": "slots debe ser >= 0"}), 400
    except:
        return jsonify({"error": "IDs de catálogos y slots deben ser numéricos"}), 400

    if max_hours not in (None, ""):
        try:
            max_hours = int(max_hours)
            if max_hours < 0:
                return jsonify({"error": "max_hours debe ser >= 0"}), 400
        except:
            return jsonify({"error": "max_hours debe ser numérico"}), 400
    else:
        max_hours = None

    def tx(conn, cur):
        # validar catálogos
        checks = [
            ("partner", id_partner),
            ("modality", id_modality),
            ("week_days", id_week_days),
            ("schedule", id_schedule),
        ]
        for table, value in checks:
            cur.execute(f"SELECT id FROM {table} WHERE id=%s LIMIT 1", [value])
            if not cur.fetchone():
                return {"error": f"Valor no encontrado en {table}", "status": 404}

        cur.execute(
            """
            INSERT INTO project
            (
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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            [
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
                comments,
            ]
        )

        return {
            "status": 201,
            "project_id": cur.lastrowid,
            "message": "Proyecto maestro creado"
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


@admin_master_projects_bp.patch("/api/admin/projects/<int:project_id>")
def update_master_project(project_id: int):
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}
    if not payload:
        return jsonify({"error": "No se enviaron cambios"}), 400

    allowed_fields = {
        "name",
        "id_partner",
        "id_modality",
        "id_week_days",
        "id_schedule",
        "slots",
        "schedule_description",
        "team_owners",
        "objectives",
        "activities",
        "clave",
        "competencies",
        "location",
        "duration",
        "audience",
        "max_hours",
        "comments"
    }

    unknown = [k for k in payload.keys() if k not in allowed_fields]
    if unknown:
        return jsonify({"error": f"Campos no permitidos: {', '.join(unknown)}"}), 400

    def tx(conn, cur):
        cur.execute(
            "SELECT id FROM project WHERE id=%s LIMIT 1 FOR UPDATE",
            [project_id]
        )
        if not cur.fetchone():
            return {"error": "Proyecto no encontrado", "status": 404}

        updates = []
        params = []

        numeric_fields = {"id_partner", "id_modality", "id_week_days", "id_schedule", "slots", "max_hours"}

        for field, value in payload.items():
            if field in numeric_fields and value not in (None, ""):
                try:
                    value = int(value)
                    if field in ("slots", "max_hours") and value < 0:
                        return {"error": f"{field} debe ser >= 0", "status": 400}
                except:
                    return {"error": f"{field} debe ser numérico", "status": 400}

            if field in ("name",) and not str(value).strip():
                return {"error": f"{field} no puede ir vacío", "status": 400}

            updates.append(f"{field} = %s")
            params.append((str(value).strip() if isinstance(value, str) else value))

        if not updates:
            return {"error": "No hay cambios válidos", "status": 400}

        params.append(project_id)

        cur.execute(
            f"""
            UPDATE project
            SET {', '.join(updates)}
            WHERE id = %s
            """,
            params
        )

        return {"status": 200, "message": "Proyecto maestro actualizado"}

    try:
        result = execute_tx(tx)

        if result.get("status") != 200:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify(result), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500