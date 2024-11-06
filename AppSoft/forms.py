from django import forms 
from AppSoft.models import MateriaPrima,Proveedores,Productos,Usuario,Compra

class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields='__all__'

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields='__all__'


class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields='__all__'

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields='__all__'

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields='__all__'
        