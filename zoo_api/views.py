from collections import OrderedDict

from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from cart.cart import Cart
from main.models import Product, ProductType, Brand
from .serializers import ProductSerializer, ProductTypeSerializer
from rest_framework import permissions



class Mypagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 25

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page_number', self.page.number),
            ('results', data),
        ]))


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(available=True).prefetch_related('product_weight', 'product_img').select_related('brand', 'pet', 'product_type')
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = Mypagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('title', 'pet', 'brand', 'product_type', )
    search_fields = ('title', 'brand__title', 'product_type__title', 'pet__name')
    @action(methods=['get'], detail=False)
    def brands(self, request):
        brands = Brand.objects.all()
        return Response({'brands': [brand.title for brand in brands]})

    @action(methods=['get'], detail=False)
    def prod_type(self, request):
        prod_type = ProductType.objects.all()
        return Response({'prod_type': [p_type.title for p_type in prod_type]})

    @action(methods=['post'], detail=True)
    def cart_add(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart = Cart(request)
        cart.add(product)
        return Response({'Add_product': ProductSerializer(product).data.get('title')})


class CartApi(APIView):
    def get(self, request):
        cart = Cart(request)
        for i in cart:
            product = i['product']
            i['product_serial'] = ProductSerializer(product).data
        total_price = cart.get_total_price()
        discount_price = cart.get_discount()
        for i in cart:
            del i['product']
        return Response({'cart': cart.cart, 'total_price': total_price, 'discount_price': discount_price})



# class ProductAPIView(generics.ListCreateAPIView):
#     queryset = Product.objects.all().prefetch_related('product_weight', 'product_img')
#     serializer_class = ProductSerializer
#
# class ProductDetailAPIView(generics.RetrieveAPIView):
#     queryset = Product.objects.all().prefetch_related('product_img', 'product_weight')
#     serializer_class = ProductSerializer
#
# class ProductTypeAPIView(APIView):
#     def get(self, request):
#         pt = ProductType.objects.all()
#         pt_serializ = ProductTypeSerializer(pt, many=True)
#         return Response(pt_serializ.data)
#
#     def post(self, request):
#         data = ProductTypeSerializer(data=request.data)
#         data.is_valid(raise_exception=True)
#
#         pt_new = ProductType.objects.create(
#             title=request.data['title'],
#             slug=request.data['slug'],
#         )
#         pt_new_serial = ProductTypeSerializer(pt_new)
#         return Response(pt_new_serial.data)