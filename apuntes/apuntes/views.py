from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def registro(request):
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
