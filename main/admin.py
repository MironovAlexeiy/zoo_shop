from django.contrib import admin
from .models import *

class ProductWeightAdmin(admin.TabularInline):
    model = ProductWeight
    fields = ('weight', 'product',)

class ProductImageInline(admin.StackedInline):
    model = ImageProduct
    max_num = 5
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        'title',
        'product_type',
        'brand',
        'available',
        'price',
        'discount',
        'amount_of_discount',
        'update',
        # 'total_views',
    )
    list_editable = ('price', 'available', 'discount', 'amount_of_discount',)

    search_fields = ('title', 'brand__title', 'product_type__title',)
    inlines = (ProductWeightAdmin, ProductImageInline)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
