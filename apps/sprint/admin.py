from django.contrib import admin
from .models import Sprint, UserStory
# Register your models here.
admin.site.register(UserStory)
admin.site.register(Sprint)