from django.shortcuts import render, redirect

# Create your views here.
from apps.proyectos.forms import ProyectoForm


def index(request):
    return render(request, 'proyectos/index.html')


def proyecto_view(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('proyectos:index')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/proyecto_form.html', {'form': form})
