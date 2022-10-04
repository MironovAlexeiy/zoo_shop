from cart.cart import Cart


class CartForSerializer:
    def __init__(self, request):
        self.cart = Cart(request)

