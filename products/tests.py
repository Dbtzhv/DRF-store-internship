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
def test_product_category_creation(user, api_client):
    payload = {"name": "new_name",
               "description": "new_description",
               "user": str(user.id)}
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse('products:productcategory-list'), data=payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_product_category_update(user, product_category, api_client):
    payload = {"name": "new_name",
               "description": "new_description",
               "user": str(user.id)}
    api_client.force_authenticate(user=user)
    response = api_client.put(reverse(
        'products:productcategory-detail', kwargs={'pk': product_category.id}), data=payload)
    data = response.data
    assert data["name"] == payload["name"]


@pytest.mark.django_db
def test_product_category_access(user, api_client, product_category):
    api_client.force_authenticate(user=user)
    response = api_client.get(
        f'/categories/{product_category.id}/')
    assert response.status_code == 200, 'Failed to access product category details'


# products

@pytest.mark.django_db
def test_product_creation(user, api_client, product_category, base64_image):
    payload = {"title": "title",
               "category": str(product_category.id),
               "description": "description",
               "price": "50.00",
               "general_quantity": 5,
               "parameters": [{"name": "Рост", "value": "15kg"}],
               "images": [{"picture": base64_image}]
               }
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse('products:product-list'), data=payload, format='json')
    print(response.data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_product_update(user, api_client, product_category, base64_image, product):
    payload = {"title": "new_title",
               "category": str(product_category.id),
               "description": "new_description",
               "price": "100.00",
               "general_quantity": 10,
               "parameters": [{"name": "Вес", "value": "10kg"}],
               "images": [{"picture": base64_image}]
               }
    api_client.force_authenticate(user=user)
    response = api_client.put(
        reverse('products:product-detail', kwargs={'pk': product.id}), data=payload, format='json')
    print(response.data, '++++++34647')
    assert response.status_code in (200, 201)
