from django.urls import include, path
from . import views

app_name= 'food'
urlpatterns = [
  path('', views.index, name='index'),
  path('registar-utilizador',views.registarutilizador,name='registarutilizador'),
  path('login-utilizador',views.loginutilizador,name='loginutilizador'),
  path('logout-utilizador',views.logoututilizador,name='logoututilizador'),
]