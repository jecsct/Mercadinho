from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# Create your models here.
class Mensagem(models.Model):
    email = models.CharField(max_length=50)
    texto_mensagem = models.CharField(max_length=500)
    dataHora = models.DateTimeField()
    tratada = models.BooleanField()

# Create your models here.
class Salesman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.DecimalField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], max_digits=2,
                                 decimal_places=1)
    profile_pic = models.ImageField()
    phone_number = models.IntegerField(blank=True,
                                       validators=[MinValueValidator(900000000), MaxValueValidator(999999999)])

    def addRating(self, newRating):
        stats = self.getRatingSum()
        totalSum = stats[0]
        totalRatings = stats[1]
        Salesman.objects.filter(id=self.id).update(
            rating=((float(totalSum) + float(newRating)) / (float(totalRatings) + 1)))

    def deleteRating(self, oldRating):
        stats = self.getRatingSum()
        totalSum = stats[0]
        totalRatings = stats[1]
        if totalRatings != 1:
            print((totalSum - float(self.rating)))
            print(totalRatings - 1)
            Salesman.objects.filter(id=self.id).update(rating=((totalSum - float(oldRating)) / (totalRatings - 1)))
        else:
            Salesman.objects.filter(id=self.id).update(rating=((totalSum - float(oldRating)) / totalRatings))

    def updateRating(self, oldRating, newRating):
        stats = self.getRatingSum()
        totalSum = stats[0]
        totalRatings = stats[1]
        Salesman.objects.filter(id=self.id).update(
            rating=(totalSum - float(oldRating) + float(newRating)) / totalRatings)

    def getRatingSum(self):
        totalSum = 0.0
        totalRatings = 0
        for p in Product.objects.all().filter(salesman_id=self.id):
            if p.rating != 0:
                totalSum = totalSum + float(p.rating)
                totalRatings += 1
        return totalSum, totalRatings


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='static/media/', blank=True)
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    gender = models.CharField(max_length=6, null=True, blank=True, choices=gender)
    birthday = models.DateField()
    credit = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    sales = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    views = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    rating = models.DecimalField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], max_digits=2,
                                 decimal_places=1)
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE)

    def addRating(self, newRating):
        comments = self.getExistingComments()
        ratingSum = float(newRating)
        for comment in comments:
            ratingSum = ratingSum + float(comment.rating)
        totalRatings = len(Comment.objects.all().filter(product_id=self.id))
        Product.objects.filter(id=self.id).update(rating=(ratingSum / (totalRatings + 1)))

    def deleteRating(self, oldRating):
        comments = self.getExistingComments()
        ratingSum = float(oldRating) * -1
        for comment in comments:
            ratingSum = ratingSum + float(comment.rating)
        totalRatings = len(Comment.objects.all().filter(product_id=self.id))
        if (totalRatings - 1) != 0:
            Product.objects.filter(id=self.id).update(rating=(ratingSum / (totalRatings - 1)))
        else:
            Product.objects.filter(id=self.id).update(rating=(ratingSum / totalRatings))

    def updateRating(self, oldRating, newRating):
        comments = self.getExistingComments()
        ratingSum = float(newRating) - float(oldRating)
        for comment in comments:
            ratingSum = ratingSum + float(comment.rating)
        totalRatings = len(Comment.objects.all().filter(product_id=self.id))
        Product.objects.filter(id=self.id).update(rating=(ratingSum / totalRatings))

    def addView(self):
        Product.objects.filter(id=self.id).update(views=self.views + 1)

    def getExistingComments(self):
        try:
            comments = Comment.objects.all().filter(product_id=self.id)
        except Comment.DoesNotExist:
            comments = []
        return comments


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    dataHour = models.DateTimeField()
    rating = models.DecimalField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], max_digits=2,
                                 decimal_places=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "product"),)


class CestoCompras(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
