from django.db import models
from apps.proyectos.models import Proyecto
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
# Create your models here.


class Sprint(models.Model):
    """
    Tabla para el sprint

    fecha_inicio: fecha en donde comenzara el sprint
    fecha_fin: fecha en donde terminara el sprint
    duracion: cantidad de dias del sprint
    proyecto: proyecto al cual pertenece el sprint
    estado: estado del sprint
    historias: historias de usuario que son asignadas al sprint
    """
    # Estados de un sprint
    ACTIVO = 'Activo'
    CULMINADO = 'Culminado'
    CANCELADO = 'Cancelado'
    ESTADO_CHOICES = [
        (ACTIVO, 'Activo'),
        (CULMINADO, 'Culminado'),
        (CANCELADO, 'Cancelado')
    ]

    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    duracion = models.PositiveIntegerField(null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    # estado de sprint
    estado = models.CharField(choices=ESTADO_CHOICES, default=True, max_length=15)

class UserStory(models.Model):
    """
    Tabla de UserStory en la base de datos
    """
    # Estados de un US
    PRODUCT_BACKLOG = 'PRODUCT_BACKLOG'
    TODO = 'TO_DO'
    INPROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    ESTADO_CHOICES = [
        (PRODUCT_BACKLOG, 'Product Backlog'),
        (TODO, 'To Do'),
        (INPROGRESS, 'In Progress'),
        (COMPLETED, 'Completed')
    ]
    # Datos
    nombre = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=50)
    prioridad = models.PositiveIntegerField()
    estado = models.CharField(choices=ESTADO_CHOICES, max_length=15)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    # Su historial
    historial = HistoricalRecords()