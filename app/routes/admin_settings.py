from flask import Blueprint, jsonify, request
from ..database import execute_tx, fetch_one
from ..authz import require_role, ROLE_ADMIN

admin_settings_bp = Blueprint("admin_settings", __name__)


def _get_int_setting(key: str, default: int) -> int:
    row = fetch_one("SELECT v FROM app_settings WHERE k=%s LIMIT 1", [key])
    try:
        return int(row["v"]) if row and row.get("v") is not None else default
    except:
        return default


@admin_settings_bp.get("/api/admin/settings")
def get_settings():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    token_ttl_hours = _get_int_setting("TOKEN_TTL_HOURS", 4)
    pass_ttl_minutes = _get_int_setting("PASS_SESSION_TTL_MINUTES", 2)

    return jsonify({
        "token_ttl_hours": token_ttl_hours,
        "pass_session_ttl_minutes": pass_ttl_minutes
    })


@admin_settings_bp.put("/api/admin/settings/token-ttl-hours")
def set_token_ttl():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}
    hours = payload.get("hours")

    try:
        hours = int(hours)
        if hours < 1 or hours > 24:
            return jsonify({"error": "hours debe estar entre 1 y 24"}), 400
    except:
        return jsonify({"error": "hours debe ser número"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            INSERT INTO app_settings (k, v)
            VALUES ('TOKEN_TTL_HOURS', %s)
            ON DUPLICATE KEY UPDATE v = VALUES(v)
            """,
            [str(hours)]
        )
        return {"status": 200}

    execute_tx(tx)
    return jsonify({
        "message": "OK",
        "token_ttl_hours": hours
    })


@admin_settings_bp.put("/api/admin/settings/pass-ttl-minutes")
def set_pass_ttl_minutes():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}
    minutes = payload.get("minutes")

    try:
        minutes = int(minutes)
        if minutes < 1 or minutes > 5:
            return jsonify({"error": "minutes debe estar entre 1 y 5"}), 400
    except:
        return jsonify({"error": "minutes debe ser número"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            INSERT INTO app_settings (k, v)
            VALUES ('PASS_SESSION_TTL_MINUTES', %s)
            ON DUPLICATE KEY UPDATE v = VALUES(v)
            """,
            [str(minutes)]
        )
        return {"status": 200}

    execute_tx(tx)
    return jsonify({
        "message": "OK",
        "pass_session_ttl_minutes": minutes
    })