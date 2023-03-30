from django.db.models import Sum, F
from orders.services import make_order
from utils.exceptions import CartError
from cart.models import CartModel, CartItemModel
from orders.models import OrderModel, OrderProductsModel
import pytest
from django.urls import reverse
import pytest
from mixer.backend.django import mixer
from users.models import UserModel
from rest_framework.test import APIClient
from cart.models import CartModel
from orders.models import OrderModel
from products.models import ProductModel


# Create your tests here.
@pytest.fixture
def user():
    return mixer.blend(UserModel)


@pytest.fixture
def product():
    return mixer.blend(ProductModel)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def cart():
    return mixer.blend(CartModel)


@pytest.fixture
def order():
    return mixer.blend(OrderModel)


@pytest.mark.django_db
def test_order_create(user, api_client, cart):
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse('orders:place_order', kwargs={'cart_id': str(cart.id)}), format='json')
    assert response.status_code in (200, 201)


@pytest.mark.django_db
def test_order_update(user, api_client, order, product):
    payload = {"items": [{"quantity": 0, "product_price": "62",
                          "product": product.id, "order": order.id}]}
    api_client.force_authenticate(user=user)
    response = api_client.put(
        reverse('orders:order-detail', kwargs={'pk': order.id}), data=payload, format='json')
    assert response.status_code in (200, 201)


@pytest.fixture
def cart_with_items():
    cart = mixer.blend(CartModel)
    mixer.blend(CartItemModel, cart=cart)
    mixer.blend(CartItemModel, cart=cart)
    return cart


@pytest.fixture
def cart_with_unavailable_items():
    cart = mixer.blend(CartModel, status='not available')
    mixer.blend(CartItemModel, cart=cart)
    return cart


@pytest.mark.django_db
def test_make_order_success(cart_with_items):
    cart_id = cart_with_items.id
    make_order(cart_with_items)
    order = OrderModel.objects.first()
    order_products = OrderProductsModel.objects.filter(order=order)
    assert order.user == cart_with_items.user
    assert order.total_price == cart_with_items.items.aggregate(
        total_price=Sum(F('product__price') * F('quantity')))['total_price']
    assert order_products.count() == cart_with_items.items.count()
    for order_item in order_products:
        cart_item = cart_with_items.items.get(product=order_item.product)
        assert order_item.quantity == cart_item.quantity
        assert order_item.product_price == cart_item.product.price
        assert order_item.order == order
    assert cart_with_items.status == 'ordered'


@pytest.mark.django_db
def test_make_order_cart_unavailable(cart_with_unavailable_items):
    with pytest.raises(CartError, match="Корзина содержит товары со статусом 'недоступен'"):
        make_order(cart_with_unavailable_items)
    assert OrderModel.objects.count() == 0
    assert OrderProductsModel.objects.count() == 0
