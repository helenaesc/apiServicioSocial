from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import fetch_all
from ..authz import require_role, ROLE_ADMIN

admin_registrations_bp = Blueprint("admin_registrations", __name__)


@admin_registrations_bp.get("/api/admin/registrations")
def list_registrations():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    event_id = request.args.get("event_id", type=int)

    if not event_id:
        return jsonify({"error": "event_id es obligatorio"}), 400

    sql = """
        SELECT
            r.id,
            r.event_id,
            r.event_project_id,
            r.id_user,
            r.request_id,
            r.project_token_id,
            r.accepted_full_name,
            r.legal_text_version,
            r.accepted_at,
            r.status AS registration_status,

            u.enrolment_number,
            CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS student_name,

            p.name AS project_name,
            p.general_name,
            pa.name AS partner_name,

            pt.token_value,

            ev.display_name AS event_display_name,
            ev.year,
            ev.season

        FROM registrations r
        JOIN users u ON u.id = r.id_user
        JOIN event_projects ep ON ep.id = r.event_project_id
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN partner pa ON pa.id = p.id_partner
        JOIN project_tokens pt ON pt.id = r.project_token_id
        JOIN events ev ON ev.id = r.event_id
        WHERE r.event_id = %s
        ORDER BY r.accepted_at DESC, r.id DESC
    """

    try:
        rows = fetch_all(sql, [event_id])
        return jsonify(rows), 200
    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500