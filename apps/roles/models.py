from django.db import models
from django.contrib.auth.models import Group
# Create your models here.

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    proyecto = models.ForeignKey(to="proyectos.Proyecto",on_delete=models.CASCADE, null=True, blank=True)
    sprint = models.ManyToManyField(to="proyectos.Sprint", blank=True)
class Meta:
    unique_together = ["nombre", "proyecto"]
    permissions = (
        ('Crear Proyecto', 'Permite crear proyectos'),
        ('Modificar Proyecto', 'Permite modificar proyectos'),
        ('Borrar Proyecto', 'Permite borrar proyectos'),
        ('Crear US', 'Crear User Story'),
        ('Modificar US', 'Modificar User Story'),
        ('Borrar US', 'Borrar User Story'),
        ('Inicializar Sprint', 'Permite iniciar Sprint'),
        ('Asignar US a Sprint', 'Permite asignar user story a un sprint'),
        ('Participar del Daily Meet', 'Permite participar del Daily Meet'),
    )