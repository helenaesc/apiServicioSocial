import os
from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx
from ..authz import require_role, ROLE_ADMIN

admin_projects_bp = Blueprint("admin_projects", __name__)

@admin_projects_bp.route("/api/admin/projects/<int:project_id>/slots", methods=["PATCH"])
def update_project_slots(project_id: int):
    role = require_role(request, {ROLE_ADMIN})
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
        # Lock del proyecto para evitar carreras
        cur.execute("SELECT id, slots FROM project WHERE id=%s LIMIT 1 FOR UPDATE", [project_id])
        proj = cur.fetchone()
        if not proj:
            return {"error": "Proyecto no encontrado", "status": 404}

        # Tokens usados (cupo ya consumido)
        cur.execute(
            "SELECT COUNT(*) AS c FROM token WHERE id_project=%s AND used=TRUE",
            [project_id],
        )
        used_count = int(cur.fetchone()["c"])

        # Tokens abiertos y vigentes (ocupando cupo aunque no se hayan usado)
        cur.execute(
            """
            SELECT COUNT(*) AS c
            FROM token
            WHERE id_project=%s
              AND used=FALSE
              AND revoked=FALSE
              AND (expires_at IS NULL OR expires_at > NOW())
            """,
            [project_id],
        )
        open_active = int(cur.fetchone()["c"])

        min_needed = used_count + open_active
        if new_slots < min_needed:
            return {
                "error": f"No puedes bajar slots a {new_slots}. Mínimo requerido: {min_needed} (usados={used_count}, abiertos={open_active}).",
                "status": 409
            }

        cur.execute("UPDATE project SET slots=%s WHERE id=%s", [new_slots, project_id])
        return {"message": "Cupo actualizado", "slots": new_slots, "status": 200}

    try:
        result = execute_tx(tx)
        if result.get("status") != 200:
            return jsonify({"error": result["error"]}), result["status"]
        return jsonify({"message": result["message"], "slots": result["slots"]}), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500