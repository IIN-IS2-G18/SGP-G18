from django import forms
from django.forms import ModelForm, ModelChoiceField, SelectDateWidget
from django.contrib.auth.models import User
from .models import Proyecto, Equipo, Sprint, UserStory, RolProyecto
from django.http import JsonResponse


class ProyectoForm(ModelForm, forms.Form):
    equipo = ModelChoiceField(initial=0, queryset=Equipo.objects.all())
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


class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = [
            "numero_sprint",
            "fecha_inicio",
            "fecha_fin",
            "duracion",
            #"proyecto",
            "estado",
        ]
# Se crea un form para el UserStory


class UserStoryForm(forms.ModelForm):
    class Meta:
        model = UserStory
        fields = [
            "nombre",
            "descripcion",
            "prioridad",
            # "sprint",
        ]


class RolProyectoForm(forms.ModelForm):
    class Meta:
        model = RolProyecto
        fields = [
            "nombre",
            "permisos"
        ]


class AgregarUsuariosRolForm(forms.ModelForm):
    class Meta:
        fields = ["usuarios","proyecto","rol"]