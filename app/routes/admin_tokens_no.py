from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx, fetch_one
from ..authz import require_role, ROLE_ADMIN
import secrets

admin_tokens_bp = Blueprint("admin_tokens", __name__)

def _gen_token(length=10):
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))

def _get_ttl_hours(cur) -> int:
    cur.execute("SELECT v FROM app_settings WHERE k='TOKEN_TTL_HOURS' LIMIT 1")
    row = cur.fetchone()
    try:
        return max(1, min(int(row["v"]), 24)) if row and row.get("v") else 4
    except:
        return 4

@admin_tokens_bp.post("/api/admin/projects/<int:project_id>/tokens")
def generate_tokens(project_id: int):
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}

    try:
        count = int(payload.get("count", 10))
        length = int(payload.get("length", 10))
    except:
        return jsonify({"error": "count y length deben ser numéricos"}), 400

    if count <= 0 or count > 200:
        return jsonify({"error": "count debe estar entre 1 y 200"}), 400
    if length < 6 or length > 20:
        return jsonify({"error": "length debe estar entre 6 y 20"}), 400

    def tx(conn, cur):
        cur.execute("SELECT id, slots FROM project WHERE id=%s LIMIT 1 FOR UPDATE", [project_id])
        proj = cur.fetchone()
        if not proj:
            return {"error": "Proyecto no encontrado", "status": 404}

        slots = int(proj.get("slots") or 0)
        if slots <= 0:
            return {"error": "El proyecto tiene slots=0. Sube el cupo antes de generar tokens.", "status": 409}

        ttl_hours = _get_ttl_hours(cur)


        cur.execute(
            "SELECT COUNT(*) AS c FROM token WHERE id_project=%s AND used=TRUE",
            [project_id],
        )
        used_count = int(cur.fetchone()["c"])


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

        remaining = max(slots - (used_count + open_active), 0)
        if remaining <= 0:
            return {"error": "No puedes abrir más cupos: ya alcanzaste el cupo total (slots).", "status": 409}
        if count > remaining:
            return {"error": f"Solo puedes crear {remaining} tokens más (slots={slots}, usados={used_count}, abiertos={open_active}).", "status": 409}

        tokens_created = []
        attempts = 0
        max_attempts = count * 15

        while len(tokens_created) < count and attempts < max_attempts:
            attempts += 1
            tok = _gen_token(length)
            try:
                cur.execute(
                    """
                    INSERT INTO token (id_project, token, used, revoked, expires_at)
                    VALUES (%s, %s, FALSE, FALSE, DATE_ADD(NOW(), INTERVAL %s HOUR))
                    """,
                    [project_id, tok, ttl_hours],
                )
                tokens_created.append(tok)
            except Exception:

                continue

        if len(tokens_created) < count:
            return {"error": f"Solo se pudieron crear {len(tokens_created)} tokens", "status": 500}

        return {
            "message": "Tokens generados",
            "created": len(tokens_created),
            "ttl_hours": ttl_hours,
            "tokens": tokens_created,  
            "status": 201
        }

    try:
        result = execute_tx(tx)
        if result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]
        return jsonify({
            "message": result["message"],
            "created": result["created"],
            "ttl_hours": result["ttl_hours"],
            "tokens": result["tokens"]
        }), 201
    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_tokens_bp.get("/api/admin/projects/<int:project_id>/tokens")
def list_tokens(project_id: int):
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    status = (request.args.get("status") or "active").lower()
    

    where = ["t.id_project=%s"]
    params = [project_id]

    if status == "active":
        where.append("t.used=FALSE AND t.revoked=FALSE AND (t.expires_at IS NULL OR t.expires_at > NOW())")
    elif status == "used":
        where.append("t.used=TRUE")
    elif status == "revoked":
        where.append("t.revoked=TRUE")
    elif status == "expired":
        where.append("t.used=FALSE AND t.revoked=FALSE AND t.expires_at IS NOT NULL AND t.expires_at <= NOW()")
    elif status == "all":
        pass
    else:
        return jsonify({"error": "status inválido (active/all/used/revoked/expired)"}), 400

    sql = f"""
      SELECT t.id, t.token, t.used, t.revoked, t.expires_at, t.created_at
      FROM token t
      WHERE {" AND ".join(where)}
      ORDER BY t.created_at DESC, t.id DESC
      LIMIT 500
    """

    def tx(conn, cur):
        cur.execute(sql, params)
        return {"rows": cur.fetchall(), "status": 200}

    result = execute_tx(tx)
    return jsonify(result["rows"]), 200


@admin_tokens_bp.post("/api/admin/tokens/revoke")
def revoke_token():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}
    tok = (payload.get("token") or "").strip().upper()
    if not tok:
        return jsonify({"error": "token es obligatorio"}), 400

    def tx(conn, cur):
       
        cur.execute(
            "SELECT id, used, revoked FROM token WHERE token=%s LIMIT 1 FOR UPDATE",
            [tok],
        )
        row = cur.fetchone()
        if not row:
            return {"error": "Token no existe", "status": 404}
        if row["used"]:
            return {"error": "No se puede revocar: token ya fue usado", "status": 409}
        if row["revoked"]:
            return {"message": "Token ya estaba revocado", "status": 200}

        cur.execute("UPDATE token SET revoked=TRUE WHERE id=%s", [row["id"]])
        return {"message": "Token revocado", "status": 200}

    result = execute_tx(tx)
    if result["status"] != 200:
        return jsonify({"error": result["error"]}), result["status"]
    return jsonify({"message": result["message"]}), 200