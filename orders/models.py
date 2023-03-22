import uuid
from django.db import models
from users.models import UserModel
from products.models import ProductModel


class OrderModel(models.Model):

    ORDER_STATUS = (
        ('new', 'Новый'),
        ('paid', 'Оплачен'),
        ('sent', 'Отправлен'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменён')
    )

    status = models.CharField(
        max_length=9, choices=ORDER_STATUS, blank=True, default='new')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='orders', verbose_name='Принадлежит')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления")
    total_price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='К оплате')

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
    product_price = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = "Товар заказа"
        verbose_name_plural = "Товары заказа"
