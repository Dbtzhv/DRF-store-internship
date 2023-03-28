from rest_framework import viewsets
from .models import ProductModel, ProductCategoryModel
from .serializers import ProductSerializer, ProductCategorySerializer
from utils.permissions import IsAdminUserOrReadOnly


class ProductAPIView(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer


class ProductCategoryAPIView(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = ProductCategoryModel.objects.all()
    serializer_class = ProductCategorySerializer
