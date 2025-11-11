from django.contrib import admin
from .models import Apunte

@admin.register(Apunte)
class ApunteAdmin(admin.ModelAdmin):
    list_display = ("usuario", "titulo", "materia", "fecha_publicacion")
    ordering = ("fecha_publicacion", "materia")