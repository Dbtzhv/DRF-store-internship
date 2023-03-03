from django.urls import path, include
from rest_framework import routers
from orders.views import OrderAPIView, OrderProductsAPIView


app_name = 'orders'

orders_router = routers.SimpleRouter()
orders_router.register('orders', OrderAPIView)

orderproducts_router = routers.SimpleRouter()
orderproducts_router.register('orderproducts', OrderProductsAPIView)

urlpatterns = [
    path('', include(orders_router.urls)),
    path('', include(orderproducts_router.urls)),
]
