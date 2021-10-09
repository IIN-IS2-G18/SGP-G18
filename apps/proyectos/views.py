from django.shortcuts import render, redirect
from .models import Proyecto, Equipo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class ProyectoCrear(LoginRequiredMixin, CreateView):
    model = Proyecto
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ProyectoCrear, self).get_context_data(**kwargs)
        context["equipos"] = Equipo.objects.all()
        context["estados"] = Proyecto.ESTADOS
        return context

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        context = {
            'form': form
        }
        print(form.errors)
        return super(ProyectoCrear, self).render_to_response(self.get_context_data(**context))


class ProyectoEditar(LoginRequiredMixin, UpdateView):
    template_name = 'proyectos/proyecto_modificar.html'
    model = Proyecto
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ProyectoEditar, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        context = {
            'form': form
        }
        print(form.errors)
        return super(ProyectoEditar, self).render_to_response(self.get_context_data(**context))


class ProyectoBorrar(LoginRequiredMixin, DeleteView):
    template_name = 'proyectos/proyecto_eliminar.html'
    model = Proyecto
    success_url = '/'



