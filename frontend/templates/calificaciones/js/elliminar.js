// eliminar.js
const API_CAL = "/api/calificaciones/";

function getQueryParam(name) {
  const params = new URLSearchParams(window.location.search);
  return params.get(name);
}

async function loadInfo(id) {
  const token = localStorage.getItem('access');
  const r = await fetch(API_CAL + id + '/', { headers: { "Authorization": `Bearer ${token}` }});
  if (!r.ok) {
    document.getElementById('mensaje').innerText = 'No se pudo cargar la calificación';
    document.getElementById('confirmBtn').disabled = true;
    return;
  }
  const c = await r.json();
  document.getElementById('mensaje').innerText = `¿Deseas eliminar la calificación #${c.id_calificacion} para RUT ${c.rut_contribuyente ? c.rut_contribuyente.rut : ''}?`;
}

document.getElementById('confirmBtn').addEventListener('click', async () => {
  const id = getQueryParam('id');
  const token = localStorage.getItem('access');
  const r = await fetch(API_CAL + id + '/', {
    method: 'DELETE',
    headers: { "Authorization": `Bearer ${token}` }
  });

  if (r.ok || r.status === 204) {
    alert('Calificación eliminada');
    window.location.href = 'listado.html';
  } else {
    const err = await r.json().catch(()=>({detail:'error'}));
    alert('Error eliminando: ' + (err.detail || JSON.stringify(err)));
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const id = getQueryParam('id');
  if (!id) {
    alert('ID no especificado'); window.location.href = 'listado.html';
    return;
  }
  loadInfo(id);
});
