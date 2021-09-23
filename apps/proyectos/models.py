from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.


class Proyecto(models.Model):
    # Los estados para un proyecto

    ACTIVO = 'ACTIVO'
    CULMINADO = 'CULMINADO'
    CANCELADO = 'CANCELADO'
    ESTADOS = [(ACTIVO, 'Activo'),
               (CULMINADO,'Culminado'),
               (CANCELADO, 'Cancelado')
               ]
    #Tablas
    id_proyectos = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    estado = models.CharField(max_length=15, choices=ESTADOS)
    numSprint = models.IntegerField(default=0)


#Permisos de un proyecto
class Meta:
    permissions = (
        #Permisos sobre el proyecto
        ('crear_proyecto', 'Crear proyecto'),
        ('modificar_proyecto','Modificar proyecto'),
        ('borrar_proyecto', 'Borrar proyecto'),
        #Permisos de los roles del proyecto
        ('crear_rol', 'Crear rol'),
        ('modificar_rol', 'Modificar rol'),
        ('asignar_rol', 'Asignar rol'),
        ('cambiar_rol', 'Cambiar rol'),
        ('borrar_rol','Borrar rol'),
        #Permisos de los usuarios del proyecto
        ('crear_usuario','Crear usuario'),
        ('modificar_usuario','Modificar usuario'),
        ('borrar_usuario','Borrar usuario'),
        #Permisos de los user story del proyecto
        ('crear_us','Crear US'),
        ('modificar_us','Modificar US'),
        ('borrar_us','Borrar US'),
    )

    def str(self):
        return "{}".format(self.nombre)

    #Cantidad de horas de trabajo diario de cada usuario
    class usuario_hora_trabajo(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
        horas = models.PositiveIntegerField(null=True)

