from django.contrib import admin
from .models import OrderModel, OrderProductsModel


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'created_at', 'updated_at', 'order_sum')
    search_fields = ('user_id__email',)


@admin.register(OrderProductsModel)
class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_id', 'quantity')
    search_fields = ('product_id__title',)
