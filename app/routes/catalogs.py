from flask import Blueprint, jsonify
from ..database import fetch_all

catalogs_bp = Blueprint("catalogs", __name__)

@catalogs_bp.get("/api/catalogs")
def catalogs():
    return jsonify({
        "socio": fetch_all("SELECT id, name FROM socio ORDER BY name"),
        "dias": fetch_all("SELECT id, description FROM dias ORDER BY id"),
        "modalidad": fetch_all("SELECT id, description FROM modalidad ORDER BY id"),
        "horario": fetch_all("SELECT id, description FROM horario ORDER BY id"),
        "status": fetch_all("SELECT id, name FROM status ORDER BY id"),
    })