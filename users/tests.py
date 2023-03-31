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
@pytest.mark.parametrize('data, expected_result', [
    ({'email': 'test@example.com', 'password': 'testpass123',
     'password2': 'testpass123'}, True),
    ({'email': 'test@example.com', 'password': 'testpass123',
     'password2': 'wrongpass'}, False),
    ({'email': 'invalid_email', 'password': 'testpass123',
     'password2': 'testpass123'}, False),
    ({'email': 'invalid_email', 'password': 'testpass123',
     'password2': 'wrongpass'}, False),
])
def test_register_serializer(data, expected_result):
    """Test creating a user using the RegisterSerializer"""
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() == expected_result
    if not expected_result:
        assert serializer.errors


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
