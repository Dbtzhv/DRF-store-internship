from django.urls import path, include
from rest_framework import routers
from .views import PaymentTransactionAPIView


app_name = 'transactions'

transactions_router = routers.SimpleRouter()
transactions_router.register(
    'transactions', PaymentTransactionAPIView, basename='paymenttransaction')

urlpatterns = [
    path('', include(transactions_router.urls)),
]
