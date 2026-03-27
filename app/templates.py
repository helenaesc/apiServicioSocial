INDEX_HTML = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Oferta Servicio Social</title>
  <style>
    :root {
      --bg: #f4f7fb;
      --panel: rgba(255, 255, 255, 0.82);
      --panel-solid: #ffffff;
      --text: #0f172a;
      --muted: #64748b;
      --line: #e2e8f0;
      --primary: #2563eb;
      --accent: #0ea5e9;
      --success-bg: #dcfce7;
      --success-text: #166534;
      --danger-bg: #fee2e2;
      --danger-text: #991b1b;
      --shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
      --radius-xl: 22px;
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
      position: relative;
      overflow: hidden;
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #0ea5e9 100%);
      color: white;
      padding: 40px 20px 80px;
    }

    .hero-inner {
      max-width: 1150px;
      margin: 0 auto;
      position: relative;
      z-index: 1;
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
      backdrop-filter: blur(8px);
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

    .container {
      max-width: 1150px;
      margin: -44px auto 32px;
      padding: 0 16px 24px;
      position: relative;
      z-index: 2;
    }

    .screen {
      max-width: 1100px;
      margin: -44px auto 32px;
      padding: 0 16px 24px;
      position: relative;
      z-index: 2;
    }

    .panel {
      background: var(--panel);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255,255,255,.7);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow);
      padding: 26px;
    }

    .panel-header {
      text-align: center;
      margin-bottom: 24px;
    }

    .panel-header h2 {
      margin: 0 0 8px;
      font-size: 1.7rem;
      color: var(--text);
    }

    .panel-header p {
      margin: 0;
      color: var(--muted);
      font-size: 1rem;
    }

    .auth-switch {
      display: flex;
      gap: 10px;
      justify-content: center;
      margin-bottom: 18px;
      flex-wrap: wrap;
    }

    .switch-btn {
      border: 1px solid #dbe3ee;
      background: white;
      color: #334155;
      padding: 10px 14px;
      border-radius: 14px;
      font-weight: 700;
      cursor: pointer;
    }

    .switch-btn.active {
      background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
      color: white;
      border: none;
    }

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
      height: 46px;
      border-radius: 14px;
      font-size: .95rem;
      transition: .2s ease;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.92);
      color: var(--text);
      padding: 0 14px;
      outline: none;
    }

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

    .btn-secondary {
      background: #eef2f7;
      color: #334155;
      border: 1px solid #dbe3ee;
    }

    .msg {
      margin-top: 12px;
      font-size: .92rem;
      min-height: 20px;
    }

    .msg.error { color: var(--danger-text); }
    .msg.ok { color: var(--success-text); }

    .season-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 18px;
    }

    .season-card, .card {
      height: auto;
      overflow: hidden;
    }

    .season-card {
      border: 1px solid #e2e8f0;
      background: white;
      border-radius: 18px;
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

    .badge-spring {
      background: #dcfce7;
      color: #166534;
    }

    .badge-winter {
      background: #dbeafe;
      color: #1d4ed8;
    }

    .filters {
      background: var(--panel);
      backdrop-filter: blur(14px);
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

    .filters-title {
      font-size: 1rem;
      font-weight: 700;
      color: var(--text);
    }

    .filters-subtitle {
      color: var(--muted);
      font-size: .92rem;
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

    .results-count {
      font-weight: 700;
      font-size: .96rem;
    }

    .results-hint {
      color: var(--muted);
      font-size: .9rem;
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

    .card {
      position: relative;
      background: var(--panel-solid);
      border: 1px solid #e9eef5;
      border-radius: 20px;
      padding: 18px;
      box-shadow: 0 10px 22px rgba(15, 23, 42, .05);
      transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
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

    .empty, .loading {
      background: white;
      border: 1px solid #e9eef5;
      border-radius: 18px;
      padding: 24px;
      text-align: center;
      color: #475569;
      box-shadow: 0 10px 22px rgba(15, 23, 42, .05);
    }

    .loading {
      display: grid;
      place-items: center;
      min-height: 120px;
      font-weight: 600;
    }

    @media (max-width: 980px) {
      .filter-grid {
        grid-template-columns: 1fr 1fr;
      }
      .actions {
        grid-column: 1 / -1;
      }
    }

    @media (max-width: 640px) {
      .filter-grid {
        grid-template-columns: 1fr;
      }
      .meta-grid {
        grid-template-columns: 1fr;
      }
      .card-head {
        flex-direction: column;
        align-items: start;
      }
      .actions {
        flex-direction: column;
        align-items: stretch;
      }
      .actions button {
        width: 100%;
      }
    }
  </style>
</head>
<body>
  <section class="hero">
    <div class="hero-inner">
      <div class="eyebrow">Tecnológico de Monterrey</div>
      <h1 id="heroTitle">Acceso al catálogo</h1>
      <p id="heroSubtitle">
        Regístrate o inicia sesión con tu matrícula y código temporal para consultar la oferta disponible.
      </p>
    </div>
  </section>

  <section id="authScreen" class="screen">
    <div class="panel" style="max-width:760px; margin:auto;">
      <div class="panel-header">
        <h2>Registro / Acceso</h2>
        <p>Primero registra tus datos. Si ya estás registrado, inicia sesión.</p>
      </div>

      <div class="auth-switch">
        <button id="btnShowRegister" class="switch-btn active" onclick="showAuthTab('register')">Registrarme</button>
        <button id="btnShowLogin" class="switch-btn" onclick="showAuthTab('login')">Ya tengo registro</button>
      </div>

      <!-- REGISTRO -->
      <div id="registerBox">
        <div class="form-grid">
          <div class="field">
            <label for="reg_first_name">Nombre</label>
            <input id="reg_first_name" placeholder="Nombre">
          </div>

          <div class="field">
            <label for="reg_second_name">Segundo nombre (opcional)</label>
            <input id="reg_second_name" placeholder="Segundo nombre">
          </div>

          <div class="field">
            <label for="reg_p_last_name">Apellido paterno</label>
            <input id="reg_p_last_name" placeholder="Apellido paterno">
          </div>

          <div class="field">
            <label for="reg_m_last_name">Apellido materno</label>
            <input id="reg_m_last_name" placeholder="Apellido materno">
          </div>

          <div class="field">
            <label for="reg_email">Correo</label>
            <input id="reg_email" placeholder="correo@ejemplo.com">
          </div>

          <div class="field">
            <label for="reg_enrolment_number">Matrícula / ID único</label>
            <input id="reg_enrolment_number" placeholder="Ej: A01234567">
          </div>

          <div class="field">
            <label for="reg_phone_number">Teléfono (opcional)</label>
            <input id="reg_phone_number" placeholder="Teléfono">
          </div>

          <div class="field">
            <label for="reg_degree">Carrera (opcional)</label>
            <input id="reg_degree" placeholder="Ej: ITC">
          </div>

          <div class="field">
            <label for="reg_semester">Semestre (opcional)</label>
            <input id="reg_semester" type="number" min="1" max="20" placeholder="Semestre">
          </div>
        </div>

        <div class="actions">
          <button class="btn-primary" onclick="registerPlayer()">Registrarme</button>
        </div>

        <div id="register_msg" class="msg"></div>
      </div>

      <!-- LOGIN -->
      <div id="loginBox" class="hidden">
        <div class="form-grid">
          <div class="field">
            <label for="login_enrolment">Matrícula / ID único</label>
            <input id="login_enrolment" placeholder="Ej: A01234567">
          </div>

          <div class="field">
            <label for="login_code">Código temporal</label>
            <input id="login_code" placeholder="Ej: ABCD-EFGH">
          </div>
        </div>

        <div class="actions">
          <button class="btn-primary" onclick="loginPlayer()">Ingresar al catálogo</button>
        </div>

        <div id="login_msg" class="msg"></div>
      </div>
    </div>
  </section>

  <section id="seasonScreen" class="screen hidden">
    <div class="panel">
      <div class="panel-header">
        <h2>Elige una temporada</h2>
        <p>Antes de mostrar el catálogo, selecciona si deseas consultar Primavera o Invierno.</p>
      </div>

      <div class="season-grid">
        <button class="season-card" onclick="selectSeason('primavera')">
          <span class="season-badge badge-spring">Primavera</span>
          <h3>Oferta de Primavera</h3>
          <p>Consulta los proyectos correspondientes al periodo de primavera.</p>
        </button>

        <button class="season-card" onclick="selectSeason('invierno')">
          <span class="season-badge badge-winter">Invierno</span>
          <h3>Oferta de Invierno</h3>
          <p>Consulta los proyectos correspondientes al periodo de invierno.</p>
        </button>
      </div>
    </div>
  </section>

  <main id="appScreen" class="container hidden">
    <section class="filters">
      <div class="filters-top">
        <div>
          <div class="filters-title">Búsqueda y filtros</div>
          <div class="filters-subtitle">Refina el catálogo con criterios específicos.</div>
        </div>
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
          <button class="btn-secondary" onclick="goBackToSeasonMenu()">Cambiar temporada</button>
        </div>
      </div>
    </section>

    <div class="toolbar">
      <div>
        <div id="resultsCount" class="results-count">Selecciona una temporada</div>
        <div class="results-hint">Consulta disponibilidad y detalles del horario por proyecto.</div>
      </div>

      <div id="seasonChip" class="season-chip hidden"></div>
    </div>

    <div id="results" class="loading">Selecciona una temporada para cargar el catálogo...</div>
  </main>

  <script>
    let currentSeason = null;
    let playerLoggedIn = false;

    async function getJSON(url) {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Error ' + response.status);
      return response.json();
    }

    function escapeHTML(value) {
      return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function showAuthTab(tab) {
      const registerBox = document.getElementById('registerBox');
      const loginBox = document.getElementById('loginBox');
      const btnShowRegister = document.getElementById('btnShowRegister');
      const btnShowLogin = document.getElementById('btnShowLogin');

      if (tab === 'register') {
        registerBox.classList.remove('hidden');
        loginBox.classList.add('hidden');
        btnShowRegister.classList.add('active');
        btnShowLogin.classList.remove('active');
      } else {
        registerBox.classList.add('hidden');
        loginBox.classList.remove('hidden');
        btnShowRegister.classList.remove('active');
        btnShowLogin.classList.add('active');
      }
    }

    function seasonLabel(season) {
      if (season === 'primavera') return 'Primavera';
      if (season === 'invierno') return 'Invierno';
      return '';
    }

    function updateSeasonUI() {
      const label = seasonLabel(currentSeason);
      const heroTitle = document.getElementById('heroTitle');
      const heroSubtitle = document.getElementById('heroSubtitle');
      const seasonChip = document.getElementById('seasonChip');

      if (playerLoggedIn && currentSeason) {
        heroTitle.textContent = 'Oferta de ' + label;
        heroSubtitle.textContent = 'Explora los proyectos disponibles para la temporada seleccionada.';
        seasonChip.textContent = 'Temporada: ' + label;
        seasonChip.classList.remove('hidden');
      } else if (playerLoggedIn) {
        heroTitle.textContent = 'Oferta de Proyectos';
        heroSubtitle.textContent = 'Selecciona una temporada para consultar los proyectos disponibles.';
        seasonChip.textContent = '';
        seasonChip.classList.add('hidden');
      } else {
        heroTitle.textContent = 'Acceso al catálogo';
        heroSubtitle.textContent = 'Regístrate o inicia sesión con tu matrícula y código temporal para consultar la oferta disponible.';
        seasonChip.textContent = '';
        seasonChip.classList.add('hidden');
      }
    }

    async function registerPlayer() {
      const msg = document.getElementById('register_msg');
      msg.textContent = '';
      msg.className = 'msg';

      const payload = {
        first_name: document.getElementById('reg_first_name').value.trim(),
        second_name: document.getElementById('reg_second_name').value.trim(),
        p_last_name: document.getElementById('reg_p_last_name').value.trim(),
        m_last_name: document.getElementById('reg_m_last_name').value.trim(),
        email: document.getElementById('reg_email').value.trim(),
        enrolment_number: document.getElementById('reg_enrolment_number').value.trim(),
        phone_number: document.getElementById('reg_phone_number').value.trim(),
        degree: document.getElementById('reg_degree').value.trim(),
        semester: document.getElementById('reg_semester').value.trim()
      };

      try {
        const res = await fetch('/api/player/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) throw new Error(data.error || 'Error al registrar');

        msg.textContent = 'Registro exitoso. Ahora solicita tu código al staff e inicia sesión.';
        msg.className = 'msg ok';

        document.getElementById('login_enrolment').value = payload.enrolment_number;
        showAuthTab('login');
      } catch (e) {
        msg.textContent = e.message;
        msg.className = 'msg error';
      }
    }

    async function loginPlayer() {
      const enrolment = document.getElementById('login_enrolment').value.trim();
      const code = document.getElementById('login_code').value.trim();
      const msg = document.getElementById('login_msg');

      msg.textContent = '';
      msg.className = 'msg';

      if (!enrolment || !code) {
        msg.textContent = 'Completa todos los campos.';
        msg.className = 'msg error';
        return;
      }

      try {
        const res = await fetch('/api/player/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            enrolment_number: enrolment,
            code: code
          })
        });

        const data = await res.json();

        if (!res.ok) throw new Error(data.error || 'Error de acceso');

        playerLoggedIn = true;
        updateSeasonUI();

        document.getElementById('authScreen').classList.add('hidden');
        document.getElementById('seasonScreen').classList.remove('hidden');

      } catch (e) {
        msg.textContent = e.message;
        msg.className = 'msg error';
      }
    }

    function fillSelect(id, items, labelKey = 'description') {
      const el = document.getElementById(id);
      const placeholder = el.options[0].outerHTML;
      el.innerHTML = placeholder;

      for (const item of items || []) {
        const opt = document.createElement('option');
        opt.value = item.id;
        opt.textContent = item[labelKey];
        el.appendChild(opt);
      }
    }

    async function loadCatalogs() {
      if (!currentSeason) return;

      const data = await getJSON('/api/catalogs?temporada=' + encodeURIComponent(currentSeason));
      fillSelect('socio', data.socio, 'name');
      fillSelect('modalidad', data.modalidad);
      fillSelect('dia', data.dias);
      fillSelect('horario', data.horario);
    }

    function card(p) {
      const disponible = Number(p.cupos_disponibles) > 0;
      const statusClass = disponible ? 'available' : 'full';
      const statusText = disponible ? 'Disponible' : 'Sin cupo';

      const descripcion = p.descripcion
        ? '<div class="desc">' + escapeHTML(p.descripcion) + '</div>'
        : '';

      const detalleHorario = p.descripcion_horario
        ? '<div class="desc"><strong>Detalle horario:</strong> ' + escapeHTML(p.descripcion_horario) + '</div>'
        : '';

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

          ${descripcion}
          ${detalleHorario}
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

      resultsCount.textContent = `${data.length} proyecto${data.length === 1 ? '' : 's'} encontrado${data.length === 1 ? '' : 's'} en ${seasonLabel(currentSeason)}`;

      if (!data.length) {
        root.className = '';
        root.innerHTML = `
          <div class="empty">
            <strong>No se encontraron proyectos con esos filtros.</strong>
            <div class="muted" style="margin-top:8px;">Prueba limpiando filtros o usando una búsqueda más general.</div>
          </div>
        `;
        return;
      }

      root.className = '';
      root.innerHTML = `<div class="grid">${data.map(card).join('')}</div>`;
    }

    function clearFilters() {
      ['q', 'socio', 'modalidad', 'dia', 'horario'].forEach(id => {
        document.getElementById(id).value = '';
      });
      loadProjects();
    }

    async function selectSeason(season) {
      currentSeason = season;
      updateSeasonUI();

      document.getElementById('seasonScreen').classList.add('hidden');
      document.getElementById('appScreen').classList.remove('hidden');

      document.getElementById('results').className = 'loading';
      document.getElementById('results').innerHTML = 'Cargando oferta...';
      document.getElementById('resultsCount').textContent = 'Cargando proyectos...';

      clearFilterValuesOnly();

      try {
        await loadCatalogs();
        await loadProjects();
      } catch (e) {
        document.getElementById('results').className = '';
        document.getElementById('results').innerHTML = `
          <div class="empty">
            <strong>Error cargando oferta</strong>
            <div class="muted" style="margin-top:8px;">${escapeHTML(e.message)}</div>
          </div>
        `;
        document.getElementById('resultsCount').textContent = 'No fue posible cargar los proyectos';
      }
    }

    function clearFilterValuesOnly() {
      ['q', 'socio', 'modalidad', 'dia', 'horario'].forEach(id => {
        document.getElementById(id).value = '';
      });
    }

    function goBackToSeasonMenu() {
      currentSeason = null;
      updateSeasonUI();
      clearFilterValuesOnly();

      document.getElementById('appScreen').classList.add('hidden');
      document.getElementById('seasonScreen').classList.remove('hidden');

      document.getElementById('results').className = 'loading';
      document.getElementById('results').innerHTML = 'Selecciona una temporada para cargar la oferta...';
      document.getElementById('resultsCount').textContent = 'Selecciona una temporada';
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('q').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') loadProjects();
      });

      document.getElementById('login_code').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') loginPlayer();
      });

      document.getElementById('login_enrolment').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') loginPlayer();
      });

      updateSeasonUI();
    });
  </script>
</body>
</html>
"""