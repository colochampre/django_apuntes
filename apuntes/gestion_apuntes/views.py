from django.shortcuts import render

# Create your views here.
def apuntes(request):
    return render(request, 'gestion_apuntes/apuntes.html')

