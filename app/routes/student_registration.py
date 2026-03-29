from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx, fetch_one
import unicodedata

student_registration_bp = Blueprint("student_registration", __name__)


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


def _normalize_text(value: str) -> str:
    value = (value or "").strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = " ".join(value.split())
    return value


@student_registration_bp.post("/api/student/registration/preview")
def preview_registration():
    payload = request.get_json(silent=True) or {}

    enrolment_number = (payload.get("enrolment_number") or "").strip().lower()
    season = _normalize_season(payload.get("season") or payload.get("temporada"))
    project_id = payload.get("project_id")
    token_value = (payload.get("token_value") or payload.get("token") or "").strip().upper()

    if not enrolment_number:
        return jsonify({"error": "Matrícula es obligatoria"}), 400
    if not season:
        return jsonify({"error": "Temporada inválida o faltante"}), 400
    if not project_id:
        return jsonify({"error": "project_id es obligatorio"}), 400
    if not token_value:
        return jsonify({"error": "token_value es obligatorio"}), 400

    try:
        project_id = int(project_id)
    except:
        return jsonify({"error": "project_id debe ser numérico"}), 400

    # 1) solicitud del alumno en esa temporada
    request_sql = """
        SELECT
            ser.id AS request_id,
            ser.status AS request_status,
            ev.id AS event_id,
            ev.year,
            ev.season,
            ev.display_name,
            u.id AS user_id,
            CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS full_name,
            u.enrolment_number
        FROM student_event_requests ser
        JOIN events ev ON ev.id = ser.event_id
        JOIN users u ON u.id = ser.id_user
        WHERE u.enrolment_number = %s
          AND ev.season = %s
        ORDER BY ev.year DESC, ser.id DESC
        LIMIT 1
    """
    req_row = fetch_one(request_sql, [enrolment_number, season])

    if not req_row:
        return jsonify({"error": "No existe solicitud para esa temporada"}), 404

    if req_row["request_status"] != "ACCESS_ENABLED":
        return jsonify({
            "error": f"La solicitud no está habilitada para registro ({req_row['request_status']})"
        }), 409

    # 2) proyecto dentro del evento/temporada
    event_project_sql = """
        SELECT
            ep.id AS event_project_id,
            ep.event_id,
            ep.project_id,
            ep.slots_total,
            ep.status AS event_project_status,
            p.name AS project_name
        FROM event_projects ep
        JOIN project p ON p.id = ep.project_id
        WHERE ep.event_id = %s
          AND ep.project_id = %s
        LIMIT 1
    """
    ep_row = fetch_one(event_project_sql, [req_row["event_id"], project_id])

    if not ep_row:
        return jsonify({"error": "El proyecto no pertenece a la temporada seleccionada"}), 404

    if ep_row["event_project_status"] != "ACTIVE":
        return jsonify({"error": "El proyecto no está disponible para registro"}), 409

    # 3) token
    token_sql = """
        SELECT
            pt.id,
            pt.token_value,
            pt.status,
            pt.expires_at,
            pt.event_project_id
        FROM project_tokens pt
        WHERE pt.token_value = %s
        LIMIT 1
    """
    tk_row = fetch_one(token_sql, [token_value])

    if not tk_row:
        return jsonify({"error": "Token no existe"}), 404

    if int(tk_row["event_project_id"]) != int(ep_row["event_project_id"]):
        return jsonify({"error": "El token no corresponde al proyecto"}), 409

    if tk_row["status"] != "AVAILABLE":
        return jsonify({"error": f"El token no está disponible ({tk_row['status']})"}), 409

    if tk_row["expires_at"] is not None:
        # dejamos que MySQL maneje esto luego en confirm también; aquí solo avisamos
        pass

    return jsonify({
        "message": "Preview válido",
        "student": {
            "user_id": req_row["user_id"],
            "full_name": req_row["full_name"],
            "enrolment_number": req_row["enrolment_number"],
        },
        "event": {
            "event_id": req_row["event_id"],
            "year": req_row["year"],
            "season": req_row["season"],
            "display_name": req_row["display_name"],
        },
        "project": {
            "event_project_id": ep_row["event_project_id"],
            "project_id": ep_row["project_id"],
            "project_name": ep_row["project_name"],
            "slots_total": ep_row["slots_total"],
        },
        "token": {
            "id": tk_row["id"],
            "token_value": tk_row["token_value"],
            "status": tk_row["status"],
            "expires_at": tk_row["expires_at"],
        }
    }), 200


@student_registration_bp.post("/api/student/registration/confirm")
def confirm_registration():
    payload = request.get_json(silent=True) or {}

    enrolment_number = (payload.get("enrolment_number") or "").strip().lower()
    season = _normalize_season(payload.get("season") or payload.get("temporada"))
    project_id = payload.get("project_id")
    token_value = (payload.get("token_value") or payload.get("token") or "").strip().upper()
    accepted_checkbox = payload.get("accepted_checkbox")
    accepted_full_name = (payload.get("accepted_full_name") or "").strip()

    if not enrolment_number:
        return jsonify({"error": "Matrícula es obligatoria"}), 400
    if not season:
        return jsonify({"error": "Temporada inválida o faltante"}), 400
    if not project_id:
        return jsonify({"error": "project_id es obligatorio"}), 400
    if not token_value:
        return jsonify({"error": "token_value es obligatorio"}), 400
    if accepted_checkbox is not True:
        return jsonify({"error": "Debes aceptar la confirmación legal"}), 400
    if not accepted_full_name:
        return jsonify({"error": "Debes escribir tu nombre completo"}), 400

    try:
        project_id = int(project_id)
    except:
        return jsonify({"error": "project_id debe ser numérico"}), 400

    def tx(conn, cur):
        # 1) solicitud del alumno
        cur.execute(
            """
            SELECT
                ser.id AS request_id,
                ser.status AS request_status,
                ser.event_id,
                ser.registered_at,
                u.id AS user_id,
                CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS full_name,
                u.enrolment_number
            FROM student_event_requests ser
            JOIN users u ON u.id = ser.id_user
            JOIN events ev ON ev.id = ser.event_id
            WHERE u.enrolment_number = %s
              AND ev.season = %s
            ORDER BY ev.year DESC, ser.id DESC
            LIMIT 1
            FOR UPDATE
            """,
            [enrolment_number, season]
        )
        req_row = cur.fetchone()

        if not req_row:
            return {"error": "No existe solicitud para esa temporada", "status": 404}

        if req_row["request_status"] != "ACCESS_ENABLED":
            return {
                "error": f"La solicitud no está habilitada para registro ({req_row['request_status']})",
                "status": 409
            }

        # 2) evitar doble registro en la misma temporada
        cur.execute(
            """
            SELECT id
            FROM registrations
            WHERE event_id = %s
              AND id_user = %s
              AND status = 'ACTIVE'
            LIMIT 1
            FOR UPDATE
            """,
            [req_row["event_id"], req_row["user_id"]]
        )
        if cur.fetchone():
            return {"error": "El alumno ya tiene un registro activo en esta temporada", "status": 409}

        # 3) proyecto en esa temporada
        cur.execute(
            """
            SELECT
                ep.id AS event_project_id,
                ep.project_id,
                ep.status AS event_project_status,
                p.name AS project_name
            FROM event_projects ep
            JOIN project p ON p.id = ep.project_id
            WHERE ep.event_id = %s
              AND ep.project_id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [req_row["event_id"], project_id]
        )
        ep_row = cur.fetchone()

        if not ep_row:
            return {"error": "El proyecto no pertenece a la temporada seleccionada", "status": 404}

        if ep_row["event_project_status"] != "ACTIVE":
            return {"error": "El proyecto no está disponible para registro", "status": 409}

        # 4) token del proyecto
        cur.execute(
            """
            SELECT
                pt.id,
                pt.token_value,
                pt.status,
                pt.expires_at,
                pt.event_project_id
            FROM project_tokens pt
            WHERE pt.token_value = %s
            LIMIT 1
            FOR UPDATE
            """,
            [token_value]
        )
        tk_row = cur.fetchone()

        if not tk_row:
            return {"error": "Token no existe", "status": 404}

        if int(tk_row["event_project_id"]) != int(ep_row["event_project_id"]):
            return {"error": "El token no corresponde al proyecto", "status": 409}

        if tk_row["status"] != "AVAILABLE":
            return {"error": f"El token no está disponible ({tk_row['status']})", "status": 409}

        if tk_row["expires_at"] is not None:
            cur.execute(
                """
                UPDATE project_tokens
                SET status = 'EXPIRED'
                WHERE id = %s
                  AND status = 'AVAILABLE'
                  AND expires_at <= NOW()
                """,
                [tk_row["id"]]
            )
            cur.execute(
                """
                SELECT status
                FROM project_tokens
                WHERE id = %s
                LIMIT 1
                """,
                [tk_row["id"]]
            )
            check_tk = cur.fetchone()
            if not check_tk or check_tk["status"] != "AVAILABLE":
                return {"error": "El token expiró", "status": 409}

        # 5) validar nombre razonablemente
        expected_name = _normalize_text(req_row["full_name"])
        provided_name = _normalize_text(accepted_full_name)

        if expected_name != provided_name:
            return {"error": "El nombre completo no coincide con el del alumno", "status": 409}

        # 6) crear registration
        cur.execute(
            """
            INSERT INTO registrations
            (
                event_id,
                event_project_id,
                id_user,
                request_id,
                project_token_id,
                accepted_checkbox,
                accepted_full_name,
                legal_text_version,
                accepted_at,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'v1', NOW(), 'ACTIVE')
            """,
            [
                req_row["event_id"],
                ep_row["event_project_id"],
                req_row["user_id"],
                req_row["request_id"],
                tk_row["id"],
                True,
                accepted_full_name,
            ]
        )
        registration_id = cur.lastrowid

        # 7) consumir token
        cur.execute(
            """
            UPDATE project_tokens
            SET status = 'USED',
                used_by_request_id = %s,
                used_at = NOW()
            WHERE id = %s
            """,
            [req_row["request_id"], tk_row["id"]]
        )

        # 8) cerrar solicitud como registrada
        cur.execute(
            """
            UPDATE student_event_requests
            SET status = 'REGISTERED',
                registered_at = NOW(),
                closed_at = NOW()
            WHERE id = %s
            """,
            [req_row["request_id"]]
        )

        return {
            "status": 201,
            "message": "Registro completado",
            "registration": {
                "id": registration_id,
                "event_id": req_row["event_id"],
                "event_project_id": ep_row["event_project_id"],
                "project_name": ep_row["project_name"],
                "token_value": tk_row["token_value"],
                "accepted_full_name": accepted_full_name,
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