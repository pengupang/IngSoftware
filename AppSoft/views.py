from django.shortcuts import render,redirect,get_object_or_404
from AppSoft.models import MateriaPrima,Productos,Proveedores,Compra, Usuario, Bodeguero, ProductoMateria
from django.contrib import messages
from . import forms
from .forms import MateriaPrimaForm,ProductosForm,ProveedoresForm,CompraForm, Usuariocuentaform, BodegueroForm,ProductoMateriaFormSet

def crearcuenta(request):
    if request.method == 'POST':
        form = Usuariocuentaform(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.estadoUsuario='True'
            form.save()
            messages.success(request, 'Cuenta creada con éxito.')
            return redirect('login')  # Redirigir al login después de crear la cuenta
    else:
        form = Usuariocuentaform()
    data = {'form': form, 'titulo': 'Crear cuenta'}
    return render(request, 'register.html', data)

def login(request):
    if request.method == 'POST':
        nombre = request.POST.get('username')
        contraseña = request.POST.get('contraseña')  # Agregamos el campo fono
        usuario = Usuario.objects.filter(nombre=nombre, contraseña=contraseña).first()  # Usamos filter() y first()
        if usuario and usuario.estadoUsuario == 'True':
            request.session['usuario_id'] = usuario.id  # Redirigir a la URL 'usuario'
            if usuario.rol.lower() == 'administrador':
                return redirect('productosCrear')  # Redirigir a la URL 'administrador'
            elif usuario.rol.lower()=='bodeguero':
                return redirect('materiaVerBodeguero')#lo mismo pero para el bodeguero
        else:
            return render(request, 'login.html', {'error': 'Usuario inválido'})
    return render(request, 'login.html')

"""
Aqui van las views de Materia Prima
"""

def materiaVer (request):
    materia=MateriaPrima.objects.filter(estadoMateria=True)
    data = {'materia' : materia, 'titulo':'Tabla Materia Prima'}
    return render (request,'materiaVer.html',data)

def materiaVerBodeguero (request):
    materia=MateriaPrima.objects.filter(estadoMateria=True)
    data = {'materia' : materia, 'titulo':'Tabla Materia Prima'}
    return render (request,'materia_bodeguero.html',data)

def materiaCrear(request):
    form = MateriaPrimaForm()
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST)
        if form.is_valid():
            nombre_materia = form.cleaned_data.get('nombre')
            if MateriaPrima.objects.filter(nombre=nombre_materia).exists():
                messages.error(request, "Materia ya existente")

            else:
                nueva_materia = form.save(commit=False)
                nueva_materia.estadoMateria = True
                nueva_materia.cantidad = 0
                nueva_materia.save()
                messages.success(request, 'Materia creada con éxito.')
                return redirect('../materiaVer/')
    data = {'form' : form , 'titulo': 'Agregar Materia Prima'}
    return render (request,'materiaCrear.html',data)

def materiaCrearBodeguero(request):
    form = MateriaPrimaForm()
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST)
        if form.is_valid():
            nombre_materia = form.cleaned_data.get('nombre')
            if MateriaPrima.objects.filter(nombre=nombre_materia).exists():
                messages.error(request, "Materia ya existente")
                print("La materia prima ya existe en la base de datos.")
            else:
                nueva_materia = form.save(commit=False)
                nueva_materia.estadoMateria = True
                nueva_materia.cantidad = 0
                nueva_materia.save()
                messages.success(request, 'Materia creada con éxito.')
                print("Materia prima creada con éxito.")
                return redirect('../materiaVerBodeguero/')
        else:
            print("Errores en el formulario:", form.errors)
                
    data = {'form': form, 'titulo': 'Agregar Materia Prima'}
    return render(request, 'materiaCrear-bodeguero.html', data)

def materiaActualizar(request,id):
    materia = MateriaPrima.objects.get(id=id)
    form= MateriaPrimaForm(instance=materia)
    if request.method == "POST": 
        form=MateriaPrimaForm(request.POST,instance=materia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Materia Actualizada con éxito.')
            return redirect('../materiaVer/')
        else:
            messages.error(request, " Ocurrio un error al actualizar la materia")
    data={'form':form , 'titulo': 'Actualizar Materia Prima'}
    return render(request,'materiaCrear.html',data)

def materiaDeshabilitar(request,id):
     materia=MateriaPrima.objects.get(id=id)
     materia.estadoMateria = False
     materia.save()
     messages.success(request, 'Materia Deshabilitada con éxito.')
     return redirect('../materiaVer')

def materiasDeshabilitadas(request):
    materia=MateriaPrima.objects.filter(estadoMateria=False)
    data = {'materia' : materia, 'titulo':'Tabla Materia Prima'}
    return render (request,'materiaDeshabilitadas.html',data)

def materiaHabilitar(request,id):
    materia=MateriaPrima.objects.get(id=id)
    materia.estadoMateria = True
    materia.save()
    messages.success(request, 'Materia Habilitada con éxito.')
    return redirect('../materiasDeshabilitadas')

"""
Aqui van las views de Productos
"""
def productosVer (request):
    productos=Productos.objects.filter(estadoProducto=True)
    data = {'productos' : productos, 'titulo':'Tabla Productos'}
    return render (request,'productosVer.html',data)

def productosVerDeshabilitados (request):
    productos=Productos.objects.filter(estadoProducto=False)
    data = {'productos' : productos, 'titulo':'Tabla Productos'}
    return render (request,'productosDeshabilitados.html',data)


def productosCrear(request):
    # Inicializar form y formset
    form = ProductosForm()
    formset = ProductoMateriaFormSet()

    if request.method == 'POST':
        form = ProductosForm(request.POST)
        formset = ProductoMateriaFormSet(request.POST)

        # Validar los formularios
        if form.is_valid() and formset.is_valid():
            producto = form.save()  # Guardar el producto

            # Procesar los formularios de la relación Producto-Materia Prima
            for producto_materia_form in formset:
                if producto_materia_form.is_valid():
                    producto_materia = producto_materia_form.save(commit=False)
                    producto_materia.producto = producto  # Asignar el producto

                    # Asegurarse de que cantidad_usada es válida
                    if producto_materia.cantidad_usada <= 0:
                        formset.add_error(None, "La cantidad usada debe ser mayor que 0.")
                        return render(request, 'productosCrear.html', {'form': form, 'formset': formset, 'titulo': 'Agregar Producto'})

                    producto_materia.save()  # Guardar la relación Producto-Materia Prima

                    # Actualizar la cantidad de materia prima
                    materia_prima = producto_materia.materia
                    if materia_prima.cantidad >= producto_materia.cantidad_usada:
                        materia_prima.cantidad -= producto_materia.cantidad_usada
                        materia_prima.save()
                    else:
                        formset.add_error(None, f"No hay suficiente {materia_prima.nombre} en inventario.")
                        return render(request, 'productosCrear.html', {'form': form, 'formset': formset, 'titulo': 'Agregar Producto'})

            return redirect('../productosVer/')
        else:
            # Si los formularios no son válidos, mostrar los errores
            return render(request, 'productosCrear.html', {'form': form, 'formset': formset, 'titulo': 'Agregar Producto'})
    
    # Si es una solicitud GET, inicializamos los formularios
    return render(request, 'productosCrear.html', {'form': form, 'formset': formset, 'titulo': 'Agregar Producto'})

def productosVerBodeguero(request):
    productos=Productos.objects.filter(estadoProducto=True)
    data = {'productos' : productos, 'titulo':'Tabla Productos'}
    return render (request,'productos_bodeguero.html',data)

def productosDeshabilitar(request,id):
     producto=Productos.objects.get(id=id)
     producto.estadoProducto = False
     producto.save()
     messages.success(request, 'Producto Deshabilitado con éxito.')
     return redirect('../productosVer')

def productosHabilitar(request,id):
    producto=Productos.objects.get(id=id)
    producto.estadoProducto = True
    producto.save()
    messages.success(request, 'Producto Habilitado con éxito.')
    return redirect('../productosDeshabilitados')

def productosActualizar(request,id):
    producto = Productos.objects.get(id=id)
    form= ProductosForm(instance=producto)
    if request.method == "POST": 
        form=ProductosForm(request.POST,instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado de forma éxitosa.')

    data={'form':form , 'titulo': 'Actualizar Producto'}
    return render(request,'productosCrear.html',data)


"""
Aqui van las views de Proveedores
"""
def proveedoresVer(request):
    proveedores=Proveedores.objects.all()
    data = {'proveedores' : proveedores, 'titulo':'Tabla Proveedores'}
    return render (request,'proveedoresVer.html',data)

def proveedoresVerBodeguero(request):
    proveedores=Proveedores.objects.all()
    data = {'proveedores' : proveedores, 'titulo':'Tabla Proveedores'}
    return render (request,'proveedores_bodeguero.html',data)

def proveedoresCrear(request):
    form = ProveedoresForm()
    if request.method == 'POST':
        form = ProveedoresForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingreso éxitoso.')
            return redirect('../proveedoresVer')
    data = {'form' : form , 'titulo': 'Agregar Proveedores'}
    return render (request,'proveedoresCrear.html',data)

def proveedoresActualizar(request,id):
    proveedor = Proveedores.objects.get(id=id)
    form= ProveedoresForm(instance=proveedor)
    if request.method == "POST": 
        form=ProveedoresForm(request.POST,instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actualización éxitosa.')
            return redirect('../proveedoresVer')
    data={'form':form , 'titulo': 'Actualizar Proveedores'}
    return render(request,'proveedoresCrear.html',data)

def proveedoresDeshabilitar(request,id):
     proveedores=Proveedores.objects.get(id=id)
     if request.method=="POST":
       proveedores.delete()
     data={"proveedores":proveedores}
     return render(request,'proveedoresCrear.html',data)

"""
Aqui van las views de Usuarios
"""
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    data = {'usuarios' : usuarios, 'titulo':'Tabla Usuarios'}
    return render(request, 'usuarios_ver.html',data)

def crear_usuario(request):
    form = Usuariocuentaform()
    if request.method == 'POST':
        form = Usuariocuentaform(request.POST)
        if form.is_valid():
            form.save()
    data = {'form' : form , 'titulo': 'Agregar Usuario'}
    return render(request, 'usuario_crear.html',data)

def actualizar_usuario(request, id):
    usuarios = Usuario.objects.get(id=id)
    form= Usuariocuentaform(instance=usuarios)
    if request.method == "POST": 
        form=Usuariocuentaform(request.POST,instance=usuarios)
        if form.is_valid():
            form.save()
    data={'form':form , 'titulo': 'Actualizar Usuarios'}
    return render(request,'usuario_crear.html',data)

def deshabilitar_usuario(request,id):
     usuarios=Usuario.objects.get(id=id)
     if request.method=="POST":
       usuarios.delete()
     data={"usuarios":usuarios}
     return render(request,'usuario_crear.html',data)

"""
Aqui van las views de ingresos
"""
def compra_agregar(request, nombre):
    materia = get_object_or_404(MateriaPrima, nombre=nombre)  

    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.materia = materia 
            compra.save()
            
            compras_previas = Compra.objects.filter(materia=materia)
            total_compras = sum(compra.cantidad for compra in compras_previas)
            materia.cantidad =total_compras
            materia.save()
            messages.success(request, 'Ingreso éxitoso.')
            return redirect('../../materiaVer/')
        else:
            messages.error(request, "Ingreso Fallido")
            print("Formulario no válido:", form.errors)
    else:
        form = CompraForm()

    context = {
        'form': form,
        'titulo': 'Agregar Compra',
        'next_id': Compra.objects.count() + 1,  
        'nomMateria': materia,  
    }
    return render(request, 'comprar_agregar.html', context)

def compra_agregarBodeguero(request, nombre):
    materia = get_object_or_404(MateriaPrima, nombre=nombre)  

    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.materia = materia 
            compra.save()
            
            compras_previas = Compra.objects.filter(materia=materia)
            total_compras = sum(compra.cantidad for compra in compras_previas)
            materia.cantidad =total_compras
            materia.save()
            messages.success(request, 'Ingreso éxitoso.')

            return redirect('../../materiaVerBodeguero/')
        else:
            messages.error(request, "Ingreso Fallido")

            print("Formulario no válido:", form.errors)
    else:
        form = CompraForm()

    context = {
        'form': form,
        'titulo': 'Agregar Compra',
        'next_id': Compra.objects.count() + 1,  
        'nomMateria': materia,  
    }
    return render(request, 'compras_bodeguero.html', context)


def compras_Ver (request):
    compras=Compra.objects.all()
    data = {'compras' : compras, 'titulo':'Tabla Compras'}
    return render (request,'compras_ver.html',data)




def bodeguerosVer(request):
    bodeguero=Bodeguero.objects.all()
    data = {'boguederos' : bodeguero, 'titulo':'Tabla Boguederos'}
    return render (request,'bodegueroVer.html',data)

def bodegueroCrear(request):
    form = BodegueroForm()
    if request.method == 'POST':
        form = BodegueroForm(request.POST)
        if form.is_valid():
            form.save()
    data = {'form' : form , 'titulo': 'Agregar Bodeguero'}
    return render (request,'bodegueroCrear.html',data)
