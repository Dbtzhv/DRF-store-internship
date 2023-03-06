from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import ProductModel
from .serializers import ProductSerializer


# Create your views here.


class ProductAPIView(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
