from django.contrib import admin
from .models import Materia

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "anio")
    ordering = ("anio", "nombre")
    