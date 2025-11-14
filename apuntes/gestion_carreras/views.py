from django.shortcuts import render
from .models import Carrera

# Create your views here.
def lista_carreras(request):
    carreras = Carrera.objects.all().order_by('nombre') # trae las carreras de la BD ordenadas por nombre
    return render(request, 'gestion_carreras/lista_carreras.html', {'carreras': carreras})  # envio la lista de carreras al template
