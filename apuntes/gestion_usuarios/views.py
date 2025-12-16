"""
Vistas para la gestión de usuarios.

Contiene las funciones para manejar el registro de usuarios, edición de perfiles,
inicio y cierre de sesión (lógica adicional), y visualización de perfiles públicos.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UsuarioCreationForm, UserEditForm, UsuarioProfileForm
from .models import Usuario

def registro(request):
    """
    Gestiona el registro de nuevos usuarios.

    Maneja tanto la solicitud GET para mostrar el formulario como la POST para procesarlo.
    Si el registro es exitoso, inicia sesión automáticamente y redirige.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.

    Returns:
        HttpResponse: La página de registro renderizada o una redirección.
    """
    # Capturar 'next' de GET o POST para persistencia
    next_url = request.GET.get('next') or request.POST.get('next', '')
    
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            if next_url:
                return redirect(next_url)
            return redirect('home')
    else:
        form = UsuarioCreationForm()
        
    return render(request, 'gestion_usuarios/register.html', {
        'form': form,
        'next': next_url
    })

@login_required
def perfil(request):
    """
    Permite al usuario autenticado ver y editar su propio perfil.

    Maneja la edición de los datos básicos del usuario (User) y los datos extendidos (Usuario).

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.

    Returns:
        HttpResponse: La página de perfil renderizada.
    """
    usuario_profile, _ = Usuario.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UsuarioProfileForm(request.POST, instance=usuario_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('gestion_usuarios:perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UsuarioProfileForm(instance=usuario_profile)

    return render(request, 'gestion_usuarios/perfil.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_user': request.user,
        'usuario_profile': usuario_profile,
        'es_propio': True
    })

def custom_logout(request):
    """
    Cierra la sesión del usuario actual y redirige a la página de inicio.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.

    Returns:
        HttpResponse: Redirección a la página de inicio.
    """
    logout(request)
    return redirect('home')

def ver_perfil_usuario(request, username):
    """
    Vista pública del perfil de un usuario.
    
    Muestra información básica y estadísticas del usuario.
    Muestra información personal solo si el usuario está viendo su propio perfil.
    
    Args:
        request (HttpRequest): El objeto de solicitud HTTP.
        username (str): El nombre de usuario del perfil a visualizar.

    Returns:
        HttpResponse: La página de perfil renderizada.
    """
    profile_user = get_object_or_404(User, username=username)
    
    usuario_profile, _ = Usuario.objects.get_or_create(user=profile_user)
    
    # Determinar si el usuario actual está viendo su propio perfil
    es_propio = request.user.is_authenticated and request.user == profile_user
    
    return render(request, 'gestion_usuarios/perfil.html', {
        'profile_user': profile_user,
        'usuario_profile': usuario_profile,
        'es_propio': es_propio
    })
