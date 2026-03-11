from flask import Blueprint, jsonify, request
from ..authz import get_role

admin_auth_bp = Blueprint("admin_auth", __name__)

@admin_auth_bp.get("/api/admin/ping")
def admin_ping():
    role = get_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401
    return jsonify({"ok": True, "role": role})