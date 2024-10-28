from django.db import models

# Create your models here.
class MateriaPrima(models.Model):
    nombre = models.CharField(max_length=60)
    cantidad = models.FloatField()
    unidadMedida= models.CharField(max_length=5)
    estadoMateria = models.BooleanField()


class Proveedores (models.Model):
    nombre = models.CharField(max_length=50)
    contacto = models.CharField(max_length=12) 

class Productos (models.Model):
    nombre = models.CharField(max_length=60)
    cantidad = models.IntegerField()
    estadoProducto = models.BooleanField()

class Usuario (models.Model):
    nombre= models.CharField(max_length=60)
    contraseña = models.CharField(max_length=10)
    rol = models.CharField(max_length=30)
    estadoUsuario = models.BooleanField()