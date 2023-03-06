from django.urls import path, include
from rest_framework import routers
from .views import CartAPIView, CartItemAPIView


app_name = 'cart'

cart_router = routers.SimpleRouter()
cart_router.register('cart', CartAPIView)

cartitems_router = routers.SimpleRouter()
cartitems_router.register('cart-item', CartItemAPIView)

urlpatterns = [
    path('', include(cart_router.urls)),
    path('', include(cartitems_router.urls)),
]
