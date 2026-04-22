from flask import Blueprint, jsonify, request, session
from mysql.connector import Error
from ..database import fetch_all, fetch_one, execute_tx
from ..authz import require_role, ROLE_ADMIN
import hashlib
import secrets
from datetime import datetime, timedelta

admin_student_support_bp = Blueprint("admin_student_support", __name__)


def _get_current_admin_role(req):
    session_role = session.get("admin_user_role")
    if session_role == ROLE_ADMIN:
        return session_role

    legacy_role = require_role(req, {ROLE_ADMIN})
    if legacy_role:
        return legacy_role

    return None


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


def _gen_pass_token(length=40) -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijklmnopqrstuvwxyz"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _get_pass_ttl_minutes(cur) -> int:
    cur.execute("SELECT v FROM app_settings WHERE k='PASS_SESSION_TTL_MINUTES' LIMIT 1")
    row = cur.fetchone()
    try:
        return max(1, min(int(row["v"]), 5)) if row and row.get("v") else 2
    except:
        return 2


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


@admin_student_support_bp.get("/api/admin/student-support/search")
def search_student_support():
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    q = (request.args.get("q") or "").strip()
    event_id = request.args.get("event_id", type=int)

    if not q and not event_id:
        return jsonify({"error": "Debes enviar q o event_id"}), 400

    where = []
    params = []

    if event_id:
        where.append("ser.event_id = %s")
        params.append(event_id)

    if q:
        like = f"%{q}%"
        where.append("""
            (
                u.enrolment_number = %s
                OR ser.folio = %s
                OR CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) LIKE %s
                OR u.email LIKE %s
                OR u.secondary_email LIKE %s
            )
        """)
        params.extend([q.lower(), q.upper(), like, like, like])

    where_sql = " AND ".join(where) if where else "1=1"

    sql = f"""
        SELECT
            ser.id AS request_id,
            ser.folio,
            ser.status AS request_status,
            ser.requested_at,
            ser.validated_at,
            ser.access_enabled_at,
            ser.registered_at,
            ser.cancelled_at,
            ser.closed_at,
            ser.notes,

            ev.id AS event_id,
            ev.year,
            ev.season,
            ev.display_name,
            ev.status AS event_status,

            u.id AS user_id,
            u.first_name,
            u.second_name,
            u.p_last_name,
            u.m_last_name,
            CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS full_name,
            u.email,
            u.secondary_email,
            u.phone_number,
            u.enrolment_number,
            u.degree,
            u.semester,

            ps.id AS active_pass_session_id,
            ps.status AS active_pass_status,
            ps.issued_at AS active_pass_issued_at,
            ps.expires_at AS active_pass_expires_at,
            ps.used_at AS active_pass_used_at,
            ps.revoked_at AS active_pass_revoked_at,
            ps.refresh_count AS active_pass_refresh_count

        FROM student_event_requests ser
        JOIN users u ON u.id = ser.id_user
        JOIN events ev ON ev.id = ser.event_id
        LEFT JOIN pass_sessions ps
          ON ps.id = (
              SELECT ps2.id
              FROM pass_sessions ps2
              WHERE ps2.request_id = ser.id
              ORDER BY ps2.id DESC
              LIMIT 1
          )
        WHERE {where_sql}
        ORDER BY ser.id DESC
        LIMIT 100
    """

    rows = fetch_all(sql, params)
    return jsonify({"items": rows}), 200


@admin_student_support_bp.get("/api/admin/student-support/request/<int:request_id>")
def get_student_support_request(request_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    sql = """
        SELECT
            ser.id AS request_id,
            ser.folio,
            ser.status AS request_status,
            ser.requested_at,
            ser.validated_at,
            ser.access_enabled_at,
            ser.registered_at,
            ser.cancelled_at,
            ser.closed_at,
            ser.notes,

            ev.id AS event_id,
            ev.year,
            ev.season,
            ev.display_name,
            ev.status AS event_status,

            u.id AS user_id,
            u.first_name,
            u.second_name,
            u.p_last_name,
            u.m_last_name,
            CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS full_name,
            u.email,
            u.secondary_email,
            u.phone_number,
            u.enrolment_number,
            u.degree,
            u.semester
        FROM student_event_requests ser
        JOIN users u ON u.id = ser.id_user
        JOIN events ev ON ev.id = ser.event_id
        WHERE ser.id = %s
        LIMIT 1
    """

    row = fetch_one(sql, [request_id])
    if not row:
        return jsonify({"error": "Solicitud no encontrada"}), 404

    passes = fetch_all(
        """
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
        ORDER BY id DESC
        """,
        [request_id]
    )

    return jsonify({
        "request": row,
        "pass_sessions": passes
    }), 200


@admin_student_support_bp.patch("/api/admin/student-support/users/<int:user_id>")
def update_student_user(user_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}

    first_name = str(payload.get("first_name") or "").strip()
    second_name = str(payload.get("second_name") or "").strip() or None
    p_last_name = str(payload.get("p_last_name") or "").strip()
    m_last_name = str(payload.get("m_last_name") or "").strip()
    email = str(payload.get("email") or "").strip().lower()
    secondary_email = str(payload.get("secondary_email") or "").strip().lower() or None
    phone_number = str(payload.get("phone_number") or "").strip() or None
    enrolment_number = str(payload.get("enrolment_number") or "").strip().lower()
    degree = str(payload.get("degree") or "").strip() or None
    semester = payload.get("semester")

    if not first_name:
        return jsonify({"error": "first_name es obligatorio"}), 400
    if not p_last_name:
        return jsonify({"error": "p_last_name es obligatorio"}), 400
    if not m_last_name:
        return jsonify({"error": "m_last_name es obligatorio"}), 400
    if not email:
        return jsonify({"error": "email es obligatorio"}), 400
    if not enrolment_number:
        return jsonify({"error": "enrolment_number es obligatorio"}), 400

    try:
        semester = int(semester) if semester not in (None, "") else None
        if semester is not None and (semester < 1 or semester > 20):
            return jsonify({"error": "semester debe estar entre 1 y 20"}), 400
    except:
        return jsonify({"error": "semester debe ser numérico"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            SELECT id
            FROM users
            WHERE id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [user_id]
        )
        user_row = cur.fetchone()
        if not user_row:
            return {"error": "Alumno no encontrado", "status": 404}

        cur.execute(
            """
            SELECT id
            FROM users
            WHERE enrolment_number = %s
              AND id <> %s
            LIMIT 1
            FOR UPDATE
            """,
            [enrolment_number, user_id]
        )
        if cur.fetchone():
            return {"error": "Ya existe otro alumno con esa matrícula", "status": 409}

        cur.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
              AND id <> %s
            LIMIT 1
            FOR UPDATE
            """,
            [email, user_id]
        )
        if cur.fetchone():
            return {"error": "Ya existe otro alumno con ese correo", "status": 409}

        cur.execute(
            """
            UPDATE users
            SET
                first_name = %s,
                second_name = %s,
                p_last_name = %s,
                m_last_name = %s,
                email = %s,
                secondary_email = %s,
                phone_number = %s,
                enrolment_number = %s,
                degree = %s,
                semester = %s
            WHERE id = %s
            """,
            [
                first_name,
                second_name,
                p_last_name,
                m_last_name,
                email,
                secondary_email,
                phone_number,
                enrolment_number,
                degree,
                semester,
                user_id
            ]
        )

        cur.execute(
            """
            SELECT
                id,
                first_name,
                second_name,
                p_last_name,
                m_last_name,
                CONCAT_WS(' ', first_name, second_name, p_last_name, m_last_name) AS full_name,
                email,
                secondary_email,
                phone_number,
                enrolment_number,
                degree,
                semester
            FROM users
            WHERE id = %s
            LIMIT 1
            """,
            [user_id]
        )
        final_user = cur.fetchone()

        return {
            "status": 200,
            "message": "Alumno actualizado correctamente",
            "user": final_user
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


@admin_student_support_bp.post("/api/admin/student-support/request/<int:request_id>/reissue-pass")
def reissue_pass_for_request(request_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    def tx(conn, cur):
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
            WHERE ser.id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [request_id]
        )
        row = cur.fetchone()

        if not row:
            return {"error": "Solicitud no encontrada", "status": 404}

        if row["request_status"] in ("REGISTERED", "CANCELLED", "CLOSED"):
            return {
                "error": f"La solicitud ya no permite generar credencial ({row['request_status']})",
                "status": 409
            }

        if row["request_status"] not in ("REQUESTED", "VALIDATED", "ACCESS_ENABLED"):
            return {
                "error": f"Estado de solicitud no válido para generar pase ({row['request_status']})",
                "status": 409
            }

        _expire_old_sessions(cur, row["request_id"])
        _revoke_active_sessions(cur, row["request_id"])

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

        plain_token = _gen_pass_token(40)
        token_hash = _sha256(plain_token)
        ttl_minutes = _get_pass_ttl_minutes(cur)
        expires_at = datetime.now() + timedelta(minutes=ttl_minutes)

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
            "message": "Nuevo pase generado. El alumno debe volver a pasar validación presencial antes de inscribirse.",
            "request": {
                "id": row["request_id"],
                "folio": row["folio"],
                "status": row["request_status"],
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
            "event": {
                "id": row["event_id"],
                "year": row["year"],
                "season": row["season"],
                "display_name": row["display_name"],
            },
            "pass_session": {
                "id": session_id,
                "plain_token": plain_token,
                "expires_at": expires_at.isoformat(sep=" ", timespec="seconds"),
                "refresh_count": next_refresh_count,
                "ttl_minutes": ttl_minutes
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


@admin_student_support_bp.post("/api/admin/student-support/pass/<int:pass_session_id>/revoke")
def revoke_pass_session(pass_session_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    def tx(conn, cur):
        cur.execute(
            """
            SELECT id, request_id, status
            FROM pass_sessions
            WHERE id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [pass_session_id]
        )
        row = cur.fetchone()

        if not row:
            return {"error": "Pase no encontrado", "status": 404}

        if row["status"] in ("USED", "EXPIRED", "REVOKED"):
            return {"error": f"El pase ya no se puede revocar ({row['status']})", "status": 409}

        cur.execute(
            """
            UPDATE pass_sessions
            SET status = 'REVOKED',
                revoked_at = NOW()
            WHERE id = %s
            """,
            [pass_session_id]
        )

        return {
            "status": 200,
            "message": "Pase revocado correctamente"
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


@admin_student_support_bp.post("/api/admin/student-support/request/<int:request_id>/enable-access")
def enable_access_manually(request_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    def tx(conn, cur):
        cur.execute(
            """
            SELECT id, status
            FROM student_event_requests
            WHERE id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [request_id]
        )
        row = cur.fetchone()

        if not row:
            return {"error": "Solicitud no encontrada", "status": 404}

        if row["status"] in ("REGISTERED", "CANCELLED", "CLOSED"):
            return {"error": f"La solicitud ya no permite acceso ({row['status']})", "status": 409}

        cur.execute(
            """
            UPDATE student_event_requests
            SET status = 'ACCESS_ENABLED',
                validated_at = COALESCE(validated_at, NOW()),
                access_enabled_at = NOW(),
                notes = CONCAT(COALESCE(notes, ''), IF(COALESCE(notes, '') = '', '', ' | '), 'ACCESS_ENABLED manual por ADMIN')
            WHERE id = %s
            """,
            [request_id]
        )

        return {
            "status": 200,
            "message": "Acceso habilitado manualmente"
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