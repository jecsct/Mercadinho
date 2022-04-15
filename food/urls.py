from django.urls import include, path
from . import views

from .views import redirect_view

app_name= 'food'
urlpatterns = [
  path("", views.index, name="index"),
  path("contactos/", views.contactos, name="contactos"),
  path("caixaMensagens/", views.caixaMensagens, name="Caixa Mensagens"),
  path("cestoCompras/", views.cestoCompras, name="Cesto Compras"),
  path("removerCesto", views.removerCesto, name="Remover Cesto"),
  path('', redirect_view),
  path('food', views.index, name='index'),
  path('registar-utilizador',views.registarutilizador,name='registarutilizador'),
  path('login-utilizador',views.loginutilizador,name='loginutilizador'),
  path('logout-utilizador',views.logoututilizador,name='logoututilizador')
]