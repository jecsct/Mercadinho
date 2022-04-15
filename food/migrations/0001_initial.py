# Generated by Django 4.0.4 on 2022-04-15 16:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Salesman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('phone_number', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(900000000), django.core.validators.MaxValueValidator(999999999)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('image', models.ImageField(upload_to='food_pics')),
                ('sales', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('views', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('salesman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.salesman')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=10000)),
                ('dataHour', models.DateTimeField()),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
    ]
