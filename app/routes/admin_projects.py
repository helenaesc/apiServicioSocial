import os
from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx
from ..authz import require_role, ROLE_ADMIN

admin_projects_bp = Blueprint("admin_projects", __name__)

@admin_projects_bp.post("/api/admin/projects")
def create_project():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}

    season = (payload.get("season") or "").strip() or None
    name = (payload.get("name") or "").strip()
    team_owners = (payload.get("team_owners") or "").strip() or None

    partner_id = payload.get("partner_id")  
    modality_id = payload.get("modality_id")
    week_days_id = payload.get("week_days_id")
    schedule_id = payload.get("schedule_id")
    slots = payload.get("slots")
    schedule_description = (payload.get("schedule_description") or "").strip() or None


    academy_mode = (payload.get("academy_mode") or "ALL").strip().upper()
    academy_group_id = payload.get("academy_group_id")
    partner_ids = payload.get("partner_ids") or []


    objectives = payload.get("objectives")
    activities = payload.get("activities")
    clave = payload.get("clave")
    competencies = payload.get("competencies")
    location = payload.get("location")
    duration = payload.get("duration")
    audience = payload.get("audience")
    max_hours = payload.get("max_hours")
    comments = payload.get("comments")

    if not name:
        return jsonify({"error": "name es obligatorio"}), 400

    for field, val in [
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

    if max_hours is not None and max_hours != "":
        try:
            max_hours = int(max_hours)
            if max_hours < 0:
                return jsonify({"error": "max_hours debe ser >= 0"}), 400
        except:
            return jsonify({"error": "max_hours debe ser número"}), 400
    else:
        max_hours = None

    if academy_mode not in {"ALL", "GROUP", "CUSTOM"}:
        return jsonify({"error": "academy_mode inválido (ALL/GROUP/CUSTOM)"}), 400

    if academy_mode == "ALL":
        academy_group_id = None
        partner_ids = []

    if academy_mode == "GROUP":
        if not academy_group_id:
            return jsonify({"error": "academy_group_id es obligatorio cuando academy_mode=GROUP"}), 400
        partner_ids = []

    if academy_mode == "CUSTOM":
        if not isinstance(partner_ids, list):
            return jsonify({"error": "partner_ids debe ser una lista"}), 400
        if not partner_ids:
            return jsonify({"error": "partner_ids es obligatorio cuando academy_mode=CUSTOM"}), 400
        try:
            partner_ids = [int(x) for x in partner_ids]
        except:
            return jsonify({"error": "partner_ids debe contener IDs numéricos"}), 400
        academy_group_id = None  

    def tx(conn, cur):

        if not partner_id:
            cur.execute("SELECT id FROM partner WHERE name=%s LIMIT 1", ["Sin preferencia"])
            row = cur.fetchone()
            if not row:
                return {"error": "No existe el partner default 'Sin preferencia'", "status": 500}
            pid_default = row["id"]
            pid_to_use = pid_default
        else:
          pid_to_use = partner_id

        cur.execute("SELECT id FROM partner WHERE id=%s LIMIT 1", [pid_to_use])
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

        if academy_mode == "GROUP":
            cur.execute("SELECT id FROM partner_group WHERE id=%s LIMIT 1", [academy_group_id])
            if not cur.fetchone():
                return {"error": "academy_group_id no existe", "status": 400}

        cur.execute(
            """
            SELECT id FROM project
            WHERE name=%s AND id_partner=%s AND id_modality=%s AND id_week_days=%s AND id_schedule=%s
            LIMIT 1
            """,
            [name, pid_to_use, modality_id, week_days_id, schedule_id],
        )
        if cur.fetchone():
            return {"error": "Proyecto ya existe con esas características", "status": 409}

        cur.execute(
            """
            INSERT INTO project
              (name, id_partner, id_modality, id_week_days, id_schedule,
               slots, schedule_description, season,
               academy_mode, academy_group_id,
               team_owners, objectives, activities, clave,
               competencies, location, duration, audience, max_hours, comments)
            VALUES
              (%s, %s, %s, %s, %s,
               %s, %s, %s,
               %s, %s,
               %s, %s, %s, %s,
               %s, %s, %s, %s, %s, %s)
            """,
            [name, pid_to_use, modality_id, week_days_id, schedule_id,
             slots, schedule_description, season,
             academy_mode, academy_group_id,
             team_owners, objectives, activities, clave,
             competencies, location, duration, audience, max_hours, comments],
        )
        new_id = cur.lastrowid

        if academy_mode == "CUSTOM":
            for pid in partner_ids:
                cur.execute("SELECT id FROM partner WHERE id=%s LIMIT 1", [pid])
                if not cur.fetchone():
                    return {"error": f"partner_id inválido en partner_ids: {pid}", "status": 400}

            for pid in partner_ids:
                cur.execute(
                    "INSERT IGNORE INTO project_partner_pref (project_id, partner_id) VALUES (%s, %s)",
                    [new_id, pid],
                )

        return {"id": new_id, "status": 201}

    try:
        result = execute_tx(tx)
        if result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]
        return jsonify({"id": result["id"], "message": "Proyecto creado"}), 201
    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500