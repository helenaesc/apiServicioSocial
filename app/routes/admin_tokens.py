from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx
import os
import secrets

admin_tokens_bp = Blueprint("admin_tokens", __name__)

def _require_admin_key(req):
    key = req.headers.get("X-ADMIN-KEY", "")
    expected = os.getenv("ADMIN_API_KEY", "")
    return bool(expected) and key == expected

def _gen_token(length=10):
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))

@admin_tokens_bp.post("/api/admin/projects/<int:project_id>/tokens")
def generate_tokens(project_id: int):
    if not _require_admin_key(request):
        return jsonify({"error": "No autorizado (X-ADMIN-KEY)"}), 401

    payload = request.get_json(silent=True) or {}
    count = int(payload.get("count", 10))
    length = int(payload.get("length", 10))

    if count <= 0 or count > 500:
        return jsonify({"error": "count debe estar entre 1 y 100"}), 400
    if length < 6 or length > 20:
        return jsonify({"error": "length debe estar entre 6 y 20"}), 400

    def tx(conn, cur):
        cur.execute("SELECT id FROM project WHERE id=%s LIMIT 1", [project_id])
        if not cur.fetchone():
            return {"error": "Proyecto no encontrado", "status": 404}

        created = 0
        attempts = 0
        max_attempts = count * 10

        while created < count and attempts < max_attempts:
            attempts += 1
            tok = _gen_token(length)
            try:
                cur.execute(
                    "INSERT INTO token (id_project, token, used) VALUES (%s, %s, FALSE)",
                    [project_id, tok],
                )
                created += 1
            except Exception:
                continue

        if created < count:
            return {"error": f"Solo se pudieron crear {created} tokens", "status": 500}

        return {"message": "Tokens generados", "created": created, "status": 201}

    try:
        result = execute_tx(tx)
        if result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]
        return jsonify({"message": result["message"], "created": result["created"]}), 201
    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500