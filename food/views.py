from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from food.models import Mensagem
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Product, Salesman, Comment


def redirect_view(request):
  return redirect('/food')

def index(request):
  return render(request, 'food/index.html')

def contactos(request):
  if request.method == 'POST':
    if request.user.is_authenticated:
      email_resposta=request.user.email
      try:
        texto_mensagem = request.POST.get("texto")
      except KeyError:
        return render(request, 'food/contactos.html')
    else:
      try:
        email_resposta = request.POST.get("email")
        texto_mensagem = request.POST.get("texto")
      except KeyError:
        return render(request, 'food/contactos.html')
    if email_resposta and texto_mensagem:
      mensagem = Mensagem(email_resposta=email_resposta, texto_mensagem=texto_mensagem, dataHora=timezone.now())
      mensagem.save()
      return  HttpResponseRedirect(reverse('food:contactos'))
    else:
      return HttpResponseRedirect(reverse('food:contactos'))
  else:
    return render(request, 'food/contactos.html')

def caixaMensagens(request):
  lista_mensagens = Mensagem.objects.order_by('-dataHora')
  return render(request, 'food/caixaMensagens.html', {'lista_mensagens':lista_mensagens})

def cestoCompras(request):
  #cesto_compras =
  #return render(request, 'food/cestoCompras.html', {'cesto_compras':cesto_compras})
  return render(request, 'food/cestoCompras.html')

def adicionarCesto(request):
  return render(request, 'food/cestoCompras.html')

def removerCesto(request):
  return render(request, 'food/cestoCompras.html')


def registarutilizador(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
        except KeyError:
            return render(request, 'food/registarutilizador.html')
        if username and email and password:
            User.objects.create_user(username=username, email=email, password=password)
            return HttpResponseRedirect(reverse('food:index'))
        else:
            return render(request, 'food/registarutilizador.html')
    else:
        return render(request, 'food/registarutilizador.html')


def loginutilizador(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
        except KeyError:
            return render(request, 'food/loginutilizador.html')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('food:index'))
            else:
                return render(request, 'food/loginutilizador.html',
                              {'error_message': "Utilizador não existe, tente de novo com outro username/password"})
        else:
            return render(request, 'food/loginutilizador.html')
    else:
        return render(request, 'food/loginutilizador.html')


def logoututilizador(request):
    logout(request)
    return HttpResponseRedirect(reverse('food:index'))

def mapPage(request):
    return render(request, 'food/mercadinhos_map.html')

def aboutPage(request):
    return render(request, 'food/about.html')

def productDetailPage(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'food/detalhe.html', {'product': product})
