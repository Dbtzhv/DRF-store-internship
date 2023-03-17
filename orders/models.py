import uuid
from django.db import models
from users.models import UserModel
from products.models import ProductModel


class OrderModel(models.Model):

    ORDER_STATUS = (
        ('n', 'Новый'),
        ('p', 'Оплачен'),
        ('s', 'Отправлен'),
        ('c', 'Завершен'),
    )

    status = models.CharField(
        max_length=1, choices=ORDER_STATUS, blank=True, default='n')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='orders', verbose_name='Принадлежит')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ('-created_at',)


class OrderProductsModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, related_name='order_items', verbose_name="Продукт")
    quantity = models.IntegerField(verbose_name="Количество")
    order = models.ForeignKey(
        OrderModel, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")

    class Meta:
        verbose_name = "Товар заказа"
        verbose_name_plural = "Товары заказа"
