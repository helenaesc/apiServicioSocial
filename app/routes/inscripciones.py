from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database import execute_tx

inscripciones_bp = Blueprint("inscripciones", __name__)

@inscripciones_bp.post("/api/enrolments")
def create_enrolment():
    payload = request.get_json(silent=True) or {}

    id_student = payload.get("id_student") 
    id_project = payload.get("id_project") 
    token_value = payload.get("token")

    if not id_student or not id_project:
        return jsonify({"error": "id_student/id_alumno e id_project/id_proyecto son obligatorios"}), 400

    # Token obligatorio
    if not token_value:
        return jsonify({"error": "token es obligatorio (1 token = 1 cupo)"}), 400

    def tx(conn, cur):
        # validar que exista el projecto
        cur.execute("SELECT id FROM project WHERE id=%s LIMIT 1", [id_project])
        if not cur.fetchone():
            return {"error": "Proyecto no encontrado", "status": 404}

        # un alumno requiere token
        cur.execute(
            "SELECT id FROM enrolment WHERE id_student=%s LIMIT 1 FOR UPDATE",
            [id_student],
        )
        if cur.fetchone():
            return {"error": "El alumno ya tiene una inscripción activa", "status": 409}

        cur.execute(
            """
            SELECT id, id_project, used
            FROM token
            WHERE token=%s
            LIMIT 1
            FOR UPDATE
            """,
            [token_value],
        )
        tk = cur.fetchone()
        if not tk:
            return {"error": "Token no existe", "status": 400}
        if tk["used"]:
            return {"error": "Token ya fue utilizado", "status": 409}
        if tk["id_project"] is None or int(tk["id_project"]) != int(id_project):
            return {"error": "Token no corresponde al proyecto", "status": 400}

        # Status pendiente
        cur.execute("SELECT id FROM status WHERE LOWER(name)='pendiente' LIMIT 1")
        st = cur.fetchone()
        status_id = st["id"] if st else None

        # Resgistros finales
        cur.execute(
            """
            INSERT INTO enrolment (id_student, id_project, id_status, id_token)
            VALUES (%s, %s, %s, %s)
            """,
            [id_student, id_project, status_id, tk["id"]],
        )
        enrolment_id = cur.lastrowid

        # Consumir el cupo para mantenerlo como un uso
        cur.execute(
            "UPDATE token SET used=TRUE WHERE id=%s AND used=FALSE",
            [tk["id"]],
        )

        return {"id": enrolment_id, "message": "Inscripción creada", "status": 201}

    try:
        result = execute_tx(tx)

        if isinstance(result, dict) and result.get("status") != 201:
            return jsonify({"error": result["error"]}), result["status"]

        return jsonify({"id": result["id"], "message": result["message"]}), 201

    except Error as e:
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500