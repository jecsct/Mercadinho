from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from .models import Comment


# decoradores recebem como parametro outra funcao, permitem adicionar funcionalidades antes de chamar a funcao a serio
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('food:index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator


def canComment(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not Comment.objects.all().filter(user_id=request.user):
            return view_func(request, *args, **kwargs)
        else:
            # return redirect('food:index')
            return HttpResponseRedirect(reverse())
    return wrapper_func