// carga.js
const UPLOAD_API = "/api/cargas/upload/";
const LIST_API = "/api/cargas/";

async function fetchHistorial() {
  const token = localStorage.getItem('access');
  const r = await fetch(LIST_API, { headers: { "Authorization": `Bearer ${token}` }});
  const data = await r.json();
  const container = document.getElementById('historial');
  if (!Array.isArray(data)) {
    // if paginated
    const list = data.results || [];
    renderHistorial(list);
    return;
  }
  renderHistorial(data);
}

function renderHistorial(list) {
  if (!list.length) {
    document.getElementById('historial').innerHTML = '<div>No hay cargas</div>';
    return;
  }
  let html = '<table class="table"><thead><tr><th>ID</th><th>Archivo</th><th>Usuario</th><th>Fecha</th><th>Estado</th><th>Procesados</th><th>Rechazados</th><th>Acciones</th></tr></thead><tbody>';
  for (const c of list) {
    html += `<tr>
      <td>${c.id}</td>
      <td>${c.nombre_original || c.archivo}</td>
      <td>${c.usuario || ''}</td>
      <td>${c.fecha_carga || ''}</td>
      <td>${c.estado || ''}</td>
      <td>${c.procesados || 0}</td>
      <td>${c.rechazados || 0}</td>
      <td>
        <a class="btn small" href="/api/cargas/${c.id}/download/">Descargar</a>
        <button class="btn small ghost" onclick="eliminarCarga(${c.id})">Eliminar</button>
      </td>
    </tr>`;
  }
  html += '</tbody></table>';
  document.getElementById('historial').innerHTML = html;
}

async function eliminarCarga(id) {
  if (!confirm('Eliminar esta carga?')) return;
  const token = localStorage.getItem('access');
  const r = await fetch(`/api/cargas/${id}/`, { method: 'DELETE', headers: { "Authorization": `Bearer ${token}` }});
  if (r.ok) {
    alert('Eliminado');
    fetchHistorial();
  } else {
    alert('Error eliminando');
  }
}

document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById('archivo');
  if (!fileInput.files.length) return alert('Selecciona un archivo');
  const fd = new FormData();
  fd.append('archivo', fileInput.files[0]);
  fd.append('tipo', document.getElementById('tipo').value);

  const token = localStorage.getItem('access');
  const r = await fetch(UPLOAD_API, {
    method: 'POST',
    headers: { "Authorization": `Bearer ${token}` },
    body: fd
  });

  const data = await r.json();
  if (r.ok) {
    alert('Archivo subido. Será procesado en breve.');
    fetchHistorial();
  } else {
    alert('Error subiendo: ' + (data.detail || JSON.stringify(data)));
  }
});

document.addEventListener('DOMContentLoaded', fetchHistorial);
