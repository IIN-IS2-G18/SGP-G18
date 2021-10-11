from django.shortcuts import render, redirect
from .models import Sprint
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class SprintCrear(LoginRequiredMixin, CreateView):
    model = Sprint
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(SprintCrear, self).get_context_data(**kwargs)
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
        return super(SprintCrear, self).render_to_response(self.get_context_data(**context))


class SprintEditar(LoginRequiredMixin, UpdateView):
    template_name = 'sprint/sprint_modificar.html'
    model = Sprint
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(SprintEditar, self).get_context_data(**kwargs)
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
        return super(SprintEditar, self).render_to_response(self.get_context_data(**context))


class SprintBorrar(LoginRequiredMixin, DeleteView):
    template_name = 'sprint/sprint_eliminar.html'
    model = Sprint
    success_url = '/'