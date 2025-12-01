from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from gestion_usuarios.models import Usuario
from gestion_materias.models import Materia
from .forms import ApunteForm
from .models import Apunte

def apuntes(request):
    """
    Vista para mostrar la página principal de apuntes.
    Actualmente, solo renderiza una plantilla estática.
    """
    return render(request, 'gestion_apuntes/apuntes.html')

@login_required
def subir_apunte(request):
    """
    Gestiona la subida de un nuevo apunte.
    Si el método es POST, procesa el formulario. Si es válido, guarda el apunte
    y redirige a la lista de apuntes de la materia correspondiente.
    Si el método es GET, muestra el formulario vacío.
    """
    if request.method == 'POST':
        form = ApunteForm(request.POST, request.FILES)
        if form.is_valid():
            apunte = form.save(commit=False)
            # Asigna el usuario actual al apunte.
            try:
                apunte.usuario = Usuario.objects.get(user=request.user)
            except Usuario.DoesNotExist:
                # Si el perfil de usuario no existe, se podría redirigir a una página de creación de perfil.
                # Por ahora, se omite para evitar errores si el usuario no está completamente configurado.
                pass

            apunte.save()
            
            # Redirige a la lista de apuntes de la materia específica.
            if apunte.materia:
                carrera = apunte.materia.carreras.first()
                if carrera:
                    url = reverse('gestion_materias:materias_por_carrera', kwargs={'carrera_id': carrera.id})
                    return redirect(f'{url}?materia_id={apunte.materia.id}')
                else:
                    # Si la materia no está asociada a ninguna carrera, redirige a la lista general de apuntes.
                    return redirect('gestion_apuntes:apuntes')
            else:
                # Si el apunte no tiene una materia asignada, redirige a la lista general.
                return redirect('gestion_apuntes:apuntes')
    else:
        form = ApunteForm()
    
    context = {'form': form}
    return render(request, 'gestion_apuntes/subir_apunte.html', context)

@login_required
def descargar_apunte(request, apunte_id):
    """
    Gestiona la descarga de un apunte.
    Verifica que el usuario esté autenticado y luego sirve el archivo.
    """
    apunte = get_object_or_404(Apunte, id=apunte_id)
    return FileResponse(apunte.archivo.open(), as_attachment=True, filename=apunte.archivo.name)

