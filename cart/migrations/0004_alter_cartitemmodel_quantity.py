# Generated by Django 3.2.18 on 2023-03-06 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_cartitemmodel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitemmodel',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
