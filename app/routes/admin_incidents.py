from flask import Blueprint, jsonify, request, session
from mysql.connector import Error
from ..database import execute_tx, fetch_all, fetch_one
from ..authz import require_role, ROLE_ADMIN, ROLE_STAFF

admin_incidents_bp = Blueprint("admin_incidents", __name__)

VALID_SEVERITIES = {"LOW", "MEDIUM", "HIGH"}
VALID_STATUSES = {"OPEN", "IN_PROGRESS", "RESOLVED", "DISMISSED"}


VALID_TYPES = {
    "ID_NO_COINCIDE",
    "FOLIO_NO_ENCONTRADO",
    "QR_INVALIDO",
    "QR_EXPIRADO",
    "DATOS_INCORRECTOS",
    "ALUMNO_YA_VALIDADO",
    "ALUMNO_YA_REGISTRADO",
    "TOKEN_INVALIDO",
    "TOKEN_YA_USADO",
    "TOKEN_REVOCADO",
    "TOKEN_EXPIRADO",
    "PROYECTO_INCORRECTO",
    "PROBLEMA_TECNICO",
    "OTRO"
}


def _get_current_incident_role(req):
    session_role = session.get("admin_user_role")
    if session_role in {ROLE_ADMIN, ROLE_STAFF}:
        return session_role

    legacy_role = require_role(req, {ROLE_ADMIN, ROLE_STAFF})
    if legacy_role:
        return legacy_role

    return None


def _get_current_admin_user_id():
    return session.get("admin_user_id")


def _normalize_status(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().upper()
    return value if value in VALID_STATUSES else None


def _normalize_severity(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().upper()
    return value if value in VALID_SEVERITIES else None


def _normalize_type(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().upper()
    return value if value in VALID_TYPES else None


@admin_incidents_bp.post("/api/incidents")
def create_incident():
    role = _get_current_incident_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401

    admin_user_id = _get_current_admin_user_id()

    payload = request.get_json(silent=True) or {}

    event_id = payload.get("event_id")
    request_id = payload.get("request_id")
    id_user = payload.get("id_user")
    incident_type = _normalize_type(payload.get("type"))
    severity = _normalize_severity(payload.get("severity")) or "MEDIUM"
    description = (payload.get("description") or "").strip() or None

    try:
        event_id = int(event_id)
    except:
        return jsonify({"error": "event_id es obligatorio y debe ser numérico"}), 400

    if request_id not in (None, ""):
        try:
            request_id = int(request_id)
        except:
            return jsonify({"error": "request_id debe ser numérico"}), 400
    else:
        request_id = None

    if id_user not in (None, ""):
        try:
            id_user = int(id_user)
        except:
            return jsonify({"error": "id_user debe ser numérico"}), 400
    else:
        id_user = None

    if not incident_type:
        return jsonify({"error": "type inválido o faltante"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            SELECT id
            FROM events
            WHERE id = %s
            LIMIT 1
            """,
            [event_id]
        )
        if not cur.fetchone():
            return {"error": "Evento no encontrado", "status": 404}

        if request_id is not None:
            cur.execute(
                """
                SELECT id
                FROM student_event_requests
                WHERE id = %s
                LIMIT 1
                """,
                [request_id]
            )
            if not cur.fetchone():
                return {"error": "Solicitud no encontrada", "status": 404}

        if id_user is not None:
            cur.execute(
                """
                SELECT id
                FROM users
                WHERE id = %s
                LIMIT 1
                """,
                [id_user]
            )
            if not cur.fetchone():
                return {"error": "Usuario no encontrado", "status": 404}

        cur.execute(
            """
            INSERT INTO incident_reports
            (
                event_id,
                request_id,
                id_user,
                reported_by_user_id,
                performed_by_admin_user_id,
                type,
                severity,
                status,
                description,
                created_at
            )
            VALUES (%s, %s, %s, NULL, %s, %s, %s, 'OPEN', %s, NOW())
            """,
            [
                event_id,
                request_id,
                id_user,
                admin_user_id,
                incident_type,
                severity,
                description
            ]
        )

        incident_id = cur.lastrowid

        cur.execute(
            """
            SELECT
                ir.id,
                ir.event_id,
                ir.request_id,
                ir.id_user,
                ir.reported_by_user_id,
                ir.performed_by_admin_user_id,
                ir.type,
                ir.severity,
                ir.status,
                ir.description,
                ir.resolution_notes,
                ir.created_at,
                ir.resolved_at
            FROM incident_reports ir
            WHERE ir.id = %s
            LIMIT 1
            """,
            [incident_id]
        )
        final_row = cur.fetchone()

        return {
            "status": 201,
            "message": "Caso reportado",
            "performed_by": {
                "role": role,
                "admin_user_id": admin_user_id
            },
            "incident": final_row
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


@admin_incidents_bp.get("/api/incidents")
def list_incidents():
    role = _get_current_incident_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401
    
    admin_user_id = _get_current_admin_user_id()

    event_id = request.args.get("event_id", type=int)
    status = _normalize_status(request.args.get("status"))
    severity = _normalize_severity(request.args.get("severity"))
    incident_type = _normalize_type(request.args.get("type"))

    where = []
    params = []

    if event_id:
        where.append("ir.event_id = %s")
        params.append(event_id)

    if status:
        where.append("ir.status = %s")
        params.append(status)

    if severity:
        where.append("ir.severity = %s")
        params.append(severity)

    if incident_type:
        where.append("ir.type = %s")
        params.append(incident_type)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    sql = f"""
        SELECT
            ir.id,
            ir.event_id,
            ir.request_id,
            ir.id_user,
            ir.reported_by_user_id,
            ir.performed_by_admin_user_id,
            ir.type,
            ir.severity,
            ir.status,
            ir.description,
            ir.resolution_notes,
            ir.created_at,
            ir.resolved_at
        FROM incident_reports ir
        {where_sql}
        ORDER BY
            CASE ir.status
                WHEN 'OPEN' THEN 1
                WHEN 'IN_PROGRESS' THEN 2
                WHEN 'RESOLVED' THEN 3
                WHEN 'DISMISSED' THEN 4
                ELSE 99
            END,
            ir.created_at DESC
        LIMIT 500
    """

    rows = fetch_all(sql, params)
    return jsonify({
        "performed_by": {
            "role": role,
            "admin_user_id": admin_user_id
        },
        "items": rows
    }), 200


@admin_incidents_bp.get("/api/incidents/<int:incident_id>")
def get_incident(incident_id: int):
    role = _get_current_incident_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401
    
    admin_user_id = _get_current_admin_user_id()

    sql = """
        SELECT
            ir.id,
            ir.event_id,
            ir.request_id,
            ir.id_user,
            ir.reported_by_user_id,
            ir.performed_by_admin_user_id,
            ir.type,
            ir.severity,
            ir.status,
            ir.description,
            ir.resolution_notes,
            ir.created_at,
            ir.resolved_at
        FROM incident_reports ir
        WHERE ir.id = %s
        LIMIT 1
    """

    row = fetch_one(sql, [incident_id])
    if not row:
        return jsonify({"error": "Caso no encontrado"}), 404

    return jsonify({
        "performed_by": {
            "role": role,
            "admin_user_id": admin_user_id
        },
        "incident": row
    }), 200


@admin_incidents_bp.patch("/api/incidents/<int:incident_id>")
def update_incident(incident_id: int):
    role = _get_current_incident_role(request)
    if not role:
        return jsonify({"error": "No autorizado"}), 401

    admin_user_id = _get_current_admin_user_id()
    payload = request.get_json(silent=True) or {}

    status = None
    severity = None

    if "status" in payload:
        status = _normalize_status(payload.get("status"))
        if not status:
            return jsonify({"error": "status inválido"}), 400

    if "severity" in payload:
        severity = _normalize_severity(payload.get("severity"))
        if not severity:
            return jsonify({"error": "severity inválido"}), 400

    resolution_notes = payload.get("resolution_notes")
    if resolution_notes is not None:
        resolution_notes = str(resolution_notes).strip() or None

    updates = []
    params = []

    if status is not None:
        updates.append("status = %s")
        params.append(status)

    if severity is not None:
        updates.append("severity = %s")
        params.append(severity)

    if "resolution_notes" in payload:
        updates.append("resolution_notes = %s")
        params.append(resolution_notes)

    if admin_user_id is not None:
        updates.append("performed_by_admin_user_id = %s")
        params.append(admin_user_id)

    if not updates:
        return jsonify({"error": "No hay cambios para aplicar"}), 400

    def tx(conn, cur):
        cur.execute(
            """
            SELECT id, status
            FROM incident_reports
            WHERE id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [incident_id]
        )
        row = cur.fetchone()
        if not row:
            return {"error": "Caso no encontrado", "status": 404}

        if status in ("RESOLVED", "DISMISSED"):
            updates_local = updates + ["resolved_at = NOW()"]
            params_local = params + [incident_id]
        else:
            updates_local = updates
            params_local = params + [incident_id]

        cur.execute(
            f"""
            UPDATE incident_reports
            SET {', '.join(updates_local)}
            WHERE id = %s
            """,
            params_local
        )

        cur.execute(
            """
            SELECT
                ir.id,
                ir.event_id,
                ir.request_id,
                ir.id_user,
                ir.reported_by_user_id,
                ir.performed_by_admin_user_id,
                ir.type,
                ir.severity,
                ir.status,
                ir.description,
                ir.resolution_notes,
                ir.created_at,
                ir.resolved_at
            FROM incident_reports ir
            WHERE ir.id = %s
            LIMIT 1
            """,
            [incident_id]
        )
        final_row = cur.fetchone()

        return {
            "status": 200,
            "message": "Caso actualizado",
            "performed_by": {
                "role": role,
                "admin_user_id": admin_user_id
            },
            "incident": final_row
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