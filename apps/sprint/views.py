from django.shortcuts import render, redirect
from .models import Sprint, UserStory
from .forms import SprintForm, UserStoryForm
from apps.proyectos.models import Proyecto
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class SprintCrear(CreateView):
    # Se especifica el models para crear view
    model = Sprint
    # Se especifican los fields a ser desplegados
    fields = [
            "numero_sprint",
            "fecha_inicio",
            "fecha_fin",
            "duracion",
            # "proyecto",
            "estado",
    ]

    def get_context_data(self, **kwargs):
        """

        Override de la función original, agregamos el query de todas las opciones para los estados.

        El contexto puede ser accedido directamente en el template de proyecto_form.html
        Agregamos al context para poder colocarlos como opciones en la lista desplegable.

        :param kwargs:
        :return: contexto
        """
        context = super(SprintCrear, self).get_context_data(**kwargs)
        context["estados"] = Proyecto.ESTADOS
        return context


class SprintModificar(UpdateView):
    model = Sprint
    fields = [
        "numero_sprint",
        "fecha_inicio",
        "fecha_fin",
        "duracion",
        # "proyecto",
        "estado",
    ]
    # Se puede especificar url exitoso
    # Url para redireccionar despues del exito
    # modificando detalles
    success_url = "/"


class SprintEliminar(DeleteView):
    model = Sprint
    success_url = "/"


class UserStoryCrear(CreateView):
    # Se especifica el models para crear view
    model = UserStory
    # Se especifican los fields a ser desplegados
    fields = [
        "nombre",
        "descripcion",
        "prioridad",
        # "estado",
        # "proyecto",
        # "sprint",
    ]

    def get_context_data(self, **kwargs):
        """

        Override de la función original, agregamos el query de todas las opciones para los estados.

        El contexto puede ser accedido directamente en el template de proyecto_form.html
        Agregamos al context para poder colocarlos como opciones en la lista desplegable.

        :param kwargs:
        :return: contexto
        """
        context = super(UserStoryCrear, self).get_context_data(**kwargs)
        context["prioridades"] = UserStory.PRIORIDADES
        return context

    def form_invalid(self, form):
        """
        Se recarga la página del form y se muestra en pantalla los errores que puedieron haber cometido
        durante la creación del form.
        :param form:
        :return: Reload del form con errores.
        """
        context = {
            'form': form
        }
        print(form.errors)
        return super(UserStoryCrear, self).render_to_response(self.get_context_data(**context))

class UserStoryModificar(UpdateView):
    model = UserStory
    fields = [
        "nombre",
        "descripcion",
        "prioridad",
        "estado",
        "proyecto",
        "sprint",
    ]
    template_name = 'userstory/userstory_form.html'


class UserStoryEliminar(DeleteView):
    model = UserStory
    success_url = "/"
