from django.shortcuts import render, redirect
from .models import Proyecto
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class ProyectoCrear(CreateView):
    model = Proyecto
    fields = '__all__'


class ProyectoEditar(UpdateView):
    model = Proyecto
    fields = '__all__'


class ProyectoBorrar(DeleteView):
    model = Proyecto
    success_url = 'home'
