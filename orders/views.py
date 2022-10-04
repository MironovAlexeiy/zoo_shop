from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView

from main.models import Product
from .models import OrderItem
from .forms import OrderCreateForm, CallBackForm, ReviewsUsForm
from cart.cart import Cart

class OrderCreate(View):

    def get(self, request):
        form = OrderCreateForm()
        cart = Cart(request)
        return render(request, 'order_create.html', {'form_order': form, 'cart_checkout': cart,})

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    )
            cart.clear()
            return redirect('order:order_success')
        else:
            return render(request, 'order_create.html', {'form_order': form})


class OrderCreateOne(View):

    def get(self, request, product_id):
        form = OrderCreateForm()
        product = Product.objects.get(id=product_id)
        return render(request, 'order_one_click.html', {'form_order': form, 'product_one': product,})


    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        print(product)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            OrderItem.objects.create(
                    order = order,
                    product=product,
                    price=product.price,
                    quantity=request.POST.get('quantity_one'),
                    )
            return redirect('order:order_success')
        else:
            return render(request, 'order_one_click.html', {'form_order': form})

def order_success(request):
    return render(request, 'order_created.html')

class CallBackCreate(CreateView):
    form_class = CallBackForm
    success_url = reverse_lazy('main:main')
    template_name = 'call_back.html'

class ReviewUsCreate(CreateView):
    form_class = ReviewsUsForm
    success_url = reverse_lazy('main:main')
    template_name = 'review_us.html'