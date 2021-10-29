from django import forms
from django.db.models import Model
from django.forms import ModelForm, ModelChoiceField, SelectDateWidget, TextInput
from django.contrib.auth.models import User
from .models import Proyecto, Equipo, Sprint, UserStory, RolProyecto
from django.http import JsonResponse


class CrearUSForm(forms.ModelForm):  # Form para nuevo US
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # En esta funcion se validan que los inputs esten dentro del dominio
    def clean(self, *args, **kwargs):
        cleaned_data = super(CrearUSForm, self).clean(*args, **kwargs)
        prioridad = cleaned_data.get('prioridad')
        if prioridad is not None:
            if prioridad < 1 or prioridad > 3:
                self.add_error('prioridad', 'Fuera de Rango')
            horas_estimadas = cleaned_data('horas_estimadas')
            if horas_estimadas is not None:
                if horas_estimadas < 0:
                    self.add_error('horas_estimadas', 'Fuera de Rango')

    class Meta:
        model = UserStory
        fields = ['id_proyecto', 'nombre', 'descripcion', 'horas_estimadas', 'prioridad', 'responsable',
                  'fecha_ingreso']
        labels = {
            'id_proyecto': 'Proyecto',
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'horas_estimadas': 'Horas Estimadas',
            'prioridad': 'Prioridad',
            'responsable': 'Responsable',
            'fecha_ingreso': 'Fecha Ingreso',
        }

        widgets = {
            'id_proyecto': forms.HiddenInput(),  # Id del proyecto OCULTO
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre del US'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion del US'}),
            'horas_estimadas': forms.HiddenInput(),
            'prioridad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1 (Muy Alta) a 5 (Muy Baja)'}),
            'responsable': forms.HiddenInput(),
        }


class EditarUSForm(forms.ModelForm):  # Form para editar US
    # Se valida que los inputs esten dentro del rango
    def clean(self, *args, **kwargs):
        cleaned_data = super(EditarUSForm, self).clean(*args, **kwargs)
        prioridad = cleaned_data.get('prioridad')
        if prioridad is not None:
            if prioridad < 1 or prioridad > 3:
                self.add_error('prioridad', 'Fuera de Rango')

    class Meta:
        model = UserStory
        fields = ['id_proyecto', 'nombre', 'descripcion', 'horas_estimadas', 'prioridad',
                  'responsable', 'fecha_ingreso']
        labels = {
            'id_proyecto': 'Proyecto',
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'horas_estimadas': 'Horas Estimadas',
            'prioridad': 'Prioridad',
            'responsable': 'Responsable',
            'fecha_ingreso': 'Fecha Ingreso',
        }

        widgets = {
            'id_proyecto': forms.HiddenInput(),  # Id del proyecto OCULTO
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre del US'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion del US'}),
            'horas_estimadas': forms.HiddenInput(),
            'prioridad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1 (Muy Alta) a 5 (Muy Baja)'}),
            'responsable': forms.HiddenInput(),
        }


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


class CrearSprintForm(forms.ModelForm):  # Form para crear sprint
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_fin'].required = False

    class Meta:
        model = Sprint
        fields = ['proyecto', 'numero_sprint', 'fecha_inicio', 'fecha_fin']
        labels = {
            'proyecto': 'ID Proyecto',
            'numero_sprint': 'Numero de Sprint',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
        }

        widgets = {
            'proyecto': forms.HiddenInput(),  # oculta el ID del Proyecto
            'numero_sprint': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero de Sprint',
                                                    'type': 'number', 'readonly': 'readonly'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }


class ModificarFechaSprintForm(forms.ModelForm):  # Form para editar la fecha del Sprint
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # para no hacer obligadatorios algunos campos
        self.fields['fecha_fin'].required = True
        self.fields['fecha_inicio'].required = True

    class Meta:
        model = Sprint
        fields = ['proyecto', 'numero_sprint', 'fecha_inicio', 'fecha_fin', 'estado_sprint']

        labels = {
            'proyecto': 'ID proyecto',
            'numero_sprint': 'Numero de Sprint',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
            'estado_sprint': 'Estado de Sprint',
        }

        widgets = {
            'proyecto': forms.HiddenInput(),  # oculta el ID del Proyecto
            'numero_sprint': forms.HiddenInput(),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'estado_sprint': forms.HiddenInput(),
        }


class HistorialUSForm(forms.ModelForm):  # Formulario para que pueda cargar la actividad que se realiza en el US
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = HistorialUS
        fields = ['fecha', 'descripcion', 'duracion', 'id_us', 'id_sprint']
        labels = {
            'fecha': 'Fecha',
            'descripcion': 'Descripcion',
            'duracion': 'Duracion',
            'id_us': 'User Story',
            'id_sprint': 'Sprint',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Actividad Hecha'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Tiempo dedicado(en horas)', 'type': 'number'}),
            'id_us': forms.HiddenInput(),
            'id_sprint': forms.HiddenInput(),
        }



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
