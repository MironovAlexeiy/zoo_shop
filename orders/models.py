from django.db import models
from main.models import Product
from django.contrib import admin

class Order(models.Model):
    name = models.CharField(max_length=150, verbose_name='ФИО')
    phone_number = models.CharField(max_length=13, verbose_name='Номер телефона')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ № {self.id}'

    @admin.display
    def get_total_coast(self):
        return f'{sum(item.get_cost() for item in self.items.all())} BYN'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='items_order', verbose_name='Товары')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return str(self.id)

    @admin.display
    def get_cost(self):
        return self.price * self.quantity



class CallBack(Order):
    call = models.BooleanField(verbose_name='Перезвонили', default=False)

class ReviewsUs(Order):
    pet = models.CharField(max_length=50, verbose_name='Имя питомца')
    reviews_us = models.TextField(verbose_name='Отзыв')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
