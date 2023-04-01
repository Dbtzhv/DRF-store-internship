from decimal import Decimal
import pytest
from django.urls import reverse
from cart.serializers import CartSerializer
from products.models import ProductModel
import pytest
from mixer.backend.django import mixer
from users.models import UserModel
from rest_framework.test import APIClient
from cart.models import CartModel, CartItemModel


# Create your tests here.
@pytest.fixture
def product():
    return mixer.blend(ProductModel, general_quantity=10)


@pytest.fixture
def cart():
    return mixer.blend(CartModel)


@pytest.fixture
def user():
    email = 'test@example.com'
    password = 'testpassword'
    return UserModel.objects.create_superuser(
        email=email,
        password=password,
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_cart_create(user, api_client, product):
    payload = {"status": "new", "items": [
        {"status": "available", "quantity": 0, "product": str(product.id)}]}
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse('cart:carts-list'), data=payload, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_cart_update(product, api_client, user, cart):
    payload = {"status": "new", "items": [
        {"status": "available", "quantity": 10, "product": str(product.id)}]}
    api_client.force_authenticate(user=user)
    response = api_client.put(reverse(
        'cart:carts-detail', kwargs={'pk': cart.id}), data=payload, format='json')
    assert response.status_code in (200, 201)


@pytest.mark.django_db
@pytest.mark.parametrize('data, expected', [
    (
        {
            'status': 'new',
            "items": [{"status": "available", "quantity": 0, "product": None}],
        },
        True
    ),
    (
        {
            'status': 'new',
            "items": [{"status": "available", "quantity": 'invalid', "product": None}],
        },
        False
    ),
])
def test_cart_serializer_valid_data(data, product, expected):
    data['items'][0]['product'] = product.id
    serializer = CartSerializer(data=data)
    assert serializer.is_valid() == expected
    if not expected:
        assert serializer.errors
