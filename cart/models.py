import uuid
from django.db import models
from users.models import UserModel
from products.models import ProductModel
from orders.models import OrderProductsModel, OrderModel
from orders.services import make_order


class CartModel(models.Model):

    CART_STATUS = (
        ('new', 'Новая'),
        ('not available', 'Недоступна'),
        ('ordered', 'Заказана'),
        ('deleted', 'Удалена'),
    )

    status = models.CharField(
        max_length=13, choices=CART_STATUS, blank=True, default='new')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='cart', verbose_name='Принадлежит')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ('-created_at',)

    def place_order(self):
        make_order(self)


class CartItemModel(models.Model):

    CARTITEM_STATUS = (
        ('available', 'Доступен'),
        ('not available', 'Недоступен'),
        ('deleted', 'Удалён'),
    )

    status = models.CharField(
        max_length=13, choices=CARTITEM_STATUS, blank=True, default='available')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, related_name='items', verbose_name="Продукт")
    quantity = models.IntegerField(verbose_name="Количество")
    cart = models.ForeignKey(
        CartModel, on_delete=models.CASCADE, related_name='items', verbose_name="Корзина")

    class Meta:
        verbose_name = "Товар корзины"
        verbose_name_plural = "Товары корзины"
