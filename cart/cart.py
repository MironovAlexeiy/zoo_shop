from decimal import Decimal
from django.conf import settings
from main.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, weight=None, weight_price=None, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if weight:
            self.cart[product_id]['weight'] = str(weight)
            self.cart[product_id]['price'] = str(weight_price)
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove_one(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = self.cart[product_id]['quantity'] - 1
            if self.cart[product_id]['quantity'] == 0:
                self.remove(product)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить изменения в сессии, чтобы убедиться что она сохранена
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            if item.get('weight'):
                item['weight'] = Decimal(item['weight'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = 0
        for item in self.cart.values():
            if item['product'].discount:
                item['price'] = item['product'].get_discount_price()
            total += item['price'] * item['quantity']
        return total
        # return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_discount(self):
        total_price = self.get_total_price()
        if total_price >= 50:
            discount_price = total_price - total_price * Decimal(0.25)
            return round(discount_price, 2)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
