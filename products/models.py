import uuid
from django.db import models
from autoslug.fields import AutoSlugField
from slugify import slugify


def set_slugify(value) -> str:
    return slugify(value).replace(' ', '-')


class ProductCategoryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, verbose_name='Категория')
    description = models.TextField(
        null=True, blank=True, verbose_name='Описание')
    slug = AutoSlugField(populate_from='name',
                         slugify=set_slugify)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=82, verbose_name='Товар')
    category = models.ForeignKey(
        ProductCategoryModel, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    description = models.TextField(max_length=256, verbose_name='Описание')
    price = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name='Цена')
    general_quantity = models.IntegerField(verbose_name='Общее количество')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class PictureModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(
        upload_to='products_images', verbose_name='Изображение')
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, verbose_name='Продукт', related_name='images')

    def __str__(self):
        return self.picture.url

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class ParameterModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, verbose_name='Название')
    value = models.CharField(max_length=255, verbose_name='Значение')
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, verbose_name='Параметры', related_name='parameters')

    def __str__(self):
        return f'{self.name} : {self.value}'

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"
