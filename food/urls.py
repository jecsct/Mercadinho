from django.urls import include, path
from . import views

#from .views import redirect_view

app_name = 'food'
urlpatterns = [
    path("", views.index, name="index"),
    path("contactos/", views.contactos, name="contactos"),
    path("caixaMensagens/", views.caixaMensagens, name="caixamensagens"),
    path("cestoCompras", views.cestoCompras, name="cestocompras"),
    path("perfil", views.perfil, name="perfil"),
    #path('', redirect_view),
    path('registerCustomer', views.registarCustomer, name='registarCustomer'),
    path('registerSalesman', views.registarSalesman, name='registarSalesman'),
    path('loginUser', views.loginutilizador, name='loginutilizador'),
    path('logout-utilizador', views.logoututilizador, name='logoututilizador'),
    path('maps', views.mapPage, name='mapPage'),
    path('about/', views.aboutPage, name='about'),
    path('<int:product_id>/', views.productDetailPage, name='productDetailPage'),
    # path('<int:product_id>/commentOnItem/', views.commentOnItem, name='commentOnItem'),
    path('<int:product_id>/commentOnItem/', views.commentOnItem, name='commentOnItem'),
    path('<int:product_id>/updateProductComment/', views.updateProductComment, name='updateProductComment'),
    path('<int:product_id>/deleteProductComment/', views.deleteProductComment, name='deleteProductComment'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('pagamento/', views.pagamento, name="pagamento"),
    path('<int:product_id>/addToCart', views.addToCart, name='addToCart'),
    path('<int:cestoCompras_id>/removeFromCart', views.removeFromCart, name='removeFromCart'),
    path('pagamento/cestoCompras', views.cestoCompras, name="cesto compras"),
    path('<int:product_id>/deleteProduct/', views.deleteProduct, name='deleteProduct'),
    path('checkOut', views.checkOut, name='checkOut'),
    path('investCrypto', views.investCrypto, name='investCrypto')
]
