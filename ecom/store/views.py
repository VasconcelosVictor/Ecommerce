from django.shortcuts import redirect, render
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .decorator import *
from .forms import *


def login_user(request):
    context_dict = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        # Se Usuário existe Loga
        if user is not None:
            login(request, user)
            messages.success(request, ("Você está autenticado !"))
            return redirect("home")
        else:
            messages.error(request, "Digite Seu usuario e senha corretamente!")
            return redirect('login')

    else:
        return render(request, "login.html", context_dict)


def logout_user(request):
    logout(request)
    messages.success(
        request, ("Você deslogado... Obrigado por ultilizar nosso serviço."))
    return redirect('login')


def register_user(request):
    context_dict = {}

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            # login
            user = authenticate(username=username, password=password1)
            login(request, user)

            messages.success(
                request, ("Registro Criado com Sucesso!! Seja bem vindo !!"))
            return redirect('home')
        else:
            messages.error(
                request, ("Opa parece que você não preencheu as informações corretamente !!"))
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('register')

    else:
        form = SignUpForm()

    context_dict['form'] = form

    return render(request, "register.html", context_dict)


def update_user(request):
    context_dict = {}
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        context_dict['user_form'] = user_form
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "Usuário Atualizando com Sucesso.")
            return redirect("home")

        return render(request, "update_user.html", context_dict)
    else:
        messages.error(
            request, "Você precisa está logado pra acessar essa página")
        return redirect("home")


def update_password(request):
    context_dict = {}
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Senha Atualizada com Sucessso!")
                login(request, current_user)
                return redirect("update-user")

            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

                return redirect("update-password")    
        else:
            form = ChangePasswordForm(current_user)

            context_dict['form'] = form

            return render(request, "update_password.html", context_dict)

    else:
        messages.success(
            request, "Você precisa fazer Login antes de entrar nessa sessão!")
        
        return redirect('home')


# **** Autenticação ****

@decorator_base
def home(request, context_dict):
    produts = Product.objects.all()
    context_dict['products'] = produts

    paginator = Paginator(produts, 50)
    page_num = request.POST.get('page', 1)
    objs = paginator.page(page_num)

    context_dict['page_obj'] = objs

    return render(request, "home.html", context_dict)


@decorator_base
def about(request, context_dict):

    return render(request, "about.html", context_dict)


@decorator_base
def product(request, context_dict, pk):
    product = Product.objects.get(id=pk)
    context_dict['product'] = product

    return render(request, "product.html", context_dict)


@decorator_base
def category(request, context_dict, pk):

    category = Category.objects.get(id=pk)
    if category:
        products = Product.objects.filter(category=category)
        context_dict['products'] = products
    else:
        messages.error(
            request, ("Opa parece que essá categoria não está mais disponível !!"))
        redirect("home")
    context_dict['category'] = category

    return render(request, "category.html", context_dict)


@decorator_base
def category_summary(request, context_dict):
    categories = Category.objects.all()

    context_dict['categories'] = categories

    return render(request, "category_summary.html", context_dict)
