from rest_framework import serializers
from .models import CartModel, CartItemModel


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartModel
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItemModel
        fields = "__all__"
