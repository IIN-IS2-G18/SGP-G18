from django.forms import ModelForm
from .models import Proyecto
from django.http import JsonResponse

class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)


class ProyectoForm(JsonableResponseMixin, ModelForm):
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
