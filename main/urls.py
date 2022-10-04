from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

app_name = 'main'

urlpatterns = [
    # path('', cache_page(60)(Main.as_view()), name='main'),
    path('', Main.as_view(), name='main'),
    path('catalog/<slug:pet_slug>/', ProductList.as_view(), name='product_pet_list'),
    path('catalog/', ProductList.as_view(), name='product_list'),
    path('filter_catalog/', filter_brands_types, name='filter_brands_types'),
    path('sort_catalog/', Sort_catalog.as_view(), name='sort_catalog'),
    path('product/<slug:product_slug>/', ProductDetail.as_view(), name='product_detail'),
    # path('product/', get_total_weight, name='get_product_weight'),
    path('articles/', ArticleView.as_view(), name='articles'),
    path('article/<slug:art_slug>/', ArticleDetail.as_view(), name='article_detail'),
    path('search/', Search.as_view(), name='search'),


    # path('account/register/', RegisterClient.as_view(), name='registration'),
    # path('account/signup/', SignUp.as_view(), name='sign'),
    # path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL} , name='logout'),
]