# Generated by Django 4.1.7 on 2023-03-22 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_cartitemmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitemmodel',
            name='status',
            field=models.CharField(blank=True, choices=[('available', 'Доступен'), ('not available', 'Недоступен'), ('deleted', 'Удалён')], default='available', max_length=13),
        ),
        migrations.AlterField(
            model_name='cartmodel',
            name='status',
            field=models.CharField(blank=True, choices=[('new', 'Новая'), ('ordered', 'Заказана'), ('deleted', 'Удалена')], default='new', max_length=7),
        ),
    ]
