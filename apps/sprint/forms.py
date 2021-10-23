from django.forms import ModelForm, SelectDateWidget
from django import forms
from .models import Sprint, UserStory
from django.http import JsonResponse


# Se crea un form para el Sprint
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
