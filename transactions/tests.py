import uuid
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from transactions.serializers import PaymentTransactionSerializer
from transactions.models import PaymentTransactionModel
from orders.models import OrderModel
from users.models import UserModel
from mixer.backend.django import mixer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserModel.objects.create(
        email='testuser@example.com',
        password='testpass'
    )


@pytest.fixture
def order(db, user):
    return OrderModel.objects.create(
        user=user,
        total_price=100.00
    )


@pytest.fixture
def transaction(db, order):
    return PaymentTransactionModel.objects.create(
        order=order,
        status='completed',
        payment_id='123456',
        data={'some': 'data'},
        value=100.00,
        operation_type='some type'
    )

# create


@pytest.mark.django_db
@pytest.mark.parametrize(
    'data, expected_status', [
        # Valid data
        ({
            'order': None,
            'status': 'completed',
            'payment_id': '123456',
            'data': {'some': 'data'},
            'value': '100.00',
            'operation_type': 'some type'
        }, status.HTTP_201_CREATED),
        # Invalid value type
        ({
            'order': None,
            'status': 'completed',
            'payment_id': '123456',
            'data': {'some': 'data'},
            'value': 'invalid',
            'operation_type': 'some type'
        }, status.HTTP_400_BAD_REQUEST),
        # Non-existent order id
        ({
            'order': 999,
            'status': 'completed',
            'payment_id': '123456',
            'data': {'some': 'data'},
            'value': '100.00',
            'operation_type': 'some type'
        }, status.HTTP_400_BAD_REQUEST),
    ]
)
def test_create_payment_transaction(api_client, user, order, data, expected_status):
    api_client.force_authenticate(user=user)
    data['order'] = order.id if data['order'] != 999 else 999

    response = api_client.post(
        reverse('transactions:paymenttransaction-list'), data=data, format='json')

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_201_CREATED:
        transaction = PaymentTransactionModel.objects.first()
        assert str(transaction.order.id) == str(order.id)
        assert transaction.status == 'completed'
        assert transaction.payment_id == '123456'
        assert transaction.data == {'some': 'data'}
        assert str(transaction.value) == '100.00'
        assert transaction.operation_type == 'some type'
    else:
        for error in response.data:
            print(error)
            assert 'value' in error or 'order' in error


# update


@pytest.mark.django_db
@pytest.mark.parametrize(
    'data, expected_status', [
        ({'status': 'declined', 'value': '50.00'}, status.HTTP_200_OK),
        ({'status': 'invalid_status', 'value': '50.00'}, status.HTTP_400_BAD_REQUEST),
        ({'status': 'invalid_status', 'value': '50.00'}, status.HTTP_400_BAD_REQUEST),
    ]
)
def test_update_payment_transaction(api_client, user, transaction, data, expected_status):
    api_client.force_authenticate(user=user)

    response = api_client.patch(
        reverse('transactions:paymenttransaction-detail',
                args=[transaction.id]),
        data=data,
        format='json'
    )

    assert response.status_code == expected_status

    updated_transaction = PaymentTransactionModel.objects.get(
        id=transaction.id)
    transaction.refresh_from_db()
    if response.status_code == status.HTTP_200_OK:
        assert updated_transaction.status == data['status']
        assert str(updated_transaction.value) == data['value']


@pytest.mark.django_db
@pytest.mark.parametrize('data, expected_result', [
    (
        {
            'status': 'completed',
            'payment_id': '1234-5678-90',
            'data': {'foo': 'bar'},
            'value': '100.00',
            'operation_type': 'payment',
            'order': None
        },
        True,
    ),
    (
        {
            'status': 'invalid_status',
            'payment_id': '1234-5678-90',
            'data': {'foo': 'bar'},
            'value': '100.00',
            'operation_type': 'payment',
            'order': None
        },
        False,
    ),
])
def test_create_payment_transaction(data, expected_result, order):
    data['order'] = order.id
    serializer = PaymentTransactionSerializer(data=data)
    assert serializer.is_valid() == expected_result
    if not expected_result:
        assert serializer.errors
