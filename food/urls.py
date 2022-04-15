from django.urls import include, path
from . import views

app_name = 'food'
urlpatterns = [
  path("", views.index, name="index"),
  path("contactos/", views.contactos, name="contactos"),
  path("caixaMensagens/", views.caixaMensagens, name="Caixa Mensagens"),
  path("cestoCompras/", views.cestoCompras, name="Cesto Compras"),
  path("removerCesto", views.removerCesto, name="Remover Cesto")
]