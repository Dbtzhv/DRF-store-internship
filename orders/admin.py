from django.contrib import admin
from .models import OrderModel, OrderProductsModel


class OrderProductInline(admin.StackedInline):
    extra = 0
    model = OrderProductsModel


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    # list_display = ('id', 'user_id', 'created_at', 'updated_at', 'order_sum')
    # search_fields = ('user_id__email',)
