from rest_framework import serializers
from .models import UserModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('password', 'is_superuser', 'is_staff',
                   'groups', 'user_permissions')


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=UserModel.objects.all().values_list('email'))])
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Пароли не совпадают!"})
        return attrs

    def create(self, validated_data):
        user = UserModel.objects.create(email=validated_data['email'],)
        user.set_password(validated_data['password'])
        user.save()
        return user
