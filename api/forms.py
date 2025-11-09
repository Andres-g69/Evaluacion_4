from django import forms
from .models import CalificacionTributaria

class CalificacionTributariaForm(forms.ModelForm):
    class Meta:
        model = CalificacionTributaria
        # puedes excluir campos automáticos o de auditoría
        exclude = ['creado_por', 'creado_en', 'actualizado_en', 'archivo_origen']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'comentario': forms.Textarea(attrs={'rows': 3}),
        }
