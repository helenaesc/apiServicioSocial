from flask import Blueprint, jsonify, request, session
from mysql.connector import Error
from ..database import execute_tx
from ..authz import require_role, ROLE_ADMIN, ROLE_STAFF
import hashlib

staff_checkin_bp = Blueprint("staff_checkin", __name__)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _get_current_role(req):
    """
    Prioridad:
    1) sesión real
    2) compatibilidad temporal con X-ADMIN-KEY
    """
    session_role = session.get("admin_user_role")
    if session_role in {ROLE_ADMIN, ROLE_STAFF}:
        return session_role

    legacy_role = require_role(req, {ROLE_ADMIN, ROLE_STAFF})
    if legacy_role:
        return legacy_role

    return None


@staff_checkin_bp.post("/api/staff/checkin/scan")
def scan_pass():
    role = _get_current_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401

    payload = request.get_json(silent=True) or {}
    plain_token = (payload.get("token") or "").strip()

    if not plain_token:
        return jsonify({"error": "token es obligatorio"}), 400

    token_hash = _sha256(plain_token)

    def tx(conn, cur):
        # Buscar sesión activa
        cur.execute(
            """
            SELECT
                ps.id AS pass_session_id,
                ps.request_id,
                ps.status AS pass_status,
                ps.issued_at,
                ps.expires_at,
                ps.used_at,
                ps.revoked_at,
                ps.refresh_count,
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
            FROM pass_sessions ps
            JOIN student_event_requests ser ON ser.id = ps.request_id
            JOIN events ev ON ev.id = ser.event_id
            JOIN users u ON u.id = ser.id_user
            WHERE ps.qr_token_hash = %s
            LIMIT 1
            FOR UPDATE
            """,
            [token_hash]
        )
        row = cur.fetchone()

        if not row:
            return {"error": "QR no reconocido", "status": 404}

        if row["pass_status"] != "ACTIVE":
            return {"error": f"QR no disponible ({row['pass_status']})", "status": 409}

        # Expiración dura
        cur.execute(
            """
            UPDATE pass_sessions
            SET status = 'EXPIRED'
            WHERE id = %s
              AND status = 'ACTIVE'
              AND expires_at <= NOW()
            """,
            [row["pass_session_id"]]
        )

        cur.execute(
            """
            SELECT status
            FROM pass_sessions
            WHERE id = %s
            LIMIT 1
            """,
            [row["pass_session_id"]]
        )
        current = cur.fetchone()

        if not current or current["status"] != "ACTIVE":
            return {"error": "QR expirado, solicita refresh al alumno", "status": 409}

        return {
            "status": 200,
            "pass_session": {
                "id": row["pass_session_id"],
                "request_id": row["request_id"],
                "status": current["status"],
                "issued_at": row["issued_at"],
                "expires_at": row["expires_at"],
                "refresh_count": row["refresh_count"],
            },
            "request": {
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
            }
        }

    try:
        result = execute_tx(tx)

        if result.get("status") != 200:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify(result), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@staff_checkin_bp.post("/api/staff/checkin/grant-access")
def grant_access():
    role = _get_current_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401

    payload = request.get_json(silent=True) or {}
    pass_session_id = payload.get("pass_session_id")
    enrolment_number = (payload.get("enrolment_number") or "").strip().lower()

    if not pass_session_id:
        return jsonify({"error": "pass_session_id es obligatorio"}), 400

    if not enrolment_number:
        return jsonify({"error": "Matrícula física es obligatoria"}), 400

    def tx(conn, cur):
        # Bloquear sesión
        cur.execute(
            """
            SELECT
                ps.id,
                ps.request_id,
                ps.status,
                ps.expires_at,
                ser.id_user,
                ser.status AS request_status,
                u.enrolment_number
            FROM pass_sessions ps
            JOIN student_event_requests ser ON ser.id = ps.request_id
            JOIN users u ON u.id = ser.id_user
            WHERE ps.id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [pass_session_id]
        )
        row = cur.fetchone()

        if not row:
            return {"error": "Sesión no encontrada", "status": 404}

        if row["status"] != "ACTIVE":
            return {"error": f"La sesión ya no está activa ({row['status']})", "status": 409}

        # Expiración
        cur.execute(
            """
            UPDATE pass_sessions
            SET status = 'EXPIRED'
            WHERE id = %s
              AND status = 'ACTIVE'
              AND expires_at <= NOW()
            """,
            [pass_session_id]
        )

        cur.execute(
            "SELECT status FROM pass_sessions WHERE id = %s LIMIT 1",
            [pass_session_id]
        )
        status_row = cur.fetchone()
        if not status_row or status_row["status"] != "ACTIVE":
            return {"error": "La sesión expiró, solicita refresh al alumno", "status": 409}

        # Comparar matrícula física
        expected = (row["enrolment_number"] or "").strip().lower()
        if expected != enrolment_number:
            return {"error": "La matrícula no coincide con la credencial", "status": 409}

        # No permitir si ya cerró o quedó cancelado
        if row["request_status"] in ("REGISTERED", "CANCELLED", "CLOSED"):
            return {"error": f"La solicitud ya no permite acceso ({row['request_status']})", "status": 409}


# Marcar QR como usado
        cur.execute(
            """
            UPDATE pass_sessions
            SET status = 'USED',
                used_at = NOW()
            WHERE id = %s
            """,
            [pass_session_id]
        )

        # Habilitar acceso en la solicitud
        cur.execute(
            """
            UPDATE student_event_requests
            SET status = 'ACCESS_ENABLED',
                validated_at = COALESCE(validated_at, NOW()),
                access_enabled_at = NOW()
            WHERE id = %s
            """,
            [row["request_id"]]
        )

        # Traer contexto completo actualizado
        cur.execute(
            """
            SELECT
                ps.id AS pass_session_id,
                ps.request_id,
                ps.status AS pass_status,
                ps.issued_at,
                ps.expires_at,
                ps.used_at,
                ps.revoked_at,
                ps.refresh_count,
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
            FROM pass_sessions ps
            JOIN student_event_requests ser ON ser.id = ps.request_id
            JOIN events ev ON ev.id = ser.event_id
            JOIN users u ON u.id = ser.id_user
            WHERE ps.id = %s
            LIMIT 1
            """,
            [pass_session_id]
        )
        final_row = cur.fetchone()

        return {
            "status": 200,
            "message": "Acceso habilitado",
            "performed_by": {
                "role": role
            },
            "pass_session": {
                "id": final_row["pass_session_id"],
                "request_id": final_row["request_id"],
                "status": final_row["pass_status"],
                "issued_at": final_row["issued_at"],
                "expires_at": final_row["expires_at"],
                "used_at": final_row["used_at"],
                "revoked_at": final_row["revoked_at"],
                "refresh_count": final_row["refresh_count"],
            },
            "request": {
                "folio": final_row["folio"],
                "status": final_row["request_status"],
                "requested_at": final_row["requested_at"],
                "validated_at": final_row["validated_at"],
                "access_enabled_at": final_row["access_enabled_at"],
                "registered_at": final_row["registered_at"],
            },
            "event": {
                "id": final_row["event_id"],
                "year": final_row["year"],
                "season": final_row["season"],
                "display_name": final_row["display_name"],
                "status": final_row["event_status"],
            },
            "student": {
                "id": final_row["user_id"],
                "full_name": final_row["full_name"],
                "email": final_row["email"],
                "secondary_email": final_row["secondary_email"],
                "phone_number": final_row["phone_number"],
                "enrolment_number": final_row["enrolment_number"],
                "degree": final_row["degree"],
                "semester": final_row["semester"],
            }
        }