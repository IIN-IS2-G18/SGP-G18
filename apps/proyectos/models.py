from django.db import models
from django.dispatch import receiver
from django.core.exceptions import FieldError
from django.contrib.auth.models import User
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
            ("eliminar_equipo" , "Permiso para eliminar el equipo")
        )

class ProyectoManager(models.Manager):
    def crear(self, **kwargs):
        """
        Funcion que crea el proyecto en la base de datos
        :param kwargs: Datos del proyecto
        :returns:  Nada si el proyecto no se creo sino la instancia del nuevo proyecto.
        """
        # Se verifica si se pasaron  los campos necesarios
        #requerimientos = ['nombre', 'descripcion', 'equipo', 'fecha_inicio', 'fecha_fin', 'estado']
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
        estado = models.CharField(max_length=10, choices=ESTADOS, blank=True) # Choices de la lista de estados

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







