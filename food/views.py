from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Salesman, Comment


def index(request):
    return HttpResponse("Viva DIAM. Esta e a pagina de entrada da app votacao.")

def productDetailPage(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'food')

def mapPage(request):
    return render(request, 'food/mercadinhos_map.html', {})

def aboutPage(request):
    return render(request, 'food/about.html', {})
