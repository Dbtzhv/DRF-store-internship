import uuid
from django.db import models
from orders.models import OrderModel


class PaymentTransactionModel(models.Model):
    TRANSACTION_STATUS = (
        ('completed', 'Произведена'),
        ('incompleted', 'Не произведена'),
        ('declined', 'Отклонена')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE,
                              related_name='transactions', verbose_name="Заказ")
    status = models.CharField(
        max_length=11, choices=TRANSACTION_STATUS, blank=True, default='not completed')
    payment_id = models.CharField(
        max_length=128, verbose_name='Идентификатор оплаты')
    data = models.JSONField()
    value = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name='Оплачено')
    operation_type = models.CharField(
        max_length=256, verbose_name='Тип операции')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Транзакция оплаты"
        verbose_name_plural = "Транзакции оплаты"
        ordering = ('-created_at',)
