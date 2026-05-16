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

def _normalize_name(value: str) -> str:
    return " ".join(str(value or "").strip().lower().split())


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


def _get_visible_event_by_season_read(season: str):
    return fetch_one(
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


def _select_request_by_id(cur, request_id: int):
    cur.execute(
        """
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
        WHERE ser.id = %s
        LIMIT 1
        """,
        [request_id]
    )
    return cur.fetchone()


def _format_request_response(row: dict, message: str, status: int):
    return {
        "status": status,
        "message": message,
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
    }


@student_requests_bp.post("/api/student/requests")
def create_student_request():
    payload = request.get_json(silent=True) or {}

    full_name = str(payload.get("full_name") or "").strip()
    enrolment_number = str(payload.get("enrolment_number") or "").strip().lower()
    secondary_email = str(
        payload.get("second_email") or payload.get("secondary_email") or ""
    ).strip().lower() or None
    phone_number = str(payload.get("phone_number") or "").strip()
    degree = str(payload.get("degree") or "").strip()
    semester_raw = payload.get("semester")
    season = _normalize_season(payload.get("season") or payload.get("temporada"))

    email = f"{enrolment_number}@tec.mx"

    if not full_name:
        return jsonify({"error": "full_name es obligatorio"}), 400

    if len(full_name) > 100:
        return jsonify({"error": "full_name no puede superar 100 caracteres"}), 400

    if len(enrolment_number) != 9 or not enrolment_number.isalnum():
        return jsonify({"error": "enrolment_number debe tener exactamente 9 caracteres alfanuméricos"}), 400

    phone_number = "".join(ch for ch in phone_number if ch.isdigit())
    if len(phone_number) != 10:
        return jsonify({"error": "phone_number debe tener exactamente 10 dígitos"}), 400

    if not degree:
        return jsonify({"error": "degree es obligatorio"}), 400

    if not season:
        return jsonify({"error": "Temporada inválida o faltante"}), 400

    try:
        semester = int(semester_raw)
        if semester < 1 or semester > 20:
            return jsonify({"error": "semester debe estar entre 1 y 20"}), 400
    except:
        return jsonify({"error": "semester debe ser numérico"}), 400

    first_name, second_name, p_last_name, m_last_name = _split_full_name(full_name)

    def tx(conn, cur):
        event_row = _get_visible_event_by_season(cur, season)
        if not event_row:
            return {
                "error": "No hay temporada visible para alumnos en esa temporada",
                "status": 404
            }

        event_id = event_row["id"]

        cur.execute(
            """
            SELECT
                id,
                enrolment_number,
                first_name,
                second_name,
                p_last_name,
                m_last_name
            FROM users
            WHERE enrolment_number = %s
            LIMIT 1
            FOR UPDATE
            """,
            [enrolment_number]
        )
        user_row = cur.fetchone()

        if user_row:
            user_id = user_row["id"]

            existing_full_name = _normalize_name(
                " ".join([
                    user_row.get("first_name") or "",
                    user_row.get("second_name") or "",
                    user_row.get("p_last_name") or "",
                    user_row.get("m_last_name") or "",
                ])
            )

            incoming_full_name = _normalize_name(full_name)

            if existing_full_name != incoming_full_name:
                return {
                    "error": (
                        "La matrícula ya está asociada a otro nombre registrado. "
                        "Si hay un error, solicita corrección con administración."
                    ),
                    "status": 409
                }

            cur.execute(
                """
                SELECT
                    ser.id AS request_id,
                    ser.folio,
                    ser.status AS request_status
                FROM student_event_requests ser
                WHERE ser.id_user = %s
                  AND ser.event_id = %s
                LIMIT 1
                FOR UPDATE
                """,
                [user_id, event_id]
            )
            existing_request = cur.fetchone()

            if existing_request:
                row = _select_request_by_id(cur, existing_request["request_id"])
                return _format_request_response(
                    row,
                    "Ya existía una solicitud para esta temporada. No se modificaron los datos del alumno.",
                    200
                )

            # Si la matrícula existe pero no tiene solicitud en este evento,
            # permitimos crear solicitud nueva para la temporada actual.
            # No actualizamos nombre/correo/teléfono desde alumno para evitar suplantación accidental.
            # Si los datos están mal, se corrigen desde Admin.
            cur.execute(
                """
                SELECT
                    id,
                    CONCAT_WS(' ', first_name, second_name, p_last_name, m_last_name) AS full_name
                FROM users
                WHERE id = %s
                LIMIT 1
                """,
                [user_id]
            )
            current_user = cur.fetchone()

        else:
            password_hash, salt = _make_temp_password_hash()

            cur.execute(
                """
                INSERT INTO users
                (
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
                    password,
                    salt
                )
                VALUES
                (
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
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
                    password_hash,
                    salt
                ]
            )
            user_id = cur.lastrowid

        folio = None
        for _ in range(8):
            candidate = _build_folio()
            cur.execute(
                """
                SELECT id
                FROM student_event_requests
                WHERE folio = %s
                LIMIT 1
                """,
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
            (
                id_user,
                event_id,
                folio,
                status,
                requested_at
            )
            VALUES
            (
                %s, %s, %s, 'REQUESTED', NOW()
            )
            """,
            [user_id, event_id, folio]
        )
        request_id = cur.lastrowid

        row = _select_request_by_id(cur, request_id)

        return _format_request_response(
            row,
            "Solicitud creada correctamente",
            201
        )

    try:
        result = execute_tx(tx)

        if result.get("status") not in (200, 201):
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify(result), result["status"]

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

    event_row = _get_visible_event_by_season_read(season)
    if not event_row:
        return jsonify({"error": "No hay temporada visible para alumnos en esa temporada"}), 404

    event_id = event_row["id"]

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
          AND ser.event_id = %s
        LIMIT 1
    """

    row = fetch_one(sql, [enrolment_number, event_id])

    if not row:
        return jsonify({"error": "No existe solicitud para esta temporada visible"}), 404

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