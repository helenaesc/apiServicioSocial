from flask import Blueprint, jsonify, request, session
from mysql.connector import Error
from ..database import fetch_all, execute_tx
from ..authz import require_role, ROLE_ADMIN

admin_registrations_bp = Blueprint("admin_registrations", __name__)


def _get_current_admin_role(req):
    session_role = session.get("admin_user_role")
    if session_role == ROLE_ADMIN:
        return session_role

    legacy_role = require_role(req, {ROLE_ADMIN})
    if legacy_role:
        return legacy_role

    return None


def _get_current_admin_user_id():
    return session.get("admin_user_id")


@admin_registrations_bp.get("/api/admin/registrations")
def list_admin_registrations():
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    event_id = request.args.get("event_id", type=int)
    if not event_id:
        return jsonify({"error": "event_id es obligatorio"}), 400

    sql = """
        SELECT
            r.id AS registration_id,
            r.status AS registration_status,
            r.event_id,
            r.event_project_id,
            r.request_id,
            r.project_token_id,
            r.accepted_full_name,
            r.legal_text_version,
            r.accepted_at,
            r.cancelled_at,
            r.cancel_reason,
            r.cancelled_by_admin_user_id,

            u.id AS student_id,
            CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS student_full_name,
            u.enrolment_number,
            u.email,

            ser.folio,
            ser.status AS request_status,

            p.id AS project_id,
            p.name AS project_name,
            p.general_name,
            pa.name AS partner_name,

            pt.token_value
        FROM registrations r
        JOIN users u ON u.id = r.id_user
        JOIN student_event_requests ser ON ser.id = r.request_id
        JOIN event_projects ep ON ep.id = r.event_project_id
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN partner pa ON pa.id = p.id_partner
        LEFT JOIN project_tokens pt ON pt.id = r.project_token_id
        WHERE r.event_id = %s
        ORDER BY r.accepted_at DESC, r.id DESC
    """

    rows = fetch_all(sql, [event_id])
    return jsonify(rows), 200


@admin_registrations_bp.patch("/api/admin/registrations/<int:registration_id>/cancel")
def cancel_admin_registration(registration_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    admin_user_id = _get_current_admin_user_id()
    payload = request.get_json(silent=True) or {}
    cancellation_reason = (payload.get("reason") or "").strip()

    if not cancellation_reason:
        return jsonify({"error": "reason es obligatorio"}), 400

    if len(cancellation_reason) > 255:
        return jsonify({"error": "reason no puede exceder 255 caracteres"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            SELECT
                r.id,
                r.status,
                r.event_id,
                r.event_project_id,
                r.request_id,
                r.id_user
            FROM registrations r
            WHERE r.id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [registration_id]
        )
        row = cur.fetchone()

        if not row:
            return {"error": "Registro no encontrado", "status": 404}

        if row["status"] == "CANCELLED":
            return {
                "status": 200,
                "message": "La inscripción ya estaba cancelada"
            }

        if row["status"] != "ACTIVE":
            return {
                "error": f"No se puede cancelar un registro con status {row['status']}",
                "status": 409
            }

        cur.execute(
            """
            UPDATE registrations
            SET status = 'CANCELLED',
                cancelled_at = NOW(),
                cancel_reason = %s,
                cancelled_by_admin_user_id = %s
            WHERE id = %s
            """,
            [cancellation_reason, admin_user_id, registration_id]
        )

        # Opcionalmente cerramos la solicitud para reflejar que ya no está vigente
        cur.execute(
            """
            UPDATE student_event_requests
            SET status = 'CLOSED',
                closed_at = COALESCE(closed_at, NOW())
            WHERE id = %s
              AND status = 'REGISTERED'
            """,
            [row["request_id"]]
        )

        cur.execute(
            """
            SELECT
                r.id AS registration_id,
                r.status AS registration_status,
                r.event_id,
                r.event_project_id,
                r.request_id,
                r.project_token_id,
                r.accepted_full_name,
                r.legal_text_version,
                r.accepted_at,
                r.cancelled_at,
                r.cancel_reason,
                r.cancelled_by_admin_user_id,

                u.id AS student_id,
                CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS student_full_name,
                u.enrolment_number,
                u.email,

                ser.folio,
                ser.status AS request_status,

                p.id AS project_id,
                p.name AS project_name,
                p.general_name,
                pa.name AS partner_name,

                pt.token_value
            FROM registrations r
            JOIN users u ON u.id = r.id_user
            JOIN student_event_requests ser ON ser.id = r.request_id
            JOIN event_projects ep ON ep.id = r.event_project_id
            JOIN project p ON p.id = ep.project_id
            LEFT JOIN partner pa ON pa.id = p.id_partner
            LEFT JOIN project_tokens pt ON pt.id = r.project_token_id
            WHERE r.id = %s
            LIMIT 1
            """,
            [registration_id]
        )
        final_row = cur.fetchone()

        return {
            "status": 200,
            "message": "Inscripción cancelada correctamente",
            "registration": final_row
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