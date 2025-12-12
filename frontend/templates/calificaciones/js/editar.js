document.addEventListener("DOMContentLoaded", function() {
  const formEditar = document.getElementById("formEditar");
  const idCalificacion = document.getElementById("id_cal").value;

  formEditar.addEventListener("submit", function(e) {
    e.preventDefault();  // Prevenir que el formulario se envíe de forma tradicional

    const rut = document.getElementById("rut").value;
    const tipoCalificacion = document.getElementById("tipoSelect").value;
    const instrumento = document.getElementById("instrumento").value;
    const periodo = document.getElementById("periodo").value;
    const monto = document.getElementById("monto").value;
    const fecha = document.getElementById("fecha").value;
    const fechaVenc = document.getElementById("fecha_venc").value;
    const estado = document.getElementById("estado").value;
    const observaciones = document.getElementById("observaciones").value;
    const vigente = document.getElementById("vigente").value;

    // Preparar los datos a enviar
    const data = {
      rut_contribuyente: rut,
      codigo_tipo_calificacion: tipoCalificacion,
      instrumento: instrumento,
      periodo: periodo,
      monto_anual: monto,
      fecha_calificacion: fecha,
      fecha_vencimiento: fechaVenc,
      estado: estado,
      observaciones: observaciones,
      vigente: vigente
    };

    // Enviar los datos con AJAX
    fetch(`/api/calificaciones/${idCalificacion}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      if (data.id_calificacion) {
        // Si la calificación fue actualizada correctamente, redirigir a listado
        window.location.href = "{% url 'frontend:calificacion_list' %}";
      } else {
        alert("Hubo un error al editar la calificación.");
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
});
