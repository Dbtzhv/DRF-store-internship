from django.urls import path, include
from rest_framework import routers
from orders.views import OrderAPIView, OrderProductsAPIView, Place_OrderView


app_name = 'orders'

orders_router = routers.SimpleRouter()
orders_router.register('orders', OrderAPIView, basename='order')

orderproducts_router = routers.SimpleRouter()
orderproducts_router.register(
    'orderproducts', OrderProductsAPIView, basename='orderproduct')

urlpatterns = [
    path('', include(orders_router.urls)),
    path('', include(orderproducts_router.urls)),
    path('orders/<uuid:cart_id>/place_order/',
         Place_OrderView, name='place_order'),
]
