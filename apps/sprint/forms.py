from django.forms import ModelForm, SelectDateWidget
from django import forms
from .models import UserStory
from django.http import JsonResponse


class CrearUserStoryForm(ModelForm):
    """
    Formulario para crear un US

    """
    class Meta:
        model = UserStory
        fields = '__all__'


class SprintForm(ModelForm, forms.Form):
    fecha_inicio = SelectDateWidget()
    fecha_fin = SelectDateWidget()

    class Meta:
        model = Sprint
        fields = '__all__'
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Finalizacion',
        }
