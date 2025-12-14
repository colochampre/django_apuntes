from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Carrera

def lista_carreras(request):
    """
    Obtiene y muestra una lista de todas las carreras, ordenadas por nombre.
    Incluye funcionalidad de búsqueda por nombre o universidad.
    """
    carreras = Carrera.objects.all().order_by('nombre')
    
    # Búsqueda
    search_query = request.GET.get('q', '').strip()
    if search_query:
        from django.db.models import Q
        carreras = carreras.filter(
            Q(nombre__icontains=search_query) |
            Q(universidad__icontains=search_query)
        )
    
    return render(request, 'gestion_carreras/lista_carreras.html', {
        'carreras': carreras,
        'search_query': search_query
    })

@login_required
def eliminar_carrera(request, carrera_id):
    """
    Elimina una carrera específica. Solo accesible para usuarios staff o superusuarios.
    """
    # Verificar que el usuario tenga permisos de administrador
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para eliminar carreras.')
        return redirect('gestion_carreras:lista_carreras')
    
    # Obtener la carrera o devolver 404 si no existe
    carrera = get_object_or_404(Carrera, id=carrera_id)
    nombre_carrera = carrera.nombre
    universidad = carrera.universidad
    
    # Eliminar la carrera
    carrera.delete()
    
    # Mensaje de éxito
    messages.success(request, f'La carrera "{nombre_carrera}" ({universidad}) ha sido eliminada exitosamente.')
    
    return redirect('gestion_carreras:lista_carreras')