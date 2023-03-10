
from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import ProductModel, ProductCategoryModel
from .serializers import ProductSerializer, ProductCategorySerializer


# Create your views here.


class ProductAPIView(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer


class ProductCategoryAPIView(viewsets.ModelViewSet):
    queryset = ProductCategoryModel.objects.all()
    serializer_class = ProductCategorySerializer
