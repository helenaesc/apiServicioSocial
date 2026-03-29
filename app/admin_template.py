ADMIN_HTML = r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Panel Admin | Registro de Proyectos</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card: #ffffff;
      --text: #0f172a;
      --text-soft: #475569;
      --muted: #94a3b8;
      --border: #e2e8f0;
      --border-strong: #cbd5e1;
      --brand: #2563eb;
      --brand-dark: #1d4ed8;
      --brand-soft: #eff6ff;
      --ok-bg: #dcfce7;
      --ok-text: #166534;
      --err-bg: #fee2e2;
      --err-text: #991b1b;
      --warn-bg: #fff7ed;
      --warn-text: #9a3412;
      --purple-bg: #ede9fe;
      --purple-text: #6d28d9;
      --shadow-sm: 0 1px 3px rgba(0,0,0,.08);
      --radius-xl: 22px;
      --radius-lg: 16px;
      --radius-md: 12px;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: linear-gradient(180deg, #f8fbff 0%, var(--bg) 100%);
      color: var(--text);
      min-height: 100vh;
    }

    .hidden { display: none !important; }

    header {
      background: var(--card);
      border-bottom: 1px solid var(--border);
      padding: 18px 26px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      position: sticky;
      top: 0;
      z-index: 50;
      box-shadow: 0 1px 3px rgba(0,0,0,.08);
    }

    .title-wrap {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .title-wrap strong {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--text);
    }

    .title-wrap span {
      font-size: .92rem;
      color: var(--text-soft);
      font-weight: 500;
    }

    .top-links {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }

    .top-links a, .top-links button {
      text-decoration: none;
      border: 1px solid var(--border);
      background: white;
      color: var(--text-soft);
      padding: 10px 12px;
      border-radius: 999px;
      font-size: .9rem;
      font-weight: 700;
      cursor: pointer;
    }

    .container {
      max-width: 1450px;
      margin: 28px auto;
      padding: 0 18px 32px;
    }

    .msg {
      display: none;
      margin-bottom: 18px;
      padding: 14px 16px;
      border-radius: var(--radius-md);
      font-size: .94rem;
      font-weight: 700;
      border: 1px solid transparent;
      box-shadow: 0 1px 3px rgba(0,0,0,.08);
    }

    .msg.ok {
      display: block;
      background: var(--ok-bg);
      color: var(--ok-text);
      border-color: #bbf7d0;
    }

    .msg.err {
      display: block;
      background: var(--err-bg);
      color: var(--err-text);
      border-color: #fecaca;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 18px;
    }

    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-xl);
      padding: 22px;
      box-shadow: 0 1px 3px rgba(0,0,0,.08);
    }

    .span-12 { grid-column: span 12; }
    .span-8 { grid-column: span 8; }
    .span-6 { grid-column: span 6; }
    .span-4 { grid-column: span 4; }

    h2, h3 {
      margin: 0 0 12px 0;
      line-height: 1.2;
    }

    h2 {
      font-size: 1.2rem;
      font-weight: 800;
    }

    h3 {
      font-size: 1rem;
      font-weight: 800;
    }

    .muted {
      color: var(--text-soft);
      font-size: .93rem;
      line-height: 1.55;
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 12px;
      margin-top: 14px;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .field label {
      font-size: .8rem;
      font-weight: 700;
      color: var(--text-soft);
      text-transform: uppercase;
      letter-spacing: .03em;
    }

    input, select, textarea, button {
      width: 100%;
      min-height: 44px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-strong);
      background: white;
      color: var(--text);
      font-size: .94rem;
      padding: 10px 12px;
      outline: none;
    }

    textarea {
      min-height: 100px;
      resize: vertical;
    }

    .actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 16px;
    }

    .actions > button {
      width: auto;
      min-width: 150px;
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--brand) 0%, #0ea5e9 100%);
      color: white;
      border: none;
      font-weight: 800;
      cursor: pointer;
    }

    .btn-secondary {
      background: #eef2f7;
      color: #334155;
      border: 1px solid #dbe3ee;
      font-weight: 800;
      cursor: pointer;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 10px;
      border-radius: 999px;
      font-size: .78rem;
      font-weight: 800;
      white-space: nowrap;
    }

    .pill-ok { background: var(--ok-bg); color: var(--ok-text); }
    .pill-err { background: var(--err-bg); color: var(--err-text); }
    .pill-warn { background: var(--warn-bg); color: var(--warn-text); }
    .pill-info { background: var(--brand-soft); color: var(--brand); }
    .pill-purple { background: var(--purple-bg); color: var(--purple-text); }
    .pill-neutral { background: #f1f5f9; color: #334155; }

    .list {
      display: grid;
      gap: 12px;
      margin-top: 14px;
    }

    .item {
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      background: #fff;
      padding: 16px;
    }

    .item-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }

    .item-title {
      font-weight: 800;
      font-size: 1rem;
      color: var(--text);
    }

    .meta {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
      margin-top: 10px;
    }

    .meta-box {
      border: 1px solid #eef2f7;
      background: #f8fafc;
      border-radius: 14px;
      padding: 10px 12px;
    }

    .meta-label {
      display: block;
      font-size: .74rem;
      text-transform: uppercase;
      color: var(--muted);
      font-weight: 800;
      margin-bottom: 4px;
      letter-spacing: .03em;
    }

    .meta-value {
      color: var(--text);
      font-weight: 700;
      font-size: .92rem;
      line-height: 1.4;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 12px;
      margin-top: 14px;
    }

    .stat-card {
      border: 1px solid #e9eef5;
      border-radius: 18px;
      background: white;
      padding: 16px;
    }

    .stat-label {
      color: var(--muted);
      font-size: .8rem;
      text-transform: uppercase;
      font-weight: 800;
      letter-spacing: .04em;
      margin-bottom: 8px;
    }

    .stat-value {
      font-size: 1.7rem;
      font-weight: 900;
      color: var(--text);
    }

    .inline-row {
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
    }

    .table-wrap {
      overflow-x: auto;
      margin-top: 14px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 860px;
    }

    th, td {
      text-align: left;
      padding: 12px 10px;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
    }

    th {
      font-size: .78rem;
      text-transform: uppercase;
      letter-spacing: .04em;
      color: var(--text-soft);
      font-weight: 800;
    }

    td {
      font-size: .92rem;
      color: var(--text);
    }

    .small {
      font-size: .84rem;
      color: var(--text-soft);
    }

    @media (max-width: 1100px) {
      .span-8, .span-6, .span-4 { grid-column: span 12; }
    }

    @media (max-width: 640px) {
      header {
        flex-direction: column;
        align-items: flex-start;
      }
      .actions {
        flex-direction: column;
        align-items: stretch;
      }
      .actions > button {
        width: 100%;
      }
    }
  </style>
</head>
<body>
  <header>
    <div class="title-wrap">
      <strong>Panel Administrativo</strong>
      <span>Temporadas · Proyectos · Dashboard · Incidentes</span>
    </div>

    <div class="top-links">
      <a href="/">Vista Alumno</a>
      <a href="/health">Health</a>
      <button type="button" onclick="logout()">Cerrar sesión</button>
    </div>
  </header>

  <div class="container">
    <div id="msg" class="msg"></div>

    <div id="loginCard" class="card span-12">
      <h2>Acceso Administrador / Staff</h2>
      <div class="muted">Ingresa tu clave para habilitar el panel.</div>

      <div class="form-grid" style="max-width:540px;">
        <div class="field">
          <label>Clave</label>
          <input id="adminKey" type="password" placeholder="Ingresa clave ADMIN o STAFF">
        </div>
      </div>

      <div class="actions">
        <button type="button" class="btn-primary" onclick="validateAndSaveKey()">Entrar</button>
        <button type="button" class="btn-secondary" onclick="clearKey(false)">Limpiar</button>
      </div>

      <div class="small" id="roleBadge" style="margin-top:12px;">Sesión actual: —</div>
    </div>

    <div id="mainDashboard" class="grid hidden">
      <div class="card span-6">
        <h2>Gestión de Temporadas</h2>
        <div class="muted">
          Crea temporadas operativas. Para empezar usa estado <strong>VISIBLE</strong> y visible para alumnos en <strong>Sí</strong>.
        </div>

        <div class="form-grid">
          <div class="field">
            <label>Año</label>
            <input id="eventYear" type="number" min="2020" max="2100" placeholder="Ej: 2026">
          </div>

          <div class="field">
            <label>Temporada</label>
            <select id="eventSeason">
              <option value="PRIMAVERA">Primavera</option>
              <option value="INVIERNO">Invierno</option>
            </select>
          </div>

          <div class="field">
            <label>Estado</label>
            <select id="eventStatus">
              <option value="VISIBLE">Visible</option>
              <option value="DRAFT">Draft</option>
              <option value="ONSITE">Onsite</option>
              <option value="CLOSED">Closed</option>
              <option value="ARCHIVED">Archived</option>
            </select>
          </div>

          <div class="field">
            <label>Visible para alumnos</label>
            <select id="eventVisible">
              <option value="true">Sí</option>
              <option value="false">No</option>
            </select>
          </div>

          <div class="field">
            <label>Abre catálogo</label>
            <input id="eventCatalogOpenAt" type="datetime-local">
          </div>

          <div class="field">
            <label>Inicio presencial</label>
            <input id="eventOnsiteStartAt" type="datetime-local">
          </div>

          <div class="field">
            <label>Fin presencial</label>
            <input id="eventOnsiteEndAt" type="datetime-local">
          </div>

          <div class="field">
            <label>Cierre registro</label>
            <input id="eventRegistrationCloseAt" type="datetime-local">
          </div>
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="createEvent()">Crear temporada</button>
          <button type="button" class="btn-secondary" onclick="loadEvents()">Recargar</button>
        </div>

        <div id="eventsList" class="list"></div>
      </div>

      <div class="card span-6">
        <h2>Operar Temporada</h2>
        <div class="muted">Selecciona una temporada para trabajar sobre ella.</div>

        <div class="form-grid">
          <div class="field">
            <label>Temporada seleccionada</label>
            <select id="eventSelector"></select>
          </div>

          <div class="field">
            <label>Nuevo estado</label>
            <select id="eventStatusUpdate">
              <option value="">Sin cambio</option>
              <option value="DRAFT">Draft</option>
              <option value="VISIBLE">Visible</option>
              <option value="ONSITE">Onsite</option>
              <option value="CLOSED">Closed</option>
              <option value="ARCHIVED">Archived</option>
            </select>
          </div>

          <div class="field">
            <label>Visible para alumnos</label>
            <select id="eventVisibleUpdate">
              <option value="">Sin cambio</option>
              <option value="true">Sí</option>
              <option value="false">No</option>
            </select>
          </div>
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="updateSelectedEvent()">Guardar cambios</button>
          <button type="button" class="btn-secondary" onclick="setSelectedEventVisible()">Marcar visible</button>
          <button type="button" class="btn-secondary" onclick="loadDashboard()">Cargar dashboard</button>
        </div>

        <div id="selectedEventInfo" class="list"></div>
      </div>

      <div class="card span-12">
        <h2>Proyecto Maestro</h2>
        <div class="muted">Crea proyectos con su ficha completa. Después podrás asignarlos a temporadas.</div>

        <div class="form-grid">
          <div class="field">
            <label>Nombre general / organización</label>
            <input id="mp_general_name" placeholder="Ej: Adidas, Tigres, Nike">
          </div>

          <div class="field">
            <label>Nombre del proyecto</label>
            <input id="mp_name" placeholder="Ej: Análisis del equipo para mejorar el rendimiento">
          </div>

          <div class="field">
            <label>Carrera preferida</label>
            <select id="mp_partner"></select>
          </div>

          <div class="field">
            <label>Modalidad</label>
            <select id="mp_modality"></select>
          </div>

          <div class="field">
            <label>Días</label>
            <select id="mp_week_days"></select>
          </div>

          <div class="field">
            <label>Horario</label>
            <select id="mp_schedule"></select>
          </div>

          <div class="field">
            <label>Cupo base</label>
            <input id="mp_slots" type="number" min="0" placeholder="Ej: 2">
          </div>

          <div class="field">
            <label>Detalle de horario</label>
            <input id="mp_schedule_description" placeholder="Ej: 10:00 a 18:00">
          </div>

          <div class="field">
            <label>Responsables / líderes</label>
            <input id="mp_team_owners" placeholder="Ej: Equipo de análisis">
          </div>

          <div class="field">
            <label>Duración</label>
            <input id="mp_duration" placeholder="Ej: 5 semanas">
          </div>

          <div class="field">
            <label>Población</label>
            <input id="mp_audience" placeholder="Ej: Jóvenes">
          </div>

          <div class="field">
            <label>Horas máximas</label>
            <input id="mp_max_hours" type="number" min="0" placeholder="Ej: 100">
          </div>

          <div class="field">
            <label>Lugar de trabajo</label>
            <input id="mp_location" placeholder="Dirección o lugar">
          </div>

          <div class="field">
            <label>Clave externa</label>
            <input id="mp_clave" placeholder="Clave usada fuera del evento">
          </div>

          <div class="field">
            <label>Competencias</label>
            <input id="mp_competencies" placeholder="Ej: creatividad, análisis">
          </div>
        </div>

        <div class="field" style="margin-top:12px;">
          <label>Objetivos</label>
          <textarea id="mp_objectives" placeholder="Objetivos del proyecto"></textarea>
        </div>

        <div class="field" style="margin-top:12px;">
          <label>Actividades</label>
          <textarea id="mp_activities" placeholder="Actividades del proyecto"></textarea>
        </div>

        <div class="field" style="margin-top:12px;">
          <label>Comentarios</label>
          <textarea id="mp_comments" placeholder="Comentarios importantes"></textarea>
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="createMasterProject()">Crear proyecto maestro</button>
          <button type="button" class="btn-secondary" onclick="loadMasterProjects()">Recargar lista</button>
        </div>
      </div>

      <div class="card span-12">
        <h2>Proyectos Maestros Existentes</h2>
        <div class="muted">Selecciona un proyecto por nombre y luego agrégalo a la temporada activa.</div>

        <div class="form-grid">
          <div class="field">
            <label>Buscar</label>
            <input id="masterProjectsSearch" placeholder="Buscar por nombre, organización, líder..." oninput="loadMasterProjects()">
          </div>
        </div>

        <div id="masterProjectsList" class="list"></div>
      </div>

      <div class="card span-8">
        <h2>Proyectos en Temporada</h2>
        <div class="muted">Agrega proyectos existentes a la temporada seleccionada y define su cupo real.</div>

        <div class="form-grid">
          <div class="field">
            <label>Proyecto maestro</label>
            <select id="projectSelector"></select>
          </div>

          <div class="field">
            <label>Slots / cupo total</label>
            <input id="slotsInput" type="number" min="0" placeholder="Ej: 10">
          </div>
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="addProjectToEvent()">Agregar proyecto a temporada</button>
          <button type="button" class="btn-secondary" onclick="loadEventProjects()">Recargar proyectos</button>
        </div>

        <div id="eventProjectsList" class="list"></div>
      </div>

      <div class="card span-4">
        <h2>Vigencia global de tokens</h2>
        <div class="muted">Controla cuántas horas durarán los nuevos tokens de proyecto.</div>

        <div class="form-grid">
          <div class="field">
            <label>Horas</label>
            <input id="ttl_hours" type="number" min="1" max="168" value="24">
          </div>
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="saveTokenTTL()">Guardar TTL</button>
          <button type="button" class="btn-secondary" onclick="loadTokenTTL()">Recargar</button>
        </div>

        <div class="small" style="margin-top:10px;">
          Valor actual: <span id="ttl_current" class="pill pill-neutral">—</span>
        </div>
      </div>

      <div class="card span-12">
        <h2>Dashboard de la Temporada</h2>
        <div class="muted">Monitorea solicitudes, validaciones, registros e incidentes.</div>
        <div id="dashboardSummary" class="stats-grid"></div>
      </div>

      <div class="card span-12">
        <h2>Resumen por Proyecto</h2>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Proyecto</th>
                <th>Carrera preferida</th>
                <th>Estado</th>
                <th>Slots</th>
                <th>Registrados</th>
                <th>Disponibles</th>
                <th>Tokens usados</th>
                <th>Revocados</th>
                <th>Expirados</th>
              </tr>
            </thead>
            <tbody id="dashboardProjectsBody">
              <tr><td colspan="9" class="small">Selecciona una temporada y carga dashboard.</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card span-6">
        <h2>Reportar Caso</h2>
        <div class="muted">Staff/Admin pueden registrar incidencias.</div>

        <div class="form-grid">
          <div class="field">
            <label>Event ID</label>
            <input id="incidentEventId" placeholder="Se llena con la temporada seleccionada">
          </div>

          <div class="field">
            <label>Request ID (opcional)</label>
            <input id="incidentRequestId" placeholder="ID de solicitud">
          </div>

          <div class="field">
            <label>User ID (opcional)</label>
            <input id="incidentUserId" placeholder="ID de usuario">
          </div>

          <div class="field">
            <label>Reported by User ID (opcional)</label>
            <input id="incidentReportedBy" placeholder="ID interno del staff/admin">
          </div>

          <div class="field">
            <label>Tipo</label>
            <select id="incidentType">
              <option value="ID_NO_COINCIDE">ID_NO_COINCIDE</option>
              <option value="FOLIO_NO_ENCONTRADO">FOLIO_NO_ENCONTRADO</option>
              <option value="QR_INVALIDO">QR_INVALIDO</option>
              <option value="QR_EXPIRADO">QR_EXPIRADO</option>
              <option value="DATOS_INCORRECTOS">DATOS_INCORRECTOS</option>
              <option value="ALUMNO_YA_VALIDADO">ALUMNO_YA_VALIDADO</option>
              <option value="ALUMNO_YA_REGISTRADO">ALUMNO_YA_REGISTRADO</option>
              <option value="TOKEN_INVALIDO">TOKEN_INVALIDO</option>
              <option value="TOKEN_YA_USADO">TOKEN_YA_USADO</option>
              <option value="TOKEN_REVOCADO">TOKEN_REVOCADO</option>
              <option value="TOKEN_EXPIRADO">TOKEN_EXPIRADO</option>
              <option value="PROYECTO_INCORRECTO">PROYECTO_INCORRECTO</option>
              <option value="PROBLEMA_TECNICO">PROBLEMA_TECNICO</option>
              <option value="OTRO">OTRO</option>
            </select>
          </div>

          <div class="field">
            <label>Severidad</label>
            <select id="incidentSeverity">
              <option value="LOW">LOW</option>
              <option value="MEDIUM" selected>MEDIUM</option>
              <option value="HIGH">HIGH</option>
            </select>
          </div>
        </div>

        <div class="field" style="margin-top:12px;">
          <label>Descripción</label>
          <textarea id="incidentDescription" placeholder="Describe el caso con claridad."></textarea>
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="createIncident()">Reportar caso</button>
          <button type="button" class="btn-secondary" onclick="loadIncidents()">Recargar incidentes</button>
        </div>
      </div>

      <div class="card span-6">
        <h2>Incidentes</h2>

        <div class="form-grid">
          <div class="field">
            <label>Filtrar status</label>
            <select id="incidentFilterStatus" onchange="loadIncidents()">
              <option value="">Todos</option>
              <option value="OPEN">OPEN</option>
              <option value="IN_PROGRESS">IN_PROGRESS</option>
              <option value="RESOLVED">RESOLVED</option>
              <option value="DISMISSED">DISMISSED</option>
            </select>
          </div>

          <div class="field">
            <label>Filtrar severidad</label>
            <select id="incidentFilterSeverity" onchange="loadIncidents()">
              <option value="">Todas</option>
              <option value="LOW">LOW</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="HIGH">HIGH</option>
            </select>
          </div>
        </div>

        <div id="incidentsList" class="list"></div>
      </div>
    </div>
  </div>

  <script>
    const storage = sessionStorage;

    function escapeHTML(value) {
      return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function showMsg(text, ok=true) {
      const el = document.getElementById('msg');
      el.textContent = text || '';
      el.className = 'msg ' + (ok ? 'ok' : 'err');
    }

    function getKey() { return storage.getItem('ADMIN_API_KEY') || ''; }
    function getRole() { return storage.getItem('ADMIN_ROLE') || ''; }

    function applyRoleUI(role) {
      document.getElementById('roleBadge').textContent = role ? `Sesión activa como: ${role}` : 'Sesión actual: —';
      document.getElementById('loginCard').classList.toggle('hidden', !!role);
      document.getElementById('mainDashboard').classList.toggle('hidden', !role);
    }

    async function getJSON(url) {
      const r = await fetch(url);
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
      return data;
    }

    async function getJSONAuth(url) {
      const r = await fetch(url, {
        headers: { 'X-ADMIN-KEY': getKey() }
      });
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
      return data;
    }

    async function postJSON(url, body) {
      const r = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-ADMIN-KEY': getKey()
        },
        body: JSON.stringify(body)
      });
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
      return data;
    }

    async function patchJSON(url, body) {
      const r = await fetch(url, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-ADMIN-KEY': getKey()
        },
        body: JSON.stringify(body)
      });
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
      return data;
    }

    async function putJSON(url, body) {
      const r = await fetch(url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-ADMIN-KEY': getKey()
        },
        body: JSON.stringify(body || {})
      });
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
      return data;
    }

    function boolFromString(v) {
      return String(v).toLowerCase() === 'true';
    }

    function toSqlDateTime(value) {
      if (!value) return null;
      return value.replace('T', ' ') + ':00';
    }

    function statusPill(status) {
      const map = {
        'DRAFT': ['pill-neutral', 'DRAFT'],
        'VISIBLE': ['pill-info', 'VISIBLE'],
        'ONSITE': ['pill-ok', 'ONSITE'],
        'CLOSED': ['pill-warn', 'CLOSED'],
        'ARCHIVED': ['pill-err', 'ARCHIVED'],
        'ACTIVE': ['pill-ok', 'ACTIVE'],
        'HIDDEN': ['pill-warn', 'HIDDEN'],
        'OPEN': ['pill-err', 'OPEN'],
        'IN_PROGRESS': ['pill-warn', 'IN_PROGRESS'],
        'RESOLVED': ['pill-ok', 'RESOLVED'],
        'DISMISSED': ['pill-neutral', 'DISMISSED']
      };
      const cfg = map[status] || ['pill-neutral', status || '—'];
      return `<span class="pill ${cfg[0]}">${cfg[1]}</span>`;
    }

    async function validateAndSaveKey() {
      const v = document.getElementById('adminKey').value.trim();
      if (!v) return showMsg('Escribe tu clave', false);

      try {
        const r = await fetch('/api/admin/ping', {
          headers: { 'X-ADMIN-KEY': v }
        });
        const data = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(data.error || ('Error ' + r.status));

        storage.setItem('ADMIN_API_KEY', v);
        storage.setItem('ADMIN_ROLE', data.role);
        applyRoleUI(data.role);

        await bootstrapAdmin();
        showMsg(`Sesión iniciada (${data.role})`);
      } catch (e) {
        showMsg('Clave inválida: ' + e.message, false);
        clearKey(false);
      }
    }

    function clearKey(show=true) {
      storage.removeItem('ADMIN_API_KEY');
      storage.removeItem('ADMIN_ROLE');
      document.getElementById('adminKey').value = '';
      applyRoleUI('');
      if (show) showMsg('Sesión cerrada');
    }

    function logout() {
      clearKey(true);
    }

    async function bootstrapAdmin() {
      await Promise.allSettled([
        loadEvents(),
        loadTokenTTL(),
        loadAdminCatalogs(),
        loadMasterProjects()
      ]);
    }

    async function createEvent() {
      try {
        showMsg('Creando temporada...');

        const year = Number(document.getElementById('eventYear').value);
        const season = document.getElementById('eventSeason').value;
        const status = document.getElementById('eventStatus').value;
        const isVisible = boolFromString(document.getElementById('eventVisible').value);

        if (!year || year < 2020 || year > 2100) {
          return showMsg('Año inválido', false);
        }

        const payload = {
          year: year,
          season: season,
          status: status,
          is_visible_to_students: isVisible,
          catalog_open_at: toSqlDateTime(document.getElementById('eventCatalogOpenAt').value),
          onsite_start_at: toSqlDateTime(document.getElementById('eventOnsiteStartAt').value),
          onsite_end_at: toSqlDateTime(document.getElementById('eventOnsiteEndAt').value),
          registration_close_at: toSqlDateTime(document.getElementById('eventRegistrationCloseAt').value)
        };

        console.log('createEvent payload:', payload);

        const data = await postJSON('/api/admin/events', payload);

        console.log('createEvent response:', data);
        showMsg(data.message || 'Temporada creada correctamente');
        await loadEvents();
      } catch (e) {
        console.error('createEvent error:', e);
        showMsg(e.message || 'Error creando temporada', false);
      }
    }

    async function loadEvents() {
      try {
        showMsg('Cargando temporadas...');

        const data = await getJSONAuth('/api/admin/events');
        console.log('loadEvents response:', data);

        const list = document.getElementById('eventsList');
        const selector = document.getElementById('eventSelector');

        list.innerHTML = '';
        selector.innerHTML = '';

        if (!data.length) {
          list.innerHTML = `<div class="item"><div class="small">No hay temporadas creadas todavía.</div></div>`;
          document.getElementById('selectedEventInfo').innerHTML = '';
          document.getElementById('incidentEventId').value = '';
          document.getElementById('eventProjectsList').innerHTML = '';
          document.getElementById('dashboardSummary').innerHTML = '';
          document.getElementById('dashboardProjectsBody').innerHTML = '<tr><td colspan="9" class="small">No hay temporadas.</td></tr>';
          document.getElementById('incidentsList').innerHTML = '';
          showMsg('No hay temporadas creadas todavía');
          return;
        }

        for (const e of data) {
          const div = document.createElement('div');
          div.className = 'item';
          div.innerHTML = `
            <div class="item-head">
              <div>
                <div class="item-title">${escapeHTML(e.display_name)}</div>
                <div class="small">Año ${e.year} · ${e.season}</div>
              </div>
              <div class="inline-row">
                ${statusPill(e.status)}
                ${e.is_visible_to_students ? '<span class="pill pill-purple">VISIBLE ALUMNO</span>' : '<span class="pill pill-neutral">NO VISIBLE</span>'}
              </div>
            </div>
          `;
          list.appendChild(div);

          const opt = document.createElement('option');
          opt.value = e.id;
          opt.textContent = `${e.display_name} · ${e.status}`;
          selector.appendChild(opt);
        }

        selector.value = String(data[0].id);

        await loadSelectedEventInfo();
        await loadEventProjects();
        await loadDashboard();
        await loadIncidents();

        showMsg('Temporadas cargadas correctamente');
      } catch (e) {
        console.error('loadEvents error:', e);
        showMsg(e.message || 'Error cargando temporadas', false);
      }
    }

    async function loadSelectedEventInfo() {
      const eventId = document.getElementById('eventSelector').value;
      const box = document.getElementById('selectedEventInfo');
      if (!eventId) {
        box.innerHTML = '';
        return;
      }

      try {
        const e = await getJSONAuth(`/api/admin/events/${eventId}`);
        box.innerHTML = `
          <div class="item">
            <div class="item-head">
              <div>
                <div class="item-title">${escapeHTML(e.display_name)}</div>
                <div class="small">${e.season} ${e.year}</div>
              </div>
              <div class="inline-row">
                ${statusPill(e.status)}
                ${e.is_visible_to_students ? '<span class="pill pill-purple">VISIBLE ALUMNO</span>' : '<span class="pill pill-neutral">NO VISIBLE</span>'}
              </div>
            </div>
            <div class="small">ID de temporada: ${e.id}</div>
          </div>
        `;
        document.getElementById('incidentEventId').value = e.id;
      } catch (e) {
        box.innerHTML = `<div class="item"><div class="small">${escapeHTML(e.message)}</div></div>`;
      }
    }

    async function updateSelectedEvent() {
      const eventId = document.getElementById('eventSelector').value;
      if (!eventId) return showMsg('Selecciona una temporada', false);

      const body = {};
      const statusVal = document.getElementById('eventStatusUpdate').value;
      const visibleVal = document.getElementById('eventVisibleUpdate').value;

      if (statusVal) body.status = statusVal;
      if (visibleVal !== '') body.is_visible_to_students = boolFromString(visibleVal);

      if (!Object.keys(body).length) {
        return showMsg('No hay cambios para aplicar', false);
      }

      try {
        const data = await patchJSON(`/api/admin/events/${eventId}`, body);
        showMsg(data.message || 'Temporada actualizada');
        await loadEvents();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function setSelectedEventVisible() {
      const eventId = document.getElementById('eventSelector').value;
      if (!eventId) return showMsg('Selecciona una temporada', false);

      try {
        const data = await putJSON(`/api/admin/events/${eventId}/visible`, {});
        showMsg(data.message || 'Temporada visible actualizada');
        await loadEvents();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function loadAdminCatalogs() {
      try {
        const data = await getJSONAuth('/api/admin/catalogs');

        fillAdminSelect('mp_partner', data.socio || [], 'name');
        fillAdminSelect('mp_modality', data.modalidad || [], 'description');
        fillAdminSelect('mp_week_days', data.dias || [], 'description');
        fillAdminSelect('mp_schedule', data.horario || [], 'description');
      } catch (e) {
        showMsg('Error cargando catálogos admin: ' + e.message, false);
      }
    }

    function fillAdminSelect(id, items, labelKey='description') {
      const el = document.getElementById(id);
      if (!el) return;
      el.innerHTML = '<option value="">Selecciona</option>';

      for (const item of items || []) {
        const opt = document.createElement('option');
        opt.value = item.id;
        opt.textContent = item[labelKey];
        el.appendChild(opt);
      }
    }

    async function createMasterProject() {
      try {
        const payload = {
          general_name: document.getElementById('mp_general_name').value.trim(),
          name: document.getElementById('mp_name').value.trim(),
          id_partner: Number(document.getElementById('mp_partner').value),
          id_modality: Number(document.getElementById('mp_modality').value),
          id_week_days: Number(document.getElementById('mp_week_days').value),
          id_schedule: Number(document.getElementById('mp_schedule').value),
          slots: Number(document.getElementById('mp_slots').value || 0),
          schedule_description: document.getElementById('mp_schedule_description').value.trim(),
          team_owners: document.getElementById('mp_team_owners').value.trim(),
          objectives: document.getElementById('mp_objectives').value.trim(),
          activities: document.getElementById('mp_activities').value.trim(),
          clave: document.getElementById('mp_clave').value.trim(),
          competencies: document.getElementById('mp_competencies').value.trim(),
          location: document.getElementById('mp_location').value.trim(),
          duration: document.getElementById('mp_duration').value.trim(),
          audience: document.getElementById('mp_audience').value.trim(),
          max_hours: document.getElementById('mp_max_hours').value.trim(),
          comments: document.getElementById('mp_comments').value.trim()
        };

        const data = await postJSON('/api/admin/projects', payload);
        showMsg(data.message || 'Proyecto maestro creado');
        await loadMasterProjects();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function loadMasterProjects() {
      try {
        const q = document.getElementById('masterProjectsSearch')?.value?.trim() || '';
        const query = q ? `?q=${encodeURIComponent(q)}` : '';
        const data = await getJSONAuth('/api/admin/projects' + query);

        const list = document.getElementById('masterProjectsList');
        const selector = document.getElementById('projectSelector');

        if (selector) {
          selector.innerHTML = '<option value="">Selecciona un proyecto</option>';
          for (const p of data) {
            const opt = document.createElement('option');
            opt.value = p.id;
            opt.textContent = `${p.general_name || 'Sin nombre general'} | ${p.name}`;
            selector.appendChild(opt);
          }
        }

        if (!list) return;

        if (!data.length) {
          list.innerHTML = `<div class="item"><div class="small">No hay proyectos maestros.</div></div>`;
          return;
        }

        list.innerHTML = data.map(p => `
          <div class="item">
            <div class="item-head">
              <div>
                <div class="item-title">${escapeHTML(p.general_name || 'Sin nombre general')} | ${escapeHTML(p.name)}</div>
                <div class="small">Project ID: ${p.id}</div>
              </div>
              <div class="inline-row">
                <span class="pill pill-info">${escapeHTML(p.modality_name || '—')}</span>
                <span class="pill pill-neutral">${escapeHTML(p.week_days_name || '—')}</span>
                <span class="pill pill-neutral">${escapeHTML(p.schedule_name || '—')}</span>
              </div>
            </div>

            <div class="meta">
              <div class="meta-box">
                <span class="meta-label">Carrera preferida</span>
                <div class="meta-value">${escapeHTML(p.partner_name || '—')}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Horario</span>
                <div class="meta-value">${escapeHTML(p.schedule_description || '—')}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Duración</span>
                <div class="meta-value">${escapeHTML(p.duration || '—')}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Clave</span>
                <div class="meta-value">${escapeHTML(p.clave || '—')}</div>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-secondary" onclick="selectMasterProject(${p.id})">Seleccionar para temporada</button>
            </div>
          </div>
        `).join('');
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    function selectMasterProject(projectId) {
      const selector = document.getElementById('projectSelector');
      if (!selector) return;
      selector.value = String(projectId);
      showMsg('Proyecto seleccionado para agregar a temporada');
    }

    async function addProjectToEvent() {
      const eventId = document.getElementById('eventSelector').value;
      const projectId = document.getElementById('projectSelector').value;
      const slots = Number(document.getElementById('slotsInput').value);

      if (!eventId) return showMsg('Selecciona una temporada', false);
      if (!projectId) return showMsg('Selecciona un proyecto maestro', false);
      if (Number.isNaN(slots) || slots < 0) return showMsg('Slots inválidos', false);

      try {
        const data = await postJSON(`/api/admin/events/${eventId}/projects`, {
          project_id: Number(projectId),
          slots_total: slots
        });
        showMsg(data.message || 'Proyecto agregado a la temporada');
        await loadEventProjects();
        await loadDashboard();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function loadEventProjects() {
      const eventId = document.getElementById('eventSelector').value;
      const container = document.getElementById('eventProjectsList');

      if (!eventId) {
        container.innerHTML = `<div class="item"><div class="small">Selecciona una temporada.</div></div>`;
        return;
      }

      try {
        const data = await getJSONAuth(`/api/admin/events/${eventId}/projects`);

        if (!data.length) {
          container.innerHTML = `<div class="item"><div class="small">No hay proyectos cargados en esta temporada.</div></div>`;
          return;
        }

        container.innerHTML = data.map(p => `
          <div class="item">
            <div class="item-head">
              <div>
                <div class="item-title">${escapeHTML(p.name)}</div>
                <div class="small">Carrera preferida: ${escapeHTML(p.partner || '—')} · Project ID: ${p.project_id} · EventProject ID: ${p.id}</div>
              </div>
              <div>${statusPill(p.status)}</div>
            </div>

            <div class="meta">
              <div class="meta-box">
                <span class="meta-label">Slots total</span>
                <div class="meta-value">${p.slots_total}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Estado</span>
                <div class="meta-value">${p.status}</div>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-secondary" onclick="quickUpdateEventProject(${p.id}, ${p.slots_total}, 'ACTIVE')">Activar</button>
              <button type="button" class="btn-secondary" onclick="quickUpdateEventProject(${p.id}, ${p.slots_total}, 'HIDDEN')">Ocultar</button>
              <button type="button" class="btn-secondary" onclick="quickUpdateEventProject(${p.id}, ${p.slots_total}, 'CLOSED')">Cerrar</button>
            </div>
          </div>
        `).join('');
      } catch (e) {
        container.innerHTML = `<div class="item"><div class="small">${escapeHTML(e.message)}</div></div>`;
      }
    }

    async function quickUpdateEventProject(eventProjectId, currentSlots, status) {
      try {
        const data = await patchJSON(`/api/admin/event-projects/${eventProjectId}`, {
          slots_total: currentSlots,
          status: status
        });
        showMsg(data.message || 'Proyecto de temporada actualizado');
        await loadEventProjects();
        await loadDashboard();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function loadTokenTTL() {
      try {
        const data = await getJSONAuth('/api/admin/settings');
        const hours = Number(data.token_ttl_hours || 24);
        document.getElementById('ttl_hours').value = hours;
        document.getElementById('ttl_current').textContent = `${hours} horas`;
      } catch (e) {
        showMsg('Error TTL: ' + e.message, false);
      }
    }

    async function saveTokenTTL() {
      const hours = Number(document.getElementById('ttl_hours').value || 24);
      if (!hours || hours < 1 || hours > 168) {
        return showMsg('Horas inválidas (1 a 168)', false);
      }

      try {
        const data = await putJSON('/api/admin/settings/token-ttl-hours', { hours });
        document.getElementById('ttl_current').textContent = `${data.token_ttl_hours} horas`;
        showMsg('TTL global actualizado');
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function loadDashboard() {
      const eventId = document.getElementById('eventSelector').value;
      if (!eventId) return;

      try {
        const summary = await getJSONAuth(`/api/admin/dashboard/summary?event_id=${eventId}`);
        const projects = await getJSONAuth(`/api/admin/dashboard/projects?event_id=${eventId}`);

        document.getElementById('dashboardSummary').innerHTML = `
          <div class="stat-card">
            <div class="stat-label">Solicitudes</div>
            <div class="stat-value">${summary.requests.total}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Requested</div>
            <div class="stat-value">${summary.requests.requested}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Validated</div>
            <div class="stat-value">${summary.requests.validated}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Access Enabled</div>
            <div class="stat-value">${summary.requests.access_enabled}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Registered</div>
            <div class="stat-value">${summary.requests.registered}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Incidentes abiertos</div>
            <div class="stat-value">${summary.incidents.open}</div>
          </div>
        `;

        const body = document.getElementById('dashboardProjectsBody');
        if (!projects.length) {
          body.innerHTML = `<tr><td colspan="9" class="small">No hay proyectos cargados en esta temporada.</td></tr>`;
        } else {
          body.innerHTML = projects.map(p => `
            <tr>
              <td><strong>${escapeHTML(p.project_name)}</strong></td>
              <td>${escapeHTML(p.partner_name || '—')}</td>
              <td>${escapeHTML(p.event_project_status)}</td>
              <td>${p.slots_total}</td>
              <td>${p.registered_count}</td>
              <td>${p.cupos_disponibles}</td>
              <td>${p.tokens_used}</td>
              <td>${p.tokens_revoked}</td>
              <td>${p.tokens_expired}</td>
            </tr>
          `).join('');
        }
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function createIncident() {
      try {
        const payload = {
          event_id: Number(document.getElementById('incidentEventId').value),
          request_id: document.getElementById('incidentRequestId').value || null,
          id_user: document.getElementById('incidentUserId').value || null,
          reported_by_user_id: document.getElementById('incidentReportedBy').value || null,
          type: document.getElementById('incidentType').value,
          severity: document.getElementById('incidentSeverity').value,
          description: document.getElementById('incidentDescription').value.trim()
        };

        const data = await postJSON('/api/incidents', payload);
        showMsg(data.message || 'Caso reportado');
        document.getElementById('incidentDescription').value = '';
        document.getElementById('incidentRequestId').value = '';
        document.getElementById('incidentUserId').value = '';
        await loadIncidents();
        await loadDashboard();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function loadIncidents() {
      const eventId = document.getElementById('eventSelector').value;
      const list = document.getElementById('incidentsList');

      if (!eventId) {
        list.innerHTML = `<div class="item"><div class="small">Selecciona una temporada.</div></div>`;
        return;
      }

      const params = new URLSearchParams();
      params.set('event_id', eventId);

      const status = document.getElementById('incidentFilterStatus').value;
      const severity = document.getElementById('incidentFilterSeverity').value;
      if (status) params.set('status', status);
      if (severity) params.set('severity', severity);

      try {
        const data = await getJSONAuth(`/api/incidents?${params.toString()}`);

        if (!data.length) {
          list.innerHTML = `<div class="item"><div class="small">No hay incidentes con esos filtros.</div></div>`;
          return;
        }

        list.innerHTML = data.map(i => `
          <div class="item">
            <div class="item-head">
              <div>
                <div class="item-title">${escapeHTML(i.type)}</div>
                <div class="small">Incident ID: ${i.id} · Request ID: ${i.request_id ?? '—'} · User ID: ${i.id_user ?? '—'}</div>
              </div>
              <div class="inline-row">
                ${statusPill(i.status)}
                <span class="pill ${i.severity === 'HIGH' ? 'pill-err' : i.severity === 'MEDIUM' ? 'pill-warn' : 'pill-ok'}">${i.severity}</span>
              </div>
            </div>

            <div class="small" style="margin-bottom:10px;">
              ${escapeHTML(i.description || 'Sin descripción')}
            </div>

            <div class="small" style="margin-bottom:10px;">
              Creado: ${escapeHTML(i.created_at || '—')} · Resuelto: ${escapeHTML(i.resolved_at || '—')}
            </div>

            <div class="actions">
              <button type="button" class="btn-secondary" onclick="updateIncidentStatus(${i.id}, 'IN_PROGRESS')">Marcar en proceso</button>
              <button type="button" class="btn-secondary" onclick="updateIncidentStatus(${i.id}, 'RESOLVED')">Resolver</button>
              <button type="button" class="btn-secondary" onclick="updateIncidentStatus(${i.id}, 'DISMISSED')">Descartar</button>
            </div>
          </div>
        `).join('');
      } catch (e) {
        list.innerHTML = `<div class="item"><div class="small">${escapeHTML(e.message)}</div></div>`;
      }
    }

    async function updateIncidentStatus(incidentId, status) {
      try {
        const data = await patchJSON(`/api/incidents/${incidentId}`, { status });
        showMsg(data.message || 'Caso actualizado');
        await loadIncidents();
        await loadDashboard();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    document.addEventListener('DOMContentLoaded', async () => {
      if (getKey()) {
        applyRoleUI(getRole());
        await bootstrapAdmin();
      } else {
        applyRoleUI('');
      }

      document.getElementById('adminKey').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') validateAndSaveKey();
      });

      document.getElementById('eventSelector').addEventListener('change', async () => {
        await loadSelectedEventInfo();
        await loadEventProjects();
        await loadDashboard();
        await loadIncidents();
      });
    });
  </script>
</body>
</html>
"""