from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import CartItemModel, CartModel
from .serializers import CartItemSerializer, CartSerializer


# Create your views here.


class CartAPIView(viewsets.ModelViewSet):
    queryset = CartModel.objects.all()
    serializer_class = CartSerializer


class CartItemAPIView(viewsets.ModelViewSet):
    queryset = CartModel.objects.all()
    serializer_class = CartItemSerializer
