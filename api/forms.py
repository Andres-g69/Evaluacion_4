# api/forms.py
from django import forms
from .models import CalificacionTributaria, TipoCalificacion, Contribuyente



class TipoCalificacionForm(forms.ModelForm):
    class Meta:
        model = TipoCalificacion
        fields = [
            'codigo', 'descripcion', 'categoria', 'monto_minimo', 'monto_maximo', 'requisitos', 'activo'
        ]
        widgets = {
            'monto_minimo': forms.NumberInput(attrs={'step': '0.01'}),
            'monto_maximo': forms.NumberInput(attrs={'step': '0.01'}),
            'requisitos': forms.Textarea(attrs={'rows': 4}),
        }

class CalificacionTributariaForm(forms.ModelForm):
    class Meta:
        model = CalificacionTributaria
        fields = [
            'rut_contribuyente',
            'codigo_tipo_calificacion',
            'fecha_calificacion',
            'monto_anual',
            'periodo',
            'estado',
            'observaciones',
            'fecha_vencimiento',
            'vigente'
        ]
        widgets = {
            'fecha_calificacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }
