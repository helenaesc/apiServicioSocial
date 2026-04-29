from flask import Blueprint, jsonify, request, session
from mysql.connector import Error
from ..database import execute_tx, fetch_all, fetch_one
from ..authz import require_role, ROLE_ADMIN

admin_event_projects_bp = Blueprint("admin_event_projects", __name__)


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


@admin_event_projects_bp.get("/api/admin/events/<int:event_id>/projects")
def list_event_projects(event_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401

    sql = """
        SELECT
            ep.id,
            ep.event_id, 
            ep.project_id,
            ep.slots_total,
            ep.status,
            p.name,
            p.general_name,
            pa.name AS partner,

            (
              SELECT COUNT(*)
              FROM registrations r
              WHERE r.event_project_id = ep.id
                AND r.status = 'ACTIVE'
            ) AS registered_count,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
                AND pt.status = 'AVAILABLE'
                AND (pt.expires_at IS NULL OR pt.expires_at > NOW())
            ) AS tokens_available,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
                AND pt.status = 'USED'
            ) AS tokens_used,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
                AND pt.status = 'REVOKED'
            ) AS tokens_revoked,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
                AND pt.status = 'EXPIRED'
            ) AS tokens_expired,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
            ) AS tokens_total

        FROM event_projects ep
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN partner pa ON pa.id = p.id_partner
        WHERE ep.event_id = %s
        ORDER BY p.general_name, p.name
    """

    rows = fetch_all(sql, [event_id])

    for r in rows:
        slots_total = int(r.get("slots_total") or 0)
        registered_count = int(r.get("registered_count") or 0)
        tokens_total = int(r.get("tokens_total") or 0)
        tokens_available = int(r.get("tokens_available") or 0)

        if tokens_total > 0:
            r["cupos_disponibles"] = tokens_available
        else:
            r["cupos_disponibles"] = max(slots_total - registered_count, 0)

    return jsonify(rows), 200

@admin_event_projects_bp.post("/api/admin/events/<int:event_id>/projects")
def add_project_to_event(event_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401

    payload = request.get_json(silent=True) or {}

    project_id = payload.get("project_id")
    slots_total = payload.get("slots_total", 0)

    if not project_id:
        return jsonify({"error": "project_id es obligatorio"}), 400

    try:
        slots_total = int(slots_total)
        if slots_total < 0:
            return jsonify({"error": "slots_total debe ser >= 0"}), 400
    except:
        return jsonify({"error": "slots_total debe ser numérico"}), 400

    def tx(conn, cur):
        # validar evento
        cur.execute(
            """
            SELECT id
            FROM events
            WHERE id = %s
            LIMIT 1
            """,
            [event_id]
        )
        if not cur.fetchone():
            return {"error": "Evento no existe", "status": 404}

        # validar proyecto
        cur.execute(
            """
            SELECT id
            FROM project
            WHERE id = %s
            LIMIT 1
            """,
            [project_id]
        )
        if not cur.fetchone():
            return {"error": "Proyecto no existe", "status": 404}

        # evitar duplicados
        cur.execute(
            """
            SELECT id
            FROM event_projects
            WHERE event_id = %s
              AND project_id = %s
            LIMIT 1
            """,
            [event_id, project_id]
        )
        if cur.fetchone():
            return {"error": "El proyecto ya está en esta temporada", "status": 409}

        cur.execute(
            """
            INSERT INTO event_projects
            (event_id, project_id, slots_total, status)
            VALUES (%s, %s, %s, 'ACTIVE')
            """,
            [event_id, project_id, slots_total]
        )

        event_project_id = cur.lastrowid

        cur.execute(
            """
            SELECT
                ep.id,
                ep.event_id,
                ep.project_id,
                ep.slots_total,
                ep.status,
                p.name,
                pa.name AS partner
            FROM event_projects ep
            JOIN project p ON p.id = ep.project_id
            LEFT JOIN partner pa ON pa.id = p.id_partner
            WHERE ep.id = %s
            LIMIT 1
            """,
            [event_project_id]
        )
        final_row = cur.fetchone()

        return {
            "status": 201,
            "message": "Proyecto agregado a la temporada",
            "performed_by": {
                "role": role
            },
            "event_project": final_row
        }

    try:
        result = execute_tx(tx)

        if result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify(result), 201

    except Error as e:
        return jsonify({"error": e.msg}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_event_projects_bp.patch("/api/admin/event-projects/<int:event_project_id>")
def update_event_project(event_project_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401

    payload = request.get_json(silent=True) or {}

    slots_total = payload.get("slots_total")
    status = payload.get("status")

    requested_slots_total = None
    requested_status = None

    if slots_total is not None:
        try:
            requested_slots_total = int(slots_total)
            if requested_slots_total < 0:
                return jsonify({"error": "slots_total inválido"}), 400
        except:
            return jsonify({"error": "slots_total debe ser numérico"}), 400

    if status is not None:
        requested_status = str(status).upper().strip()
        if requested_status not in ("ACTIVE", "HIDDEN", "CLOSED"):
            return jsonify({"error": "status inválido"}), 400

    if requested_slots_total is None and requested_status is None:
        return jsonify({"error": "No hay cambios"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            SELECT
                id,
                event_id,
                project_id,
                slots_total,
                status
            FROM event_projects
            WHERE id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [event_project_id]
        )
        ep = cur.fetchone()

        if not ep:
            return {"error": "Registro no encontrado", "status": 404}

        # Conteo de tokens comprometidos
        cur.execute(
            """
            SELECT
                SUM(CASE WHEN status = 'USED' THEN 1 ELSE 0 END) AS used_count,
                SUM(CASE WHEN status = 'AVAILABLE' THEN 1 ELSE 0 END) AS available_count,
                SUM(CASE WHEN status = 'RESERVED' THEN 1 ELSE 0 END) AS reserved_count
            FROM project_tokens
            WHERE event_project_id = %s
            """,
            [event_project_id]
        )
        token_counts = cur.fetchone() or {}

        used_count = int(token_counts.get("used_count") or 0)
        available_count = int(token_counts.get("available_count") or 0)
        reserved_count = int(token_counts.get("reserved_count") or 0)

        committed_capacity = used_count + available_count + reserved_count

        # Si quieren bajar slots, respetar capacidad comprometida
        if requested_slots_total is not None:
            if requested_slots_total < committed_capacity:
                return {
                    "error": (
                        f"No puedes bajar slots_total a {requested_slots_total}. "
                        f"Actualmente hay {committed_capacity} lugares comprometidos "
                        f"(USED={used_count}, AVAILABLE={available_count}, RESERVED={reserved_count}). "
                        f"Revoca tokens abiertos primero o usa un valor mayor o igual a {committed_capacity}."
                    ),
                    "status": 409
                }

        updates = []
        params = []

        if requested_slots_total is not None:
            updates.append("slots_total = %s")
            params.append(requested_slots_total)

        if requested_status is not None:
            updates.append("status = %s")
            params.append(requested_status)

        if not updates:
            return {"error": "No hay cambios válidos", "status": 400}

        params.append(event_project_id)

        cur.execute(
            f"""
            UPDATE event_projects
            SET {', '.join(updates)}
            WHERE id = %s
            """,
            params
        )

        cur.execute(
            """
            SELECT
                ep.id,
                ep.event_id,
                ep.project_id,
                ep.slots_total,
                ep.status,
                p.name,
                pa.name AS partner
            FROM event_projects ep
            JOIN project p ON p.id = ep.project_id
            LEFT JOIN partner pa ON pa.id = p.id_partner
            WHERE ep.id = %s
            LIMIT 1
            """,
            [event_project_id]
        )
        final_row = cur.fetchone()

        return {
            "status": 200,
            "message": "Actualizado",
            "performed_by": {
                "role": role
            },
            "event_project": final_row,
            "capacity": {
                "used": used_count,
                "available": available_count,
                "reserved": reserved_count,
                "committed": committed_capacity
            }
        }

    try:
        result = execute_tx(tx)

        if result.get("status") != 200:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify(result), 200

    except Error as e:
        return jsonify({"error": e.msg}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500