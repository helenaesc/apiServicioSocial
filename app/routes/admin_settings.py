from flask import Blueprint, jsonify, request
from ..database import execute_tx, fetch_one
from ..authz import require_role, ROLE_ADMIN

admin_settings_bp = Blueprint("admin_settings", __name__)

@admin_settings_bp.get("/api/admin/settings")
def get_settings():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    row = fetch_one("SELECT v FROM app_settings WHERE k='TOKEN_TTL_HOURS' LIMIT 1")
    hours = int(row["v"]) if row and row.get("v") else 24
    return jsonify({"token_ttl_hours": hours})

@admin_settings_bp.put("/api/admin/settings/token-ttl-hours")
def set_token_ttl():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}
    hours = payload.get("hours")

    try:
        hours = int(hours)
        if hours < 1 or hours > 168:
            return jsonify({"error": "hours debe estar entre 1 y 168"}), 400
    except:
        return jsonify({"error": "hours debe ser número"}), 400

    def tx(conn, cur):
        cur.execute(
            "INSERT INTO app_settings (k,v) VALUES ('TOKEN_TTL_HOURS', %s) "
            "ON DUPLICATE KEY UPDATE v=VALUES(v)",
            [str(hours)]
        )
        return {"status": 200}

    execute_tx(tx)
    return jsonify({"message": "OK", "token_ttl_hours": hours})