from flask import Blueprint, jsonify, request, session
from mysql.connector import Error
from ..database import fetch_all, fetch_one, execute_tx
from ..authz import require_role, ROLE_ADMIN, ROLE_STAFF
import hashlib
import hmac
import json
import os

admin_registrations_bp = Blueprint("admin_registrations", __name__)


def _get_current_admin_role(req):
    session_role = session.get("admin_user_role")
    if session_role in {ROLE_ADMIN, ROLE_STAFF}:
        return session_role

    legacy_role = require_role(req, {ROLE_ADMIN, ROLE_STAFF})
    if legacy_role:
        return legacy_role

    return None


def _get_current_admin_user_id():
    return session.get("admin_user_id")


def _sign_snapshot(snapshot_json: str) -> str:
    secret = os.getenv("APP_SIGNATURE_SECRET", "").strip()
    if not secret:
        raise RuntimeError("APP_SIGNATURE_SECRET no está configurado")

    return hmac.new(
        secret.encode("utf-8"),
        snapshot_json.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def _insert_registration_audit(
    cur,
    registration_id: int,
    event_id: int,
    id_user: int,
    action_type: str,
    old_status: str | None,
    new_status: str | None,
    actor_type: str,
    actor_admin_user_id: int | None = None,
    reason: str | None = None,
    snapshot: dict | None = None,
):
    snapshot_json = json.dumps(snapshot, ensure_ascii=False, sort_keys=True) if snapshot is not None else None

    cur.execute(
        """
        INSERT INTO registration_audit_log
        (
            registration_id,
            event_id,
            id_user,
            action_type,
            old_status,
            new_status,
            actor_type,
            actor_admin_user_id,
            reason,
            snapshot_json
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """,
        [
            registration_id,
            event_id,
            id_user,
            action_type,
            old_status,
            new_status,
            actor_type,
            actor_admin_user_id,
            reason,
            snapshot_json,
        ]
    )


@admin_registrations_bp.get("/api/admin/registrations")
def list_registrations():
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401

    event_id = request.args.get("event_id", type=int)
    status = (request.args.get("status") or "").strip().upper()

    if not event_id:
        return jsonify({"error": "event_id es obligatorio"}), 400

    where = ["r.event_id = %s"]
    params = [event_id]

    if status:
        where.append("r.status = %s")
        params.append(status)

    sql = f"""
        SELECT
            r.id AS registration_id,
            r.event_id,
            r.event_project_id,
            r.id_user,
            r.request_id,
            r.project_token_id,
            r.accepted_full_name,
            r.legal_text_version,
            r.accepted_at,
            r.status AS registration_status,
            r.cancelled_at,
            r.cancel_reason,
            r.cancelled_by_admin_user_id,

            u.enrolment_number,
            CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS student_name,

            ser.folio,

            p.name AS project_name,
            p.general_name,
            pa.name AS partner_name,

            pt.token_value
        FROM registrations r
        JOIN users u
            ON u.id = r.id_user
        JOIN student_event_requests ser
            ON ser.id = r.request_id
        JOIN event_projects ep
            ON ep.id = r.event_project_id
        JOIN project p
            ON p.id = ep.project_id
        LEFT JOIN partner pa
            ON pa.id = p.id_partner
        LEFT JOIN project_tokens pt
            ON pt.id = r.project_token_id
        WHERE {" AND ".join(where)}
        ORDER BY
            CASE r.status
                WHEN 'ACTIVE' THEN 1
                WHEN 'CANCELLED' THEN 2
                ELSE 99
            END,
            r.accepted_at DESC,
            r.id DESC
    """

    rows = fetch_all(sql, params)
    return jsonify(rows), 200


@admin_registrations_bp.patch("/api/admin/registrations/<int:registration_id>/cancel")
def cancel_registration(registration_id: int):
    role = _get_current_admin_role(request)
    if role != ROLE_ADMIN:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    admin_user_id = _get_current_admin_user_id()
    payload = request.get_json(silent=True) or {}
    reason = (payload.get("reason") or "").strip()

    if not reason:
        return jsonify({"error": "reason es obligatorio"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            SELECT
                r.id,
                r.status,
                r.event_id,
                r.event_project_id,
                r.id_user,
                r.request_id,
                r.project_token_id
            FROM registrations r
            WHERE r.id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [registration_id]
        )
        reg = cur.fetchone()

        if not reg:
            return {"error": "Registro no encontrado", "status": 404}

        if reg["status"] == "CANCELLED":
            return {"error": "La inscripción ya está cancelada", "status": 409}

        if reg["status"] != "ACTIVE":
            return {
                "error": f"No se puede cancelar un registro en estado {reg['status']}",
                "status": 409
            }

        # 1) liberar token si existe
        if reg["project_token_id"]:
            cur.execute(
                """
                UPDATE project_tokens
                SET status = 'AVAILABLE',
                    used_by_request_id = NULL,
                    used_at = NULL
                WHERE id = %s
                  AND status = 'USED'
                """,
                [reg["project_token_id"]]
            )

        # 2) cancelar registro
        cur.execute(
            """
            UPDATE registrations
            SET status = 'CANCELLED',
                cancelled_at = NOW(),
                cancel_reason = %s,
                cancelled_by_admin_user_id = %s
            WHERE id = %s
            """,
            [reason, admin_user_id, registration_id]
        )
        
        _insert_registration_audit(
            cur=cur,
            registration_id=registration_id,
            event_id=reg["event_id"],
            id_user=reg["id_user"],
            action_type="REGISTER_CANCELLED",
            old_status="ACTIVE",
            new_status="CANCELLED",
            actor_type="ADMIN",
            actor_admin_user_id=admin_user_id,
            reason=reason,
            snapshot={
                "request_id": reg["request_id"],
                "event_project_id": reg["event_project_id"],
                "project_token_id": reg["project_token_id"],
            }
        )

        # 3) revocar cualquier pase ACTIVO vigente para obligar nuevo flujo presencial
        cur.execute(
            """
            UPDATE pass_sessions
            SET status = 'REVOKED',
                revoked_at = NOW()
            WHERE request_id = %s
              AND status = 'ACTIVE'
            """,
            [reg["request_id"]]
        )

        # 4) regresar solicitud a VALIDATED, no a ACCESS_ENABLED
        #    así el alumno NO puede seguir directo al paso 4
        cur.execute(
            """
            UPDATE student_event_requests
            SET status = 'VALIDATED',
                access_enabled_at = NULL,
                registered_at = NULL,
                closed_at = NULL,
                notes = CONCAT(
                    COALESCE(notes, ''),
                    IF(COALESCE(notes, '') = '', '', ' | '),
                    'Baja aplicada por ADMIN. Requiere nuevo pase y nueva validación presencial.'
                )
            WHERE id = %s
            """,
            [reg["request_id"]]
        )

        return {
            "status": 200,
            "message": "Inscripción cancelada. Token liberado. Solicitud regresada a VALIDATED y requiere nuevo check-in."
        }

    try:
        result = execute_tx(tx)

        if result.get("status") != 200:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({"message": result["message"]}), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_registrations_bp.get("/api/admin/registrations/evidence")
def get_registration_evidence_by_enrolment():
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401

    enrolment_number = (request.args.get("enrolment_number") or "").strip().lower()
    event_id = request.args.get("event_id", type=int)

    if not enrolment_number:
        return jsonify({"error": "enrolment_number es obligatorio"}), 400

    where_extra = ""
    params = [enrolment_number]

    if event_id:
        where_extra = "AND r.event_id = %s"
        params.append(event_id)

    sql = f"""
        SELECT
            r.id AS registration_id,
            r.event_id,
            r.event_project_id,
            r.id_user,
            r.request_id,
            r.project_token_id,
            r.accepted_checkbox,
            r.accepted_full_name,
            r.legal_text_version,
            r.accepted_at,
            r.acceptance_snapshot_json,
            r.acceptance_hash,
            r.acceptance_signature,
            r.accepted_ip,
            r.accepted_user_agent,
            r.status AS registration_status,
            r.cancelled_at,
            r.cancel_reason,
            r.cancelled_by_admin_user_id,

            u.enrolment_number,
            CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS student_full_name,

            ser.folio,

            ev.id AS event_real_id,
            ev.display_name,

            p.name AS project_name,
            p.general_name
        FROM registrations r
        JOIN users u
            ON u.id = r.id_user
        JOIN student_event_requests ser
            ON ser.id = r.request_id
        JOIN events ev
            ON ev.id = r.event_id
        JOIN event_projects ep
            ON ep.id = r.event_project_id
        JOIN project p
            ON p.id = ep.project_id
        WHERE u.enrolment_number = %s
          {where_extra}
        ORDER BY r.accepted_at DESC, r.id DESC
        LIMIT 1
    """

    row = fetch_one(sql, params)

    if not row:
        return jsonify({"error": "No se encontró evidencia para esa matrícula"}), 404

    snapshot_json = row.get("acceptance_snapshot_json") or ""
    stored_hash = row.get("acceptance_hash")
    stored_signature = row.get("acceptance_signature")

    snapshot_data = {}
    if snapshot_json:
        try:
            snapshot_data = json.loads(snapshot_json)
        except Exception:
            snapshot_data = {}

    student_fingerprint = snapshot_data.get("student_fingerprint")

    recalculated_hash = hashlib.sha256(snapshot_json.encode("utf-8")).hexdigest() if snapshot_json else None
    recalculated_signature = _sign_snapshot(snapshot_json) if snapshot_json else None

    hash_matches = bool(snapshot_json and stored_hash == recalculated_hash)
    signature_matches = bool(snapshot_json and stored_signature == recalculated_signature)
    verified = hash_matches and signature_matches

    return jsonify({
        "registration": {
            "id": row["registration_id"],
            "status": row["registration_status"],
            "cancelled_at": row["cancelled_at"],
            "cancel_reason": row["cancel_reason"],
            "cancelled_by_admin_user_id": row["cancelled_by_admin_user_id"],
        },
        "student": {
            "full_name": row["student_full_name"],
            "enrolment_number": row["enrolment_number"],
            "student_fingerprint": student_fingerprint,
        },
        "request": {
            "folio": row["folio"],
        },
        "event": {
            "id": row["event_real_id"],
            "display_name": row["display_name"],
        },
        "project": {
            "event_project_id": row["event_project_id"],
            "project_name": row["project_name"],
            "general_name": row["general_name"],
        },
        "legal_confirmation": {
            "accepted_checkbox": row["accepted_checkbox"],
            "accepted_full_name": row["accepted_full_name"],
            "legal_text_version": row["legal_text_version"],
            "accepted_at": row["accepted_at"],
            "accepted_ip": row["accepted_ip"],
            "accepted_user_agent": row["accepted_user_agent"],
        },
        "evidence": {
            "snapshot_json": snapshot_json,
            "snapshot_data": snapshot_data,
            "stored_hash": stored_hash,
            "stored_signature": stored_signature,
            "recalculated_hash": recalculated_hash,
            "recalculated_signature": recalculated_signature,
        },
        "verification": {
            "hash_matches": hash_matches,
            "signature_matches": signature_matches,
            "verified": verified,
        }
    }), 200