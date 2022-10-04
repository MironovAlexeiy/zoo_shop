from django.urls import path
from .views import OrderCreate, OrderCreateOne, order_success, CallBackCreate, ReviewUsCreate

app_name = 'order'

urlpatterns = [
    path('', OrderCreate.as_view(), name='order_create'),
    path('order_one/<int:product_id>/', OrderCreateOne.as_view(), name='order_one'),
    path('order_success/', order_success, name='order_success'),
    path('callback/', CallBackCreate.as_view(), name='call_back'),
    path('review/', ReviewUsCreate.as_view(), name='reviewus'),
]