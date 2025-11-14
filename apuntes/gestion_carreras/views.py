from django.shortcuts import render
from .models import Carrera
# Create your views here.
def lista_carreras(request):
    carreras = Carrera.objects.all() # trae todas las carreras de la BD
    return render(request, 'gestion_carreras/lista_carreras.html', {
        'carreras': carreras}) # envio la lista de carreras al template
