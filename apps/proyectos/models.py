from django.db import models
from django.dispatch import receiver
from django.core.exceptions import FieldError
from django.contrib.auth.models import User, Permission
from django.db.models import CASCADE
from datetime import date, timezone
from django.utils import *
# === Models for Todos app ===


class Equipo(models.Model):
    """
    Modelo para representar los Equipos en el proyecto.

    Necesita de un nombre y de una lista de usuario que conforman el equipo

    Para trazabilidad se agregaron los campos de created_at y updated_at que son calculados en el momento
    de crear el objeto.
    """
    nombre = models.CharField(max_length=20)
    usuarios = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("agregar_integrante", "Permiso para agregar integrante al equipo."),
            ("eliminar_integrante", "Permiso para eliminar integrante al equipo."),
            ("crear_equipo", "Permiso para crear el equipo."),
            ("eliminar_equipo", "Permiso para eliminar el equipo")
        )


class Proyecto(models.Model):
        """
        El model guarda informacion de todos los proyectos del sistema.

        :param id: ID unico
        :param nombre: Nombre del Proyecto
        :param descripcion: Descripcion del proyecto
        :param equipo: Personas que realizan el proyecto
        :param fecha_inicio: Fecha de Inicio del Proyecto
        :param fecha_fin: Fecha de finalizacion del Proyecto
        :param estado: Estado del proyecto
        """
        # Estados de un proyecto
        ACTIVO = 'ACTIVO'
        CULMINADO = 'CULMINADO'
        CANCELADO = 'CANCELADO'
        ESTADOS = [(ACTIVO, 'Activo'),
                   (CULMINADO, 'Culminado'),
                   (CANCELADO, 'Cancelado')
                   ]

        nombre = models.CharField(max_length=150, unique=True)  # Nombre del proyecto
        descripcion = models.TextField(max_length=250, blank=True, null=True)  # Descripcion del proyecto
        fecha_inicio = models.DateField(null=True, blank=True)  # Fecha de inicio del proyecto
        fecha_fin = models.DateField(null=True, blank=True)  # Fecha fin del proyecto
        equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
        estado = models.CharField(max_length=10, choices=ESTADOS, blank=True)  # Choices de la lista de estados
        scrum_master = models.ForeignKey(User, on_delete=models.CASCADE)  # Scrum Master del proyecto

        def __str__(self):
            """
            :return: retorna el nombre del proyecto
            """
            return self.nombre

        class Meta:
            permissions = (
                ("crear_proyecto", "Permiso para crear un proyecto."),
                ("ver_proyecto", "Permiso para ver el proyecto."),
                ("editar_proyectos", "Permiso para editar el proyecto."),
                ("borrar_proyectos", "Permiso para borrar el proyecto."),
                ("cancelar_proyectos", "Permiso para cancelar el proyecto."),
                ("culminar_proyectos", "Permiso para culminar el proyecto."),
            )


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

    nombre = models.CharField(max_length=15, unique=True)  # Nombre del US
    descripcion = models.CharField(max_length=50, blank=True, null=True)  # Descripcion del US
    prioridad = models.IntegerField(null=True, blank=True)  # Prioridad del US del 1 al 3
    fecha_ingreso = models.DateField("Date", default=date.today)
    estado_us = models.CharField(choices=ESTADO_CHOICES, default=PRODUCTBACKLOG, max_length=15)  # Estados del US
    horas_estimadas = models.FloatField(null=True, blank=True)  # Horas estimadas del US
    tiempo = models.FloatField(default=0)  # Tiempo dedicado al US en horas
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=False)  # Proyecto al que pertenece el US
    responsable = models.ForeignKey(User, on_delete=CASCADE, blank=True)  # Miembro responsable de trabajar en el US

    """def __str__(self):
        return self.nombre"""


class Sprint(models.Model):
    """
    Tabla para el sprint
    """
    # Estados de un sprint
    PLANIFICANDO = 'PLANIFICANDO'
    ACTIVO = 'ACTIVO'
    CULMINADO = 'CULMINADO'
    CANCELADO = 'CANCELADO'
    ESTADO_CHOICES = [
        (PLANIFICANDO, 'Planificando'),
        (ACTIVO, 'Activo'),
        (CULMINADO, 'Culminado'),
        (CANCELADO, 'Cancelado')
    ]
    numero_sprint = models.PositiveIntegerField(null=True)  # Numero del Sprint
    fecha_inicio = models.DateField(null=True, blank=True)  # Fecha de inicio del Sprint
    fecha_fin = models.DateField(null=True, blank=True)  # Fecha de fin del Sprint
    # duracion = models.PositiveIntegerField(null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True)  # Proyecto al que pertenece el Sprint.
    # estado de sprint
    estado_sprint = models.CharField(choices=ESTADO_CHOICES, default=ACTIVO, max_length=15)  # Estado en que se encuentra el Sprint

    class Meta:
        permissions = (
            ("crear_sprint", "Permiso para crear sprint."),
            ("ver_sprint", "Permiso para ver el sprint."),
            ("editar_sprint", "Permiso para editar el sprint."),
            ("borrar_sprint", "Permiso para borrar el sprint."),
            ("cancelar_sprint", "Permiso para cancelar el sprint."),
            ("culminar_sprint", "Permiso para culminar el sprint."),
        )


class HistorialUS(models.Model):  # Modelo para el historial del US
    fecha = models.DateField(default=timezone.now)  # hora y fecha del registro de actividad que se relaciona al US
    descripcion = models.CharField(max_length=250)  # Descripcion del trabajo realizado sobre el US
    duracion = models.FloatField()  # tiempo que se dedica al trabajo sobre el US
    id_us = models.ForeignKey(UserStory, on_delete=models.CASCADE)  # Sobre que US se realiza la acitivdad
    id_sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)

class RolProyecto(models.Model):
    nombre = models.CharField(max_length=15)
    permisos = models.ManyToManyField(Permission,)

class RolProyectoUsuarios(models.Model):
    rol = models.ForeignKey(RolProyecto, on_delete=CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=CASCADE)
    usuarios = models.ForeignKey(User, on_delete=CASCADE)