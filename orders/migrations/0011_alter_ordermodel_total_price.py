# Generated by Django 4.1.7 on 2023-03-30 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_orderproductsmodel_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='К оплате'),
        ),
    ]
