from rest_framework import serializers
from .models import CartModel, CartItemModel
from drf_writable_nested import WritableNestedModelSerializer


class CartItemSerializer(serializers.ModelSerializer):
    singe_item_price = serializers.SerializerMethodField('get_item_price')

    def get_item_price(self, obj):
        return obj.product.price

    class Meta:
        model = CartItemModel
        exclude = ('cart',)


class CartSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    items = CartItemSerializer(many=True, required=True)
    total_sum = serializers.SerializerMethodField('get_field_name')

    def get_field_name(self, obj):
        return sum([i.quantity*i.product.price for i in obj.items.all()])

    class Meta:
        model = CartModel
        # exclude = ('user',)
        fields = ('id', 'status', 'created_at', 'total_sum', 'items')
