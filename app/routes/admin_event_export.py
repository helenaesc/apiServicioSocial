from flask import Blueprint, jsonify, request, session, send_file
from ..database import fetch_all, fetch_one
from ..authz import require_role, ROLE_ADMIN
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
import hashlib
import hmac
import json
import os
from io import BytesIO

admin_event_export_bp = Blueprint("admin_event_export", __name__)


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


def _autosize_columns(ws):
    widths = {}
    for row in ws.iter_rows():
        for cell in row:
            value = "" if cell.value is None else str(cell.value)
            widths[cell.column] = max(widths.get(cell.column, 0), len(value))
    for col_idx, width in widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = min(max(width + 2, 12), 60)


def _style_sheet(ws, title=None):
    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(color="FFFFFF", bold=True)
    thin_gray = Side(style="thin", color="D9E2F3")
    border = Border(bottom=thin_gray)

    if title:
        ws["A1"] = title
        ws["A1"].font = Font(bold=True, size=14, color="1F1F1F")
        ws["A1"].alignment = Alignment(horizontal="left")
        ws.append([])

    # detectar fila de encabezados
    header_row = 3 if title else 1
    for cell in ws[header_row]:
        if cell.value is not None:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = border

    ws.freeze_panes = f"A{header_row + 1}"
    _autosize_columns(ws)


def _write_table(ws, headers, rows, title=None):
    if title:
        ws["A1"] = title
        ws["A1"].font = Font(bold=True, size=14)
        ws.append([])

    ws.append(headers)
    for row in rows:
        ws.append([row.get(h) for h in headers])

    _style_sheet(ws, title=title)


@admin_event_export_bp.get("/api/admin/events/<int:event_id>/export")
def export_event_report(event_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    event_row = fetch_one(
        """
        SELECT
            id,
            year,
            season,
            display_name,
            status,
            is_visible_to_students,
            catalog_open_at,
            onsite_start_at,
            onsite_end_at,
            registration_close_at
        FROM events
        WHERE id = %s
        LIMIT 1
        """,
        [event_id]
    )

    if not event_row:
        return jsonify({"error": "Evento no encontrado"}), 404

    # =========================
    # Resumen requests
    # =========================
    req_summary = fetch_one(
        """
        SELECT
            SUM(CASE WHEN status = 'REQUESTED' THEN 1 ELSE 0 END) AS requested_count,
            SUM(CASE WHEN status = 'VALIDATED' THEN 1 ELSE 0 END) AS validated_count,
            SUM(CASE WHEN status = 'ACCESS_ENABLED' THEN 1 ELSE 0 END) AS access_enabled_count,
            SUM(CASE WHEN status = 'REGISTERED' THEN 1 ELSE 0 END) AS registered_count,
            SUM(CASE WHEN status = 'CANCELLED' THEN 1 ELSE 0 END) AS cancelled_count,
            SUM(CASE WHEN status = 'CLOSED' THEN 1 ELSE 0 END) AS closed_count,
            COUNT(*) AS total_requests
        FROM student_event_requests
        WHERE event_id = %s
        """,
        [event_id]
    ) or {}

    # =========================
    # Resumen incidentes
    # =========================
    incident_summary = fetch_one(
        """
        SELECT
            SUM(CASE WHEN status = 'OPEN' THEN 1 ELSE 0 END) AS open_count,
            SUM(CASE WHEN status = 'IN_PROGRESS' THEN 1 ELSE 0 END) AS in_progress_count,
            SUM(CASE WHEN status = 'RESOLVED' THEN 1 ELSE 0 END) AS resolved_count,
            SUM(CASE WHEN status = 'DISMISSED' THEN 1 ELSE 0 END) AS dismissed_count,
            COUNT(*) AS total_incidents
        FROM incident_reports
        WHERE event_id = %s
        """,
        [event_id]
    ) or {}

    # =========================
    # Resumen tokens
    # =========================
    token_summary = fetch_one(
        """
        SELECT
            SUM(CASE WHEN pt.status = 'AVAILABLE' AND (pt.expires_at IS NULL OR pt.expires_at > NOW()) THEN 1 ELSE 0 END) AS available_count,
            SUM(CASE WHEN pt.status = 'RESERVED' THEN 1 ELSE 0 END) AS reserved_count,
            SUM(CASE WHEN pt.status = 'USED' THEN 1 ELSE 0 END) AS used_count,
            SUM(CASE WHEN pt.status = 'REVOKED' THEN 1 ELSE 0 END) AS revoked_count,
            SUM(CASE WHEN pt.status = 'EXPIRED' THEN 1 ELSE 0 END) AS expired_count,
            COUNT(*) AS total_tokens
        FROM project_tokens pt
        JOIN event_projects ep ON ep.id = pt.event_project_id
        WHERE ep.event_id = %s
        """,
        [event_id]
    ) or {}

    # =========================
    # Proyectos activos
    # =========================
    projects_rows = fetch_all(
        """
        SELECT
            ep.id AS event_project_id,
            ep.event_id,
            ep.project_id,
            ep.slots_total,
            ep.status AS event_project_status,
            p.name AS project_name,
            p.general_name,
            pa.name AS partner_name,

            (
              SELECT COUNT(*)
              FROM registrations r
              WHERE r.event_project_id = ep.id
                AND r.status = 'ACTIVE'
            ) AS registered_count,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
                AND pt.status = 'AVAILABLE'
                AND (pt.expires_at IS NULL OR pt.expires_at > NOW())
            ) AS tokens_available,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
                AND pt.status = 'USED'
            ) AS tokens_used,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
                AND pt.status = 'REVOKED'
            ) AS tokens_revoked,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
                AND pt.status = 'EXPIRED'
            ) AS tokens_expired,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
            ) AS tokens_total
        FROM event_projects ep
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN partner pa ON pa.id = p.id_partner
        WHERE ep.event_id = %s
        ORDER BY p.name
        """,
        [event_id]
    )

    for r in projects_rows:
        slots_total = int(r.get("slots_total") or 0)
        registered_count = int(r.get("registered_count") or 0)
        tokens_total = int(r.get("tokens_total") or 0)
        tokens_available = int(r.get("tokens_available") or 0)

        if tokens_total > 0:
            r["cupos_disponibles"] = tokens_available
        else:
            r["cupos_disponibles"] = max(slots_total - registered_count, 0)

    # =========================
    # Inscritos
    # =========================
    registrations_rows = fetch_all(
        """
        SELECT
            r.id AS registration_id,
            r.event_id,
            r.event_project_id,
            r.request_id,
            r.project_token_id,
            r.id_user AS student_id,
            CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS student_full_name,
            u.enrolment_number,
            u.email,
            ser.folio,
            p.name AS project_name,
            p.general_name,
            pa.name AS partner_name,
            pt.token_value,
            r.accepted_full_name,
            r.legal_text_version,
            r.accepted_at,
            r.status AS registration_status
        FROM registrations r
        JOIN users u ON u.id = r.id_user
        JOIN student_event_requests ser ON ser.id = r.request_id
        JOIN event_projects ep ON ep.id = r.event_project_id
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN partner pa ON pa.id = p.id_partner
        JOIN project_tokens pt ON pt.id = r.project_token_id
        WHERE r.event_id = %s
        ORDER BY r.accepted_at DESC, r.id DESC
        """,
        [event_id]
    )

    # =========================
    # Tokens
    # =========================
    tokens_rows = fetch_all(
        """
        SELECT
            pt.id AS token_id,
            pt.event_project_id,
            p.name AS project_name,
            p.general_name,
            pa.name AS partner_name,
            pt.token_value,
            pt.status AS token_status,
            pt.reserved_by_request_id,
            pt.reserved_at,
            pt.reserved_until,
            pt.used_by_request_id,
            pt.used_at,
            pt.revoked_at,
            pt.revoke_reason,
            pt.revoked_by_admin_user_id,
            pt.expires_at,
            pt.created_at
        FROM project_tokens pt
        JOIN event_projects ep ON ep.id = pt.event_project_id
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN partner pa ON pa.id = p.id_partner
        WHERE ep.event_id = %s
        ORDER BY pt.created_at DESC, pt.id DESC
        """,
        [event_id]
    )

    # =========================
    # Incidentes
    # =========================
    incidents_rows = fetch_all(
        """
        SELECT
            ir.id AS incident_id,
            ir.event_id,
            ir.request_id,
            ir.id_user,
            ir.performed_by_admin_user_id,
            ir.type,
            ir.severity,
            ir.status,
            ir.description,
            ir.resolution_notes,
            ir.created_at,
            ir.resolved_at
        FROM incident_reports ir
        WHERE ir.event_id = %s
        ORDER BY ir.created_at DESC, ir.id DESC
        """,
        [event_id]
    )

    # =========================
    # Evidencia legal
    # =========================
    evidence_rows_raw = fetch_all(
        """
        SELECT
            r.id AS registration_id,
            r.request_id,
            ser.folio,
            CONCAT_WS(' ', u.first_name, u.second_name, u.p_last_name, u.m_last_name) AS student_full_name_system,
            r.accepted_full_name,
            u.enrolment_number,
            p.name AS project_name,
            p.general_name,
            pa.name AS partner_name,
            pt.token_value,
            r.legal_text_version,
            r.accepted_at,
            r.accepted_ip,
            r.accepted_user_agent,
            r.acceptance_snapshot_json,
            r.acceptance_hash,
            r.acceptance_signature
        FROM registrations r
        JOIN users u ON u.id = r.id_user
        JOIN student_event_requests ser ON ser.id = r.request_id
        JOIN event_projects ep ON ep.id = r.event_project_id
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN partner pa ON pa.id = p.id_partner
        JOIN project_tokens pt ON pt.id = r.project_token_id
        WHERE r.event_id = %s
        ORDER BY r.accepted_at DESC, r.id DESC
        """,
        [event_id]
    )

    evidence_rows = []
    snapshot_rows = []

    for r in evidence_rows_raw:
        snapshot_json = r.get("acceptance_snapshot_json") or ""
        stored_hash = r.get("acceptance_hash") or ""
        stored_signature = r.get("acceptance_signature") or ""

        calculated_hash = _sha256_text(snapshot_json) if snapshot_json else None
        try:
            calculated_signature = _sign_snapshot(snapshot_json) if snapshot_json else None
            signature_error = None
        except Exception as e:
            calculated_signature = None
            signature_error = str(e)

        hash_verified = bool(snapshot_json) and bool(stored_hash) and (calculated_hash == stored_hash)
        signature_verified = (
            bool(snapshot_json)
            and bool(stored_signature)
            and bool(calculated_signature)
            and (calculated_signature == stored_signature)
        )
        verified = hash_verified and signature_verified

        evidence_rows.append({
            "registration_id": r["registration_id"],
            "request_id": r["request_id"],
            "folio": r["folio"],
            "student_full_name_system": r["student_full_name_system"],
            "accepted_full_name": r["accepted_full_name"],
            "enrolment_number": r["enrolment_number"],
            "project_name": r["project_name"],
            "general_name": r["general_name"],
            "partner_name": r["partner_name"],
            "token_value": r["token_value"],
            "legal_text_version": r["legal_text_version"],
            "accepted_at": r["accepted_at"],
            "accepted_ip": r["accepted_ip"],
            "accepted_user_agent": r["accepted_user_agent"],
            "acceptance_hash": stored_hash,
            "acceptance_signature": stored_signature,
            "hash_verified": hash_verified,
            "signature_verified": signature_verified,
            "verified": verified,
            "signature_error": signature_error,
        })

        snapshot_rows.append({
            "registration_id": r["registration_id"],
            "request_id": r["request_id"],
            "acceptance_snapshot_json": snapshot_json
        })

    # =========================
    # Crear workbook
    # =========================
    wb = Workbook()

    # Hoja 1: Resumen
    ws = wb.active
    ws.title = "Resumen_Temporada"

    resumen_rows = [
        {"campo": "event_id", "valor": event_row["id"]},
        {"campo": "display_name", "valor": event_row["display_name"]},
        {"campo": "year", "valor": event_row["year"]},
        {"campo": "season", "valor": event_row["season"]},
        {"campo": "status", "valor": event_row["status"]},
        {"campo": "is_visible_to_students", "valor": event_row["is_visible_to_students"]},
        {"campo": "catalog_open_at", "valor": event_row["catalog_open_at"]},
        {"campo": "onsite_start_at", "valor": event_row["onsite_start_at"]},
        {"campo": "onsite_end_at", "valor": event_row["onsite_end_at"]},
        {"campo": "registration_close_at", "valor": event_row["registration_close_at"]},
        {"campo": "requests_requested", "valor": int(req_summary.get("requested_count") or 0)},
        {"campo": "requests_validated", "valor": int(req_summary.get("validated_count") or 0)},
        {"campo": "requests_access_enabled", "valor": int(req_summary.get("access_enabled_count") or 0)},
        {"campo": "requests_registered", "valor": int(req_summary.get("registered_count") or 0)},
        {"campo": "requests_cancelled", "valor": int(req_summary.get("cancelled_count") or 0)},
        {"campo": "requests_closed", "valor": int(req_summary.get("closed_count") or 0)},
        {"campo": "requests_total", "valor": int(req_summary.get("total_requests") or 0)},
        {"campo": "incidents_open", "valor": int(incident_summary.get("open_count") or 0)},
        {"campo": "incidents_in_progress", "valor": int(incident_summary.get("in_progress_count") or 0)},
        {"campo": "incidents_resolved", "valor": int(incident_summary.get("resolved_count") or 0)},
        {"campo": "incidents_dismissed", "valor": int(incident_summary.get("dismissed_count") or 0)},
        {"campo": "incidents_total", "valor": int(incident_summary.get("total_incidents") or 0)},
        {"campo": "tokens_available", "valor": int(token_summary.get("available_count") or 0)},
        {"campo": "tokens_reserved", "valor": int(token_summary.get("reserved_count") or 0)},
        {"campo": "tokens_used", "valor": int(token_summary.get("used_count") or 0)},
        {"campo": "tokens_revoked", "valor": int(token_summary.get("revoked_count") or 0)},
        {"campo": "tokens_expired", "valor": int(token_summary.get("expired_count") or 0)},
        {"campo": "tokens_total", "valor": int(token_summary.get("total_tokens") or 0)},
    ]
    _write_table(ws, ["campo", "valor"], resumen_rows, title="Resumen de Temporada")

    # Hoja 2
    ws = wb.create_sheet("Proyectos_Activos")
    _write_table(ws, [
        "event_project_id",
        "event_id",
        "project_id",
        "project_name",
        "general_name",
        "partner_name",
        "event_project_status",
        "slots_total",
        "registered_count",
        "tokens_available",
        "tokens_used",
        "tokens_revoked",
        "tokens_expired",
        "tokens_total",
        "cupos_disponibles",
    ], projects_rows, title="Proyectos Activos")

    # Hoja 3
    ws = wb.create_sheet("Inscritos")
    _write_table(ws, [
        "registration_id",
        "event_id",
        "event_project_id",
        "request_id",
        "project_token_id",
        "student_id",
        "student_full_name",
        "enrolment_number",
        "email",
        "folio",
        "project_name",
        "general_name",
        "partner_name",
        "token_value",
        "accepted_full_name",
        "legal_text_version",
        "accepted_at",
        "registration_status",
    ], registrations_rows, title="Inscritos")

    # Hoja 4
    ws = wb.create_sheet("Tokens")
    _write_table(ws, [
        "token_id",
        "event_project_id",
        "project_name",
        "general_name",
        "partner_name",
        "token_value",
        "token_status",
        "reserved_by_request_id",
        "reserved_at",
        "reserved_until",
        "used_by_request_id",
        "used_at",
        "revoked_at",
        "revoke_reason",
        "revoked_by_admin_user_id",
        "expires_at",
        "created_at",
    ], tokens_rows, title="Tokens")

    # Hoja 5
    ws = wb.create_sheet("Incidentes")
    _write_table(ws, [
        "incident_id",
        "event_id",
        "request_id",
        "id_user",
        "performed_by_admin_user_id",
        "type",
        "severity",
        "status",
        "description",
        "resolution_notes",
        "created_at",
        "resolved_at",
    ], incidents_rows, title="Incidentes")

    # Hoja 6
    ws = wb.create_sheet("Evidencia_Legal")
    _write_table(ws, [
        "registration_id",
        "request_id",
        "folio",
        "student_full_name_system",
        "accepted_full_name",
        "enrolment_number",
        "project_name",
        "general_name",
        "partner_name",
        "token_value",
        "legal_text_version",
        "accepted_at",
        "accepted_ip",
        "accepted_user_agent",
        "acceptance_hash",
        "acceptance_signature",
        "hash_verified",
        "signature_verified",
        "verified",
        "signature_error",
    ], evidence_rows, title="Evidencia Legal")

    # Hoja 7
    ws = wb.create_sheet("Snapshot_JSON")
    _write_table(ws, [
        "registration_id",
        "request_id",
        "acceptance_snapshot_json",
    ], snapshot_rows, title="Snapshot JSON")

    # Formato de fechas simple
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if hasattr(cell.value, "year") and hasattr(cell.value, "month"):
                    cell.number_format = "yyyy-mm-dd hh:mm:ss"

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    season_clean = str(event_row["season"]).lower()
    year_clean = str(event_row["year"])
    filename = f"reporte_evento_{event_id}{season_clean}{year_clean}.xlsx"

    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )