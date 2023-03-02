from django.db import models
import uuid


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=82)
    category = models.CharField(max_length=82)
    description = models.TextField(max_length=256)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    general_quantity = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
