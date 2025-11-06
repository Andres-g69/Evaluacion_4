from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_rol


class Auditoria(models.Model):
    id_auditoria = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.usuario} - {self.accion}"


class ArchivoCarga(models.Model):
    id_archivo = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)
    tipo_archivo = models.CharField(max_length=100)

    def __str__(self):
        return f"Archivo {self.id_archivo} - {self.tipo_archivo}"


class Instrumento(models.Model):
    id_instrumento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    inscrito = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class FactorConversion(models.Model):
    id_factor = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    valor = models.FloatField()

    def __str__(self):
        return self.descripcion


class CalificacionTributaria(models.Model):
    id_calificacion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    fecha = models.DateField()
    tipo = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    factor = models.ForeignKey(FactorConversion, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"Calificación {self.id_calificacion} - {self.tipo}"


class HistorialCalificacion(models.Model):
    id_historial = models.AutoField(primary_key=True)
    calificacion = models.ForeignKey(CalificacionTributaria, on_delete=models.CASCADE)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    observacion = models.TextField()

    def __str__(self):
        return f"Historial {self.id_historial}"


class CargaRegistro(models.Model):
    id_registro = models.AutoField(primary_key=True)
    archivo = models.ForeignKey(ArchivoCarga, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f"Registro {self.id_registro}"


# Create your models here.
