from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartRemoveProduct
from decimal import Decimal

@require_POST    #разрешает только POST-запросы
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    some_weight = ''
    some_price = ''
    if request.POST.get('weight') and request.POST.get('weight') != None:
        some_weight = request.POST.get('weight').replace(',', '.')
        some_price = product.product_weight.get(weight=some_weight).price_for_weight()
    if request.POST.get('weight_input') and request.POST.get('price_input'):
        some_weight = request.POST.get('weight_input').replace(',', '.')
        some_price = str(request.POST.get('price_input')).replace(',', '.')
    if form.is_valid():
        cd = form.cleaned_data
        if some_weight and some_price:
            cart.add(product=product,
                 quantity=cd['quantity'],
                 weight=some_weight,
                 weight_price=some_price,
                 update_quantity=cd['update'])
        else:
            cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])

    return redirect(request.META.get('HTTP_REFERER'))

@require_POST
def cart_remove_one(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartRemoveProduct(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.remove_one(product=product, quantity=cd['quantity'])
    return redirect(request.META.get('HTTP_REFERER'))

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})


