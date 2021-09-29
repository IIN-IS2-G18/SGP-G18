from django.db import models
from django.dispatch import receiver
from django.core.exceptions import FieldError


class ProyectoManager(models.Manager):
    def crear(self, **kwargs):
        """
        Funcion que crea el proyecto en la base de datos
        :param kwargs: Datos del proyecto
        :returns:  Nada si el proyecto no se creo sino la instancia del nuevo proyecto.
        """
        # Se verifica si se pasaron  los campos necesarios
        requerimientos = ['nombre', 'descripcion', 'equipo', 'fecha_inicio', 'fecha_fin', 'estado']

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

            id = models.AutoField(primary_key=True)
            nombre = models.TextField('Nombre del Proyecto')
            descripcion = models.TextField('Descripcion', max_length=180)
            equipo = models.ManyToManyField(User, related_name='mm_proyecto_equipo')
            fecha_inicio = models.DateField(null=True)
            fecha_fin = models.DateField(null=True)
            estado = models.CharField(max_length=10, choices=ESTADOS, blank=True) # Choices de la lista de estados

            def get_state(self):
                """
                :return: retorna el estado del proyecto
                """
                return self.estado






