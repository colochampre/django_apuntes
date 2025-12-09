from django.shortcuts import render, get_object_or_404
from gestion_carreras.models import Carrera
from gestion_materias.models import Materia
from gestion_apuntes.models import Apunte
from gestion_usuarios.models import Usuario

def listar_materias_por_carrera(request, carrera_id):
    """
    Lista las materias de una carrera y muestra los apuntes de una materia seleccionada.
    Si no se especifica una materia, no se muestra ningún apunte.
    """
    carrera = get_object_or_404(Carrera, id=carrera_id) 
    materias = carrera.materias.all().order_by("nombre")
    
    materia_seleccionada = None
    apuntes = []
    usuario_actual = None

    # Obtener o crear el usuario actual si está autenticado
    if request.user.is_authenticated:
        try:
            usuario_actual = Usuario.objects.get(user=request.user)
        except Usuario.DoesNotExist:
            # Crear automáticamente el objeto Usuario si no existe
            usuario_actual = Usuario.objects.create(user=request.user)
            usuario_actual.save()

    materia_id = request.GET.get('materia_id')
    if materia_id:
        materia_seleccionada = get_object_or_404(Materia, id=materia_id)

    if materia_seleccionada:
        apuntes = Apunte.objects.filter(materia=materia_seleccionada).order_by("-fecha_publicacion")
        
        # Agregar la puntuación del usuario actual a cada apunte
        if usuario_actual:
            for apunte in apuntes:
                apunte.puntuacion_del_usuario = apunte.puntuacion_usuario(usuario_actual)

    context = {
        "carrera": carrera, 
        "materias": materias,
        "materia_seleccionada": materia_seleccionada,
        "apuntes": apuntes,
        "usuario_actual": usuario_actual
    }
    return render(request, "gestion_materias/lista_materias.html", context)