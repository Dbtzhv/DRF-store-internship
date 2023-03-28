from django.urls import path, include
from rest_framework import routers
from products.views import ProductAPIView, ProductCategoryAPIView


app_name = 'products'

products_router = routers.SimpleRouter()
products_router.register('products', ProductAPIView)

productcategories_router = routers.SimpleRouter()
productcategories_router.register(
    'categories', ProductCategoryAPIView, basename='productcategory')

urlpatterns = [
    path('', include(products_router.urls)),
    path('', include(productcategories_router.urls)),
]
