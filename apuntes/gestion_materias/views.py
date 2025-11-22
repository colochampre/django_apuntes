from django.shortcuts import render, get_object_or_404
from gestion_carreras.models import Carrera
from gestion_materias.models import Materia
from gestion_apuntes.models import Apunte

# Create your views here.
def listar_materias_por_carrera(request, carrera_id):
    carrera = get_object_or_404(Carrera, id=carrera_id) 
    materias = carrera.materias.all().order_by("nombre")
    context = {"carrera": carrera, "materias": materias}
    return render(request, "gestion_materias/lista_materias.html", context)

def apuntes_por_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    apuntes = Apunte.objects.filter(materia=materia).order_by("-fecha_publicacion")
    context = {"materia": materia, "apuntes": apuntes}
    return render(request, "gestion_materias/apuntes_por_materia.html", context)