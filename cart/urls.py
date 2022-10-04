from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('remove_one/<int:product_id>/', cart_remove_one, name='cart_remove_one'),
]