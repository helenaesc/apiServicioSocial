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