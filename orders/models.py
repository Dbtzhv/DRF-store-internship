from django.db import models
from users.models import UserModel
import uuid
from products.models import ProductModel


class OrderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(
        to=UserModel, related_name='orders', verbose_name='user email', on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        'Дата создания', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)
    order_sum = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderProductsModel(models.Model):
    order_id = models.ForeignKey(
        to=OrderModel, related_name='products', on_delete=models.CASCADE)
    product_id = models.ForeignKey(
        to=ProductModel, related_name='order', verbose_name='product title', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'order:{self.order_id}; product:{self.product_id}'

    class Meta:
        verbose_name = "Товары в заказе"
        verbose_name_plural = "Товары в заказах"
