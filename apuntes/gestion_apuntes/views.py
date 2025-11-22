from django.shortcuts import render, redirect
from gestion_usuarios.models import Usuario
from gestion_materias.models import Materia
from .forms import ApunteForm
from .models import Apunte # Import Apunte model to get the ID for redirect

# Create your views here.
def apuntes(request):
    # This view likely lists all apuntes or a filtered set
    # For now, it just renders a template.
    # We might want to redirect to a specific materia's apuntes after upload.
    return render(request, 'gestion_apuntes/apuntes.html')

def subir_apunte(request):
    if request.method == 'POST':
        form = ApunteForm(request.POST, request.FILES)
        if form.is_valid():
            apunte = form.save(commit=False)
            # Assuming the user is logged in
            # You might need to get the Usuario object associated with request.user
            # For simplicity, let's assume request.user is directly the Usuario instance or can be queried.
            # If request.user is Django's default User model, you'd need:
            try:
                apunte.usuario = Usuario.objects.get(user=request.user)
            except Usuario.DoesNotExist:
                # Handle case where Usuario profile doesn't exist for the logged-in User
                # Maybe redirect to profile creation or show an error
                pass # For now, let's proceed, though it might error if apunte.usuario is not set.

            apunte.save()
            # Redirect to the list of apuntes for the specific materia if possible
            if apunte.materia:
                return redirect('gestion_materias:apuntes_por_materia', materia_id=apunte.materia.id)
            else:
                return redirect('gestion_apuntes:apuntes') # Fallback to general apuntes list
    else:
        form = ApunteForm()
    
    context = {'form': form}
    return render(request, 'gestion_apuntes/subir_apunte.html', context)
