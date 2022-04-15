from django.utils import timezone

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from food.models import Mensagem


def index(request):
  return HttpResponse("Viva DIAM! Esta e a pagina de entrada da app votacao.")

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
  lista_mensagens=Mensagem.objects.order_by('-dataHora')
  return render(request, 'food/caixaMensagens.html', {'lista_mensagens':lista_mensagens})

def cestoCompras(request):
  return render(request, 'food/cestoCompras.html')

def removerCesto(request):
  return render(request, 'food/cestoCompras.html')
