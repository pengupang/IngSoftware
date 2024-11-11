from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Productos, ProductoMateria, MateriaPrima

@receiver(m2m_changed, sender=Productos.composicion.through)
def descontar_materia_prima(sender, instance, action, **kwargs):
    if action == 'post_add':
        for producto_materia in ProductoMateria.objects.filter(producto=instance):
            materia = producto_materia.materia
            cantidad_usada = producto_materia.cantidad_usada
            
            # Descontar la cantidad usada de la materia prima
            if materia.cantidad >= cantidad_usada:
                materia.cantidad -= cantidad_usada
                materia.save()  # Asegurarse de guardar los cambios en la base de datos
            else:
                raise ValueError(f"No hay suficiente cantidad de {materia.nombre} en inventario.")