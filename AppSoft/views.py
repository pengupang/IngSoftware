from django.shortcuts import render,redirect,get_object_or_404
from AppSoft.models import MateriaPrima,Productos,Proveedores,Compra, Usuario, Bodeguero, ProductoMateria
from django.contrib import messages
from . import forms
from .forms import MateriaPrimaForm,ProductosForm,ProveedoresForm,CompraForm, Usuariocuentaform, BodegueroForm

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
                return redirect('../nuevosProducto')  # Redirigir a la URL 'administrador'
            elif usuario.rol.lower()=='bodeguero':
                return redirect('../materiaVerBodeguero')#lo mismo pero para el bodeguero
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
def productosVer(request):
    productos = Productos.objects.filter(estadoProducto=True).prefetch_related('productomateria_set__materia')
    data = {'productos': productos, 'titulo': 'Tabla Productos'}
    return render(request, 'productosVer.html', data)


def productosVerDeshabilitados (request):
    productos=Productos.objects.filter(estadoProducto=False)
    data = {'productos' : productos, 'titulo':'Tabla Productos'}
    return render (request,'productosDeshabilitados.html',data)


def productosCrearNuevo(request):
    form = ProductosForm()
    materias_primas = MateriaPrima.objects.all()  # Obtenemos todas las materias primas

    if request.method == 'POST':
        form = ProductosForm(request.POST)
        if form.is_valid():
            # Crear el producto con la cantidad especificada
            nuevo_producto = form.save(commit=False)
            nuevo_producto.estadoProducto = True
            nuevo_producto.save()

            # Obtener las materias primas seleccionadas
            materias_seleccionadas = request.POST.getlist('composicion')

            for materia_id in materias_seleccionadas:
                materia = get_object_or_404(MateriaPrima, id=materia_id)

                # Obtener la cantidad utilizada de la materia prima seleccionada
                cantidad_utilizada = float(request.POST.get(f'cantidad_utilizada_{materia_id}', 0))

                if cantidad_utilizada > 0:
                    # Crear la relación ProductoMateria
                    ProductoMateria.objects.create(
                        producto=nuevo_producto,
                        materia=materia,
                        cantidad_utilizada=cantidad_utilizada
                    )

                    # Restar la cantidad de materia prima utilizada
                    if materia.cantidad >= cantidad_utilizada:
                        materia.cantidad -= cantidad_utilizada
                        materia.save()
                    else:
                        # Si no hay suficiente cantidad, mostrar un error
                        messages.error(request, f"Inventario insuficiente para {materia.nombre}")
                        
            return redirect('../productosVer/')  # Redirigir a la vista que lista los productos

    data = {
        'form': form,
        'materias_primas': materias_primas,
        'titulo': 'Agregar Producto'
    }
    return render(request, 'productosNuevos.html', data)



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

def productosActualizar(request, id):
    producto = get_object_or_404(Productos, id=id)
    titulo = "Actualizar Producto"

    if request.method == 'POST':
        cantidad_agregar = int(request.POST.get('cantidad', 0))
        producto.cantidad += cantidad_agregar
        producto.save()

        for composicion in producto.productomateria_set.all():
            materia_id = composicion.materia.id
            nueva_cantidad_utilizada = float(request.POST.get(f'cantidad_utilizada_{materia_id}', 0))
            diferencia_cantidad = nueva_cantidad_utilizada - composicion.cantidad_utilizada
            
            # Actualizar la cantidad de materia prima en el inventario
            if composicion.materia.cantidad >= diferencia_cantidad:
                composicion.materia.cantidad -= diferencia_cantidad
                composicion.materia.save()

                # Actualizar la cantidad utilizada en la relación ProductoMateria
                composicion.cantidad_utilizada = nueva_cantidad_utilizada
                composicion.save()
            else:
                messages.error(request, f"Inventario insuficiente para {composicion.materia.nombre}")
                

        return redirect('productosVer')

    data = {
        'titulo': titulo,
        'producto': producto
    }
    return render(request, 'agregarCantidadProducto.html', data)




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

def delete_usuario(request, id):
    usuario = Usuario.objects.get(id=id)
    if usuario:
        usuario.estadoUsuario = 'False'
        usuario.save()
    return redirect('login')

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
    data = {'compras' : compras, 'titulo':'Tabla Ingresos Materia Prima'}
    return render (request,'compras_ver.html',data)




def bodeguerosVer(request):
    bodeguero=Bodeguero.objects.all()
    data = {'boguederos' : bodeguero, 'titulo':'Tabla Boguederos'}
    return render (request,'BodegueroVer.html',data)

def bodegueroCrear(request):
    form = BodegueroForm()
    if request.method == 'POST':
        form = BodegueroForm(request.POST)
        if form.is_valid():
            form.save()
    data = {'form' : form , 'titulo': 'Agregar Bodeguero'}
    return render (request,'bodegueroCrear.html',data)
