from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Equipo, Proyecto, Sprint, UserStory
import unittest
from datetime import datetime
import traceback
# Create your tests here.

class ProyectoTestCase(TestCase):

    def test_crear_proyecto(self):
        '''
        Test para crear un proyecto.
        '''
        print("Test: Creando Proyecto...")

        #creamos miembros del equipo
        miembro_1 = User(username="test")
        miembro_1.set_password('test')
        miembro_1.save()
        miembro_2 = User(username="test1")
        miembro_2.set_password('test')
        miembro_2.save()
        miembro_3 = User(username="test2")
        miembro_2.set_password('test')
        miembro_3.save()

        # nos loqueamos
        c = Client()
        logueado = c.login(username="test", password="test")
        self.assertTrue(logueado)

        #creamos el equipo
        equipo = Equipo.objects.create(nombre="equipo_test")
        equipo.usuarios.set([miembro_1,miembro_2,miembro_3])
        equipo.save()

        #creamos el proyecto
        response = c.post('/proyectos/crear/',{
            "nombre": "proyecto test",
            "descripcion": "breve descripcion de prueba",
            "equipo" : equipo.id,
            'fecha_inicio': '10/02/2021',
            'fecha_fin': '10/03/2021',
            'estado' : 'ACTIVO'})
        self.assertEqual(response.url, '/')
        print("Test: Proyecto creado!")

class SprintTestCase(TestCase):

    def test_crear_sprint(self):
        """
        Test para crear un Sprint.
        """
        print("Test: Creando Sprint...")

        # creamos miembros del equipo
        miembro_1 = User(username="test")
        miembro_1.set_password('test')
        miembro_1.save()
        miembro_2 = User(username="test1")
        miembro_2.set_password('test')
        miembro_2.save()
        miembro_3 = User(username="test2")
        miembro_2.set_password('test')
        miembro_3.save()

        # creamos el equipo
        equipo = Equipo.objects.create(nombre="equipo_test")
        equipo.usuarios.set([miembro_1, miembro_2, miembro_3])
        equipo.save()


        descripcion = "sprint prueba"
        fecha_inicio = datetime.now()
        fecha_fin = datetime.now()
        nombre = "nombre_test"


        proyecto = Proyecto.objects.create(nombre=nombre,
                                           estado='ACTIVO',
                                           fecha_inicio=fecha_inicio,
                                           fecha_fin=fecha_fin,
                                           descripcion=descripcion,
                                           )
        proyecto.save()
        sprint = Sprint(
                        proyecto=proyecto,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        estado='CULMINADO')
        sprint.save()