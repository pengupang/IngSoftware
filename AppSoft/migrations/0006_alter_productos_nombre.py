# Generated by Django 5.1.1 on 2024-12-03 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppSoft', '0005_alter_productos_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='nombre',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]
