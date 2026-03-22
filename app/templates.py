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
      --primary-dark: #1d4ed8;
      --accent: #0ea5e9;
      --success-bg: #dcfce7;
      --success-text: #166534;
      --danger-bg: #fee2e2;
      --danger-text: #991b1b;
      --shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
      --radius-xl: 22px;
      --radius-lg: 16px;
      --radius-md: 12px;
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

    .hidden {
      display: none !important;
    }

    .hero {
      position: relative;
      overflow: hidden;
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #0ea5e9 100%);
      color: white;
      padding: 40px 20px 80px;
    }

    .hero::after {
      content: "";
      position: absolute;
      inset: auto -60px -90px auto;
      width: 260px;
      height: 260px;
      background: rgba(255,255,255,.10);
      border-radius: 50%;
      filter: blur(2px);
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

    .season-screen {
      max-width: 1100px;
      margin: -44px auto 32px;
      padding: 0 16px 24px;
      position: relative;
      z-index: 2;
    }

    .season-panel {
      background: var(--panel);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255,255,255,.7);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow);
      padding: 26px;
    }

    .season-header {
      text-align: center;
      margin-bottom: 24px;
    }

    .season-header h2 {
      margin: 0 0 8px;
      font-size: 1.7rem;
      color: var(--text);
    }

    .season-header p {
      margin: 0;
      color: var(--muted);
      font-size: 1rem;
    }

    .season-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 18px;
    }

   .season-card,
.card {
  height: auto;
  overflow: hidden;
}

.season-card h3,
.season-card p,
.title,
.desc,
.meta-value,
.meta-label {
  white-space: normal;
  overflow-wrap: break-word;
  word-break: break-word;
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

    .season-card h3 {
      margin: 0 0 14px;
      font-size: 1.25rem;
      color: var(--text);
    }

    .season-card p {
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
      font-size: .95rem;
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

    input, select, button {
      height: 46px;
      border-radius: 14px;
      font-size: .95rem;
      transition: .2s ease;
    }

    input, select {
      width: 100%;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.92);
      color: var(--text);
      padding: 0 14px;
      outline: none;
    }

    input::placeholder {
      color: #94a3b8;
    }

    input:focus, select:focus {
      border-color: rgba(37, 99, 235, .5);
      box-shadow: 0 0 0 4px rgba(37, 99, 235, .10);
      background: white;
    }

    .actions {
      display: flex;
      gap: 10px;
      align-items: end;
    }

    button {
      border: none;
      padding: 0 18px;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
      color: white;
      box-shadow: 0 10px 20px rgba(37, 99, 235, .20);
    }

    .btn-primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 14px 28px rgba(37, 99, 235, .24);
    }

    .btn-secondary {
      background: #eef2f7;
      color: #334155;
      border: 1px solid #dbe3ee;
    }

    .btn-secondary:hover {
      background: #e7edf5;
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

    .card:hover {
      transform: translateY(-3px);
      box-shadow: 0 18px 35px rgba(15, 23, 42, .10);
      border-color: #d7e3f3;
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

    .desc strong {
      color: #0f172a;
    }

    .footer {
      margin-top: 22px;
      color: var(--muted);
      font-size: .85rem;
      text-align: center;
    }

    .footer code {
      background: #eef2ff;
      color: #3730a3;
      padding: 2px 8px;
      border-radius: 8px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
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

    .muted {
      color: var(--muted);
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
      .hero {
        padding: 30px 16px 74px;
      }

      .container,
      .season-screen {
        padding: 0 12px 20px;
      }

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
      <h1 id="heroTitle">Oferta Servicio Social</h1>
      <p id="heroSubtitle">
        Selecciona una temporada para consultar los proyectos disponibles.
      </p>
    </div>
  </section>

  <section id="seasonScreen" class="season-screen">
    <div class="season-panel">
      <div class="season-header">
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
          <label for="socio">Socio</label>
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

    <div class="footer">
      Este catálogo consume <code>/api/projects</code> y catálogos de apoyo desde <code>/api/catalogs</code>.
    </div>
  </main>

  <script>
    let currentSeason = null;

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

      if (currentSeason) {
        heroTitle.textContent = 'Oferta de ' + label;
        heroSubtitle.textContent = 'Explora los proyectos disponibles para la temporada seleccionada.';
        seasonChip.textContent = 'Temporada: ' + label;
        seasonChip.classList.remove('hidden');
      } else {
        heroTitle.textContent = 'Oferta de Proyectos';
        heroSubtitle.textContent = 'Selecciona una temporada para consultar los proyectos disponibles.';
        seasonChip.textContent = '';
        seasonChip.classList.add('hidden');
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

      updateSeasonUI();
    });
  </script>
</body>
</html>
"""