from users.serializers import UserSerializer
import pytest
from users.serializers import RegisterSerializer
from users.models import UserModel
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.mark.django_db
def test_create_user():
    """Test creating a new user"""
    email = 'test@example.com'
    password = 'testpass123'
    user = UserModel.objects.create_user(
        email=email,
        password=password,
    )
    assert user.email == email
    assert user.check_password(password)


@pytest.mark.django_db
def test_create_superuser():
    """Test creating a new superuser and checking JWT-auth"""
    email = 'superuser@example.com'
    password = 'testpass123'
    superuser = UserModel.objects.create_superuser(
        email=email,
        password=password,
    )
    assert superuser.email == email
    assert superuser.check_password(password)
    assert superuser.is_staff is True
    assert superuser.is_superuser is True

    client = APIClient()
    url = reverse('users:token_obtain_pair')
    data = {'email': email, 'password': password}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_register_serializer_valid_data():
    """Test creating a user with valid data using the RegisterSerializer"""
    data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'password2': 'testpass123',
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is True


@pytest.mark.django_db
def test_register_serializer_invalid_data():
    """Test creating a user with invalid data using the RegisterSerializer"""
    data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'password2': 'wrongpass',
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is False
    assert 'password' in serializer.errors


@pytest.mark.django_db
def test_update_user():
    """Test updating user data"""
    email = 'test@example.com'
    password = 'testpass123'
    new_email = 'newtest@example.com'
    new_first_name = 'New'
    new_last_name = 'Test'
    user = UserModel.objects.create_user(
        email=email,
        password=password,
        first_name='Old',
        last_name='Test',
    )
    serializer = UserSerializer(instance=user, data={
        'email': new_email,
        'first_name': new_first_name,
        'last_name': new_last_name,
    }, partial=True)
    assert serializer.is_valid() is True
    serializer.save()
    user.refresh_from_db()
    assert user.email == new_email
    assert user.first_name == new_first_name
    assert user.last_name == new_last_name


@pytest.mark.django_db
def test_update_user_with_invalid_data():
    """Test updating user data with invalid data"""
    email = 'test@example.com'
    password = 'testpass123'
    new_email = 'newtest'
    new_first_name = 'New'
    new_last_name = 'Newy'
    user = UserModel.objects.create_user(
        email=email,
        password=password,
        first_name='Old',
        last_name='Test',
    )
    serializer = UserSerializer(instance=user, data={
        'email': new_email,
        'first_name': new_first_name,
        'last_name': new_last_name,
    }, partial=True)
    assert serializer.is_valid() is False
