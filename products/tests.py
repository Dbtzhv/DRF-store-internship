# import pytest
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from mixer.backend.django import mixer
# from products.models import ProductCategoryModel
# from users.models import UserModel
# from rest_framework_simplejwt.tokens import AccessToken


# @pytest.fixture
# def api_client():
#     return APIClient()


# @pytest.fixture
# def user():
#     email = 'superuser@example.com'
#     password = 'testpass123'
#     return UserModel.objects.create_superuser(
#         email=email,
#         password=password,
#     )


# @pytest.fixture
# def product_category():
#     return mixer.blend(ProductCategoryModel)


# @pytest.fixture
# def token(user):
#     access_token = AccessToken.for_user(user)
#     return f'Bearer {access_token}'


# @pytest.mark.django_db
# def test_create_product_category(api_client, user, token):
#     headers = {'Authorization': token}

#     data = {
#         'name': 'Test category',
#         'description': 'Test description'
#     }

#     print('Token:', token)
#     print('Headers:', headers)
#     response = api_client.post(
#         reverse('products:productcategory-list'), data=data, headers=headers)

#     assert response.status_code == status.HTTP_201_CREATED
#     assert ProductCategoryModel.objects.filter(name=data['name']).exists()


# def test_delete_product_category(api_client, user, product_category):
#     api_client.force_authenticate(user=user)

#     response = api_client.delete(reverse('products:productcategory-detail', args=[product_category.id]))

#     assert response.status_code == status.HTTP_204_NO_CONTENT
#     assert not ProductCategoryModel.objects.filter(id=product_category.id).exists()


# def test_create_product_category_with_invalid_data(api_client, user):
#     api_client.force_authenticate(user=user)

#     data = {
#         'name': '',
#         'description': 'Test description'
#     }

#     response = api_client.post(reverse('products:productcategory-list'), data=data)

#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert not ProductCategoryModel.objects.filter(description=data['description']).exists()
