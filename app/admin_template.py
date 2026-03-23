ADMIN_HTML = r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Portal Administrativo | Servicio Social</title>
  <style>
    :root {
      /* Paleta Dashboard Profesional */
      --bg: #f8fafc;        /* Fondo Slate muy claro */
      --card: #ffffff;      /* Tarjetas Blancas puras */
      
      --text: #0f172a;      /* Texto Navy oscuro (principal) */
      --text-label: #475569; /* Etiquetas Slate oscuro */
      --text-muted: #94a3b8; /* Texto desactivado/secundario */
      
      --border: #e2e8f0;    /* Línea Slate sutil */
      --border-soft: #cbd5e1; /* Línea ligeramente más fuerte (inputs) */
      
      /* Acentos de Marca (Blue) */
      --brand: #2563eb;     /* Azul moderno y vibrante */
      --brand-hover: #1d4ed8; /* Azul oscuro para hover */
      --brand-soft: #eff6ff;  /* Fondo azul muy suave para highlights */
      
      /* Estados Semánticos Pulidos */
      --ok-bg: #d1fae5;     /* Emerald suave */
      --ok-text: #065f46;
      --err-bg: #fee2e2;    /* Red suave */
      --err-text: #991b1b;
      --danger: #ef4444;    /* Red vibrante (acciones de peligro) */
      --warn-bg: #fff7ed;   /* Orange suave */
      --warn-text: #9a3412;

      /* UI Details */
      --radius-lg: 12px;
      --radius-md: 8px;
      --radius-sm: 6px;
      --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    * { box-sizing: border-box; }

    body {
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      margin: 0;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
    }

    /* Header Limpio */
    header {
      background: var(--card);
      border-bottom: 1px solid var(--border);
      padding: 20px 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
      position: sticky; top: 0; z-index: 100;
    }

    header .title {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    header .title strong {
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--text);
    }

    header .title span {
      font-size: 0.875rem;
      color: var(--text-label);
      font-weight: 500;
    }

    header a {
      color: var(--text-label);
      text-decoration: none;
      font-size: 0.93rem;
      font-weight: 600;
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      transition: all 0.2s;
    }

    header a:hover {
      background: var(--bg);
      color: var(--brand);
    }

    /* Contenedor Principal */
    .container {
      max-width: 1280px;
      margin: 32px auto;
      padding: 0 32px;
      width: 100%;
    }

    /* Mensajes de Estado Flotantes */
    .msg {
      display: none;
      margin-bottom: 24px;
      padding: 14px 18px;
      border-radius: var(--radius-md);
      font-size: 0.95rem;
      font-weight: 600;
      border: 1px solid transparent;
      box-shadow: var(--shadow-sm);
    }

    .msg.ok { background: var(--ok-bg); color: var(--ok-text); border-color: #a7f3d0; }
    .msg.err { background: var(--err-bg); color: var(--err-text); border-color: #fecaca; }

    /* Grid Layout */
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
      gap: 20px;
    }

    /* Diseño de Tarjetas Pulido */
    .card {
      background: var(--card);
      padding: 24px;
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-sm);
      border: 1px solid var(--border);
      transition: box-shadow 0.2s, border-color 0.2s;
    }

    .card:hover {
      box-shadow: var(--shadow-md);
      border-color: #cbd5e1; /* Borde sutil en hover */
    }

    h3 {
      margin: 0 0 16px 0;
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text);
    }

    .muted {
      color: var(--text-label);
      font-size: 0.9rem;
      line-height: 1.5;
      margin-bottom: 20px;
    }

    /* Formularios Modernos */
    label {
      display: block;
      margin: 16px 0 6px;
      color: var(--text-label);
      font-size: 0.84rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    input, select, textarea {
      width: 100%;
      box-sizing: border-box;
      padding: 12px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-soft);
      background: white;
      font-size: 0.93rem;
      color: var(--text);
      outline: none;
      transition: all 0.2s;
    }

    input::placeholder { color: var(--text-muted); }

    input:focus, select:focus, textarea:focus {
      border-color: var(--brand);
      box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
    }

    textarea { min-height: 100px; resize: vertical; line-height: 1.4; }

    .row { display: flex; gap: 16px; flex-wrap: wrap; }
    .row > * { flex: 1; min-width: 180px; }

    /* Acciones */
    .actions {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 20px;
      align-items: center;
    }

    .actions button {
      width: auto !important;
      padding: 10px 18px;
    }

    /* Botones Modernos */
    button {
      width: 100%;
      box-sizing: border-box;
      padding: 12px 16px;
      border-radius: var(--radius-md);
      border: 1px solid transparent;
      background: var(--card);
      font-size: 0.93rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }

    .btn { /* Primario Azul */
      background: var(--brand);
      color: white;
      box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    .btn:hover { background: var(--brand-hover); transform: translateY(-1px); }

    .btn2 { /* Secundario Blanco con borde */
      background: white;
      border: 1px solid var(--border-soft);
      color: var(--text-label);
    }
    .btn2:hover { background: var(--bg); color: var(--text); border-color: var(--border-soft); }

    .btnDanger { /* Peligro Rojo */
      background: var(--danger);
      color: white;
      box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.2);
    }
    .btnDanger:hover { background: #dc2626; transform: translateY(-1px); }

    .btnWarn { /* Advertencia Naranja */
      background: #f97316; /* Orange más vibrante que el de root */
      color: white;
    }
    .btnWarn:hover { background: #ea580c; }

    .hr { height: 1px; background: var(--border); margin: 20px 0; border: none; }

    /* Píldoras de Estado (Pills) */
    .pill {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 999px;
      background: var(--bg);
      color: var(--text-label);
      font-size: 0.78rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .pill.ok { background: var(--ok-bg); color: var(--ok-text); }
    .pill.err { background: var(--err-bg); color: var(--err-text); }
    .pill.warn { background: var(--warn-bg); color: var(--warn-text); border: 1px solid #fed7aa; }

    /* Lista de Proyectos */
    .projects {
      display: grid;
      grid-template-columns: 1fr; /* Lista vertical para Admin */
      gap: 16px;
      margin-top: 16px;
    }

    .meta { font-size: 0.93rem; color: var(--text-label); line-height: 1.5; }
    .meta div { margin-bottom: 4px; }
    .meta strong { color: var(--text); font-weight: 600; }
    
    .mini { font-size: 0.8rem; color: var(--text-label); line-height: 1.4; }

    .hide { display: none !important; }

    .topbar { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }

    /* Box de Tokens */
    .tokbox {
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg);
      padding: 20px;
      margin-top: 16px;
    }
    .tokbox textarea { min-height: 160px; font-family: monospace; font-size: 0.9rem; }

    /* Tablas Modernas */
    table { width: 100%; border-collapse: collapse; margin-top: 12px; }
    th, td { padding: 12px 8px; text-align: left; vertical-align: middle; border-bottom: 1px solid var(--border); }
    th { color: var(--text-label); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; }
    td { font-size: 0.93rem; }
    tr:last-child td { border-bottom: none; }
    
    code {
      background: var(--text);
      color: #e2e8f0;
      padding: 3px 6px;
      border-radius: var(--radius-sm);
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 0.9em;
    }

    /* Responsive */
    @media (max-width: 768px) {
      header { padding: 16px; flex-direction: column; align-items: flex-start; }
      .container { padding: 0 16px; margin: 20px auto; }
      .grid { grid-template-columns: 1fr; }
      .card { padding: 18px; }
      .topbar { width: 100%; justify-content: flex-end; }
    }
  </style>
</head>
<body>
  <header>
    <div class="title">
      <strong>Portal Administrativo</strong>
      <span>Proyectos · Cupos · Acceso Staff</span>
    </div>
    <div class="topbar">
      <a href="/">Vista Estudiante</a>
      <a href="/health">Health Check</a>
    </div>
  </header>

  <div class="container">
    <div id="msg" class="msg"></div>

    <div class="card" id="loginCard">
      <h3>Acceso Administrador</h3>
      <div class="muted">Ingresa tu clave de acceso. Al validarla, se activarán las funciones de gestión correspondientes a tu rol.</div>

      <label>Clave</label>
      <input id="adminKey" type="password" placeholder="Ingresa clave ADMIN o STAFF">

      <div class="actions">
        <button class="btn" onclick="validateAndSaveKey()">Entrar al Panel</button>
        <button class="btn2" onclick="clearKey(true)">Limpiar</button>
      </div>

      <div class="hr"></div>
      <div class="mini" id="roleBadge">Sesión actual: —</div>
    </div>

    <div class="grid hide" id="mainDashboard" style="margin-top:20px;">

      <div class="card hide" id="accessCodeCard">
        <h3>Códigos Estudiantes</h3>
        <div class="muted">
          Genera códigos temporales para que los estudiantes puedan visualizar el catálogo. Verifica su identidad antes de entregar el código.
        </div>

        <label>ID Único del Estudiante</label>
        <input id="access_enrolment" placeholder="Ej: A01234567">

        <div class="row">
          <div>
            <label>Duración (horas)</label>
            <input id="access_hours" type="number" min="1" max="168" value="72">
          </div>
          <div>
            <label>&nbsp;</label>
            <button class="btn" onclick="createAccessCode()">Generar Código</button>
          </div>
        </div>

        <div class="actions" style="justify-content:space-between; margin-top: 24px;">
          <button class="btn2" onclick="resetAccess()">Limpiar Datos</button>
          <button class="btnDanger" onclick="logout()">Cerrar Sesión Panel</button>
        </div>

        <div class="tokbox" style="margin-top: 20px; border-style: dashed; padding: 16px;">
          <div class="mini"><strong>Último código generado:</strong> <code id="last_code">—</code></div>
          <div class="mini" style="margin-top: 4px;"><strong>Expira:</strong> <span id="last_exp">—</span></div>
        </div>
      </div>

      <div class="card hide" id="createProjectCard">
        <h3>Crear Nuevo Proyecto Operativo</h3>

        <div class="row">
          <div>
            <label>Socio Formador (Familia)</label>
            <input id="name" placeholder="Nombre de la Organización">
          </div>
          <div>
            <label>Nombre del Equipo/Proyecto</label>
            <input id="team_owners" placeholder="Nombre específico del proyecto">
          </div>
        </div>

        <div class="row">
          <div>
            <label>Temporada / Año</label>
            <input id="season" placeholder="Ej: Verano 2026">
          </div>
          <div>
            <label>Cupo Total (Slots)</label>
            <input id="slots" type="number" min="0" value="0">
          </div>
        </div>

        <div class="row">
          <div>
            <label>Modalidad</label>
            <select id="modality_id"><option value="">Selecciona...</option></select>
          </div>
          <div>
            <label>Días</label>
            <select id="week_days_id"><option value="">Selecciona...</option></select>
          </div>
          <div>
            <label>Horario</label>
            <select id="schedule_id"><option value="">Selecciona...</option></select>
          </div>
        </div>

        <label>Descripción detallada horario</label>
        <input id="schedule_description" placeholder="Ej: Lunes y Miércoles 9-12">

        <label>Filtro de Carreras Permitidas (Socio)</label>
        <select id="academy_mode" onchange="onAcademyModeChange()">
          <option value="ALL">Todas las carreras</option>
          <option value="GROUP">Por Grupo (Grupos de Carreras)</option>
          <option value="CUSTOM">Manual (Selección específica)</option>
        </select>

        <div id="academy_group_wrap" class="hide">
          <label>Grupo de Carreras</label>
          <select id="academy_group_id"><option value="">Selecciona...</option></select>
        </div>

        <div id="academy_custom_wrap" class="hide">
          <label>Selección Manual (Carreras)</label>
          <select id="partner_ids" multiple size="10"></select>
          <div class="mini" style="margin-top:4px;">Tip: Usa Ctrl (Win) o Cmd (Mac) para selección múltiple.</div>
        </div>

        <div class="hr"></div>

        <div class="row">
          <div>
            <label>Objetivos</label>
            <textarea id="objectives"></textarea>
          </div>
          <div>
            <label>Actividades</label>
            <textarea id="activities"></textarea>
          </div>
        </div>

        <div class="actions">
          <button class="btn" onclick="createProject()">Crear Proyecto</button>
          <button class="btn2" onclick="resetProjectForm()">Limpiar Formulario</button>
        </div>
      </div>

    </div> <div class="card hide" id="projectsCard" style="margin-top:20px;">
      <h3>Gestión de Cupos Reales y Tokens (Control Total)</h3>
      <div class="muted">
        Usa esta sección para monitorear inscritos y abrir vacantes reales generando tokens. <br>
        <strong>Slots</strong> = Cupo total del equipo. <strong>Tokens</strong> = Vacantes abiertas para inscripciones.
      </div>

      <div class="hr"></div>
      <h3 style="font-size: 1rem; margin-bottom: 8px;">Vigencia Global de Nuevos Tokens</h3>
      <div class="muted">Cuánto tiempo durarán los tokens (vacantes) generados a partir de este momento.</div>

      <div class="row" style="align-items:flex-end;">
        <div>
          <label>Duración por defecto (horas)</label>
          <input id="ttl_hours" type="number" min="1" max="168" value="24">
        </div>
        <div>
          <label>&nbsp;</label>
          <button class="btn2" onclick="saveTokenTTL()">Guardar TTL</button>
        </div>
      </div>
      <div class="mini" style="margin-top:8px;"><strong>Valor actual:</strong> <span id="ttl_current" class="pill">—</span></div>

      <div class="hr"></div>
      
      <div id="projects" class="projects"></div>

      <div id="tokensOut" class="tokbox hide" style="border-style:dashed; margin-top:24px;">
        <h3 style="font-size: 1rem;">Tokens Recién Generados (Vacantes Abiertas)</h3>
        <div class="muted" id="tokensOutMeta">—</div>

        <label>Lista de Tokens (uno por línea)</label>
        <textarea id="tokensOutText" readonly></textarea>

        <div class="actions">
          <button class="btn" onclick="copyTokensOut()">Copiar Lista de Tokens</button>
          <button class="btn2" onclick="clearTokensOut()">Cerrar y Limpiar Caja</button>
        </div>
      </div>
    </div>

  </div>

<script>
  // Se borra al cerrar pestaña
  const storage = sessionStorage;

  function showMsg(text, ok=true) {
    const el = document.getElementById('msg');
    el.className = 'msg ' + (ok ? 'ok' : 'err');
    el.textContent = text;
    el.style.display = 'block';
    el.scrollIntoView({behavior:'smooth', block:'start'}); // Scroll al mensaje
    setTimeout(() => { el.style.display = 'none'; }, 5200);
  }

  function getKey() { return storage.getItem('ADMIN_API_KEY') || ''; }
  function getRole() { return storage.getItem('ADMIN_ROLE') || ''; }

  // Actualiza la UI basándose en el rol
  function applyRoleUI(role) {
    document.getElementById('roleBadge').textContent = role ? `Sesión activa como: ${role}` : 'Sesión actual: —';

    const loginCard = document.getElementById('loginCard');
    const mainDash = document.getElementById('mainDashboard'); // Contenedor Grid
    const access = document.getElementById('accessCodeCard');
    const create = document.getElementById('createProjectCard');
    const projCard = document.getElementById('projectsCard');

    const logged = (role === 'ADMIN' || role === 'STAFF');
    loginCard.classList.toggle('hide', logged);
    mainDash.classList.toggle('hide', !logged);

    access.classList.toggle('hide', !(role === 'ADMIN' || role === 'STAFF'));
    create.classList.toggle('hide', !(role === 'ADMIN'));
    projCard.classList.toggle('hide', !(role === 'ADMIN'));
  }

  async function validateAndSaveKey() {
    const v = document.getElementById('adminKey').value.trim();
    if (!v) return showMsg('Escribe tu clave', false);

    try {
      const r = await fetch('/api/admin/ping', { headers: { 'X-ADMIN-KEY': v }});
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || ('Error ' + r.status));

      storage.setItem('ADMIN_API_KEY', v);
      storage.setItem('ADMIN_ROLE', data.role);
      applyRoleUI(data.role);

      // Carga de datos tras login
      await loadCatalogs();
      if (data.role === 'ADMIN') {
        await loadProjects();
        await loadTokenTTL();
      }
      onAcademyModeChange();

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
    if (show) showMsg('Sesión cerrada correctamente');
  }

  function logout(){ clearKey(true); resetAccess(); }

  // HELPERS API
  async function getJSON(url) {
    const r = await fetch(url);
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  async function getJSONAuth(url) {
    const key = getKey();
    const r = await fetch(url, { headers: { 'X-ADMIN-KEY': key }});
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  async function postJSON(url, bodyObj) {
    const key = getKey();
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-ADMIN-KEY': key },
      body: JSON.stringify(bodyObj)
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  async function patchJSON(url, bodyObj) {
    const key = getKey();
    const r = await fetch(url, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', 'X-ADMIN-KEY': key },
      body: JSON.stringify(bodyObj)
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  async function putJSONAuth(url, bodyObj) {
    const key = getKey();
    const r = await fetch(url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'X-ADMIN-KEY': key },
      body: JSON.stringify(bodyObj)
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  // TTL SETTINGS
  async function loadTokenTTL() {
    try {
      const data = await getJSONAuth('/api/admin/settings');
      const hours = Number(data.token_ttl_hours || 24);
      document.getElementById('ttl_hours').value = hours;
      document.getElementById('ttl_current').textContent = `${hours} horas`;
    } catch (e) { showMsg('Error TTL: '+e.message, false); }
  }

  async function saveTokenTTL() {
    const hours = Number(document.getElementById('ttl_hours').value || 24);
    if (!hours || hours < 1 || hours > 168) return showMsg('Horas inválidas (1 a 168)', false);
    try {
      const res = await putJSONAuth('/api/admin/settings/token-ttl-hours', { hours });
      document.getElementById('ttl_current').textContent = `${res.token_ttl_hours} horas`;
      showMsg('TTL Global actualizado');
    } catch (e) { showMsg(e.message, false); }
  }

  // CATALOGS
  function fillSelect(id, items) {
    const el = document.getElementById(id);
    el.innerHTML = '<option value="">Selecciona...</option>';
    for (const item of items || []) {
      const opt = document.createElement('option');
      opt.value = item.id;
      opt.textContent = item.name || item.description || item.team_owners || ('ID ' + item.id); // Agregué team_owners para academies
      el.appendChild(opt);
    }
  }

  async function loadCatalogs() {
    try {
      const data = await getJSON('/api/catalogs');
      fillSelect('modality_id', data.modalidad || data.modality);
      fillSelect('week_days_id', data.dias || data.week_days);
      fillSelect('schedule_id', data.horario || data.schedule);
      fillSelect('academy_group_id', data.partner_group || []);
      const ms = document.getElementById('partner_ids');
      ms.innerHTML = '';
      for (const a of (data.socio || data.partner || [])) {
        const opt = document.createElement('option');
        opt.value = a.id;
        opt.textContent = a.name + (a.team_owners ? ` (${a.team_owners})` : '');
        ms.appendChild(opt);
      }
    } catch(e) { console.error('Error catálogos', e); }
  }

  function onAcademyModeChange(){
    const mode = document.getElementById('academy_mode').value;
    document.getElementById('academy_group_wrap').classList.toggle('hide', mode !== 'GROUP');
    document.getElementById('academy_custom_wrap').classList.toggle('hide', mode !== 'CUSTOM');
  }

  // ACCESS CODES (STAFF)
  function resetAccess() {
    document.getElementById('access_enrolment').value = '';
    document.getElementById('access_hours').value = 72;
    document.getElementById('last_code').textContent = '—';
    document.getElementById('last_exp').textContent = '—';
  }

  async function createAccessCode() {
    try {
      const enrolment_number = document.getElementById('access_enrolment').value.trim();
      const hours = Number(document.getElementById('access_hours').value || 72);
      if (!enrolment_number) return showMsg('Ingresa ID del estudiante', false);
      const res = await postJSON('/api/admin/access-codes', { enrolment_number, hours });
      document.getElementById('last_code').textContent = res.code || '—';
      document.getElementById('last_exp').textContent = res.expires_at || '—';
      showMsg('Código de acceso generado');
    } catch (e) { showMsg(e.message, false); }
  }

  // CREATE PROJECT (ADMIN)
  function resetProjectForm() {
    [ 'name','team_owners','season','slots','schedule_description','modality_id','week_days_id','schedule_id','academy_mode','academy_group_id','objectives','activities'].forEach(id => {
      const el = document.getElementById(id);
      if(!el) return;
      if (el.tagName === 'SELECT' && id !== 'academy_mode') el.value = '';
      else if (el.tagName === 'SELECT' && id === 'academy_mode') el.value = 'ALL';
      else if (id === 'slots') el.value = 0;
      else el.value = '';
    });
    const ms = document.getElementById('partner_ids');
    Array.from(ms.options).forEach(o => o.selected = false);
    onAcademyModeChange();
  }

  async function createProject() {
    const academy_mode = document.getElementById('academy_mode').value;
    const academy_group_id = document.getElementById('academy_group_id').value ? Number(document.getElementById('academy_group_id').value) : null;
    const partner_ids = Array.from(document.getElementById('partner_ids').selectedOptions).map(o => Number(o.value));
    if (academy_mode === 'GROUP' && !academy_group_id) return showMsg('Selecciona Grupo de Carreras', false);
    if (academy_mode === 'CUSTOM' && partner_ids.length === 0) return showMsg('Selecciona al menos 1 carrera manual', false);

    const body = {
      name: document.getElementById('name').value.trim(),
      team_owners: document.getElementById('team_owners').value.trim(),
      season: document.getElementById('season').value.trim(),
      slots: Number(document.getElementById('slots').value),
      schedule_description: document.getElementById('schedule_description').value.trim(),
      modality_id: Number(document.getElementById('modality_id').value),
      week_days_id: Number(document.getElementById('week_days_id').value),
      schedule_id: Number(document.getElementById('schedule_id').value),
      academy_mode, academy_group_id, partner_ids, objectives: document.getElementById('objectives').value.trim(), activities: document.getElementById('activities').value.trim()
    };
    if (!body.name || !body.team_owners || !body.modality_id) return showMsg('Faltan datos obligatorios', false);

    try {
      const res = await postJSON('/api/admin/projects', body);
      showMsg(`Proyecto creado (ID=${res.id})`);
      resetProjectForm();
      await loadProjects();
    } catch (e) { showMsg(e.message, false); }
  }

  // PROJ CONTROL LIST (ADMIN)
  async function loadProjects() {
    try {
      const data = await getJSONAuth('/api/admin/projects');
      const root = document.getElementById('projects');
      root.innerHTML = (data || []).map(projectCard).join('');
    } catch(e){ showMsg(e.message, false); }
  }

  // Slots
  async function updateSlots(projectId) {
    const slots = Number(document.getElementById(`slots-${projectId}`).value);
    if (slots < 0) return showMsg('Cupo inválido', false);
    try {
      const res = await patchJSON(`/api/admin/projects/${projectId}/slots`, { slots });
      showMsg(`Slots actualizados: ${res.slots}`);
      await loadProjects();
    } catch (e) { showMsg(e.message, false); }
  }

  // Tokens
  async function genTokens(projectId) {
    const count = Number(document.getElementById(`count-${projectId}`).value || 1);
    const projectName = document.getElementById(`projname-${projectId}`)?.textContent || '';
    if (count < 1) return showMsg('Cantidad inválida', false);
    try {
      const res = await postJSON(`/api/admin/projects/${projectId}/tokens`, { count });
      showMsg(`Vacantes abiertas: ${res.created} (tokens)`);
      if (res.tokens?.length) showTokensOut(res.tokens, res.ttl_hours, projectName);
      await loadProjects();
    } catch (e) { showMsg(e.message, false); }
  }

  // Tokens Output
  function showTokensOut(tokens, ttlHours, projectName='') {
    const box = document.getElementById('tokensOut');
    document.getElementById('tokensOutText').value = (tokens || []).join('\n');
    document.getElementById('tokensOutMeta').textContent = `Proyecto: ${projectName} | Cantidad: ${tokens.length} | Vigencia: ${ttlHours} horas`;
    box.classList.remove('hide');
    box.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  async function copyTokensOut() {
    const txt = document.getElementById('tokensOutText');
    txt.select(); document.execCommand('copy');
    showMsg('Tokens copiados al portapapeles');
  }
  function clearTokensOut() { document.getElementById('tokensOut').classList.add('hide'); }

  // Template para tarjeta proyecto
  function projectCard(p) {
    const disp = (p.cupos_disponibles ?? 0);
    const pill = disp > 0 ? '<span class="pill ok">Cupo Real</span>' : '<span class="pill warn">Sin Vacantes</span>';
    return `
      <div class="card" style="margin-bottom: 12px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;">
          <div>
            <strong id="projname-${p.id}">${p.name}</strong> <span class="mini">(${p.team_owners})</span>
            <div class="meta" style="margin-top:8px;">
              <div>T: <strong>${p.cupos}</strong> slots (total) · I: <strong>${p.inscritos}</strong> · V Reales: <strong>${disp}</strong> (tokens disp.)</div>
              <div class="mini">${p.modality} · ${p.dia} · ${p.horario}</div>
            </div>
          </div>
          ${pill}
        </div>
        <div class="hr" style="margin: 16px 0;"></div>
        <div class="row">
          <div>
            <label>Subir Slots Total</label>
            <input id="slots-${p.id}" type="number" value="${p.cupos}">
          </div>
          <div>
            <label>&nbsp;</label>
            <button class="btn2" onclick="updateSlots(${p.id})">Guardar Slots</button>
          </div>
        </div>
        <div class="row" style="margin-top:10px;">
          <div>
            <label>Abrir Vacantes Reales (Cantidad)</label>
            <input id="count-${p.id}" type="number" value="1" min="1">
          </div>
          <div>
            <label>&nbsp;</label>
            <button class="btn" onclick="genTokens(${p.id})">Abrir Vacantes (Generar Tokens)</button>
          </div>
        </div>
      </div>
    `;
  }

  // Inicialización
  document.addEventListener('DOMContentLoaded', () => {
    // Si ya hay key en session, saltamos login
    if (getKey()) validateAndSaveKey(); 
    else applyRoleUI('');

    // Enter en clave
    document.getElementById('adminKey').addEventListener('keypress', (e) => {
      if(e.key === 'Enter') validateAndSaveKey();
    });
  });
</script>
</body>
</html>
"""