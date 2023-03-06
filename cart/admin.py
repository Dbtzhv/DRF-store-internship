from django.contrib import admin
from .models import CartItemModel, CartModel


@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'cart')
    search_fields = ('cart',)


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user',)
    readonly_fields = ('created_at',)
