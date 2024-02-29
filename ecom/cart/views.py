from django.shortcuts import render, get_object_or_404

from store.decorator import decorator_base
from .cart import Cart
from store.models import *
from django.http import JsonResponse


@decorator_base
def cart_summary(request, context_dict):
    #
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quantis()
    context_dict['cart_products'] = cart_products
    context_dict['cart_quantities'] = quantities

    return render(request, "cart_summary.html", context_dict)


def cart_add(request):
    cart = Cart(request)
    # se POST
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, id=product_id)

        # Salve no dicionario cart a sessao de produtos selecionados
        cart.add(product=product, quantity=product_qty)

        # Quantidade de itens no carrinho
        cart_quantity = cart.__len__()

        reponse = JsonResponse({'quantity': cart_quantity})
        return reponse


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        reponse = JsonResponse({'quantity': product_qty})

        return reponse


def cart_delete(request):

    return render(request, "", context={})
