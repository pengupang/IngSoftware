# Generated by Django 5.1.1 on 2024-12-03 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppSoft', '0003_alter_compra_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='nombre',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]
