from django.urls import include, path
from . import views

app_name = 'food'
urlpatterns = [
  path("", views.index, name="index"),
  path("contactos/", views.contactos, name="contactos")
]