from django.core.cache import cache
from django.db.models import Count

from .models import Product, Brand, ProductType, Pet, Articles
from .views import r

def common_variables(request):
    # получаем набор рейтинга товаров
    most_popular = cache.get('most_popular')
    if not most_popular:
        product_rank = r.zrange('product_rank', 0, -1, desc=True)[:4]
        product_rank_id = [int(id) for id in product_rank]
        most_popular = list(Product.objects.filter(id__in=product_rank_id))
        most_popular.sort(key=lambda x: product_rank_id.index(x.id))
        cache.set('most_popular', most_popular, 60)
    # products_popular = Product.objects.filter(available=True).annotate(view=Count('views')).order_by('view')[:4]
    pets = Pet.objects.all()
    articles = Articles.objects.all()[:3].select_related('pet')
    products_new = Product.objects.prefetch_related('product_img').filter(available=True).order_by('-created')[:4]
    brands = Brand.objects.all()
    product_types = ProductType.objects.all()
    variables = {
        'products_popular':most_popular,
        'pet_list': pets,
        'articles': articles,
        'products_new': products_new,
        'brands': brands,
        'product_types': product_types,
    }
    return variables