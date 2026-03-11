from flask import Blueprint, jsonify
from ..database import fetch_all

catalogs_bp = Blueprint("catalogs", __name__)

@catalogs_bp.get("/api/catalogs")
def catalogs():
    return jsonify({
        "socio": fetch_all("SELECT id, name FROM partner ORDER BY name"),
        "dias": fetch_all("SELECT id, name AS description FROM week_days ORDER BY id"),
        "modalidad": fetch_all("SELECT id, name AS description FROM modality ORDER BY id"),
        "horario": fetch_all("SELECT id, name AS description FROM schedule ORDER BY id"),
        "status": fetch_all("SELECT id, name FROM status ORDER BY id"),
    })