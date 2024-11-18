# Generated by Django 5.1 on 2024-11-18 16:03

import AppSoft.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppSoft', '0002_remove_productomateria_cantidad_usada_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='cantidad',
            field=models.FloatField(validators=[AppSoft.validators.MinValueValidator(0.0)]),
        ),
    ]
