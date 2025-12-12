from django.contrib import admin
from . import models

@admin.register(models.Contribuyente)
class ContribuyenteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'razon_social', 'email', 'telefono', 'activo', 'fecha_creacion')
    search_fields = ('rut', 'razon_social', 'email')
    list_filter = ('activo', 'tipo_contribuyente')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_creacion',)

class CalificacionTributariaInline(admin.TabularInline):
    model = models.CalificacionTributaria
    fk_name = 'rut_contribuyente'
    extra = 0
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

@admin.register(models.TipoCalificacion)
class TipoCalificacionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'categoria', 'activo', 'monto_minimo', 'monto_maximo')
    search_fields = ('codigo', 'descripcion')

@admin.register(models.CalificacionTributaria)
class CalificacionTributariaAdmin(admin.ModelAdmin):
    list_display = ('id_calificacion', 'rut_contribuyente', 'codigo_tipo_calificacion', 'fecha_calificacion', 'monto_anual', 'vigente')
    search_fields = ('id_calificacion', 'rut_contribuyente__rut')
    list_filter = ('vigente', 'estado', 'codigo_tipo_calificacion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_calificacion',)

@admin.register(models.DocumentoTributario)
class DocumentoTributarioAdmin(admin.ModelAdmin):
    list_display = ('id_documento', 'rut_contribuyente', 'tipo_documento', 'fecha_emision', 'monto_documento')
    search_fields = ('id_documento', 'rut_contribuyente__rut')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
