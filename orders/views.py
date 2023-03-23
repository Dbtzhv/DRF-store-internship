from django.shortcuts import render
from rest_framework import generics, viewsets
from .services import CartError
from .models import OrderModel, OrderProductsModel
from .serializers import OrderSerializer, OrderProductsSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cart.models import CartModel

# Create your views here.


class OrderAPIView(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer


class OrderProductsAPIView(viewsets.ModelViewSet):
    queryset = OrderProductsModel.objects.all()
    serializer_class = OrderProductsSerializer


@api_view(['POST'])
def Place_OrderView(request, cart_id):
    try:
        cart = CartModel.objects.get(pk=cart_id)
    except CartModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        cart.place_order()
    except CartError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Order placed successfully'})
