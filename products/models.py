import uuid
from django.db import models


class ProductCategoryModel(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=82)
    category = models.ForeignKey(
        ProductCategoryModel, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(max_length=256)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    general_quantity = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class PictureModel(models.Model):
    picture = models.ImageField(upload_to='products_images')
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.picture.url

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
