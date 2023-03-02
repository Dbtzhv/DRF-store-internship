from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import UserModel
from .serializers import UserSerializer, RegisterSerializer


class UserAPIView(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

# Class based view to register user


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
