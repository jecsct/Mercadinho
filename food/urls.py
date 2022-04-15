from django.urls import include, path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("contactos", views.contactos, name="contactos")
]