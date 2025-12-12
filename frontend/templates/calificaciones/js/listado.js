document.addEventListener("DOMContentLoaded", function() {
  // Hacemos la solicitud a la API para obtener las calificaciones
  fetch("/api/calificaciones/")
    .then(response => response.json())
    .then(data => {
      const calificacionesList = document.getElementById("calificaciones-list");
      if (data.results.length > 0) {
        data.results.forEach(calificacion => {
          // Creamos una fila para cada calificación
          const row = document.createElement("tr");
          
          row.innerHTML = `
            <td>${calificacion.rut_contribuyente}</td>
            <td>${calificacion.instrumento}</td>
            <td>${calificacion.codigo_tipo_calificacion}</td>
            <td>${calificacion.estado}</td>
            <td>${new Date(calificacion.fecha_calificacion).toLocaleDateString()}</td>
            <td>
              <a href="/frontend/calificaciones/editar/${calificacion.id_calificacion}/" class="btn small ghost">Editar</a>
              <a href="/frontend/calificaciones/eliminar/${calificacion.id_calificacion}/" class="btn small" style="background:#e74c3c">Eliminar</a>
            </td>
          `;
          
          calificacionesList.appendChild(row);
        });
      } else {
        // Si no hay calificaciones, mostramos un mensaje
        const row = document.createElement("tr");
        row.innerHTML = `<td colspan="6" style="text-align:center;padding:18px">No hay registros.</td>`;
        calificacionesList.appendChild(row);
      }
    })
    .catch(error => console.error("Error al cargar las calificaciones:", error));
});
