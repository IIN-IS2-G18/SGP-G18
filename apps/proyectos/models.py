from django.db import models
from django.dispatch import receiver
from django.core.exceptions import FieldError
from django.contrib.auth.models import User
from django.db.models import CASCADE
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
            ("agregar_integrante", "Permiso para editar el proyecto."),
            ("eliminar_integrante", "Permiso para cancelar el proyecto."),
            ("crear_equipo", "Permiso para crear el equipo."),
            ("eliminar_equipo", "Permiso para eliminar el equipo")
        )


class ProyectoManager(models.Manager):
    def crear(self, **kwargs):
        """
        Funcion que crea el proyecto en la base de datos
        :param kwargs: Datos del proyecto
        :returns:  Nada si el proyecto no se creo sino la instancia del nuevo proyecto.
        """
        # Se verifica si se pasaron  los campos necesarios
        # requerimientos = ['nombre', 'descripcion', 'equipo', 'fecha_inicio', 'fecha_fin', 'estado']
        requerimientos = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']

        for requerimiento in requerimientos:
            if requerimiento not in kwargs.keys():
                raise KeyError('{} es requerido.'.format(requerimiento))

        proyecto = Proyecto()

        proyecto.nombre = kwargs['nombre']
        proyecto.descripcion = kwargs['descripcion']
        proyecto.equipo = kwargs['equipo']
        proyecto.fecha_inicio = kwargs['fecha_inicio']
        proyecto.fecha_fin = kwargs['fecha_fin']
        proyecto.estado = kwargs['estado']

        proyecto.save()


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

        nombre = models.TextField('Nombre del Proyecto')
        descripcion = models.TextField('Descripcion', max_length=181)
        fecha_inicio = models.DateField(null=True)
        fecha_fin = models.DateField(null=True)
        equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
        estado = models.CharField(max_length=10, choices=ESTADOS, blank=True)  # Choices de la lista de estados

        def get_state(self):
            """
            :return: retorna el estado del proyecto
            """
            return self.estado

        # Se linkea el Manager del proyecto con el proyecto
        objects = models.Manager()
        projects = ProyectoManager()

        class Meta:
            permissions = (
                ("crear_proyecto", "Permiso para crear un proyecto."),
                ("ver_proyecto", "Permiso para ver el proyecto."),
                ("editar_proyectos", "Permiso para editar el proyecto."),
                ("borrar_proyectos", "Permiso para borrar el proyecto."),
                ("cancelar_proyectos", "Permiso para cancelar el proyecto."),
                ("culminar_proyectos", "Permiso para culminar el proyecto."),
            )


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
    ACTIVO = 'ACTIVO'
    CULMINADO = 'CULMINADO'
    CANCELADO = 'CANCELADO'
    ESTADO_CHOICES = [
        (ACTIVO, 'Activo'),
        (CULMINADO, 'Culminado'),
        (CANCELADO, 'Cancelado')
    ]

    numero_sprint = models.PositiveIntegerField(null=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    duracion = models.PositiveIntegerField(null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True)
    # estado de sprint
    estado = models.CharField(choices=ESTADO_CHOICES, default=ACTIVO, max_length=15)

    class Meta:
        permissions = (
            ("crear_sprint", "Permiso para crear sprint."),
            ("ver_sprint", "Permiso para ver el sprint."),
            ("editar_sprint", "Permiso para editar el sprint."),
            ("borrar_sprint", "Permiso para borrar el sprint."),
            ("cancelar_sprint", "Permiso para cancelar el sprint."),
            ("culminar_sprint", "Permiso para culminar el sprint."),
        )


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

    class Meta:
        permissions = (
            ("crear_us", "Permiso para crear un US."),
            ("modificar_us", "Permiso para modificar el US."),
            ("borrar_us", "Permiso para borrar el US."),
        )