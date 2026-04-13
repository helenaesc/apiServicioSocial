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
      --bg: #f4f7fa;
      --bg-soft: #fbfcfe;
      --panel: #ffffff;
      --panel-soft: #f8fbff;
      --text: #111827;
      --text-soft: #6b7280;
      --muted: #98a2b3;
      --line: #e5e7eb;
      --line-strong: #d1d5db;

      --blue: #3B82F6;
      --orange: #FF8C42;
      --green: #43AA8B;
      --pink: #F25C78;
      --purple: #7D5BA6;

      --blue-soft: #EFF6FF;
      --orange-soft: #FFF3EA;
      --green-soft: #ECFDF7;
      --pink-soft: #FFF1F5;
      --purple-soft: #F5F0FB;

      --shadow-sm: 0 4px 16px rgba(16, 24, 40, 0.05);
      --shadow-md: 0 12px 28px rgba(16, 24, 40, 0.08);
      --shadow-lg: 0 20px 40px rgba(16, 24, 40, 0.10);

      --r-sm: 12px;
      --r-md: 16px;
      --r-lg: 22px;
      --r-xl: 28px;
      --r-pill: 999px;
    }

    * { box-sizing: border-box; }

    html, body {
      margin: 0;
      padding: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: radial-gradient(circle at top left, #ffffff 0%, #f7f9fd 28%, #f4f7fa 100%);
      color: var(--text);
      min-height: 100vh;
    }

    .hidden { display: none !important; }

    .page-shell {
      max-width: 1460px;
      margin: 0 auto;
      padding: 20px;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
      margin-bottom: 18px;
    }

    .brand {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .brand strong {
      font-size: 1.2rem;
      font-weight: 900;
      letter-spacing: -.02em;
    }

    .brand span {
      font-size: .92rem;
      color: var(--text-soft);
    }

    .top-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .link-btn {
      text-decoration: none;
      border: 1px solid var(--line);
      background: white;
      color: var(--text-soft);
      border-radius: var(--r-md);
      padding: 10px 14px;
      font-size: .9rem;
      font-weight: 800;
      box-shadow: var(--shadow-sm);
      transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
    }

    .link-btn:hover {
      transform: translateY(-1px);
      border-color: var(--line-strong);
      box-shadow: var(--shadow-md);
    }

    .msg {
      display: none;
      margin-bottom: 18px;
      padding: 14px 16px;
      border-radius: 14px;
      font-size: .94rem;
      font-weight: 800;
      border: 1px solid transparent;
      box-shadow: var(--shadow-sm);
    }

    .msg.ok {
      display: block;
      background: var(--green-soft);
      color: var(--green);
      border-color: #cdeee4;
    }

    .msg.err {
      display: block;
      background: var(--pink-soft);
      color: var(--pink);
      border-color: #ffd7df;
    }

    .hero {
      position: relative;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: var(--r-xl);
      background:
        radial-gradient(circle at top right, rgba(125,91,166,0.15) 0%, rgba(125,91,166,0) 30%),
        radial-gradient(circle at bottom left, rgba(59,130,246,0.10) 0%, rgba(59,130,246,0) 24%),
        linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
      box-shadow: var(--shadow-lg);
      padding: 24px;
      margin-bottom: 18px;
    }

    .hero-grid {
      display: grid;
      grid-template-columns: 1.2fr .8fr;
      gap: 18px;
      align-items: center;
    }

    .hero-kicker {
      font-size: .76rem;
      text-transform: uppercase;
      letter-spacing: .1em;
      color: var(--purple);
      font-weight: 900;
      margin-bottom: 8px;
    }

    .hero h1 {
      margin: 0 0 10px;
      font-size: clamp(1.8rem, 3vw, 2.7rem);
      line-height: 1.05;
      letter-spacing: -.04em;
    }

    .hero p {
      margin: 0;
      color: var(--text-soft);
      font-size: 1rem;
      line-height: 1.6;
      max-width: 760px;
    }

    .hero-badges {
      margin-top: 16px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .hero-side {
      display: grid;
      gap: 12px;
    }

    .hero-panel {
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.84);
      backdrop-filter: blur(8px);
      border-radius: var(--r-lg);
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .hero-panel-label {
      font-size: .74rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 6px;
    }

    .hero-panel-value {
      font-size: 1rem;
      font-weight: 900;
      line-height: 1.35;
    }

    .hero-panel-sub {
      margin-top: 5px;
      color: var(--text-soft);
      font-size: .88rem;
      line-height: 1.45;
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

    .chip-primary { background: var(--purple-soft); color: var(--purple); border-color: #e6dbf3; }
    .chip-green { background: var(--green-soft); color: var(--green); border-color: #cdeee4; }
    .chip-orange { background: var(--orange-soft); color: var(--orange); border-color: #ffe1cf; }
    .chip-pink { background: var(--pink-soft); color: var(--pink); border-color: #ffd7df; }
    .chip-blue { background: var(--blue-soft); color: var(--blue); border-color: #d6e4ff; }
    .chip-neutral { background: #f2f4f7; color: #475467; border-color: #eaecf0; }

    .nav-strip {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
      margin-bottom: 18px;
    }

    .nav-card {
      border: 1px solid var(--line);
      background: white;
      border-radius: var(--r-lg);
      padding: 16px;
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    .nav-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .nav-card.active {
      border-color: #d6e4ff;
      background: linear-gradient(135deg, var(--blue-soft) 0%, white 100%);
      box-shadow: var(--shadow-md);
    }

    .nav-card.done {
      border-color: #bee7da;
      background: linear-gradient(135deg, var(--green-soft) 0%, white 100%);
    }

    .nav-index {
      font-size: .72rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 6px;
    }

    .nav-title {
      font-size: .98rem;
      font-weight: 900;
      margin-bottom: 4px;
    }

    .nav-desc {
      color: var(--text-soft);
      font-size: .84rem;
      line-height: 1.45;
    }

    .layout {
      display: grid;
      grid-template-columns: 1fr 360px;
      gap: 18px;
      align-items: start;
    }

    .main-column {
      display: grid;
      gap: 18px;
    }

    .side-column {
      position: sticky;
      top: 20px;
      display: grid;
      gap: 18px;
    }

    .section {
      display: none;
    }

    .section.active {
      display: block;
    }

    .card {
      border: 1px solid var(--line);
      background: linear-gradient(180deg, #ffffff 0%, #fcfdff 100%);
      border-radius: var(--r-lg);
      padding: 22px;
      box-shadow: var(--shadow-md);
    }

    .card-title-row {
      display: flex;
      justify-content: space-between;
      align-items: start;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }

    .card h2 {
      margin: 0;
      font-size: 1.12rem;
      line-height: 1.2;
      font-weight: 900;
    }

    .card-subtitle {
      color: var(--text-soft);
      font-size: .93rem;
      line-height: 1.55;
      margin-bottom: 14px;
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .field.span-2 {
      grid-column: span 2;
    }

    .field label {
      font-size: .76rem;
      text-transform: uppercase;
      letter-spacing: .06em;
      color: var(--muted);
      font-weight: 900;
    }

    input, select, textarea, button {
      font: inherit;
    }

    input, select, textarea {
      width: 100%;
      min-height: 46px;
      border: 1px solid var(--line-strong);
      background: white;
      border-radius: 14px;
      padding: 11px 13px;
      color: var(--text);
      transition: border-color .16s ease, box-shadow .16s ease;
    }

    textarea {
      min-height: 110px;
      resize: vertical;
    }

    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: var(--blue);
      box-shadow: 0 0 0 4px rgba(59,130,246,0.10);
    }

    .actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 16px;
    }

    button {
      border: none;
      min-height: 46px;
      border-radius: 14px;
      padding: 10px 15px;
      font-size: .94rem;
      font-weight: 900;
      cursor: pointer;
      transition: transform .15s ease, box-shadow .15s ease, opacity .15s ease;
    }

    button:hover {
      transform: translateY(-1px);
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--purple) 0%, #9b79c6 100%);
      color: white;
      box-shadow: 0 10px 20px rgba(125,91,166,0.20);
    }

    .btn-green {
      background: linear-gradient(135deg, var(--green) 0%, #57c3a2 100%);
      color: white;
      box-shadow: 0 10px 20px rgba(67,170,139,0.18);
    }

    .btn-orange {
      background: linear-gradient(135deg, var(--orange) 0%, #ffad76 100%);
      color: white;
      box-shadow: 0 10px 20px rgba(255,140,66,0.18);
    }

    .btn-blue {
      background: linear-gradient(135deg, var(--blue) 0%, #60A5FA 100%);
      color: white;
      box-shadow: 0 10px 20px rgba(59,130,246,0.18);
    }

    .btn-secondary {
      background: white;
      color: var(--text-soft);
      border: 1px solid var(--line);
      box-shadow: var(--shadow-sm);
    }

    .catalog-toolbar {
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 14px;
    }

    .catalog-stats {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 14px;
      padding: 14px 16px;
      background: linear-gradient(135deg, #fafbff 0%, #f6f9ff 100%);
      border: 1px solid var(--line);
      border-radius: 16px;
    }

    .catalog-count {
      font-weight: 900;
      font-size: .96rem;
    }

    .catalog-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
    }

    .project-card {
      position: relative;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 24px;
      background:
        radial-gradient(circle at top right, rgba(59,130,246,0.10) 0%, rgba(59,130,246,0.00) 30%),
        radial-gradient(circle at bottom left, rgba(125,91,166,0.10) 0%, rgba(125,91,166,0.00) 28%),
        linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
      box-shadow: var(--shadow-md);
      padding: 16px;
      transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    .project-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-lg);
      border-color: #d6e4ff;
    }

    .project-card.selected {
      border-color: #e2c6ef;
      box-shadow: 0 0 0 4px rgba(125,91,166,0.08), var(--shadow-lg);
    }

    .project-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      margin-bottom: 12px;
    }

    .project-org {
      font-size: .72rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 4px;
    }

    .project-title {
      font-size: 1.02rem;
      line-height: 1.25;
      font-weight: 900;
      margin-bottom: 3px;
    }

    .project-subtitle {
      color: var(--text-soft);
      font-size: .86rem;
      line-height: 1.4;
    }

    .project-rank {
      min-width: 56px;
      text-align: center;
      border-radius: 16px;
      padding: 10px 8px;
      border: 1px solid #dae7ff;
      background: linear-gradient(180deg, #eff5ff 0%, #ffffff 100%);
      color: var(--blue);
      font-size: .72rem;
      font-weight: 900;
    }

    .project-hero {
      border: 1px solid #e6ecf5;
      border-radius: 18px;
      background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 45%, #faf5ff 100%);
      padding: 14px;
      min-height: 116px;
      display: flex;
      align-items: flex-end;
      margin-bottom: 12px;
    }

    .project-hero-text {
      font-size: .9rem;
      font-weight: 700;
      line-height: 1.5;
      color: #344054;
    }

    .project-stats {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 12px;
    }

    .project-stat {
      border: 1px solid #edf1f7;
      background: #f9fafb;
      border-radius: 14px;
      padding: 10px 12px;
    }

    .project-stat-label {
      display: block;
      font-size: .7rem;
      text-transform: uppercase;
      letter-spacing: .04em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 4px;
    }

    .project-stat-value {
      font-size: .88rem;
      font-weight: 800;
      color: var(--text);
      line-height: 1.35;
    }

    .project-extra {
      display: grid;
      gap: 8px;
      margin-bottom: 12px;
    }

    .project-extra-row {
      color: var(--text-soft);
      font-size: .86rem;
      line-height: 1.45;
    }

    .project-extra-row strong {
      color: var(--text);
    }

    .selected-banner {
      border: 1px dashed #e2c6ef;
      background: linear-gradient(135deg, #fcf8ff 0%, #ffffff 100%);
      border-radius: 16px;
      padding: 14px 16px;
      margin-bottom: 14px;
    }

    .selected-banner-title {
      font-size: .88rem;
      color: var(--purple);
      font-weight: 900;
      margin-bottom: 4px;
    }

    .selected-banner-text {
      font-size: .9rem;
      color: var(--text-soft);
      line-height: 1.45;
    }

    .info-stack {
      display: grid;
      gap: 12px;
    }

    .info-card {
      border: 1px solid var(--line);
      background: white;
      border-radius: 18px;
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .info-head {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: start;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }

    .info-title {
      font-size: .98rem;
      font-weight: 900;
    }

    .info-sub {
      color: var(--text-soft);
      font-size: .84rem;
    }

    .meta-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }

    .meta-box {
      border: 1px solid #edf1f7;
      background: #f9fafb;
      border-radius: 14px;
      padding: 10px 12px;
    }

    .meta-label {
      display: block;
      font-size: .7rem;
      text-transform: uppercase;
      letter-spacing: .04em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 4px;
    }

    .meta-value {
      font-size: .88rem;
      font-weight: 800;
      line-height: 1.4;
      color: var(--text);
    }

    .mono {
      display: inline-block;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      background: #111827;
      color: #f8fafc;
      border-radius: 12px;
      padding: 9px 11px;
      font-size: .88rem;
      word-break: break-all;
    }

    .mono-soft {
      display: inline-block;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      background: #f2f4f7;
      color: #344054;
      border: 1px solid #eaecf0;
      border-radius: 10px;
      padding: 6px 9px;
      font-size: .82rem;
      word-break: break-all;
    }

    .qr-shell {
      border: 1px solid var(--line);
      background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
      border-radius: 22px;
      padding: 18px;
      display: grid;
      gap: 14px;
      box-shadow: var(--shadow-sm);
    }

    .qr-head {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }

    .qr-canvas-wrap {
      min-height: 240px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px dashed #d8e4ff;
      background: #fcfdff;
      border-radius: 18px;
    }

    .qr-plain {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      background: #111827;
      color: #f8fafc;
      border-radius: 14px;
      padding: 12px;
      font-size: .9rem;
      text-align: center;
      word-break: break-all;
    }

    .legal-box {
      border: 1px solid #dbeafe;
      background: #f8fbff;
      border-radius: 16px;
      padding: 16px;
      margin-top: 12px;
    }

    .preview-box {
      display: grid;
      gap: 12px;
      margin-top: 14px;
    }

    .success-card {
      border: 1px solid #cceee3;
      background: linear-gradient(135deg, #ecfdf7 0%, #ffffff 100%);
      border-radius: 18px;
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .success-title {
      font-size: 1rem;
      font-weight: 900;
      color: var(--green);
      margin-bottom: 8px;
    }

    .empty-state {
      border: 1px dashed var(--line-strong);
      background: linear-gradient(180deg, #fcfcfd 0%, #f9fafb 100%);
      border-radius: 18px;
      padding: 20px;
      text-align: center;
      color: var(--text-soft);
      box-shadow: var(--shadow-sm);
    }

    .empty-title {
      font-size: .96rem;
      font-weight: 900;
      color: var(--text);
      margin-bottom: 6px;
    }

    @media (max-width: 1280px) {
      .nav-strip {
        grid-template-columns: repeat(3, 1fr);
      }

      .layout {
        grid-template-columns: 1fr;
      }

      .side-column {
        position: static;
      }

      .hero-grid {
        grid-template-columns: 1fr;
      }

      .catalog-toolbar {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }
    }

    @media (max-width: 820px) {
      .nav-strip {
        grid-template-columns: repeat(2, 1fr);
      }

      .form-grid,
      .meta-grid {
        grid-template-columns: 1fr;
      }

      .field.span-2 {
        grid-column: span 1;
      }

      .catalog-toolbar {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .project-stats {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 560px) {
      .page-shell {
        padding: 14px;
      }

      .nav-strip {
        grid-template-columns: 1fr;
      }

      .catalog-toolbar {
        grid-template-columns: 1fr;
      }

      .actions {
        flex-direction: column;
      }

      button {
        width: 100%;
      }
    }
  </style>
</head>
<body>
  <div class="page-shell">
    <div id="msg" class="msg"></div>

    <div class="topbar">
      <div class="brand">
        <strong>Registro de Proyectos</strong>
        <span>Explora el catálogo, solicita tu pase y cierra tu inscripción.</span>
      </div>
      <div class="top-actions">
        <a href="/admin" class="link-btn">Admin</a>
        <a href="/health" class="link-btn">Health</a>
      </div>
    </div>

    <section class="hero">
      <div class="hero-grid">
        <div>
          <div class="hero-kicker">Ruta del alumno</div>
          <h1>Explora primero. Decide bien. Regístrate solo cuando ya tengas acceso.</h1>
          <p>
            Puedes revisar el catálogo antes de solicitar tu pase. Cuando el staff te habilite acceso, podrás cerrar tu inscripción con el token del proyecto.
          </p>
          <div class="hero-badges">
            <span class="chip chip-primary">Catálogo visible</span>
            <span class="chip chip-green">Flujo guiado</span>
            <span class="chip chip-blue">Credencial viva</span>
          </div>
        </div>

        <div class="hero-side">
          <div class="hero-panel">
            <div class="hero-panel-label">Estado de ruta</div>
            <div class="hero-panel-value" id="heroRouteStatus">Explorando catálogo</div>
            <div class="hero-panel-sub">Tu progreso se actualiza conforme completas cada paso.</div>
          </div>
          <div class="hero-panel">
            <div class="hero-panel-label">Proyecto actual</div>
            <div class="hero-panel-value" id="heroProjectStatus">Sin proyecto seleccionado</div>
            <div class="hero-panel-sub">Selecciona uno desde el catálogo para preparar tu cierre.</div>
          </div>
        </div>
      </div>
    </section>

    <section class="nav-strip" id="stepsBar">
      <div class="nav-card active" data-step="1" onclick="showStudentSection('catalogSection')">
        <div class="nav-index">Paso 1</div>
        <div class="nav-title">Explorar catálogo</div>
        <div class="nav-desc">Busca, compara y elige un proyecto con intención.</div>
      </div>
      <div class="nav-card" data-step="2" onclick="showStudentSection('requestSection')">
        <div class="nav-index">Paso 2</div>
        <div class="nav-title">Solicitar pase</div>
        <div class="nav-desc">Genera tu folio con tus datos completos.</div>
      </div>
      <div class="nav-card" data-step="3" onclick="showStudentSection('passSection')">
        <div class="nav-index">Paso 3</div>
        <div class="nav-title">Mostrar QR</div>
        <div class="nav-desc">Presenta tu credencial viva al staff.</div>
      </div>
      <div class="nav-card" data-step="4" onclick="showStudentSection('registrationSection')">
        <div class="nav-index">Paso 4</div>
        <div class="nav-title">Cerrar inscripción</div>
        <div class="nav-desc">Haz preview y confirma legalmente.</div>
      </div>
      <div class="nav-card" data-step="5" onclick="showStudentSection('statusSection')">
        <div class="nav-index">Mi estado</div>
        <div class="nav-title">Seguimiento</div>
        <div class="nav-desc">Consulta folio, pase y progreso actual.</div>
      </div>
    </section>

    <div class="layout">
      <main class="main-column">
        <section id="catalogSection" class="section active">
          <div class="card">
            <div class="card-title-row">
              <div>
                <h2>Catálogo de proyectos</h2>
              </div>
              <span class="chip chip-primary">Explorar</span>
            </div>

            <div class="card-subtitle">
              Revisa la temporada, filtra el catálogo y elige el proyecto que más te interese. Ver catálogo no te registra todavía.
            </div>

            <div class="catalog-toolbar">
              <div class="field">
                <label>Temporada</label>
                <select id="seasonSelector">
                  <option value="PRIMAVERA">Primavera</option>
                  <option value="INVIERNO">Invierno</option>
                </select>
              </div>
              <div class="field">
                <label>Buscar</label>
                <input id="catalogSearch" placeholder="Nombre, responsables, comentarios">
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
              <button type="button" class="btn-blue" onclick="goToSectionAndStep('requestSection', 2)">Ya elegí proyecto</button>
            </div>

            <div class="catalog-stats">
              <div class="catalog-count" id="catalogCountLabel">Sin catálogo cargado</div>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <span class="chip chip-blue" id="catalogSeasonChip">Temporada</span>
                <span class="chip chip-neutral" id="catalogProjectsChip">0 proyectos</span>
              </div>
            </div>

            <div id="selectedProjectBanner" class="selected-banner hidden">
              <div class="selected-banner-title">Proyecto seleccionado</div>
              <div id="selectedProjectBannerText" class="selected-banner-text">Aún no seleccionas proyecto.</div>
            </div>

            <div id="catalogList" class="catalog-grid"></div>
          </div>
        </section>

        <section id="requestSection" class="section">
          <div class="card">
            <div class="card-title-row">
              <div>
                <h2>Solicitar pase</h2>
              </div>
              <span class="chip chip-orange">Paso 2</span>
            </div>

            <div class="card-subtitle">
              Esto no te registra todavía. Solo crea tu solicitud y tu folio para que el staff pueda validarte presencialmente.
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
                <input id="secondEmailInput" type="email" placeholder="Opcional">
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
              <button type="button" class="btn-orange" onclick="createStudentRequest()">Solicitar pase</button>
              <button type="button" class="btn-secondary" onclick="loadStudentRequest()">Consultar solicitud</button>
              <button type="button" class="btn-blue" onclick="goToSectionAndStep('passSection', 3)">Ir a mi QR</button>
            </div>
          </div>
        </section>

        <section id="passSection" class="section">
          <div class="card">
            <div class="card-title-row">
              <div>
                <h2>Credencial viva</h2>
              </div>
              <span class="chip chip-blue">Paso 3</span>
            </div>

            <div class="card-subtitle">
              Refresca tu QR cuando el staff te lo pida. El QR cambia y el anterior deja de servir.
            </div>

            <div class="actions">
              <button type="button" class="btn-blue" onclick="refreshStudentPass()">Refrescar credencial</button>
              <button type="button" class="btn-secondary" onclick="loadStudentPass()">Consultar pase</button>
              <button type="button" class="btn-green" onclick="goToSectionAndStep('registrationSection', 4)">Ya tengo acceso</button>
            </div>

            <div id="passInfo" class="info-stack" style="margin-top:14px;"></div>

            <div class="qr-shell" style="margin-top:14px;">
              <div class="qr-head">
                <div>
                  <div style="font-weight:900; margin-bottom:3px;">QR vigente del pase</div>
                  <div style="font-size:.86rem; color:var(--text-soft);">
                    Este código cambia al refrescarse y deja de servir al expirar o cuando el staff lo usa.
                  </div>
                </div>
                <div id="qrStatusBadge" class="chip chip-neutral">Sin sesión</div>
              </div>
              <div class="qr-canvas-wrap">
                <div id="qrCanvas"></div>
              </div>
              <div id="qrPlainToken" class="qr-plain">Genera tu código</div>
            </div>
          </div>
        </section>

        <section id="registrationSection" class="section">
          <div class="card">
            <div class="card-title-row">
              <div>
                <h2>Cierre de inscripción</h2>
              </div>
              <span class="chip chip-green">Paso 4</span>
            </div>

            <div class="card-subtitle">
              Solo cuando el staff ya te haya habilitado acceso y tengas el token del proyecto, primero haz preview y luego confirma.
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

            <div class="legal-box">
              <div style="font-size:.84rem; font-weight:900; margin-bottom:8px; color:var(--text);">
                Confirmación legal
              </div>
              <label style="display:flex; gap:10px; align-items:flex-start; font-size:.92rem; line-height:1.55; color:var(--text);">
                <input id="acceptanceCheckbox" type="checkbox" style="width:auto; min-height:auto; margin-top:3px;">
                <span>
                  Confirmo que realicé esta inscripción de manera personal, que acepto el proyecto seleccionado y que entiendo que el cierre queda auditado con token y registro digital.
                </span>
              </label>
            </div>

            <div class="actions">
              <button type="button" class="btn-secondary" onclick="previewRegistration()">Ver preview</button>
              <button type="button" class="btn-green" id="confirmRegistrationBtn" onclick="confirmRegistration()">Confirmar inscripción</button>
              <button type="button" class="btn-blue" onclick="goToSectionAndStep('statusSection', 5)">Ver mi estado</button>
            </div>

            <div id="registrationPreview" class="preview-box"></div>
            <div id="registrationSuccessBox" class="preview-box hidden"></div>
          </div>
        </section>

        <section id="statusSection" class="section">
          <div class="card">
            <div class="card-title-row">
              <div>
                <h2>Mi estado actual</h2>
              </div>
              <span class="chip chip-primary">Seguimiento</span>
            </div>

            <div class="card-subtitle">
              Aquí puedes revisar tu folio, el estado de tu solicitud y tu progreso general dentro del flujo.
            </div>

            <div id="requestInfo" class="info-stack"></div>
          </div>
        </section>
      </main>

      <aside class="side-column">
        <section class="card" id="studentRegistrationSection">
          <div class="card-title-row">
            <div>
              <h2>Resumen de avance</h2>
            </div>
            <span class="chip chip-neutral">Ruta</span>
          </div>

          <div class="info-stack">
            <div class="info-card">
              <div class="info-head">
                <div>
                  <div class="info-title">Estado actual</div>
                  <div class="info-sub">Lectura rápida de tu progreso</div>
                </div>
              </div>
              <div class="meta-grid">
                <div class="meta-box">
                  <span class="meta-label">Ruta</span>
                  <div class="meta-value" id="sideRouteStatus">Explorando catálogo</div>
                </div>
                <div class="meta-box">
                  <span class="meta-label">Proyecto</span>
                  <div class="meta-value" id="sideProjectStatus">Sin selección</div>
                </div>
              </div>
            </div>

            <div class="info-card">
              <div class="info-head">
                <div>
                  <div class="info-title">Atajos</div>
                  <div class="info-sub">Muévete rápido según tu estado</div>
                </div>
              </div>
              <div class="actions" style="margin-top:0;">
                <button type="button" class="btn-secondary" onclick="showStudentSection('catalogSection')">Catálogo</button>
                <button type="button" class="btn-secondary" onclick="showStudentSection('requestSection')">Pase</button>
                <button type="button" class="btn-secondary" onclick="showStudentSection('passSection')">QR</button>
                <button type="button" class="btn-secondary" onclick="showStudentSection('registrationSection')">Registro</button>
              </div>
            </div>
          </div>
        </section>
      </aside>
    </div>
  </div>

  <script>
    let currentCatalog = [];
    let currentRequest = null;
    let currentPass = null;
    let currentPreview = null;
    let currentSelectedProject = null;
    let currentRegistration = null;
    let catalogSearchTimer = null;
    let canStudentRegister = false;
    
    function humanizeErrorMessage(err) {
      const raw =
        (typeof err === 'string' ? err : '') ||
        err?.error ||
        err?.message ||
        '';

      const msg = raw.toLowerCase();

      // --- TOKENS ---
      if (msg.includes('token no existe')) {
        return 'Ese token no existe. Verifica que esté bien escrito.';
      }

      if (msg.includes('token expir')) {
        return 'Ese token ya expiró. Solicita uno nuevo al socio del proyecto.';
      }

      if (msg.includes('token ya fue utilizado')) {
        return 'Ese token ya fue utilizado y no puede volver a usarse.';
      }

      if (msg.includes('token fue revocado')) {
        return 'Ese token fue revocado. Solicita uno nuevo al responsable del proyecto.';
      }

      if (msg.includes('token no corresponde')) {
        return 'Ese token no pertenece al proyecto seleccionado.';
      }

      if (msg.includes('token está reservado')) {
        return 'Ese token está reservado por otro alumno.';
      }

      // --- SOLICITUD ---
      if (msg.includes('no existe solicitud')) {
        return 'No tienes una solicitud para esta temporada. Primero solicita tu pase.';
      }

      if (msg.includes('no está habilitada para registro')) {
        return 'Aún no estás habilitado por staff. Muestra tu QR para validación.';
      }

      if (msg.includes('ya tiene un registro activo')) {
        return 'Ya estás inscrito en esta temporada.';
      }

      if (msg.includes('solicitud ya no permite acceso')) {
        return 'Esta solicitud ya fue cerrada o cancelada.';
      }

      // --- QR / PASE ---
      if (msg.includes('qr no reconocido')) {
        return 'El QR no es válido. Genera uno nuevo.';
      }

      if (msg.includes('qr expirado')) {
        return 'El QR expiró. Pide al alumno que lo refresque.';
      }

      if (msg.includes('qr no disponible')) {
        return 'Este QR ya no está disponible (puede haber sido usado o expirado).';
      }

      if (msg.includes('la sesión ya no está activa')) {
        return 'La sesión del QR ya no está activa.';
      }

      // --- MATRÍCULA ---
      if (msg.includes('matrícula no coincide')) {
        return 'La matrícula no coincide con la del pase.';
      }

      // --- PROYECTOS ---
      if (msg.includes('proyecto no pertenece')) {
        return 'El proyecto no corresponde a la temporada seleccionada.';
      }

      if (msg.includes('proyecto no está disponible')) {
        return 'Este proyecto ya no está disponible para inscripción.';
      }

      // --- CAMPOS ---
      if (msg.includes('es obligatorio')) {
        return 'Faltan campos obligatorios. Revisa la información.';
      }

      // --- TEMPORADA ---
      if (msg.includes('temporada inválida')) {
        return 'La temporada seleccionada no es válida.';
      }

      if (msg.includes('no hay temporada visible')) {
        return 'No hay temporada activa disponible en este momento.';
      }

      // --- FALLBACK ---
      if (raw) {
        return raw; // muestra mensaje backend si no lo reconocemos
      }

      return 'Ocurrió un error inesperado. Intenta nuevamente.';
    }

    function syncRegistrationLock() {
      const step4Card = document.querySelector('.nav-card[data-step="4"]');
      const previewBtn = document.querySelector('button[onclick="previewRegistration()"]');
      const confirmBtn = document.getElementById('confirmRegistrationBtn');
      const tokenInput = document.getElementById('projectTokenInput');
      const nameInput = document.getElementById('acceptanceFullNameInput');
      const legalInput = document.getElementById('legalVersionInput');
      const checkbox = document.getElementById('acceptanceCheckbox');

      canStudentRegister =
        !!currentRegistration ||
        currentRequest?.request?.status === 'ACCESS_ENABLED' ||
        currentRequest?.status === 'ACCESS_ENABLED' ||
        currentPass?.flow?.can_register === true;

      if (step4Card) {
        step4Card.style.opacity = canStudentRegister ? '1' : '.55';
        step4Card.style.pointerEvents = canStudentRegister ? 'auto' : 'none';
        step4Card.title = canStudentRegister
          ? ''
          : 'Bloqueado: primero debes mostrar tu QR al staff para habilitar acceso';
      }

      if (previewBtn) previewBtn.disabled = !canStudentRegister;
      if (confirmBtn) confirmBtn.disabled = !canStudentRegister;
      if (tokenInput) tokenInput.disabled = !canStudentRegister;
      if (nameInput) nameInput.disabled = !canStudentRegister;
      if (legalInput) legalInput.disabled = !canStudentRegister;
      if (checkbox) checkbox.disabled = !canStudentRegister;
    }

    function escapeHTML(value) {
      return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function showMsg(text, ok = true) {
      const el = document.getElementById('msg');
      if (!el) return;
      el.textContent = text || '';
      el.className = 'msg ' + (ok ? 'ok' : 'err');
    }

    function getSeason() {
      const el = document.getElementById('seasonSelector');
      return el ? el.value : 'PRIMAVERA';
    }

    function getEnrolment() {
      return (document.getElementById('enrolmentInput')?.value || '').trim().toLowerCase();
    }

    function showStudentSection(sectionId) {
      document.querySelectorAll('.section').forEach(el => el.classList.remove('active'));
      document.getElementById(sectionId)?.classList.add('active');
    }

    function setCurrentStep(step) {
      document.querySelectorAll('.nav-card').forEach(el => {
        const n = Number(el.getAttribute('data-step'));
        el.classList.remove('active', 'done');
        if (n < step) el.classList.add('done');
        else if (n === step) el.classList.add('active');
      });
    }

    function goToSectionAndStep(sectionId, step) {
      showStudentSection(sectionId);
      setCurrentStep(step);
    }

    async function getJSON(url) {
      const r = await fetch(url);
      const data = await r.json().catch(() => ({}));

      if (!r.ok) {
        throw {
          error: data.error || data.message || ('Error ' + r.status),
          status: r.status
        };
      }

      return data;
    }

    async function postJSON(url, body) {
      const r = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      const data = await r.json().catch(() => ({}));

      if (!r.ok) {
        throw {
          error: data.error || data.message || ('Error ' + r.status),
          status: r.status
        };
      }

      return data;
    }

    async function tryGet(urls) {
      let lastError = null;

      for (const url of urls) {
        try {
          return await getJSON(url);
        } catch (e) {
          console.error('Falló GET:', url, e);
          lastError = e;
        }
      }

      throw lastError || new Error('No se pudo completar la consulta');
    }

    async function tryPost(candidates) {
      let lastError = null;

      for (const item of candidates) {
        try {
          return await postJSON(item.url, item.body);
        } catch (e) {
          console.error('Falló POST:', item.url, e);
          lastError = e;
        }
      }

      throw lastError || new Error('No se pudo completar la operación');
    }

    function fillSelect(id, items, labelKey = 'description') {
      const el = document.getElementById(id);
      if (!el) return;
      const firstOption = el.querySelector('option')
        ? el.querySelector('option').outerHTML
        : '<option value="">Todas</option>';
      el.innerHTML = firstOption;
      for (const item of (items || [])) {
        const opt = document.createElement('option');
        opt.value = item.id ?? item.value ?? item.name ?? '';
        opt.textContent =
          item[labelKey] ??
          item.description ??
          item.name ??
          item.label ??
          item.value ??
          'Opción';
        el.appendChild(opt);
      }
    }

    function updateHeroState() {
      const route = document.getElementById('heroRouteStatus');
      const project = document.getElementById('heroProjectStatus');
      const sideRoute = document.getElementById('sideRouteStatus');
      const sideProject = document.getElementById('sideProjectStatus');

      let routeText = 'Explorando catálogo';

      if (currentRegistration) routeText = 'Inscripción completada';
      else if (currentPreview) routeText = 'Preview listo para confirmar';
      else if (currentPass && (currentPass.pass_session || currentPass.active_session)) routeText = 'Pase activo para validación';
      else if (currentRequest) routeText = 'Solicitud creada';

      let projectText = 'Sin proyecto seleccionado';
      if (currentSelectedProject) {
        projectText = `${currentSelectedProject.general_name || currentSelectedProject.organization || 'Proyecto'} | ${currentSelectedProject.name || currentSelectedProject.project_name || 'Sin nombre'}`;
      }

      if (route) route.textContent = routeText;
      if (project) project.textContent = projectText;
      if (sideRoute) sideRoute.textContent = routeText;
      if (sideProject) sideProject.textContent = currentSelectedProject ? (currentSelectedProject.name || currentSelectedProject.project_name || 'Proyecto') : 'Sin selección';
    }

    function renderEmptyState(title, subtitle) {
      return `
        <div class="empty-state">
          <div class="empty-title">${escapeHTML(title)}</div>
          <div>${escapeHTML(subtitle || '')}</div>
        </div>
      `;
    }

    function resetCatalogFilters() {
      document.getElementById('catalogSearch').value = '';
      document.getElementById('filterPartner').value = '';
      document.getElementById('filterModality').value = '';
      document.getElementById('filterWeekDays').value = '';
      document.getElementById('filterSchedule').value = '';
      loadCatalog();
    }

    function renderSelectedProjectBanner() {
      const banner = document.getElementById('selectedProjectBanner');
      const text = document.getElementById('selectedProjectBannerText');
      if (!banner || !text) return;

      if (!currentSelectedProject) {
        banner.classList.add('hidden');
        text.textContent = 'Aún no seleccionas proyecto.';
        updateHeroState();
        return;
      }

      banner.classList.remove('hidden');
      text.innerHTML = `
        <strong>${escapeHTML(currentSelectedProject.general_name || currentSelectedProject.organization || 'Proyecto')}</strong> |
        ${escapeHTML(currentSelectedProject.name || currentSelectedProject.project_name || 'Sin nombre')}
        · ${escapeHTML(currentSelectedProject.modalidad || currentSelectedProject.modality || currentSelectedProject.modality_name || '—')}
        · ${escapeHTML(currentSelectedProject.horario || currentSelectedProject.schedule || currentSelectedProject.schedule_name || '—')}
      `;
      updateHeroState();
    }

    function renderCatalogHeader(projects, eventInfo = null) {
      const season = eventInfo?.season || getSeason();
      const displayName = eventInfo?.display_name || season;
      const countLabel = document.getElementById('catalogCountLabel');
      const seasonChip = document.getElementById('catalogSeasonChip');
      const projectsChip = document.getElementById('catalogProjectsChip');

      if (countLabel) countLabel.textContent = `Catálogo de ${displayName}`;
      if (seasonChip) seasonChip.textContent = season;
      if (projectsChip) projectsChip.textContent = `${projects.length} proyectos`;
    }

    function renderCatalog(projects) {
      const list = document.getElementById('catalogList');
      if (!list) return;

      if (!projects || !projects.length) {
        list.innerHTML = renderEmptyState(
          'No hay proyectos para mostrar',
          'Prueba otros filtros o revisa si la temporada ya tiene proyectos activos y visibles para alumno.'
        );
        return;
      }

      list.innerHTML = projects.map((p, idx) => {
        const projectId = p.id ?? p.project_id ?? '';
        const generalName = p.general_name ?? p.organization ?? p.partner_group ?? 'Proyecto';
        const projectName = p.name ?? p.project_name ?? 'Sin nombre';
        const partnerName = p.socio ?? p.partner ?? p.partner_name ?? 'Sin preferencia';
        const modalidad = p.modalidad ?? p.modality ?? p.modality_name ?? '—';
        const dias = p.dia ?? p.days ?? p.week_days ?? p.week_days_name ?? '—';
        const horario = p.horario ?? p.schedule ?? p.schedule_name ?? '—';
        const cupos = p.cupos_disponibles ?? p.cupos ?? p.slots_total ?? '—';
        const objetivos = p.objectives ?? p.comments ?? p.description ?? 'Proyecto activo para esta temporada.';
        const duracion = p.duration ?? '—';
        const location = p.location ?? '—';
        const competencies = p.competencies ?? '—';
        const isSelected =
          currentSelectedProject &&
          Number(currentSelectedProject.id ?? currentSelectedProject.project_id) === Number(projectId);

        return `
          <article class="project-card ${isSelected ? 'selected' : ''}">
            <div class="project-head">
              <div>
                <div class="project-org">${escapeHTML(generalName)}</div>
                <div class="project-title">${escapeHTML(projectName)}</div>
                <div class="project-subtitle">Carrera preferida: ${escapeHTML(partnerName)}</div>
              </div>
              <div class="project-rank">CARD<br>#${idx + 1}</div>
            </div>

            <div class="project-hero">
              <div class="project-hero-text">
                ${escapeHTML(String(objetivos).slice(0, 155))}
              </div>
            </div>

            <div class="project-stats">
              <div class="project-stat">
                <span class="project-stat-label">Modalidad</span>
                <div class="project-stat-value">${escapeHTML(modalidad)}</div>
              </div>
              <div class="project-stat">
                <span class="project-stat-label">Días</span>
                <div class="project-stat-value">${escapeHTML(dias)}</div>
              </div>
              <div class="project-stat">
                <span class="project-stat-label">Horario</span>
                <div class="project-stat-value">${escapeHTML(horario)}</div>
              </div>
              <div class="project-stat">
                <span class="project-stat-label">Cupos</span>
                <div class="project-stat-value">${escapeHTML(cupos)}</div>
              </div>
            </div>

            <div class="project-extra">
              <div class="project-extra-row"><strong>Duración:</strong> ${escapeHTML(duracion)}</div>
              <div class="project-extra-row"><strong>Lugar:</strong> ${escapeHTML(location)}</div>
              <div class="project-extra-row"><strong>Competencias:</strong> ${escapeHTML(competencies)}</div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="selectProject(${Number(projectId)})">Elegir proyecto</button>
              <button type="button" class="btn-blue" onclick="selectProjectAndContinue(${Number(projectId)})">Elegir y seguir</button>
            </div>
          </article>
        `;
      }).join('');
    }

    function selectProject(projectId) {
      const project = currentCatalog.find(p => Number(p.id ?? p.project_id) === Number(projectId));
      if (!project) return;

      currentSelectedProject = project;
      document.getElementById('selectedProjectId').value = String(project.id ?? project.project_id ?? '');
      document.getElementById('selectedProjectName').value =
        `${project.general_name ?? project.organization ?? 'Sin nombre general'} | ${project.name ?? project.project_name ?? 'Sin nombre'}`;

      renderCatalog(currentCatalog);
      renderSelectedProjectBanner();
      updateHeroState();
      showMsg('Proyecto seleccionado para el cierre de inscripción');
    }

    function selectProjectAndContinue(projectId) {
      selectProject(projectId);
      goToSectionAndStep('requestSection', 2);
    }

    async function loadCatalogsForSeason() {
      try {
        const season = getSeason();
        const data = await tryGet([
          `/api/catalogs?temporada=${encodeURIComponent(season)}`,
          `/api/catalogs?season=${encodeURIComponent(season)}`,
          `/api/catalogs`
        ]);

        const partners = data.socio || data.partner || data.partners || data.carreras || [];
        const modalities = data.modalidad || data.modality || data.modalities || [];
        const weekDays = data.dias || data.week_days || data.weekDays || data.days || [];
        const schedules = data.horario || data.schedule || data.schedules || [];

        fillSelect('filterPartner', partners, 'name');
        fillSelect('filterModality', modalities, 'description');
        fillSelect('filterWeekDays', weekDays, 'description');
        fillSelect('filterSchedule', schedules, 'description');
      } catch (e) {
        showMsg('No se pudieron cargar los catálogos: ' + e.message, false);
      }
    }

    async function loadCatalog() {
      try {
        const season = getSeason();
        const q = (document.getElementById('catalogSearch').value || '').trim();
        const socio = document.getElementById('filterPartner').value;
        const modalidad = document.getElementById('filterModality').value;
        const dia = document.getElementById('filterWeekDays').value;
        const horario = document.getElementById('filterSchedule').value;

        const params1 = new URLSearchParams();
        params1.set('temporada', season);
        if (q) params1.set('q', q);
        if (socio) params1.set('socio', socio);
        if (modalidad) params1.set('modalidad', modalidad);
        if (dia) params1.set('dia', dia);
        if (horario) params1.set('horario', horario);

        const params2 = new URLSearchParams();
        params2.set('season', season);
        if (q) params2.set('q', q);
        if (socio) params2.set('partner', socio);
        if (modalidad) params2.set('modality', modalidad);
        if (dia) params2.set('week_days', dia);
        if (horario) params2.set('schedule', horario);

        const data = await tryGet([
          `/api/projects?${params1.toString()}`,
          `/api/projects?${params2.toString()}`,
          `/api/projects`
        ]);

        currentCatalog = data.items || data.projects || data.rows || (Array.isArray(data) ? data : []);
        const eventInfo = data.event || data.current_event || null;

        renderCatalogHeader(currentCatalog, eventInfo);
        renderCatalog(currentCatalog);
        renderSelectedProjectBanner();

        if (!currentCatalog.length) {
          showMsg('No hay proyectos visibles para alumno en esta temporada', false);
        } else {
          showMsg('Catálogo cargado correctamente');
        }
      } catch (e) {
        currentCatalog = [];
        renderCatalogHeader([], null);
        renderCatalog([]);
        showMsg('No se pudo cargar el catálogo: ' + e.message, false);
      }
    }

    function scheduleCatalogSearch() {
      clearTimeout(catalogSearchTimer);
      catalogSearchTimer = setTimeout(() => {
        loadCatalog();
      }, 280);
    }

    function renderRequestStatus(status) {
      const value = String(status || '').toUpperCase();
      const map = {
        REQUESTED: ['chip chip-blue', 'REQUESTED'],
        VALIDATED: ['chip chip-primary', 'VALIDATED'],
        ACCESS_ENABLED: ['chip chip-green', 'ACCESS_ENABLED'],
        REGISTERED: ['chip chip-green', 'REGISTERED'],
        CANCELLED: ['chip chip-pink', 'CANCELLED'],
        CLOSED: ['chip chip-orange', 'CLOSED']
      };
      const cfg = map[value] || ['chip chip-neutral', value || '—'];
      return `<span class="${cfg[0]}">${cfg[1]}</span>`;
    }

    function renderRequestInfo(data) {
      const box = document.getElementById('requestInfo');
      if (!box) return;

      if (!data) {
        box.innerHTML = renderEmptyState(
          'Todavía no hay información de solicitud',
          'Primero captura tus datos y genera tu folio.'
        );
        updateHeroState();
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
        <div class="info-card">
          <div class="info-head">
            <div>
              <div class="info-title">Folio ${escapeHTML(request.folio || '—')}</div>
              <div class="info-sub">Estado actual de tu solicitud</div>
            </div>
            <div>${renderRequestStatus(request.status)}</div>
          </div>

          <div class="meta-grid">
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
      updateHeroState();
      syncRegistrationLock();
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
          season: getSeason(),
          temporada: getSeason()
        };

        if (!payload.full_name || !payload.enrolment_number || !payload.email || !payload.phone_number || !payload.degree || !payload.semester) {
          return showMsg('Faltan campos obligatorios para solicitar pase', false);
        }

        const data = await tryPost([
          { url: '/api/student/requests', body: payload },
          { url: '/api/student/request', body: payload },
          { url: '/api/student_requests', body: payload }
        ]);

        currentRequest = data;
        renderRequestInfo(data);
        setCurrentStep(3);
        updateHeroState();
        showMsg(data.message || 'Solicitud procesada correctamente');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    async function loadStudentRequest() {
      try {
        const enrolment = getEnrolment();
        if (!enrolment) return showMsg('Primero escribe tu matrícula', false);

        const season = getSeason();

        const data = await getJSON(
          `/api/student/requests?enrolment_number=${encodeURIComponent(enrolment)}&season=${encodeURIComponent(season)}`
        );

        currentRequest = data;
        renderRequestInfo(data);
        updateHeroState();
        showMsg('Solicitud cargada correctamente');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    } 

    function renderStudentQR(plainToken) {
      const qrCanvas = document.getElementById('qrCanvas');
      const qrPlainToken = document.getElementById('qrPlainToken');
      if (!qrCanvas || !qrPlainToken) return;

      qrCanvas.innerHTML = '';
      qrPlainToken.textContent = plainToken || 'Genera tu código';

      if (!plainToken) return;

      new QRCode(qrCanvas, {
        text: plainToken,
        width: 190,
        height: 190,
        correctLevel: QRCode.CorrectLevel.M
      });
    }

    function renderPassInfo(data) {
      const box = document.getElementById('passInfo');
      const statusBadge = document.getElementById('qrStatusBadge');
      if (!box || !statusBadge) return;

      if (!data) {
        box.innerHTML = renderEmptyState(
          'Todavía no hay información del pase',
          'Cuando tu solicitud exista, podrás consultar o refrescar tu credencial viva.'
        );
        statusBadge.className = 'chip chip-neutral';
        statusBadge.textContent = 'Sin sesión';
        renderStudentQR('');
        updateHeroState();
        syncRegistrationLock();
        return;
      }

      const request = data.request || {};
      const event = data.event || {};
      const student = data.student || {};
      const session = data.pass_session || data.active_session || null;

      box.innerHTML = `
        <div class="info-card">
          <div class="info-head">
            <div>
              <div class="info-title">${escapeHTML(student.full_name || 'Alumno')}</div>
              <div class="info-sub">Matrícula: ${escapeHTML(student.enrolment_number || '—')}</div>
            </div>
            <div>${renderRequestStatus(request.status)}</div>
          </div>

          <div class="meta-grid">
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

      if (session) {
        statusBadge.className = 'chip chip-green';
        statusBadge.textContent = 'QR activo';
      } else {
        statusBadge.className = 'chip chip-neutral';
        statusBadge.textContent = 'Sin sesión';
      }

      renderStudentQR(currentToken);
      updateHeroState();
      syncRegistrationLock();
    }

    async function loadStudentPass() {
      try {
        const enrolment = getEnrolment();
        if (!enrolment) return showMsg('Primero escribe tu matrícula', false);

        const season = getSeason();
        const data = await tryGet([
          `/api/student/pass?enrolment_number=${encodeURIComponent(enrolment)}&season=${encodeURIComponent(season)}`,
          `/api/student/pass?enrolment_number=${encodeURIComponent(enrolment)}&temporada=${encodeURIComponent(season)}`
        ]);

        currentPass = data;
        renderPassInfo(data);
        updateHeroState();
        goToSectionAndStep('passSection', 3);
        showMsg('Estado del pase cargado correctamente');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    async function refreshStudentPass() {
      try {
        const enrolment = getEnrolment();
        if (!enrolment) return showMsg('Primero escribe tu matrícula', false);

        const payload = {
          enrolment_number: enrolment,
          season: getSeason(),
          temporada: getSeason()
        };

        const data = await postJSON('/api/student/pass/refresh', payload);

        currentPass = data;
        renderPassInfo(data);
        setCurrentStep(3);
        updateHeroState();
        showMsg(data.message || 'Credencial actualizada');
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    function renderPreview(data) {
      const box = document.getElementById('registrationPreview');
      if (!box) return;

      if (!data) {
        box.innerHTML = renderEmptyState(
          'Todavía no hay preview',
          'Escribe el token del proyecto y usa “Ver preview” para revisar antes de confirmar.'
        );
        return;
      }

      const student = data.student || {};
      const event = data.event || {};
      const project = data.project || {};
      const token = data.token || {};

      box.innerHTML = `
        <div class="info-card">
          <div class="info-head">
            <div>
              <div class="info-title">Preview válido</div>
              <div class="info-sub">Revisa cuidadosamente antes de confirmar</div>
            </div>
            <div><span class="chip chip-green">PREVIEW OK</span></div>
          </div>

          <div class="meta-grid">
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
      if (!box || !btn) return;

      if (!data) {
        box.classList.add('hidden');
        box.innerHTML = '';
        btn.disabled = false;
        updateHeroState();
        syncRegistrationLock();
        return;
      }

      btn.disabled = true;
      box.classList.remove('hidden');
      box.innerHTML = `
        <div class="success-card">
          <div class="success-title">🎉 Inscripción completada</div>
          <div class="meta-grid">
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
      updateHeroState();
      syncRegistrationLock();
    }

    async function previewRegistration() {
      try {
        const enrolment = getEnrolment();
        const projectId = document.getElementById('selectedProjectId').value.trim();
        const tokenValue = document.getElementById('projectTokenInput').value.trim();

        if (!enrolment) return showMsg('Primero escribe tu matrícula', false);
        if (!projectId) return showMsg('Primero elige un proyecto', false);
        if (!tokenValue) return showMsg('Falta el token del proyecto', false);

        if (!canStudentRegister) {
          return showMsg('Aún no tienes acceso habilitado. Primero muestra tu QR al staff.', false);
        }

        const payload = {
          enrolment_number: enrolment,
          season: getSeason(),
          temporada: getSeason(),
          project_id: Number(projectId),
          token_value: tokenValue
        };

        const data = await tryPost([
          { url: '/api/student/registration/preview', body: payload },
          { url: '/api/student_registration/preview', body: payload }
        ]);

        currentPreview = data;
        renderPreview(data);
        setCurrentStep(4);
        updateHeroState();
        showMsg(data.message || 'Preview válido');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
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

        if (!canStudentRegister) {
          return showMsg('Aún no tienes acceso habilitado. Primero muestra tu QR al staff.', false);
        }

        const payload = {
          enrolment_number: enrolment,
          season: getSeason(),
          temporada: getSeason(),
          project_id: Number(projectId),
          token_value: tokenValue,
          accepted_checkbox: acceptedCheckbox,
          accepted_full_name: acceptedFullName,
          legal_text_version: legalVersion
        };

        const data = await tryPost([
          { url: '/api/student/registration/confirm', body: payload },
          { url: '/api/student_registration/confirm', body: payload }
        ]);

        currentRegistration = {
          project_name: data.registration?.project_name || currentSelectedProject?.name || '—',
          general_name: data.registration?.general_name || currentSelectedProject?.general_name || '—',
          token_value: data.registration?.token_value || tokenValue,
          accepted_at: data.registration?.accepted_at || new Date().toLocaleString(),
          season: getSeason()
        };

        renderRegistrationSuccess(currentRegistration);
        setCurrentStep(5);
        updateHeroState();
        showMsg(data.message || 'Registro completado');
        showStudentSection('statusSection');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    document.addEventListener('DOMContentLoaded', async () => {
      try {
        document.getElementById('seasonSelector')?.addEventListener('change', async () => {
          await loadCatalogsForSeason();
          await loadCatalog();
        });

        document.getElementById('catalogSearch')?.addEventListener('input', scheduleCatalogSearch);
        document.getElementById('filterPartner')?.addEventListener('change', loadCatalog);
        document.getElementById('filterModality')?.addEventListener('change', loadCatalog);
        document.getElementById('filterWeekDays')?.addEventListener('change', loadCatalog);
        document.getElementById('filterSchedule')?.addEventListener('change', loadCatalog);

        await loadCatalogsForSeason();
        await loadCatalog();

        renderSelectedProjectBanner();
        renderRequestInfo(null);
        renderPassInfo(null);
        renderPreview(null);
        renderRegistrationSuccess(null);
        setCurrentStep(1);
        updateHeroState();
        syncRegistrationLock();
        showStudentSection('catalogSection');
      } catch (e) {
        console.error('Error al inicializar alumno:', e);
        showMsg('Error al inicializar la página: ' + e.message, false);
      }
    });
  </script>
</body>
</html>
"""