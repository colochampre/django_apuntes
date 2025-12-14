from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UsuarioCreationForm, UserEditForm, UsuarioProfileForm
from .models import Usuario

def registro(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UsuarioCreationForm()
    return render(request, 'gestion_usuarios/register.html', {'form': form})

@login_required
def perfil(request):
    try:
        usuario_profile = request.user.usuario
    except Usuario.DoesNotExist:
        usuario_profile = Usuario.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UsuarioProfileForm(request.POST, instance=usuario_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('perfil')
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
    logout(request)
    return redirect('home')

def ver_perfil_usuario(request, username):
    """
    Vista pública de perfil de usuario.
    Muestra información personal solo si el usuario está viendo su propio perfil.
    """
    profile_user = get_object_or_404(User, username=username)
    
    try:
        usuario_profile = profile_user.usuario
    except Usuario.DoesNotExist:
        usuario_profile = Usuario.objects.create(user=profile_user)
    
    # Determinar si el usuario actual está viendo su propio perfil
    es_propio = request.user.is_authenticated and request.user == profile_user
    
    return render(request, 'gestion_usuarios/perfil.html', {
        'profile_user': profile_user,
        'usuario_profile': usuario_profile,
        'es_propio': es_propio
    })
