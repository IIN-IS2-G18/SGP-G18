"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from .views import ProyectoCrear, ProyectoEditar, ProyectoBorrar, ProyectoDetalle, SprintCrear, \
    SprintModificar, SprintEliminar, SprintEliminar, UserStoryCrear, EquipoCrear, EquipoModificar, EquipoBorrar, \
    RolProyectoCrear, AgregarUsuariosRolView

from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('crear/', ProyectoCrear.as_view()),
    path('<int:pk>/modificar/', ProyectoEditar.as_view(), name='proyecto_editar'),
    path('<int:pk>/eliminar/', ProyectoBorrar.as_view(), name='proyecto_borrar'),
    path('<int:pk>/detalle/', ProyectoDetalle.as_view(), name='proyecto_detalle'),
    path('<int:pkproy>/detalle/crearsprint/', SprintCrear.as_view(), name='crear_sprint'),
    path('<int:pkproy>/detalle/<int:pk>/modificar/', SprintModificar.as_view(), name='sprint_modificar'),
    path('<int:pkproy>/detalle/<int:pk>/eliminar/', SprintEliminar.as_view(), name='sprint_eliminar'),
    path('crearUS/', UserStoryCrear.as_view()),
    path('crearEquipo/', EquipoCrear.as_view(), name='equipo_crear'),
    path('<int:pk>/modificarEquipo', EquipoModificar.as_view(), name='equipo_modificar'),
    path('<int:pk>/eliminarEquipo', EquipoBorrar.as_view(), name='equipo_eliminar'),

    path('roles/crear/', RolProyectoCrear.as_view(),name='rolproyecto_crear'),
    path('<int:pk>/roles/agregarusuarios', AgregarUsuariosRolView.as_view(),name='rolproyecto_agregar')

]
