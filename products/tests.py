import json
import requests
from django.urls import reverse
from products.models import ProductCategoryModel
from products.models import ProductModel, ProductCategoryModel
import pytest
from mixer.backend.django import mixer
from products.models import ProductCategoryModel
from users.models import UserModel
from rest_framework.test import APIClient
import base64
from rest_framework import status
from products.serializers import ProductCategorySerializer


# categories

@pytest.fixture
def base64_image():
    with open(r'utils\Plato.jpg', 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def product_category():
    return mixer.blend(ProductCategoryModel)


@pytest.fixture
def product():
    return mixer.blend(ProductModel)


@pytest.fixture
def user():
    email = 'test@example.com'
    password = 'testpassword'
    return UserModel.objects.create_superuser(
        email=email,
        password=password,
    )


@pytest.mark.django_db
@pytest.mark.parametrize('data, expected_result', [
    (
        {
            'name': 'Картины',
            'description': 'Домашние картины',
            'user': None
        },
        True,
    ),
    (
        {
            'name': 'Картины',
            'user': 'invalid'
        },
        False,
    ),
])
def test_create_payment_transaction(data, expected_result, user):
    data['user'] = user.id if data['user'] != 'invalid' else 'invalid'
    serializer = ProductCategorySerializer(data=data)
    assert serializer.is_valid() == expected_result
    if not expected_result:
        assert serializer.errors


@pytest.mark.django_db
@pytest.mark.parametrize(
    'data, expected_status', [
        ({'name': 'name', 'description': 'description',
         'user': 'invalid'}, status.HTTP_400_BAD_REQUEST),
        ({'name': 'name', 'description': 'description',
         'user': None}, status.HTTP_201_CREATED),
        ({'name': 'name', 'description': 'description',
         'user': None}, status.HTTP_201_CREATED),
    ]
)
def test_product_category_creation(user, api_client, data, expected_status):
    data['user'] = user.id if data['user'] == None else 'invalid'
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse('products:productcategory-list'), data=data, format='json')
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'data, expected_status', [
        ({'name': 'name', 'description': 'description',
         'user': 'invalid'}, status.HTTP_400_BAD_REQUEST),
        ({'name': 'name', 'description': 'new_description',
         'user': None}, status.HTTP_200_OK),
        ({'name': 'new_name', 'description': 'description',
         'user': None}, status.HTTP_200_OK),
    ]
)
def test_product_category_update(user, product_category, api_client,  data, expected_status):
    data['user'] = user.id if data['user'] == None else 'invalid'
    api_client.force_authenticate(user=user)
    response = api_client.put(reverse(
        'products:productcategory-detail', kwargs={'pk': product_category.id}), data=data)
    r_data = response.data
    if expected_status != status.HTTP_400_BAD_REQUEST:
        assert r_data["name"] == data["name"]
        assert r_data["description"] == data["description"]
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_product_category_access(user, api_client, product_category):
    api_client.force_authenticate(user=user)
    response = api_client.get(
        f'/categories/{product_category.id}/')
    assert response.status_code == 200, 'Failed to access product category details'


# products

@pytest.mark.django_db
@pytest.mark.parametrize(
    'payload, expected_status', [
        ({"title": "title",
          "category": None,
          "description": "description",
          "price": "50.00",
          "general_quantity": 5,
          "parameters": [{"name": "Рост", "value": "15kg"}],
          "images": [{"picture": base64_image}]
          }, 201),
        ({"title": "new_title",
          "category": None,
          "description": "new_description",
          "price": "100.00",
          "general_quantity": 10,
          "parameters": [{"name": "Вес", "value": "10kg"}],
          "images": [{"picture": base64_image}]
          }, 200)
    ]
)
def test_product_creation_and_update(user, api_client, product, payload, expected_status, base64_image, product_category):
    payload['images'][0]["picture"] = base64_image
    payload['category'] = str(product_category.id)
    if expected_status == 200:
        url = reverse('products:product-detail', kwargs={'pk': product.id})
        method = api_client.put
    else:
        url = reverse('products:product-list')
        method = api_client.post
    api_client.force_authenticate(user=user)
    response = method(url, data=payload, format='json')
    assert response.status_code == expected_status
