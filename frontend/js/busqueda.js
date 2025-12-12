// busqueda.js
const SEARCH_API = "/api/calificaciones/buscar/"; // endpoint avanzado
// fallback: const SEARCH_API_FALLBACK = "/api/calificaciones/?search=";

async function buscar(page = 1) {
  const token = localStorage.getItem('access');
  if (!token) return window.location.href = "/frontend/login.html";

  const rut = document.getElementById('q_rut').value.trim();
  const tipo = document.getElementById('q_tipo').value.trim();
  const estado = document.getElementById('q_estado').value.trim();
  const fecha_from = document.getElementById('q_fecha_from').value;
  const fecha_to = document.getElementById('q_fecha_to').value;
  const page_size = 20;

  const params = new URLSearchParams();
  if (rut) params.append('rut', rut);
  if (tipo) params.append('tipo', tipo);
  if (estado) params.append('estado', estado);
  if (fecha_from) params.append('fecha_from', fecha_from);
  if (fecha_to) params.append('fecha_to', fecha_to);
  params.append('page', page);
  params.append('page_size', page_size);

  const url = SEARCH_API + '?' + params.toString();

  const r = await fetch(url, { headers: { "Authorization": `Bearer ${token}` }});

  if (r.status === 401) {
    await autoRefreshToken();
    return buscar(page);
  }

  if (!r.ok) {
    const txt = await r.text();
    document.getElementById('results_table').innerText = 'Error: ' + txt;
    return;
  }

  const data = await r.json();
  renderResults(data);
}

function renderResults(data) {
  const results = data.results || [];
  document.getElementById('results_count').innerText = `Resultados: ${data.count || results.length}`;
  const tableDiv = document.getElementById('results_table');
  if (!results.length) {
    tableDiv.innerHTML = '<div>No se encontraron resultados</div>';
    document.getElementById('results_pagination').innerHTML = '';
    return;
  }

  let html = '<table class="table"><thead><tr>';
  html += '<th>ID</th><th>RUT</th><th>Razón Social</th><th>Tipo</th><th>Instrumento</th><th>Fecha</th><th>Estado</th><th>Acciones</th>';
  html += '</tr></thead><tbody>';

  for (const c of results) {
    const rut = c.rut_contribuyente ? c.rut_contribuyente.rut : '';
    const razon = c.rut_contribuyente ? c.rut_contribuyente.razon_social : '';
    const tipoCod = c.codigo_tipo_calificacion ? c.codigo_tipo_calificacion.codigo : '';
    html += `<tr>
      <td>${c.id_calificacion}</td>
      <td>${rut}</td>
      <td>${razon}</td>
      <td>${tipoCod}</td>
      <td>${c.instrumento || ''}</td>
      <td>${c.fecha_calificacion || ''}</td>
      <td>${c.estado || ''}</td>
      <td>
        <a href="/frontend/calificaciones/editar.html?id=${c.id_calificacion}" class="btn small">Editar</a>
        <a href="/frontend/calificaciones/eliminar.html?id=${c.id_calificacion}" class="btn small" style="background:#e74c3c">Eliminar</a>
      </td>
    </tr>`;
  }

  html += '</tbody></table>';
  tableDiv.innerHTML = html;

  // pagination controls
  const pgDiv = document.getElementById('results_pagination');
  pgDiv.innerHTML = '';
  const page = data.page || 1;
  const page_size = data.page_size || results.length;
  const total = data.count || results.length;
  const totalPages = Math.ceil(total / page_size);

  if (totalPages > 1) {
    const prev = document.createElement('button');
    prev.className = 'btn ghost';
    prev.textContent = '← Anterior';
    prev.disabled = page <= 1;
    prev.onclick = () => buscar(page - 1);
    pgDiv.appendChild(prev);

    const info = document.createElement('span');
    info.style.margin = '0 12px';
    info.textContent = `Página ${page} de ${totalPages}`;
    pgDiv.appendChild(info);

    const next = document.createElement('button');
    next.className = 'btn ghost';
    next.textContent = 'Siguiente →';
    next.disabled = page >= totalPages;
    next.onclick = () => buscar(page + 1);
    pgDiv.appendChild(next);
  }
}

function resetForm() {
  document.getElementById('q_rut').value = '';
  document.getElementById('q_tipo').value = '';
  document.getElementById('q_estado').value = '';
  document.getElementById('q_fecha_from').value = '';
  document.getElementById('q_fecha_to').value = '';
  document.getElementById('results_table').innerHTML = '';
  document.getElementById('results_pagination').innerHTML = '';
  document.getElementById('results_count').innerText = 'Resultados: 0';
}

document.addEventListener('DOMContentLoaded', () => {
  // optionally auto search on load
  // buscar();
});
