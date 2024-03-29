from rest_framework import serializers
from .models import CartModel, CartItemModel
from drf_writable_nested import WritableNestedModelSerializer


class CartItemSerializer(serializers.ModelSerializer):
    single_item_price = serializers.SerializerMethodField('get_item_price')

    def get_item_price(self, obj):
        return obj.product.price

    def validate(self, data):
        """
        Check that quantity is not greater than general_quantity
        """
        if data['quantity'] > data['product'].general_quantity:
            data['status'] = 'not available'
        return data

    class Meta:
        model = CartItemModel
        exclude = ('cart',)


class CartSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    items = CartItemSerializer(many=True, required=True)
    total_sum = serializers.SerializerMethodField('get_field_name')

    def validate(self, data):
        """
        Check that quantity is not greater than general_quantity
        """
        if 'not available' in [i['status'] for i in data['items']]:
            data['status'] = 'not available'
        return data

    def get_field_name(self, obj):
        return sum([i.quantity*i.product.price for i in obj.items.all()])

    class Meta:
        model = CartModel
        # exclude = ('user',)
        fields = ('id', 'status', 'created_at', 'total_sum', 'items')
