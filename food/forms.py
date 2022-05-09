from django.forms import ModelForm, EmailInput, DateInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime

from food.models import Customer, Mensagem, Salesman, Product
from django import forms


class UserForm(UserCreationForm):
    password1 = forms.PasswordInput()
    username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')
        widgets = {
            "email": EmailInput(attrs={'type': 'email'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        del self.fields['password2']


class CustomerForm(ModelForm):
    credit = forms.IntegerField(initial=0)
    class Meta:
        model = Customer
        fields = ('gender', 'profile_pic', 'birthday', 'credit')
        widgets = {
            "birthday": DateInput(attrs={'type': 'date'}),
        }


class SalesmanForm(ModelForm):
    rating = forms.IntegerField(initial=0)

    class Meta:
        model = Salesman
        fields = ('rating', 'profile_pic', 'phone_number')


class ContactForm(ModelForm):
    dataHora = forms.DateTimeField(initial=datetime.datetime.now())
    texto_mensagem = forms.Textarea()

    class Meta:
        model = Mensagem
        fields = ('email', 'texto_mensagem', 'dataHora')
