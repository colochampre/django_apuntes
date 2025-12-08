from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from gestion_usuarios.models import Usuario
from gestion_materias.models import Materia
from .forms import ApunteForm
from .models import Apunte, Puntuacion

def apuntes(request):
    """
    Vista para mostrar la página principal de apuntes.
    Actualmente, solo renderiza una plantilla estática.
    """
    return render(request, 'gestion_apuntes/lista_apuntes.html')

@login_required
def subir_apunte(request, materia_id):
    """
    Gestiona la subida de un nuevo apunte para una materia específica.
    """
    materia = get_object_or_404(Materia, pk=materia_id)

    if request.method == 'POST':
        form = ApunteForm(request.POST, request.FILES)
        # Eliminamos el campo materia del formulario para que no se valide
        if 'materia' in form.fields:
            del form.fields['materia']
            
        if form.is_valid():
            apunte = form.save(commit=False)
            apunte.materia = materia # Asignamos la materia automáticamente
            
            # Asigna el usuario actual al apunte.
            try:
                apunte.usuario = Usuario.objects.get(user=request.user)
            except Usuario.DoesNotExist:
                pass

            apunte.save()
            
            # Redirige a la lista de apuntes de la materia específica.
            carrera = materia.carreras.first()
            if carrera:
                url = reverse('gestion_materias:materias_por_carrera', kwargs={'carrera_id': carrera.id})
                return redirect(f'{url}?materia_id={materia.id}')
            else:
                return redirect('gestion_apuntes:apuntes')
    else:
        form = ApunteForm()
        if 'materia' in form.fields:
            del form.fields['materia']
    
    context = {'form': form, 'materia': materia}
    return render(request, 'gestion_apuntes/subir_apunte.html', context)

@login_required
def descargar_apunte(request, apunte_id):
    """
    Gestiona la descarga de un apunte.
    Verifica que el usuario esté autenticado y luego sirve el archivo.
    """
    apunte = get_object_or_404(Apunte, id=apunte_id)
    return FileResponse(apunte.archivo.open(), as_attachment=True, filename=apunte.archivo.name)

@login_required
def puntuar_apunte(request, apunte_id):
    """
    Permite a un usuario puntuar un apunte con un valor de 1 a 5.
    Si ya puntuó, actualiza su puntuación.
    """
    if request.method == 'POST':
        apunte = get_object_or_404(Apunte, id=apunte_id)
        valor = request.POST.get('valor')
        
        try:
            valor = int(valor)
            if valor < 1 or valor > 5:
                return JsonResponse({'error': 'Valor inválido'}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Valor inválido'}, status=400)
        
        try:
            usuario = Usuario.objects.get(user=request.user)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=400)
        
        # Crear o actualizar la puntuación
        puntuacion, created = Puntuacion.objects.update_or_create(
            apunte=apunte,
            usuario=usuario,
            defaults={'valor': valor}
        )
        
        # Calcular el nuevo promedio
        promedio = apunte.promedio_puntuacion()
        total = apunte.total_puntuaciones()
        
        return JsonResponse({
            'success': True,
            'promedio': promedio,
            'total': total,
            'tu_puntuacion': valor,
            'mensaje': 'Puntuación actualizada' if not created else 'Puntuación registrada'
        })
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)