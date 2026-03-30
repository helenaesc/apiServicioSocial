from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx
from ..authz import require_role, ROLE_ADMIN
import secrets

admin_project_tokens_bp = Blueprint("admin_project_tokens", __name__)

VALID_STATUSES = {"AVAILABLE", "USED", "REVOKED", "EXPIRED", "RESERVED"}


def _gen_token(length=10):
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _get_ttl_hours(cur) -> int:
    cur.execute("SELECT v FROM app_settings WHERE k='TOKEN_TTL_HOURS' LIMIT 1")
    row = cur.fetchone()
    try:
        return max(1, min(int(row["v"]), 168)) if row and row.get("v") else 24
    except:
        return 24


@admin_project_tokens_bp.post("/api/admin/event-projects/<int:event_project_id>/tokens")
def generate_project_tokens(event_project_id: int):
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
        # bloquear proyecto de temporada
        cur.execute(
            """
            SELECT id, slots_total, status
            FROM event_projects
            WHERE id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [event_project_id]
        )
        ep = cur.fetchone()

        if not ep:
            return {"error": "Proyecto en temporada no encontrado", "status": 404}

        if ep["status"] != "ACTIVE":
            return {"error": "El proyecto en temporada no está activo", "status": 409}

        slots_total = int(ep.get("slots_total") or 0)
        if slots_total <= 0:
            return {"error": "El proyecto en temporada tiene slots_total=0", "status": 409}

        ttl_hours = _get_ttl_hours(cur)

        # expirar disponibles vencidos
        cur.execute(
            """
            UPDATE project_tokens
            SET status = 'EXPIRED'
            WHERE event_project_id = %s
              AND status = 'AVAILABLE'
              AND expires_at IS NOT NULL
              AND expires_at <= NOW()
            """,
            [event_project_id]
        )

        # contar usados
        cur.execute(
            """
            SELECT COUNT(*) AS c
            FROM project_tokens
            WHERE event_project_id = %s
              AND status = 'USED'
            """,
            [event_project_id]
        )
        used_count = int(cur.fetchone()["c"])

        # contar abiertos (AVAILABLE + RESERVED)
        cur.execute(
            """
            SELECT COUNT(*) AS c
            FROM project_tokens
            WHERE event_project_id = %s
              AND status IN ('AVAILABLE', 'RESERVED')
            """,
            [event_project_id]
        )
        open_count = int(cur.fetchone()["c"])

        remaining = max(slots_total - (used_count + open_count), 0)

        if remaining <= 0:
            return {
                "error": "No puedes crear más tokens: ya alcanzaste el cupo total disponible.",
                "status": 409
            }

        if count > remaining:
            return {
                "error": f"Solo puedes crear {remaining} tokens más (slots_total={slots_total}, usados={used_count}, abiertos={open_count}).",
                "status": 409
            }

        tokens_created = []
        attempts = 0
        max_attempts = count * 15

        while len(tokens_created) < count and attempts < max_attempts:
            attempts += 1
            tok = _gen_token(length)

            try:
                cur.execute(
                    """
                    INSERT INTO project_tokens
                    (event_project_id, token_value, status, expires_at)
                    VALUES (
                        %s,
                        %s,
                        'AVAILABLE',
                        DATE_ADD(NOW(), INTERVAL %s HOUR)
                    )
                    """,
                    [event_project_id, tok, ttl_hours]
                )
                tokens_created.append(tok)
            except Exception:
                continue

        if len(tokens_created) < count:
            return {
                "error": f"Solo se pudieron crear {len(tokens_created)} tokens",
                "status": 500
            }

        return {
            "status": 201,
            "message": "Tokens generados",
            "created": len(tokens_created),
            "ttl_hours": ttl_hours,
            "tokens": tokens_created
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


@admin_project_tokens_bp.get("/api/admin/event-projects/<int:event_project_id>/tokens")
def list_project_tokens(event_project_id: int):
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    status = (request.args.get("status") or "AVAILABLE").strip().upper()

    if status not in VALID_STATUSES and status != "ALL":
        return jsonify({"error": "status inválido (AVAILABLE/USED/REVOKED/EXPIRED/RESERVED/ALL)"}), 400

    def tx(conn, cur):
        # expirar primero
        cur.execute(
            """
            UPDATE project_tokens
            SET status = 'EXPIRED'
            WHERE event_project_id = %s
              AND status = 'AVAILABLE'
              AND expires_at IS NOT NULL
              AND expires_at <= NOW()
            """,
            [event_project_id]
        )

        where = ["pt.event_project_id = %s"]
        params = [event_project_id]

        if status != "ALL":
            where.append("pt.status = %s")
            params.append(status)

        sql = f"""
            SELECT
                pt.id,
                pt.token_value,
                pt.status,
                pt.reserved_by_request_id,
                pt.reserved_at,
                pt.reserved_until,
                pt.used_by_request_id,
                pt.used_at,
                pt.revoked_at,
                pt.revoke_reason,
                pt.expires_at,
                pt.created_at
            FROM project_tokens pt
            WHERE {' AND '.join(where)}
            ORDER BY pt.created_at DESC, pt.id DESC
            LIMIT 500
        """
        cur.execute(sql, params)
        rows = cur.fetchall()

        cur.execute(
            """
            SELECT
                SUM(CASE WHEN status = 'AVAILABLE' THEN 1 ELSE 0 END) AS available_count,
                SUM(CASE WHEN status = 'RESERVED' THEN 1 ELSE 0 END) AS reserved_count,
                SUM(CASE WHEN status = 'USED' THEN 1 ELSE 0 END) AS used_count,
                SUM(CASE WHEN status = 'REVOKED' THEN 1 ELSE 0 END) AS revoked_count,
                SUM(CASE WHEN status = 'EXPIRED' THEN 1 ELSE 0 END) AS expired_count,
                COUNT(*) AS total_count
            FROM project_tokens
            WHERE event_project_id = %s
            """,
            [event_project_id]
        )
        summary = cur.fetchone()

        return {
            "status": 200,
            "summary": {
                "available": int(summary.get("available_count") or 0),
                "reserved": int(summary.get("reserved_count") or 0),
                "used": int(summary.get("used_count") or 0),
                "revoked": int(summary.get("revoked_count") or 0),
                "expired": int(summary.get("expired_count") or 0),
                "total": int(summary.get("total_count") or 0),
            },
            "items": rows
        }

    try:
        result = execute_tx(tx)
        return jsonify({
            "summary": result["summary"],
            "items": result["items"]
        }), 200
    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_project_tokens_bp.post("/api/admin/project-tokens/revoke")
def revoke_project_token():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}
    tok = (payload.get("token") or "").strip().upper()
    reason = (payload.get("reason") or "").strip() or None

    if not tok:
        return jsonify({"error": "token es obligatorio"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            UPDATE project_tokens
            SET status = 'EXPIRED'
            WHERE token_value = %s
              AND status = 'AVAILABLE'
              AND expires_at IS NOT NULL
              AND expires_at <= NOW()
            """,
            [tok]
        )

        cur.execute(
            """
            SELECT id, status
            FROM project_tokens
            WHERE token_value = %s
            LIMIT 1
            FOR UPDATE
            """,
            [tok]
        )
        row = cur.fetchone()

        if not row:
            return {"error": "Token no existe", "status": 404}

        if row["status"] == "USED":
            return {"error": "No se puede revocar: token ya fue usado", "status": 409}

        if row["status"] == "REVOKED":
            return {"message": "Token ya estaba revocado", "status": 200}

        if row["status"] == "EXPIRED":
            return {"message": "Token ya estaba expirado", "status": 200}

        cur.execute(
            """
            UPDATE project_tokens
            SET status = 'REVOKED',
                revoked_at = NOW(),
                revoke_reason = %s
            WHERE id = %s
            """,
            [reason, row["id"]]
        )

        return {"message": "Token revocado", "status": 200}

    try:
        result = execute_tx(tx)

        if result["status"] != 200:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({"message": result["message"]}), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500