# Generated by Django 5.1 on 2024-11-10 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppSoft', '0011_alter_compra_cantidad_alter_compra_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='cantidad',
            field=models.FloatField(),
        ),
    ]
