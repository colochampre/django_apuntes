from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
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
        'usuario_profile': usuario_profile
    })

def custom_logout(request):
    logout(request)
    return redirect('home')
