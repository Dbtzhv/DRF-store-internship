from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import UserModel
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny


class UserAPIView(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

# Class based view to register user


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
