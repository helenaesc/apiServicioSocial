from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx

inscripciones_bp = Blueprint("inscripciones", __name__)

def create_inscripcion():
    payload = request.get_json(silent=True) or {}

    id_alumno = payload.get("id_alumno")
    id_proyecto = payload.get("id_proyecto")
    token_value = payload.get("token")  # opcional, string

    if not id_alumno or not id_proyecto:
        return jsonify({"error": "id_alumno e id_proyecto son obligatorios"}), 400

    def tx(conn, cur):
        # Validar proyecto y cupos disponibles (lock del registro de proyecto para evitar sobrecupo)
        cur.execute(
            """
            SELECT p.id, p.cupos,
                   GREATEST(p.cupos - COALESCE(SUM(CASE WHEN st.name = 'Rechazado' THEN 0 ELSE 1 END), 0), 0) AS disponibles
            FROM project p
            LEFT JOIN inscripcion i ON i.id_proyecto = p.id
            LEFT JOIN status st ON st.id = i.id_status
            WHERE p.id = %s
            GROUP BY p.id, p.cupos
            FOR UPDATE
            """,
            [id_proyecto],
        )
        project = cur.fetchone()
        if not project:
            return {"error": "Proyecto no encontrado", "status": 404}
        if int(project["disponibles"] or 0) <= 0:
            return {"error": "No hay cupos disponibles", "status": 409}

        # Evitar inscripción duplicada por alumno-proyecto (si quieres permitir reinscripción, quita esta validación)
        cur.execute(
            "SELECT id FROM inscripcion WHERE id_alumno = %s AND id_proyecto = %s LIMIT 1",
            [id_alumno, id_proyecto],
        )
        existing = cur.fetchone()
        if existing:
            return {"error": "El alumno ya está inscrito en este proyecto", "status": 409}

        # Obtener status Pendiente
        cur.execute("SELECT id FROM status WHERE name = 'Pendiente' LIMIT 1")
        st = cur.fetchone()
        status_id = st["id"] if st else None

        token_id = None
        if token_value:
            cur.execute(
                "SELECT id, used, id_proyecto FROM token WHERE token = %s LIMIT 1 FOR UPDATE",
                [token_value],
            )
            tk = cur.fetchone()
            if not tk:
                return {"error": "Token no existe", "status": 400}
            if tk["used"]:
                return {"error": "Token ya fue utilizado", "status": 409}
            if tk["id_proyecto"] is not None and int(tk["id_proyecto"]) != int(id_proyecto):
                return {"error": "Token no corresponde al proyecto", "status": 400}
            token_id = tk["id"]

        cur.execute(
            """
            INSERT INTO inscripcion (id_alumno, id_proyecto, id_status, id_token)
            VALUES (%s, %s, %s, %s)
            """,
            [id_alumno, id_proyecto, status_id, token_id],
        )
        new_id = cur.lastrowid

        if token_id:
            cur.execute("UPDATE token SET used = TRUE WHERE id = %s", [token_id])

        return {"id": new_id, "message": "Inscripción creada", "status": 201}

    try:
        result = execute_tx(tx)
        if isinstance(result, dict) and "status" in result and result["status"] != 201:
            return jsonify({"error": result["error"]}), result["status"]
        return jsonify({"id": result["id"], "message": result["message"]}), 201
    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
