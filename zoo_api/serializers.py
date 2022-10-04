import io

from rest_framework import serializers
from decimal import Decimal

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from cart.cart import Cart
from main.models import Product, Pet, Brand, ImageProduct
from .utils import CartForSerializer

class ProductTypeSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('name', )

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('title', )

class ProductSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)
    product_type = ProductTypeSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = Product
        fields = "__all__"


# class CartSerializer(serializers.Serializer):










# class ProductModel:
#     def __init__(self, title, price):
#         self.title = title
#         self.price = Decimal(price)
#
# class ProductModelSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#
#
#
# def encode():
#     model = ProductModel('Корм для собак', 100)
#     model_sr = ProductModelSerializer(model)
#     # print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     # print(json)
#     return json
#
# def decode():
#     stream = io.BytesIO(encode())
#     data = JSONParser().parse(stream)
#     serial = ProductModelSerializer(data=data)
#     serial.is_valid()
#     print(serial.validated_data)
