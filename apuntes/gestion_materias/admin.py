from django.contrib import admin
from .models import Materia

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'anio')  # columnas visibles en la lista principal
    list_filter = ('anio',)  # filtro lateral por año
    search_fields = ('nombre',)  # barra de búsqueda por nombre
    ordering = ('anio', 'nombre')

    fieldsets = (
        ('Información de la materia', {
            'fields': ('nombre', 'anio'),
            'description': 'Datos básicos de la materia.'
        }),
    )
