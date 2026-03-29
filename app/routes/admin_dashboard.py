from flask import Blueprint, jsonify, request
from ..database import fetch_all, fetch_one
from ..authz import require_role, ROLE_ADMIN

admin_dashboard_bp = Blueprint("admin_dashboard", __name__)


@admin_dashboard_bp.get("/api/admin/dashboard/summary")
def dashboard_summary():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    event_id = request.args.get("event_id", type=int)

    if not event_id:
        return jsonify({"error": "event_id es obligatorio"}), 400

    event_sql = """
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
    """
    event_row = fetch_one(event_sql, [event_id])

    if not event_row:
        return jsonify({"error": "Evento no encontrado"}), 404

    summary_sql = """
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
    """
    req_summary = fetch_one(summary_sql, [event_id]) or {}

    incidents_sql = """
        SELECT
            SUM(CASE WHEN status = 'OPEN' THEN 1 ELSE 0 END) AS open_count,
            SUM(CASE WHEN status = 'IN_PROGRESS' THEN 1 ELSE 0 END) AS in_progress_count,
            SUM(CASE WHEN status = 'RESOLVED' THEN 1 ELSE 0 END) AS resolved_count,
            SUM(CASE WHEN status = 'DISMISSED' THEN 1 ELSE 0 END) AS dismissed_count,
            COUNT(*) AS total_incidents
        FROM incident_reports
        WHERE event_id = %s
    """
    incident_summary = fetch_one(incidents_sql, [event_id]) or {}

    return jsonify({
        "event": event_row,
        "requests": {
            "requested": int(req_summary.get("requested_count") or 0),
            "validated": int(req_summary.get("validated_count") or 0),
            "access_enabled": int(req_summary.get("access_enabled_count") or 0),
            "registered": int(req_summary.get("registered_count") or 0),
            "cancelled": int(req_summary.get("cancelled_count") or 0),
            "closed": int(req_summary.get("closed_count") or 0),
            "total": int(req_summary.get("total_requests") or 0),
        },
        "incidents": {
            "open": int(incident_summary.get("open_count") or 0),
            "in_progress": int(incident_summary.get("in_progress_count") or 0),
            "resolved": int(incident_summary.get("resolved_count") or 0),
            "dismissed": int(incident_summary.get("dismissed_count") or 0),
            "total": int(incident_summary.get("total_incidents") or 0),
        }
    }), 200


@admin_dashboard_bp.get("/api/admin/dashboard/projects")
def dashboard_projects():
    role = require_role(request, {ROLE_ADMIN})
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    event_id = request.args.get("event_id", type=int)

    if not event_id:
        return jsonify({"error": "event_id es obligatorio"}), 400

    event_row = fetch_one("SELECT id FROM events WHERE id = %s LIMIT 1", [event_id])
    if not event_row:
        return jsonify({"error": "Evento no encontrado"}), 404

    sql = """
        SELECT
            ep.id AS event_project_id,
            ep.event_id,
            ep.project_id,
            ep.slots_total,
            ep.status AS event_project_status,
            p.name AS project_name,
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
        JOIN partner pa ON pa.id = p.id_partner
        WHERE ep.event_id = %s
        ORDER BY p.name
    """

    rows = fetch_all(sql, [event_id])

    for r in rows:
        slots_total = int(r.get("slots_total") or 0)
        registered_count = int(r.get("registered_count") or 0)
        tokens_available = int(r.get("tokens_available") or 0)

        # fallback visual útil
        if int(r.get("tokens_total") or 0) > 0:
            r["cupos_disponibles"] = tokens_available
        else:
            r["cupos_disponibles"] = max(slots_total - registered_count, 0)

    return jsonify(rows), 200