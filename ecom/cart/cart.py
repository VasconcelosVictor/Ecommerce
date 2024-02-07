# Classe usada pra Guardar Session key do nosso usuário pra todas as Páginas.

class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get("session_key")

        # Se o usuário for novo criará uma nova session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #
        self.cart = cart

    def add(self, product):

        product_id = str(product.id)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True
