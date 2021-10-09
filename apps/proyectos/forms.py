from django import forms
from django.forms import ModelForm, ModelChoiceField, SelectDateWidget
from .models import Proyecto, Equipo
from django.http import JsonResponse



class ProyectoForm(ModelForm, forms.Form):
    equipo = ModelChoiceField(initial = 0, queryset=Equipo.objects.all())
    fechaInicio = SelectDateWidget()
    fechaFin = SelectDateWidget()
    class Meta:
        model = Proyecto
        fields = '__all__'
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'equipo' : 'Equipo',
            'fechaInicio': 'Fecha de Inicio',
            'fechaFin': 'Fecha de Finalizacion',
            'estado' : 'Estado'
        }

