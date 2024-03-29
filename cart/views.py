from .models import CartModel
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, viewsets
from .models import CartItemModel, CartModel
from .serializers import CartItemSerializer, CartSerializer
from utils.exceptions import CartError


# Create your views here.


class CartAPIView(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

    queryset = CartModel.objects.all()
    serializer_class = CartSerializer


class CartItemAPIView(viewsets.ModelViewSet):

    queryset = CartItemModel.objects.all()
    serializer_class = CartItemSerializer
