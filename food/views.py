from django.shortcuts import render
from django.http import HttpResponse


def index(request):
  return HttpResponse("Viva DIAM! Esta e a pagina de entrada da app votacao.")

def contactos(request):
  #if request.method == 'POST':

  #else:
  return render(request, 'food/contactos.html')
