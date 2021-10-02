from django.forms import ModelForm
from .models import Proyecto


class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'fechaInicio': 'Fecha de Inicio',
            'fechaFin': 'Fecha de Finalizacion',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'fechaInicio': forms.DateInput,
            'fechaFin': forms.DateInput,
        }
