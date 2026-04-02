from flask import Blueprint, jsonify, request
from ..database import fetch_all, fetch_one

projects_bp = Blueprint("projects", __name__)


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
    """
    Busca el evento visible para estudiantes de la temporada solicitada.
    Si por error hay más de uno visible, toma el más reciente.
    """
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


@projects_bp.get("/api/projects")
def list_projects():
    raw_season = request.args.get("temporada") or request.args.get("season")
    season = _normalize_season(raw_season)

    if not season:
        return jsonify({"error": "Temporada inválida o faltante"}), 400

    event_row = _get_visible_event(season)
    if not event_row:
        return jsonify({"error": "No hay temporada visible para estudiantes"}), 404

    event_id = event_row["id"]

    q = request.args.get("q", "").strip()
    socio = request.args.get("socio", type=int)
    modalidad = request.args.get("modalidad", type=int)
    dia = request.args.get("dia", type=int)
    horario = request.args.get("horario", type=int)

    where = ["ep.event_id = %s", "ep.status = 'ACTIVE'"]
    params = [event_id]

    if q:
        where.append("(p.name LIKE %s OR p.schedule_description LIKE %s OR p.team_owners LIKE %s)")
        like = f"%{q}%"
        params.extend([like, like, like])

    if socio:
        where.append("p.id_partner = %s")
        params.append(socio)

    if modalidad:
        where.append("p.id_modality = %s")
        params.append(modalidad)

    if dia:
        where.append("p.id_week_days = %s")
        params.append(dia)

    if horario:
        where.append("p.id_schedule = %s")
        params.append(horario)

    where_sql = " AND ".join(where)

    sql = f"""
        SELECT
            p.id,
            p.general_name,
            ep.id AS event_project_id,
            ev.id AS event_id,
            ev.display_name AS temporada,
            p.name,
            ep.slots_total AS cupos,
            p.schedule_description AS descripcion_horario,
            p.team_owners,
            p.objectives,
            p.activities,
            p.clave,
            p.competencies,
            p.location,
            p.duration,
            p.audience,
            p.max_hours,
            p.comments,
            pa.name AS socio,
            m.name AS modalidad,
            wd.name AS dia,
            sc.name AS horario,

            (
              SELECT COUNT(*)
              FROM registrations r
              WHERE r.event_project_id = ep.id
                AND r.status = 'ACTIVE'
            ) AS inscritos,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
            ) AS tokens_total,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
                AND pt.status = 'AVAILABLE'
                AND (pt.expires_at IS NULL OR pt.expires_at > NOW())
            ) AS tokens_disponibles

        FROM event_projects ep
        JOIN events ev ON ev.id = ep.event_id
        JOIN project p ON p.id = ep.project_id
        JOIN partner pa ON pa.id = p.id_partner
        JOIN modality m ON m.id = p.id_modality
        JOIN week_days wd ON wd.id = p.id_week_days
        JOIN schedule sc ON sc.id = p.id_schedule
        WHERE {where_sql}
        ORDER BY p.name
    """

    rows = fetch_all(sql, params)

    for r in rows:
        tokens_total = int(r.get("tokens_total") or 0)
        inscritos = int(r.get("inscritos") or 0)
        cupos = int(r.get("cupos") or 0)
        tokens_disponibles = int(r.get("tokens_disponibles") or 0)

        if tokens_total > 0:
            r["cupos_disponibles"] = tokens_disponibles
        else:
            r["cupos_disponibles"] = max(cupos - inscritos, 0)

    return jsonify({
        "event": {
            "id": event_row["id"],
            "year": event_row["year"],
            "season": event_row["season"],
            "display_name": event_row["display_name"],
            "status": event_row["status"],
        },
        "items": rows
    })


@projects_bp.get("/api/projects/<int:project_id>")
def get_project(project_id: int):
    raw_season = request.args.get("temporada") or request.args.get("season")
    season = _normalize_season(raw_season)

    if not season:
        return jsonify({"error": "Temporada inválida o faltante"}), 400

    event_row = _get_visible_event(season)
    if not event_row:
        return jsonify({"error": "No hay temporada visible para estudiantes"}), 404

    event_id = event_row["id"]

    sql = """
        SELECT
            p.id,
            p.general_name,
            ep.id AS event_project_id,
            ev.id AS event_id,
            ev.display_name AS temporada,
            p.name,
            ep.slots_total AS cupos,
            p.schedule_description AS descripcion_horario,
            p.team_owners,
            p.objectives,
            p.activities,
            p.clave,
            p.competencies,
            p.location,
            p.duration,
            p.audience,
            p.max_hours,
            p.comments,
            pa.id AS socio_id,
            pa.name AS socio,
            m.id AS modalidad_id,
            m.name AS modalidad,
            wd.id AS dia_id,
            wd.name AS dia,
            sc.id AS horario_id,
            sc.name AS horario,

            (
              SELECT COUNT(*)
              FROM registrations r
              WHERE r.event_project_id = ep.id
                AND r.status = 'ACTIVE'
            ) AS inscritos,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
            ) AS tokens_total,

            (
              SELECT COUNT(*)
              FROM project_tokens pt
              WHERE pt.event_project_id = ep.id
                AND pt.status = 'AVAILABLE'
                AND (pt.expires_at IS NULL OR pt.expires_at > NOW())
            ) AS tokens_disponibles

        FROM event_projects ep
        JOIN events ev ON ev.id = ep.event_id
        JOIN project p ON p.id = ep.project_id
        JOIN partner pa ON pa.id = p.id_partner
        JOIN modality m ON m.id = p.id_modality
        JOIN week_days wd ON wd.id = p.id_week_days
        JOIN schedule sc ON sc.id = p.id_schedule
        WHERE ep.event_id = %s
          AND ep.status = 'ACTIVE'
          AND p.id = %s
        LIMIT 1
    """

    row = fetch_one(sql, [event_id, project_id])
    if not row:
        return jsonify({"error": "Proyecto no encontrado en la temporada seleccionada"}), 404

    tokens_total = int(row.get("tokens_total") or 0)
    inscritos = int(row.get("inscritos") or 0)
    cupos = int(row.get("cupos") or 0)
    tokens_disponibles = int(row.get("tokens_disponibles") or 0)

    if tokens_total > 0:
        row["cupos_disponibles"] = tokens_disponibles
    else:
        row["cupos_disponibles"] = max(cupos - inscritos, 0)

    return jsonify({
        "event": {
            "id": event_row["id"],
            "year": event_row["year"],
            "season": event_row["season"],
            "display_name": event_row["display_name"],
            "status": event_row["status"],
        },
        "item": row
    })