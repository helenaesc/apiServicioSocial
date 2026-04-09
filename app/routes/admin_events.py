from flask import Blueprint, jsonify, request, session
from mysql.connector import Error
from ..database import execute_tx, fetch_all, fetch_one
from ..authz import require_role, ROLE_ADMIN

admin_events_bp = Blueprint("admin_events", __name__)

def _get_current_admin_role(req):
    session_role = session.get("admin_user_role")
    if session_role == ROLE_ADMIN:
        return session_role

    legacy_role = require_role(req, {ROLE_ADMIN})
    if legacy_role:
        return legacy_role

    return None


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

VALID_SEASONS = {"PRIMAVERA", "INVIERNO"}
VALID_STATUSES = {"DRAFT", "VISIBLE", "ONSITE", "CLOSED", "ARCHIVED"}


def _normalize_season(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().upper()
    mapping = {
        "PRIMAVERA": "PRIMAVERA",
        "SPRING": "PRIMAVERA",
        "INVIERNO": "INVIERNO",
        "WINTER": "INVIERNO",
    }
    return mapping.get(value)


def _normalize_status(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().upper()
    return value if value in VALID_STATUSES else None


def _build_display_name(year: int, season: str) -> str:
    season_title = "Primavera" if season == "PRIMAVERA" else "Invierno"
    return f"{season_title} {year}"


@admin_events_bp.get("/api/admin/events")
def list_events():
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    year = request.args.get("year", type=int)
    season = _normalize_season(request.args.get("season"))
    status = _normalize_status(request.args.get("status"))

    where = []
    params = []

    if year:
        where.append("year = %s")
        params.append(year)

    if season:
        where.append("season = %s")
        params.append(season)

    if status:
        where.append("status = %s")
        params.append(status)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    sql = f"""
        SELECT
            id,
            year,
            season,
            display_name,
            catalog_open_at,
            onsite_start_at,
            onsite_end_at,
            registration_close_at,
            status,
            is_visible_to_students,
            created_at,
            updated_at
        FROM events
        {where_sql}
        ORDER BY year DESC,
                 FIELD(season, 'PRIMAVERA', 'INVIERNO'),
                 id DESC
    """

    rows = fetch_all(sql, params)
    return jsonify(rows), 200


@admin_events_bp.get("/api/admin/events/<int:event_id>")
def get_event(event_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    sql = """
        SELECT
            id,
            year,
            season,
            display_name,
            catalog_open_at,
            onsite_start_at,
            onsite_end_at,
            registration_close_at,
            status,
            is_visible_to_students,
            created_at,
            updated_at
        FROM events
        WHERE id = %s
        LIMIT 1
    """
    row = fetch_one(sql, [event_id])

    if not row:
        return jsonify({"error": "Temporada no encontrada"}), 404

    return jsonify(row), 200


@admin_events_bp.post("/api/admin/events")
def create_event():
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}

    year = payload.get("year")
    season = _normalize_season(payload.get("season"))
    catalog_open_at = payload.get("catalog_open_at")
    onsite_start_at = payload.get("onsite_start_at")
    onsite_end_at = payload.get("onsite_end_at")
    registration_close_at = payload.get("registration_close_at")
    status = _normalize_status(payload.get("status")) or "DRAFT"
    is_visible_to_students = bool(payload.get("is_visible_to_students", False))

    try:
        year = int(year)
        if year < 2020 or year > 2100:
            return jsonify({"error": "year debe estar entre 2020 y 2100"}), 400
    except:
        return jsonify({"error": "year es obligatorio y debe ser numérico"}), 400

    if not season:
        return jsonify({"error": "season debe ser PRIMAVERA o INVIERNO"}), 400

    if status not in VALID_STATUSES:
        return jsonify({"error": "status inválido"}), 400

    display_name = _build_display_name(year, season)

    def tx(conn, cur):
        cur.execute(
            """
            SELECT id
            FROM events
            WHERE year = %s AND season = %s
            LIMIT 1
            FOR UPDATE
            """,
            [year, season]
        )
        if cur.fetchone():
            return {"error": "Ya existe esa temporada para ese año", "status": 409}

        if is_visible_to_students:
            cur.execute(
                """
                UPDATE events
                SET is_visible_to_students = FALSE
                WHERE is_visible_to_students = TRUE
                """
            )

        cur.execute(
            """
            INSERT INTO events
            (
                year, season, display_name,
                catalog_open_at, onsite_start_at, onsite_end_at, registration_close_at,
                status, is_visible_to_students
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            [
                year, season, display_name,
                catalog_open_at, onsite_start_at, onsite_end_at, registration_close_at,
                status, is_visible_to_students
            ]
        )

        event_id = cur.lastrowid

        return {
            "status": 201,
            "id": event_id,
            "display_name": display_name
        }

    try:
        result = execute_tx(tx)

        if result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({
            "message": "Temporada creada",
            "performed_by": {
                "role": role
            },
            "id": result["id"],
            "display_name": result["display_name"]
        }), 201

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_events_bp.patch("/api/admin/events/<int:event_id>")
def update_event(event_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    payload = request.get_json(silent=True) or {}

    allowed_fields = {
        "catalog_open_at",
        "onsite_start_at",
        "onsite_end_at",
        "registration_close_at",
        "status",
        "is_visible_to_students",
    }

    if not payload:
        return jsonify({"error": "No se enviaron cambios"}), 400

    unknown = [k for k in payload.keys() if k not in allowed_fields]
    if unknown:
        return jsonify({"error": f"Campos no permitidos: {', '.join(unknown)}"}), 400

    status = None
    if "status" in payload:
        status = _normalize_status(payload.get("status"))
        if not status:
            return jsonify({"error": "status inválido"}), 400

    is_visible_to_students = None
    if "is_visible_to_students" in payload:
        is_visible_to_students = bool(payload.get("is_visible_to_students"))

    def tx(conn, cur):
        cur.execute(
            """
            SELECT id, year, season, display_name, status, is_visible_to_students
            FROM events
            WHERE id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [event_id]
        )
        row = cur.fetchone()
        if not row:
            return {"error": "Temporada no encontrada", "status": 404}

        updates = []
        params = []

        for field in ("catalog_open_at", "onsite_start_at", "onsite_end_at", "registration_close_at"):
            if field in payload:
                updates.append(f"{field} = %s")
                params.append(payload.get(field))

        if status is not None:
            updates.append("status = %s")
            params.append(status)

        if is_visible_to_students is not None:
            if is_visible_to_students:
                cur.execute(
                    """
                    UPDATE events
                    SET is_visible_to_students = FALSE
                    WHERE is_visible_to_students = TRUE
                      AND id <> %s
                    """,
                    [event_id]
                )
            updates.append("is_visible_to_students = %s")
            params.append(is_visible_to_students)

        if not updates:
            return {"error": "No hay cambios válidos para aplicar", "status": 400}

        params.append(event_id)

        cur.execute(
            f"""
            UPDATE events
            SET {', '.join(updates)}
            WHERE id = %s
            """,
            params
        )

        return {"status": 200, "message": "Temporada actualizada"}

    try:
        result = execute_tx(tx)

        if result.get("status") != 200:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({
            "message": result["message"],
            "performed_by": {
                "role": role
            }
        }), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_events_bp.put("/api/admin/events/<int:event_id>/visible")
def set_visible_event(event_id: int):
    role = _get_current_admin_role(request)
    if not role:
        return jsonify({"error": "No autorizado (solo ADMIN)"}), 401

    def tx(conn, cur):
        cur.execute(
            """
            SELECT id, status
            FROM events
            WHERE id = %s
            LIMIT 1
            FOR UPDATE
            """,
            [event_id]
        )
        row = cur.fetchone()
        if not row:
            return {"error": "Temporada no encontrada", "status": 404}

        if row["status"] not in ("VISIBLE", "ONSITE"):
            return {
                "error": "Solo se puede marcar visible una temporada en estado VISIBLE u ONSITE",
                "status": 409
            }

        cur.execute("UPDATE events SET is_visible_to_students = FALSE WHERE is_visible_to_students = TRUE")
        cur.execute("UPDATE events SET is_visible_to_students = TRUE WHERE id = %s", [event_id])

        return {"status": 200, "message": "Temporada visible actualizada"}

    try:
        result = execute_tx(tx)

        if result.get("status") != 200:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({
            "message": result["message"],
            "performed_by": {
                "role": role
            }
        }), 200

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500