from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx, fetch_one
import unicodedata
import hashlib
import json
import hmac
import os

student_registration_bp = Blueprint("student_registration", __name__)


def _sign_snapshot(snapshot_json: str) -> str:
    secret = os.getenv("APP_SIGNATURE_SECRET", "").strip()
    if not secret:
        raise RuntimeError("APP_SIGNATURE_SECRET no está configurado")
    return hmac.new(
        secret.encode("utf-8"),
        snapshot_json.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


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


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _build_acceptance_snapshot(
    req_row: dict,
    ep_row: dict,
    token_row: dict,
    accepted_full_name: str,
    legal_text_version: str,
) -> dict:
    return {
        "event_id": req_row["event_id"],
        "request_id": req_row["request_id"],
        "user_id": req_row["user_id"],
        "enrolment_number": req_row["enrolment_number"],
        "student_full_name_system": req_row["full_name"],
        "accepted_full_name": accepted_full_name,
        "event_project_id": ep_row["event_project_id"],
        "project_id": ep_row["project_id"],
        "project_name": ep_row["project_name"],
        "general_name": ep_row["general_name"],
        "partner_name": ep_row["partner_name"],
        "token_id": token_row["id"],
        "token_value": token_row["token_value"],
        "legal_text_version": legal_text_version,
    }


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

    event_project_sql = """
        SELECT
            ep.id AS event_project_id,
            ep.event_id,
            ep.project_id,
            ep.slots_total,
            ep.status AS event_project_status,
            p.name AS project_name,
            p.general_name,
            pa.name AS partner_name
        FROM event_projects ep
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN partner pa ON pa.id = p.id_partner
        WHERE ep.event_id = %s
          AND ep.project_id = %s
        LIMIT 1
    """
    ep_row = fetch_one(event_project_sql, [req_row["event_id"], project_id])

    if not ep_row:
        return jsonify({"error": "El proyecto no pertenece a la temporada seleccionada"}), 404

    if ep_row["event_project_status"] != "ACTIVE":
        return jsonify({"error": "El proyecto no está disponible para registro"}), 409

    token_sql = """
        SELECT
            pt.id,
            pt.token_value,
            pt.status,
            pt.expires_at,
            pt.event_project_id,
            pt.reserved_by_request_id,
            pt.reserved_until
        FROM project_tokens pt
        WHERE pt.token_value = %s
        LIMIT 1
    """
    tk_row = fetch_one(token_sql, [token_value])

    if not tk_row:
        return jsonify({"error": "Token no existe"}), 404

    if int(tk_row["event_project_id"]) != int(ep_row["event_project_id"]):
        return jsonify({"error": "El token no corresponde al proyecto"}), 409

    if tk_row["status"] not in ("AVAILABLE", "RESERVED"):
        return jsonify({"error": f"El token no está disponible ({tk_row['status']})"}), 409

    if tk_row["status"] == "RESERVED":
        if tk_row["reserved_by_request_id"] != req_row["request_id"]:
            return jsonify({"error": "El token está reservado por otra solicitud"}), 409

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
            "general_name": ep_row["general_name"],
            "partner_name": ep_row["partner_name"],
            "slots_total": ep_row["slots_total"],
        },
        "token": {
            "id": tk_row["id"],
            "token_value": tk_row["token_value"],
            "status": tk_row["status"],
            "expires_at": tk_row["expires_at"],
        },
        "legal_confirmation": {
            "accepted_checkbox_required": True,
            "accepted_full_name_required": True,
            "legal_text_version_default": "v1",
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
    legal_text_version = (payload.get("legal_text_version") or "v1").strip()

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

    accepted_ip = (
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.headers.get("X-Real-IP", "").strip()
        or (request.remote_addr or "").strip()
        or None
    )
    accepted_user_agent = (request.headers.get("User-Agent") or "").strip() or None

    def tx(conn, cur):
        # 1) solicitud del alumno
        cur.execute(
            """
            SELECT
                ser.id AS request_id,
                ser.status AS request_status,
                ser.event_id,
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

        # 2) evitar doble registro
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

        # 3) proyecto en temporada
        cur.execute(
            """
            SELECT
                ep.id AS event_project_id,
                ep.project_id,
                ep.status AS event_project_status,
                p.name AS project_name,
                p.general_name,
                pa.name AS partner_name
            FROM event_projects ep
            JOIN project p ON p.id = ep.project_id
            LEFT JOIN partner pa ON pa.id = p.id_partner
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
                pt.event_project_id,
                pt.reserved_by_request_id,
                pt.reserved_until
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

        # 5) expirar si corresponde
        cur.execute(
            """
            UPDATE project_tokens
            SET status = 'EXPIRED'
            WHERE id = %s
              AND status = 'AVAILABLE'
              AND expires_at IS NOT NULL
              AND expires_at <= NOW()
            """,
            [tk_row["id"]]
        )

        cur.execute(
            """
            SELECT
                id,
                token_value,
                status,
                reserved_by_request_id,
                reserved_until
            FROM project_tokens
            WHERE id = %s
            LIMIT 1
            """,
            [tk_row["id"]]
        )
        tk_row = cur.fetchone()

        if tk_row["status"] == "EXPIRED":
            return {"error": "El token expiró", "status": 409}

        if tk_row["status"] == "USED":
            return {"error": "El token ya fue utilizado", "status": 409}

        if tk_row["status"] == "REVOKED":
            return {"error": "El token fue revocado", "status": 409}

        if tk_row["status"] == "RESERVED":
            if tk_row["reserved_by_request_id"] != req_row["request_id"]:
                return {"error": "El token está reservado por otra solicitud", "status": 409}

        if tk_row["status"] not in ("AVAILABLE", "RESERVED"):
            return {"error": f"El token no está disponible ({tk_row['status']})", "status": 409}

        # 6) validar nombre razonablemente
        expected_name = _normalize_text(req_row["full_name"])
        provided_name = _normalize_text(accepted_full_name)

        if expected_name != provided_name:
            return {"error": "El nombre completo no coincide con el del alumno", "status": 409}

        # 7) construir snapshot + hash + firma
        snapshot = _build_acceptance_snapshot(
            req_row=req_row,
            ep_row=ep_row,
            token_row=tk_row,
            accepted_full_name=accepted_full_name,
            legal_text_version=legal_text_version,
        )
        snapshot_json = json.dumps(snapshot, ensure_ascii=False, sort_keys=True)
        acceptance_hash = _sha256_text(snapshot_json)
        acceptance_signature = _sign_snapshot(snapshot_json)

        # 8) crear registration
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
                acceptance_snapshot_json,
                acceptance_hash,
                acceptance_signature,
                accepted_ip,
                accepted_user_agent,
                status
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, NOW(),
                %s, %s, %s, %s, %s,
                'ACTIVE'
            )
            """,
            [
                req_row["event_id"],
                ep_row["event_project_id"],
                req_row["user_id"],
                req_row["request_id"],
                tk_row["id"],
                True,
                accepted_full_name,
                legal_text_version,
                snapshot_json,
                acceptance_hash,
                acceptance_signature,
                accepted_ip,
                accepted_user_agent,
            ]
        )
        registration_id = cur.lastrowid

        # 9) consumir token
        cur.execute(
            """
            UPDATE project_tokens
            SET status = 'USED',
                used_by_request_id = %s,
                used_at = NOW(),
                reserved_by_request_id = NULL,
                reserved_at = NULL,
                reserved_until = NULL
            WHERE id = %s
            """,
            [req_row["request_id"], tk_row["id"]]
        )

        # 10) cerrar solicitud
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
            "event": {
                "id": req_row["event_id"],
                "season": season,
            },
            "student": {
                "id": req_row["user_id"],
                "full_name": req_row["full_name"],
                "enrolment_number": req_row["enrolment_number"],
            },
            "project": {
                "event_project_id": ep_row["event_project_id"],
                "project_id": ep_row["project_id"],
                "project_name": ep_row["project_name"],
                "general_name": ep_row["general_name"],
                "partner_name": ep_row["partner_name"],
            },
            "token": {
                "id": tk_row["id"],
                "token_value": tk_row["token_value"],
                "status": "USED",
            },
            "registration": {
                "id": registration_id,
                "event_id": req_row["event_id"],
                "event_project_id": ep_row["event_project_id"],
                "project_name": ep_row["project_name"],
                "general_name": ep_row["general_name"],
                "token_value": tk_row["token_value"],
                "accepted_full_name": accepted_full_name,
                "legal_text_version": legal_text_version,
                "acceptance_hash": acceptance_hash,
                "acceptance_signature": acceptance_signature,
            },
            "legal_confirmation": {
                "accepted_checkbox": True,
                "accepted_full_name": accepted_full_name,
                "legal_text_version": legal_text_version,
                "acceptance_hash": acceptance_hash,
                "acceptance_signature": acceptance_signature,
                "accepted_ip": accepted_ip,
                "accepted_user_agent": accepted_user_agent,
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