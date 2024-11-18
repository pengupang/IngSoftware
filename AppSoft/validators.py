import re
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _

# Función para calcular el dígito verificador (DV) del RUT
def calcular_dv(rut):
    suma = 0
    multiplicador = 2  # Iniciar con el multiplicador de 2

    # Iterar sobre el cuerpo del RUT (8 primeros dígitos) desde el último al primero
    for i in range(len(rut) - 1, -1, -1):
        suma += int(rut[i]) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2  # Ciclo del multiplicador: [2, 3, 4, 5, 6, 7, 2, 3, ...]

    # Calcular el resto de la suma dividida por 11
    resto = suma % 11

    # Determinar el DV según el resto
    if resto == 1:
        return "K"
    elif resto == 0:
        return "0"
    else:
        return str(11 - resto)

# Función para validar el RUT con el DV
def validar_rut_mod11(rut_completo):
    # Limpiar el RUT (eliminar puntos, guiones y convertir a mayúsculas)
    rut_completo = rut_completo.replace(".", "").replace("-", "").upper()

    print(f"RUT limpio: {rut_completo}")  # Depuración: mostrar el RUT limpio

    # Extraer el cuerpo del RUT y el dígito verificador ingresado
    cuerpo, dv_ingresado = rut_completo[:-1], rut_completo[-1]

    # Validar que el cuerpo sea numérico
    if not cuerpo.isdigit():
        raise ValueError("El RUT debe contener solo números en el cuerpo.")

    # Calcular el dígito verificador esperado
    dv_calculado = calcular_dv(cuerpo)
    print(f"Dígito verificador calculado: {dv_calculado}")  # Depuración: mostrar el DV calculado

    # Comparar el DV calculado con el ingresado
    return dv_calculado == dv_ingresado

class MinValueValidator(BaseValidator):
    message = _('Asegurese que el valor sea mayor a %(limit_value)s.')
    code = 'min_value'
    def compare(self, value, limit_value):
        return value < limit_value 