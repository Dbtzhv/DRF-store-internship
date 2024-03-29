# Generated by Django 4.1.7 on 2023-03-17 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0024_alter_productcategorymodel_slug'),
        ('orders', '0004_auto_20230310_1844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordermodel',
            options={'ordering': (
                '-created_at',), 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderproductsmodel',
            options={'verbose_name': 'Товар заказа',
                     'verbose_name_plural': 'Товары заказа'},
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='order_sum',
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='orderproductsmodel',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='orderproductsmodel',
            name='product_id',
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='status',
            field=models.CharField(blank=True, choices=[('n', 'Новый'), ('p', 'Оплачен'), (
                's', 'Отправлен'), ('c', 'Завершен')], default='n', max_length=1),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='user',
            field=models.ForeignKey(default='00673639-98a2-4380-9234-8deaa6f07653', on_delete=django.db.models.deletion.CASCADE,
                                    related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Принадлежит'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderproductsmodel',
            name='order',
            field=models.ForeignKey(default='af00fa7f-ff76-4657-a33c-3e5cde1e8831', on_delete=django.db.models.deletion.CASCADE,
                                    related_name='items', to='orders.ordermodel', verbose_name='Заказ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderproductsmodel',
            name='product',
            field=models.ForeignKey(default='af00fa7f-ff76-4657-a33c-3e5cde1e8830', on_delete=django.db.models.deletion.CASCADE,
                                    related_name='order_items', to='products.productmodel', verbose_name='Продукт'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='created_at',
            field=models.DateTimeField(
                auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='updated_at',
            field=models.DateTimeField(
                auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='orderproductsmodel',
            name='id',
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
