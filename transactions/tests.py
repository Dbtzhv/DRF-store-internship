import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from transactions.models import PaymentTransactionModel
from orders.models import OrderModel
from users.models import UserModel


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
def test_create_payment_transaction(api_client, user, order):
    api_client.force_authenticate(user=user)

    data = {
        'order': order.id,
        'status': 'completed',
        'payment_id': '123456',
        'data': {'some': 'data'},
        'value': '100.00',
        'operation_type': 'some type'
    }

    response = api_client.post(
        reverse('transactions:paymenttransaction-list'), data=data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert PaymentTransactionModel.objects.count() == 1

    transaction = PaymentTransactionModel.objects.first()

    assert str(transaction.order.id) == str(order.id)
    assert transaction.status == 'completed'
    assert transaction.payment_id == '123456'
    assert transaction.data == {'some': 'data'}
    assert str(transaction.value) == '100.00'
    assert transaction.operation_type == 'some type'


# update
@pytest.mark.django_db
def test_update_payment_transaction(api_client, user, order, transaction):
    api_client.force_authenticate(user=user)

    data = {
        'status': 'declined',
        'value': '50.00'
    }

    response = api_client.patch(
        reverse('transactions:paymenttransaction-detail',
                args=[transaction.id]),
        data=data,
        format='json'
    )

    assert response.status_code == status.HTTP_200_OK

    updated_transaction = PaymentTransactionModel.objects.get(
        id=transaction.id)
    assert updated_transaction.status == 'declined'
    assert str(updated_transaction.value) == '50.00'
