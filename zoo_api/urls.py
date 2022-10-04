from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartApi.as_view()),


    # path('product/<int:pk>/cart', CartApi.as_view()),
    # path('productslist/', ProductAPIView.as_view()),
    # path('productdetail/<int:pk>/', ProductDetailAPIView.as_view()),
    # path('ptlist/', ProductTypeAPIView.as_view()),
]