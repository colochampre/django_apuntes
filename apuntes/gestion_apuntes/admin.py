from django.contrib import admin
from .models import Apunte

@admin.register(Apunte)
class ApunteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'materia', 'usuario', 'fecha_publicacion')  # columnas visibles en la lista
    list_filter = ('materia', 'fecha_publicacion')  # filtros laterales
    search_fields = ('titulo', 'descripcion', 'usuario__user__username')  # barra de búsqueda
    ordering = ('titulo',)
    readonly_fields = ('fecha_publicacion',)  # evita modificar la fecha desde el admin

    fieldsets = (
        ('Información general', {
            'fields': ('titulo', 'descripcion', 'archivo')
        }),
        ('Relaciones', {
            'fields': ('materia', 'usuario')
        }),
        ('Metadatos', {
            'fields': ('fecha_publicacion',),
        }),
    )
