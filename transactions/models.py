import uuid
from django.db import models
from orders.models import OrderModel


class PaymentTransactionModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE,
                              related_name='transactions', verbose_name="Заказ")
    verification_text = models.CharField(
        max_length=255, blank=True, verbose_name="№ Чека")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Транзакция оплаты"
        verbose_name_plural = "Транзакции оплаты"
        ordering = ('-created_at',)
