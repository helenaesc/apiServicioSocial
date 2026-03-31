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

    .top-links a {
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
      cursor: pointer;
      box-shadow: 0 10px 20px rgba(37,99,235,.18);
    }

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

    .project-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }

    .project-card {
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      background: white;
      padding: 18px;
      box-shadow: 0 6px 18px rgba(15,23,42,.05);
    }

    .project-card h3 {
      margin-bottom: 6px;
    }

    .project-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 14px;
    }

    .project-actions button {
      width: auto;
      min-width: 140px;
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

    .qr-box {
      border: 1px dashed var(--border-strong);
      border-radius: var(--radius-lg);
      background: #f8fafc;
      padding: 18px;
    }

    .preview-box {
      border: 1px solid #dbeafe;
      border-radius: var(--radius-lg);
      background: #f8fbff;
      padding: 16px;
      margin-top: 12px;
    }

    .section-divider {
      height: 1px;
      background: linear-gradient(90deg, transparent, #dbeafe, transparent);
      margin: 8px 0 18px;
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
      <strong>Registro de Proyectos</strong>
      <span>Consulta proyectos, solicita tu pase y completa tu inscripción</span>
    </div>

    <div class="top-links">
      <a href="/admin">Admin</a>
      <a href="/health">Health</a>
    </div>
  </header>

  <div class="container">
    <div id="msg" class="msg"></div>

    <div class="grid">
      <div class="card span-12">
        <h2>Temporada y catálogo</h2>
        <div class="muted">
          Primero elige una temporada para consultar el catálogo disponible. Desde aquí puedes explorar proyectos antes de solicitar tu pase.
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
        <div id="catalogList" class="project-grid"></div>
      </div>

      <div class="card span-6">
        <h2>Solicitar pase</h2>
        <div class="muted">
          El pase no te registra. Solo genera tu solicitud y te permite presentarte al evento para validación presencial.
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
        <h2>Mi solicitud</h2>
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
        <h2>Credencial viva</h2>
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

        <div class="qr-box" style="margin-top:16px;">
          <div class="small" style="margin-bottom:10px;"><strong>QR vigente del pase</strong></div>

          <div id="qrCanvasWrap" style="display:flex; justify-content:center; align-items:center; min-height:180px;">
            <div id="qrCanvas"></div>
          </div>

          <div id="qrPlainToken" class="mono" style="margin-top:12px;">Genera tu código</div>

          <div class="small" style="margin-top:12px; text-align:center;">
            Este QR cambia al refrescarse y deja de servir al expirar o cuando el staff lo usa.
          </div>
        </div>
      </div>

      <div class="card span-6">
        <h2>Cierre de inscripción</h2>
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
          <button type="button" class="btn-primary" onclick="confirmRegistration()">Confirmar inscripción</button>
        </div>

        <div id="registrationPreview" class="list">
          <div class="item">
            <div class="small">Todavía no hay preview del cierre.</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    let currentCatalog = [];
    let currentRequest = null;
    let currentPass = null;
    let currentPreview = null;
    let currentSelectedProject = null;

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

    function fillSelect(id, items, labelKey='description') {
      const el = document.getElementById(id);
      if (!el) return;

      const first = el.querySelector('option') ? el.querySelector('option').outerHTML : '<option value="">Todos</option>';
      el.innerHTML = first;

      for (const item of items || []) {
        const opt = document.createElement('option');
        opt.value = item.id;
        opt.textContent = item[labelKey];
        el.appendChild(opt);
      }
    }

    function renderCatalogHeader(projects) {
      const season = getSeason();
      const el = document.getElementById('catalogHeader');

      el.innerHTML = `
        <div class="item">
          <div class="item-head">
            <div>
              <div class="item-title">Catálogo de ${escapeHTML(season)}</div>
              <div class="small">Total de proyectos mostrados: ${projects.length}</div>
            </div>
            <div class="inline-row">
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
            <div class="small">No hay proyectos para mostrar con esos filtros.</div>
          </div>
        `;
        return;
      }

      list.innerHTML = projects.map(p => `
        <div class="project-card">
          <div class="item-head">
            <div>
              <h3>${escapeHTML(p.general_name || 'Sin nombre general')} | ${escapeHTML(p.name || 'Sin nombre')}</h3>
              <div class="small">Carrera preferida: ${escapeHTML(p.socio || p.partner_name || '—')}</div>
            </div>
            <div class="inline-row">
              <span class="pill pill-info">${escapeHTML(p.modalidad || '—')}</span>
              <span class="pill pill-neutral">${escapeHTML(p.dia || '—')}</span>
              <span class="pill pill-neutral">${escapeHTML(p.horario || '—')}</span>
            </div>
          </div>

          <div class="meta">
            <div class="meta-box">
              <span class="meta-label">Cupos disponibles</span>
              <div class="meta-value">${escapeHTML(p.cupos_disponibles ?? p.cupos ?? '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Horario</span>
              <div class="meta-value">${escapeHTML(p.descripcion_horario || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Duración</span>
              <div class="meta-value">${escapeHTML(p.duration || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Lugar</span>
              <div class="meta-value">${escapeHTML(p.location || '—')}</div>
            </div>
          </div>

          <div class="section-divider"></div>

          <div class="small"><strong>Objetivos:</strong> ${escapeHTML(p.objectives || '—')}</div>
          <div class="small" style="margin-top:8px;"><strong>Actividades:</strong> ${escapeHTML(p.activities || '—')}</div>
          <div class="small" style="margin-top:8px;"><strong>Competencias:</strong> ${escapeHTML(p.competencies || '—')}</div>
          <div class="small" style="margin-top:8px;"><strong>Comentarios:</strong> ${escapeHTML(p.comments || '—')}</div>

          <div class="project-actions">
            <button type="button" class="btn-primary" onclick="selectProject(${Number(p.id)})">Elegir proyecto</button>
          </div>
        </div>
      `).join('');
    }

    function selectProject(projectId) {
      const project = currentCatalog.find(p => Number(p.id) === Number(projectId));
      if (!project) return;

      currentSelectedProject = project;

      document.getElementById('selectedProjectId').value = String(project.id);
      document.getElementById('selectedProjectName').value = `${project.general_name || 'Sin nombre general'} | ${project.name || 'Sin nombre'}`;

      showMsg('Proyecto seleccionado para cierre de inscripción');
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

    async function loadCatalog() {
      try {
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

        const projects = await getJSON(`/api/projects?${params.toString()}`);
        currentCatalog = projects || [];

        renderCatalogHeader(currentCatalog);
        renderCatalog(currentCatalog);

        showMsg('Catálogo cargado correctamente');
      } catch (e) {
        currentCatalog = [];
        renderCatalogHeader([]);
        renderCatalog([]);
        showMsg(e.message, false);
      }
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
            <div class="inline-row">
              ${renderRequestStatus(request.status)}
            </div>
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

    function renderRequestStatus(status) {
      const value = String(status || '').toUpperCase();
      const map = {
        REQUESTED: ['pill-info', 'REQUESTED'],
        VALIDATED: ['pill-purple', 'VALIDATED'],
        ACCESS_ENABLED: ['pill-ok', 'ACCESS_ENABLED'],
        REGISTERED: ['pill-ok', 'REGISTERED'],
        CANCELLED: ['pill-err', 'CANCELLED'],
        CLOSED: ['pill-warn', 'CLOSED']
      };
      const cfg = map[value] || ['pill-neutral', value || '—'];
      return `<span class="pill ${cfg[0]}">${cfg[1]}</span>`;
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

      if (!data) {
        box.innerHTML = `<div class="item"><div class="small">Todavía no hay información del pase.</div></div>`;
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
            <div class="inline-row">
              ${renderRequestStatus(request.status)}
            </div>
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

        const plainToken = data.pass_session?.plain_token || '';
        renderStudentQR(plainToken);

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
            <div class="inline-row">
              <span class="pill pill-ok">PREVIEW OK</span>
            </div>
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

        currentPreview = null;
        renderPreview({
          student: { full_name: acceptedFullName },
          event: { display_name: getSeason() },
          project: {
            general_name: data.registration?.general_name || currentSelectedProject?.general_name || '—',
            project_name: data.registration?.project_name || currentSelectedProject?.name || '—'
          },
          token: { token_value: data.registration?.token_value || tokenValue }
        });

        showMsg(data.message || 'Registro completado');
      } catch (e) {
        showMsg(e.message, false);
      }
    }

    document.addEventListener('DOMContentLoaded', async () => {
      document.getElementById('seasonSelector').addEventListener('change', async () => {
        await loadCatalogsForSeason();
        await loadCatalog();
      });

      document.getElementById('catalogSearch').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') loadCatalog();
      });

      await loadCatalogsForSeason();
      await loadCatalog();
    });
  </script>
</body>
</html>
"""