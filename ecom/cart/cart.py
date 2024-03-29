from store.models import *

# Classe usada pra Guardar Session key do nosso usuário pra todas as Páginas


class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get("session_key")

        # Se o usuário for novo criará uma nova session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #
        self.cart = cart

    def add(self, product, quantity):

        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Pega ids do carrinho
        produtc_ids = self.cart.keys()
        # Usa ids pra procurar no model
        produtcs = Product.objects.filter(id__in=produtc_ids)

        return produtcs

    def get_quantis(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        # relembrando o carrinho na sessao é {"id": quantidade} str e int
        product_id = str(product)
        product_quantity = int(quantity)

        ourcart = self.cart

        # Atualiza o Dicionario do Carrinho
        ourcart[product_id] = product_quantity
        self.session.modified = True
        cart_updated = self.cart
        return cart_updated

    def delete(self, product):

        product_id = str(product)
        # Remover do dicionario
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def total(self):
        total = 0
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.sale_price != 0:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total
