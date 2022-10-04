from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, ListView

from cart.cart import Cart
from cart.forms import CartAddProductForm
from .models import *
from .utils import get_pet_name
from .forms import *
import redis
from django.conf import settings

#подключение к Redis
r = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)

# def get_user_ip(request):
#     # ip_real_user = request.META.get('HTTP_X_FORWARDED_FOR') ---------получаем ip-only пользователя
#     # if ip_real_user:
#     #     ip = ip_real_user.split(',')[0]
#     ip = request.META.get('REMOTE_ADDR')  # получаем ip нашего сервера
#     return ip


class Main(View):
    def get(self, request):
        return render(request, 'main.html',)



class ProductList(View):

    def get(self,request, pet_slug=None, *args, **kwargs):
        products = Product.objects.select_related('pet', 'product_type', 'brand').prefetch_related('product_img', 'product_weight').filter(available=True)
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context = {
            'page_object': page_object,
        }
        if request.GET.get('some_price'):
            som_price = request.GET.get('some_price')
            som_weight = request.GET.get('some_weight')
            context['some_weight'] = som_weight
            context['some_price'] = som_price
        if pet_slug:
            products_pet = products.prefetch_related('product_weight', 'product_img').filter(pet__slug=pet_slug)
            pet_name = get_pet_name(str(Pet.objects.get(slug=pet_slug)))
            paginator_pet = Paginator(products_pet, 12)
            page_number = request.GET.get('page')
            page_object = paginator_pet.get_page(page_number)
            article_pet = Articles.objects.filter(pet__slug=pet_slug).select_related('pet')
            context.update({
                'pet_name': pet_name,
                'page_object': page_object,
                'articles': article_pet,
                'products_popular': products_pet,

            })

        return render(request, 'catalog.html', context)

def filter_brands_types(request):
    brands_filter = request.GET.getlist('brands_form')
    product_type_filter = request.GET.get('product_types_form')
    products = ''
    if brands_filter or product_type_filter:
        products = Product.objects.filter(
            Q(product_type__title__exact=product_type_filter) |
            Q(brand__title__in=brands_filter)
        ).filter(available=True).prefetch_related('product_img', 'product_weight')
    if brands_filter and product_type_filter:
        products = Product.objects.filter(
            Q(brand__title__in=brands_filter) &
            Q(product_type__title__exact=product_type_filter)
        ).filter(available=True).prefetch_related('product_img', 'product_weight')
    context = {
        'page_object': products
    }
    return render(request, 'catalog.html', context)

class Sort_catalog(View):

    def get(self,request, pet_slug=None, *args, **kwargs):
        key = request.GET.get('select_sort')
        if key == 'popular':
            product_rank = r.zrange('product_rank', 0, -1, desc=True)[:10]
            product_rank_id = [int(id) for id in product_rank]
            most_popular = list(Product.objects.filter(id__in=product_rank_id))
            most_popular.sort(key=lambda x: product_rank_id.index(x.id))
            products = most_popular
        else:
            products = Product.objects.prefetch_related('product_img').filter(available=True).order_by(key)
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context = {
            'page_object': page_object,
        }

        return render(request, 'catalog.html', context)

class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self,*args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        product = super(ProductDetail, self).get_object()
        total_views = r.incr(f'product:{product.id}:id')
        r.zincrby('product_rank', 1, product.id)
        context['total_views'] = total_views
        return context

    # def get_object(self, queryset=None):
    #     product = super(ProductDetail, self).get_object()
    #     user_ip = get_user_ip(self.request)
    #     print(user_ip)
    #     if UserIp.objects.get_or_create(ip=user_ip):
    #         product.views.add(UserIp.objects.get(ip=user_ip))
    #     return product

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        som_price = request.GET.get('some_price')
        som_weight = request.GET.get('some_weight')
        context = {
            'some_weight': som_weight,
            'some_price': som_price,
        }
        if request.GET.get('weight_input'):
            weight_input = Decimal(request.GET.get('weight_input'))
            if weight_input > self.object.available_weight:
                error = f'К сожалению, в наличие нет указанного количества товара.' \
                        f'Максимальный размер заказа может составить: {self.object.available_weight} кг.'
                context.update({
                    'error': error,
                })
            else:
                price_weight_input = round(self.object.price * weight_input, 2)
                context.update({
                    'price_input': price_weight_input,
                    'weight_input': weight_input,
                })
        context.update(self.get_context_data(object=self.object))
        return self.render_to_response(context)


class ArticleView(ListView):
    model = Articles
    template_name = 'articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Articles.objects.filter(is_published=True).select_related('pet')

class ArticleDetail(DetailView):
    model = Articles
    context_object_name = 'article'
    slug_url_kwarg = 'art_slug'
    template_name = 'article_detail.html'


class Search(View):

    def get(self, request, *args, **kwargs):
        result = ''
        query = self.request.GET.get('q')
        if query:
            result = Product.objects.filter(
                Q(title__icontains=query) |
                Q(brand__title__icontains=query) |
                Q(product_type__title__icontains=query)
            )
        paginator = Paginator(result, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'result': page_obj,
            'count': paginator.count
        }
        return render(request, 'blocks/search.html', context)














# class RegisterClient(View):
#     def get(self, request):
#         form = FormRegistration()
#         return render(request, 'register.html', {'form': form})
#
#     def post(self, request):
#         form = FormRegistration(request.POST)
#         if form.is_valid():
#             client = form.save()
#             if client is not None:
#                 login(request, client)
#                 return HttpResponseRedirect('/')
#         return render(request, 'register.html', {'form': form})
#
# class SignUp(View):
#     def get(self, request, *args, **kwargs):
#         form = Sign()
#         return render(request, 'account/login.html', {'form': form})
#
#     def post(self,request, *args, **kwargs):
#         form=Sign(request.POST)
#         if form.is_valid():
#             email = request.POST['email']
#             password = request.POST['password']
#             client = authenticate(request, email=email, password=password)
#             if client is not None:
#                 login(request, client)
#                 return HttpResponseRedirect('/')
#         return render(request, 'account/login.html', {'form': form})

