# Generated by Django 5.1 on 2024-11-10 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppSoft', '0009_alter_compra_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='cantidad',
            field=models.FloatField(default=0),
        ),
    ]