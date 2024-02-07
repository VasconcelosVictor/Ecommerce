from .cart import Cart

# Cria processador de contexto pro carrinho tabalhar em todas as paginas 
def cart(request):
    
    return {'cart': Cart(request)}

