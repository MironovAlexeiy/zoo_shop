from django.db import models
from django.urls import reverse
from django.contrib import admin
from decimal import Decimal

class Product(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название товара')
    description = models.TextField(verbose_name='описание')
    pet = models.ForeignKey('Pet', on_delete=models.SET_NULL, null=True, related_name='pet', verbose_name='Питомец')
    slug = models.SlugField(max_length=250, unique=True)
    key_features = models.TextField(verbose_name='ключевые особенности', blank=True)
    compound = models.TextField(verbose_name='состав')
    guaranteed_analysis = models.TextField(verbose_name='гарантированный анализ', blank=True)
    nutritional_supplements = models.TextField(verbose_name='пищевые добавки', blank=True)
    product_type = models.ForeignKey('ProductType', on_delete=models.SET_NULL, null=True, related_name='type', verbose_name='Тип товара')
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, related_name='brand', verbose_name='Бренд')
    available = models.BooleanField(verbose_name='доступность')
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, verbose_name='Цена за 1кг или за нек. единицу')
    discount = models.BooleanField(default=False, blank=True, verbose_name='Товар на акции')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    # views = models.ManyToManyField('UserIp', blank=True, related_name='product_views', verbose_name='Просмотры')
    amount_of_discount = models.IntegerField(verbose_name='Размер скидки в %', default=0, blank=True)
    available_weight = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='доступный вес в кг', blank=True)

    def get_discount_price(self):
        if self.amount_of_discount:
            discount_price = self.price * Decimal((self.amount_of_discount / 100))
            price = self.price - discount_price
            return round(price, 2)


    # @admin.display
    # def total_views(self):
    #     return self.views.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:product_detail', kwargs={'product_slug': self.slug})

    class Meta:
        ordering = ('title', '-created',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductWeight(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_weight')
    weight = models.DecimalField(max_digits=6, decimal_places=3, blank=True, verbose_name='Вес в кг')

    def __str__(self):
        return self.product.title

    @admin.display
    def price_for_weight(self):
        price = self.product.price * self.weight
        return round(price, 2)



class ImageProduct(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='product_img')


class Brand(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название бренда')
    image = models.ImageField(upload_to='brands')
    slug = models.SlugField(max_length=250, unique=True)
    sale = models.BooleanField(default=False, blank=True,verbose_name='Распродажа у бренда')
    product_type = models.ManyToManyField('ProductType', related_name='prod_type')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'



class ProductType(models.Model):
    title = models.CharField(max_length=250, verbose_name='Тип товара')
    slug = models.SlugField(max_length=250, unique=True)
    sale = models.BooleanField(default=False, blank=True, verbose_name='Скидка у категории')


    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'

class Pet(models.Model):
    name = models.CharField(max_length=100, verbose_name='Вид питомца')
    img = models.ImageField(upload_to='pets/%Y/%m/%d', blank=True)
    slug = models.SlugField(max_length=250, null=True, unique=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'


class Articles(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название статьи')
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    pet = models.ForeignKey(Pet, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='articles/%Y/%m/%d', blank=True)
    time_read = models.PositiveIntegerField(verbose_name='Время чтения, мин.')
    is_published = models.BooleanField(verbose_name='Опубликовано', default=False)
    created = models.DateField(auto_now_add=True, verbose_name="Дата опубликования")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-created', 'title',)

    def get_absolute_url(self):
        return reverse('main:article_detail', kwargs={'art_slug': self.slug})


# class UserIp(models.Model):
#     ip = models.CharField(max_length=150)


