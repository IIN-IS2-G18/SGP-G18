from django.shortcuts import render, redirect
from .models import Proyecto
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse


class ProyectoCrear(CreateView):
    model = Proyecto
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ProyectoCrear, self).get_context_data(**kwargs)
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


class ProyectoEditar(UpdateView):
    model = Proyecto
    fields = '__all__'


class ProyectoBorrar(DeleteView):
    model = Proyecto
    success_url = 'home'
