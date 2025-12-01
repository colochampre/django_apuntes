from django.shortcuts import render
from .models import Carrera

def lista_carreras(request):
    """
    Obtiene y muestra una lista de todas las carreras, ordenadas por nombre.
    """
    carreras = Carrera.objects.all().order_by('nombre')  # Obtiene las carreras de la base de datos ordenadas por nombre
    return render(request, 'gestion_carreras/lista_carreras.html', {'carreras': carreras})  # Envía la lista de carreras al template