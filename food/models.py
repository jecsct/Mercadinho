from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Mensagem(models.Model):
    email_resposta = models.CharField(max_length=50)
    texto_mensagem = models.CharField(max_length=500)
    dataHora = models.DateTimeField('Data Mensagem Enviada')

# Create your models here.
class Salesman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.DecimalField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], max_digits=2,
                                 decimal_places=1)
    phone_number = models.IntegerField(blank=True,
                                       validators=[MinValueValidator(900000000), MaxValueValidator(999999999)])

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='food_pics')
    sales = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    views = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    rating = models.DecimalField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], max_digits=2,
                                 decimal_places=1)
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    dataHour = models.DateTimeField()
    rating = models.DecimalField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], max_digits=2,
                                 decimal_places=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "product"),)
