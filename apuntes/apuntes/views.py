"""
Vistas principales del proyecto.

Este módulo contiene las vistas generales que no pertenecen a una aplicación específica,
como la página de inicio y el registro de usuarios.
"""

from django.shortcuts import render

def home(request):
    """
    Renderiza la página de inicio del sitio.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con la plantilla 'home.html' renderizada.
    """
    return render(request, 'home.html')

def registro(request):
    """
    Gestiona el registro de nuevos usuarios.

    Si la solicitud es POST, procesa el formulario de registro. Si es válida,
    crea el usuario, inicia sesión y redirige a la página correspondiente.
    Si la solicitud es GET, muestra el formulario de registro vacío.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con la plantilla de registro o una redirección.
    """
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Obtener el parámetro 'next' de la URL
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
    else:
        form = UsuarioCreationForm()
    return render(request, 'gestion_usuarios/register.html', {'form': form})
