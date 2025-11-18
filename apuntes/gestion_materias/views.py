from django.shortcuts import render, get_object_or_404
from gestion_carreras.models import Carrera


# Create your views here.
def listar_materias_por_carrera(request, carrera_id):
    # Obtenemos la carrera específica o mostramos un error 404 si no existe
    carrera = get_object_or_404(Carrera, id=carrera_id)

    # Obtenemos todas las materias asociadas a esa carrera
    materias = carrera.materias.all().order_by("nombre")

    context = {"carrera": carrera, "materias": materias}

    return render(request, "gestion_materias/lista_materias.html", context)
