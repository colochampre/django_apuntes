from django.shortcuts import render, get_object_or_404
from gestion_carreras.models import Carrera
from gestion_materias.models import Materia
from gestion_apuntes.models import Apunte

def listar_materias_por_carrera(request, carrera_id):
    """
    Lista las materias de una carrera y muestra los apuntes de una materia seleccionada.
    Si no se especifica una materia, no se muestra ningún apunte.
    """
    carrera = get_object_or_404(Carrera, id=carrera_id) 
    materias = carrera.materias.all().order_by("nombre")
    
    materia_seleccionada = None
    apuntes = []

    materia_id = request.GET.get('materia_id')
    if materia_id:
        materia_seleccionada = get_object_or_404(Materia, id=materia_id)

    if materia_seleccionada:
        apuntes = Apunte.objects.filter(materia=materia_seleccionada).order_by("-fecha_publicacion")

    context = {
        "carrera": carrera, 
        "materias": materias,
        "materia_seleccionada": materia_seleccionada,
        "apuntes": apuntes
    }
    return render(request, "gestion_materias/lista_materias.html", context)