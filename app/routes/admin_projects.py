from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx
from ..authz import require_role, ROLE_ADMIN
import os

admin_projects_bp = Blueprint("admin_projects", __name__)

@admin_projects_bp.post("/api/admin/projects")
def create_project():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}),401

    payload = request.get_json(silent=True) or {}
    
    season = payload.get("season")
    name = (payload.get("name") or "").strip()
    partner_id = payload.get("partner_id")
    modality_id = payload.get("modality_id")
    week_days_id = payload.get("week_days_id")
    schedule_id = payload.get("schedule_id")
    slots = payload.get("slots")
    schedule_description = payload.get("schedule_description")
    project_description = payload.get("project_description")
    team_owners = payload.get("team_owners")
    carreer = payload.get("carreer")
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

    if max_hours is not None and max_hours != "":
        try:
            max_hours = int(max_hours)
            if max_hours < 0:
                return jsonify({"error": "max_hours debe ser >= 0"}), 400
        except:
            return jsonify({"error": "max_hours debe ser número"}), 400
    else:
        max_hours = None

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
                slots, schedule_description, project_description, season,
                team_owners, carreers, objectives, activities, clave,
                competencies, location, duration, audience, max_hours, comments)
            VALUES (%s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s)
            """,
            [name, partner_id, modality_id, week_days_id, schedule_id,
            slots, schedule_description, project_description,
            team_owners, carreer, objectives, activities, clave,
            competencies, location, duration, audience, max_hours, comments],   
        )
        new_id = cur.lastrowid
        return {"id": new_id, "status": 201}

    result = execute_tx(tx)
    if result.get("status") != 201:
        return jsonify({"error": result["error"]}), result["status"]
    return jsonify({"id": result["id"], "message": "Proyecto creado"}), 201