from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test  # Aquí agregamos la importación
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from api.models import CalificacionTributaria
from api.forms import CalificacionTributariaForm, TipoCalificacionForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@login_required
def tipo_calificacion_create_view(request):
    if request.method == 'POST':
        form = TipoCalificacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('frontend:calificaciones_listado_view')  # Redirigir a la vista de listado de calificaciones
    else:
        form = TipoCalificacionForm()
    
    return render(request, 'calificaciones/formulario.html', {'form': form, 'modo': 'crear'})

@csrf_exempt
def archivo_carga_procesar(request):
    if request.method == "POST" and request.FILES['archivo']:
        archivo = request.FILES['archivo']
        # Aquí iría la lógica para procesar el archivo, como validar, leer o guardar los datos.
        # Por ejemplo, podrías guardar el archivo o procesarlo según el tipo.
        return HttpResponse("Archivo procesado correctamente.")
    return render(request, 'frontend/carga.html')

@login_required
def carga_view(request):
    return render(request, "frontend/Carga.html")
from api.models import CalificacionTributaria

@login_required
def calificacion_list_view(request):
    calificaciones = CalificacionTributaria.objects.all()
    return render(request, 'calificaciones/listado.html', {'calificaciones': calificaciones})

@login_required
def calificaciones_list_view(request):
    calificaciones = CalificacionTributaria.objects.select_related(
        "rut_contribuyente", "codigo_tipo_calificacion"
    ).all()
    return render(request, "calificaciones/listado.html", {
        "calificaciones": calificaciones
    })

@login_required
def calificaciones_listado_view(request):
    calificaciones = CalificacionTributaria.objects.all()
    return render(request, "calificaciones/listado.html", {'calificaciones': calificaciones})

# Vista para crear una calificación
@login_required
def calificaciones_crear_view(request):
    if request.method == 'POST':
        form = CalificacionTributariaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Calificación creada correctamente.")
            return redirect('frontend:calificaciones')
    else:
        form = CalificacionTributariaForm()
    
    return render(request, "calificaciones/crear.html", {'form': form})

# Vista para editar una calificación
@login_required
def calificaciones_editar_view(request, id):
    calificacion = get_object_or_404(CalificacionTributaria, id=id)
    if request.method == 'POST':
        form = CalificacionTributariaForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Calificación actualizada correctamente.")
            return redirect('frontend:calificaciones')
    else:
        form = CalificacionTributariaForm(instance=calificacion)
    
    return render(request, "calificaciones/editar.html", {'form': form, 'calificacion': calificacion})

# Vista para eliminar una calificación
@login_required
def calificaciones_eliminar_view(request, id):
    calificacion = get_object_or_404(CalificacionTributaria, id=id)
    if request.method == 'POST':
        calificacion.delete()
        messages.success(request, "Calificación eliminada correctamente.")
        return redirect('frontend:calificaciones')
    
    return render(request, "calificaciones/eliminar.html", {'calificacion': calificacion})

# Vistas de autenticación
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect("frontend:dashboard")
        messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, "frontend/Login.html")

def logout_view(request):
    auth_logout(request)
    return redirect("frontend:login")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect("frontend:register")
        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        return redirect("frontend:dashboard")
    return render(request, "frontend/Register.html")

@login_required
def dashboard_view(request):
    return render(request, "frontend/Dashboard.html")

# CBV for create/update/delete using the ModelForm
class CalificacionCreateView(CreateView):
    model = CalificacionTributaria
    form_class = CalificacionTributariaForm
    template_name = "calificaciones/formulario.html"
    success_url = reverse_lazy('frontend:calificaciones')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.usuario_creacion = self.request.user.username
        obj.usuario_actualizacion = self.request.user.username
        obj.save()
        return super().form_valid(form)

class CalificacionUpdateView(UpdateView):
    model = CalificacionTributaria
    form_class = CalificacionTributariaForm
    template_name = "calificaciones/formulario.html"
    success_url = reverse_lazy('frontend:calificaciones')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.usuario_actualizacion = self.request.user.username
        obj.save()
        return super().form_valid(form)

class CalificacionDeleteView(DeleteView):
    model = CalificacionTributaria
    template_name = "calificaciones/confirmar_eliminacion.html"
    success_url = reverse_lazy('frontend:calificaciones')

# Admin views (examples)
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser or u.is_staff)(view_func)

@login_required
@admin_required
def admin_dashboard_view(request):
    return render(request, "admin/admin_dashboard.html")

@login_required
@admin_required
def admin_usuarios_view(request):
    from django.contrib.auth.models import User
    usuarios = User.objects.all().order_by("id")
    return render(request, "admin/admin_usuarios.html", {"usuarios": usuarios})

@login_required
@admin_required
def admin_auditorias_view(request):
    from api.models import Auditoria
    auditorias = Auditoria.objects.select_related('usuario').order_by('-fecha_operacion')
    return render(request, "admin/admin_auditorias.html", {'auditorias': auditorias})

@login_required
def perfil_usuario(request):
    return render(request, "frontend/perfil_usuario.html", {'user': request.user})
