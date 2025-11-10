from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'nombre_completo', 'listar_carreras')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('carrera',)
    ordering = ('user__first_name', 'user__last_name')

    fieldsets = (
        ('Información del usuario', {
            'fields': ('user',),
        }),
        ('Carreras asociadas', {
            'fields': ('carrera',),
        }),
    )

    filter_horizontal = ('carrera',)  # mejor visualización del ManyToMany

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Usuario'

    def nombre_completo(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    nombre_completo.short_description = 'Nombre completo'

    def listar_carreras(self, obj):
        return ", ".join([c.nombre for c in obj.carrera.all()])
    listar_carreras.short_description = 'Carreras'
