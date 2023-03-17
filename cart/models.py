import uuid
from django.db import models
from users.models import UserModel
from products.models import ProductModel
from orders.models import OrderProductsModel, OrderModel


class CartModel(models.Model):

    CART_STATUS = (
        ('n', 'Новая'),
        ('o', 'Заказана'),
        ('d', 'Удалена'),
    )

    status = models.CharField(
        max_length=1, choices=CART_STATUS, blank=True, default='n')
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
        order = OrderModel.objects.create(
            user=self.user,
        )

        for item in self.items.all():
            OrderProductsModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )

        for item in self.items.all():
            item.product.general_quantity -= item.quantity
            item.product.save()
            if item.product.general_quantity <= 0:
                item.delete()

        self.status = 'o'
        self.save()


class CartItemModel(models.Model):

    CARTITEM_STATUS = (
        ('a', 'Доступен'),
        ('n', 'Недоступен'),
        ('d', 'Удалён'),
    )

    status = models.CharField(
        max_length=1, choices=CARTITEM_STATUS, blank=True, default='a')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, related_name='items', verbose_name="Продукт")
    quantity = models.IntegerField(verbose_name="Количество")
    cart = models.ForeignKey(
        CartModel, on_delete=models.CASCADE, related_name='items', verbose_name="Корзина")

    class Meta:
        verbose_name = "Товар корзины"
        verbose_name_plural = "Товары корзины"
