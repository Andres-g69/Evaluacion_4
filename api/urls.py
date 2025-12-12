from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.tipos_calificacion import TipoCalificacionViewSet
from api.views.calificaciones import CalificacionTributariaViewSet, CalificacionSearchAPIView
from api.views.cargas import CargaListView, CargaDeleteView, CargaCreateView, CargaDownloadView

app_name = "api"

router = DefaultRouter()
router.register(r'tipos-calificacion', TipoCalificacionViewSet, basename='tipos-calificacion')
router.register(r'calificaciones', CalificacionTributariaViewSet, basename='calificaciontributaria')

urlpatterns = [
    path('api/', include(router.urls)),  # Rutas de la API ahora tienen un prefijo 'api/'

    # Calificaciones: búsqueda
    path('api/calificaciones/buscar/', CalificacionSearchAPIView.as_view(), name='calificacion_search'),

    # Cargas
    path('api/cargas/', CargaListView.as_view(), name='cargas_list'),
    path('api/cargas/upload/', CargaCreateView.as_view(), name='cargas_upload'),
    path('api/cargas/<int:pk>/download/', CargaDownloadView.as_view(), name='cargas_download'),
    path('api/cargas/<int:pk>/', CargaDeleteView.as_view(), name='cargas_delete'),
]
