from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx
import os

admin_projects_bp = Blueprint("admin_projects", __name__)

def _require_admin_key(req):
    key = req.headers.get("X-ADMIN-KEY", "")
    expected = os.getenv("ADMIN_API_KEY", "")
    return bool(expected) and key == expected

@admin_projects_bp.post("/api/admin/projects")
def create_project():
    if not _require_admin_key(request):
        return jsonify({"error": "No autorizado (X-ADMIN-KEY)"}), 401

    payload = request.get_json(silent=True) or {}

    name = (payload.get("name") or "").strip()
    partner_id = payload.get("partner_id")
    modality_id = payload.get("modality_id")
    week_days_id = payload.get("week_days_id")
    schedule_id = payload.get("schedule_id")
    slots = payload.get("slots")
    schedule_description = payload.get("schedule_description")
    project_description = payload.get("project_description")

    if not name:
        return jsonify({"error": "name es obligatorio"}), 400
    for field, val in [
        ("partner_id", partner_id),
        ("modality_id", modality_id),
        ("week_days_id", week_days_id),
        ("schedule_id", schedule_id),
        ("slots", slots),
    ]:
        if val is None:
            return jsonify({"error": f"{field} es obligatorio"}), 400

    try:
        slots = int(slots)
        if slots < 0:
            return jsonify({"error": "slots debe ser >= 0"}), 400
    except:
        return jsonify({"error": "slots debe ser número"}), 400

    def tx(conn, cur):
        cur.execute("SELECT id FROM partner WHERE id=%s LIMIT 1", [partner_id])
        if not cur.fetchone():
            return {"error": "partner_id no existe", "status": 400}

        cur.execute("SELECT id FROM modality WHERE id=%s LIMIT 1", [modality_id])
        if not cur.fetchone():
            return {"error": "modality_id no existe", "status": 400}

        cur.execute("SELECT id FROM week_days WHERE id=%s LIMIT 1", [week_days_id])
        if not cur.fetchone():
            return {"error": "week_days_id no existe", "status": 400}

        cur.execute("SELECT id FROM schedule WHERE id=%s LIMIT 1", [schedule_id])
        if not cur.fetchone():
            return {"error": "schedule_id no existe", "status": 400}


        cur.execute(
            """
            SELECT id FROM project
            WHERE name=%s AND id_partner=%s AND id_modality=%s AND id_week_days=%s AND id_schedule=%s
            LIMIT 1
            """,
            [name, partner_id, modality_id, week_days_id, schedule_id],
        )
        existing = cur.fetchone()
        if existing:
            return {"error": "Proyecto ya existe con esas características", "status": 409}

        cur.execute(
            """
            INSERT INTO project
              (name, id_partner, id_modality, id_week_days, id_schedule,
               slots, schedule_description, project_description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            [name, partner_id, modality_id, week_days_id, schedule_id,
             slots, schedule_description, project_description],
        )
        new_id = cur.lastrowid
        return {"id": new_id, "status": 201}

    result = execute_tx(tx)
    if result.get("status") != 201:
        return jsonify({"error": result["error"]}), result["status"]
    return jsonify({"id": result["id"], "message": "Proyecto creado"}), 201