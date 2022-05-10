import random
from time import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required
from food.models import Mensagem, Customer, Salesman
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from .forms import CustomerForm, UserForm, ContactForm, SalesmanForm
from .models import Product, Comment, CestoCompras
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import User, Group


def index(request):
    products = Product.objects.all()
    if request.user.groups.filter(name='Salesman').exists():
        products = products.filter(salesman_id=request.user.salesman.id)
    context = {'products_list': products}
    return render(request, 'food/index.html', context)


def contactos(request):
    error_message = False
    if request.method == 'POST':
        if not request.POST.get("email") == request.user.email:
            Mensagem(email=request.POST.get("email"),
                     texto_mensagem=request.POST.get("message"),
                     dataHora=datetime.datetime.now()).save()
            return HttpResponseRedirect(reverse('food:contactos'))
        else:
            error_message = 'Não pode enviar emails para si próprio';
    return render(request, 'food/contactos.html', {'error_message': error_message})


@login_required
def caixaMensagens(request):
    lista_mensagens = Mensagem.objects.order_by('-dataHora').filter(email=request.user.email)
    return render(request, 'food/caixaMensagens.html', {'lista_mensagens': lista_mensagens})


@login_required
@allowed_users(allowed_roles=['Customer'])
def cestoCompras(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user=user)
    try:
        cesto_compras = CestoCompras.objects.filter(customer=customer)
    except CestoCompras.DoesNotExist:
        cesto_compras = None
    return render(request, 'food/cestoCompras.html', {'cesto_compras': cesto_compras})


@login_required(login_url="food:loginutilizador")
@allowed_users(allowed_roles=['Customer'])
def addToCart(request, product_id):
    try:
        for x in range(int(request.POST.get('quant'))):
            user = request.user
            customer = Customer.objects.get(user=user)
            product = Product.objects.get(id=product_id)
            shoppingCart = CestoCompras(customer=customer, product=product)
            shoppingCart.save()
        comments = Comment.objects.all().filter(product_id=product_id)
        product.addView()
        context = {'product': product, 'comments': comments, 'confirmation' : 'Produto adicionado'}
        return render(request, 'food/detalhe.html', context)
    except:
        user = request.user
        customer = Customer.objects.get(user=user)
        product = Product.objects.get(id=product_id)
        shoppingCart = CestoCompras(customer=customer, product=product)
        shoppingCart.save()
        products_list = Product.objects.all()
        context = {'products_list': products_list,'confirmation':'Produto adicionado', 'p' : product}
        return render(request, 'food/index.html', context)


@login_required
@allowed_users(allowed_roles=['Customer'])
def removeFromCart(request, cestoCompras_id):
    get_object_or_404(CestoCompras, pk=cestoCompras_id).delete()
    return HttpResponseRedirect(reverse('food:cestocompras'))


@login_required
def perfil(request):
    comments = Comment.objects.all().filter(user=request.user)
    return render(request, "food/perfil.html", {'comments': comments})


@unauthenticated_user
def registarCustomer(request):
    if request.method == "POST":
        if request.FILES['photo']:
            image = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password"],
                email=request.POST["email"]
            )
            Group.objects.get(name='Customer').user_set.add(user)
            Customer(
                profile_pic=uploaded_file_url,
                gender=request.POST["gender"],
                birthday=request.POST["birthday"],
                credit=request.POST["credits"],
                user_id=user.id
            ).save()
            login(request, user)
            return HttpResponseRedirect(reverse('food:index'))
    return render(request, 'food/registarCustomer.html')


@unauthenticated_user
def registarSalesman(request):
    if request.method == "POST" and request.FILES['photo']:
        image = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        user = User.objects.create_user(
            username=request.POST["username"],
            password=request.POST["password"],
            email=request.POST["email"]
        )
        Group.objects.get(name='Salesman').user_set.add(user)
        Salesman(
            profile_pic=uploaded_file_url,
            rating=0,
            phone_number=request.POST["telephone"],
            user_id=user.id
        ).save()
        login(request, user)
        return HttpResponseRedirect(reverse('food:index'))
    return render(request, 'food/registarSalesman.html')


@login_required
@allowed_users(allowed_roles=['Salesman'])
def addProduct(request):
    if request.method == 'POST' and request.FILES['myfile']:
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


@unauthenticated_user
def loginutilizador(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
        except KeyError:
            return render(request, 'food/loginutilizador.html')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('food:index'))
            else:
                return render('food/loginutilizador.html',
                              {'error_message': 'Utilizador não existe ou a password está incorreta'})
        else:
            return render(request, 'food/loginutilizador.html')
    else:
        return render(request, 'food/loginutilizador.html')


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
    products = Product.objects.all().exclude(id=product_id)
    context = {'product': product, 'comments': comments, "products": products}
    return render(request, 'food/detalhe.html', context)


@login_required
@allowed_users(allowed_roles=['Customer'])
def commentOnItem(request, product_id):
    if request.method == 'POST':
        commentText = request.POST['commentInput']
        commentRating = request.POST['ratingInput']
        product = Product.objects.get(id=product_id)
        Salesman.objects.get(id=product.salesman_id).addRating(newRating=commentRating)
        product.addRating(newRating=commentRating)
        Comment(user=request.user, text=commentText, dataHour=datetime.datetime.now(), rating=commentRating,
                product=product).save()
    return HttpResponseRedirect(reverse('food:productDetailPage', args=(product_id,)))


@login_required
@allowed_users(allowed_roles=['Customer'])
def deleteProductComment(request, product_id):
    product = Product.objects.get(id=product_id)
    comment = Comment.objects.get(product_id=product_id, user_id=request.user.id)
    if request.method == 'POST':
        Salesman.objects.get(id=product.salesman_id).deleteRating(comment.rating)
        product.deleteRating(comment.rating)
        comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # volta para a página anterior. necessário por causa do perfil


@login_required
@allowed_users(allowed_roles=['Customer'])
def updateProductComment(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comment = Comment.objects.get(product_id=product_id, user_id=request.user.id)
    if request.method == 'POST':
        newText = request.POST['newCommentText']
        newRating = request.POST['newCommentRating']
        product.updateRating(comment.rating, newRating)
        Salesman.objects.get(id=product.salesman_id).updateRating(newRating=newRating, oldRating=newRating)
        Comment.objects.filter(user_id=request.user.id, product_id=product_id).update(text=newText, rating=newRating)
        return HttpResponseRedirect(reverse('food:productDetailPage', args=(product_id,)))
    context = {'product': product, 'comment': comment}
    return render(request, 'food/updateProductComment.html', context)


@login_required
@allowed_users(allowed_roles=['Salesman'])
def deleteProduct(request, product_id):
    get_object_or_404(Product, pk=product_id).delete()
    return HttpResponseRedirect(reverse('food:index'))


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

def get_price(customer):
    shopping_cart = CestoCompras.objects.filter(customer=customer)
    price = 0
    for item in shopping_cart:
        price += item.product.price
    return price

@login_required
def pagamento(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user=user)
    price = get_price(customer)
    if price == 0:
        return render(request, 'food/cestoCompras.html', {'error_message': "O seu carrinho está vazio"})
    return render(request, 'food/pagamento.html', {'price': price})

def checkOut(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user=user)
    shopping_cart = CestoCompras.objects.filter(customer=customer)
    for item in shopping_cart:
        item.product.sales += 1
        item.product.save()
    price = get_price(customer)
    if customer.credit - price < 0:
        return render(request, 'food/pagamento.html', {'price': price,
                                                       'error_message': "Não tem laterninhas suficientes para esta compra. Vá investir na crypto"})
    else:
        if request.method == 'POST':
            morada = request.POST['morada']
            zipCode = request.POST['ZipCode']
            if morada and zipCode:
                customer.credit = customer.credit - price
                customer.save()
                CestoCompras.objects.filter(customer=customer).delete()
                products = Product.objects.all()
                enviado = "A sua encomenda está confirmada! Será enviada para a " + str(morada) + " com o codigo postal " + str(zipCode)
                context = {'products_list': products, 'enviado':enviado }
                return render(request, 'food/index.html', context)
            else:
                return render(request, 'food/pagamento.html', {'price': price,
                                                               'error_message': "Preencha a Morada e o Código Postal"})
    return render(request, 'food/pagamento.html',{'price':price})

@login_required(login_url="food:loginutilizador")
@allowed_users(allowed_roles=['Customer'])
def investCrypto(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user=user)
    customer.credit = random.randint(1,1000000)
    customer.save()
    return HttpResponseRedirect(reverse('food:about'))