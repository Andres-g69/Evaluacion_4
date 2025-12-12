from django.urls import path
from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("carga/", views.carga_view, name="carga"),


    # calificaciones (HTML)
    path("calificaciones/", views.calificaciones_list_view, name="calificaciones"),
    path('calificaciones/', views.calificacion_list_view, name='calificaciones_listado_view'),
    path("calificaciones/nueva/", views.CalificacionCreateView.as_view(), name="calificacion_create_view"),
    path("calificaciones/<int:pk>/editar/", views.CalificacionUpdateView.as_view(), name="calificacion_update_view"),
    path("calificaciones/<int:pk>/eliminar/", views.CalificacionDeleteView.as_view(), name="calificacion_delete_view"),
    path('archivo-carga-procesar/', views.archivo_carga_procesar, name='archivo-carga-procesar'),
    
    
    path("calificaciones/listado/", views.calificaciones_listado_view, name="calificaciones_listado"),
    path("calificaciones/crear/", views.calificaciones_crear_view, name="calificaciones_crear"),
    path("calificaciones/editar/<int:id>/", views.calificaciones_editar_view, name="calificaciones_editar"),
    path("calificaciones/eliminar/<int:id>/", views.calificaciones_eliminar_view, name="calificaciones_eliminar"),

    # busqueda / perfil / admin
    path("busqueda/", views.calificaciones_list_view, name="busqueda"),  # puedes cambiar para vista de búsqueda
    path("perfil/", views.perfil_usuario, name="perfil_usuario"),
    path("adminpanel/", views.admin_dashboard_view, name="adminpanel"),
    path("admin/usuarios/", views.admin_usuarios_view, name="admin_usuarios"),
    path("admin/auditorias/", views.admin_auditorias_view, name="admin_auditorias"),
]
