from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx, fetch_all, fetch_one
from ..authz import require_role, ROLE_ADMIN

admin_master_projects_bp = Blueprint("admin_master_projects", __name__)


def _clean_str(value):
    value = str(value).strip() if value is not None else ""
    return value or None


def _required_str(value, field_name):
    value = _clean_str(value)
    if not value:
        raise ValueError(f"{field_name} es obligatorio")
    return value


def _required_int(value, field_name, min_value=None, max_value=None):
    try:
        n = int(value)
    except:
        raise ValueError(f"{field_name} debe ser numérico")

    if min_value is not None and n < min_value:
        raise ValueError(f"{field_name} debe ser >= {min_value}")

    if max_value is not None and n > max_value:
        raise ValueError(f"{field_name} debe ser <= {max_value}")

    return n


def _optional_int(value, field_name, min_value=None, max_value=None):
    if value in (None, ""):
        return None

    try:
        n = int(value)
    except:
        raise ValueError(f"{field_name} debe ser numérico")

    if min_value is not None and n < min_value:
        raise ValueError(f"{field_name} debe ser >= {min_value}")

    if max_value is not None and n > max_value:
        raise ValueError(f"{field_name} debe ser <= {max_value}")

    return n


def _normalize_partner_ids(raw_partner_ids, fallback_id):
    ids = []

    if isinstance(raw_partner_ids, list):
        for value in raw_partner_ids:
            try:
                n = int(value)
                if n > 0 and n not in ids:
                    ids.append(n)
            except:
                pass

    if fallback_id and fallback_id not in ids:
        ids.insert(0, fallback_id)

    return ids


def _attach_partner_ids(rows):
    for row in rows:
        csv = row.get("partner_ids_csv") or ""
        row["partner_ids"] = [
            int(x) for x in csv.split(",")
            if x.strip().isdigit()
        ]
        row["partner_names"] = row.get("partner_names") or row.get("partner_name") or "Sin preferencia"
        row.pop("partner_ids_csv", None)
    return rows


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
              p.general_name LIKE %s
              OR p.name LIKE %s
              OR p.objectives LIKE %s
              OR p.activities LIKE %s
              OR p.clave LIKE %s
              OR p.competencies LIKE %s
              OR p.location LIKE %s
              OR p.audience LIKE %s
              OR pa.name LIKE %s
              OR EXISTS (
                    SELECT 1
                    FROM project_partner_pref ppp2
                    JOIN partner pa2 ON pa2.id = ppp2.partner_id
                    WHERE ppp2.project_id = p.id
                      AND pa2.name LIKE %s
              )
            )
        """)
        like = f"%{q}%"
        params.extend([like, like, like, like, like, like, like, like, like, like])

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
            p.academy_mode,
            p.academy_group_id,

            pa.name AS partner_name,
            m.name AS modality_name,
            wd.name AS week_days_name,
            sc.name AS schedule_name,

            GROUP_CONCAT(DISTINCT ppp.partner_id ORDER BY ppp.partner_id SEPARATOR ',') AS partner_ids_csv,
            GROUP_CONCAT(DISTINCT pp.name ORDER BY pp.name SEPARATOR ', ') AS partner_names

        FROM project p
        LEFT JOIN partner pa ON pa.id = p.id_partner
        LEFT JOIN modality m ON m.id = p.id_modality
        LEFT JOIN week_days wd ON wd.id = p.id_week_days
        LEFT JOIN schedule sc ON sc.id = p.id_schedule
        LEFT JOIN project_partner_pref ppp ON ppp.project_id = p.id
        LEFT JOIN partner pp ON pp.id = ppp.partner_id
        {where_sql}
        GROUP BY
            p.id,
            p.general_name,
            p.name,
            p.id_partner,
            p.id_modality,
            p.id_week_days,
            p.id_schedule,
            p.slots,
            p.schedule_description,
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
            p.academy_mode,
            p.academy_group_id,
            pa.name,
            m.name,
            wd.name,
            sc.name
        ORDER BY p.general_name, p.name, p.id DESC
    """

    rows = fetch_all(sql, params)
    return jsonify(_attach_partner_ids(rows)), 200


@admin_master_projects_bp.get("/api/admin/projects/<int:project_id>")
def get_master_project(project_id: int):
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    sql = """
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
            p.academy_mode,
            p.academy_group_id,

            pa.name AS partner_name,
            m.name AS modality_name,
            wd.name AS week_days_name,
            sc.name AS schedule_name,

            GROUP_CONCAT(DISTINCT ppp.partner_id ORDER BY ppp.partner_id SEPARATOR ',') AS partner_ids_csv,
            GROUP_CONCAT(DISTINCT pp.name ORDER BY pp.name SEPARATOR ', ') AS partner_names

        FROM project p
        LEFT JOIN partner pa ON pa.id = p.id_partner
        LEFT JOIN modality m ON m.id = p.id_modality
        LEFT JOIN week_days wd ON wd.id = p.id_week_days
        LEFT JOIN schedule sc ON sc.id = p.id_schedule
        LEFT JOIN project_partner_pref ppp ON ppp.project_id = p.id
        LEFT JOIN partner pp ON pp.id = ppp.partner_id
        WHERE p.id = %s
        GROUP BY
            p.id,
            p.general_name,
            p.name,
            p.id_partner,
            p.id_modality,
            p.id_week_days,
            p.id_schedule,
            p.slots,
            p.schedule_description,
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
            p.academy_mode,
            p.academy_group_id,
            pa.name,
            m.name,
            wd.name,
            sc.name
        LIMIT 1
    """

    row = fetch_one(sql, [project_id])

    if not row:
        return jsonify({"error": "Proyecto no encontrado"}), 404

    return jsonify(_attach_partner_ids([row])[0]), 200


@admin_master_projects_bp.post("/api/admin/projects")
def create_master_project():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}

    try:
        general_name = _required_str(payload.get("general_name"), "general_name")
        name = _required_str(payload.get("name"), "name")

        id_partner = _required_int(payload.get("id_partner"), "id_partner", min_value=1)
        id_modality = _required_int(payload.get("id_modality"), "id_modality", min_value=1)
        id_week_days = _required_int(payload.get("id_week_days"), "id_week_days", min_value=1)
        id_schedule = _required_int(payload.get("id_schedule"), "id_schedule", min_value=1)

        partner_ids = _normalize_partner_ids(payload.get("partner_ids"), id_partner)
        if not partner_ids:
            raise ValueError("Debes seleccionar al menos una carrera preferida")

        slots = _required_int(payload.get("slots", 0), "slots", min_value=0, max_value=5000)
        max_hours = _optional_int(payload.get("max_hours"), "max_hours", min_value=0, max_value=1000)

        schedule_description = _clean_str(payload.get("schedule_description"))
        objectives = _required_str(payload.get("objectives"), "objectives")
        activities = _required_str(payload.get("activities"), "activities")
        clave = _clean_str(payload.get("clave"))
        competencies = _clean_str(payload.get("competencies"))
        location = _clean_str(payload.get("location"))
        duration = _clean_str(payload.get("duration"))
        audience = _clean_str(payload.get("audience"))
        comments = _clean_str(payload.get("comments"))
        season = _clean_str(payload.get("season"))

        academy_mode = _clean_str(payload.get("academy_mode")) or "CUSTOM"
        academy_group_id = payload.get("academy_group_id")

        if academy_mode not in ("ALL", "GROUP", "CUSTOM"):
            return jsonify({"error": "academy_mode inválido"}), 400

        if academy_mode == "GROUP":
            academy_group_id = _required_int(academy_group_id, "academy_group_id", min_value=1)
        else:
            academy_group_id = None

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    def tx(conn, cur):
        for table, value, label in [
            ("partner", id_partner, "Carrera principal"),
            ("modality", id_modality, "Modalidad"),
            ("week_days", id_week_days, "Días"),
            ("schedule", id_schedule, "Horario"),
        ]:
            cur.execute(f"SELECT id FROM {table} WHERE id=%s LIMIT 1", [value])
            if not cur.fetchone():
                return {"error": f"{label} no encontrado", "status": 404}

        for partner_id in partner_ids:
            cur.execute("SELECT id FROM partner WHERE id=%s LIMIT 1", [partner_id])
            if not cur.fetchone():
                return {"error": f"Carrera preferida no encontrada: {partner_id}", "status": 404}

        if academy_group_id:
            cur.execute("SELECT id FROM partner_group WHERE id=%s LIMIT 1", [academy_group_id])
            if not cur.fetchone():
                return {"error": "Grupo de carreras no encontrado", "status": 404}

        cur.execute(
            """
            SELECT id
            FROM project
            WHERE general_name = %s
              AND name = %s
              AND id_modality = %s
              AND id_week_days = %s
              AND id_schedule = %s
            LIMIT 1
            FOR UPDATE
            """,
            [general_name, name, id_modality, id_week_days, id_schedule]
        )

        if cur.fetchone():
            return {
                "error": "Ya existe un proyecto con ese nombre general, nombre, modalidad, días y horario",
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
                comments,
                season,
                academy_mode,
                academy_group_id
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s, NULL,
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s
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
                objectives,
                activities,
                clave,
                competencies,
                location,
                duration,
                audience,
                max_hours,
                comments,
                season,
                academy_mode,
                academy_group_id,
            ]
        )

        project_id = cur.lastrowid

        for partner_id in partner_ids:
            cur.execute(
                """
                INSERT INTO project_partner_pref (project_id, partner_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE partner_id = VALUES(partner_id)
                """,
                [project_id, partner_id]
            )

        return {
            "status": 201,
            "project_id": project_id,
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
        "general_name",
        "name",
        "id_partner",
        "partner_ids",
        "id_modality",
        "id_week_days",
        "id_schedule",
        "slots",
        "schedule_description",
        "objectives",
        "activities",
        "clave",
        "competencies",
        "location",
        "duration",
        "audience",
        "max_hours",
        "comments",
        "season",
        "academy_mode",
        "academy_group_id",
    }

    unknown = [k for k in payload.keys() if k not in allowed_fields]
    if unknown:
        return jsonify({"error": f"Campos no permitidos: {', '.join(unknown)}"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            SELECT id, id_partner
            FROM project
            WHERE id=%s
            LIMIT 1
            FOR UPDATE
            """,
            [project_id]
        )
        current = cur.fetchone()

        if not current:
            return {"error": "Proyecto no encontrado", "status": 404}

        updates = []
        params = []

        numeric_fields = {
            "id_partner",
            "id_modality",
            "id_week_days",
            "id_schedule",
            "slots",
            "max_hours",
            "academy_group_id",
        }

        text_required = {"general_name", "name", "objectives", "activities"}

        partner_ids = None

        for field, value in payload.items():
            if field == "partner_ids":
                fallback_id = payload.get("id_partner") or current["id_partner"]
                try:
                    fallback_id = int(fallback_id)
                except:
                    fallback_id = current["id_partner"]

                partner_ids = _normalize_partner_ids(value, fallback_id)
                if not partner_ids:
                    return {"error": "Debes seleccionar al menos una carrera preferida", "status": 400}
                continue

            if field == "academy_mode":
                value = _clean_str(value) or "CUSTOM"
                if value not in ("ALL", "GROUP", "CUSTOM"):
                    return {"error": "academy_mode inválido", "status": 400}

            if field in numeric_fields and value not in (None, ""):
                try:
                    value = int(value)
                    if field in ("slots", "max_hours") and value < 0:
                        return {"error": f"{field} debe ser >= 0", "status": 400}
                    if field not in ("slots", "max_hours") and value < 1:
                        return {"error": f"{field} debe ser >= 1", "status": 400}
                except:
                    return {"error": f"{field} debe ser numérico", "status": 400}

            if field in text_required and not _clean_str(value):
                return {"error": f"{field} no puede ir vacío", "status": 400}

            if field in allowed_fields:
                updates.append(f"{field} = %s")
                params.append(_clean_str(value) if isinstance(value, str) else value)

        if updates:
            params.append(project_id)
            cur.execute(
                f"""
                UPDATE project
                SET {', '.join(updates)}
                WHERE id = %s
                """,
                params
            )

        if partner_ids is not None:
            for partner_id in partner_ids:
                cur.execute("SELECT id FROM partner WHERE id=%s LIMIT 1", [partner_id])
                if not cur.fetchone():
                    return {"error": f"Carrera preferida no encontrada: {partner_id}", "status": 404}

            cur.execute("DELETE FROM project_partner_pref WHERE project_id=%s", [project_id])

            for partner_id in partner_ids:
                cur.execute(
                    """
                    INSERT INTO project_partner_pref (project_id, partner_id)
                    VALUES (%s, %s)
                    """,
                    [project_id, partner_id]
                )

        if not updates and partner_ids is None:
            return {"error": "No hay cambios válidos", "status": 400}

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