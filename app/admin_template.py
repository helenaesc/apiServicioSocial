ADMIN_HTML = r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Panel Admin | Registro de Proyectos</title>
  <script src="https://unpkg.com/html5-qrcode"></script>
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
      --shadow-md: 0 12px 30px rgba(15, 23, 42, 0.08);
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
      box-shadow: var(--shadow-sm);
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

    .top-links a:hover, .top-links button:hover {
      border-color: var(--brand);
      color: var(--brand);
    }

    .container {
      max-width: 1500px;
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
      box-shadow: var(--shadow-sm);
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
      box-shadow: var(--shadow-sm);
      padding: 22px;
    }

    .span-12 { grid-column: span 12; }
    .span-8 { grid-column: span 8; }
    .span-6 { grid-column: span 6; }
    .span-4 { grid-column: span 4; }
    .span-3 { grid-column: span 3; }

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

    .small {
      font-size: .84rem;
      color: var(--text-soft);
    }

    .mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: .92rem;
      background: #0f172a;
      color: #e2e8f0;
      border-radius: 14px;
      padding: 10px 12px;
      word-break: break-all;
    }

    .section-title {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }

    .section-title .left {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .section-anchor {
      scroll-margin-top: 90px;
    }

    .quick-nav {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .quick-nav button {
      width: auto;
      min-height: auto;
      padding: 9px 12px;
      border-radius: 999px;
      font-size: .85rem;
      font-weight: 800;
      border: 1px solid var(--border);
      background: white;
      cursor: pointer;
    }

    .quick-nav button:hover {
      border-color: var(--brand);
      color: var(--brand);
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
      transition: .18s ease;
    }

    textarea {
      min-height: 100px;
      resize: vertical;
    }

    input:focus, select:focus, textarea:focus {
      border-color: var(--brand);
      box-shadow: 0 0 0 4px rgba(37,99,235,.10);
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
      box-shadow: 0 10px 20px rgba(37,99,235,.18);
      cursor: pointer;
    }

    .btn-primary:hover { background: var(--brand-dark); }

    .btn-secondary {
      background: #eef2f7;
      color: #334155;
      border: 1px solid #dbe3ee;
      font-weight: 800;
      cursor: pointer;
    }

    .btn-danger {
      background: #ef4444;
      color: white;
      border: none;
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
      box-shadow: 0 6px 18px rgba(15,23,42,.05);
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
      min-width: 920px;
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

    .subgrid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 18px;
    }

    @media (max-width: 1200px) {
      .span-8, .span-6, .span-4, .span-3 { grid-column: span 12; }
      .subgrid { grid-template-columns: 1fr; }
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
      <span>Control integral del evento, proyectos, tokens, check-in y seguimiento</span>
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
      <div class="muted">
        Ingresa tu clave para habilitar el panel. El sistema mostrará acciones según el rol.
      </div>

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
      <div class="card span-12">
        <div class="section-title">
          <div class="left">
            <h2>Mapa rápido del panel</h2>
            <div class="muted">
              Navega por módulos para que el panel no se sienta amontonado.
            </div>
          </div>
        </div>

        <div class="quick-nav">
          <button type="button" onclick="scrollToSection('dashboardSection')">Dashboard</button>
          <button type="button" onclick="scrollToSection('eventsSection')">Temporadas</button>
          <button type="button" onclick="scrollToSection('masterProjectsSection')">Proyectos maestros</button>
          <button type="button" onclick="scrollToSection('eventProjectsSection')">Proyectos en temporada</button>
          <button type="button" onclick="scrollToSection('tokensSection')">Tokens</button>
          <button type="button" onclick="scrollToSection('checkinSection')">Check-in staff</button>
          <button type="button" onclick="scrollToSection('incidentsSection')">Incidentes</button>
        </div>
      </div>

      <div class="card span-12 section-anchor" id="dashboardSection">
        <div class="section-title">
          <div class="left">
            <h2>Dashboard</h2>
            <div class="muted">
              Vista ejecutiva del evento y de los proyectos cargados en la temporada seleccionada.
            </div>
          </div>
        </div>

        <div class="form-grid">
          <div class="field">
            <label>Temporada para dashboard</label>
            <select id="dashboardEventSelector"></select>
          </div>
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="loadDashboard()">Cargar dashboard</button>
          <button type="button" class="btn-secondary" onclick="loadEvents()">Recargar temporadas</button>
        </div>

        <div id="dashboardSummary" class="stats-grid"></div>

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

      <div class="card span-12 section-anchor" id="eventsSection">
        <div class="section-title">
          <div class="left">
            <h2>Temporadas</h2>
            <div class="muted">
              Crea temporadas, cambia estado y decide cuál queda visible para estudiantes.
            </div>
          </div>
        </div>

        <div class="subgrid">
          <div>
            <h3>Crear temporada</h3>
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
              <button type="button" class="btn-primary" onclick="createAdminEvent()">Crear temporada</button>
              <button type="button" class="btn-secondary" onclick="loadEvents()">Recargar</button>
            </div>
          </div>

          <div>
            <h3>Operar temporada</h3>
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
            </div>

            <div id="selectedEventInfo" class="list"></div>
          </div>
        </div>

        <div id="eventsList" class="list"></div>
      </div>

      <div class="card span-12 section-anchor" id="masterProjectsSection">
        <div class="section-title">
          <div class="left">
            <h2>Proyectos maestros</h2>
            <div class="muted">
              Crea la ficha completa del proyecto base y luego asígnalo a una temporada.
            </div>
          </div>
        </div>

        <div class="subgrid">
          <div>
            <h3>Crear proyecto maestro</h3>

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

          <div>
            <h3>Import / Export</h3>
            <div class="muted">
              Importa proyectos maestros desde Excel o exporta el catálogo base actual.
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Archivo Excel (.xlsx)</label>
                <input id="importProjectsFile" type="file" accept=".xlsx">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="importProjects()">Importar proyectos</button>
              <button type="button" class="btn-secondary" onclick="exportProjects()">Exportar proyectos</button>
            </div>

            <div id="importProjectsResult" class="list"></div>
          </div>
        </div>

        <div class="form-grid" style="margin-top:18px;">
          <div class="field">
            <label>Buscar proyecto maestro</label>
            <input id="masterProjectsSearch" placeholder="Buscar por nombre, organización, líder..." oninput="loadMasterProjects()">
          </div>
        </div>

        <div id="masterProjectsList" class="list"></div>
      </div>

      <div class="card span-12 section-anchor" id="eventProjectsSection">
        <div class="section-title">
          <div class="left">
            <h2>Proyectos en temporada</h2>
            <div class="muted">
              Vincula proyectos maestros a una temporada y define su cupo real para ese evento.
            </div>
          </div>
        </div>

        <div class="form-grid">
          <div class="field">
            <label>Temporada</label>
            <select id="eventProjectEventSelector"></select>
          </div>

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

      <div class="card span-12 section-anchor" id="tokensSection">
        <div class="section-title">
          <div class="left">
            <h2>Tokens de inscripción</h2>
            <div class="muted">
              Genera, lista y revoca tokens de los proyectos en temporada.
            </div>
          </div>
        </div>

        <div class="subgrid">
          <div>
            <h3>Configuración y generación</h3>

            <div class="form-grid">
              <div class="field">
                <label>Proyecto en temporada</label>
                <select id="tokensEventProjectSelector"></select>
              </div>

              <div class="field">
                <label>Cantidad a generar</label>
                <input id="tokensCount" type="number" min="1" max="200" value="5">
              </div>

              <div class="field">
                <label>Longitud del token</label>
                <input id="tokensLength" type="number" min="6" max="20" value="10">
              </div>

              <div class="field">
                <label>TTL global (horas)</label>
                <input id="ttl_hours" type="number" min="1" max="168" value="24">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="generateProjectTokens()">Generar tokens</button>
              <button type="button" class="btn-secondary" onclick="loadTokenTTL()">Recargar TTL</button>
              <button type="button" class="btn-secondary" onclick="saveTokenTTL()">Guardar TTL</button>
            </div>

            <div class="small" style="margin-top:10px;">
              Valor actual: <span id="ttl_current" class="pill pill-neutral">—</span>
            </div>

            <div id="tokensGenerationResult" class="list"></div>
          </div>

          <div>
            <h3>Revocar token</h3>

            <div class="form-grid">
              <div class="field">
                <label>Token</label>
                <input id="revokeTokenValue" placeholder="Ej: ABCDE23456">
              </div>

              <div class="field">
                <label>Motivo</label>
                <input id="revokeTokenReason" placeholder="Ej: Error del líder">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-danger" onclick="revokeProjectToken()">Revocar token</button>
            </div>
          </div>
        </div>

        <div class="form-grid" style="margin-top:18px;">
          <div class="field">
            <label>Filtrar estado de tokens</label>
            <select id="tokensStatusFilter" onchange="loadProjectTokens()">
              <option value="ALL">Todos</option>
              <option value="AVAILABLE">Available</option>
              <option value="RESERVED">Reserved</option>
              <option value="USED">Used</option>
              <option value="REVOKED">Revoked</option>
              <option value="EXPIRED">Expired</option>
            </select>
          </div>
        </div>

        <div id="tokensSummary" class="stats-grid"></div>

        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Token</th>
                <th>Estado</th>
                <th>Reservado por request</th>
                <th>Reserved until</th>
                <th>Usado por request</th>
                <th>Usado</th>
                <th>Revocado</th>
                <th>Expira</th>
                <th>Creado</th>
              </tr>
            </thead>
            <tbody id="tokensTableBody">
              <tr><td colspan="9" class="small">Selecciona un proyecto en temporada y carga tokens.</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card span-12 section-anchor" id="checkinSection">
        <div class="section-title">
          <div class="left">
            <h2>Check-in Staff / Lector QR</h2>
            <div class="muted">
              Escanea el QR, revisa los datos del alumno y habilita acceso validando matrícula física.
            </div>
          </div>
        </div>

        <div class="form-grid">
          <div class="field">
            <label>QR escaneado</label>
            <input id="staffScannedToken" placeholder="Aquí aparece el token escaneado o puedes pegarlo manualmente">
          </div>

          <div class="field">
            <label>Matrícula física presentada</label>
            <input id="staffPhysicalEnrolment" placeholder="Ej: A01234567">
          </div>
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="startQrScanner()">Abrir cámara</button>
          <button type="button" class="btn-secondary" onclick="stopQrScanner()">Detener cámara</button>
          <button type="button" class="btn-secondary" onclick="scanStaffQr()">Verificar QR</button>
          <button type="button" class="btn-primary" onclick="grantStaffAccess()">Dar acceso</button>
        </div>

        <div id="staffScanner" style="width:100%; max-width:420px; margin-top:18px;"></div>
        <div id="staffCheckinInfo" class="list"></div>
      </div>

      <div class="card span-12 section-anchor" id="incidentsSection">
        <div class="section-title">
          <div class="left">
            <h2>Incidentes</h2>
            <div class="muted">
              Reporta y da seguimiento a casos operativos, errores, conflictos o excepciones.
            </div>
          </div>
        </div>

        <div class="subgrid">
          <div>
            <h3>Reportar caso</h3>

            <div class="form-grid">
              <div class="field">
                <label>Temporada / Event ID</label>
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
            </div>
          </div>

          <div>
            <h3>Consultar incidentes</h3>

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

            <div class="actions">
              <button type="button" class="btn-secondary" onclick="loadIncidents()">Recargar incidentes</button>
            </div>

            <div id="incidentsList" class="list"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const storage = sessionStorage;
    let staffQrScanner = null;
    let lastScannedPassSession = null;
    let allEvents = [];
    let masterProjectsCache = [];
    let eventProjectsCache = [];

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

    function boolFromString(v) {
      return String(v).toLowerCase() === 'true';
    }

    function toSqlDateTime(value) {
      if (!value) return null;
      return value.replace('T', ' ') + ':00';
    }

    function scrollToSection(id) {
      const el = document.getElementById(id);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
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

    function fillSelect(id, items, placeholderText='Selecciona', labelFn=null) {
      const el = document.getElementById(id);
      if (!el) return;
      el.innerHTML = `<option value="">${placeholderText}</option>`;
      for (const item of items || []) {
        const opt = document.createElement('option');
        opt.value = item.id;
        opt.textContent = labelFn ? labelFn(item) : (item.name || item.description || item.display_name || item.id);
        el.appendChild(opt);
      }
    }

    function fillSelectNoBlank(id, items, labelFn=null) {
      const el = document.getElementById(id);
      if (!el) return;
      el.innerHTML = '';
      for (const item of items || []) {
        const opt = document.createElement('option');
        opt.value = item.id;
        opt.textContent = labelFn ? labelFn(item) : (item.name || item.description || item.display_name || item.id);
        el.appendChild(opt);
      }
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
        loadAdminCatalogs(),
        loadMasterProjects(),
        loadTokenTTL()
      ]);
    }

    async function createAdminEvent() {
      try {
        const year = Number(document.getElementById('eventYear').value);
        const season = document.getElementById('eventSeason').value;
        const status = document.getElementById('eventStatus').value;
        const isVisible = boolFromString(document.getElementById('eventVisible').value);

        if (!year || year < 2020 || year > 2100) {
          return showMsg('Año inválido', false);
        }

        const payload = {
          year,
          season,
          status,
          is_visible_to_students: isVisible,
          catalog_open_at: toSqlDateTime(document.getElementById('eventCatalogOpenAt').value),
          onsite_start_at: toSqlDateTime(document.getElementById('eventOnsiteStartAt').value),
          onsite_end_at: toSqlDateTime(document.getElementById('eventOnsiteEndAt').value),
          registration_close_at: toSqlDateTime(document.getElementById('eventRegistrationCloseAt').value)
        };

        const data = await postJSON('/api/admin/events', payload);
        showMsg(data.message || 'Temporada creada');
        await loadEvents();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function loadEvents() {
      try {
        const data = await getJSONAuth('/api/admin/events');
        allEvents = data || [];

        const eventsList = document.getElementById('eventsList');
        const eventSelector = document.getElementById('eventSelector');
        const dashboardSelector = document.getElementById('dashboardEventSelector');
        const eventProjectSelector = document.getElementById('eventProjectEventSelector');

        eventsList.innerHTML = '';

        fillSelectNoBlank('eventSelector', allEvents, e => `${e.display_name} · ${e.status}`);
        fillSelectNoBlank('dashboardEventSelector', allEvents, e => `${e.display_name} · ${e.status}`);
        fillSelectNoBlank('eventProjectEventSelector', allEvents, e => `${e.display_name} · ${e.status}`);

        if (!allEvents.length) {
          eventsList.innerHTML = `<div class="item"><div class="small">No hay temporadas creadas todavía.</div></div>`;
          document.getElementById('selectedEventInfo').innerHTML = '';
          return showMsg('No hay temporadas creadas todavía');
        }

        eventsList.innerHTML = allEvents.map(e => `
          <div class="item">
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

            <div class="meta">
              <div class="meta-box">
                <span class="meta-label">Catálogo abre</span>
                <div class="meta-value">${escapeHTML(e.catalog_open_at || '—')}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Inicio presencial</span>
                <div class="meta-value">${escapeHTML(e.onsite_start_at || '—')}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Fin presencial</span>
                <div class="meta-value">${escapeHTML(e.onsite_end_at || '—')}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Cierre registro</span>
                <div class="meta-value">${escapeHTML(e.registration_close_at || '—')}</div>
              </div>
            </div>
          </div>
        `).join('');

        if (eventSelector.options.length) eventSelector.selectedIndex = 0;
        if (dashboardSelector.options.length) dashboardSelector.selectedIndex = 0;
        if (eventProjectSelector.options.length) eventProjectSelector.selectedIndex = 0;

        await loadSelectedEventInfo();
        await loadEventProjects();
        await loadDashboard();
        await loadIncidents();
      } catch (e) {
        showMsg(e.message, false);
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
        fillSelect('mp_partner', data.socio || [], 'Selecciona', item => item.name);
        fillSelect('mp_modality', data.modalidad || [], 'Selecciona', item => item.description);
        fillSelect('mp_week_days', data.dias || [], 'Selecciona', item => item.description);
        fillSelect('mp_schedule', data.horario || [], 'Selecciona', item => item.description);
      } catch (e) {
        showMsg('Error cargando catálogos admin: ' + e.message, false);
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

        masterProjectsCache = data || [];

        fillSelect('projectSelector', masterProjectsCache, 'Selecciona proyecto', p => `${p.general_name || 'Sin nombre general'} | ${p.name}`);

        const list = document.getElementById('masterProjectsList');
        if (!masterProjectsCache.length) {
          list.innerHTML = `<div class="item"><div class="small">No hay proyectos maestros.</div></div>`;
          return;
        }

        list.innerHTML = masterProjectsCache.map(p => `
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
          </div>
        `).join('');
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function importProjects() {
      try {
        const fileInput = document.getElementById('importProjectsFile');
        const file = fileInput.files?.[0];
        if (!file) return showMsg('Selecciona un archivo Excel', false);

        const formData = new FormData();
        formData.append('file', file);

        const r = await fetch('/api/admin/projects/import', {
          method: 'POST',
          headers: { 'X-ADMIN-KEY': getKey() },
          body: formData
        });

        const data = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(data.error || ('Error ' + r.status));

        document.getElementById('importProjectsResult').innerHTML = `
          <div class="item">
            <div class="item-title">${escapeHTML(data.message || 'Importación completada')}</div>
            <div class="small">Insertados: ${data.inserted || 0} · Fallidos: ${data.failed || 0}</div>
            ${(data.errors && data.errors.length)
              ? `<div class="list" style="margin-top:10px;">${data.errors.map(e => `<div class="item"><div class="small">Fila ${e.row}: ${escapeHTML(e.error)}</div></div>`).join('')}</div>`
              : '<div class="small" style="margin-top:10px;">Sin errores.</div>'}
          </div>
        `;

        showMsg(data.message || 'Importación completada');
        await loadMasterProjects();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    function exportProjects() {
      window.open('/api/admin/projects/export', '_blank');
    }

    async function addProjectToEvent() {
      const eventId = document.getElementById('eventProjectEventSelector').value;
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
      const eventId = document.getElementById('eventProjectEventSelector').value;
      const container = document.getElementById('eventProjectsList');

      if (!eventId) {
        container.innerHTML = `<div class="item"><div class="small">Selecciona una temporada.</div></div>`;
        return;
      }

      try {
        const data = await getJSONAuth(`/api/admin/events/${eventId}/projects`);
        eventProjectsCache = data || [];

        fillSelect('tokensEventProjectSelector', eventProjectsCache, 'Selecciona proyecto en temporada', p => `${p.name} · ${p.partner || '—'} · EventProject ${p.id}`);

        if (!eventProjectsCache.length) {
          container.innerHTML = `<div class="item"><div class="small">No hay proyectos cargados en esta temporada.</div></div>`;
          return;
        }

        container.innerHTML = eventProjectsCache.map(p => `
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

    async function generateProjectTokens() {
      try {
        const eventProjectId = document.getElementById('tokensEventProjectSelector').value;
        const count = Number(document.getElementById('tokensCount').value || 0);
        const length = Number(document.getElementById('tokensLength').value || 0);

        if (!eventProjectId) return showMsg('Selecciona un proyecto en temporada', false);

        const data = await postJSON(`/api/admin/event-projects/${eventProjectId}/tokens`, {
          count,
          length
        });

        document.getElementById('tokensGenerationResult').innerHTML = `
          <div class="item">
            <div class="item-title">${escapeHTML(data.message || 'Tokens generados')}</div>
            <div class="small">Creados: ${data.created || 0} · TTL: ${data.ttl_hours || '—'} horas</div>
            <div class="mono" style="margin-top:10px;">${(data.tokens || []).join(', ')}</div>
          </div>
        `;

        showMsg(data.message || 'Tokens generados');
        await loadProjectTokens();
        await loadDashboard();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function loadProjectTokens() {
      const eventProjectId = document.getElementById('tokensEventProjectSelector').value;
      const status = document.getElementById('tokensStatusFilter').value || 'ALL';

      if (!eventProjectId) {
        document.getElementById('tokensTableBody').innerHTML = `<tr><td colspan="9" class="small">Selecciona un proyecto en temporada.</td></tr>`;
        return;
      }

      try {
        const data = await getJSONAuth(`/api/admin/event-projects/${eventProjectId}/tokens?status=${encodeURIComponent(status)}`);
        const s = data.summary || {};

        document.getElementById('tokensSummary').innerHTML = `
          <div class="stat-card"><div class="stat-label">Available</div><div class="stat-value">${s.available || 0}</div></div>
          <div class="stat-card"><div class="stat-label">Reserved</div><div class="stat-value">${s.reserved || 0}</div></div>
          <div class="stat-card"><div class="stat-label">Used</div><div class="stat-value">${s.used || 0}</div></div>
          <div class="stat-card"><div class="stat-label">Revoked</div><div class="stat-value">${s.revoked || 0}</div></div>
          <div class="stat-card"><div class="stat-label">Expired</div><div class="stat-value">${s.expired || 0}</div></div>
          <div class="stat-card"><div class="stat-label">Total</div><div class="stat-value">${s.total || 0}</div></div>
        `;

        const items = data.items || [];
        document.getElementById('tokensTableBody').innerHTML = items.length
          ? items.map(t => `
              <tr>
                <td class="mono">${escapeHTML(t.token_value || '—')}</td>
                <td>${escapeHTML(t.status || '—')}</td>
                <td>${escapeHTML(t.reserved_by_request_id || '—')}</td>
                <td>${escapeHTML(t.reserved_until || '—')}</td>
                <td>${escapeHTML(t.used_by_request_id || '—')}</td>
                <td>${escapeHTML(t.used_at || '—')}</td>
                <td>${escapeHTML(t.revoked_at || '—')}</td>
                <td>${escapeHTML(t.expires_at || '—')}</td>
                <td>${escapeHTML(t.created_at || '—')}</td>
              </tr>
            `).join('')
          : `<tr><td colspan="9" class="small">No hay tokens con ese filtro.</td></tr>`;
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function revokeProjectToken() {
      try {
        const token = document.getElementById('revokeTokenValue').value.trim().toUpperCase();
        const reason = document.getElementById('revokeTokenReason').value.trim();

        if (!token) return showMsg('Escribe un token', false);

        const data = await postJSON('/api/admin/project-tokens/revoke', { token, reason });
        showMsg(data.message || 'Token revocado');
        await loadProjectTokens();
        await loadDashboard();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function loadDashboard() {
      const eventId = document.getElementById('dashboardEventSelector').value;
      if (!eventId) return;

      try {
        const summary = await getJSONAuth(`/api/admin/dashboard/summary?event_id=${eventId}`);
        const projects = await getJSONAuth(`/api/admin/dashboard/projects?event_id=${eventId}`);

        document.getElementById('dashboardSummary').innerHTML = `
          <div class="stat-card"><div class="stat-label">Solicitudes</div><div class="stat-value">${summary.requests.total}</div></div>
          <div class="stat-card"><div class="stat-label">Requested</div><div class="stat-value">${summary.requests.requested}</div></div>
          <div class="stat-card"><div class="stat-label">Validated</div><div class="stat-value">${summary.requests.validated}</div></div>
          <div class="stat-card"><div class="stat-label">Access Enabled</div><div class="stat-value">${summary.requests.access_enabled}</div></div>
          <div class="stat-card"><div class="stat-label">Registered</div><div class="stat-value">${summary.requests.registered}</div></div>
          <div class="stat-card"><div class="stat-label">Incidentes abiertos</div><div class="stat-value">${summary.incidents.open}</div></div>
        `;

        const body = document.getElementById('dashboardProjectsBody');
        const items = projects || [];
        body.innerHTML = items.length
          ? items.map(p => `
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
            `).join('')
          : `<tr><td colspan="9" class="small">No hay proyectos cargados en esta temporada.</td></tr>`;
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function startQrScanner() {
      try {
        if (staffQrScanner) {
          await stopQrScanner();
        }

        staffQrScanner = new Html5Qrcode("staffScanner");

        await staffQrScanner.start(
          { facingMode: "environment" },
          {
            fps: 10,
            qrbox: { width: 220, height: 220 }
          },
          async (decodedText) => {
            document.getElementById('staffScannedToken').value = decodedText;
            await scanStaffQr();
          },
          (errorMessage) => {}
        );

        showMsg('Cámara activa para escaneo QR');
      } catch (e) {
        showMsg('No se pudo abrir la cámara: ' + e.message, false);
      }
    }

    async function stopQrScanner() {
      try {
        if (staffQrScanner) {
          await staffQrScanner.stop();
          await staffQrScanner.clear();
          staffQrScanner = null;
          showMsg('Cámara detenida');
        }
      } catch (e) {
        showMsg('Error al detener cámara: ' + e.message, false);
      }
    }

    async function scanStaffQr() {
      try {
        const token = document.getElementById('staffScannedToken').value.trim();
        if (!token) return showMsg('Escanea o pega primero un QR/token', false);

        const data = await postJSON('/api/staff/checkin/scan', { token });
        lastScannedPassSession = data.pass_session?.id || null;

        document.getElementById('staffCheckinInfo').innerHTML = `
          <div class="item">
            <div class="item-head">
              <div>
                <div class="item-title">${escapeHTML(data.student?.full_name || 'Alumno')}</div>
                <div class="small">Matrícula registrada: ${escapeHTML(data.student?.enrolment_number || '—')}</div>
              </div>
              <div>${statusPill(data.request?.status || 'REQUESTED')}</div>
            </div>

            <div class="meta">
              <div class="meta-box"><span class="meta-label">Folio</span><div class="meta-value">${escapeHTML(data.request?.folio || '—')}</div></div>
              <div class="meta-box"><span class="meta-label">Temporada</span><div class="meta-value">${escapeHTML(data.event?.display_name || '—')}</div></div>
              <div class="meta-box"><span class="meta-label">QR expira</span><div class="meta-value">${escapeHTML(data.pass_session?.expires_at || '—')}</div></div>
              <div class="meta-box"><span class="meta-label">Carrera</span><div class="meta-value">${escapeHTML(data.student?.degree || '—')}</div></div>
            </div>
          </div>
        `;

        showMsg('QR válido. Verifica ahora la matrícula física.');
      } catch (e) {
        lastScannedPassSession = null;
        document.getElementById('staffCheckinInfo').innerHTML = '';
        showMsg(e.message, false);
      }
    }

    async function grantStaffAccess() {
      try {
        const passSessionId = lastScannedPassSession;
        const enrolment = document.getElementById('staffPhysicalEnrolment').value.trim();

        if (!passSessionId) return showMsg('Primero debes verificar el QR', false);
        if (!enrolment) return showMsg('Falta capturar la matrícula física', false);

        const data = await postJSON('/api/staff/checkin/grant-access', {
          pass_session_id: passSessionId,
          enrolment_number: enrolment
        });

        showMsg(data.message || 'Acceso habilitado');
        document.getElementById('staffCheckinInfo').innerHTML += `
          <div class="item">
            <div class="item-title">Acceso habilitado correctamente</div>
            <div class="small">El alumno ya puede entrar al catálogo y cerrar inscripción.</div>
          </div>
        `;
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
      const eventId = document.getElementById('eventSelector').value || document.getElementById('dashboardEventSelector').value;
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
        document.getElementById('incidentEventId').value = document.getElementById('eventSelector').value || '';
      });

      document.getElementById('dashboardEventSelector').addEventListener('change', async () => {
        await loadDashboard();
      });

      document.getElementById('eventProjectEventSelector').addEventListener('change', async () => {
        await loadEventProjects();
      });

      document.getElementById('tokensEventProjectSelector').addEventListener('change', async () => {
        await loadProjectTokens();
      });
    });
  </script>
</body>
</html>
"""