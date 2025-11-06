from django.contrib import admin
from .models import (
    Usuario,
    Rol,
    Auditoria,
    ArchivoCarga,
    Instrumento,
    CalificacionTributaria,
    HistorialCalificacion,
    FactorConversion,
    CargaRegistro
)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre', 'apellido', 'correo')
    search_fields = ('nombre', 'apellido', 'correo')


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'nombre_rol', 'usuario')
    list_filter = ('nombre_rol',)
    search_fields = ('nombre_rol', 'usuario__nombre')


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('id_auditoria', 'usuario', 'accion', 'fecha', 'ip')
    list_filter = ('fecha', 'accion')
    search_fields = ('usuario__nombre', 'accion', 'ip')


@admin.register(ArchivoCarga)
class ArchivoCargaAdmin(admin.ModelAdmin):
    list_display = ('id_archivo', 'usuario', 'fecha_carga', 'estado', 'tipo_archivo')
    list_filter = ('estado', 'tipo_archivo')
    search_fields = ('usuario__nombre', 'tipo_archivo')


@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ('id_instrumento', 'nombre', 'tipo', 'inscrito')
    list_filter = ('tipo', 'inscrito')
    search_fields = ('nombre', 'tipo')


@admin.register(CalificacionTributaria)
class CalificacionTributariaAdmin(admin.ModelAdmin):
    list_display = ('id_calificacion', 'usuario', 'instrumento', 'fecha', 'tipo', 'monto', 'factor', 'estado')
    list_filter = ('tipo', 'estado', 'fecha')
    search_fields = ('usuario__nombre', 'instrumento__nombre')


@admin.register(HistorialCalificacion)
class HistorialCalificacionAdmin(admin.ModelAdmin):
    list_display = ('id_historial', 'calificacion', 'fecha_modificacion', 'observacion')
    list_filter = ('fecha_modificacion',)
    search_fields = ('calificacion__id_calificacion', 'observacion')


@admin.register(FactorConversion)
class FactorConversionAdmin(admin.ModelAdmin):
    list_display = ('id_factor', 'descripcion', 'valor')
    search_fields = ('descripcion',)


@admin.register(CargaRegistro)
class CargaRegistroAdmin(admin.ModelAdmin):
    list_display = ('id_registro', 'archivo', 'usuario', 'fecha_registro', 'descripcion')
    list_filter = ('fecha_registro',)
    search_fields = ('archivo__id_archivo', 'usuario__nombre', 'descripcion')

