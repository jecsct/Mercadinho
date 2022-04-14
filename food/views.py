from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Viva DIAM. Esta e a pagina de entrada da app votacao.")


def mapPage(request):
    return render(request, 'food/mercadinhos_map.html', {})

def aboutPage(request):
    return render(request, 'food/about.html', {})
