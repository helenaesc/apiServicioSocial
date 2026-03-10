INDEX_HTML = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Catálogo de Proyectos</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f5f7fb; color: #1f2937; }
    header { background: #0f172a; color: white; padding: 16px 20px; }
    .container { max-width: 1100px; margin: 20px auto; padding: 0 16px; }
    .filters { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; background: white; padding: 14px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,.05); }
    input, select, button { padding: 10px; border-radius: 8px; border: 1px solid #cbd5e1; }
    button { background: #0ea5e9; color: white; border: none; cursor: pointer; }
    button:hover { opacity: .95; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 14px; margin-top: 16px; }
    .card { background: white; padding: 14px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,.05); }
    .title { font-size: 1.05rem; font-weight: 700; margin-bottom: 6px; }
    .meta { font-size: .9rem; color: #475569; line-height: 1.45; }
    .desc { font-size: .92rem; margin-top: 8px; color: #334155; }
    .pill { display: inline-block; margin-top: 8px; background: #e2e8f0; color: #0f172a; padding: 3px 8px; border-radius: 999px; font-size: .8rem; }
    .empty { padding: 20px; background: white; border-radius: 12px; margin-top: 16px; }
    .footer { color: #64748b; font-size: .8rem; margin-top: 20px; }
    .row { display:flex; gap:8px; align-items:center; flex-wrap: wrap; }
  </style>
</head>
<body>
  <header>
    <h2 style="margin:0;">Catálogo de Proyectos (Poncho)</h2>
  </header>

  <div class="container">
    <div class="filters">
      <input id="q" placeholder="Buscar por proyecto o descripción">
      <select id="socio"><option value="">Socio (todos)</option></select>
      <select id="modalidad"><option value="">Modalidad (todas)</option></select>
      <select id="dia"><option value="">Día (todos)</option></select>
      <select id="horario"><option value="">Horario (todos)</option></select>
      <div class="row">
        <button onclick="loadProjects()">Buscar</button>
        <button onclick="clearFilters()" style="background:#64748b;">Limpiar</button>
      </div>
    </div>

    <div id="results"></div>
    <div class="footer">Este catálogo consume <code>/api/projects</code> y catálogos de apoyo desde <code>/api/catalogs</code>.</div>
  </div>

  <script>
    async function getJSON(url) {
      const r = await fetch(url);
      if (!r.ok) throw new Error('Error ' + r.status);
      return r.json();
    }

    function fillSelect(id, items, labelKey='description') {
      const el = document.getElementById(id);
      const first = el.innerHTML;
      el.innerHTML = first;
      for (const item of items) {
        const opt = document.createElement('option');
        opt.value = item.id;
        opt.textContent = item[labelKey];
        el.appendChild(opt);
      }
    }

    async function loadCatalogs() {
      const data = await getJSON('/api/catalogs');
      fillSelect('socio', data.socio, 'name');
      fillSelect('modalidad', data.modalidad);
      fillSelect('dia', data.dias);
      fillSelect('horario', data.horario);
    }

    function card(p) {
      const desc = p.descripcion || '';
      const dh = p.descripcion_horario ? <div class="desc"><strong>Detalle horario:</strong> ${p.descripcion_horario}</div> : '';
      return `
        <div class="card">
          <div class="title">${p.name}</div>
          <div class="meta">
            <div><strong>Socio:</strong> ${p.socio}</div>
            <div><strong>Modalidad:</strong> ${p.modalidad}</div>
            <div><strong>Día:</strong> ${p.dia}</div>
            <div><strong>Horario:</strong> ${p.horario}</div>
            <div><strong>Cupos:</strong> ${p.cupos} | <strong>Inscritos:</strong> ${p.inscritos} | <strong>Disponibles:</strong> ${p.cupos_disponibles}</div>
          </div>
          ${desc ? <div class="desc">${desc}</div> : ''}
          ${dh}
          ${p.cupos_disponibles > 0 ? '<span class="pill">Disponible</span>' : '<span class="pill">Sin cupo</span>'}
        </div>`;
    }

    async function loadProjects() {
      const params = new URLSearchParams();
      for (const id of ['q','socio','modalidad','dia','horario']) {
        const v = document.getElementById(id).value.trim();
        if (v) params.set(id, v);
      }
      const data = await getJSON('/api/projects?' + params.toString());
      const root = document.getElementById('results');
      if (!data.length) {
        root.innerHTML = '<div class="empty">No se encontraron proyectos con esos filtros.</div>';
        return;
      }
      root.innerHTML = <div class="grid">${data.map(card).join('')}</div>;
    }

    function clearFilters() {
      ['q','socio','modalidad','dia','horario'].forEach(id => document.getElementById(id).value = '');
      loadProjects();
    }

    (async () => {
      try {
        await loadCatalogs();
        await loadProjects();
      } catch (e) {
        document.getElementById('results').innerHTML = <div class="empty">Error cargando catálogo: ${e.message}</div>;
      }
    })();
  </script>
</body>
</html>
"""

ADMIN_HTML = r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Admin - Proyectos</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f5f7fb; color: #1f2937; }
    header { background: #0f172a; color: white; padding: 16px 20px; display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap;}
    header a { color:#e2e8f0; text-decoration:none; font-size:.95rem; }
    .container { max-width: 1100px; margin: 20px auto; padding: 0 16px; }
    .grid2 { display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:14px; }
    .card { background: white; padding: 14px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,.05); }
    h3 { margin: 0 0 10px 0; }
    label { font-size:.85rem; color:#475569; display:block; margin:8px 0 4px; }
    input, select, textarea, button { width:100%; box-sizing:border-box; padding: 10px; border-radius: 8px; border: 1px solid #cbd5e1; }
    textarea { min-height: 84px; resize: vertical; }
    button { background: #0ea5e9; color: white; border: none; cursor: pointer; }
    button:hover { opacity: .95; }
    .btn2 { background:#64748b; }
    .row { display:flex; gap:10px; flex-wrap:wrap; }
    .row > * { flex:1; min-width: 160px; }
    .msg { margin-bottom: 14px; padding: 12px; border-radius: 12px; display:none; }
    .msg.ok { background:#dcfce7; color:#166534; }
    .msg.err { background:#fee2e2; color:#991b1b; }
    .pill { display:inline-block; background:#e2e8f0; color:#0f172a; padding:3px 8px; border-radius:999px; font-size:.8rem; }
    .projects { display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:14px; margin-top:14px; }
    .meta { font-size:.9rem; color:#475569; line-height:1.45; }
    .small { font-size:.85rem; color:#64748b; }
    .actions { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-top:10px; }
    .actions input { width: 120px; }
    .actions button { width:auto; padding:10px 12px; }
    .hr { height:1px; background:#e2e8f0; margin:12px 0; }
    code { background:#0b1220; color:#e2e8f0; padding:2px 6px; border-radius:6px; }
  </style>
</head>
<body>
  <header>
    <div>
      <strong>Panel Admin</strong>
      <span class="small">— Crear proyectos y abrir cupos (tokens)</span>
    </div>
    <div class="row" style="max-width:420px;">
      <a href="/">Ver catálogo</a>
      <a href="/health">Health</a>
    </div>
  </header>

  <div class="container">
    <div id="msg" class="msg"></div>

    <div class="grid2">

      <div class="card">
        <h3>Clave Admin</h3>
        <div class="small">Se guarda en este navegador para no teclearla cada vez.</div>

        <label>ADMIN KEY</label>
        <input id="adminKey" type="password" placeholder="Escribe tu clave admin">

        <div class="actions">
          <button onclick="saveKey()">Guardar clave</button>
          <button class="btn2" onclick="clearKey()">Borrar clave</button>
        </div>

        <div class="hr"></div>
        <div class="small">
          Todas las llamadas admin mandan el header <code>X-ADMIN-KEY</code>.
        </div>
      </div>

      <div class="card">
        <h3>Crear proyecto</h3>

        <label>Nombre</label>
        <input id="name" placeholder="Ej: Ampre 100h">

        <div class="row">
          <div>
            <label>Partner (socio)</label>
            <select id="partner_id"><option value="">Selecciona...</option></select>
          </div>
          <div>
            <label>Modalidad</label>
            <select id="modality_id"><option value="">Selecciona...</option></select>
          </div>
        </div>

        <div class="row">
          <div>
            <label>Días</label>
            <select id="week_days_id"><option value="">Selecciona...</option></select>
          </div>
          <div>
            <label>Horario</label>
            <select id="schedule_id"><option value="">Selecciona...</option></select>
          </div>
        </div>

        <label>Cupos (slots)</label>
        <input id="slots" type="number" min="0" value="0">

        <label>Descripción de horario</label>
        <input id="schedule_description" placeholder="Ej: 3 días, 9-12, etc.">

        <label>Descripción del proyecto</label>
        <textarea id="project_description" placeholder="Ej: Stand A1. Buscamos 2 defensas..."></textarea>

        <div class="actions">
          <button onclick="createProject()">Crear</button>
          <button class="btn2" onclick="resetForm()">Limpiar</button>
        </div>

        <div class="small">Después de crear, abre cupos generando tokens.</div>
      </div>

    </div>

    <div class="card" style="margin-top:14px;">
      <h3>Proyectos</h3>
      <div class="small">Aquí puedes ver cupos disponibles (tokens no usados) y generar más tokens.</div>
      <div id="projects" class="projects"></div>
    </div>

  </div>

<script>
  function showMsg(text, ok=true) {
    const el = document.getElementById('msg');
    el.className = 'msg ' + (ok ? 'ok' : 'err');
    el.textContent = text;
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 4500);
  }

  function getKey() {
    return localStorage.getItem('ADMIN_API_KEY') || '';
  }
  function saveKey() {
    const v = document.getElementById('adminKey').value.trim();
    if (!v) return showMsg('Escribe una clave primero', false);
    localStorage.setItem('ADMIN_API_KEY', v);
    showMsg('Clave guardada');
  }
  function clearKey() {
    localStorage.removeItem('ADMIN_API_KEY');
    document.getElementById('adminKey').value = '';
    showMsg('Clave borrada');
  }

  async function getJSON(url) {
    const r = await fetch(url);
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  async function postJSON(url, bodyObj) {
    const key = getKey();
    const r = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-ADMIN-KEY': key
      },
      body: JSON.stringify(bodyObj)
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  function fillSelect(selectId, items, labelKey='name') {
    const el = document.getElementById(selectId);
    el.innerHTML = '<option value="">Selecciona...</option>';
    for (const item of items) {
      const opt = document.createElement('option');
      opt.value = item.id;
      opt.textContent = item[labelKey];
      el.appendChild(opt);
    }
  }

  async function loadCatalogs() {
    const data = await getJSON('/api/catalogs');
    // /api/catalogs devuelve llaves en español: socio/dias/modalidad/horario
    fillSelect('partner_id', data.socio, 'name');
    fillSelect('modality_id', data.modalidad, 'description');
    fillSelect('week_days_id', data.dias, 'description');
    fillSelect('schedule_id', data.horario, 'description');
  }

  function resetForm() {
    ['name','partner_id','modality_id','week_days_id','schedule_id','slots','schedule_description','project_description']
      .forEach(id => {
        const el = document.getElementById(id);
        if (el.tagName === 'SELECT') el.value = '';
        else if (id === 'slots') el.value = 0;
        else el.value = '';
      });
  }

  async function createProject() {
    const body = {
      name: document.getElementById('name').value.trim(),
      partner_id: Number(document.getElementById('partner_id').value),
      modality_id: Number(document.getElementById('modality_id').value),
      week_days_id: Number(document.getElementById('week_days_id').value),
      schedule_id: Number(document.getElementById('schedule_id').value),
      slots: Number(document.getElementById('slots').value),
      schedule_description: document.getElementById('schedule_description').value.trim(),
      project_description: document.getElementById('project_description').value.trim(),
    };

    if (!body.name) return showMsg('Falta nombre', false);
    if (!body.partner_id || !body.modality_id || !body.week_days_id || !body.schedule_id) {
      return showMsg('Faltan catálogos (partner/modalidad/días/horario)', false);
    }

    try {
      const res = await postJSON('/api/admin/projects', body);
      showMsg(`Proyecto creado (id=${res.id})`);
      resetForm();
      await loadProjects();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  function projectCard(p) {
    const disp = (p.cupos_disponibles ?? 0);
    const pill = disp > 0 ? '<span class="pill">Disponible</span>' : '<span class="pill">Sin cupo</span>';

    return `
      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;">
          <div>
            <div style="font-weight:700;">${p.name}</div>
            <div class="meta">
              <div><strong>Socio:</strong> ${p.socio}</div>
              <div><strong>Modalidad:</strong> ${p.modalidad}</div>
              <div><strong>Día:</strong> ${p.dia}</div>
              <div><strong>Horario:</strong> ${p.horario}</div>
              <div><strong>Cupos:</strong> ${p.cupos} | <strong>Inscritos:</strong> ${p.inscritos} | <strong>Disponibles:</strong> ${disp}</div>
            </div>
          </div>
          <div>${pill}</div>
        </div>

        ${(p.descripcion || '') ? `<div class="small" style="margin-top:8px;">${p.descripcion}</div>` : ''}
        ${(p.descripcion_horario || '') ? `<div class="small" style="margin-top:6px;"><strong>Horario:</strong> ${p.descripcion_horario}</div>` : ''}

        <div class="hr"></div>

        <div class="actions">
          <input id="count-${p.id}" type="number" min="1" value="10" />
          <button onclick="genTokens(${p.id})">Generar tokens</button>
        </div>
        <div class="small">Generar tokens = abrir cupos reales (1 token = 1 cupo).</div>
      </div>
    `;
  }

  async function loadProjects() {
    const data = await getJSON('/api/projects');
    const root = document.getElementById('projects');
    if (!data.length) {
      root.innerHTML = '<div class="card">No hay proyectos. Crea uno arriba.</div>';
      return;
    }
    root.innerHTML = data.map(projectCard).join('');
  }

  async function genTokens(projectId) {
    const count = Number(document.getElementById(`count-${projectId}`).value || 10);
    try {
      const res = await postJSON(`/api/admin/projects/${projectId}/tokens`, { count, length: 10 });
      showMsg(`Tokens generados: ${res.created}`);
      await loadProjects();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  (async () => {
    try {
      document.getElementById('adminKey').value = getKey();
      await loadCatalogs();
      await loadProjects();
    } catch (e) {
      showMsg('Error cargando admin: ' + e.message, false);
    }
  })();
</script>
</body>
</html>
"""