from django.shortcuts import render, get_object_or_404
from gestion_carreras.models import Carrera
from gestion_materias.models import Materia
from gestion_apuntes.models import Apunte

# Create your views here.
def listar_materias_por_carrera(request, carrera_id):
    carrera = get_object_or_404(Carrera, id=carrera_id) 
    materias = carrera.materias.all().order_by("nombre")
    
    materia_seleccionada = None
    apuntes = []

    materia_id = request.GET.get('materia_id')
    if materia_id:
        materia_seleccionada = get_object_or_404(Materia, id=materia_id)
    elif materias.exists():
        materia_seleccionada = materias.first()

    if materia_seleccionada:
        apuntes = Apunte.objects.filter(materia=materia_seleccionada).order_by("-fecha_publicacion")

    context = {
        "carrera": carrera, 
        "materias": materias,
        "materia_seleccionada": materia_seleccionada,
        "apuntes": apuntes
    }
    return render(request, "gestion_materias/lista_materias.html", context)