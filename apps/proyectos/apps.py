from django.apps import AppConfig


class ProyectoConfig(AppConfig):
    name = 'apps.proyectos'


class SprintConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sprint'
