from flask import Blueprint, jsonify, render_template_string
from ..database import fetch_one
from ..templates import INDEX_HTML
from ..admin_template import ADMIN_HTML

views_bp = Blueprint("views", __name__)

@views_bp.get("/")
def index():
    return render_template_string(INDEX_HTML)

@views_bp.get("/health")
def health():
    try:
        row = fetch_one("SELECT 1 AS ok")
        return jsonify({"status": "ok", "db": bool(row and row.get("ok") == 1)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@views_bp.get("/admin")
def admin():
    return render_template_string(ADMIN_HTML)   