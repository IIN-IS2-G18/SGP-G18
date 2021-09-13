from django.shortcuts import render, redirect

# Create your views here.
from apps.proyectos.forms import ProyectoForm
from apps.proyectos.models import Proyecto


def index(request):
    return render(request, 'proyectos/index.html')


def proyecto_view(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('index')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/proyecto_form.html', {'form': form})

def proyecto_list(request):
    proyecto = Proyecto.objects.all()
    contexto = {'proyectos':proyecto}
    return render(request, 'proyectos/proyectos_list.html', contexto)
