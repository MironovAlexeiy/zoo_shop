from .cart import Cart
from .forms import CartAddProductForm

def cart(request):

    return {
        'cart': Cart(request),
        'cart_form': CartAddProductForm(request.POST),
    }