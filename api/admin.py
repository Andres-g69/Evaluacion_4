from django.contrib import admin
from .models import (
    UserProfile,
    Instrumento,
    FactorConversion,
    ArchivoCarga,
    CargaError,
    CalificacionTributaria,
    HistorialCalificacion,
    Auditoria,
    CargaRegistro,
)

admin.site.register(Instrumento)
admin.site.register(FactorConversion)
admin.site.register(ArchivoCarga)
admin.site.register(CargaError)
admin.site.register(CalificacionTributaria)
admin.site.register(HistorialCalificacion)
admin.site.register(Auditoria)
admin.site.register(CargaRegistro)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("get_username", "get_email", "role", "activo")

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Usuario"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Correo"
