import uuid
from django.db import models
from users.models import UserModel
from products.models import ProductModel


class CartModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


class CartItemModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    cart = models.ForeignKey(
        CartModel, on_delete=models.CASCADE, related_name='items')

    class Meta:
        verbose_name = "Товар корзины"
        verbose_name_plural = "Товары корзины"
