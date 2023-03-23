import uuid
from django.db import models
from users.models import UserModel
from products.models import ProductModel
from orders.models import OrderProductsModel, OrderModel
from cart.services import CartError
from .services import make_order


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
        # if self.status != 'not available':
        #     order = OrderModel.objects.create(
        #         user=self.user,
        #         total_price=sum(
        #             [i.quantity*i.product.price for i in CartItemModel.objects.filter(cart=self.id)])
        #     )

        #     for item in CartItemModel.objects.filter(cart=self.id):
        #         OrderProductsModel.objects.create(
        #             order=order,
        #             product=item.product,
        #             quantity=item.quantity,
        #             product_price=item.product.price
        #         )

        #         item.product.general_quantity -= item.quantity
        #         item.product.save()

        #     self.status = 'ordered'
        #     self.save()

        # else:
        #     raise CartError("Корзина содержит товары со статусом 'недоступен'")


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
