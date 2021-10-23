from django import forms
from django.forms import ModelForm, ModelChoiceField, SelectDateWidget
from django.contrib.auth.models import User
from .models import Proyecto, Equipo
from django.http import JsonResponse



class ProyectoForm(ModelForm, forms.Form):
    fechaInicio = SelectDateWidget()
    fechaFin = SelectDateWidget()
    class Meta:
        model = Proyecto
        fields = '__all__'
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'equipo': 'Equipo',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Finalizacion',
            'estado': 'Estado'
        }


class EquipoForm(ModelForm, forms.Form):
    usuarios = ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Equipo
        fields = '__all__'
