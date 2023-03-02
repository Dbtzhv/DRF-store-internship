"""loftstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import UserAPIView, RegisterUserAPIView
from orders.views import OrderAPIView, OrderProductsAPIView
from products.views import ProductAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

users_router = routers.SimpleRouter()
users_router.register('users', UserAPIView)

orders_router = routers.SimpleRouter()
users_router.register('orders', OrderAPIView)

orderproducts_router = routers.SimpleRouter()
orderproducts_router.register('orderproducts', OrderProductsAPIView)

products_router = routers.SimpleRouter()
products_router.register('products', ProductAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(users_router.urls)),
    path('api/v1/', include(orders_router.urls)),
    path('api/v1/', include(orderproducts_router.urls)),
    path('api/v1/', include(products_router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/register/', RegisterUserAPIView.as_view()),
]
