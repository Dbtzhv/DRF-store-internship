from users.serializers import UserSerializer
import pytest
from users.serializers import RegisterSerializer
from users.models import UserModel
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    email = 'test@example.com'
    password = 'testpassword'
    return UserModel.objects.create(
        email=email,
        password=password,
    )


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
def test_update_user(client, user):
    """Test updating user data"""
    client.force_authenticate(user=user)
    payload = {
        'email': 'new_mail@example.com'
    }
    response = client.put(
        reverse('users:user-detail', kwargs={'pk': user.id}), data=payload)
    data = response.data

    assert data['email'] == payload['email']


@pytest.mark.django_db
def test_registration_api(client):
    payload = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'password2': 'testpass123',
    }
    response = client.post('/register/', data=payload)
    data = response.data

    assert data['email'] == payload['email']
    assert 'access_token' in data
