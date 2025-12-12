from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import os
from django.conf import settings


# -----------------------------------------------------------
#  TIPO_CALIFICACION
# -----------------------------------------------------------
class TipoCalificacion(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    monto_minimo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monto_maximo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    requisitos = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tipo_calificacion"

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


# -----------------------------------------------------------
#  CONTRIBUYENTE
# -----------------------------------------------------------
class Contribuyente(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    razon_social = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100)
    fecha_inscripcion = models.DateField(null=True, blank=True)
    tipo_contribuyente = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.CharField(max_length=50)
    usuario_actualizacion = models.CharField(max_length=50)

    class Meta:
        db_table = "contribuyente"

    def __str__(self):
        return f"{self.rut} - {self.razon_social}"


# -----------------------------------------------------------
#  CALIFICACION_TRIBUTARIA
# -----------------------------------------------------------
class CalificacionTributaria(models.Model):
    id_calificacion = models.BigAutoField(primary_key=True)

    rut_contribuyente = models.ForeignKey(
        Contribuyente,
        on_delete=models.CASCADE,
        db_column='rut_contribuyente',
        related_name='calificaciones'
    )

    codigo_tipo_calificacion = models.ForeignKey(
        TipoCalificacion,
        on_delete=models.PROTECT,
        db_column='codigo_tipo_calificacion',
        related_name='calificaciones'
    )

    fecha_calificacion = models.DateField()
    monto_anual = models.DecimalField(max_digits=12, decimal_places=2)
    periodo = models.IntegerField()
    estado = models.CharField(max_length=20)
    observaciones = models.TextField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    vigente = models.BooleanField(default=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.CharField(max_length=50)
    usuario_actualizacion = models.CharField(max_length=50)

    class Meta:
        db_table = "calificacion_tributaria"

    def __str__(self):
        return f"Calificación {self.id_calificacion} ({self.rut_contribuyente_id})"


# -----------------------------------------------------------
#  DOCUMENTO_TRIBUTARIO
# -----------------------------------------------------------
class DocumentoTributario(models.Model):
    id_documento = models.BigAutoField(primary_key=True)

    rut_contribuyente = models.ForeignKey(
        Contribuyente,
        on_delete=models.CASCADE,
        db_column='rut_contribuyente',
        related_name='documentos'
    )

    tipo_documento = models.CharField(max_length=20)
    fecha_emision = models.DateField()
    fecha_recepcion = models.DateField(null=True, blank=True)
    monto_documento = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20)
    ruta_archivo = models.CharField(max_length=500, null=True, blank=True)
    hash_archivo = models.CharField(max_length=64, null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.CharField(max_length=50)

    class Meta:
        db_table = "documento_tributario"

    def __str__(self):
        return f"Documento {self.id_documento} ({self.rut_contribuyente_id})"



# -----------------------------------------------------------
#  TIPO_DOCUMENTO
# -----------------------------------------------------------
class TipoDocumento(models.Model):
    codigo = models.CharField(max_length=20, primary_key=True)
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=10)
    requiere_validacion = models.BooleanField(default=False)
    dias_vencimiento = models.IntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "tipo_documento"

    def __str__(self):
        return self.codigo


# -----------------------------------------------------------
#  NOTIFICACION
# -----------------------------------------------------------
class Notificacion(models.Model):
    id_notificacion = models.BigAutoField(primary_key=True)

    rut_contribuyente = models.ForeignKey(
        "Contribuyente",
        on_delete=models.CASCADE,
        db_column='rut_contribuyente',
        related_name='notificaciones'
    )

    tipo_notificacion = models.CharField(max_length=50)
    destinatario = models.CharField(max_length=100)
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=20)

    fecha_envio = models.DateTimeField(null=True, blank=True)
    fecha_programada = models.DateTimeField(null=True, blank=True)
    intentos_envio = models.IntegerField(default=0)
    error_envio = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "notificacion"

    def __str__(self):
        return f"Notificación {self.id_notificacion}"


# -----------------------------------------------------------
#  USUARIO
# -----------------------------------------------------------
class Usuario(models.Model):
    id_usuario = models.CharField(max_length=50, primary_key=True)
    nombre_usuario = models.CharField(max_length=50)
    contraseña_hash = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    rol = models.CharField(max_length=20)

    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateField()
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    intento_fallidos = models.IntegerField(default=0)
    bloqueado = models.BooleanField(default=False)
    fecha_bloqueo = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "usuario"

    def __str__(self):
        return self.id_usuario


# -----------------------------------------------------------
#  AUDITORIA
# -----------------------------------------------------------
class Auditoria(models.Model):
    id_auditoria = models.BigAutoField(primary_key=True)
    tabla_afectada = models.CharField(max_length=30)
    operacion = models.CharField(max_length=20)
    usuario = models.CharField(max_length=50)
    fecha_operacion = models.DateTimeField(auto_now_add=True)

    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)

    id_sesion = models.CharField(max_length=100, null=True, blank=True)
    user_agent = models.CharField(max_length=200, null=True, blank=True)
    aplicacion_origen = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "api_auditoria"

    def __str__(self):
        return f"Auditoria {self.id_auditoria}"


# -----------------------------------------------------------
#  SESION_USUARIO
# -----------------------------------------------------------
class SesionUsuario(models.Model):
    id_sesion = models.CharField(max_length=100, primary_key=True)

    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='sesiones'
    )

    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    ip_address = models.CharField(max_length=45)
    user_agent = models.CharField(max_length=100)
    estado = models.CharField(max_length=20)
    datos_sesion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "sesion_usuario"

    def __str__(self):
        return self.id_sesion


# -----------------------------------------------------------
#  LOG_ERROR
# -----------------------------------------------------------
class LogError(models.Model):
    id_error = models.BigAutoField(primary_key=True)
    aplicacion = models.CharField(max_length=50)
    nivel_error = models.CharField(max_length=20)
    modulo = models.CharField(max_length=100)
    mensaje_error = models.TextField()
    stack_trace = models.TextField(null=True, blank=True)
    usuario = models.CharField(max_length=50, null=True, blank=True)
    fecha_error = models.DateTimeField(auto_now_add=True)
    contexto_adicional = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "log_error"

    def __str__(self):
        return f"Error {self.id_error}"


# -----------------------------------------------------------
#  PERMISO
# -----------------------------------------------------------
class Permiso(models.Model):
    codigo_permiso = models.CharField(max_length=50, primary_key=True)
    descripcion = models.CharField(max_length=100)
    modulo = models.CharField(max_length=50)
    nivel_acceso = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "permiso"

    def __str__(self):
        return self.codigo_permiso


# -----------------------------------------------------------
#  ROL_PERMISO
# -----------------------------------------------------------
class RolPermiso(models.Model):
    codigo_rol = models.CharField(max_length=20, primary_key=True)
    codigo_permiso = models.ForeignKey(
        Permiso,
        on_delete=models.CASCADE,
        db_column='codigo_permiso',
        related_name='permisos_asignados'
    )
    concedido = models.BooleanField(default=True)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rol_permiso"

    def __str__(self):
        return f"{self.codigo_rol} - {self.codigo_permiso.codigo_permiso}"


# -----------------------------------------------------------
#  PARAMETRO_SISTEMA
# -----------------------------------------------------------
class ParametroSistema(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)
    descripcion = models.CharField(max_length=100)
    valor = models.CharField(max_length=500)
    tipo_dato = models.CharField(max_length=20)
    editable = models.BooleanField(default=False)
    categoria = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "parametro_sistema"

    def __str__(self):
        return self.codigo


# -----------------------------------------------------------
#  HISTORICO_CALIFICACION
# -----------------------------------------------------------
class HistoricoCalificacion(models.Model):
    id_historico = models.BigAutoField(primary_key=True)

    id_calificacion = models.ForeignKey(
        "CalificacionTributaria",
        on_delete=models.CASCADE,
        db_column='id_calificacion',
        related_name='historicos'
    )

    rut_contribuyente = models.ForeignKey(
        "Contribuyente",
        on_delete=models.CASCADE,
        db_column='rut_contribuyente',
        related_name='historicos_calificacion'
    )

    codigo_tipo_calificacion = models.ForeignKey(
        "TipoCalificacion",
        on_delete=models.CASCADE,
        db_column='codigo_tipo_calificacion',
        related_name='historicos'
    )

    fecha_calificacion = models.DateField()
    monto_anual = models.FloatField()
    periodo = models.IntegerField()
    estado = models.CharField(max_length=20)
    observaciones = models.TextField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    vigente = models.BooleanField(default=True)

    usuario_modificacion = models.CharField(max_length=50)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    tipo_modificacion = models.CharField(max_length=20)

    class Meta:
        db_table = "historico_calificacion"

    def __str__(self):
        return f"Histórico {self.id_historico}"


# -----------------------------------------------------------
#  VALIDACION_TRIBUTARIA
# -----------------------------------------------------------
class ValidacionTributaria(models.Model):
    id_validacion = models.BigAutoField(primary_key=True)

    id_calificacion = models.ForeignKey(
        "CalificacionTributaria",
        on_delete=models.CASCADE,
        db_column='id_calificacion',
        related_name='validaciones'
    )

    rut_contribuyente = models.ForeignKey(
        "Contribuyente",
        on_delete=models.CASCADE,
        db_column='rut_contribuyente',
        related_name='validaciones'
    )

    fecha_validacion = models.DateField()
    tipo_validacion = models.CharField(max_length=20)
    resultado = models.CharField(max_length=20)
    observaciones = models.TextField(null=True, blank=True)
    monto_validado = models.FloatField(null=True, blank=True)

    usuario_validador = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "validacion_tributaria"

    def __str__(self):
        return f"Validación {self.id_validacion}"

class Poblacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = "poblacion"

    def __str__(self):
        return self.nombre


class CargaArchivo(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'PENDIENTE'),
        ('EN_PROCESO', 'EN_PROCESO'),
        ('COMPLETADO', 'COMPLETADO'),
        ('ERROR', 'ERROR'),
    )
    id = models.BigAutoField(primary_key=True)
    archivo = models.FileField(upload_to='uploads/%Y/%m/%d/')
    nombre_original = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=50, default='CALIFICACIONES')
    usuario = models.CharField(max_length=100, null=True, blank=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    detalle_error = models.TextField(null=True, blank=True)
    procesados = models.IntegerField(default=0)
    rechazados = models.IntegerField(default=0)

    class Meta:
        db_table = "carga_archivo"

    def __str__(self):
        return f"Carga {self.id} - {self.nombre_original or self.archivo.name}"

    def file_path(self):
        if not self.archivo: return None
        # ruta física
        return os.path.join(settings.MEDIA_ROOT, self.archivo.name)