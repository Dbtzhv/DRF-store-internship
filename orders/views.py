from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import OrderModel, OrderProductsModel
from .serializers import OrderSerializer, OrderProductsSerializer

# Create your views here.


class OrderAPIView(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer


class OrderProductsAPIView(viewsets.ModelViewSet):
    queryset = OrderProductsModel.objects.all()
    serializer_class = OrderProductsSerializer
