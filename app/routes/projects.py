from flask import Blueprint, jsonify, request
from ..database import fetch_all, fetch_one

projects_bp = Blueprint("projects", __name__)

@projects_bp.get("/api/projects")
def list_projects():
    q = request.args.get("q", "").strip()
    socio = request.args.get("socio", type=int)        # partner
    modalidad = request.args.get("modalidad", type=int) # modality
    dia = request.args.get("dia", type=int)            # week_days
    horario = request.args.get("horario", type=int)    # schedule

    where = []
    params = []

    if q:
        where.append("(p.name LIKE %s OR p.project_description LIKE %s OR p.schedule_description LIKE %s)")
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

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    sql = f"""
        SELECT
            p.id,
            p.name,
            p.slots AS cupos,
            p.project_description AS descripcion,
            p.schedule_description AS descripcion_horario,
            p.team_owners,
            p.carreer,
            p.objectives,
            p.activities,
            p.clave,
            p.competencies,
            p.location,
            p.duration,
            p.audience,
            p.max_hours,
            p.comments,
            p.season,
            pa.name AS socio,
            m.name AS modalidad,
            wd.name AS dia,
            sc.name AS horario,

            -- inscritos (todo excepto rechazado)
            (
              SELECT COUNT(*)
              FROM enrolment e
              LEFT JOIN status st ON st.id = e.id_status
              WHERE e.id_project = p.id
                AND (st.name IS NULL OR LOWER(st.name) <> 'rechazado')
            ) AS inscritos,

            -- tokens totales y disponibles
            (SELECT COUNT(*) FROM token t WHERE t.id_project = p.id) AS tokens_total,
            (SELECT COUNT(*) FROM token t WHERE t.id_project = p.id AND t.used = FALSE) AS tokens_disponibles

        FROM project p
        JOIN partner pa ON pa.id = p.id_partner
        JOIN modality m ON m.id = p.id_modality
        JOIN week_days wd ON wd.id = p.id_week_days
        JOIN schedule sc ON sc.id = p.id_schedule
        {where_sql}
        ORDER BY p.name
    """

    rows = fetch_all(sql, params)

    for r in rows:
        tokens_total = int(r.get("tokens_total") or 0)
        if tokens_total > 0:
            r["cupos_disponibles"] = int(r.get("tokens_disponibles") or 0)
        else:
            r["cupos_disponibles"] = max(int(r["cupos"]) - int(r["inscritos"]), 0)

    return jsonify(rows)


@projects_bp.get("/api/projects/<int:project_id>")
def get_project(project_id: int):
    sql = """
        SELECT
            p.id,
            p.name,
            p.slots AS cupos,
            p.project_description AS descripcion,
            p.schedule_description AS descripcion_horario,
            p.team_owners,
            p.carreer,
            p.objectives,
            p.activities,
            p.clave,
            p.competencies,
            p.location,
            p.duration,
            p.audience,
            p.max_hours,
            p.comments,
            p.season,
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
              FROM enrolment e
              LEFT JOIN status st ON st.id = e.id_status
              WHERE e.id_project = p.id
                AND (st.name IS NULL OR LOWER(st.name) <> 'rechazado')
            ) AS inscritos,

            (SELECT COUNT(*) FROM token t WHERE t.id_project = p.id) AS tokens_total,
            (SELECT COUNT(*) FROM token t WHERE t.id_project = p.id AND t.used = FALSE) AS tokens_disponibles

        FROM project p
        JOIN partner pa ON pa.id = p.id_partner
        JOIN modality m ON m.id = p.id_modality
        JOIN week_days wd ON wd.id = p.id_week_days
        JOIN schedule sc ON sc.id = p.id_schedule
        WHERE p.id = %s
        LIMIT 1
    """
    row = fetch_one(sql, [project_id])
    if not row:
        return jsonify({"error": "Proyecto no encontrado"}), 404

    tokens_total = int(row.get("tokens_total") or 0)
    if tokens_total > 0:
        row["cupos_disponibles"] = int(row.get("tokens_disponibles") or 0)
    else:
        row["cupos_disponibles"] = max(int(row["cupos"]) - int(row["inscritos"]), 0)

    return jsonify(row)