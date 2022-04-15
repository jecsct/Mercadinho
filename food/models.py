from django.db import models

# Create your models here.
class Mensagem(models.Model):
    email_resposta=models.CharField(max_length=50)
    texto_mensagem=models.CharField(max_length=500)