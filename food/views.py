from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required
from food.models import Mensagem
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import CustomerForm, UserForm, ContactForm
from .models import Product, Comment
from .decorators import unauthenticated_user, allowed_users


def redirect_view(request):
    return redirect('/food')


def index(request):
    products = Product.objects.all()
    context = {'products_list': products}
    return render(request, 'food/index.html', context)


def contactos(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ContactForm(request.POST, initial={'email_envio': request.user.email})
        else:
            form = ContactForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.save()
            return render(request, 'food/contactos.html', {'contactForm': form})
    else:
        if request.user.is_authenticated:
            form = ContactForm(initial={'email_envio': request.user.email})
        else:
            form = ContactForm()
    return render(request, 'food/contactos.html', {'contactForm': form})


def caixaMensagens(request):
    lista_mensagens = Mensagem.objects.order_by('-dataHora')
    return render(request, 'food/caixaMensagens.html', {'lista_mensagens': lista_mensagens})


def cestoCompras(request):
    # cesto_compras =
    # return render(request, 'food/cestoCompras.html', {'cesto_compras':cesto_compras})
    return render(request, 'food/cestoCompras.html')


def adicionarCesto(request):
    return render(request, 'food/cestoCompras.html')


def removerCesto(request):
    return render(request, 'food/cestoCompras.html')


def perfil(request):
    return render(request, "food/perfil.html")


def registarutilizador(request):
    if request.method == "POST":
        customerForm = CustomerForm(request.POST)
        userForm = UserForm(request.POST)
        if customerForm.is_valid() and userForm.is_valid():
            user = userForm.save(commit=False)
            user.save()

            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()

            return render(request, 'food/index.html')
    else:
        customerForm = CustomerForm()
        userForm = UserForm()
        return render(request, 'food/registarutilizador.html', {'userForm': userForm, 'customerForm': customerForm})


@unauthenticated_user
def loginutilizador(request):
    error_message = False
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "food/index.html")
        error_message = 'Utilizador não existe ou a password está incorreta'
    form = AuthenticationForm()
    return render(request, "food/loginutilizador.html", {"loginform": form, 'error_message': error_message})


@login_required
def logoututilizador(request):
    logout(request)
    return HttpResponseRedirect(reverse('food:index'))


def mapPage(request):
    return render(request, 'food/mercadinhos_map.html')


def aboutPage(request):
    return render(request, 'food/about.html')


def productDetailPage(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = Comment.objects.all().filter(product_id=product_id)
    product.addView()
    context = {'product': product, 'comments': comments}
    return render(request, 'food/detalhe.html', context)


@login_required
def commentOnItem(request, product_id):
    if request.method == 'POST':
        commentText = request.POST['commentInput']
        commentRating = request.POST['ratingInput']
        product = Product.objects.get(id=product_id)
        # product.update(rating=calculateItemRating(product_id, commentRating))
        product.addRating(newRating=commentRating)
        Comment(user=request.user, text=commentText, dataHour=datetime.datetime.now(), rating=commentRating,
                product=product).save()
    return HttpResponseRedirect(reverse('food:productDetailPage', args=(product_id,)))
    # return productDetailPage(request, product_id)


@login_required
def updateProductComment(request, product_id):
    print(request.method)
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        newText = request.POST['newCommentText']
        newRating = request.POST['newCommentRating']
        product.updateRating(Comment.objects.get(product_id=product_id, user_id=request.user.id).rating, newRating)
        Comment.objects.filter(user_id=request.user.id, product_id=product_id).update(text=newText, rating=newRating)
        return HttpResponseRedirect(reverse('food:productDetailPage', args=(product_id,)))
    comment = Comment.objects.get(user_id=request.user.id, product_id=product_id)
    context = {'product': product, 'comment': comment}
    return render(request, 'food/updateProductComment.html', context)


@login_required
def deleteProductComment(request, product_id):
    if request.method == 'POST':
        Product.objects.get(id=product_id).deleteRating(
            Comment.objects.get(product_id=product_id, user_id=request.user.id).rating)
        Comment.objects.get(product=product_id, user_id=request.user).delete()
    return HttpResponseRedirect(reverse('food:productDetailPage', args=(product_id,)))


@login_required
@allowed_users(allowed_roles=['Salesman'])
def addProduct(request):
    if request.method == 'POST':
        if request.FILES['myfile']:
            productImage = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(productImage.name, productImage)
            uploaded_file_url = fs.url(filename)
            Product.objects.create(name=request.POST.get('productName'),
                                   description=request.POST.get('productDescription'),
                                   price=request.POST.get('productPrice'),
                                   image=uploaded_file_url,
                                   salesman_id=request.user.salesman.id
                                   )
            return HttpResponseRedirect(reverse('food:index'))
    return render(request, 'food/add_product.html')
