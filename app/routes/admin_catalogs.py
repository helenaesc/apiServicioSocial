from flask import Blueprint, jsonify, request
from ..database import fetch_all
from ..authz import require_role, ROLE_ADMIN

admin_catalogs_bp = Blueprint("admin_catalogs", __name__)

@admin_catalogs_bp.get("/api/admin/catalogs")
def admin_catalogs():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    return jsonify({
        "socio": fetch_all("SELECT id, name FROM partner ORDER BY name"),
        "dias": fetch_all("SELECT id, name AS description FROM week_days ORDER BY id"),
        "modalidad": fetch_all("SELECT id, name AS description FROM modality ORDER BY id"),
        "horario": fetch_all("SELECT id, name AS description FROM schedule ORDER BY id"),
        "status": fetch_all("SELECT id, name FROM status ORDER BY id"),
        "partner_group": fetch_all("SELECT id, name FROM partner_group ORDER BY name"),
    }), 200