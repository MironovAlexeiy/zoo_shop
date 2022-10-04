from django.contrib import admin
from .models import Order, OrderItem, CallBack, ReviewsUs

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'created', 'get_total_coast' ,'paid', 'update',)
    list_filter = ('paid', 'created', 'update')
    inlines = (OrderItemInline,)
    list_editable = ('paid',)

@admin.register(CallBack)
class CallBackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'call', 'created',)
    exclude = ('paid',)

@admin.register(ReviewsUs)
class ReviewsUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'pet', 'reviews_us', 'is_published',)
    exclude = ('paid', )
