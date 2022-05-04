from django.forms import ModelForm, EmailInput, DateInput, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime

from food.models import Customer, Mensagem
from django import forms


class UserForm(UserCreationForm):
    password1 = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')
        widgets = {
            "email": EmailInput(attrs={'type': 'email'}),
            "password1": PasswordInput(attrs={'type': 'password'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        del self.fields['password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('gender', 'profile_pic', 'birthday')
        widgets = {
            "birthday": DateInput(attrs={'type': 'date'}),
        }


class ContactForm(ModelForm):
    dataHora = forms.DateTimeField(initial=datetime.datetime.now())

    class Meta:
        model = Mensagem
        fields = ('email_envio', 'email_resposta', 'texto_mensagem', 'dataHora')
        widgets = {
            "texto_mensagem": forms.Textarea
        }
