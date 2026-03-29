from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx, fetch_all, fetch_one
from ..authz import require_role, ROLE_ADMIN

admin_event_projects_bp = Blueprint("admin_event_projects", __name__)


@admin_event_projects_bp.get("/api/admin/events/<int:event_id>/projects")
def list_event_projects(event_id: int):
    role = require_role(request, {ROLE_ADMIN})
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
            pa.name AS partner
        FROM event_projects ep
        JOIN project p ON p.id = ep.project_id
        JOIN partner pa ON pa.id = p.id_partner
        WHERE ep.event_id = %s
        ORDER BY p.name
    """

    rows = fetch_all(sql, [event_id])
    return jsonify(rows), 200


@admin_event_projects_bp.post("/api/admin/events/<int:event_id>/projects")
def add_project_to_event(event_id: int):
    role = require_role(request, {ROLE_ADMIN})
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
        cur.execute("SELECT id FROM events WHERE id=%s LIMIT 1", [event_id])
        if not cur.fetchone():
            return {"error": "Evento no existe", "status": 404}

        # validar proyecto
        cur.execute("SELECT id FROM project WHERE id=%s LIMIT 1", [project_id])
        if not cur.fetchone():
            return {"error": "Proyecto no existe", "status": 404}

        # evitar duplicados
        cur.execute("""
            SELECT id FROM event_projects
            WHERE event_id=%s AND project_id=%s
            LIMIT 1
        """, [event_id, project_id])

        if cur.fetchone():
            return {"error": "El proyecto ya está en esta temporada", "status": 409}

        cur.execute("""
            INSERT INTO event_projects
            (event_id, project_id, slots_total, status)
            VALUES (%s, %s, %s, 'ACTIVE')
        """, [event_id, project_id, slots_total])

        return {"status": 201, "message": "Proyecto agregado a la temporada"}

    try:
        result = execute_tx(tx)

        if result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({"message": result["message"]}), 201

    except Error as e:
        return jsonify({"error": e.msg}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_event_projects_bp.patch("/api/admin/event-projects/<int:event_project_id>")
def update_event_project(event_project_id: int):
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado"}), 401

    payload = request.get_json(silent=True) or {}

    slots_total = payload.get("slots_total")
    status = payload.get("status")

    updates = []
    params = []

    if slots_total is not None:
        try:
            slots_total = int(slots_total)
            if slots_total < 0:
                return jsonify({"error": "slots_total inválido"}), 400
        except:
            return jsonify({"error": "slots_total debe ser numérico"}), 400

        updates.append("slots_total = %s")
        params.append(slots_total)

    if status is not None:
        status = status.upper()
        if status not in ("ACTIVE", "HIDDEN", "CLOSED"):
            return jsonify({"error": "status inválido"}), 400

        updates.append("status = %s")
        params.append(status)

    if not updates:
        return jsonify({"error": "No hay cambios"}), 400

    def tx(conn, cur):
        cur.execute("""
            SELECT id FROM event_projects
            WHERE id = %s
            LIMIT 1
            FOR UPDATE
        """, [event_project_id])

        if not cur.fetchone():
            return {"error": "Registro no encontrado", "status": 404}

        params.append(event_project_id)

        cur.execute(f"""
            UPDATE event_projects
            SET {', '.join(updates)}
            WHERE id = %s
        """, params)

        return {"status": 200, "message": "Actualizado"}

    try:
        result = execute_tx(tx)

        if result.get("status") != 200:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({"message": result["message"]}), 200

    except Error as e:
        return jsonify({"error": e.msg}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500