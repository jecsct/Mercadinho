from django.shortcuts import render
from django.http import HttpResponse


def index(request):
  return HttpResponse("Viva DIAM! Esta e a pagina de entrada da app votacao.")

def contactos(request):
  if request.method == 'POST':
    try:
      email_resposta = request.POST.get("email")
      texto_mensagem = request.POST.get("texto")
    except KeyError:
      return render(request,'food/contactos.html')
    if email_resposta and texto_mensagem:
      mensagem = Mensagem(email_resposta=email_resposta, texto_mensagem=texto_mensagem)
  else:
    return render(request, 'food/contactos.html')
