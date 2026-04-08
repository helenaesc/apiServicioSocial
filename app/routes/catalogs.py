from flask import Blueprint, jsonify, request
from ..database import fetch_all, fetch_one

catalogs_bp = Blueprint("catalogs", __name__)


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


def _get_visible_event(season: str):
    sql = """
        SELECT
            id,
            year,
            season,
            display_name,
            status
        FROM events
        WHERE season = %s
          AND is_visible_to_students = TRUE
          AND status IN ('VISIBLE', 'ONSITE')
        ORDER BY year DESC, id DESC
        LIMIT 1
    """
    return fetch_one(sql, [season])


@catalogs_bp.get("/api/catalogs")
def catalogs():
    raw_season = request.args.get("temporada") or request.args.get("season")
    season = _normalize_season(raw_season)

    if not season:
        return jsonify({"error": "Temporada inválida o faltante"}), 400

    event_row = _get_visible_event(season)
    if not event_row:
        return jsonify({"error": "No hay temporada visible para estudiantes"}), 404

    socio_sql = """
        SELECT DISTINCT pa.id, pa.name
        FROM event_projects ep
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN partner pa ON pa.id = p.id_partner
        WHERE ep.event_id = %s
          AND ep.status = 'ACTIVE'
          AND pa.id IS NOT NULL
        ORDER BY pa.name
    """

    dias_sql = """
        SELECT DISTINCT wd.id, wd.name AS description
        FROM event_projects ep
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN week_days wd ON wd.id = p.id_week_days
        WHERE ep.event_id = %s
          AND ep.status = 'ACTIVE'
          AND wd.id IS NOT NULL
        ORDER BY wd.id
    """

    modalidad_sql = """
        SELECT DISTINCT m.id, m.name AS description
        FROM event_projects ep
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN modality m ON m.id = p.id_modality
        WHERE ep.event_id = %s
          AND ep.status = 'ACTIVE'
          AND m.id IS NOT NULL
        ORDER BY m.id
    """

    horario_sql = """
        SELECT DISTINCT sc.id, sc.name AS description
        FROM event_projects ep
        JOIN project p ON p.id = ep.project_id
        LEFT JOIN schedule sc ON sc.id = p.id_schedule
        WHERE ep.event_id = %s
          AND ep.status = 'ACTIVE'
          AND sc.id IS NOT NULL
        ORDER BY sc.id
    """

    return jsonify({
        "event": {
            "id": event_row["id"],
            "year": event_row["year"],
            "season": event_row["season"],
            "display_name": event_row["display_name"],
            "status": event_row["status"],
        },
        "socio": fetch_all(socio_sql, [event_row["id"]]),
        "dias": fetch_all(dias_sql, [event_row["id"]]),
        "modalidad": fetch_all(modalidad_sql, [event_row["id"]]),
        "horario": fetch_all(horario_sql, [event_row["id"]]),
    })