from django.db import models


# Create your models here.

class Proyecto(models.Model):
    id_proyectos = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    estado = models.IntegerField(default=0)
