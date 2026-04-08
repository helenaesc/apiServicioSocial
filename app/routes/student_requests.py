from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx, fetch_one
import secrets
import hashlib

student_requests_bp = Blueprint("student_requests", __name__)


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


def _build_folio() -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    middle = "".join(secrets.choice(alphabet) for _ in range(6))
    return f"FI-{middle}"


def _make_temp_salt(length: int = 10) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _make_temp_password_hash() -> tuple[str, str]:
    temp_plain = secrets.token_urlsafe(16)
    salt = _make_temp_salt(10)
    password_hash = hashlib.sha256((temp_plain + salt).encode("utf-8")).hexdigest()
    return password_hash, salt


def _split_full_name(full_name: str):
    """
    Separación básica:
    - primera palabra -> first_name
    - segunda palabra opcional -> second_name
    - resto intenta dividirse en apellidos
    """
    parts = [p for p in full_name.strip().split() if p]

    if len(parts) == 1:
        return parts[0], None, "X", "X"

    if len(parts) == 2:
        return parts[0], None, parts[1], "X"

    if len(parts) == 3:
        return parts[0], None, parts[1], parts[2]

    first_name = parts[0]
    second_name = parts[1]
    p_last_name = parts[2]
    m_last_name = " ".join(parts[3:])
    return first_name, second_name, p_last_name, m_last_name


def _get_visible_event_by_season(cur, season: str):
    cur.execute(
        """
        SELECT id, year, season, display_name, status
        FROM events
        WHERE season = %s
          AND is_visible_to_students = TRUE
          AND status IN ('VISIBLE', 'ONSITE')
        ORDER BY year DESC, id DESC
        LIMIT 1
        """,
        [season]
    )
    return cur.fetchone()

@student_requests_bp.get("/api/student/requests")
def get_student_request():
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

    return jsonify({
        "message": "Solicitud encontrada",
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
        "request": {
            "id": row["request_id"],
            "folio": row["folio"],
            "status": row["request_status"],
            "requested_at": row["requested_at"],
            "validated_at": row["validated_at"],
            "access_enabled_at": row["access_enabled_at"],
            "registered_at": row["registered_at"],
        }
    }), 200