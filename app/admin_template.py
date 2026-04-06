ADMIN_HTML = r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Panel Administrativo</title>
  <script src="https://unpkg.com/html5-qrcode"></script>
  <style>
    :root {
      --bg: #F4F7FA;
      --panel: #FFFFFF;
      --panel-soft: #FAFBFD;
      --text: #1F2937;
      --text-soft: #6B7280;
      --muted: #94A3B8;
      --line: #E5E7EB;
      --line-strong: #D1D5DB;

      --orange: #FF8C42;
      --green: #43AA8B;
      --purple: #7D5BA6;
      --pink: #F25C78;

      --orange-soft: #FFF3EA;
      --green-soft: #ECFDF7;
      --purple-soft: #F5F0FB;
      --pink-soft: #FFF1F5;

      --shadow-sm: 0 2px 10px rgba(15, 23, 42, 0.04);
      --shadow-md: 0 10px 24px rgba(15, 23, 42, 0.06);

      --r-md: 12px;
      --r-lg: 16px;
      --r-xl: 22px;
      --r-pill: 999px;

      --module-accent: var(--purple);
      --module-accent-soft: var(--purple-soft);
    }

    * { box-sizing: border-box; }

    html, body {
      margin: 0;
      padding: 0;
      font-family: Inter, Montserrat, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
    }

    .hidden { display: none !important; }

    .app-shell {
      display: grid;
      grid-template-columns: 300px 1fr;
      min-height: 100vh;
    }

    .sidebar {
      background: #FFFFFF;
      border-right: 1px solid var(--line);
      padding: 18px 16px;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
    }

    .sidebar-shell {
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .brand-box {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--r-xl);
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .brand-title {
      font-size: 1.06rem;
      font-weight: 900;
      margin-bottom: 4px;
      color: var(--text);
    }

    .brand-subtitle {
      font-size: .88rem;
      color: var(--text-soft);
      line-height: 1.45;
    }

    .role-box {
      margin-top: 12px;
      border-radius: var(--r-md);
      background: var(--panel-soft);
      border: 1px solid var(--line);
      padding: 12px 14px;
      font-size: .9rem;
      color: var(--text-soft);
      font-weight: 700;
    }

    .nav-group {
      display: grid;
      gap: 10px;
    }

    .nav-group-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 0 4px;
    }

    .nav-group-title {
      font-size: .76rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      font-weight: 900;
      color: var(--muted);
    }

    .nav-group-pill {
      font-size: .72rem;
      font-weight: 900;
      padding: 6px 9px;
      border-radius: var(--r-pill);
      white-space: nowrap;
    }

    .pill-purple { background: var(--purple-soft); color: var(--purple); }
    .pill-orange { background: var(--orange-soft); color: var(--orange); }
    .pill-green  { background: var(--green-soft); color: var(--green); }
    .pill-pink   { background: var(--pink-soft); color: var(--pink); }
    .pill-neutral { background: #F3F4F6; color: #374151; }

    .nav-list {
      display: grid;
      gap: 8px;
    }

    .nav-item {
      width: 100%;
      text-align: left;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text);
      border-radius: var(--r-lg);
      padding: 12px 14px;
      font-size: .94rem;
      font-weight: 800;
      cursor: pointer;
      transition: background .18s ease, transform .16s ease, border-color .18s ease, box-shadow .18s ease;
    }

    .nav-item:hover {
      transform: translateY(-1px);
      background: #F9FAFB;
      border-color: var(--line);
      box-shadow: var(--shadow-sm);
    }

    .nav-item.active {
      background: var(--module-accent-soft);
      border-color: color-mix(in srgb, var(--module-accent) 35%, white);
      color: var(--module-accent);
      box-shadow: var(--shadow-sm);
    }

    .sidebar-actions {
      display: grid;
      gap: 10px;
      margin-top: 6px;
    }

    .sidebar-actions a,
    .sidebar-actions button {
      text-decoration: none;
      text-align: center;
      border: 1px solid var(--line);
      background: white;
      color: var(--text-soft);
      border-radius: var(--r-md);
      padding: 11px 12px;
      font-size: .9rem;
      font-weight: 800;
      cursor: pointer;
      transition: transform .16s ease, box-shadow .16s ease, border-color .16s ease;
    }

    .sidebar-actions a:hover,
    .sidebar-actions button:hover {
      transform: translateY(-1px);
      box-shadow: var(--shadow-sm);
      border-color: var(--line-strong);
    }

    .main {
      padding: 22px;
    }

    .topbar {
      margin-bottom: 18px;
    }

    .screen-header {
      background: linear-gradient(135deg, white 0%, var(--module-accent-soft) 100%);
      border: 1px solid color-mix(in srgb, var(--module-accent) 25%, white);
      border-radius: var(--r-xl);
      padding: 18px 20px;
      box-shadow: var(--shadow-md);
    }

    .screen-header__content {
      display: flex;
      justify-content: space-between;
      gap: 14px;
      flex-wrap: wrap;
      align-items: center;
    }

    .screen-kicker {
      font-size: .76rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--module-accent);
      font-weight: 900;
      margin-bottom: 5px;
    }

    .screen-title strong {
      display: block;
      font-size: 1.34rem;
      font-weight: 900;
      margin-bottom: 4px;
      color: var(--text);
    }

    .screen-title span {
      display: block;
      color: var(--text-soft);
      font-size: .95rem;
    }

    .screen-badges {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 12px;
      border-radius: var(--r-pill);
      font-size: .8rem;
      font-weight: 900;
      white-space: nowrap;
      border: 1px solid transparent;
    }

    .chip-accent {
      background: var(--module-accent-soft);
      color: var(--module-accent);
      border-color: color-mix(in srgb, var(--module-accent) 20%, white);
    }

    .chip-dark {
      background: white;
      color: var(--text-soft);
      border-color: var(--line);
    }

    .login-wrap {
      max-width: 760px;
      margin: 40px auto;
      padding: 0 18px;
    }

    .login-card,
    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      box-shadow: var(--shadow-sm);
      padding: 22px;
    }

    .msg {
      display: none;
      margin-bottom: 18px;
      padding: 14px 16px;
      border-radius: var(--r-md);
      font-size: .94rem;
      font-weight: 800;
      border: 1px solid transparent;
      box-shadow: var(--shadow-sm);
    }

    .msg.ok {
      display: block;
      background: var(--green-soft);
      color: var(--green);
      border-color: #CDEFE4;
    }

    .msg.err {
      display: block;
      background: var(--pink-soft);
      color: var(--pink);
      border-color: #FFD4DD;
    }

    .module {
      display: none;
    }

    .module.active {
      display: block;
    }

    .module-grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 18px;
    }

    .span-12 { grid-column: span 12; }
    .span-8 { grid-column: span 8; }
    .span-6 { grid-column: span 6; }
    .span-4 { grid-column: span 4; }

    .module-card-title {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }

    h2, h3 {
      margin: 0;
      line-height: 1.2;
    }

    h2 {
      font-size: 1.14rem;
      font-weight: 900;
    }

    h3 {
      font-size: 1rem;
      font-weight: 900;
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

    .screen-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 12px;
      border-radius: var(--r-pill);
      background: var(--module-accent-soft);
      color: var(--module-accent);
      font-size: .82rem;
      font-weight: 900;
      border: 1px solid color-mix(in srgb, var(--module-accent) 16%, white);
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
      font-size: .78rem;
      font-weight: 900;
      color: var(--text-soft);
      text-transform: uppercase;
      letter-spacing: .04em;
    }

    input, select, textarea, button {
      width: 100%;
      min-height: 44px;
      border-radius: var(--r-md);
      border: 1px solid var(--line-strong);
      background: white;
      color: var(--text);
      font-size: .94rem;
      padding: 10px 12px;
      outline: none;
      transition: border-color .18s ease, box-shadow .18s ease, transform .16s ease;
    }

    textarea {
      min-height: 100px;
      resize: vertical;
    }

    input:focus, select:focus, textarea:focus {
      border-color: var(--module-accent);
      box-shadow: 0 0 0 3px color-mix(in srgb, var(--module-accent) 14%, white);
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

    .btn-primary,
    .btn-secondary,
    .btn-danger {
      min-height: 44px;
      border-radius: var(--r-md);
      padding: 10px 14px;
      font-size: .94rem;
      font-weight: 900;
      cursor: pointer;
      transition: transform .15s ease, box-shadow .15s ease, opacity .15s ease, border-color .15s ease;
    }

    .btn-primary:hover,
    .btn-secondary:hover,
    .btn-danger:hover {
      transform: translateY(-1px) scale(1.01);
    }

    .btn-primary {
      background: var(--module-accent);
      color: white;
      border: none;
      box-shadow: 0 8px 18px color-mix(in srgb, var(--module-accent) 22%, white);
    }

    .btn-secondary {
      background: #FFFFFF;
      color: #374151;
      border: 1px solid var(--line);
      box-shadow: var(--shadow-sm);
    }

    .btn-danger {
      background: var(--pink);
      color: white;
      border: none;
      box-shadow: 0 8px 18px rgba(242,92,120,0.18);
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 11px;
      border-radius: var(--r-pill);
      font-size: .76rem;
      font-weight: 900;
      white-space: nowrap;
    }

    .badge-success { background: var(--green-soft); color: var(--green); }
    .badge-warn { background: var(--orange-soft); color: var(--orange); }
    .badge-danger { background: var(--pink-soft); color: var(--pink); }
    .badge-purple { background: var(--purple-soft); color: var(--purple); }
    .badge-neutral { background: #F3F4F6; color: #374151; }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-top: 16px;
    }

    .kpi-card {
      border-radius: var(--r-lg);
      padding: 18px;
      color: white;
      box-shadow: var(--shadow-sm);
    }

    .kpi-card--green { background: linear-gradient(135deg, #43AA8B 0%, #57C3A2 100%); }
    .kpi-card--orange { background: linear-gradient(135deg, #FF8C42 0%, #FFAA6E 100%); }
    .kpi-card--purple { background: linear-gradient(135deg, #7D5BA6 0%, #9B79C6 100%); }
    .kpi-card--pink { background: linear-gradient(135deg, #F25C78 0%, #FF7D96 100%); }

    .kpi-label {
      font-size: .78rem;
      text-transform: uppercase;
      letter-spacing: .05em;
      font-weight: 900;
      opacity: .95;
      margin-bottom: 8px;
    }

    .kpi-value {
      font-size: 2rem;
      font-weight: 900;
      line-height: 1;
      margin-bottom: 8px;
    }

    .kpi-sub {
      font-size: .84rem;
      opacity: .96;
    }

    .meta {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
      margin-top: 10px;
    }

    .meta-box {
      border: 1px solid var(--line);
      background: var(--panel-soft);
      border-radius: var(--r-md);
      padding: 10px 12px;
    }

    .meta-label {
      display: block;
      font-size: .72rem;
      text-transform: uppercase;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 4px;
      letter-spacing: .04em;
    }

    .meta-value {
      color: var(--text);
      font-weight: 800;
      font-size: .92rem;
      line-height: 1.4;
    }

    .record-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }

    .record-card {
      background: #FFF;
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .record-card__head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }

    .record-card__title {
      font-size: .98rem;
      font-weight: 900;
      color: var(--text);
      margin-bottom: 3px;
    }

    .record-card__sub {
      font-size: .84rem;
      color: var(--text-soft);
    }

    .record-stack {
      display: grid;
      gap: 8px;
      margin-top: 10px;
    }

    .stack-row {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: start;
      font-size: .88rem;
    }

    .stack-row strong {
      color: var(--text-soft);
      font-weight: 800;
      min-width: 120px;
    }

    .stack-row span {
      text-align: right;
      color: var(--text);
      font-weight: 700;
      word-break: break-word;
    }

    .mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: .9rem;
      background: #111827;
      color: #E5EEF8;
      border-radius: var(--r-md);
      padding: 9px 11px;
      word-break: break-all;
      display: inline-block;
    }

    .mono-soft {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: .88rem;
      color: #334155;
      background: #F3F4F6;
      border: 1px solid var(--line);
      padding: 5px 8px;
      border-radius: 10px;
      display: inline-block;
    }

    .xp-wrapper {
      display: flex;
      flex-direction: column;
      gap: 6px;
      min-width: 180px;
    }

    .xp-text {
      font-size: .78rem;
      font-weight: 900;
      color: var(--text-soft);
      display: flex;
      justify-content: space-between;
      gap: 10px;
    }

    .xp-bar-bg {
      width: 100%;
      height: 12px;
      background: #E5E7EB;
      border-radius: 999px;
      overflow: hidden;
    }

    .xp-bar-fill {
      height: 100%;
      width: 0%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--purple) 0%, #9B79C6 100%);
      transition: width .35s ease;
    }

    .xp-bar-fill.level-up {
      background: linear-gradient(90deg, var(--green) 0%, #57C3A2 100%);
    }

    .scanner-shell {
      max-width: 620px;
      margin: 18px auto 0;
      display: grid;
      gap: 14px;
      justify-items: center;
    }

    #staffScanner {
      width: 100%;
      max-width: 420px;
      border-radius: var(--r-lg);
      overflow: hidden;
      border: 1px solid var(--line);
      background: white;
      box-shadow: var(--shadow-sm);
    }

    .center-note {
      text-align: center;
      color: var(--text-soft);
      font-size: .9rem;
      max-width: 620px;
      margin: 0 auto;
    }

    @media (max-width: 1280px) {
      .stats-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 1200px) {
      .app-shell {
        grid-template-columns: 1fr;
      }

      .sidebar {
        position: static;
        height: auto;
      }

      .span-8, .span-6, .span-4 {
        grid-column: span 12;
      }
    }

    @media (max-width: 700px) {
      .stats-grid {
        grid-template-columns: 1fr;
      }

      .main {
        padding: 18px;
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
  <div id="loginWrap" class="login-wrap">
    <div id="msg" class="msg"></div>

    <div id="loginCard" class="login-card">
      <h2>Acceso Administrador / Staff</h2>
      <div class="muted">
        Ingresa tu clave para abrir el panel. Staff verá solo herramientas operativas.
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
  </div>

  <div id="appShell" class="app-shell hidden">
    <aside class="sidebar">
      <div class="sidebar-shell">
        <div class="brand-box">
          <div class="brand-title">Panel de Eventos Grandes</div>
          <div class="brand-subtitle">
            Operación clara, rápida y visual para temporadas, accesos y seguimiento.
          </div>

          <div class="role-box" id="sidebarRoleBox">
            Rol actual: —
          </div>
        </div>

        <div id="adminNavWrap">
          <div class="nav-group">
            <div class="nav-group-header">
              <div class="nav-group-title">Estrategia</div>
              <span class="nav-group-pill pill-purple">Morado</span>
            </div>
            <div class="nav-list">
              <button class="nav-item active" data-module="summaryModule" onclick="showModule('summaryModule', this)">Dashboard</button>
              <button class="nav-item" data-module="eventsModule" onclick="showModule('eventsModule', this)">Temporadas</button>
              <button class="nav-item" data-module="masterProjectsModule" onclick="showModule('masterProjectsModule', this)">Proyectos Base</button>
            </div>
          </div>

          <div class="nav-group">
            <div class="nav-group-header">
              <div class="nav-group-title">Operación</div>
              <div style="display:flex; gap:6px; flex-wrap:wrap;">
                <span class="nav-group-pill pill-orange">Naranja</span>
                <span class="nav-group-pill pill-green">Verde</span>
              </div>
            </div>
            <div class="nav-list">
              <button class="nav-item" data-module="eventProjectsModule" onclick="showModule('eventProjectsModule', this)">Proyectos Activos</button>
              <button class="nav-item" data-module="tokensModule" onclick="showModule('tokensModule', this)">Generar Tokens</button>
              <button class="nav-item" data-module="registrationsModule" onclick="showModule('registrationsModule', this)">Inscritos</button>
              <button class="nav-item" data-module="checkinModule" onclick="showModule('checkinModule', this)">Check-in (QR)</button>
            </div>
          </div>

          <div class="nav-group">
            <div class="nav-group-header">
              <div class="nav-group-title">Control</div>
              <span class="nav-group-pill pill-pink">Rosa</span>
            </div>
            <div class="nav-list">
              <button class="nav-item" data-module="incidentsModule" onclick="showModule('incidentsModule', this)">Incidentes</button>
              <button class="nav-item" data-module="importExportModule" onclick="showModule('importExportModule', this)">Carga Masiva</button>
            </div>
          </div>
        </div>

        <div id="staffNavWrap" class="hidden">
          <div class="nav-group">
            <div class="nav-group-header">
              <div class="nav-group-title">Operación Staff</div>
              <span class="nav-group-pill pill-green">Verde</span>
            </div>
            <div class="nav-list">
              <button class="nav-item active" data-module="checkinModule" onclick="showModule('checkinModule', this)">Check-in (QR)</button>
              <button class="nav-item" data-module="incidentsModule" onclick="showModule('incidentsModule', this)">Incidentes</button>
            </div>
          </div>
        </div>

        <div class="sidebar-actions">
          <a href="/">Vista Alumno</a>
          <a href="/health">Health</a>
          <button type="button" onclick="logout()">Cerrar sesión</button>
        </div>
      </div>
    </aside>

    <main class="main">
      <div id="msgApp" class="msg"></div>

      <div class="topbar">
        <div class="screen-header">
          <div class="screen-header__content">
            <div class="screen-title">
              <div class="screen-kicker" id="moduleKicker">Estrategia</div>
              <strong id="moduleTitle">Dashboard</strong>
              <span id="moduleSubtitle">Visión ejecutiva del evento.</span>
            </div>

            <div class="screen-badges">
              <span class="chip chip-accent" id="headerAccentBadge">Módulo activo</span>
              <span class="chip chip-dark" id="headerRoleBadge">Panel operativo</span>
            </div>
          </div>
        </div>
      </div>

      <div class="module active" id="summaryModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Dashboard Ejecutivo</h2>
              <span class="screen-chip">Resumen general</span>
            </div>
            <div class="muted">
              KPI ejecutivos y avance por proyecto para la temporada seleccionada.
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

            <div id="dashboardProjectsBody" class="record-grid">
              <div class="record-card">
                <div class="record-card__title">Selecciona una temporada</div>
                <div class="record-card__sub">Carga el dashboard para ver proyectos, ocupación y tokens.</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="module" id="eventsModule">
        <div class="module-grid">
          <div class="card span-6">
            <div class="module-card-title">
              <h2>Crear temporada</h2>
              <span class="screen-chip">Configuración</span>
            </div>
            <div class="muted">
              Crea una temporada y define sus ventanas operativas.
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
              <button type="button" class="btn-primary" onclick="createAdminEvent()">Crear temporada</button>
              <button type="button" class="btn-secondary" onclick="loadEvents()">Recargar</button>
            </div>
          </div>

          <div class="card span-6">
            <div class="module-card-title">
              <h2>Operar temporada</h2>
              <span class="screen-chip">Edición rápida</span>
            </div>
            <div class="muted">
              Ajusta estado y visibilidad de una temporada existente.
            </div>

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

            <div id="selectedEventInfo" class="record-grid"></div>
          </div>

          <div class="card span-12">
            <div class="module-card-title">
              <h2>Temporadas existentes</h2>
              <span class="screen-chip">Historial</span>
            </div>
            <div id="eventsList" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="masterProjectsModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Proyectos Base</h2>
              <span class="screen-chip">Catálogo maestro</span>
            </div>
            <div class="muted">
              Aquí vive la ficha base de cada proyecto.
            </div>

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
              <button type="button" class="btn-primary" onclick="createMasterProject()">Crear proyecto base</button>
              <button type="button" class="btn-secondary" onclick="loadMasterProjects()">Recargar lista</button>
            </div>
          </div>

          <div class="card span-12">
            <div class="module-card-title">
              <h2>Catálogo de proyectos base</h2>
              <span class="screen-chip">Consulta</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Buscar proyecto base</label>
                <input id="masterProjectsSearch" placeholder="Buscar por nombre, organización, líder..." oninput="loadMasterProjects()">
              </div>
            </div>

            <div id="masterProjectsList" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="eventProjectsModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Proyectos Activos</h2>
              <span class="screen-chip">Operación</span>
            </div>
            <div class="muted">
              Activa un proyecto base dentro de una temporada y define su cupo.
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Temporada</label>
                <select id="eventProjectEventSelector"></select>
              </div>

              <div class="field">
                <label>Proyecto base</label>
                <select id="projectSelector"></select>
              </div>

              <div class="field">
                <label>Slots / cupo total</label>
                <input id="slotsInput" type="number" min="0" placeholder="Ej: 10">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="addProjectToEvent()">Activar proyecto</button>
              <button type="button" class="btn-secondary" onclick="loadEventProjects()">Recargar proyectos</button>
            </div>

            <div id="eventProjectsList" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="tokensModule">
        <div class="module-grid">
          <div class="card span-6">
            <div class="module-card-title">
              <h2>Generar Tokens</h2>
              <span class="screen-chip">Acceso</span>
            </div>
            <div class="muted">
              Genera tokens para proyectos activos y controla su vigencia.
            </div>

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
                <input id="tokensLength" type="number" min="6" max="20" value="8">
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
              Valor actual: <span id="ttl_current" class="badge badge-warn">—</span>
            </div>

            <div id="tokensGenerationResult" class="record-grid"></div>
          </div>

          <div class="card span-6">
            <div class="module-card-title">
              <h2>Revocar token</h2>
              <span class="screen-chip">Acción crítica</span>
            </div>
            <div class="muted">
              Revoca un token cuando haya error, conflicto o corrección operativa.
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Token</label>
                <input id="revokeTokenValue" placeholder="Ej: A7K9P3Q2">
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

          <div class="card span-12">
            <div class="module-card-title">
              <h2>Tokens del proyecto</h2>
              <span class="screen-chip">Seguimiento</span>
            </div>

            <div class="form-grid">
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
            <div id="tokensCards" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="registrationsModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Inscritos</h2>
              <span class="screen-chip">Cierre final</span>
            </div>
            <div class="muted">
              Consulta qué alumno cerró contrato, en qué proyecto y con qué token.
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Temporada</label>
                <select id="registrationsEventSelector"></select>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="loadRegistrations()">Cargar inscripciones</button>
            </div>

            <div id="registrationsCards" class="record-grid">
              <div class="record-card">
                <div class="record-card__title">Selecciona una temporada</div>
                <div class="record-card__sub">Carga inscripciones cerradas para ver resultados.</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="module" id="checkinModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Check-in (QR)</h2>
              <span class="screen-chip">Acceso presencial</span>
            </div>
            <div class="center-note">
              Escanea el QR, valida matrícula y habilita acceso sin ruido visual.
            </div>

            <div class="form-grid" style="margin-top:18px;">
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

            <div class="scanner-shell">
              <div id="staffScanner"></div>
            </div>

            <div id="staffCheckinInfo" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="incidentsModule">
        <div class="module-grid">
          <div class="card span-6">
            <div class="module-card-title">
              <h2>Incidentes</h2>
              <span class="screen-chip">Control crítico</span>
            </div>
            <div class="muted">
              Reporta y da seguimiento a errores, conflictos o casos especiales.
            </div>

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
            </div>
          </div>

          <div class="card span-6">
            <div class="module-card-title">
              <h2>Listado de incidentes</h2>
              <span class="screen-chip">Seguimiento</span>
            </div>
            <div class="muted">
              Revisa severidad, estado y resuelve incidentes abiertos.
            </div>

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

            <div id="incidentsList" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="importExportModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Carga Masiva (Import / Export)</h2>
              <span class="screen-chip">Control de catálogo</span>
            </div>
            <div class="muted">
              Importa o exporta proyectos base desde Excel.
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

            <div id="importProjectsResult" class="record-grid"></div>
          </div>
        </div>
      </div>
    </main>
  </div>

  <script>
    const storage = sessionStorage;
    let staffQrScanner = null;
    let lastScannedPassSession = null;
    let allEvents = [];
    let masterProjectsCache = [];
    let eventProjectsCache = [];

    const MODULE_META = {
      summaryModule: {
        title: 'Dashboard',
        subtitle: 'Visión ejecutiva del evento.',
        kicker: 'Estrategia',
        accent: '#7D5BA6',
        accentSoft: '#F5F0FB'
      },
      eventsModule: {
        title: 'Temporadas',
        subtitle: 'Configuración de ciclos y ventanas operativas.',
        kicker: 'Estrategia',
        accent: '#7D5BA6',
        accentSoft: '#F5F0FB'
      },
      masterProjectsModule: {
        title: 'Proyectos Base',
        subtitle: 'Catálogo maestro de proyectos.',
        kicker: 'Estrategia',
        accent: '#7D5BA6',
        accentSoft: '#F5F0FB'
      },
      eventProjectsModule: {
        title: 'Proyectos Activos',
        subtitle: 'Activación de proyectos por temporada.',
        kicker: 'Operación',
        accent: '#FF8C42',
        accentSoft: '#FFF3EA'
      },
      tokensModule: {
        title: 'Generar Tokens',
        subtitle: 'Flujos de acceso, vigencia y control de tokens.',
        kicker: 'Operación',
        accent: '#FF8C42',
        accentSoft: '#FFF3EA'
      },
      registrationsModule: {
        title: 'Inscritos',
        subtitle: 'Consulta de cierres de inscripción.',
        kicker: 'Operación',
        accent: '#43AA8B',
        accentSoft: '#ECFDF7'
      },
      checkinModule: {
        title: 'Check-in (QR)',
        subtitle: 'Escaneo y habilitación de acceso.',
        kicker: 'Operación',
        accent: '#43AA8B',
        accentSoft: '#ECFDF7'
      },
      incidentsModule: {
        title: 'Incidentes',
        subtitle: 'Seguimiento de problemas y casos especiales.',
        kicker: 'Control',
        accent: '#F25C78',
        accentSoft: '#FFF1F5'
      },
      importExportModule: {
        title: 'Carga Masiva',
        subtitle: 'Importación y exportación del catálogo.',
        kicker: 'Control',
        accent: '#F25C78',
        accentSoft: '#FFF1F5'
      }
    };

    function escapeHTML(value) {
      return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function showMsg(text, ok = true) {
      const el = document.getElementById('msgApp');
      const elLogin = document.getElementById('msg');
      const target = document.getElementById('appShell').classList.contains('hidden') ? elLogin : el;

      target.textContent = text || '';
      target.className = 'msg ' + (ok ? 'ok' : 'err');
    }

    function getKey() {
      return storage.getItem('ADMIN_API_KEY') || '';
    }

    function getRole() {
      return storage.getItem('ADMIN_ROLE') || '';
    }

    function setModuleAccent(accent, accentSoft) {
      document.documentElement.style.setProperty('--module-accent', accent);
      document.documentElement.style.setProperty('--module-accent-soft', accentSoft);
    }

    function showModule(moduleId, btn = null) {
      document.querySelectorAll('.module').forEach(m => m.classList.remove('active'));
      const moduleEl = document.getElementById(moduleId);
      if (moduleEl) moduleEl.classList.add('active');

      document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
      document.querySelectorAll(`.nav-item[data-module="${moduleId}"]`).forEach(x => x.classList.add('active'));

      const meta = MODULE_META[moduleId] || MODULE_META.summaryModule;
      document.getElementById('moduleTitle').textContent = meta.title;
      document.getElementById('moduleSubtitle').textContent = meta.subtitle;
      document.getElementById('moduleKicker').textContent = meta.kicker;
      document.getElementById('headerAccentBadge').textContent = meta.title;

      setModuleAccent(meta.accent, meta.accentSoft);
    }

    function applyRoleUI(role) {
      const loginWrap = document.getElementById('loginWrap');
      const appShell = document.getElementById('appShell');
      const roleBadge = document.getElementById('roleBadge');
      const sidebarRoleBox = document.getElementById('sidebarRoleBox');
      const headerRoleBadge = document.getElementById('headerRoleBadge');

      roleBadge.textContent = role ? `Sesión activa como: ${role}` : 'Sesión actual: —';
      sidebarRoleBox.textContent = role ? `Rol actual: ${role}` : 'Rol actual: —';
      headerRoleBadge.textContent = role ? role : 'Panel operativo';

      loginWrap.classList.toggle('hidden', !!role);
      appShell.classList.toggle('hidden', !role);

      const adminNavWrap = document.getElementById('adminNavWrap');
      const staffNavWrap = document.getElementById('staffNavWrap');

      if (role === 'ADMIN') {
        adminNavWrap.classList.remove('hidden');
        staffNavWrap.classList.add('hidden');
        showModule('summaryModule');
      } else if (role === 'STAFF') {
        adminNavWrap.classList.add('hidden');
        staffNavWrap.classList.remove('hidden');
        showModule('checkinModule');
      }
    }

    function boolFromString(v) {
      return String(v).toLowerCase() === 'true';
    }

    function toSqlDateTime(value) {
      if (!value) return null;
      return value.replace('T', ' ') + ':00';
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

    function statusBadge(status) {
      const value = String(status || '').toUpperCase();
      const map = {
        DRAFT: ['badge badge-purple', 'DRAFT'],
        VISIBLE: ['badge badge-purple', 'VISIBLE'],
        ONSITE: ['badge badge-success', 'ONSITE'],
        CLOSED: ['badge badge-warn', 'CLOSED'],
        ARCHIVED: ['badge badge-danger', 'ARCHIVED'],
        ACTIVE: ['badge badge-success', 'ACTIVE'],
        HIDDEN: ['badge badge-warn', 'HIDDEN'],
        OPEN: ['badge badge-danger', 'OPEN'],
        IN_PROGRESS: ['badge badge-warn', 'IN_PROGRESS'],
        RESOLVED: ['badge badge-success', 'RESOLVED'],
        DISMISSED: ['badge badge-neutral', 'DISMISSED'],
        AVAILABLE: ['badge badge-success', 'AVAILABLE'],
        RESERVED: ['badge badge-warn', 'RESERVED'],
        USED: ['badge badge-neutral', 'USED'],
        REVOKED: ['badge badge-danger', 'REVOKED'],
        EXPIRED: ['badge badge-danger', 'EXPIRED']
      };
      const cfg = map[value] || ['badge badge-neutral', value || '—'];
      return `<span class="${cfg[0]}">${cfg[1]}</span>`;
    }

    function fillSelect(id, items, placeholderText = 'Selecciona', labelFn = null) {
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

    function fillSelectNoBlank(id, items, labelFn = null) {
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

    function renderXPBar(registrados, slotsTotales) {
      const usados = Number(registrados || 0);
      const total = Number(slotsTotales || 0);
      const porcentaje = total > 0 ? Math.round((usados / total) * 100) : 0;
      const porcentajeSeguro = Math.min(porcentaje, 100);
      const levelUpClass = porcentaje >= 100 ? 'level-up' : '';

      return `
        <div class="xp-wrapper">
          <div class="xp-text">
            <span>Ocupación</span>
            <span>${porcentaje}%</span>
          </div>
          <div class="xp-bar-bg">
            <div class="xp-bar-fill ${levelUpClass}" style="width:${porcentajeSeguro}%"></div>
          </div>
        </div>
      `;
    }

    function renderEmptyCard(title, subtitle='') {
      return `
        <div class="record-card">
          <div class="record-card__title">${escapeHTML(title)}</div>
          <div class="record-card__sub">${escapeHTML(subtitle)}</div>
        </div>
      `;
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

    function clearKey(show = true) {
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

        fillSelectNoBlank('eventSelector', allEvents, e => `${e.display_name} · ${e.status}`);
        fillSelectNoBlank('dashboardEventSelector', allEvents, e => `${e.display_name} · ${e.status}`);
        fillSelectNoBlank('eventProjectEventSelector', allEvents, e => `${e.display_name} · ${e.status}`);
        fillSelectNoBlank('registrationsEventSelector', allEvents, e => `${e.display_name} · ${e.status}`);

        const eventsList = document.getElementById('eventsList');
        if (!allEvents.length) {
          eventsList.innerHTML = renderEmptyCard('No hay temporadas creadas todavía', 'Crea la primera temporada para comenzar.');
          document.getElementById('selectedEventInfo').innerHTML = '';
          return showMsg('No hay temporadas creadas todavía');
        }

        eventsList.innerHTML = allEvents.map(e => `
          <div class="record-card">
            <div class="record-card__head">
              <div>
                <div class="record-card__title">${escapeHTML(e.display_name)}</div>
                <div class="record-card__sub">Año ${e.year} · ${e.season}</div>
              </div>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                ${statusBadge(e.status)}
                ${e.is_visible_to_students ? '<span class="badge badge-success">VISIBLE ALUMNO</span>' : '<span class="badge badge-neutral">NO VISIBLE</span>'}
              </div>
            </div>

            <div class="meta">
              <div class="meta-box"><span class="meta-label">Catálogo abre</span><div class="meta-value">${escapeHTML(e.catalog_open_at || '—')}</div></div>
              <div class="meta-box"><span class="meta-label">Inicio presencial</span><div class="meta-value">${escapeHTML(e.onsite_start_at || '—')}</div></div>
              <div class="meta-box"><span class="meta-label">Fin presencial</span><div class="meta-value">${escapeHTML(e.onsite_end_at || '—')}</div></div>
              <div class="meta-box"><span class="meta-label">Cierre registro</span><div class="meta-value">${escapeHTML(e.registration_close_at || '—')}</div></div>
            </div>
          </div>
        `).join('');

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
          <div class="record-card">
            <div class="record-card__head">
              <div>
                <div class="record-card__title">${escapeHTML(e.display_name)}</div>
                <div class="record-card__sub">${e.season} ${e.year}</div>
              </div>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                ${statusBadge(e.status)}
                ${e.is_visible_to_students ? '<span class="badge badge-success">VISIBLE ALUMNO</span>' : '<span class="badge badge-neutral">NO VISIBLE</span>'}
              </div>
            </div>
            <div class="stack-row"><strong>ID:</strong><span>${e.id}</span></div>
          </div>
        `;
        document.getElementById('incidentEventId').value = e.id;
      } catch (e) {
        box.innerHTML = renderEmptyCard(e.message || 'No se pudo cargar la temporada');
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
        showMsg(data.message || 'Proyecto base creado');
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
        fillSelect('projectSelector', masterProjectsCache, 'Selecciona proyecto base', p => `${p.general_name || 'Sin nombre general'} | ${p.name}`);

        const list = document.getElementById('masterProjectsList');
        if (!masterProjectsCache.length) {
          list.innerHTML = renderEmptyCard('No hay proyectos base', 'Crea el primero para empezar a operar.');
          return;
        }

        list.innerHTML = masterProjectsCache.map(p => `
          <div class="record-card">
            <div class="record-card__head">
              <div>
                <div class="record-card__title">${escapeHTML(p.general_name || 'Sin nombre general')} | ${escapeHTML(p.name)}</div>
                <div class="record-card__sub">Project ID: ${p.id}</div>
              </div>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <span class="badge badge-purple">${escapeHTML(p.modality_name || '—')}</span>
                <span class="badge badge-neutral">${escapeHTML(p.week_days_name || '—')}</span>
                <span class="badge badge-neutral">${escapeHTML(p.schedule_name || '—')}</span>
              </div>
            </div>

            <div class="record-stack">
              <div class="stack-row"><strong>Carrera:</strong><span>${escapeHTML(p.partner_name || '—')}</span></div>
              <div class="stack-row"><strong>Horario:</strong><span>${escapeHTML(p.schedule_description || '—')}</span></div>
              <div class="stack-row"><strong>Duración:</strong><span>${escapeHTML(p.duration || '—')}</span></div>
              <div class="stack-row"><strong>Clave:</strong><span>${escapeHTML(p.clave || '—')}</span></div>
            </div>
          </div>
        `).join('');
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function addProjectToEvent() {
      const eventId = document.getElementById('eventProjectEventSelector').value;
      const projectId = document.getElementById('projectSelector').value;
      const slots = Number(document.getElementById('slotsInput').value);

      if (!eventId) return showMsg('Selecciona una temporada', false);
      if (!projectId) return showMsg('Selecciona un proyecto base', false);
      if (Number.isNaN(slots) || slots < 0) return showMsg('Slots inválidos', false);

      try {
        const data = await postJSON(`/api/admin/events/${eventId}/projects`, {
          project_id: Number(projectId),
          slots_total: slots
        });
        showMsg(data.message || 'Proyecto activado en temporada');
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
        container.innerHTML = renderEmptyCard('Selecciona una temporada', 'Después podrás ver y operar los proyectos activos.');
        return;
      }

      try {
        const data = await getJSONAuth(`/api/admin/events/${eventId}/projects`);
        eventProjectsCache = data || [];

        fillSelect('tokensEventProjectSelector', eventProjectsCache, 'Selecciona proyecto en temporada', p => `${p.name} · ${p.partner || '—'} · EventProject ${p.id}`);

        if (!eventProjectsCache.length) {
          container.innerHTML = renderEmptyCard('No hay proyectos activos', 'Activa un proyecto para esta temporada.');
          return;
        }

        container.innerHTML = eventProjectsCache.map(p => `
          <div class="record-card">
            <div class="record-card__head">
              <div>
                <div class="record-card__title">${escapeHTML(p.name)}</div>
                <div class="record-card__sub">Carrera preferida: ${escapeHTML(p.partner || '—')}</div>
              </div>
              <div>${statusBadge(p.status)}</div>
            </div>

            <div class="record-stack">
              <div class="stack-row"><strong>Project ID:</strong><span>${p.project_id}</span></div>
              <div class="stack-row"><strong>EventProject ID:</strong><span>${p.id}</span></div>
              <div class="stack-row"><strong>Slots:</strong><span>${p.slots_total}</span></div>
            </div>

            <div class="actions">
              <button type="button" class="btn-secondary" onclick="quickUpdateEventProject(${p.id}, ${p.slots_total}, 'ACTIVE')">Activar</button>
              <button type="button" class="btn-secondary" onclick="quickUpdateEventProject(${p.id}, ${p.slots_total}, 'HIDDEN')">Ocultar</button>
              <button type="button" class="btn-secondary" onclick="quickUpdateEventProject(${p.id}, ${p.slots_total}, 'CLOSED')">Cerrar</button>
            </div>
          </div>
        `).join('');
      } catch (e) {
        container.innerHTML = renderEmptyCard(e.message || 'No se pudo cargar proyectos activos');
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

        const data = await postJSON(`/api/admin/event-projects/${eventProjectId}/tokens`, { count, length });

        document.getElementById('tokensGenerationResult').innerHTML = `
          <div class="record-card">
            <div class="record-card__title">${escapeHTML(data.message || 'Tokens generados')}</div>
            <div class="record-card__sub">Creados: ${data.created || 0} · TTL: ${data.ttl_hours || '—'} horas</div>
            <div style="margin-top:12px;" class="mono">${(data.tokens || []).join(', ')}</div>
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
      const cards = document.getElementById('tokensCards');

      if (!eventProjectId) {
        cards.innerHTML = renderEmptyCard('Selecciona un proyecto', 'Después podrás ver el estado de sus tokens.');
        return;
      }

      try {
        const data = await getJSONAuth(`/api/admin/event-projects/${eventProjectId}/tokens?status=${encodeURIComponent(status)}`);
        const s = data.summary || {};

        document.getElementById('tokensSummary').innerHTML = `
          <div class="kpi-card kpi-card--orange">
            <div class="kpi-label">Available</div>
            <div class="kpi-value">${s.available || 0}</div>
            <div class="kpi-sub">Tokens libres</div>
          </div>
          <div class="kpi-card kpi-card--orange">
            <div class="kpi-label">Reserved</div>
            <div class="kpi-value">${s.reserved || 0}</div>
            <div class="kpi-sub">En espera</div>
          </div>
          <div class="kpi-card kpi-card--green">
            <div class="kpi-label">Used</div>
            <div class="kpi-value">${s.used || 0}</div>
            <div class="kpi-sub">Ya utilizados</div>
          </div>
          <div class="kpi-card kpi-card--pink">
            <div class="kpi-label">Revocados + Expirados</div>
            <div class="kpi-value">${(s.revoked || 0) + (s.expired || 0)}</div>
            <div class="kpi-sub">Fuera de circulación</div>
          </div>
        `;

        const items = data.items || [];
        cards.innerHTML = items.length
          ? items.map(t => `
              <div class="record-card">
                <div class="record-card__head">
                  <div>
                    <div class="record-card__title">Token</div>
                    <div class="record-card__sub"><span class="mono">${escapeHTML(t.token_value || '—')}</span></div>
                  </div>
                  <div>${statusBadge(t.status || '—')}</div>
                </div>

                <div class="record-stack">
                  <div class="stack-row"><strong>Reservado por:</strong><span>${escapeHTML(t.reserved_by_request_id || '—')}</span></div>
                  <div class="stack-row"><strong>Reserved until:</strong><span>${escapeHTML(t.reserved_until || '—')}</span></div>
                  <div class="stack-row"><strong>Usado por:</strong><span>${escapeHTML(t.used_by_request_id || '—')}</span></div>
                  <div class="stack-row"><strong>Usado:</strong><span>${escapeHTML(t.used_at || '—')}</span></div>
                  <div class="stack-row"><strong>Revocado:</strong><span>${escapeHTML(t.revoked_at || '—')}</span></div>
                  <div class="stack-row"><strong>Expira:</strong><span>${escapeHTML(t.expires_at || '—')}</span></div>
                </div>
              </div>
            `).join('')
          : renderEmptyCard('No hay tokens con ese filtro', 'Prueba otro estado o genera nuevos tokens.');
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
          <div class="kpi-card kpi-card--green">
            <div class="kpi-label">Total Inscritos</div>
            <div class="kpi-value">${summary.requests.registered || 0}</div>
            <div class="kpi-sub">Alumnos con cierre final</div>
          </div>
          <div class="kpi-card kpi-card--orange">
            <div class="kpi-label">Tokens Pendientes</div>
            <div class="kpi-value">${(summary.tokens?.available || 0) + (summary.tokens?.reserved || 0)}</div>
            <div class="kpi-sub">Disponibles o reservados</div>
          </div>
          <div class="kpi-card kpi-card--purple">
            <div class="kpi-label">Proyectos</div>
            <div class="kpi-value">${summary.projects?.total || (projects || []).length || 0}</div>
            <div class="kpi-sub">Activos en temporada</div>
          </div>
          <div class="kpi-card kpi-card--pink">
            <div class="kpi-label">Incidentes</div>
            <div class="kpi-value">${summary.incidents?.open || 0}</div>
            <div class="kpi-sub">Pendientes de resolver</div>
          </div>
        `;

        const body = document.getElementById('dashboardProjectsBody');
        const items = projects || [];

        body.innerHTML = items.length
          ? items.map(p => `
              <div class="record-card">
                <div class="record-card__head">
                  <div>
                    <div class="record-card__title">${escapeHTML(p.project_name)}</div>
                    <div class="record-card__sub">${escapeHTML(p.partner_name || 'Sin carrera preferida')}</div>
                  </div>
                  <div>${statusBadge(p.event_project_status)}</div>
                </div>

                <div class="record-stack">
                  <div class="stack-row"><strong>Slots:</strong><span>${p.slots_total}</span></div>
                  <div class="stack-row"><strong>Registrados:</strong><span>${p.registered_count}</span></div>
                  <div class="stack-row"><strong>Disponibles:</strong><span>${p.cupos_disponibles}</span></div>
                  <div class="stack-row"><strong>Tokens usados:</strong><span>${p.tokens_used}</span></div>
                  <div class="stack-row"><strong>Revocados:</strong><span>${p.tokens_revoked}</span></div>
                  <div class="stack-row"><strong>Expirados:</strong><span>${p.tokens_expired}</span></div>
                </div>

                <div style="margin-top:12px;">
                  ${renderXPBar(p.registered_count, p.slots_total)}
                </div>
              </div>
            `).join('')
          : renderEmptyCard('No hay proyectos cargados en esta temporada', 'Activa proyectos para empezar a operar.');
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function loadRegistrations() {
      const eventId = document.getElementById('registrationsEventSelector').value;
      const cards = document.getElementById('registrationsCards');

      if (!eventId) {
        cards.innerHTML = renderEmptyCard('Selecciona una temporada', 'Luego podrás consultar inscripciones cerradas.');
        return;
      }

      try {
        const rows = await getJSONAuth(`/api/admin/registrations?event_id=${encodeURIComponent(eventId)}`);

        if (!rows.length) {
          cards.innerHTML = renderEmptyCard('No hay inscripciones cerradas', 'Todavía no hay cierres en esta temporada.');
          return;
        }

        cards.innerHTML = rows.map(r => `
          <div class="record-card">
            <div class="record-card__head">
              <div>
                <div class="record-card__title">${escapeHTML(r.student_name || '—')}</div>
                <div class="record-card__sub"><span class="mono-soft">${escapeHTML(r.enrolment_number || '—')}</span></div>
              </div>
              <div>${statusBadge(r.registration_status || 'ACTIVE')}</div>
            </div>

            <div class="record-stack">
              <div class="stack-row"><strong>Proyecto:</strong><span>${escapeHTML(r.project_name || '—')}</span></div>
              <div class="stack-row"><strong>Organización:</strong><span>${escapeHTML(r.general_name || '—')}</span></div>
              <div class="stack-row"><strong>Token:</strong><span class="mono">${escapeHTML(r.token_value || '—')}</span></div>
              <div class="stack-row"><strong>Fecha cierre:</strong><span>${escapeHTML(r.accepted_at || '—')}</span></div>
            </div>
          </div>
        `).join('');

        showMsg('Inscripciones cerradas cargadas correctamente');
      } catch (e) {
        cards.innerHTML = renderEmptyCard(e.message || 'No se pudo cargar inscripciones');
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
          { fps: 10, qrbox: { width: 220, height: 220 } },
          async (decodedText) => {
            document.getElementById('staffScannedToken').value = decodedText;
            await scanStaffQr();
          },
          () => {}
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
          <div class="record-card">
            <div class="record-card__head">
              <div>
                <div class="record-card__title">${escapeHTML(data.student?.full_name || 'Alumno')}</div>
                <div class="record-card__sub">Matrícula registrada: ${escapeHTML(data.student?.enrolment_number || '—')}</div>
              </div>
              <div>${statusBadge(data.request?.status || 'REQUESTED')}</div>
            </div>

            <div class="record-stack">
              <div class="stack-row"><strong>Folio:</strong><span>${escapeHTML(data.request?.folio || '—')}</span></div>
              <div class="stack-row"><strong>Temporada:</strong><span>${escapeHTML(data.event?.display_name || '—')}</span></div>
              <div class="stack-row"><strong>QR expira:</strong><span>${escapeHTML(data.pass_session?.expires_at || '—')}</span></div>
              <div class="stack-row"><strong>Carrera:</strong><span>${escapeHTML(data.student?.degree || '—')}</span></div>
            </div>
          </div>
        `;

        showMsg('QR válido. Verifica ahora la matrícula física.');
      } catch (e) {
        lastScannedPassSession = null;
        document.getElementById('staffCheckinInfo').innerHTML = renderEmptyCard('QR inválido o no disponible', e.message || '');
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
          <div class="record-card">
            <div class="record-card__title">Acceso habilitado correctamente</div>
            <div class="record-card__sub">El alumno ya puede entrar al catálogo y cerrar inscripción.</div>
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
      const eventId =
        document.getElementById('eventSelector').value ||
        document.getElementById('dashboardEventSelector').value ||
        document.getElementById('eventProjectEventSelector').value;

      const list = document.getElementById('incidentsList');

      if (!eventId) {
        list.innerHTML = renderEmptyCard('Selecciona una temporada', 'Luego podrás consultar incidentes.');
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
          list.innerHTML = renderEmptyCard('No hay incidentes con esos filtros', 'Prueba otro estado o severidad.');
          return;
        }

        list.innerHTML = data.map(i => `
          <div class="record-card">
            <div class="record-card__head">
              <div>
                <div class="record-card__title">${escapeHTML(i.type)}</div>
                <div class="record-card__sub">Incident ID: ${i.id} · Request ID: ${i.request_id ?? '—'} · User ID: ${i.id_user ?? '—'}</div>
              </div>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                ${statusBadge(i.status)}
                <span class="${i.severity === 'HIGH' ? 'badge badge-danger' : i.severity === 'MEDIUM' ? 'badge badge-warn' : 'badge badge-success'}">${i.severity}</span>
              </div>
            </div>

            <div class="record-stack">
              <div class="stack-row"><strong>Descripción:</strong><span>${escapeHTML(i.description || 'Sin descripción')}</span></div>
              <div class="stack-row"><strong>Creado:</strong><span>${escapeHTML(i.created_at || '—')}</span></div>
              <div class="stack-row"><strong>Resuelto:</strong><span>${escapeHTML(i.resolved_at || '—')}</span></div>
            </div>

            <div class="actions">
              <button type="button" class="btn-secondary" onclick="updateIncidentStatus(${i.id}, 'IN_PROGRESS')">Marcar en proceso</button>
              <button type="button" class="btn-secondary" onclick="updateIncidentStatus(${i.id}, 'RESOLVED')">Resolver</button>
              <button type="button" class="btn-secondary" onclick="updateIncidentStatus(${i.id}, 'DISMISSED')">Descartar</button>
            </div>
          </div>
        `).join('');
      } catch (e) {
        list.innerHTML = renderEmptyCard(e.message || 'No se pudo cargar incidentes');
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

    async function markIncidentAsResolved(incidentId) {
      return updateIncidentStatus(incidentId, 'RESOLVED');
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
          <div class="record-card">
            <div class="record-card__title">${escapeHTML(data.message || 'Importación completada')}</div>
            <div class="record-card__sub">Insertados: ${data.inserted || 0} · Fallidos: ${data.failed || 0}</div>
          </div>
          ${(data.errors && data.errors.length)
            ? data.errors.map(e => `
              <div class="record-card">
                <div class="record-card__title">Fila ${e.row}</div>
                <div class="record-card__sub">${escapeHTML(e.error)}</div>
              </div>
            `).join('')
            : ''}
        `;

        showMsg(data.message || 'Importación completada');
        await loadMasterProjects();
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function exportProjects() {
      try {
        const r = await fetch('/api/admin/projects/export', {
          headers: { 'X-ADMIN-KEY': getKey() }
        });

        if (!r.ok) {
          const data = await r.json().catch(() => ({}));
          throw new Error(data.error || ('Error ' + r.status));
        }

        const blob = await r.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'projects_export.xlsx';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

        showMsg('Exportación iniciada correctamente');
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

      document.getElementById('registrationsEventSelector').addEventListener('change', async () => {
        await loadRegistrations();
      });
    });
  </script>
</body>
</html>
"""