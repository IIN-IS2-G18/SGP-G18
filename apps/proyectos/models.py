from django.db import models

# Create your models here.

class Proyecto(models.Model):
    id_proyectos = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    estado = models.IntegerField()
