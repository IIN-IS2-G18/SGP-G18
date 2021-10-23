from django.db import models
from apps.proyectos.models import Proyecto
from django.contrib.auth.models import User
from django.db.models import CASCADE

# Create your models here.


class Sprint(models.Model):
    """
    Tabla para el sprint

    nombre: identificador para el sprint
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

    numero_sprint = models.PositiveIntegerField(null=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    duracion = models.PositiveIntegerField(null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True)
    # estado de sprint
    estado = models.CharField(choices=ESTADO_CHOICES, default=True, max_length=15)


def __str__(self):
    return self.nombre



class UserStory(models.Model):
    """
    Tabla de UserStory en la base de datos
    """
    # Estados de un US
    TODO = 'TO_DO'
    INPROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    PRODUCTBACKLOG = 'PRODUCT_BACKLOG'
    ESTADO_CHOICES = [
        (TODO, 'To Do'),
        (INPROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (PRODUCTBACKLOG, 'Product Backlog')
    ]
    # Prioridades del US
    BAJA = 'BAJA'
    ALTA = 'ALTA'
    EMERGENCIA = 'EMERGENCIA'
    PRIORIDADES = [
        (BAJA, 'Baja'),
        (ALTA, 'Alta'),
        (EMERGENCIA, 'Emergencia')
    ]
    # Datos
    nombre = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=50)
    prioridad = models.CharField(choices=PRIORIDADES, max_length=15)
    estado_us = models.CharField(choices=ESTADO_CHOICES, default=PRODUCTBACKLOG, max_length=15)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    
