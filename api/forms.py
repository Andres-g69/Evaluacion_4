from django import forms
from .models import CalificacionTributaria, Instrumento, FactorConversion

class CalificacionTributariaForm(forms.ModelForm):
    # 🔽 Instrumento como lista desplegable
    instrumento = forms.ChoiceField(
        choices=Instrumento.INSTRUMENTO_CHOICES,
        required=False,
        label="Instrumento",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # 🔽 Factor como lista desplegable
    factor = forms.ChoiceField(
        choices=FactorConversion.FACTOR_CHOICES,
        required=False,
        label="Factor de Conversión",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CalificacionTributaria
        # Excluimos campos automáticos o de auditoría
        exclude = ['creado_por', 'creado_en', 'actualizado_en', 'archivo_origen']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
