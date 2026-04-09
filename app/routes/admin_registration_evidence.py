from flask import Blueprint, jsonify, request, session
from ..database import fetch_one
from ..authz import require_role, ROLE_ADMIN
import hashlib
import hmac
import json
import os

admin_registration_evidence_bp = Blueprint("admin_registration_evidence", __name__)


def _get_current_admin_role(req):
    """
    Prioridad:
    1) sesión real
    2) compatibilidad temporal con X-ADMIN-KEY
    """
    session_role = session.get("admin_user_role")
    if session_role == ROLE_ADMIN:
        return session_role

    legacy_role = require_role(req, {ROLE_ADMIN})
    if legacy_role:
        return legacy_role

    return None


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sign_snapshot(snapshot_json: str) -> str:
    secret = os.getenv("APP_SIGNATURE_SECRET", "").strip()
    if not secret:
        raise RuntimeError("APP_SIGNATURE_SECRET no está configurado")
    return hmac.new(
        secret.encode("utf-8"),
        snapshot_json.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def _safe_load_snapshot(snapshot_json: str):
    try:
        return json.loads(snapshot_json) if snapshot_json else None
    except Exception:
        return None


@admin_registration_evidence_bp.get("/api/admin/registrations/<int:registration_id>/evidence")
def get_registration_evidence(registration_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    sql = """
        SELECT
            r.id,
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
            r.status,

            ev.year,
            ev.season,
            ev.display_name AS event_display_name,

            p.name AS project_name,
            p.general_name,
            pa.name AS partner_name,

            pt.token_value,

            CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS student_full_name,
            u.enrolment_number,
            u.email,

            ser.folio,
            ser.status AS request_status
        FROM registrations r
        JOIN events ev ON ev.id = r.event_id
        JOIN event_projects ep ON ep.id = r.event_project_id
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN partner pa ON pa.id = p.id_partner
        JOIN project_tokens pt ON pt.id = r.project_token_id
        JOIN users u ON u.id = r.id_user
        JOIN student_event_requests ser ON ser.id = r.request_id
        WHERE r.id = %s
        LIMIT 1
    """

    row = fetch_one(sql, [registration_id])

    if not row:
        return jsonify({"error": "Registro no encontrado"}), 404

    snapshot_json = row.get("acceptance_snapshot_json") or ""
    stored_hash = row.get("acceptance_hash") or ""
    stored_signature = row.get("acceptance_signature") or ""

    calculated_hash = _sha256_text(snapshot_json) if snapshot_json else None

    try:
        calculated_signature = _sign_snapshot(snapshot_json) if snapshot_json else None
        signature_error = None
    except Exception as e:
        calculated_signature = None
        signature_error = str(e)

    hash_matches = bool(snapshot_json) and bool(stored_hash) and (calculated_hash == stored_hash)
    signature_matches = (
        bool(snapshot_json)
        and bool(stored_signature)
        and bool(calculated_signature)
        and (calculated_signature == stored_signature)
    )

    verified = hash_matches and signature_matches

    return jsonify({
        "performed_by": {
            "role": role,
            "admin_user_id": session.get("admin_user_id")
        },
        "registration": {
            "id": row["id"],
            "status": row["status"],
            "event_id": row["event_id"],
            "event_project_id": row["event_project_id"],
            "request_id": row["request_id"],
            "project_token_id": row["project_token_id"],
            "accepted_at": row["accepted_at"],
        },
        "event": {
            "id": row["event_id"],
            "year": row["year"],
            "season": row["season"],
            "display_name": row["event_display_name"],
        },
        "student": {
            "id": row["id_user"],
            "full_name": row["student_full_name"],
            "enrolment_number": row["enrolment_number"],
            "email": row["email"],
        },
        "request": {
            "id": row["request_id"],
            "folio": row["folio"],
            "status": row["request_status"],
        },
        "project": {
            "id": row["event_project_id"],
            "project_name": row["project_name"],
            "general_name": row["general_name"],
            "partner_name": row["partner_name"],
        },
        "token": {
            "id": row["project_token_id"],
            "token_value": row["token_value"],
        },
        "legal_confirmation": {
            "accepted_checkbox": bool(row["accepted_checkbox"]),
            "accepted_full_name": row["accepted_full_name"],
            "legal_text_version": row["legal_text_version"],
            "accepted_at": row["accepted_at"],
            "accepted_ip": row["accepted_ip"],
            "accepted_user_agent": row["accepted_user_agent"],
        },
        "evidence": {
            "snapshot_json": snapshot_json,
            "snapshot": _safe_load_snapshot(snapshot_json),
            "stored_hash": stored_hash,
            "calculated_hash": calculated_hash,
            "stored_signature": stored_signature,
            "calculated_signature": calculated_signature,
        },
        "verification": {
            "hash_matches": hash_matches,
            "signature_matches": signature_matches,
            "verified": verified,
            "signature_error": signature_error
        }
    }), 200