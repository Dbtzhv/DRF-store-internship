# Generated by Django 3.2.18 on 2023-03-10 14:26

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alter_productcategorymodel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategorymodel',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name'),
        ),
    ]