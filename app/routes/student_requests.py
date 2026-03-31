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


@student_requests_bp.post("/api/student/requests")
def create_student_request():
    payload = request.get_json(silent=True) or {}

    full_name = (payload.get("full_name") or "").strip()
    enrolment_number = (payload.get("enrolment_number") or "").strip().lower()
    email = (payload.get("email") or "").strip().lower()
    second_email = (payload.get("second_email") or "").strip().lower() or None
    phone_number = (payload.get("phone_number") or "").strip() or None
    degree = (payload.get("degree") or "").strip() or None
    semester = payload.get("semester")
    season = _normalize_season(payload.get("season") or payload.get("temporada"))

    if not full_name:
        return jsonify({"error": "Nombre completo es obligatorio"}), 400
    if not enrolment_number:
        return jsonify({"error": "Matrícula es obligatoria"}), 400
    if not email:
        return jsonify({"error": "Correo principal es obligatorio"}), 400
    if not season:
        return jsonify({"error": "Temporada inválida o faltante"}), 400

    if len(enrolment_number) > 10:
        return jsonify({"error": "La matrícula no puede exceder 10 caracteres"}), 400

    if semester not in (None, ""):
        try:
            semester = int(semester)
            if semester < 1 or semester > 20:
                return jsonify({"error": "semester debe estar entre 1 y 20"}), 400
        except:
            return jsonify({"error": "semester debe ser numérico"}), 400
    else:
        semester = None

    if second_email and second_email == email:
        second_email = None

    first_name, second_name, p_last_name, m_last_name = _split_full_name(full_name)

    def tx(conn, cur):
        event_row = _get_visible_event_by_season(cur, season)
        if not event_row:
            return {"error": "No hay temporada visible para estudiantes", "status": 404}

        event_id = event_row["id"]

        cur.execute(
            """
            SELECT id, first_name, second_name, p_last_name, m_last_name,
                   email, secondary_email, enrolment_number, phone_number, degree, semester
            FROM users
            WHERE enrolment_number = %s
            LIMIT 1
            FOR UPDATE
            """,
            [enrolment_number]
        )
        user = cur.fetchone()

        if user:
            cur.execute(
                """
                SELECT id
                FROM users
                WHERE email = %s
                  AND id <> %s
                LIMIT 1
                """,
                [email, user["id"]]
            )
            email_conflict = cur.fetchone()
            if email_conflict:
                return {
                    "error": "Ese correo ya está ligado a otro alumno. Solicita apoyo a ADMIN.",
                    "status": 409
                }

            cur.execute(
                """
                UPDATE users
                SET first_name = %s,
                    second_name = %s,
                    p_last_name = %s,
                    m_last_name = %s,
                    email = %s,
                    secondary_email = %s,
                    phone_number = %s,
                    degree = %s,
                    semester = %s
                WHERE id = %s
                """,
                [
                    first_name, second_name, p_last_name, m_last_name,
                    email, second_email, phone_number, degree, semester, user["id"]
                ]
            )
            user_id = user["id"]
        else:
            cur.execute(
                "SELECT id FROM users WHERE email = %s LIMIT 1",
                [email]
            )
            email_row = cur.fetchone()
            if email_row:
                return {
                    "error": "Ese correo ya está ligado a otro alumno. Solicita apoyo a ADMIN.",
                    "status": 409
                }

            password_hash, salt = _make_temp_password_hash()

            cur.execute(
                """
                INSERT INTO users
                (
                    first_name, second_name, p_last_name, m_last_name,
                    email, secondary_email, enrolment_number, phone_number,
                    password, salt, admin, degree, semester
                )
                VALUES (%s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, FALSE, %s, %s)
                """,
                [
                    first_name, second_name, p_last_name, m_last_name,
                    email, second_email, enrolment_number, phone_number,
                    password_hash, salt, degree, semester
                ]
            )
            user_id = cur.lastrowid

        cur.execute(
            """
            SELECT id, folio, status, requested_at, validated_at, access_enabled_at, registered_at
            FROM student_event_requests
            WHERE event_id = %s
              AND id_user = %s
            LIMIT 1
            FOR UPDATE
            """,
            [event_id, user_id]
        )
        existing = cur.fetchone()

        if existing:
            return {
                "status": 200,
                "already_exists": True,
                "message": "Ya existe una solicitud para esta temporada",
                "request": {
                    "id": existing["id"],
                    "folio": existing["folio"],
                    "status": existing["status"],
                    "requested_at": existing["requested_at"],
                    "validated_at": existing["validated_at"],
                    "access_enabled_at": existing["access_enabled_at"],
                    "registered_at": existing["registered_at"],
                },
                "event": {
                    "id": event_row["id"],
                    "year": event_row["year"],
                    "season": event_row["season"],
                    "display_name": event_row["display_name"],
                    "status": event_row["status"],
                },
                "user": {
                    "id": user_id,
                    "full_name": full_name,
                    "email": email,
                    "second_email": second_email,
                    "phone_number": phone_number,
                    "enrolment_number": enrolment_number,
                    "degree": degree,
                    "semester": semester
                }
            }

        folio = None
        for _ in range(20):
            candidate = _build_folio()
            cur.execute(
                "SELECT id FROM student_event_requests WHERE folio = %s LIMIT 1",
                [candidate]
            )
            if not cur.fetchone():
                folio = candidate
                break

        if not folio:
            return {"error": "No se pudo generar un folio único", "status": 500}

        cur.execute(
            """
            INSERT INTO student_event_requests
            (event_id, id_user, folio, status, requested_at)
            VALUES (%s, %s, %s, 'REQUESTED', NOW())
            """,
            [event_id, user_id, folio]
        )

        request_id = cur.lastrowid

        return {
            "status": 201,
            "already_exists": False,
            "message": "Solicitud de pase creada",
            "request": {
                "id": request_id,
                "folio": folio,
                "status": "REQUESTED",
            },
            "event": {
                "id": event_row["id"],
                "year": event_row["year"],
                "season": event_row["season"],
                "display_name": event_row["display_name"],
                "status": event_row["status"],
            },
            "user": {
                "id": user_id,
                "full_name": full_name,
                "email": email,
                "second_email": second_email,
                "phone_number": phone_number,
                "enrolment_number": enrolment_number,
                "degree": degree,
                "semester": semester
            }
        }

    try:
        result = execute_tx(tx)

        if result.get("status") == 201:
            return jsonify(result), 201

        if result.get("status") == 200:
            return jsonify(result), 200

        return jsonify({"error": result["error"]}), result["status"]

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
            ser.id,
            ser.folio,
            ser.status,
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
            u.first_name,
            u.second_name,
            u.p_last_name,
            u.m_last_name,
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

    return jsonify(row), 200