from django.contrib import admin
from .models import Carrera

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'universidad', 'get_materias')  # columnas visibles en la lista
    list_filter = ('universidad',)  # filtro lateral por universidad
    search_fields = ('nombre', 'universidad')  # barra de búsqueda
    ordering = ('nombre', 'universidad')
    list_per_page = 20  # número de elementos por página

    fieldsets = (
        ('Información general', {
            'fields': ('nombre', 'universidad')
        }),
    )

    def get_materias(self, obj):
        return ", ".join([f"{m.nombre} ({m.anio}°)" for m in obj.materias.all()])
    get_materias.short_description = 'Materias'  # nombre de la columna en el admin
