from rest_framework import serializers

from cart.models import CartModel
from .models import OrderModel, OrderProductsModel
from drf_writable_nested import WritableNestedModelSerializer


class OrderProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProductsModel
        fields = "__all__"


class OrderSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    items = OrderProductsSerializer(many=True, required=True)

    class Meta:
        model = OrderModel
        fields = ('id', 'items')
