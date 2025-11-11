from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("user__username", "mostrar_carreras")
    ordering = ("carrera", "user__username")
    
    def mostrar_carreras(self, obj):
        return ", " .join([c.nombre for c in obj.carrera.all()])
    mostrar_carreras.short_description = "carreras"