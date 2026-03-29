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

    return jsonify({
        "event": {
            "id": event_row["id"],
            "year": event_row["year"],
            "season": event_row["season"],
            "display_name": event_row["display_name"],
            "status": event_row["status"],
        },
        "socio": fetch_all("SELECT id, name FROM partner ORDER BY name"),
        "dias": fetch_all("SELECT id, name AS description FROM week_days ORDER BY id"),
        "modalidad": fetch_all("SELECT id, name AS description FROM modality ORDER BY id"),
        "horario": fetch_all("SELECT id, name AS description FROM schedule ORDER BY id"),
        "status": fetch_all("SELECT id, name FROM status ORDER BY id"),
        "partner_group": fetch_all("SELECT id, name FROM partner_group ORDER BY name"),
    })