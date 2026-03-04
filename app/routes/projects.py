from flask import Blueprint, jsonify, request
from ..database import fetch_all, fetch_one

projects_bp = Blueprint("projects", __name__)

def list_projects():
    q = request.args.get("q", "").strip()
    socio = request.args.get("socio", type=int)
    modalidad = request.args.get("modalidad", type=int)
    dia = request.args.get("dia", type=int)
    horario = request.args.get("horario", type=int)
    only_available = request.args.get("only_available", "false").lower() in {"1", "true", "yes"}

    where = []
    params = []

    if q:
        where.append("(p.name LIKE %s OR p.descripcion LIKE %s OR p.descripcion_horario LIKE %s)")
        like = f"%{q}%"
        params.extend([like, like, like])
    if socio:
        where.append("p.id_socio = %s")
        params.append(socio)
    if modalidad:
        where.append("p.id_modalidad = %s")
        params.append(modalidad)
    if dia:
        where.append("p.id_dias = %s")
        params.append(dia)
    if horario:
        where.append("p.id_horario = %s")
        params.append(horario)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    # Nota: contamos inscripciones activas (todo excepto Rechazado). Si id_status es NULL, se considera activa.
    sql = f"""
        SELECT
            p.id,
            p.name,
            p.cupos,
            p.descripcion,
            p.descripcion_horario,
            s.name AS socio,
            m.description AS modalidad,
            d.description AS dia,
            h.description AS horario,
            COALESCE(SUM(CASE WHEN st.name = 'Rechazado' THEN 0 ELSE 1 END), 0) AS inscritos,
            GREATEST(p.cupos - COALESCE(SUM(CASE WHEN st.name = 'Rechazado' THEN 0 ELSE 1 END), 0), 0) AS cupos_disponibles
        FROM project p
        INNER JOIN socio s ON s.id = p.id_socio
        INNER JOIN modalidad m ON m.id = p.id_modalidad
        INNER JOIN dias d ON d.id = p.id_dias
        INNER JOIN horario h ON h.id = p.id_horario
        LEFT JOIN inscripcion i ON i.id_proyecto = p.id
        LEFT JOIN status st ON st.id = i.id_status
        {where_sql}
        GROUP BY p.id, p.name, p.cupos, p.descripcion, p.descripcion_horario, s.name, m.description, d.description, h.description
    """

    rows = fetch_all(sql, params)
    if only_available:
        rows = [r for r in rows if (r.get("cupos_disponibles") or 0) > 0]
    return jsonify(rows)


def get_project(project_id: int):
    sql = """
        SELECT
            p.id,
            p.name,
            p.cupos,
            p.descripcion,
            p.descripcion_horario,
            s.id AS socio_id,
            s.name AS socio,
            m.id AS modalidad_id,
            m.description AS modalidad,
            d.id AS dia_id,
            d.description AS dia,
            h.id AS horario_id,
            h.description AS horario,
            COALESCE(SUM(CASE WHEN st.name = 'Rechazado' THEN 0 ELSE 1 END), 0) AS inscritos,
            GREATEST(p.cupos - COALESCE(SUM(CASE WHEN st.name = 'Rechazado' THEN 0 ELSE 1 END), 0), 0) AS cupos_disponibles
        FROM project p
        INNER JOIN socio s ON s.id = p.id_socio
        INNER JOIN modalidad m ON m.id = p.id_modalidad
        INNER JOIN dias d ON d.id = p.id_dias
        INNER JOIN horario h ON h.id = p.id_horario
        LEFT JOIN inscripcion i ON i.id_proyecto = p.id
        LEFT JOIN status st ON st.id = i.id_status
        WHERE p.id = %s
        GROUP BY p.id, p.name, p.cupos, p.descripcion, p.descripcion_horario,
                 s.id, s.name, m.id, m.description, d.id, d.description, h.id, h.description
    """
    row = fetch_one(sql, [project_id])
    if not row:
        return jsonify({"error": "Proyecto no encontrado"}), 404
    return jsonify(row)