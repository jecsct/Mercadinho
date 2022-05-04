from django.urls import include, path
from . import views

from .views import redirect_view

app_name = 'food'
urlpatterns = [

    path("", views.index, name="index"),
    path("contactos/", views.contactos, name="contactos"),
    path("caixaMensagens/", views.caixaMensagens, name="caixamensagens"),
    path("cestoCompras/", views.cestoCompras, name="cestocompras"),
    path("removerCesto/", views.removerCesto, name="removercesto"),
    path("perfil", views.perfil, name="perfil"),
    path('', redirect_view),
    path('registar-utilizador', views.registarutilizador, name='registarutilizador'),
    path('login-utilizador', views.loginutilizador, name='loginutilizador'),
    path('logout-utilizador', views.logoututilizador, name='logoututilizador'),
    path('maps', views.mapPage, name='mapPage'),
    path('about/', views.aboutPage, name='about'),
    path('<int:product_id>/', views.productDetailPage, name='productDetailPage'),
    # path('<int:product_id>/commentOnItem/', views.commentOnItem, name='commentOnItem'),
    path('<int:product_id>/commentOnItem/', views.commentOnItem, name='commentOnItem'),
    path('<int:product_id>/updateProductComment/', views.updateProductComment, name='updateProductComment'),
    path('<int:product_id>/deleteProductComment/', views.deleteProductComment, name='deleteProductComment'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('<int:product_id>/deleteProduct/', views.deleteProduct, name='deleteProduct'),

    path('base/', views.base, name='base'),
]
