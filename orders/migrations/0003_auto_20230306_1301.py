# Generated by Django 3.2.18 on 2023-03-06 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20230301_2236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordermodel',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderproductsmodel',
            options={'verbose_name': 'Товары в заказе', 'verbose_name_plural': 'Товары в заказах'},
        ),
    ]
