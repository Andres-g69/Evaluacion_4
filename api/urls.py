from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# =============================
# ROUTER API REST PRINCIPAL
# =============================
router = DefaultRouter()
router.register(r'usuarios', views.UserProfileViewSet, basename='usuarios')
router.register(r'instrumentos', views.InstrumentoViewSet, basename='instrumentos')
router.register(r'factores', views.FactorConversionViewSet, basename='factores')
router.register(r'calificaciones', views.CalificacionTributariaViewSet, basename='calificaciones')
router.register(r'historial', views.HistorialCalificacionViewSet, basename='historial')
router.register(r'archivos', views.ArchivoCargaViewSet, basename='archivos')
router.register(r'errores', views.CargaErrorViewSet, basename='errores')
router.register(r'registros', views.CargaRegistroViewSet, basename='registros')
router.register(r'auditoria', views.AuditoriaViewSet, basename='auditoria')

# =============================
# URLS DE API + CRUD HTML
# =============================
# =============================
# URLS DE API + CRUD HTML
# =============================
urlpatterns = [
    # CRUD HTML
    path('calificaciones/html/', views.calificacion_list_view, name='calificacion_list_view'),
    path('calificaciones/html/nueva/', views.calificacion_create_view, name='calificacion_create_view'),
    path('calificaciones/html/<int:id>/editar/', views.calificacion_update_view, name='calificacion_update_view'),
    path('calificaciones/html/<int:id>/eliminar/', views.calificacion_delete_view, name='calificacion_delete_view'),

        # API REST Framework
    path('', include(router.urls)),

]
