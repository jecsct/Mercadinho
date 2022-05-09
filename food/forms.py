from django.forms import ModelForm
import datetime

from food.models import Mensagem
from django import forms


class ContactForm(ModelForm):
    dataHora = forms.DateTimeField(initial=datetime.datetime.now())
    texto_mensagem = forms.Textarea()

    class Meta:
        model = Mensagem
        fields = ('email', 'texto_mensagem', 'dataHora')
