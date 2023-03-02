from rest_framework import serializers
from .models import OrderModel, OrderProductsModel


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"


class OrderProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProductsModel
        fields = "__all__"
