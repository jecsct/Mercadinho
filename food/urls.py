from django.urls import include, path
from . import views

from .views import redirect_view

app_name = 'food'
urlpatterns = [
    path('', redirect_view),
    path('food/', views.index, name='index'),
    path('registar-utilizador/', views.registarutilizador, name='registarutilizador'),
    path('login-utilizador/', views.loginutilizador, name='loginutilizador'),
    path('logout-utilizador/', views.logoututilizador, name='logoututilizador'),
    # path("", views.index, name="index"),
    path('maps/', views.mapPage, name='mapPage'),
    path('about/', views.aboutPage, name='aboutPage'),
    path('<int:questao_id>', views.productDetailPage, name='productDetailPage'),
]
