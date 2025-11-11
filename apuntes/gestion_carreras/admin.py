from django.contrib import admin
from .models import Carrera

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ("nombre", "universidad", "get_materias")
    filter_horizontal = ("materias",)
    list_filter = ("materias",)
    fields = ["nombre", "universidad","materias"]
    
    def get_materias(self, obj):
        return ", " .join ([materia.nombre for materia in obj.materias.all ()])
    get_materias.short_description = "materias"
   
