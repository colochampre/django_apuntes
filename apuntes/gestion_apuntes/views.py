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
    # Obtener carrera_id desde GET o POST
    carrera_id = request.GET.get('carrera_id') or request.POST.get('carrera_id')

    if request.method == 'POST':
        form = ApunteForm(request.POST, request.FILES, materia=materia)
        # Eliminamos el campo materia del formulario para que no se valide
        if 'materia' in form.fields:
            del form.fields['materia']
            
        if form.is_valid():
            apunte = form.save(commit=False)
            apunte.materia = materia # Asignamos la materia automáticamente
            
            # Asigna el usuario actual al apunte.
            apunte.usuario, _ = Usuario.objects.get_or_create(user=request.user)

            apunte.save()
            
            # Redirige a la lista de apuntes de la materia específica.
            # Usar carrera_id si está disponible, sino usar la primera carrera
            if carrera_id:
                url = reverse('gestion_materias:materias_por_carrera', kwargs={'carrera_id': carrera_id})
                return redirect(f'{url}?materia_id={materia.id}')
            else:
                carrera = materia.carreras.first()
                if carrera:
                    url = reverse('gestion_materias:materias_por_carrera', kwargs={'carrera_id': carrera.id})
                    return redirect(f'{url}?materia_id={materia.id}')
                else:
                    return redirect('gestion_apuntes:apuntes')
    else:
        form = ApunteForm(materia=materia)
        if 'materia' in form.fields:
            del form.fields['materia']
    
    context = {'form': form, 'materia': materia, 'carrera_id': carrera_id}
    return render(request, 'gestion_apuntes/subir_apunte.html', context)

def descargar_apunte(request, apunte_id):
    """
    Gestiona la descarga de un apunte.
    Si el usuario no está autenticado, redirige al login y luego vuelve a la página anterior iniciando la descarga.
    """
    if not request.user.is_authenticated:
        from django.contrib.auth import REDIRECT_FIELD_NAME
        from urllib.parse import urlparse, parse_qs, urlunparse, urlencode as urllib_urlencode

        # Obtener la página anterior (referer)
        referer = request.META.get('HTTP_REFERER', '/')
        
        # Parsear la URL para agregar el parámetro de descarga de forma segura
        parsed_ref = urlparse(referer)
        query = parse_qs(parsed_ref.query)
        query['download_pending'] = str(apunte_id)
        
        # Reconstruir la URL de retorno
        new_query_str = urllib_urlencode(query, doseq=True)
        next_url = urlunparse((
            parsed_ref.scheme,
            parsed_ref.netloc,
            parsed_ref.path,
            parsed_ref.params,
            new_query_str,
            parsed_ref.fragment
        ))
        
        # Redirigir al login con el next configurado
        login_url = reverse('gestion_usuarios:login')
        params = {REDIRECT_FIELD_NAME: next_url}
        return redirect(f"{login_url}?{urllib_urlencode(params)}")

    apunte = get_object_or_404(Apunte, id=apunte_id)
    
    # Servir el archivo
    response = FileResponse(apunte.archivo.open(), as_attachment=True, filename=apunte.archivo.name)
    
    return response

@login_required
def puntuar_apunte(request, apunte_id):
    """
    Permite a un usuario puntuar un apunte con un valor de 1 a 5.
    Si ya puntuó, actualiza su puntuación.
    Los autores no pueden puntuar sus propios apuntes.
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
        
        usuario, _ = Usuario.objects.get_or_create(user=request.user)
        
        # Verificar que el usuario no sea el autor del apunte
        if apunte.usuario == usuario:
            return JsonResponse({'error': 'No podés puntuar tu propio apunte'}, status=403)
        
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

@login_required
def eliminar_apunte(request, apunte_id):
    """
    Permite eliminar un apunte.
    Solo el autor del apunte, staff o superusuarios pueden eliminarlo.
    """
    from django.contrib import messages
    
    apunte = get_object_or_404(Apunte, id=apunte_id)
    
    # Verificar permisos: autor, staff o superuser
    es_autor = apunte.usuario and apunte.usuario.user == request.user
    es_staff = request.user.is_staff or request.user.is_superuser
    
    if not (es_autor or es_staff):
        messages.error(request, 'No tenés permisos para eliminar este apunte.')
        return redirect('gestion_apuntes:apuntes')
    
    # Guardar información para redirección
    materia = apunte.materia
    titulo_apunte = apunte.titulo
    
    # Obtener carrera_id desde el referer (URL anterior)
    referer = request.META.get('HTTP_REFERER', '')
    carrera_id = None
    
    # Intentar extraer carrera_id de la URL anterior
    if 'por_carrera/' in referer:
        try:
            # Extraer el ID de carrera de la URL
            import re
            match = re.search(r'/por_carrera/(\d+)/', referer)
            if match:
                carrera_id = match.group(1)
        except:
            pass
    
    # Eliminar el apunte
    apunte.delete()
    
    messages.success(request, f'El apunte "{titulo_apunte}" fue eliminado exitosamente.')
    
    # Redirigir a la lista de apuntes de la materia
    if carrera_id and materia:
        url = reverse('gestion_materias:materias_por_carrera', kwargs={'carrera_id': carrera_id})
        return redirect(f'{url}?materia_id={materia.id}')
    elif materia:
        # Fallback: usar la primera carrera
        carrera = materia.carreras.first()
        if carrera:
            url = reverse('gestion_materias:materias_por_carrera', kwargs={'carrera_id': carrera.id})
            return redirect(f'{url}?materia_id={materia.id}')
    
    return redirect('gestion_apuntes:apuntes')