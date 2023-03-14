from django.contrib import admin
from .models import CartItemModel, CartModel


class CartItemInline(admin.StackedInline):
    extra = 0
    model = CartItemModel


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('user', 'created_at')
    search_fields = ('user',)
    readonly_fields = ('created_at',)
