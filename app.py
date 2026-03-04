import os
from datetime import datetime
from flask import Flask, jsonify, request, render_template_string
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# -----------------------------
# Configuración de BD (MySQL)
# -----------------------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "poncho"),
    "autocommit": False,
}


def get_conn():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(sql, params=None):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or [])
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()


def fetch_one(sql, params=None):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or [])
        row = cur.fetchone()
        return row
    finally:
        cur.close()
        conn.close()


def execute_tx(statements_fn):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        result = statements_fn(conn, cur)
        conn.commit()
        return result
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


# -----------------------------
# HTML (catálogo simple)
# -----------------------------
INDEX_HTML = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Catálogo de Proyectos</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f5f7fb; color: #1f2937; }
    header { background: #0f172a; color: white; padding: 16px 20px; }
    .container { max-width: 1100px; margin: 20px auto; padding: 0 16px; }
    .filters { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; background: white; padding: 14px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,.05); }
    input, select, button { padding: 10px; border-radius: 8px; border: 1px solid #cbd5e1; }
    button { background: #0ea5e9; color: white; border: none; cursor: pointer; }
    button:hover { opacity: .95; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 14px; margin-top: 16px; }
    .card { background: white; padding: 14px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,.05); }
    .title { font-size: 1.05rem; font-weight: 700; margin-bottom: 6px; }
    .meta { font-size: .9rem; color: #475569; line-height: 1.45; }
    .desc { font-size: .92rem; margin-top: 8px; color: #334155; }
    .pill { display: inline-block; margin-top: 8px; background: #e2e8f0; color: #0f172a; padding: 3px 8px; border-radius: 999px; font-size: .8rem; }
    .empty { padding: 20px; background: white; border-radius: 12px; margin-top: 16px; }
    .footer { color: #64748b; font-size: .8rem; margin-top: 20px; }
    .row { display:flex; gap:8px; align-items:center; flex-wrap: wrap; }
  </style>
</head>
<body>
  <header>
    <h2 style="margin:0;">Catálogo de Proyectos (Poncho)</h2>
  </header>

  <div class="container">
    <div class="filters">
      <input id="q" placeholder="Buscar por proyecto o descripción">
      <select id="socio"><option value="">Socio (todos)</option></select>
      <select id="modalidad"><option value="">Modalidad (todas)</option></select>
      <select id="dia"><option value="">Día (todos)</option></select>
      <select id="horario"><option value="">Horario (todos)</option></select>
      <div class="row">
        <button onclick="loadProjects()">Buscar</button>
        <button onclick="clearFilters()" style="background:#64748b;">Limpiar</button>
      </div>
    </div>

    <div id="results"></div>
    <div class="footer">Este catálogo consume <code>/api/projects</code> y catálogos de apoyo desde <code>/api/catalogs</code>.</div>
  </div>

  <script>
    async function getJSON(url) {
      const r = await fetch(url);
      if (!r.ok) throw new Error('Error ' + r.status);
      return r.json();
    }

    function fillSelect(id, items, labelKey='description') {
      const el = document.getElementById(id);
      const first = el.innerHTML;
      el.innerHTML = first;
      for (const item of items) {
        const opt = document.createElement('option');
        opt.value = item.id;
        opt.textContent = item[labelKey];
        el.appendChild(opt);
      }
    }

    async function loadCatalogs() {
      const data = await getJSON('/api/catalogs');
      fillSelect('socio', data.socio, 'name');
      fillSelect('modalidad', data.modalidad);
      fillSelect('dia', data.dias);
      fillSelect('horario', data.horario);
    }

    function card(p) {
      const desc = p.descripcion || '';
      const dh = p.descripcion_horario ? <div class="desc"><strong>Detalle horario:</strong> ${p.descripcion_horario}</div> : '';
      return `
        <div class="card">
          <div class="title">${p.name}</div>
          <div class="meta">
            <div><strong>Socio:</strong> ${p.socio}</div>
            <div><strong>Modalidad:</strong> ${p.modalidad}</div>
            <div><strong>Día:</strong> ${p.dia}</div>
            <div><strong>Horario:</strong> ${p.horario}</div>
            <div><strong>Cupos:</strong> ${p.cupos} | <strong>Inscritos:</strong> ${p.inscritos} | <strong>Disponibles:</strong> ${p.cupos_disponibles}</div>
          </div>
          ${desc ? <div class="desc">${desc}</div> : ''}
          ${dh}
          ${p.cupos_disponibles > 0 ? '<span class="pill">Disponible</span>' : '<span class="pill">Sin cupo</span>'}
        </div>`;
    }

    async function loadProjects() {
      const params = new URLSearchParams();
      for (const id of ['q','socio','modalidad','dia','horario']) {
        const v = document.getElementById(id).value.trim();
        if (v) params.set(id, v);
      }
      const data = await getJSON('/api/projects?' + params.toString());
      const root = document.getElementById('results');
      if (!data.length) {
        root.innerHTML = '<div class="empty">No se encontraron proyectos con esos filtros.</div>';
        return;
      }
      root.innerHTML = <div class="grid">${data.map(card).join('')}</div>;
    }

    function clearFilters() {
      ['q','socio','modalidad','dia','horario'].forEach(id => document.getElementById(id).value = '');
      loadProjects();
    }

    (async () => {
      try {
        await loadCatalogs();
        await loadProjects();
      } catch (e) {
        document.getElementById('results').innerHTML = <div class="empty">Error cargando catálogo: ${e.message}</div>;
      }
    })();
  </script>
</body>
</html>
"""


# -----------------------------
# Endpoints de vista / salud
# -----------------------------
@app.get("/")
def index():
    return render_template_string(INDEX_HTML)


@app.get("/health")
def health():
    try:
        row = fetch_one("SELECT 1 AS ok")
        return jsonify({"status": "ok", "db": bool(row and row.get("ok") == 1)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# -----------------------------
# Endpoints API (catálogo)
# -----------------------------
@app.get("/api/catalogs")
def catalogs():
    return jsonify({
        "socio": fetch_all("SELECT id, name FROM socio ORDER BY name"),
        "dias": fetch_all("SELECT id, description FROM dias ORDER BY id"),
        "modalidad": fetch_all("SELECT id, description FROM modalidad ORDER BY id"),
        "horario": fetch_all("SELECT id, description FROM horario ORDER BY id"),
        "status": fetch_all("SELECT id, name FROM status ORDER BY id"),
    })


@app.get("/api/projects")
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


@app.get("/api/projects/<int:project_id>")
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


@app.post("/api/inscripciones")
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


# -----------------------------
# Punto de entrada
# -----------------------------
if __name__ == "__main__":
    # Ejecutar: python app.py
    # Dependencias: pip install flask mysql-connector-python
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)