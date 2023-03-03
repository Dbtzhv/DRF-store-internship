from django.urls import path, include
from rest_framework import routers
from products.views import ProductAPIView


app_name = 'products'

products_router = routers.SimpleRouter()
products_router.register('products', ProductAPIView)

urlpatterns = [
    path('', include(products_router.urls)),
]
