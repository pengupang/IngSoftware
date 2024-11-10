from django import forms 
from AppSoft.models import MateriaPrima,Proveedores,Productos,Usuario,Compra

class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields='__all__'

class Usuariocuentaform(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'rol','contraseña', 'estadoUsuario']

    def clean_nombre(self):
        nombre= self.cleaned_data.get('nombre')
        if Usuario.objects.filter(nombre=nombre).exists():
             raise forms.ValidationError('utilize otro nombre')
        return nombre    
    
    def clean_tipo(self):
        rol = self.cleaned_data.get('tipo')
        if rol not in ['administrador', 'bodeguero']:
            raise forms.ValidationError('Tipo de usuario inválido.')
        return rol       

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields='__all__'
        widgets = {
            'nombre' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Proveedor'}),
            'contacto' : forms.TextInput(attrs= {'class':'form-control','placeholder' : 'Contacto' })

        }


class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields='__all__'
        widgets = {
            'nombre' : forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad' : forms.TextInput(attrs={'class': 'form-control'}),
            'estadoProducto' : forms.TextInput(attrs={'class': 'form-control'}),
                                       
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields='__all__'

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['fecha', 'proveedor', 'lote', 'cantidad']  # Excluir 'materia' para no mostrarlo

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'lote': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad', 'min': 1}),
        }