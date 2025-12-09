from django.contrib import admin
from .models import Apunte, Puntuacion

@admin.register(Apunte)
class ApunteAdmin(admin.ModelAdmin):
    list_display = ("usuario", "titulo", "materia", "fecha_publicacion")
    ordering = ("fecha_publicacion", "materia")

@admin.register(Puntuacion)
class PuntuacionAdmin(admin.ModelAdmin):
    list_display = ("apunte", "usuario", "valor", "fecha")
    list_filter = ("valor", "fecha")
    ordering = ("-fecha",)