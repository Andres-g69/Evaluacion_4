from .models import Auditoria
from django.utils import timezone

def registrar_auditoria(usuario, accion, request=None, detalle="Acción: Inicio de sesión", unique_per_session=False):
    """
    Registra una acción realizada por un usuario en el sistema.
    Si unique_per_session es True, actualiza el registro si existe uno similar para el mismo usuario en la sesión.
    """
    ip = None
    if request:
        ip = request.META.get("REMOTE_ADDR")
    
    if unique_per_session:
        auditoria = Auditoria.objects.filter(usuario=usuario, accion=accion).first()
        if auditoria:
            auditoria.fecha = timezone.now()
            auditoria.ip = ip
            auditoria.detalle = detalle
            auditoria.save()
            return auditoria

    # Si no existe o no se quiere actualizar, se crea una nueva
    return Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        fecha=timezone.now(),
        ip=ip,
        detalle=detalle
    )
