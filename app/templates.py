INDEX_HTML = r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Registro de Proyectos</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
  <style>
    :root {
      --bg: #eef3fb;
      --bg-2: #f8fbff;

      --panel: #ffffff;
      --panel-soft: #f6f9ff;

      --text: #1b2435;
      --text-soft: #607089;
      --muted: #93a1b7;

      --line: #dbe4f2;
      --line-strong: #c7d4e8;

      --brand: #4f7cff;
      --brand-2: #72a7ff;
      --accent: #ff5d73;

      --ok-bg: #dcfce7;
      --ok-text: #166534;

      --warn-bg: #fef3c7;
      --warn-text: #92400e;

      --err-bg: #fee2e2;
      --err-text: #991b1b;

      --purple-bg: #ede9fe;
      --purple-text: #6d28d9;

      --shadow-sm: 0 2px 6px rgba(15, 23, 42, 0.05);
      --shadow-md: 0 14px 28px rgba(35, 60, 120, 0.10);

      --r-sm: 10px;
      --r-md: 14px;
      --r-lg: 18px;
      --r-xl: 24px;
      --r-pill: 999px;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, #ffffff 0%, #eef4ff 28%, #eaf1fb 100%);
      min-height: 100vh;
    }

    header {
      position: sticky;
      top: 0;
      z-index: 40;
      background: rgba(255,255,255,0.86);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--line);
    }

    .header-shell {
      max-width: 1440px;
      margin: 0 auto;
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .brand-copy {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .brand-copy strong {
      font-size: 1.12rem;
      font-weight: 900;
      color: var(--text);
    }

    .brand-copy span {
      font-size: .92rem;
      color: var(--text-soft);
    }

    .top-links {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .top-links a {
      text-decoration: none;
      border: 1px solid var(--line);
      background: white;
      color: var(--text-soft);
      padding: 10px 12px;
      border-radius: var(--r-md);
      font-size: .9rem;
      font-weight: 800;
      box-shadow: var(--shadow-sm);
    }

    .top-links a:hover {
      border-color: var(--brand);
      color: var(--brand);
    }

    .container {
      max-width: 1440px;
      margin: 24px auto;
      padding: 0 18px 32px;
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

    .hero {
      position: relative;
      overflow: hidden;
      background: linear-gradient(135deg, #ffffff 0%, #f5f9ff 100%);
      border: 1px solid var(--line);
      border-radius: var(--r-xl);
      padding: 22px;
      box-shadow: var(--shadow-md);
      margin-bottom: 18px;
    }

    .hero::before {
      content: "";
      position: absolute;
      right: -40px;
      top: -40px;
      width: 180px;
      height: 180px;
      border-radius: 999px;
      background: radial-gradient(circle, rgba(79,124,255,0.18) 0%, rgba(79,124,255,0.00) 72%);
      pointer-events: none;
    }

    .hero-content {
      position: relative;
      z-index: 1;
      display: flex;
      justify-content: space-between;
      gap: 18px;
      flex-wrap: wrap;
      align-items: center;
    }

    .hero-copy {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .hero-kicker {
      font-size: .76rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--muted);
      font-weight: 900;
    }

    .hero-copy strong {
      font-size: 1.4rem;
      font-weight: 900;
    }

    .hero-copy span {
      color: var(--text-soft);
      max-width: 760px;
      line-height: 1.5;
    }

    .hero-badges {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
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
    }

    .chip-primary {
      background: #eff6ff;
      color: var(--brand);
      border: 1px solid #d8e5ff;
    }

    .chip-dark {
      background: #1f2a44;
      color: #eaf1ff;
      border: 1px solid rgba(255,255,255,0.08);
    }

    .steps {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 18px;
    }

    .step-card {
      border: 1px solid var(--line);
      background: white;
      border-radius: var(--r-lg);
      padding: 14px;
      box-shadow: var(--shadow-sm);
      position: relative;
      overflow: hidden;
    }

    .step-card.active {
      border-color: #cfe0ff;
      background: linear-gradient(135deg, #eef4ff 0%, #ffffff 100%);
    }

    .step-card.done {
      border-color: #bbf7d0;
      background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
    }

    .step-index {
      font-size: .74rem;
      text-transform: uppercase;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 6px;
      letter-spacing: .05em;
    }

    .step-title {
      font-size: .95rem;
      font-weight: 900;
      margin-bottom: 4px;
    }

    .step-desc {
      font-size: .83rem;
      color: var(--text-soft);
      line-height: 1.4;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 18px;
    }

    .card {
      background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
      border: 1px solid var(--line);
      border-radius: var(--r-xl);
      box-shadow: var(--shadow-md);
      padding: 22px;
      position: relative;
      overflow: hidden;
    }

    .card::after {
      content: "";
      position: absolute;
      top: 0;
      right: 0;
      width: 78px;
      height: 78px;
      background: linear-gradient(135deg, rgba(79,124,255,0.10) 0%, rgba(79,124,255,0.00) 72%);
      clip-path: polygon(100% 0, 0 0, 100% 100%);
      pointer-events: none;
    }

    .span-12 { grid-column: span 12; }
    .span-8 { grid-column: span 8; }
    .span-6 { grid-column: span 6; }
    .span-4 { grid-column: span 4; }

    .module-card-title {
      position: relative;
      z-index: 1;
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

    .screen-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 12px;
      border-radius: var(--r-pill);
      background: #eff6ff;
      color: var(--brand);
      font-size: .82rem;
      font-weight: 900;
    }

    .muted {
      position: relative;
      z-index: 1;
      color: var(--text-soft);
      font-size: .93rem;
      line-height: 1.55;
    }

    .small {
      font-size: .84rem;
      color: var(--text-soft);
    }

    .form-grid {
      position: relative;
      z-index: 1;
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
      transition: .18s ease;
    }

    textarea {
      min-height: 100px;
      resize: vertical;
    }

    input:focus, select:focus, textarea:focus {
      border-color: var(--brand-2);
      box-shadow: 0 0 0 3px rgba(79,124,255,0.10);
    }

    .actions {
      position: relative;
      z-index: 1;
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 16px;
    }

    .actions > button {
      width: auto;
      min-width: 150px;
    }

    .btn-primary, .btn-secondary, .btn-danger {
      min-height: 44px;
      border-radius: var(--r-md);
      padding: 10px 14px;
      font-size: .94rem;
      font-weight: 900;
      cursor: pointer;
      transition: transform .15s ease, box-shadow .15s ease;
    }

    .btn-primary:hover, .btn-secondary:hover, .btn-danger:hover {
      transform: translateY(-1px);
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--accent) 0%, #ff7b8d 100%);
      color: white;
      border: none;
      box-shadow: 0 10px 18px rgba(230,57,70,0.18);
    }

    .btn-secondary {
      background: #f8fafc;
      color: #334155;
      border: 1px solid var(--line);
    }

    .btn-danger {
      background: #ef4444;
      color: white;
      border: none;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 11px;
      border-radius: var(--r-pill);
      font-size: .76rem;
      font-weight: 900;
      white-space: nowrap;
    }

    .pill-ok { background: var(--ok-bg); color: var(--ok-text); }
    .pill-err { background: var(--err-bg); color: var(--err-text); }
    .pill-warn { background: var(--warn-bg); color: var(--warn-text); }
    .pill-info { background: #eff6ff; color: var(--brand-2); }
    .pill-purple { background: var(--purple-bg); color: var(--purple-text); }
    .pill-neutral { background: #f1f5f9; color: #334155; }

    .list {
      position: relative;
      z-index: 1;
      display: grid;
      gap: 12px;
      margin-top: 14px;
    }

    .item {
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      background: #fff;
      padding: 16px;
      box-shadow: var(--shadow-sm);
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
      font-weight: 900;
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

    .project-grid {
      position: relative;
      z-index: 1;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 16px;
      margin-top: 16px;
    }

    .tcg-card {
      position: relative;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
      box-shadow: var(--shadow-md);
      padding: 16px;
      transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    .tcg-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 18px 34px rgba(35, 60, 120, 0.12);
      border-color: #cfe0ff;
    }

    .tcg-card.selected {
      border-color: #ffb7c0;
      box-shadow: 0 0 0 3px rgba(255,93,115,0.12), 0 18px 34px rgba(35, 60, 120, 0.12);
    }

    .tcg-card::before {
      content: "";
      position: absolute;
      inset: 0;
      background:
        radial-gradient(circle at top right, rgba(79,124,255,0.12) 0%, rgba(79,124,255,0) 30%),
        radial-gradient(circle at bottom left, rgba(255,93,115,0.10) 0%, rgba(255,93,115,0) 28%);
      pointer-events: none;
    }

    .tcg-card__content {
      position: relative;
      z-index: 1;
    }

    .tcg-top {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      margin-bottom: 12px;
    }

    .tcg-kicker {
      font-size: .74rem;
      text-transform: uppercase;
      letter-spacing: .05em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 4px;
    }

    .tcg-title {
      font-size: 1rem;
      font-weight: 900;
      line-height: 1.25;
      margin-bottom: 2px;
    }

    .tcg-subtitle {
      color: var(--text-soft);
      font-size: .86rem;
      line-height: 1.4;
    }

    .tcg-rank {
      min-width: 54px;
      text-align: center;
      border-radius: 16px;
      padding: 10px 8px;
      background: linear-gradient(180deg, #eff6ff 0%, #ffffff 100%);
      border: 1px solid #dbe7ff;
      font-size: .74rem;
      font-weight: 900;
      color: var(--brand);
    }

    .tcg-hero {
      border: 1px solid #e7eef9;
      background: linear-gradient(135deg, #f5f9ff 0%, #eef4ff 50%, #fff5f7 100%);
      border-radius: 18px;
      min-height: 120px;
      padding: 14px;
      display: flex;
      align-items: flex-end;
      margin-bottom: 12px;
    }

    .tcg-hero-text {
      font-size: .9rem;
      color: #34445f;
      line-height: 1.45;
      font-weight: 700;
    }

    .tcg-stats {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      margin-bottom: 12px;
    }

    .tcg-stat {
      border: 1px solid #eef2f7;
      background: #f8fafc;
      border-radius: 14px;
      padding: 10px 12px;
    }

    .tcg-stat-label {
      display: block;
      font-size: .7rem;
      text-transform: uppercase;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 4px;
      letter-spacing: .04em;
    }

    .tcg-stat-value {
      font-size: .88rem;
      font-weight: 800;
      color: var(--text);
      line-height: 1.35;
    }

    .tcg-extra {
      display: grid;
      gap: 8px;
      margin-bottom: 12px;
    }

    .tcg-extra-row {
      font-size: .85rem;
      color: var(--text-soft);
      line-height: 1.45;
    }

    .tcg-extra-row strong {
      color: var(--text);
    }

    .tcg-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .selection-banner {
      position: relative;
      z-index: 1;
      border: 1px dashed #ffb7c0;
      background: linear-gradient(135deg, #fff7f8 0%, #ffffff 100%);
      border-radius: 16px;
      padding: 14px 16px;
      margin-top: 12px;
    }

    .selection-title {
      font-size: .9rem;
      font-weight: 900;
      margin-bottom: 4px;
      color: #b42339;
    }

    .qr-shell {
      position: relative;
      z-index: 1;
      border: 1px solid var(--line);
      background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
      border-radius: 20px;
      padding: 18px;
      display: grid;
      gap: 14px;
    }

    .qr-status-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .qr-canvas-wrap {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 220px;
      border: 1px dashed #d6e4ff;
      border-radius: 18px;
      background: #fcfdff;
    }

    .mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: .92rem;
      background: #16233c;
      color: #e8eef8;
      border-radius: var(--r-md);
      padding: 10px 12px;
      word-break: break-all;
    }

    .preview-box {
      position: relative;
      z-index: 1;
      border: 1px solid #dbeafe;
      border-radius: var(--r-lg);
      background: #f8fbff;
      padding: 16px;
      margin-top: 12px;
    }

    .success-card {
      border: 1px solid #bbf7d0;
      background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
      border-radius: 18px;
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .success-title {
      font-size: 1rem;
      font-weight: 900;
      color: var(--ok-text);
      margin-bottom: 8px;
    }

    .table-wrap {
      overflow-x: auto;
    }

    @media (max-width: 1200px) {
      .steps {
        grid-template-columns: repeat(2, 1fr);
      }

      .span-8, .span-6, .span-4 {
        grid-column: span 12;
      }
    }

    @media (max-width: 768px) {
      .steps {
        grid-template-columns: 1fr;
      }

      .hero-content {
        flex-direction: column;
        align-items: start;
      }
    }

    @media (max-width: 640px) {
      .container {
        padding: 0 14px 28px;
      }

      .actions {
        flex-direction: column;
        align-items: stretch;
      }

      .actions > button {
        width: 100%;
      }

      .tcg-stats {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <header>
    <div class="header-shell">
      <div class="brand-copy">
        <strong>Registro de Proyectos</strong>
        <span>Explora proyectos, solicita tu pase y cierra tu inscripción.</span>
      </div>

      <div class="top-links">
        <a href="/admin">Admin</a>
        <a href="/health">Health</a>
      </div>
    </div>
  </header>

  <div class="container">
    <div id="msg" class="msg"></div>

    <div class="hero">
      <div class="hero-content">
        <div class="hero-copy">
          <div class="hero-kicker">Ruta del alumno</div>
          <strong>Explora, solicita, valida y registra</strong>
          <span>
            Primero explora el catálogo. Después solicita tu pase. Cuando el staff valide tu acceso, ya podrás cerrar tu inscripción con el token del proyecto.
          </span>
        </div>

        <div class="hero-badges">
          <span class="chip chip-primary">Catálogo vivo</span>
          <span class="chip chip-dark">Registro guiado</span>
        </div>
      </div>
    </div>

    <div class="steps" id="stepsBar">
      <div class="step-card active" data-step="1">
        <div class="step-index">Paso 1</div>
        <div class="step-title">Explorar</div>
        <div class="step-desc">Revisa proyectos y elige el que más te convenga.</div>
      </div>

      <div class="step-card" data-step="2">
        <div class="step-index">Paso 2</div>
        <div class="step-title">Solicitud</div>
        <div class="step-desc">Genera tu folio y deja tus datos completos.</div>
      </div>

      <div class="step-card" data-step="3">
        <div class="step-index">Paso 3</div>
        <div class="step-title">QR</div>
        <div class="step-desc">Muestra tu credencial viva al staff para habilitar acceso.</div>
      </div>

      <div class="step-card" data-step="4">
        <div class="step-index">Paso 4</div>
        <div class="step-title">Registro</div>
        <div class="step-desc">Cierra tu inscripción con el token del proyecto.</div>
      </div>
    </div>

    <div class="grid">
      <div class="card span-12">
        <div class="module-card-title">
          <h2>Catálogo de proyectos</h2>
          <span class="screen-chip">Tarjetas activas</span>
        </div>
        <div class="muted">
          Selecciona primero la temporada y revisa el catálogo disponible antes de solicitar tu pase.
        </div>

        <div class="form-grid">
          <div class="field">
            <label>Temporada</label>
            <select id="seasonSelector">
              <option value="PRIMAVERA">Primavera</option>
              <option value="INVIERNO">Invierno</option>
            </select>
          </div>

          <div class="field">
            <label>Buscar proyecto</label>
            <input id="catalogSearch" placeholder="Nombre, comentarios, descripción, responsables">
          </div>

          <div class="field">
            <label>Carrera preferida</label>
            <select id="filterPartner">
              <option value="">Todas</option>
            </select>
          </div>

          <div class="field">
            <label>Modalidad</label>
            <select id="filterModality">
              <option value="">Todas</option>
            </select>
          </div>

          <div class="field">
            <label>Días</label>
            <select id="filterWeekDays">
              <option value="">Todos</option>
            </select>
          </div>

          <div class="field">
            <label>Horario</label>
            <select id="filterSchedule">
              <option value="">Todos</option>
            </select>
          </div>
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="loadCatalog()">Cargar catálogo</button>
          <button type="button" class="btn-secondary" onclick="resetCatalogFilters()">Limpiar filtros</button>
        </div>

        <div id="catalogHeader" class="list"></div>

        <div id="selectedProjectBanner" class="selection-banner hidden">
          <div class="selection-title">Proyecto seleccionado</div>
          <div id="selectedProjectBannerText" class="small">Aún no seleccionas proyecto.</div>
        </div>

        <div id="catalogList" class="project-grid"></div>
      </div>

      <div class="card span-6">
        <div class="module-card-title">
          <h2>Solicitar pase</h2>
          <span class="screen-chip">Paso 2</span>
        </div>
        <div class="muted">
          El pase no te registra todavía. Solo genera tu solicitud y tu folio para avanzar a validación presencial.
        </div>

        <div class="form-grid">
          <div class="field">
            <label>Nombre completo</label>
            <input id="fullNameInput" placeholder="Nombre completo">
          </div>

          <div class="field">
            <label>Matrícula</label>
            <input id="enrolmentInput" placeholder="Ej: A01234567">
          </div>

          <div class="field">
            <label>Correo principal</label>
            <input id="emailInput" type="email" placeholder="correo@ejemplo.com">
          </div>

          <div class="field">
            <label>Segundo correo</label>
            <input id="secondEmailInput" type="email" placeholder="opcional">
          </div>

          <div class="field">
            <label>Teléfono</label>
            <input id="phoneInput" placeholder="10 dígitos o similar">
          </div>

          <div class="field">
            <label>Carrera</label>
            <input id="degreeInput" placeholder="Ej: LAF, LAE, NEG">
          </div>

          <div class="field">
            <label>Semestre</label>
            <input id="semesterInput" type="number" min="1" max="20" placeholder="Ej: 5">
          </div>
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="createStudentRequest()">Solicitar pase</button>
          <button type="button" class="btn-secondary" onclick="loadStudentRequest()">Consultar mi solicitud</button>
        </div>
      </div>

      <div class="card span-6">
        <div class="module-card-title">
          <h2>Mi solicitud</h2>
          <span class="screen-chip">Folio</span>
        </div>
        <div class="muted">
          Aquí puedes consultar tu folio y el estado actual de tu solicitud para la temporada elegida.
        </div>

        <div id="requestInfo" class="list">
          <div class="item">
            <div class="small">Todavía no hay información cargada.</div>
          </div>
        </div>
      </div>

      <div class="card span-6">
        <div class="module-card-title">
          <h2>Credencial viva</h2>
          <span class="screen-chip">Paso 3</span>
        </div>
        <div class="muted">
          Refresca tu credencial cuando el staff te lo pida. El QR cambia y el anterior deja de servir.
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="refreshStudentPass()">Refrescar credencial</button>
          <button type="button" class="btn-secondary" onclick="loadStudentPass()">Consultar estado del pase</button>
        </div>

        <div id="passInfo" class="list">
          <div class="item">
            <div class="small">Todavía no hay información del pase.</div>
          </div>
        </div>

        <div class="qr-shell">
          <div class="qr-status-row">
            <div>
              <div class="item-title">QR vigente del pase</div>
              <div class="small">Este código cambia al refrescarse y deja de servir al expirar o cuando el staff lo usa.</div>
            </div>
            <div id="qrStatusBadge" class="pill pill-neutral">Sin sesión</div>
          </div>

          <div class="qr-canvas-wrap">
            <div id="qrCanvas"></div>
          </div>

          <div id="qrPlainToken" class="mono">Genera tu código</div>
        </div>
      </div>

      <div class="card span-6">
        <div class="module-card-title">
          <h2>Cierre de inscripción</h2>
          <span class="screen-chip">Paso 4</span>
        </div>
        <div class="muted">
          Cuando el staff ya te haya habilitado acceso y tengas el token del proyecto, haz preview y luego confirma.
        </div>

        <div class="form-grid">
          <div class="field">
            <label>Proyecto seleccionado</label>
            <input id="selectedProjectName" placeholder="Elige un proyecto del catálogo" readonly>
          </div>

          <div class="field">
            <label>ID del proyecto</label>
            <input id="selectedProjectId" placeholder="Se llena al elegir un proyecto" readonly>
          </div>

          <div class="field">
            <label>Token del proyecto</label>
            <input id="projectTokenInput" placeholder="Token que te entrega el proyecto">
          </div>

          <div class="field">
            <label>Nombre completo para aceptación</label>
            <input id="acceptanceFullNameInput" placeholder="Debe coincidir con tu nombre">
          </div>

          <div class="field">
            <label>Versión legal</label>
            <input id="legalVersionInput" value="v1">
          </div>
        </div>

        <div class="preview-box">
          <div class="small" style="margin-bottom:8px;"><strong>Confirmación legal</strong></div>
          <label style="display:flex; gap:10px; align-items:flex-start; font-size:.92rem; color:var(--text);">
            <input id="acceptanceCheckbox" type="checkbox" style="width:auto; min-height:auto; margin-top:3px;">
            <span>
              Confirmo que realicé esta inscripción de manera personal, que acepto el proyecto y que entiendo que el cierre queda auditado con token y registro digital.
            </span>
          </label>
        </div>

        <div class="actions">
          <button type="button" class="btn-secondary" onclick="previewRegistration()">Ver preview</button>
          <button type="button" class="btn-primary" id="confirmRegistrationBtn" onclick="confirmRegistration()">Confirmar inscripción</button>
        </div>

        <div id="registrationPreview" class="list">
          <div class="item">
            <div class="small">Todavía no hay preview del cierre.</div>
          </div>
        </div>

        <div id="registrationSuccessBox" class="list hidden"></div>
      </div>
    </div>
  </div>

  <script>
    let currentCatalog = [];
    let currentRequest = null;
    let currentPass = null;
    let currentPreview = null;
    let currentSelectedProject = null;
    let currentRegistration = null;

    function escapeHTML(value) {
      return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function debounce(fn, delay) {
      let timeout;
      return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), delay);
      };
    }

    function showMsg(text, ok = true) {
      const el = document.getElementById('msg');
      el.textContent = text || '';
      el.className = 'msg ' + (ok ? 'ok' : 'err');
    }

    function getSeason() {
      return document.getElementById('seasonSelector').value;
    }

    function getEnrolment() {
      return (document.getElementById('enrolmentInput').value || '').trim().toLowerCase();
    }

    async function getJSON(url) {
      const r = await fetch(url);
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
      return data;
    }

    async function postJSON(url, body) {
      const r = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
      return data;
    }

    function fillSelect(id, items, labelKey = 'description') {
      const el = document.getElementById(id);
      if (!el) return;

      const firstOption = el.querySelector('option') ? el.querySelector('option').outerHTML : '<option value="">Todos</option>';
      el.innerHTML = firstOption;

      for (const item of items || []) {
        const opt = document.createElement('option');
        opt.value = item.id;
        opt.textContent = item[labelKey];
        el.appendChild(opt);
      }
    }

    function setCurrentStep(step) {
      document.querySelectorAll('.step-card').forEach(el => {
        const stepNum = Number(el.getAttribute('data-step'));
        el.classList.remove('active', 'done');

        if (stepNum < step) {
          el.classList.add('done');
        } else if (stepNum === step) {
          el.classList.add('active');
        }
      });
    }

    function renderCatalogHeader(projects, eventInfo = null) {
      const season = eventInfo?.season || getSeason();
      const displayName = eventInfo?.display_name || season;
      const el = document.getElementById('catalogHeader');

      el.innerHTML = `
        <div class="item">
          <div class="item-head">
            <div>
              <div class="item-title">Catálogo de ${escapeHTML(displayName)}</div>
              <div class="small">Total de proyectos mostrados: ${projects.length}</div>
            </div>
            <div>
              <span class="pill pill-info">${escapeHTML(season)}</span>
            </div>
          </div>
        </div>
      `;
    }

    function renderCatalog(projects) {
      const list = document.getElementById('catalogList');

      if (!projects || !projects.length) {
        list.innerHTML = `
          <div class="item">
            <div class="small">No hay proyectos para mostrar con esos filtros o no hay proyectos activos en esta temporada.</div>
          </div>
        `;
        return;
      }

      list.innerHTML = projects.map((p, idx) => `
        <div class="tcg-card ${currentSelectedProject && Number(currentSelectedProject.id) === Number(p.id) ? 'selected' : ''}">
          <div class="tcg-card__content">
            <div class="tcg-top">
              <div>
                <div class="tcg-kicker">${escapeHTML(p.general_name || 'Proyecto')}</div>
                <div class="tcg-title">${escapeHTML(p.name || 'Sin nombre')}</div>
                <div class="tcg-subtitle">Carrera preferida: ${escapeHTML(p.socio || 'Sin preferencia')}</div>
              </div>

              <div class="tcg-rank">
                CARD<br>#${idx + 1}
              </div>
            </div>

            <div class="tcg-hero">
              <div class="tcg-hero-text">
                ${escapeHTML((p.objectives || p.comments || 'Proyecto activo para esta temporada.').slice(0, 140))}
              </div>
            </div>

            <div class="tcg-stats">
              <div class="tcg-stat">
                <span class="tcg-stat-label">Modalidad</span>
                <div class="tcg-stat-value">${escapeHTML(p.modalidad || '—')}</div>
              </div>

              <div class="tcg-stat">
                <span class="tcg-stat-label">Días</span>
                <div class="tcg-stat-value">${escapeHTML(p.dia || '—')}</div>
              </div>

              <div class="tcg-stat">
                <span class="tcg-stat-label">Horario</span>
                <div class="tcg-stat-value">${escapeHTML(p.horario || '—')}</div>
              </div>

              <div class="tcg-stat">
                <span class="tcg-stat-label">Cupos</span>
                <div class="tcg-stat-value">${escapeHTML(p.cupos_disponibles ?? p.cupos ?? '—')}</div>
              </div>
            </div>

            <div class="tcg-extra">
              <div class="tcg-extra-row"><strong>Duración:</strong> ${escapeHTML(p.duration || '—')}</div>
              <div class="tcg-extra-row"><strong>Lugar:</strong> ${escapeHTML(p.location || '—')}</div>
              <div class="tcg-extra-row"><strong>Competencias:</strong> ${escapeHTML(p.competencies || '—')}</div>
            </div>

            <div class="tcg-actions">
              <button type="button" class="btn-primary" onclick="selectProject(${Number(p.id)})">Elegir proyecto</button>
            </div>
          </div>
        </div>
      `).join('');
    }

    function renderSkeleton() {
      const list = document.getElementById('catalogList');

      list.innerHTML = Array(6).fill(`
        <div class="tcg-card">
          <div class="tcg-card__content">
            <div style="height:16px;width:60%;background:#eef2f7;border-radius:6px;margin-bottom:8px;"></div>
            <div style="height:12px;width:40%;background:#eef2f7;border-radius:6px;margin-bottom:12px;"></div>
            <div style="height:100px;background:#eef2f7;border-radius:12px;margin-bottom:12px;"></div>
            <div style="height:12px;width:80%;background:#eef2f7;border-radius:6px;margin-bottom:6px;"></div>
            <div style="height:12px;width:70%;background:#eef2f7;border-radius:6px;"></div>
          </div>
        </div>
      `).join('');
    }


    function renderSelectedProjectBanner() {
      const banner = document.getElementById('selectedProjectBanner');
      const text = document.getElementById('selectedProjectBannerText');

      if (!currentSelectedProject) {
        banner.classList.add('hidden');
        text.textContent = 'Aún no seleccionas proyecto.';
        return;
      }

      banner.classList.remove('hidden');
      text.innerHTML = `
        <strong>${escapeHTML(currentSelectedProject.general_name || 'Proyecto')}</strong> |
        ${escapeHTML(currentSelectedProject.name || 'Sin nombre')}
        · ${escapeHTML(currentSelectedProject.modalidad || '—')}
        · ${escapeHTML(currentSelectedProject.horario || '—')}
      `;
    }

    function selectProject(projectId) {
      const project = currentCatalog.find(p => Number(p.id) === Number(projectId));
      if (!project) return;

      currentSelectedProject = project;

      document.getElementById('selectedProjectId').value = String(project.id);
      document.getElementById('selectedProjectName').value = `${project.general_name || 'Sin nombre general'} | ${project.name || 'Sin nombre'}`;

      renderCatalog(currentCatalog);
      renderSelectedProjectBanner();
      setCurrentStep(2);
      showMsg('Proyecto seleccionado para el cierre de inscripción');
    }

    function resetCatalogFilters() {
      document.getElementById('catalogSearch').value = '';
      document.getElementById('filterPartner').value = '';
      document.getElementById('filterModality').value = '';
      document.getElementById('filterWeekDays').value = '';
      document.getElementById('filterSchedule').value = '';
      loadCatalog();
    }

    async function loadCatalogsForSeason() {
      try {
        const season = getSeason();
        const data = await getJSON(`/api/catalogs?temporada=${encodeURIComponent(season)}`);

        fillSelect('filterPartner', data.socio || [], 'name');
        fillSelect('filterModality', data.modalidad || [], 'description');
        fillSelect('filterWeekDays', data.dias || [], 'description');
        fillSelect('filterSchedule', data.horario || [], 'description');
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    let lastRequestId = 0;

    async function loadCatalog() {
      const requestId = ++lastRequestId;

      try {
        renderSkeleton();

        // ⚡ pequeño delay para UX más suave (opcional pero pro)
        await new Promise(r => setTimeout(r, 200));

        const season = getSeason();
        const q = (document.getElementById('catalogSearch').value || '').trim();
        const socio = document.getElementById('filterPartner').value;
        const modalidad = document.getElementById('filterModality').value;
        const dia = document.getElementById('filterWeekDays').value;
        const horario = document.getElementById('filterSchedule').value;

        const params = new URLSearchParams();
        params.set('temporada', season);
        if (q) params.set('q', q);
        if (socio) params.set('socio', socio);
        if (modalidad) params.set('modalidad', modalidad);
        if (dia) params.set('dia', dia);
        if (horario) params.set('horario', horario);

        const data = await getJSON(`/api/projects?${params.toString()}`);

        // 🚫 Evita respuestas viejas (race condition fix)
        if (requestId !== lastRequestId) return;

        currentCatalog = data.items || [];

        renderCatalogHeader(currentCatalog, data.event || null);
        renderCatalog(currentCatalog);
        renderSelectedProjectBanner();

        showMsg('Catálogo cargado correctamente');

      } catch (e) {
        // 🚫 Evita errores de requests viejos
        if (requestId !== lastRequestId) return;

        currentCatalog = [];
        renderCatalogHeader([], null);

        // 💀 Error específico de temporada
        if (e.message && e.message.toLowerCase().includes('temporada')) {
          document.getElementById('catalogList').innerHTML = `
            <div class="item" style="border-color:#fecaca;background:#fee2e2;">
              <div class="item-title" style="color:#991b1b;">
                No hay proyectos disponibles
              <div>
              <div class="small" style="color:#7f1d1d;">
                Aún no se ha habilitado una temporada para estudiantes.
              <div>
            </div>
          `;
          return;
        }

        renderCatalog([]);
        showMsg(e.message, false);
      }
    }


    function renderRequestStatus(status) {
      const value = String(status || '').toUpperCase();
      const map = {
        REQUESTED: ['pill pill-info', 'REQUESTED'],
        VALIDATED: ['pill pill-purple', 'VALIDATED'],
        ACCESS_ENABLED: ['pill pill-ok', 'ACCESS_ENABLED'],
        REGISTERED: ['pill pill-ok', 'REGISTERED'],
        CANCELLED: ['pill pill-err', 'CANCELLED'],
        CLOSED: ['pill pill-warn', 'CLOSED']
      };
      const cfg = map[value] || ['pill pill-neutral', value || '—'];
      return `<span class="${cfg[0]}">${cfg[1]}</span>`;
    }

    function renderRequestInfo(data) {
      const box = document.getElementById('requestInfo');

      if (!data) {
        box.innerHTML = `
          <div class="item"><div class="small">Todavía no hay información cargada.</div></div>
        `;
        return;
      }

      const request = data.request || data;
      const event = data.event || {};
      const user = data.user || {
        email: data.email,
        secondary_email: data.secondary_email,
        phone_number: data.phone_number,
        enrolment_number: data.enrolment_number,
        degree: data.degree,
        semester: data.semester
      };

      box.innerHTML = `
        <div class="item">
          <div class="item-head">
            <div>
              <div class="item-title">Folio ${escapeHTML(request.folio || '—')}</div>
              <div class="small">Estado actual de tu solicitud</div>
            </div>
            <div>${renderRequestStatus(request.status)}</div>
          </div>

          <div class="meta">
            <div class="meta-box">
              <span class="meta-label">Temporada</span>
              <div class="meta-value">${escapeHTML(event.display_name || getSeason())}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Correo principal</span>
              <div class="meta-value">${escapeHTML(user.email || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Segundo correo</span>
              <div class="meta-value">${escapeHTML(user.second_email || user.secondary_email || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Matrícula</span>
              <div class="meta-value">${escapeHTML(user.enrolment_number || getEnrolment() || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Carrera</span>
              <div class="meta-value">${escapeHTML(user.degree || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Semestre</span>
              <div class="meta-value">${escapeHTML(user.semester || '—')}</div>
            </div>
          </div>
        </div>
      `;
    }

    async function createStudentRequest() {
      try {
        const payload = {
          full_name: document.getElementById('fullNameInput').value.trim(),
          enrolment_number: document.getElementById('enrolmentInput').value.trim(),
          email: document.getElementById('emailInput').value.trim(),
          second_email: document.getElementById('secondEmailInput').value.trim(),
          phone_number: document.getElementById('phoneInput').value.trim(),
          degree: document.getElementById('degreeInput').value.trim(),
          semester: document.getElementById('semesterInput').value.trim(),
          season: getSeason()
        };

        const data = await postJSON('/api/student/requests', payload);
        currentRequest = data;
        renderRequestInfo(data);
        setCurrentStep(3);
        showMsg(data.message || 'Solicitud procesada correctamente');
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    async function loadStudentRequest() {
      try {
        const enrolment = getEnrolment();
        if (!enrolment) return showMsg('Primero escribe tu matrícula', false);

        const season = getSeason();
        const data = await getJSON(`/api/student/requests?enrolment_number=${encodeURIComponent(enrolment)}&season=${encodeURIComponent(season)}`);
        currentRequest = data;
        renderRequestInfo(data);
        showMsg('Solicitud cargada correctamente');
      } catch (e) {
        currentRequest = null;
        renderRequestInfo(null);
        showMsg(e.message, false);
      }
    }

    function renderStudentQR(plainToken) {
      const qrCanvas = document.getElementById('qrCanvas');
      const qrPlainToken = document.getElementById('qrPlainToken');

      qrCanvas.innerHTML = '';
      qrPlainToken.textContent = plainToken || 'Sin código';

      if (!plainToken) return;

      new QRCode(qrCanvas, {
        text: plainToken,
        width: 180,
        height: 180,
        correctLevel: QRCode.CorrectLevel.M
      });
    }

    function renderPassInfo(data) {
      const box = document.getElementById('passInfo');
      const statusBadge = document.getElementById('qrStatusBadge');

      if (!data) {
        box.innerHTML = `<div class="item"><div class="small">Todavía no hay información del pase.</div></div>`;
        statusBadge.className = 'pill pill-neutral';
        statusBadge.textContent = 'Sin sesión';
        renderStudentQR('');
        return;
      }

      const request = data.request || {};
      const event = data.event || {};
      const student = data.student || {};
      const session = data.pass_session || data.active_session || null;

      box.innerHTML = `
        <div class="item">
          <div class="item-head">
            <div>
              <div class="item-title">${escapeHTML(student.full_name || 'Alumno')}</div>
              <div class="small">Matrícula: ${escapeHTML(student.enrolment_number || '—')}</div>
            </div>
            <div>${renderRequestStatus(request.status)}</div>
          </div>

          <div class="meta">
            <div class="meta-box">
              <span class="meta-label">Folio</span>
              <div class="meta-value">${escapeHTML(request.folio || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Temporada</span>
              <div class="meta-value">${escapeHTML(event.display_name || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Sesión activa</span>
              <div class="meta-value">${session ? escapeHTML(session.status || 'ACTIVE') : 'Sin sesión activa'}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Expira</span>
              <div class="meta-value">${session ? escapeHTML(session.expires_at || '—') : '—'}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Refresh count</span>
              <div class="meta-value">${session ? escapeHTML(session.refresh_count || 0) : 0}</div>
            </div>
          </div>
        </div>
      `;

      const currentToken =
        data.pass_session?.plain_token ||
        data.active_session?.plain_token ||
        '';

      statusBadge.className = session ? 'pill pill-ok' : 'pill pill-neutral';
      statusBadge.textContent = session ? 'QR activo' : 'Sin sesión';

      renderStudentQR(currentToken);
    }

    async function loadStudentPass() {
      try {
        const enrolment = getEnrolment();
        if (!enrolment) return showMsg('Primero escribe tu matrícula', false);

        const season = getSeason();
        const data = await getJSON(`/api/student/pass?enrolment_number=${encodeURIComponent(enrolment)}&season=${encodeURIComponent(season)}`);
        currentPass = data;
        renderPassInfo(data);
        showMsg('Estado del pase cargado correctamente');
      } catch (e) {
        currentPass = null;
        renderPassInfo(null);
        showMsg(e.message, false);
      }
    }

    async function refreshStudentPass() {
      try {
        const enrolment = getEnrolment();
        if (!enrolment) return showMsg('Primero escribe tu matrícula', false);

        const payload = {
          enrolment_number: enrolment,
          season: getSeason()
        };

        const data = await postJSON('/api/student/pass/refresh', payload);
        currentPass = data;
        renderPassInfo(data);
        setCurrentStep(3);
        showMsg(data.message || 'Credencial actualizada');
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    function renderPreview(data) {
      const box = document.getElementById('registrationPreview');

      if (!data) {
        box.innerHTML = `<div class="item"><div class="small">Todavía no hay preview del cierre.</div></div>`;
        return;
      }

      const student = data.student || {};
      const event = data.event || {};
      const project = data.project || {};
      const token = data.token || {};

      box.innerHTML = `
        <div class="item">
          <div class="item-head">
            <div>
              <div class="item-title">Preview válido</div>
              <div class="small">Revisa bien antes de confirmar</div>
            </div>
            <div><span class="pill pill-ok">PREVIEW OK</span></div>
          </div>

          <div class="meta">
            <div class="meta-box">
              <span class="meta-label">Alumno</span>
              <div class="meta-value">${escapeHTML(student.full_name || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Temporada</span>
              <div class="meta-value">${escapeHTML(event.display_name || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Proyecto</span>
              <div class="meta-value">${escapeHTML(project.general_name || '—')} | ${escapeHTML(project.project_name || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Carrera preferida</span>
              <div class="meta-value">${escapeHTML(project.partner_name || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Token</span>
              <div class="meta-value">${escapeHTML(token.token_value || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Token expira</span>
              <div class="meta-value">${escapeHTML(token.expires_at || '—')}</div>
            </div>
          </div>
        </div>
      `;
    }

    function renderRegistrationSuccess(data) {
      const box = document.getElementById('registrationSuccessBox');
      const btn = document.getElementById('confirmRegistrationBtn');

      if (!data) {
        box.classList.add('hidden');
        box.innerHTML = '';
        btn.disabled = false;
        return;
      }

      btn.disabled = true;
      box.classList.remove('hidden');

      box.innerHTML = `
        <div class="success-card">
          <div class="success-title">🎉 Inscripción completada</div>

          <div class="meta">
            <div class="meta-box">
              <span class="meta-label">Proyecto</span>
              <div class="meta-value">${escapeHTML(data.project_name || '—')}</div>
            </div>

            <div class="meta-box">
              <span class="meta-label">Organización</span>
              <div class="meta-value">${escapeHTML(data.general_name || '—')}</div>
            </div>

            <div class="meta-box">
              <span class="meta-label">Temporada</span>
              <div class="meta-value">${escapeHTML(data.season || getSeason())}</div>
            </div>

            <div class="meta-box">
              <span class="meta-label">Token usado</span>
              <div class="meta-value">${escapeHTML(data.token_value || '—')}</div>
            </div>

            <div class="meta-box">
              <span class="meta-label">Fecha</span>
              <div class="meta-value">${escapeHTML(data.accepted_at || '—')}</div>
            </div>

            <div class="meta-box">
              <span class="meta-label">Estado</span>
              <div class="meta-value">REGISTRADO</div>
            </div>
          </div>
        </div>
      `;
    }

    async function previewRegistration() {
      try {
        const enrolment = getEnrolment();
        const projectId = document.getElementById('selectedProjectId').value.trim();
        const tokenValue = document.getElementById('projectTokenInput').value.trim();

        if (!enrolment) return showMsg('Primero escribe tu matrícula', false);
        if (!projectId) return showMsg('Primero elige un proyecto', false);
        if (!tokenValue) return showMsg('Falta el token del proyecto', false);

        const payload = {
          enrolment_number: enrolment,
          season: getSeason(),
          project_id: Number(projectId),
          token_value: tokenValue
        };

        const data = await postJSON('/api/student/registration/preview', payload);
        currentPreview = data;
        renderPreview(data);
        setCurrentStep(4);

        showMsg(data.message || 'Preview válido');
      } catch (e) {
        currentPreview = null;
        renderPreview(null);
        showMsg(e.message, false);
      }
    }

    async function confirmRegistration() {
      try {
        const enrolment = getEnrolment();
        const projectId = document.getElementById('selectedProjectId').value.trim();
        const tokenValue = document.getElementById('projectTokenInput').value.trim();
        const acceptedFullName = document.getElementById('acceptanceFullNameInput').value.trim();
        const acceptedCheckbox = document.getElementById('acceptanceCheckbox').checked;
        const legalVersion = document.getElementById('legalVersionInput').value.trim() || 'v1';

        if (!enrolment) return showMsg('Primero escribe tu matrícula', false);
        if (!projectId) return showMsg('Primero elige un proyecto', false);
        if (!tokenValue) return showMsg('Falta el token del proyecto', false);
        if (!acceptedFullName) return showMsg('Debes escribir tu nombre completo', false);
        if (!acceptedCheckbox) return showMsg('Debes aceptar la confirmación legal', false);

        const payload = {
          enrolment_number: enrolment,
          season: getSeason(),
          project_id: Number(projectId),
          token_value: tokenValue,
          accepted_checkbox: acceptedCheckbox,
          accepted_full_name: acceptedFullName,
          legal_text_version: legalVersion
        };

        const data = await postJSON('/api/student/registration/confirm', payload);

        currentRegistration = {
          project_name: data.registration?.project_name || currentSelectedProject?.name || '—',
          general_name: data.registration?.general_name || currentSelectedProject?.general_name || '—',
          token_value: data.registration?.token_value || tokenValue,
          accepted_at: data.registration?.accepted_at || new Date().toLocaleString(),
          season: getSeason()
        };

        renderRegistrationSuccess(currentRegistration);
        setCurrentStep(4);
        showMsg(data.message || 'Registro completado');
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    document.addEventListener('DOMContentLoaded', async () => {
      const debouncedLoad = debounce(loadCatalog, 400);

      document.getElementById('seasonSelector').addEventListener('change', async () => {
        await loadCatalogsForSeason();
        await loadCatalog();
      });

      document.getElementById('catalogSearch').addEventListener('input', debouncedLoad);

      document.getElementById('filterPartner').addEventListener('change', loadCatalog);
      document.getElementById('filterModality').addEventListener('change', loadCatalog);
      document.getElementById('filterWeekDays').addEventListener('change', loadCatalog);
      document.getElementById('filterSchedule').addEventListener('change', loadCatalog);

      await loadCatalogsForSeason();
      await loadCatalog();
      renderSelectedProjectBanner();
      setCurrentStep(1);
    });


  // Auto-recarga en filtros (incluye temporada)
  ['filterPartner','filterModality','filterWeekDays','filterSchedule','seasonSelector']
    .forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('change', async () => {
          // Solo temporada necesita recargar catálogos
          if (id === 'seasonSelector') {
            await loadCatalogsForSeason();
          }
          await loadCatalog();
        });
      }
    });

  // Enter para buscar
  document.getElementById('catalogSearch').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') loadCatalog();
  });

  // Carga inicial
  await loadCatalogsForSeason();
  await loadCatalog();

  renderSelectedProjectBanner();
  setCurrentStep(1);

  // Auto refresh del QR (opcional)
  setInterval(() => {
    if (currentPass) {
      refreshStudentPass();
    }
  }, 60000); // cada 60s
});

  </script>
</body>
</html>
"""