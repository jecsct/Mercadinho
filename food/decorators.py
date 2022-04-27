from django.http import HttpResponse
from django.shortcuts import redirect


# decoradores recebem como parametro outra funcao, permitem adicionar funcionalidades antes de chamar a funcao a serio
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('food:index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
