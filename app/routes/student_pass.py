from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx, fetch_one
import hashlib
import secrets
from datetime import datetime, timedelta

student_pass_bp = Blueprint("student_pass", __name__)

PASS_TTL_MINUTES = 5


def _normalize_season(raw: str | None) -> str | None:
    if not raw:
        return None

    value = raw.strip().upper()
    mapping = {
        "PRIMAVERA": "PRIMAVERA",
        "SPRING": "PRIMAVERA",
        "INVIERNO": "INVIERNO",
        "WINTER": "INVIERNO",
    }
    return mapping.get(value)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _gen_pass_token(length=32) -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijklmnopqrstuvwxyz"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _expire_old_sessions(cur, request_id: int):
    cur.execute(
        """
        UPDATE pass_sessions
        SET status = 'EXPIRED'
        WHERE request_id = %s
          AND status = 'ACTIVE'
          AND expires_at <= NOW()
        """,
        [request_id]
    )


def _revoke_active_sessions(cur, request_id: int):
    cur.execute(
        """
        UPDATE pass_sessions
        SET status = 'REVOKED',
            revoked_at = NOW()
        WHERE request_id = %s
          AND status = 'ACTIVE'
        """,
        [request_id]
    )


@student_pass_bp.get("/api/student/pass")
def get_student_pass():
    enrolment_number = (request.args.get("enrolment_number") or "").strip().lower()
    season = _normalize_season(request.args.get("season") or request.args.get("temporada"))

    if not enrolment_number:
        return jsonify({"error": "Matrícula es obligatoria"}), 400

    if not season:
        return jsonify({"error": "Temporada inválida o faltante"}), 400

    sql = """
        SELECT
            ser.id AS request_id,
            ser.folio,
            ser.status AS request_status,
            ser.requested_at,
            ser.validated_at,
            ser.access_enabled_at,
            ser.registered_at,
            ev.id AS event_id,
            ev.year,
            ev.season,
            ev.display_name,
            ev.status AS event_status,
            u.id AS user_id,
            CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS full_name,
            u.email,
            u.secondary_email,
            u.phone_number,
            u.enrolment_number,
            u.degree,
            u.semester
        FROM student_event_requests ser
        JOIN events ev ON ev.id = ser.event_id
        JOIN users u ON u.id = ser.id_user
        WHERE u.enrolment_number = %s
          AND ev.season = %s
        ORDER BY ev.year DESC, ser.id DESC
        LIMIT 1
    """

    row = fetch_one(sql, [enrolment_number, season])

    if not row:
        return jsonify({"error": "No existe solicitud para esa temporada"}), 404

    active_sql = """
        SELECT
            id,
            status,
            issued_at,
            expires_at,
            used_at,
            revoked_at,
            refresh_count
        FROM pass_sessions
        WHERE request_id = %s
          AND status = 'ACTIVE'
          AND expires_at > NOW()
        ORDER BY id DESC
        LIMIT 1
    """
    active_session = fetch_one(active_sql, [row["request_id"]])

    return jsonify({
        "request": {
            "id": row["request_id"],
            "folio": row["folio"],
            "status": row["request_status"],
            "requested_at": row["requested_at"],
            "validated_at": row["validated_at"],
            "access_enabled_at": row["access_enabled_at"],
            "registered_at": row["registered_at"],
        },
        "event": {
            "id": row["event_id"],
            "year": row["year"],
            "season": row["season"],
            "display_name": row["display_name"],
            "status": row["event_status"],
        },
        "student": {
            "id": row["user_id"],
            "full_name": row["full_name"],
            "email": row["email"],
            "secondary_email": row["secondary_email"],
            "phone_number": row["phone_number"],
            "enrolment_number": row["enrolment_number"],
            "degree": row["degree"],
            "semester": row["semester"],
        },
        "active_session": active_session
    }), 200


@student_pass_bp.post("/api/student/pass/refresh")
def refresh_student_pass():
    payload = request.get_json(silent=True) or {}

    enrolment_number = (payload.get("enrolment_number") or "").strip().lower()
    season = _normalize_season(payload.get("season") or payload.get("temporada"))

    if not enrolment_number:
        return jsonify({"error": "Matrícula es obligatoria"}), 400

    if not season:
        return jsonify({"error": "Temporada inválida o faltante"}), 400

    def tx(conn, cur):
        # 1) encontrar solicitud
        cur.execute(
            """
            SELECT
                ser.id AS request_id,
                ser.folio,
                ser.status AS request_status,
                ev.id AS event_id,
                ev.year,
                ev.season,
                ev.display_name,
                ev.status AS event_status,
                u.id AS user_id,
                CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS full_name,
                u.email,
                u.secondary_email,
                u.phone_number,
                u.enrolment_number,
                u.degree,
                u.semester
            FROM student_event_requests ser
            JOIN events ev ON ev.id = ser.event_id
            JOIN users u ON u.id = ser.id_user
            WHERE u.enrolment_number = %s
              AND ev.season = %s
            ORDER BY ev.year DESC, ser.id DESC
            LIMIT 1
            FOR UPDATE
            """,
            [enrolment_number, season]
        )
        row = cur.fetchone()

        if not row:
            return {"error": "No existe solicitud para esa temporada", "status": 404}

        if row["request_status"] in ("CANCELLED", "CLOSED"):
            return {"error": "La solicitud no está disponible", "status": 409}

        # 2) expirar sesiones viejas
        _expire_old_sessions(cur, row["request_id"])

        # 3) buscar último refresh_count
        cur.execute(
            """
            SELECT refresh_count
            FROM pass_sessions
            WHERE request_id = %s
            ORDER BY id DESC
            LIMIT 1
            """,
            [row["request_id"]]
        )
        prev = cur.fetchone()
        next_refresh_count = int(prev["refresh_count"] or 0) + 1 if prev else 1

        # 4) revocar cualquier sesión activa aún viva
        _revoke_active_sessions(cur, row["request_id"])

        # 5) generar nuevo token
        plain_token = _gen_pass_token(40)
        token_hash = _sha256(plain_token)
        expires_at = datetime.now() + timedelta(minutes=PASS_TTL_MINUTES)

        cur.execute(
            """
            INSERT INTO pass_sessions
            (request_id, qr_token_hash, status, issued_at, expires_at, refresh_count)
            VALUES (%s, %s, 'ACTIVE', NOW(), %s, %s)
            """,
            [row["request_id"], token_hash, expires_at, next_refresh_count]
        )
        session_id = cur.lastrowid

        return {
            "status": 201,
            "message": "Credencial actualizada",
            "request": {
                "id": row["request_id"],
                "folio": row["folio"],
                "status": row["request_status"],
            },
            "event": {
                "id": row["event_id"],
                "year": row["year"],
                "season": row["season"],
                "display_name": row["display_name"],
                "status": row["event_status"],
            },
            "student": {
                "id": row["user_id"],
                "full_name": row["full_name"],
                "email": row["email"],
                "secondary_email": row["secondary_email"],
                "phone_number": row["phone_number"],
                "enrolment_number": row["enrolment_number"],
                "degree": row["degree"],
                "semester": row["semester"],
            },
            "pass_session": {
                "id": session_id,
                "plain_token": plain_token,
                "expires_at": expires_at.isoformat(sep=" ", timespec="seconds"),
                "refresh_count": next_refresh_count,
                "ttl_minutes": PASS_TTL_MINUTES
            }
        }

    try:
        result = execute_tx(tx)

        if result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify(result), 201

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500