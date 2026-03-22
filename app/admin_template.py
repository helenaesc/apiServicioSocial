ADMIN_HTML = r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Panel Admin</title>
  <style>
    :root{
      --bg:#f5f7fb; --card:#ffffff; --text:#0f172a; --muted:#64748b; --line:#e2e8f0;
      --brand:#0ea5e9; --dark:#0b1220; --ok:#dcfce7; --okText:#166534; --err:#fee2e2; --errText:#991b1b;
    }
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;margin:0;background:var(--bg);color:var(--text);}
    header{background:var(--dark);color:white;padding:14px 18px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;}
    header .title{display:flex;flex-direction:column;gap:2px}
    header .title strong{font-size:1.05rem;}
    header .title span{font-size:.85rem;color:#cbd5e1}
    header a{color:#e2e8f0;text-decoration:none;font-size:.9rem}
    .container{max-width:1100px;margin:16px auto;padding:0 14px;}
    .msg{display:none;margin-bottom:12px;padding:12px;border-radius:12px;font-size:.95rem}
    .msg.ok{background:var(--ok);color:var(--okText)}
    .msg.err{background:var(--err);color:var(--errText)}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:14px;}
    .card{background:var(--card);padding:14px;border-radius:14px;box-shadow:0 2px 10px rgba(2,6,23,.06);border:1px solid rgba(226,232,240,.7);}
    h3{margin:0 0 10px 0;font-size:1rem}
    .muted{color:var(--muted);font-size:.85rem;line-height:1.4}
    label{display:block;margin:10px 0 5px;color:#475569;font-size:.84rem}
    input,select,textarea,button{width:100%;box-sizing:border-box;padding:10px;border-radius:10px;border:1px solid #cbd5e1;background:white}
    textarea{min-height:82px;resize:vertical}
    .row{display:flex;gap:10px;flex-wrap:wrap}
    .row>*{flex:1;min-width:160px}
    .actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;align-items:center}
    .actions button{width:auto;padding:10px 14px;border:none;border-radius:10px;cursor:pointer}
    .btn{background:var(--brand);color:white}
    .btn2{background:#64748b;color:white}
    .btnDanger{background:#ef4444;color:white}
    .hr{height:1px;background:var(--line);margin:12px 0}
    .pill{display:inline-block;padding:3px 10px;border-radius:999px;background:#e2e8f0;color:#0f172a;font-size:.78rem}
    .projects{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px;margin-top:10px}
    .meta{font-size:.9rem;color:#475569;line-height:1.45}
    .mini{font-size:.8rem;color:var(--muted)}
    .hide{display:none !important}
    .topbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
  </style>
</head>
<body>
  <header>
    <div class="title">
      <strong>Panel Admin</strong>
      <span>ADMIN: proyectos + cupos | STAFF: códigos de acceso</span>
    </div>
    <div class="topbar">
      <a href="/">Catálogo</a>
      <a href="/health">Health</a>
    </div>
  </header>

  <div class="container">
    <div id="msg" class="msg"></div>

    <!-- Login compacto -->
    <div class="card" id="loginCard">
      <h3>Acceso</h3>
      <div class="muted">Escribe tu clave. Al validar, se activa el panel y se oculta esta sección.</div>

      <label>Clave</label>
      <input id="adminKey" type="password" placeholder="Clave ADMIN o STAFF">

      <div class="actions">
        <button class="btn" onclick="validateAndSaveKey()">Entrar</button>
        <button class="btn2" onclick="clearKey(true)">Limpiar</button>
      </div>

      <div class="hr"></div>
      <div class="muted" id="roleBadge">Rol: —</div>
    </div>

    <div class="grid" style="margin-top:14px;">

      <!-- STAFF y ADMIN -->
      <div class="card hide" id="accessCodeCard">
        <h3>Códigos de acceso (catálogo)</h3>
        <div class="muted">Se genera viendo gafete/foto + ID único. (En BD se guarda hasheado.)</div>

        <label>ID único del jugador (enrolment_number)</label>
        <input id="access_enrolment" placeholder="Ej: A01234567">

        <div class="row">
          <div>
            <label>Duración (horas)</label>
            <input id="access_hours" type="number" min="1" max="168" value="72">
          </div>
          <div>
            <label>&nbsp;</label>
            <button class="btn" onclick="createAccessCode()">Generar código</button>
          </div>
        </div>

        <div class="actions">
          <button class="btn2" onclick="resetAccess()">Limpiar</button>
          <button class="btnDanger" onclick="logout()">Cerrar sesión</button>
        </div>

        <div class="hr"></div>
        <div class="mini"><strong>Último código:</strong> <span id="last_code">—</span></div>
        <div class="mini"><strong>Expira:</strong> <span id="last_exp">—</span></div>
      </div>

      <!-- SOLO ADMIN -->
      <div class="card hide" id="createProjectCard">
        <h3>Crear proyecto (solo ADMIN)</h3>

        <div class="row">
          <div>
            <label>Nombre general</label>
            <input id="name" placeholder="Ej: Nombre del proyecto general">
          </div>
          <div>
            <label>Nombre (único)</label>
            <input id="team_owners" placeholder="Ej: Nombre del socio">
          </div>
        </div>

        <div class="row">
          <div>
            <label>Temporada / Evento</label>
            <input id="season" placeholder="Ej: Verano">
          </div>
          <div>
            <label>Cupo (slots)</label>
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

        <label>Detalle horario</label>
        <input id="schedule_description" placeholder="Ej: 3 días, 9-12, etc.">

        <!-- Carreras permitidas -->
        <label>Carreras permitidas</label>
        <select id="academy_mode" onchange="onAcademyModeChange()">
          <option value="ALL">Todas</option>
          <option value="GROUP">Por grupo</option>
          <option value="CUSTOM">Manual (selección)</option>
        </select>

        <div id="academy_group_wrap" class="hide">
          <label>Grupo</label>
          <select id="academy_group_id"><option value="">Selecciona...</option></select>
        </div>

        <div id="academy_custom_wrap" class="hide">
          <label>Academias (manual)</label>
          <select id="partner_ids" multiple size="10"></select>
          <div class="mini">Tip: Ctrl (Windows) / Cmd (Mac) para seleccionar varias.</div>
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

        <div class="row">
          <div>
            <label>Clave (informativa)</label>
            <input id="clave" placeholder="Ej: Clave a registrar en IRIS">
          </div>
          <div>
            <label>Competencias</label>
            <textarea id="competencies"></textarea>
          </div>
        </div>

        <div class="row">
          <div>
            <label>Lugar</label>
            <input id="location">
          </div>
          <div>
            <label>Duración</label>
            <input id="duration">
          </div>
        </div>

        <div class="row">
          <div>
            <label>Público</label>
            <input id="audience">
          </div>
          <div>
            <label>Horas máximas</label>
            <input id="max_hours" type="number" min="0">
          </div>
        </div>

        <label>Comentarios</label>
        <textarea id="comments"></textarea>

        <div class="actions">
          <button class="btn" onclick="createProject()">Crear</button>
          <button class="btn2" onclick="resetProjectForm()">Limpiar</button>
        </div>
      </div>

    </div>

    <!-- SOLO ADMIN -->
    <div class="card hide" id="projectsCard" style="margin-top:14px;">
      <h3>Proyectos (abrir cupos)</h3>
      <div class="muted">Generar tokens = abrir cupos reales (1 token = 1 cupo).</div>
      <div id="projects" class="projects"></div>
    </div>

  </div>

<script>
  const storage = sessionStorage;

  function showMsg(text, ok=true) {
    const el = document.getElementById('msg');
    el.className = 'msg ' + (ok ? 'ok' : 'err');
    el.textContent = text;
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 4500);
  }

  function getKey() { return storage.getItem('ADMIN_API_KEY') || ''; }
  function getRole() { return storage.getItem('ADMIN_ROLE') || ''; }

  function applyRoleUI(role) {
    document.getElementById('roleBadge').textContent = role ? `Rol: ${role}` : 'Rol: —';

    const loginCard = document.getElementById('loginCard');
    const access = document.getElementById('accessCodeCard');
    const create = document.getElementById('createProjectCard');
    const projCard = document.getElementById('projectsCard');

    const logged = (role === 'ADMIN' || role === 'STAFF');
    loginCard.classList.toggle('hide', logged);

    access.classList.toggle('hide', !(role === 'ADMIN' || role === 'STAFF'));
    create.classList.toggle('hide', !(role === 'ADMIN'));
    projCard.classList.toggle('hide', !(role === 'ADMIN'));
  }

  async function validateAndSaveKey() {
    const v = document.getElementById('adminKey').value.trim();
    if (!v) return showMsg('Escribe una clave primero', false);

    try {
      const r = await fetch('/api/admin/ping', { headers: { 'X-ADMIN-KEY': v }});
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || ('Error ' + r.status));

      storage.setItem('ADMIN_API_KEY', v);
      storage.setItem('ADMIN_ROLE', data.role);
      applyRoleUI(data.role);

      await loadCatalogs();
      if (data.role === 'ADMIN') await loadProjects();
      onAcademyModeChange();

      showMsg(`Sesión activa (${data.role})`);
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
    if (show) showMsg('Sesión borrada');
  }

  function logout(){ clearKey(true); resetAccess(); }

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
      headers: { 'Content-Type': 'application/json', 'X-ADMIN-KEY': key },
      body: JSON.stringify(bodyObj)
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  function fillSelect(id, items) {
    const el = document.getElementById(id);
    el.innerHTML = '<option value="">Selecciona...</option>';
    for (const item of items || []) {
      const opt = document.createElement('option');
      opt.value = item.id;
      opt.textContent = item.name || item.description || ('ID ' + item.id);
      el.appendChild(opt);
    }
  }

  async function loadCatalogs() {
    const data = await getJSON('/api/catalogs');

    fillSelect('modality_id', data.modalidad || data.modality);
    fillSelect('week_days_id', data.dias || data.week_days);
    fillSelect('schedule_id', data.horario || data.schedule);

    fillSelect('academy_group_id', data.partner_group || []);

    const academias = (data.socio || data.partner || []);
    const ms = document.getElementById('partner_ids');
    ms.innerHTML = '';
    for (const a of academias) {
      const opt = document.createElement('option');
      opt.value = a.id;
      opt.textContent = a.name;
      ms.appendChild(opt);
    }
  }

  function onAcademyModeChange(){
    const mode = document.getElementById('academy_mode').value;
    document.getElementById('academy_group_wrap').classList.toggle('hide', mode !== 'GROUP');
    document.getElementById('academy_custom_wrap').classList.toggle('hide', mode !== 'CUSTOM');
  }

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
      if (!enrolment_number) return showMsg('Falta ID único', false);

      const res = await postJSON('/api/admin/access-codes', { enrolment_number, hours });
      document.getElementById('last_code').textContent = res.code || '—';
      document.getElementById('last_exp').textContent = res.expires_at || '—';
      showMsg('Código generado');
    } catch (e) { showMsg(e.message, false); }
  }

  function resetProjectForm() {
    ['name','team_owners','season','slots','schedule_description','modality_id','week_days_id','schedule_id',
     'academy_mode','academy_group_id','objectives','activities','clave','competencies','location','duration','audience','max_hours','comments'
    ].forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      if (el.tagName === 'SELECT') el.value = '';
      else if (id === 'slots') el.value = 0;
      else el.value = '';
    });
    const ms = document.getElementById('partner_ids');
    if (ms) Array.from(ms.options).forEach(o => o.selected = false);
    onAcademyModeChange();
  }

  async function createProject() {
    const academy_mode = document.getElementById('academy_mode').value;
    const academy_group_id = document.getElementById('academy_group_id').value ? Number(document.getElementById('academy_group_id').value) : null;
    const partner_ids = Array.from(document.getElementById('partner_ids').selectedOptions).map(o => Number(o.value));

    if (academy_mode === 'GROUP' && !academy_group_id) return showMsg('Selecciona un grupo', false);
    if (academy_mode === 'CUSTOM' && partner_ids.length === 0) return showMsg('Selecciona al menos 1 academia manual', false);

    const body = {
      name: document.getElementById('name').value.trim(),
      team_owners: document.getElementById('team_owners').value.trim(),
      season: document.getElementById('season').value.trim(),

      modality_id: Number(document.getElementById('modality_id').value),
      week_days_id: Number(document.getElementById('week_days_id').value),
      schedule_id: Number(document.getElementById('schedule_id').value),

      slots: Number(document.getElementById('slots').value),
      schedule_description: document.getElementById('schedule_description').value.trim(),

      academy_mode,
      academy_group_id,
      partner_ids,

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

    if (!body.name) return showMsg('Falta nombre general', false);
    if (!body.team_owners) return showMsg('Falta nombre del equipo', false);
    if (!body.modality_id || !body.week_days_id || !body.schedule_id) {
      return showMsg('Faltan catálogos (modalidad/días/horario)', false);
    }

    try {
      const res = await postJSON('/api/admin/projects', body);
      showMsg(`Proyecto creado (id=${res.id})`);
      resetProjectForm();
      await loadProjects();
    } catch (e) { showMsg(e.message, false); }
  }

  function projectCard(p) {
    const disp = (p.cupos_disponibles ?? 0);
    const pill = disp > 0 ? '<span class="pill">Disponible</span>' : '<span class="pill">Sin cupo</span>';
    return `
      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;">
          <div>
            <div style="font-weight:700;">${p.name} <span class="mini">(${p.team_owners || ''})</span></div>
            <div class="meta">
              ${p.season ? `<div><strong>Temporada:</strong> ${p.season}</div>` : ''}
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
          <button class="btn" onclick="genTokens(${p.id})">Generar tokens</button>
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
    } catch (e) { showMsg(e.message, false); }
  }

  (async () => {
    try {
      document.getElementById('adminKey').value = getKey();
      applyRoleUI(getRole());
      if (getRole()) {
        await loadCatalogs();
        if (getRole() === 'ADMIN') await loadProjects();
        onAcademyModeChange();
      }
    } catch (e) {
      showMsg('Error cargando panel: ' + e.message, false);
    }
  })();
</script>
</body>
</html>
"""