from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Prefetch
from gestion_carreras.models import Carrera
from gestion_materias.models import Materia
from gestion_apuntes.models import Apunte, Puntuacion
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
        usuario_actual, _ = Usuario.objects.get_or_create(user=request.user)

    materia_id = request.GET.get('materia_id')
    if materia_id:
        materia_seleccionada = get_object_or_404(Materia, id=materia_id)

    if materia_seleccionada:
        apuntes_list = Apunte.objects.filter(materia=materia_seleccionada).order_by("-fecha_publicacion")
        
        # Aplicar búsqueda si hay término de búsqueda
        search_query = request.GET.get('q', '').strip()
        if search_query:
            from django.db.models import Q
            apuntes_list = apuntes_list.filter(
                Q(titulo__icontains=search_query) | 
                Q(descripcion__icontains=search_query)
            )
            
        # Optimización: Prefetch de puntuaciones del usuario actual
        if usuario_actual:
            apuntes_list = apuntes_list.prefetch_related(
                Prefetch(
                    'puntuaciones',
                    queryset=Puntuacion.objects.filter(usuario=usuario_actual),
                    to_attr='user_score_list'
                )
            )
        
        # Configurar paginación: 12 apuntes por página
        # Divisible por 1, 2, 3 y 4 para filas completas en todos los breakpoints responsive:
        # - 1 columna (móvil): 12 filas
        # - 2 columnas (tablet): 6 filas
        # - 3 columnas (desktop): 4 filas
        # - 4 columnas (pantallas grandes): 3 filas
        paginator = Paginator(apuntes_list, 12)
        page = request.GET.get('page')
        
        try:
            apuntes = paginator.page(page)
        except PageNotAnInteger:
            # Si page no es un entero, mostrar la primera página
            apuntes = paginator.page(1)
        except EmptyPage:
            # Si page está fuera de rango, mostrar la última página
            apuntes = paginator.page(paginator.num_pages)
        
        # Agregar la puntuación del usuario actual a cada apunte (usando los datos pre-cargados)
        if usuario_actual:
            for apunte in apuntes:
                # Usamos la lista pre-cargada en lugar de hacer una query por cada apunte
                if hasattr(apunte, 'user_score_list') and apunte.user_score_list:
                    apunte.puntuacion_del_usuario = apunte.user_score_list[0].valor
                else:
                    apunte.puntuacion_del_usuario = None

    context = {
        "carrera": carrera, 
        "materias": materias,
        "materia_seleccionada": materia_seleccionada,
        "apuntes": apuntes,
        "usuario_actual": usuario_actual,
        "search_query": request.GET.get('q', '')
    }
    return render(request, "gestion_materias/lista_materias.html", context)