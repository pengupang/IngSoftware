from django.db import models
import datetime

# Create your models here.
class MateriaPrima(models.Model):
    UNIDAD_MEDIDA = [
        ('kg', 'Kilogramo'),
        ('g', 'Gramo'),
        ('l', 'Litro'),
        ('ml', 'Mililitro'),
        # Agrega más opciones según tus necesidades
    ]
    
    nombre = models.CharField(max_length=60)
    cantidad = models.FloatField()
    unidadMedida= models.CharField(max_length=5,choices=UNIDAD_MEDIDA)
    estadoMateria = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class Proveedores (models.Model):
    nombre = models.CharField(max_length=50)
    contacto = models.CharField(max_length=12)
    def __str__(self):
        return self.nombre

    
class Productos(models.Model):
    nombre = models.CharField(max_length=60)
    cantidad = models.IntegerField()
    composicion = models.ManyToManyField('MateriaPrima', through='ProductoMateria',related_name='productos')
    estadoProducto = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class ProductoMateria(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    materia = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)
    cantidad_usada = models.FloatField(default=1)

class Usuario (models.Model):
    nombre= models.CharField(max_length=60)
    contraseña = models.CharField(max_length=10)
    rol = models.CharField(max_length=30)
    estadoUsuario = models.CharField(max_length=25) #Lo arregle para que funcioné de mejor manera el estado y no tener que investigar más de la cuenta

class Compra(models.Model):
    fecha = models.DateField()
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    lote = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.FloatField()
    materia = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Compra {self.id} - {self.materia.nombre}"
    

class Bodeguero (models.Model):
    nombre = models.CharField(max_length=50)
    contacto = models.CharField(max_length=16) 
    def __str__(self):
        return self.nombre