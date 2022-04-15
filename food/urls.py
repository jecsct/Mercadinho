from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("maps/", views.mapPage, name="mapPage"),
    path("about/", views.aboutPage, name="aboutPage"),
    path('<int:product_id>', views.productDetailPage, name='productDetailPage'),
]
