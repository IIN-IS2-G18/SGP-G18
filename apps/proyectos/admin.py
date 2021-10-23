from django.contrib import admin
from .models import Proyecto, Equipo, Sprint, UserStory
admin.site.register(Proyecto)
admin.site.register(Equipo)
admin.site.register(UserStory)
admin.site.register(Sprint)
