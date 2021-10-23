from .views import SprintCrear, SprintModificar, SprintEliminar, UserStoryCrear, UserStoryModificar, UserStoryEliminar
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('crearsprint/', SprintCrear.as_view()),
    path('int:<pk>/modificar/', SprintModificar.as_view(), name='sprint_modificar'),
    path('<int:pk>/eliminar/', SprintEliminar.as_view(), name='sprint_eliminar'),
    path('crearUS/', UserStoryCrear.as_view()),
]
