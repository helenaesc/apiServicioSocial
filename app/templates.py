INDEX_HTML = r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Registro de Proyectos</title>
  <style>
    :root {
      --bg: #f4f7fb;
      --panel: #ffffff;
      --text: #0f172a;
      --muted: #64748b;
      --line: #e2e8f0;
      --primary: #2563eb;
      --primary-dark: #1d4ed8;
      --accent: #0ea5e9;
      --success-bg: #dcfce7;
      --success-text: #166534;
      --danger-bg: #fee2e2;
      --danger-text: #991b1b;
      --warn-bg: #fff7ed;
      --warn-text: #9a3412;
      --shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
      --radius-xl: 22px;
      --radius-lg: 18px;
      --radius-md: 14px;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 28%),
        radial-gradient(circle at top right, rgba(14, 165, 233, 0.12), transparent 24%),
        linear-gradient(180deg, #f8fbff 0%, var(--bg) 100%);
      color: var(--text);
      min-height: 100vh;
    }

    .hidden { display: none !important; }

    .hero {
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #0ea5e9 100%);
      color: white;
      padding: 36px 20px 72px;
    }

    .hero-inner {
      max-width: 1150px;
      margin: 0 auto;
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: .82rem;
      letter-spacing: .04em;
      text-transform: uppercase;
      background: rgba(255,255,255,.12);
      border: 1px solid rgba(255,255,255,.18);
      padding: 8px 12px;
      border-radius: 999px;
    }

    h1 {
      margin: 16px 0 10px;
      font-size: clamp(2rem, 4vw, 3rem);
      line-height: 1.05;
      letter-spacing: -0.03em;
    }

    .hero p {
      margin: 0;
      max-width: 760px;
      color: rgba(255,255,255,.88);
      font-size: 1rem;
      line-height: 1.6;
    }

    .screen, .container {
      max-width: 1150px;
      margin: -40px auto 32px;
      padding: 0 16px 24px;
      position: relative;
      z-index: 2;
    }

    .panel {
      background: var(--panel);
      border: 1px solid rgba(255,255,255,.7);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow);
      padding: 24px;
    }

    .panel-header {
      text-align: center;
      margin-bottom: 20px;
    }

    .panel-header h2 {
      margin: 0 0 8px;
      font-size: 1.7rem;
    }

    .panel-header p {
      margin: 0;
      color: var(--muted);
    }

    .msg {
      margin-top: 12px;
      min-height: 20px;
      font-size: .93rem;
      font-weight: 600;
    }

    .msg.ok { color: var(--success-text); }
    .msg.error { color: var(--danger-text); }

    .season-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 18px;
    }

    .season-card {
      border: 1px solid #e2e8f0;
      background: white;
      border-radius: var(--radius-lg);
      padding: 22px;
      text-align: left;
      cursor: pointer;
      box-shadow: 0 8px 18px rgba(15, 23, 42, .05);
      transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    .season-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 18px 36px rgba(15, 23, 42, .11);
      border-color: #cfe0f6;
    }

    .season-badge {
      display: inline-block;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: .78rem;
      font-weight: 800;
      margin-bottom: 14px;
    }

    .badge-spring { background: #dcfce7; color: #166534; }
    .badge-winter { background: #dbeafe; color: #1d4ed8; }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .field label {
      font-size: .82rem;
      font-weight: 600;
      color: #334155;
    }

    input, select, button, textarea {
      width: 100%;
      min-height: 46px;
      border-radius: 14px;
      font-size: .95rem;
      transition: .2s ease;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.92);
      color: var(--text);
      padding: 10px 14px;
      outline: none;
    }

    textarea { min-height: 100px; resize: vertical; }

    input:focus, select:focus, textarea:focus {
      border-color: rgba(37, 99, 235, .5);
      box-shadow: 0 0 0 4px rgba(37, 99, 235, .10);
      background: white;
    }

    .actions {
      display: flex;
      gap: 10px;
      align-items: end;
      flex-wrap: wrap;
      margin-top: 16px;
    }

    button {
      border: none;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
      color: white;
      box-shadow: 0 10px 20px rgba(37, 99, 235, .20);
    }

    .btn-primary:hover { background: var(--primary-dark); }

    .btn-secondary {
      background: #eef2f7;
      color: #334155;
      border: 1px solid #dbe3ee;
    }

    .btn-danger {
      background: #ef4444;
      color: white;
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 10px;
      border-radius: 999px;
      font-size: .78rem;
      font-weight: 800;
      white-space: nowrap;
    }

    .status-requested { background: #f1f5f9; color: #334155; }
    .status-validated { background: #dbeafe; color: #1d4ed8; }
    .status-access-enabled { background: #dcfce7; color: #166534; }
    .status-registered { background: #ede9fe; color: #6d28d9; }
    .status-cancelled, .status-closed { background: #fee2e2; color: #991b1b; }

    .card {
      background: white;
      border: 1px solid #e9eef5;
      border-radius: 20px;
      padding: 18px;
      box-shadow: 0 10px 22px rgba(15, 23, 42, .05);
      position: relative;
      overflow: hidden;
    }

    .card::before {
      content: "";
      position: absolute;
      inset: 0 0 auto 0;
      height: 4px;
      background: linear-gradient(90deg, var(--primary), var(--accent));
    }

    .card-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      margin-bottom: 12px;
    }

    .title {
      font-size: 1.08rem;
      font-weight: 800;
      line-height: 1.3;
      color: var(--text);
      margin: 0;
    }

    .status {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 10px;
      border-radius: 999px;
      font-size: .78rem;
      font-weight: 800;
      white-space: nowrap;
    }

    .status.available {
      background: var(--success-bg);
      color: var(--success-text);
    }

    .status.full {
      background: var(--danger-bg);
      color: var(--danger-text);
    }

    .meta-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 14px;
    }

    .meta-item {
      background: #f8fafc;
      border: 1px solid #eef2f7;
      border-radius: 14px;
      padding: 10px 12px;
    }

    .meta-label {
      display: block;
      font-size: .75rem;
      color: var(--muted);
      margin-bottom: 4px;
      text-transform: uppercase;
      letter-spacing: .03em;
      font-weight: 700;
    }

    .meta-value {
      font-size: .92rem;
      color: #0f172a;
      font-weight: 600;
      line-height: 1.35;
    }

    .desc {
      color: #334155;
      font-size: .94rem;
      line-height: 1.6;
      margin-top: 12px;
    }

    .filters {
      background: var(--panel);
      border: 1px solid rgba(255,255,255,.7);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow);
      padding: 18px;
    }

    .filters-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }

    .filter-grid {
      display: grid;
      grid-template-columns: 1.4fr repeat(4, minmax(140px, 1fr)) auto;
      gap: 12px;
    }

    .toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-top: 20px;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }

    .season-chip {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: white;
      border: 1px solid #dbe3ee;
      border-radius: 999px;
      padding: 8px 12px;
      font-size: .9rem;
      font-weight: 700;
      color: #1e293b;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 16px;
    }

    .empty, .loading {
      background: white;
      border: 1px solid #e9eef5;
      border-radius: 18px;
      padding: 24px;
      text-align: center;
      color: #475569;
      box-shadow: 0 10px 22px rgba(15, 23, 42, .05);
    }

    .pass-box {
      display: grid;
      grid-template-columns: 1.2fr .8fr;
      gap: 20px;
    }

    .qr-box {
      border: 2px dashed #cbd5e1;
      border-radius: 18px;
      min-height: 260px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      background: #f8fafc;
      padding: 16px;
    }

    .mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      background: #0f172a;
      color: #e2e8f0;
      padding: 8px 10px;
      border-radius: 10px;
      word-break: break-word;
      font-size: .9rem;
    }

    .mini {
      font-size: .84rem;
      color: var(--muted);
      line-height: 1.5;
    }

    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, .45);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 18px;
      z-index: 999;
    }

    .modal {
      width: min(720px, 100%);
      background: white;
      border-radius: 20px;
      box-shadow: 0 30px 60px rgba(0,0,0,.18);
      padding: 22px;
    }

    .checkbox-row {
      display: flex;
      gap: 10px;
      align-items: flex-start;
      margin-top: 14px;
    }

    .checkbox-row input[type="checkbox"] {
      width: 18px;
      min-height: 18px;
      margin-top: 3px;
    }

    @media (max-width: 980px) {
      .filter-grid { grid-template-columns: 1fr 1fr; }
      .pass-box { grid-template-columns: 1fr; }
    }

    @media (max-width: 640px) {
      .filter-grid { grid-template-columns: 1fr; }
      .meta-grid { grid-template-columns: 1fr; }
      .card-head { flex-direction: column; align-items: start; }
      .actions { flex-direction: column; align-items: stretch; }
      .actions button { width: 100%; }
    }
  </style>
</head>
<body>
  <section class="hero">
    <div class="hero-inner">
      <div class="eyebrow">Sistema de Registro</div>
      <h1 id="heroTitle">Solicita tu pase</h1>
      <p id="heroSubtitle">
        Elige temporada, solicita tu pase, muestra tu credencial en el evento y cierra tu inscripción con el proyecto.
      </p>
    </div>
  </section>

  <!-- 1. Selección de temporada -->
  <section id="seasonScreen" class="screen">
    <div class="panel">
      <div class="panel-header">
        <h2>Elige una temporada</h2>
        <p>Selecciona la temporada en la que deseas consultar proyectos y solicitar tu pase.</p>
      </div>

      <div class="season-grid">
        <button class="season-card" onclick="selectSeason('PRIMAVERA')">
          <span class="season-badge badge-spring">Primavera</span>
          <h3>Primavera</h3>
          <p>Consulta y participa en la temporada de primavera.</p>
        </button>

        <button class="season-card" onclick="selectSeason('INVIERNO')">
          <span class="season-badge badge-winter">Invierno</span>
          <h3>Invierno</h3>
          <p>Consulta y participa en la temporada de invierno.</p>
        </button>
      </div>
    </div>
  </section>

  <!-- 2. Solicitar pase -->
  <section id="requestScreen" class="screen hidden">
    <div class="panel">
      <div class="panel-header">
        <h2>Solicitar pase</h2>
        <p>Completa tus datos para generar tu folio y tu credencial digital.</p>
      </div>

      <div class="form-grid">
        <div class="field">
          <label for="full_name">Nombre completo</label>
          <input id="full_name" placeholder="Ej: Juan Pérez López">
        </div>

        <div class="field">
          <label for="enrolment_number">Matrícula</label>
          <input id="enrolment_number" placeholder="Ej: A01234567">
        </div>

        <div class="field">
          <label for="email">Correo principal</label>
          <input id="email" placeholder="correo@ejemplo.com">
        </div>

        <div class="field">
          <label for="second_email">Segundo correo (opcional)</label>
          <input id="second_email" placeholder="otrocorreo@ejemplo.com">
        </div>

        <div class="field">
          <label for="phone_number">Teléfono (opcional)</label>
          <input id="phone_number" placeholder="Teléfono">
        </div>

        <div class="field">
          <label for="degree">Carrera (opcional)</label>
          <input id="degree" placeholder="Ej: ITC">
        </div>

        <div class="field">
          <label for="semester">Semestre (opcional)</label>
          <input id="semester" type="number" min="1" max="20" placeholder="Semestre">
        </div>
      </div>

      <div class="actions">
        <button class="btn-primary" onclick="submitStudentRequest()">Solicitar pase</button>
        <button class="btn-secondary" onclick="goBackToSeason()">Cambiar temporada</button>
      </div>

      <div id="requestMsg" class="msg"></div>
    </div>
  </section>

  <!-- 3. Credencial viva -->
  <section id="passScreen" class="screen hidden">
    <div class="panel">
      <div class="panel-header">
        <h2>Mi credencial</h2>
        <p>Muéstrala en la entrada. Cuando el staff te lo indique, refresca tu código y enseña tu matrícula física.</p>
      </div>

      <div class="pass-box">
        <div>
          <div class="meta-grid">
            <div class="meta-item">
              <span class="meta-label">Alumno</span>
              <div id="passStudentName" class="meta-value">—</div>
            </div>
            <div class="meta-item">
              <span class="meta-label">Matrícula</span>
              <div id="passEnrolment" class="meta-value">—</div>
            </div>
            <div class="meta-item">
              <span class="meta-label">Temporada</span>
              <div id="passSeason" class="meta-value">—</div>
            </div>
            <div class="meta-item">
              <span class="meta-label">Folio</span>
              <div id="passFolio" class="meta-value">—</div>
            </div>
            <div class="meta-item">
              <span class="meta-label">Estado</span>
              <div id="passStatusWrap" class="meta-value">—</div>
            </div>
            <div class="meta-item">
              <span class="meta-label">Expira</span>
              <div id="passExpiresAt" class="meta-value">—</div>
            </div>
          </div>

          <div class="actions">
            <button class="btn-primary" onclick="refreshStudentPass()">Refrescar código</button>
            <button id="goToCatalogBtn" class="btn-secondary hidden" onclick="openCatalog()">Entrar al catálogo</button>
            <button class="btn-secondary" onclick="reloadStudentPass()">Actualizar estado</button>
          </div>

          <div id="passMsg" class="msg"></div>
        </div>

        <div class="qr-box">
          <div class="mini" style="margin-bottom:10px;"><strong>Código vigente del pase</strong></div>
          <div id="qrPlaceholder" class="mono">Genera tu código</div>
          <div class="mini" style="margin-top:12px; text-align:center;">
            Este código cambia al refrescarse y deja de servir al expirar o cuando el staff lo usa.
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 4. Catálogo -->
  <main id="catalogScreen" class="container hidden">
    <section class="filters">
      <div class="filters-top">
        <div>
          <div style="font-size:1rem;font-weight:700;color:var(--text);">Búsqueda y filtros</div>
          <div style="color:var(--muted);font-size:.92rem;">Refina el catálogo con criterios específicos.</div>
        </div>
        <div id="seasonChip" class="season-chip hidden"></div>
      </div>

      <div class="filter-grid">
        <div class="field">
          <label for="q">Búsqueda</label>
          <input id="q" placeholder="Buscar por proyecto o descripción">
        </div>

        <div class="field">
          <label for="socio">Carrera</label>
          <select id="socio"><option value="">Todos</option></select>
        </div>

        <div class="field">
          <label for="modalidad">Modalidad</label>
          <select id="modalidad"><option value="">Todas</option></select>
        </div>

        <div class="field">
          <label for="dia">Día</label>
          <select id="dia"><option value="">Todos</option></select>
        </div>

        <div class="field">
          <label for="horario">Horario</label>
          <select id="horario"><option value="">Todos</option></select>
        </div>

        <div class="actions">
          <button class="btn-primary" onclick="loadProjects()">Buscar</button>
          <button class="btn-secondary" onclick="clearFilters()">Limpiar</button>
          <button class="btn-secondary" onclick="backToPass()">Volver a credencial</button>
        </div>
      </div>
    </section>

    <div class="toolbar">
      <div>
        <div id="resultsCount" style="font-weight:700;font-size:.96rem;">Cargando catálogo...</div>
        <div style="color:var(--muted);font-size:.9rem;">Consulta disponibilidad y detalles del proyecto.</div>
      </div>
      <button class="btn-secondary" onclick="openCroquis()">Ver croquis</button>
    </div>

    <div id="results" class="loading">Cargando oferta...</div>
  </main>

  <!-- Modal de registro -->
  <div id="registrationModalWrap" class="modal-backdrop hidden">
    <div class="modal">
      <div class="panel-header" style="text-align:left;margin-bottom:16px;">
        <h2 style="margin:0 0 6px;">Cerrar inscripción</h2>
        <p>Confirma tu registro con el token del proyecto y tu aceptación final.</p>
      </div>

      <div class="form-grid">
        <div class="field">
          <label>Proyecto</label>
          <input id="regProjectName" readonly>
        </div>

        <div class="field">
          <label>Token del proyecto</label>
          <input id="regTokenValue" placeholder="Ingresa el token que te dio el líder">
        </div>

        <div class="field">
          <label>Nombre completo para confirmar</label>
          <input id="regAcceptedFullName" placeholder="Escribe tu nombre completo">
        </div>
      </div>

      <div class="checkbox-row">
        <input type="checkbox" id="regAcceptedCheckbox">
        <label for="regAcceptedCheckbox" style="margin:0; font-size:.92rem; color:#334155;">
          Confirmo que este registro lo realizo por decisión propia, que el token fue entregado por el proyecto correcto y que acepto cerrar mi inscripción con este proyecto.
        </label>
      </div>

      <div class="actions">
        <button class="btn-secondary" onclick="previewRegistration()">Validar datos</button>
        <button class="btn-primary" onclick="confirmRegistration()">Confirmar inscripción</button>
        <button class="btn-secondary" onclick="closeRegistrationModal()">Cancelar</button>
      </div>

      <div id="registrationMsg" class="msg"></div>
    </div>
  </div>

  <!-- Modal Croquis -->
  <div id="croquisWrap" class="modal-backdrop hidden">
    <div class="modal">
      <div class="panel-header" style="text-align:left;margin-bottom:16px;">
        <h2 style="margin:0 0 6px;">Croquis del evento</h2>
        <p>Aquí puedes mostrar después la distribución física de proyectos, staff, entrada y zonas importantes.</p>
      </div>

      <div class="empty" style="margin:0;">
        <strong>Croquis pendiente</strong>
        <div class="mini" style="margin-top:8px;">
          Recomendación: usarlo como complemento del catálogo, no como reemplazo.
        </div>
      </div>

      <div class="actions">
        <button class="btn-secondary" onclick="closeCroquis()">Cerrar</button>
      </div>
    </div>
  </div>

  <script>
    let currentSeason = null;
    let currentRequest = null;
    let currentStudent = null;
    let currentEvent = null;
    let currentPass = null;
    let currentProjects = [];
    let selectedProject = null;

    function escapeHTML(value) {
      return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    async function getJSON(url) {
      const response = await fetch(url);
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.error || ('Error ' + response.status));
      return data;
    }

    async function postJSON(url, bodyObj) {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyObj)
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.error || ('Error ' + response.status));
      return data;
    }

    function showMsg(id, text, ok=true) {
      const el = document.getElementById(id);
      el.textContent = text || '';
      el.className = 'msg ' + (ok ? 'ok' : 'error');
    }

    function clearMsg(id) {
      const el = document.getElementById(id);
      el.textContent = '';
      el.className = 'msg';
    }

    function seasonLabel(season) {
      if (season === 'PRIMAVERA') return 'Primavera';
      if (season === 'INVIERNO') return 'Invierno';
      return season || '';
    }

    function requestStatusPill(status) {
      const map = {
        'REQUESTED': ['status-requested', 'Solicitado'],
        'VALIDATED': ['status-validated', 'Validado'],
        'ACCESS_ENABLED': ['status-access-enabled', 'Acceso habilitado'],
        'REGISTERED': ['status-registered', 'Registrado'],
        'CANCELLED': ['status-cancelled', 'Cancelado'],
        'CLOSED': ['status-closed', 'Cerrado'],
      };
      const cfg = map[status] || ['status-requested', status || '—'];
      return `<span class="status-pill ${cfg[0]}">${cfg[1]}</span>`;
    }

    function hideAllMainScreens() {
      document.getElementById('seasonScreen').classList.add('hidden');
      document.getElementById('requestScreen').classList.add('hidden');
      document.getElementById('passScreen').classList.add('hidden');
      document.getElementById('catalogScreen').classList.add('hidden');
    }

    function selectSeason(season) {
      currentSeason = season;
      hideAllMainScreens();
      document.getElementById('requestScreen').classList.remove('hidden');
      document.getElementById('heroTitle').textContent = `Solicitar pase · ${seasonLabel(season)}`;
      document.getElementById('heroSubtitle').textContent = 'Completa tus datos para generar tu credencial digital.';
      clearMsg('requestMsg');
    }

    function goBackToSeason() {
      currentSeason = null;
      hideAllMainScreens();
      document.getElementById('seasonScreen').classList.remove('hidden');
      document.getElementById('heroTitle').textContent = 'Solicita tu pase';
      document.getElementById('heroSubtitle').textContent = 'Elige temporada, solicita tu pase, muestra tu credencial en el evento y cierra tu inscripción con el proyecto.';
    }

    async function submitStudentRequest() {
      clearMsg('requestMsg');

      if (!currentSeason) {
        showMsg('requestMsg', 'Primero selecciona una temporada.', false);
        return;
      }

      const payload = {
        full_name: document.getElementById('full_name').value.trim(),
        enrolment_number: document.getElementById('enrolment_number').value.trim(),
        email: document.getElementById('email').value.trim(),
        second_email: document.getElementById('second_email').value.trim(),
        phone_number: document.getElementById('phone_number').value.trim(),
        degree: document.getElementById('degree').value.trim(),
        semester: document.getElementById('semester').value.trim(),
        season: currentSeason
      };

      try {
        const data = await postJSON('/api/student/requests', payload);

        currentRequest = data.request || null;
        currentStudent = data.user || null;
        currentEvent = data.event || null;

        showMsg('requestMsg', data.message || 'Solicitud procesada correctamente.');
        openPassScreen();
        await refreshStudentPass();
      } catch (e) {
        showMsg('requestMsg', e.message, false);
      }
    }

    function openPassScreen() {
      hideAllMainScreens();
      document.getElementById('passScreen').classList.remove('hidden');
      document.getElementById('heroTitle').textContent = 'Mi credencial';
      document.getElementById('heroSubtitle').textContent = 'Muéstrala en la entrada y refresca tu código cuando staff te lo indique.';
      renderPassInfo();
    }

    function renderPassInfo() {
      if (!currentStudent || !currentRequest || !currentEvent) return;

      document.getElementById('passStudentName').textContent = currentStudent.full_name || '—';
      document.getElementById('passEnrolment').textContent = currentStudent.enrolment_number || '—';
      document.getElementById('passSeason').textContent = currentEvent.display_name || seasonLabel(currentSeason);
      document.getElementById('passFolio').textContent = currentRequest.folio || '—';
      document.getElementById('passStatusWrap').innerHTML = requestStatusPill(currentRequest.status);

      const expiresText = currentPass?.pass_session?.expires_at || currentPass?.active_session?.expires_at || '—';
      document.getElementById('passExpiresAt').textContent = expiresText;

      const btn = document.getElementById('goToCatalogBtn');
      const canEnterCatalog = currentRequest.status === 'ACCESS_ENABLED' || currentRequest.status === 'REGISTERED';
      btn.classList.toggle('hidden', !canEnterCatalog);
    }

    async function loadStudentPass() {
      if (!currentStudent?.enrolment_number || !currentSeason) return;

      const data = await getJSON(
        `/api/student/pass?enrolment_number=${encodeURIComponent(currentStudent.enrolment_number)}&season=${encodeURIComponent(currentSeason)}`
      );

      currentRequest = data.request || currentRequest;
      currentEvent = data.event || currentEvent;
      currentStudent = data.student || currentStudent;
      currentPass = data;

      renderPassInfo();
      clearMsg('passMsg');
    }

    async function reloadStudentPass() {
      try {
        await loadStudentPass();
        showMsg('passMsg', 'Estado actualizado.');
      } catch (e) {
        showMsg('passMsg', e.message, false);
      }
    }

    async function refreshStudentPass() {
      clearMsg('passMsg');

      if (!currentStudent?.enrolment_number || !currentSeason) {
        showMsg('passMsg', 'Faltan datos para generar credencial.', false);
        return;
      }

      try {
        const data = await postJSON('/api/student/pass/refresh', {
          enrolment_number: currentStudent.enrolment_number,
          season: currentSeason
        });

        currentPass = data;
        currentRequest = data.request || currentRequest;
        currentEvent = data.event || currentEvent;
        currentStudent = data.student || currentStudent;

        renderPassInfo();

        // Temporalmente mostramos el token plano.
        // Luego aquí mismo se puede convertir a QR visual.
        const plainToken = data.pass_session?.plain_token || 'Sin código';
        document.getElementById('qrPlaceholder').textContent = plainToken;

        showMsg('passMsg', 'Código actualizado. Muéstralo al staff.');
      } catch (e) {
        showMsg('passMsg', e.message, false);
      }
    }

    async function loadCatalogs() {
      if (!currentSeason) return;

      const data = await getJSON('/api/catalogs?temporada=' + encodeURIComponent(currentSeason));
      fillSelect('socio', data.socio || [], 'name');
      fillSelect('modalidad', data.modalidad || [], 'description');
      fillSelect('dia', data.dias || [], 'description');
      fillSelect('horario', data.horario || [], 'description');
    }

    function fillSelect(id, items, labelKey = 'description') {
      const el = document.getElementById(id);
      const first = '<option value="">Todos</option>';
      el.innerHTML = first;

      for (const item of items || []) {
        const opt = document.createElement('option');
        opt.value = item.id;
        opt.textContent = item[labelKey];
        el.appendChild(opt);
      }
    }

    function openCatalog() {
      hideAllMainScreens();
      document.getElementById('catalogScreen').classList.remove('hidden');
      document.getElementById('heroTitle').textContent = 'Catálogo de proyectos';
      document.getElementById('heroSubtitle').textContent = 'Consulta proyectos disponibles y cierra tu inscripción con un token válido.';
      document.getElementById('seasonChip').textContent = currentEvent?.display_name || seasonLabel(currentSeason);
      document.getElementById('seasonChip').classList.remove('hidden');
      loadCatalogs().then(loadProjects).catch(err => {
        document.getElementById('results').className = '';
        document.getElementById('results').innerHTML = `<div class="empty"><strong>Error</strong><div class="mini" style="margin-top:8px;">${escapeHTML(err.message)}</div></div>`;
      });
    }

    function backToPass() {
      openPassScreen();
    }

    function card(p) {
      const disponible = Number(p.cupos_disponibles) > 0;
      const statusClass = disponible ? 'available' : 'full';
      const statusText = disponible ? 'Disponible' : 'Sin cupo';

      return `
        <article class="card">
          <div class="card-head">
            <h3 class="title">${escapeHTML(p.name)}</h3>
            <span class="status ${statusClass}">${statusText}</span>
          </div>

          <div class="meta-grid">
            <div class="meta-item">
              <span class="meta-label">Socio</span>
              <div class="meta-value">${escapeHTML(p.socio)}</div>
            </div>

            <div class="meta-item">
              <span class="meta-label">Modalidad</span>
              <div class="meta-value">${escapeHTML(p.modalidad)}</div>
            </div>

            <div class="meta-item">
              <span class="meta-label">Día</span>
              <div class="meta-value">${escapeHTML(p.dia)}</div>
            </div>

            <div class="meta-item">
              <span class="meta-label">Horario</span>
              <div class="meta-value">${escapeHTML(p.horario)}</div>
            </div>

            <div class="meta-item">
              <span class="meta-label">Cupos</span>
              <div class="meta-value">${escapeHTML(p.cupos)}</div>
            </div>

            <div class="meta-item">
              <span class="meta-label">Disponibilidad</span>
              <div class="meta-value">
                Inscritos: ${escapeHTML(p.inscritos)} · Disponibles: ${escapeHTML(p.cupos_disponibles)}
              </div>
            </div>
          </div>

          ${p.descripcion_horario ? `<div class="desc"><strong>Horario:</strong> ${escapeHTML(p.descripcion_horario)}</div>` : ''}
          ${p.objectives ? `<div class="desc"><strong>Objetivos:</strong> ${escapeHTML(p.objectives)}</div>` : ''}
          ${p.activities ? `<div class="desc"><strong>Actividades:</strong> ${escapeHTML(p.activities)}</div>` : ''}

          <div class="actions">
            <button class="btn-primary" ${!disponible ? 'disabled' : ''} onclick="openRegistrationModal(${Number(p.id)})">
              Registrarme
            </button>
            <button class="btn-secondary" onclick="viewProjectDetail(${Number(p.id)})">Ver detalle</button>
          </div>
        </article>
      `;
    }

    async function loadProjects() {
      if (!currentSeason) return;

      const root = document.getElementById('results');
      const resultsCount = document.getElementById('resultsCount');

      root.className = 'loading';
      root.innerHTML = 'Cargando oferta...';

      const params = new URLSearchParams();
      params.set('temporada', currentSeason);

      for (const id of ['q', 'socio', 'modalidad', 'dia', 'horario']) {
        const el = document.getElementById(id);
        const value = el.value.trim();
        if (value) params.set(id, value);
      }

      const data = await getJSON('/api/projects?' + params.toString());
      const items = data.items || [];
      currentProjects = items;

      if (data.event?.display_name) {
        resultsCount.textContent = `${items.length} proyecto${items.length === 1 ? '' : 's'} encontrado${items.length === 1 ? '' : 's'} en ${data.event.display_name}`;
      } else {
        resultsCount.textContent = `${items.length} proyecto${items.length === 1 ? '' : 's'} encontrado${items.length === 1 ? '' : 's'} en ${seasonLabel(currentSeason)}`;
      }

      if (!items.length) {
        root.className = '';
        root.innerHTML = `
          <div class="empty">
            <strong>No se encontraron proyectos con esos filtros.</strong>
            <div class="mini" style="margin-top:8px;">Prueba limpiando filtros o usando una búsqueda más general.</div>
          </div>
        `;
        return;
      }

      root.className = '';
      root.innerHTML = `<div class="grid">${items.map(card).join('')}</div>`;
    }

    function clearFilters() {
      ['q', 'socio', 'modalidad', 'dia', 'horario'].forEach(id => {
        document.getElementById(id).value = '';
      });
      loadProjects();
    }

    function openRegistrationModal(projectId) {
      selectedProject = currentProjects.find(p => Number(p.id) === Number(projectId)) || null;
      if (!selectedProject) return;

      document.getElementById('regProjectName').value = selectedProject.name || '';
      document.getElementById('regTokenValue').value = '';
      document.getElementById('regAcceptedCheckbox').checked = false;
      document.getElementById('regAcceptedFullName').value = currentStudent?.full_name || '';
      clearMsg('registrationMsg');

      document.getElementById('registrationModalWrap').classList.remove('hidden');
    }

    function closeRegistrationModal() {
      document.getElementById('registrationModalWrap').classList.add('hidden');
      selectedProject = null;
      clearMsg('registrationMsg');
    }

    async function previewRegistration() {
      if (!selectedProject) return;

      clearMsg('registrationMsg');

      try {
        const data = await postJSON('/api/student/registration/preview', {
          enrolment_number: currentStudent?.enrolment_number,
          season: currentSeason,
          project_id: selectedProject.id,
          token_value: document.getElementById('regTokenValue').value.trim()
        });

        showMsg('registrationMsg', data.message || 'Validación correcta.');
      } catch (e) {
        showMsg('registrationMsg', e.message, false);
      }
    }

    async function confirmRegistration() {
      if (!selectedProject) return;

      clearMsg('registrationMsg');

      try {
        const data = await postJSON('/api/student/registration/confirm', {
          enrolment_number: currentStudent?.enrolment_number,
          season: currentSeason,
          project_id: selectedProject.id,
          token_value: document.getElementById('regTokenValue').value.trim(),
          accepted_checkbox: document.getElementById('regAcceptedCheckbox').checked,
          accepted_full_name: document.getElementById('regAcceptedFullName').value.trim()
        });

        showMsg('registrationMsg', data.message || 'Registro completado.');
        await loadStudentPass();
        await loadProjects();

        setTimeout(() => {
          closeRegistrationModal();
          openPassScreen();
        }, 1200);
      } catch (e) {
        showMsg('registrationMsg', e.message, false);
      }
    }

    async function viewProjectDetail(projectId) {
      try {
        const data = await getJSON(`/api/projects/${projectId}?temporada=${encodeURIComponent(currentSeason)}`);
        const item = data.item || null;
        if (!item) return;

        alert(
          `Proyecto: ${item.name}\n\n` +
          `Socio: ${item.socio}\n` +
          `Modalidad: ${item.modalidad}\n` +
          `Día: ${item.dia}\n` +
          `Horario: ${item.horario}\n` +
          `Duración: ${item.duration || '—'}\n` +
          `Lugar: ${item.location || '—'}\n` +
          `Horas máximas: ${item.max_hours || '—'}\n` +
          `Población: ${item.audience || '—'}\n` +
          `Competencias: ${item.competencies || '—'}\n` +
          `Clave externa: ${item.clave || '—'}\n` +
          `Comentarios: ${item.comments || '—'}`
        );
      } catch (e) {
        alert('Error: ' + e.message);
      }
    }

    function openCroquis() {
      document.getElementById('croquisWrap').classList.remove('hidden');
    }

    function closeCroquis() {
      document.getElementById('croquisWrap').classList.add('hidden');
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('q').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') loadProjects();
      });
    });
  </script>
</body>
</html>
"""