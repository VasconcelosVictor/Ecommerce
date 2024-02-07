from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import *
from django.http import JsonResponse


def cart_summary(request):

    return render(request, "cart_summary.html", context={})


def cart_add(request):
    cart = Cart(request)
    # se POST
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        product = get_object_or_404(Product, id=product_id)

        # Salve no dicionario cart a sessao de produtos selecionados
        cart.add(product=product)
        reponse = JsonResponse({'product name': product.name})
        return reponse


def cart_update(request):

    return render(request, "", context={})


def cart_delete(request):

    return render(request, "", context={})
