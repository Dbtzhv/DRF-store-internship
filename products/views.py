
from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import ProductModel, ProductCategoryModel
from .serializers import ProductSerializer, ProductCategorySerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS

# Create your views here.


class IsAdminUserOrReadOnly(BasePermission):
    """
    Allows access only to admin users or read only.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff or request.method in SAFE_METHODS)


class ProductAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer


class ProductCategoryAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = ProductCategoryModel.objects.all()
    serializer_class = ProductCategorySerializer
