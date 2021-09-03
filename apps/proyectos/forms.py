from django import forms
from apps.proyectos.models import Proyecto


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto

        fields = [
            'nombre',
            'descripcion',
            'fechaInicio',
            'fechaFin',
        ]

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
