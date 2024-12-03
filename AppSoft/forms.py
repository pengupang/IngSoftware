from django import forms 
from django.forms import inlineformset_factory
from AppSoft.models import MateriaPrima,Proveedores,Productos,Usuario,Compra, Bodeguero

class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields='__all__'
        widgets={
            'nombre' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la materia','required': 'required'}),
            'unidadMedida': forms.Select(attrs={'class': 'form-select', 'required': 'required'})
        }

class Usuariocuentaform(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'rol','contraseña', 'estadoUsuario']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre Usuario','required':'required'}),
            'rol' : forms.Select(attrs={'class':'form-control','placeholder':'Rol','required':'required'},choices={'administrador':'administrador','bodeguero':'bodeguero'}),
            'contraseña' : forms.TextInput(attrs={'class':'form-control','type':'password','placeholder':'contraseña','required':'required'}),
            'estadoUsuario' : forms.CheckboxInput(attrs={'class':'form-check-input'})
        }

    def clean_nombre(self):
        nombre= self.cleaned_data.get('nombre')
        if Usuario.objects.filter(nombre=nombre).exists():
             raise forms.ValidationError('utilize otro nombre')
        return nombre    
    
    def clean_tipo(self):
        rol = self.cleaned_data.get('rol')
        if rol not in ['administrador', 'bodeguero']:
            raise forms.ValidationError('Tipo de usuario inválido.')
        return rol       

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Proveedor'}),
            'contacto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Contacto', 'min': 100000000, 'max': 99999999999, 'pattern': r'^\d{9}$'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT', 'pattern': r'^\d{1,8}-[0-9kK]{1}$'})
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Proveedores.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError('Ya existe un proveedor con este nombre.')
        return nombre


class ProductosForm(forms.ModelForm):
    composicion = forms.ModelMultipleChoiceField(
        queryset=MateriaPrima.objects.filter(estadoMateria=True),  # Solo materias activas
        widget=forms.CheckboxSelectMultiple
    )
    cantidad = forms.IntegerField(
        min_value=1,
        label='Cantidad de Productos',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad Producto', 'required': 'required'})
    )

    class Meta:
        model = Productos
        fields = ['nombre', 'cantidad', 'composicion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Producto', 'required': 'required'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        composicion = cleaned_data.get('composicion')
        cantidad = cleaned_data.get('cantidad')

        if composicion:
            for materia in composicion:
                if materia.cantidad < cantidad:
                    raise forms.ValidationError(f"No hay suficiente stock de la materia prima: {materia.nombre}. Disponible: {materia.cantidad}.")
        return cleaned_data




class ProductoMateriaForm(forms.Form):
    materia_id = forms.IntegerField(widget=forms.HiddenInput())
    cantidad_utilizada = forms.FloatField(label="Cantidad utilizada", min_value=1)


class CantidadMateriaPrimaForm(forms.Form):
    materia_id = forms.IntegerField(widget=forms.HiddenInput())
    cantidad_utilizada = forms.FloatField(label="Cantidad utilizada", min_value=0)



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
            'lote': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Lote'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
        }

class BodegueroForm(forms.ModelForm):
    class Meta:
        model = Bodeguero
        fields='__all__'
        widgets = {
            'nombre' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Bodeguero'}),
            'contacto' : forms.TextInput(attrs= {'class':'form-control','placeholder' : 'Contacto' })

        }