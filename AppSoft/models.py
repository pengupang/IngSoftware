from django.db import models
import datetime

# Create your models here.
class MateriaPrima(models.Model):
    nombre = models.CharField(max_length=60)
    unidadMedida= models.CharField(max_length=5)
    estadoMateria = models.BooleanField()
    def __str__(self):
        return self.nombre

class Proveedores (models.Model):
    nombre = models.CharField(max_length=50)
    contacto = models.CharField(max_length=12) 
    def __str__(self):
        return self.nombre

class Productos (models.Model):
    nombre = models.CharField(max_length=60)
    cantidad = models.IntegerField()
    estadoProducto = models.BooleanField()

class Usuario (models.Model):
    nombre= models.CharField(max_length=60)
    contraseña = models.CharField(max_length=10)
    rol = models.CharField(max_length=30)
    estadoUsuario = models.BooleanField()

class Compra (models.Model):
    fecha = models.DateField(default=datetime.date.today)
    proveedor = models.ForeignKey(Proveedores,on_delete=models.CASCADE, related_name='proveedor_compras')
    lote = models.IntegerField()
    cantidad = models.IntegerField()
    materia = models.ForeignKey(MateriaPrima,on_delete=models.CASCADE , related_name= 'materia_compras')
    def __str__(self) :
        return f"{self.materia} - {self.proveedor.nombre}" 