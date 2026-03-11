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
      <span class="small">— ADMIN crea proyectos y abre cupos; STAFF solo genera códigos de acceso</span>
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
        <h3>Acceso</h3>
        <div class="small">Escribe tu clave, se valida con <code>/api/admin/ping</code> y se guarda en este navegador.</div>

        <label>KEY</label>
        <input id="adminKey" type="password" placeholder="Clave ADMIN o STAFF">

        <div class="actions">
          <button onclick="validateAndSaveKey()">Validar y guardar</button>
          <button class="btn2" onclick="clearKey()">Borrar</button>
        </div>

        <div class="hr"></div>
        <div class="small" id="roleBadge">Rol: —</div>
      </div>

      <!-- STAFF y ADMIN -->
      <div class="card" id="accessCodeCard" style="display:none;">
        <h3>Generar código de acceso (para entrar al catálogo)</h3>

        <label>Email del jugador (debe existir en users)</label>
        <input id="access_email" placeholder="ej: jugador@correo.com">

        <label>Duración (horas)</label>
        <input id="access_hours" type="number" min="1" max="168" value="72">

        <div class="actions">
          <button onclick="createAccessCode()">Generar</button>
          <button class="btn2" onclick="resetAccess()">Limpiar</button>
        </div>

        <div class="small">El código se entrega en el stand. En BD se guarda hasheado (no en claro).</div>
        <div class="hr"></div>
        <div class="small"><strong>Último código generado:</strong> <span id="last_code">—</span></div>
        <div class="small"><strong>Expira:</strong> <span id="last_exp">—</span></div>
      </div>

      <!-- SOLO ADMIN -->
      <div class="card" id="createProjectCard" style="display:none;">
        <h3>Crear proyecto (solo ADMIN)</h3>

        <label>Nombre del proyecto</label>
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

        <label>Cupo (slots)</label>
        <input id="slots" type="number" min="0" value="0">

        <label>Descripción de horario</label>
        <input id="schedule_description" placeholder="Ej: 3 días, 9-12, etc.">

        <label>Descripción del proyecto</label>
        <textarea id="project_description" placeholder="Ej: Stand A1. Buscamos 2 defensas..."></textarea>

        <label>Nombre del equipo (dueños)</label>
        <input id="team_owners" placeholder="Ej: Dueños / responsables">

        <label>Posiciones</label>
        <textarea id="carreers" placeholder="Ej: 1 portero, 2 defensas, 1 delantero"></textarea>

        <label>Objetivos</label>
        <textarea id="objectives" placeholder="Objetivos del equipo/proyecto"></textarea>

        <label>Actividades a realizar</label>
        <textarea id="activities" placeholder="Actividades que realizarán"></textarea>

        <label>Clave (informativa del proyecto)</label>
        <input id="clave" placeholder="Ej: AMPRE-100">

        <label>Competencias</label>
        <textarea id="competencies" placeholder="Competencias"></textarea>

        <label>Lugar donde se realizará</label>
        <input id="location" placeholder="Lugar">

        <label>Duración</label>
        <input id="duration" placeholder="Ej: 3 días / 8 semanas">

        <label>Público</label>
        <input id="audience" placeholder="Ej: alumnos 3°-6°">

        <label>Horas máximas a acreditar</label>
        <input id="max_hours" type="number" min="0" placeholder="Ej: 100">

        <label>Comentarios adicionales</label>
        <textarea id="comments" placeholder="Notas extra"></textarea>

        <div class="actions">
          <button onclick="createProject()">Crear</button>
          <button class="btn2" onclick="resetProjectForm()">Limpiar</button>
        </div>
      </div>

    </div>

    <!-- SOLO ADMIN (porque genera tokens/cupos) -->
    <div class="card" id="projectsCard" style="margin-top:14px; display:none;">
      <h3>Proyectos (solo ADMIN para abrir cupos)</h3>
      <div class="small">Generar tokens = abrir cupos reales (1 token = 1 cupo).</div>
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

  function getKey() { return localStorage.getItem('ADMIN_API_KEY') || ''; }
  function getRole() { return localStorage.getItem('ADMIN_ROLE') || ''; }

  function clearKey() {
    localStorage.removeItem('ADMIN_API_KEY');
    localStorage.removeItem('ADMIN_ROLE');
    document.getElementById('adminKey').value = '';
    applyRoleUI('');
    showMsg('Clave borrada');
  }

  async function validateAndSaveKey() {
    const v = document.getElementById('adminKey').value.trim();
    if (!v) return showMsg('Escribe una clave primero', false);

    try {
      const r = await fetch('/api/admin/ping', { headers: { 'X-ADMIN-KEY': v }});
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || ('Error ' + r.status));

      localStorage.setItem('ADMIN_API_KEY', v);
      localStorage.setItem('ADMIN_ROLE', data.role);

      showMsg(`Clave válida. Rol: ${data.role}`);
      applyRoleUI(data.role);

      await loadCatalogs();
      if (data.role === 'ADMIN') await loadProjects();
    } catch (e) {
      showMsg('Clave inválida: ' + e.message, false);
      localStorage.removeItem('ADMIN_API_KEY');
      localStorage.removeItem('ADMIN_ROLE');
      applyRoleUI('');
    }
  }

  function applyRoleUI(role) {
    document.getElementById('roleBadge').textContent = role ? `Rol: ${role}` : 'Rol: —';

    const access = document.getElementById('accessCodeCard');
    const create = document.getElementById('createProjectCard');
    const projCard = document.getElementById('projectsCard');

    // STAFF y ADMIN ven access codes
    access.style.display = (role === 'ADMIN' || role === 'STAFF') ? 'block' : 'none';

    // SOLO ADMIN ve crear proyecto y abrir cupos
    create.style.display = (role === 'ADMIN') ? 'block' : 'none';
    projCard.style.display = (role === 'ADMIN') ? 'block' : 'none';
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

  function fillSelect(id, items, labelKey='name') {
    const el = document.getElementById(id);
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
    fillSelect('partner_id', data.socio, 'name');
    fillSelect('modality_id', data.modalidad, 'description');
    fillSelect('week_days_id', data.dias, 'description');
    fillSelect('schedule_id', data.horario, 'description');
  }

  function resetAccess() {
    document.getElementById('access_email').value = '';
    document.getElementById('access_hours').value = 72;
  }

  async function createAccessCode() {
    try {
      const email = document.getElementById('access_email').value.trim();
      const hours = Number(document.getElementById('access_hours').value || 72);
      const res = await postJSON('/api/admin/access-codes', { email, hours });
      document.getElementById('last_code').textContent = res.code || '—';
      document.getElementById('last_exp').textContent = res.expires_at || '—';
      showMsg('Código generado');
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  function resetProjectForm() {
    ['name','partner_id','modality_id','week_days_id','schedule_id','slots',
     'schedule_description','project_description','team_owners','carreers','objectives','activities',
     'clave','competencies','location','duration','audience','max_hours','comments'
    ].forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
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
      team_owners: document.getElementById('team_owners').value.trim(),
      carreers: document.getElementById('carreers').value.trim(),
      objectives: document.getElementById('objectives').value.trim(),
      activities: document.getElementById('activities').value.trim(),
      clave: document.getElementById('clave').value.trim(),
      competencies: document.getElementById('competencies').value.trim(),
      location: document.getElementById('location').value.trim(),
      duration: document.getElementById('duration').value.trim(),
      audience: document.getElementById('audience').value.trim(),
      max_hours: document.getElementById('max_hours').value.trim(),
      comments: document.getElementById('comments').value.trim(),
    };

    if (!body.name) return showMsg('Falta nombre', false);
    if (!body.partner_id || !body.modality_id || !body.week_days_id || !body.schedule_id) {
      return showMsg('Faltan catálogos (partner/modalidad/días/horario)', false);
    }

    try {
      const res = await postJSON('/api/admin/projects', body);
      showMsg(`Proyecto creado (id=${res.id})`);
      resetProjectForm();
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

        <div class="hr"></div>

        <div class="actions">
          <input id="count-${p.id}" type="number" min="1" value="10" />
          <button onclick="genTokens(${p.id})">Generar tokens</button>
        </div>
      </div>
    `;
  }

  async function loadProjects() {
    const data = await getJSON('/api/projects');
    const root = document.getElementById('projects');
    root.innerHTML = data.length ? data.map(projectCard).join('') : '<div class="card">No hay proyectos.</div>';
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
      // Cargar key/rol guardados y adaptar UI
      document.getElementById('adminKey').value = getKey();
      applyRoleUI(getRole());

      // Si ya hay rol, carga catálogos
      if (getRole()) await loadCatalogs();
      if (getRole() === 'ADMIN') await loadProjects();
    } catch (e) {
      showMsg('Error cargando admin: ' + e.message, false);
    }
  })();
</script>
</body>
</html>
"""