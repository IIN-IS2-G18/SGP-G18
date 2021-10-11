from django.shortcuts import render, redirect
from .models import Proyecto, Equipo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class ProyectoCrear(LoginRequiredMixin, CreateView):
    """
    View creado específicamente para crear un proyecto.

    Utiliza un LoginRequiredMixin para asegurarnos de que solo puede ser accedida
    por usuarios que están logueados y hereda del CreateView.
    """
    model = Proyecto
    fields = '__all__'

    def get_context_data(self, **kwargs):
        """

        Override de la función original, agregamos el query de todos los equipos dentro del proyecto
        y las opciones para los estados.

        El contexto puede ser accedido directamente en el template de proyecto_form.html
        Agregamos al context para poder colocarlos como opciones en la lista desplegable.

        :param kwargs:
        :return: contexto
        """
        context = super(ProyectoCrear, self).get_context_data(**kwargs)
        context["equipos"] = Equipo.objects.all()
        context["estados"] = Proyecto.ESTADOS
        return context

    def get_success_url(self):
        """
        Override de la función original

        Se implementa un template personalizado en caso de que el proyecto fue creado/actualizado exitosamente
        :return: redireccionamiento hacia la página de éxito
        """
        return reverse('home')

    def form_valid(self, form):
        """
        En caso de que el form sea válido, este es guardado y se crea el objeto en la base de datos.
        :param form:
        :return: Redireccionamiento a la página de éxito
        """
        form.save()
        return HttpResponseRedirect(self.get_success_url())

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
        return super(ProyectoCrear, self).render_to_response(self.get_context_data(**context),)



class ProyectoEditar(LoginRequiredMixin, UpdateView):

    """
    View creado para actualizar el proyecto en caso de ser necesario.
    
    Utiliza un LoginRequiredMixin para asegurarnos de que solo puede ser accedida
    por usuarios que están logueados y hereda del CreateView.
    
    """
    template_name = 'proyectos/proyecto_modificar.html'
    model = Proyecto
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        """
        Override creado para incluir más datos a los datos del contexto y poder
        visualizarlos en el template correspondiente.
        :param kwargs:
        :return: contexto
        """
        context = super(ProyectoEditar, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        """
        :return: el path del template personalizado.
        """
        return reverse('home')

    def form_valid(self, form):
        """
                En caso de que el form sea válido, este es guardado y se crea el objeto en la base de datos.
                :param form:
                :return: Redireccionamiento a la página de éxito
                """
        form.save()
        return HttpResponseRedirect(self.get_success_url())

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
        return super(ProyectoEditar, self).render_to_response(self.get_context_data(**context))


class ProyectoBorrar(LoginRequiredMixin, DeleteView):
    """
    View implementado para eliminar un proyecto de la base de datos

    Requiere que el usuario esté logueado y hereda de DeleteView.

    El template es una página que solicita una confirmación para eliminar el proyecto.

    El url de éxito redirige a home.
    """
    template_name = 'proyectos/proyecto_eliminar.html'
    model = Proyecto
    success_url = '/'



