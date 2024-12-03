from django.shortcuts import render,redirect,get_object_or_404
from AppSoft.models import MateriaPrima,Productos,Proveedores,Compra, Usuario, Bodeguero, ProductoMateria
from .validators import validar_rut_mod11
from django.core.exceptions import ValidationError
from django.contrib import messages
from . import forms
from django.db.models import Q
from datetime import datetime
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
    busqueda = request.GET.get('datosMatAd','')
    if busqueda :
        materia = MateriaPrima.objects.filter(
            Q(nombre__icontains=busqueda) & 
            Q(estadoMateria=True)
        )
    data = {'materia' : materia, 'titulo':'Tabla Materia Prima'}
    return render (request,'materiaVer.html',data)

def materiaVerBodeguero (request):
    materia=MateriaPrima.objects.filter(estadoMateria=True)
    busqueda = request.GET.get('matBodeguero','')
    if busqueda :
        materia = MateriaPrima.objects.filter(
            Q(nombre__icontains=busqueda) & 
            Q(estadoMateria=True)
        )
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
    busqueda = request.GET.get('productoVer','')
    if busqueda :
        productos = Productos.objects.filter(
            Q(nombre__icontains=busqueda) |
            Q(composicion__nombre__contains = busqueda) & 
            Q(estadoProducto=True)
            
        )
    data = {'productos': productos, 'titulo': 'Tabla Productos'}
    return render(request, 'productosVer.html', data)


def productosVerDeshabilitados (request):
    productos=Productos.objects.filter(estadoProducto=False)
    data = {'productos' : productos, 'titulo':'Tabla Productos'}
    return render (request,'productosDeshabilitados.html',data)


def productosCrearNuevo(request):
    form = ProductosForm()
    # Solo mostrar materias primas activas
    materias_primas = MateriaPrima.objects.filter(estadoMateria=True)

    if request.method == 'POST':
        form = ProductosForm(request.POST)
        if form.is_valid():
            nuevo_producto = form.save(commit=False)
            nuevo_producto.estadoProducto = True

            materias_seleccionadas = request.POST.getlist('composicion')
            materias_insuficientes = []

            for materia_id in materias_seleccionadas:
                materia = get_object_or_404(MateriaPrima, id=materia_id)

                cantidad_utilizada = float(request.POST.get(f'cantidad_utilizada_{materia_id}', 0))

                if cantidad_utilizada <= 0:
                    messages.error(request, f"La cantidad utilizada para {materia.nombre} debe ser mayor a 0.")
                    return render(request, 'productosNuevos.html', {'form': form, 'materias_primas': materias_primas, 'titulo': 'Agregar Producto'})

                if materia.cantidad < cantidad_utilizada:
                    materias_insuficientes.append(f"{materia.nombre} (Disponible: {materia.cantidad}, Necesaria: {cantidad_utilizada})")


            if materias_insuficientes:
                messages.error(request, f"Stock insuficiente para: {', '.join(materias_insuficientes)}")
                return render(request, 'productosNuevos.html', {'form': form, 'materias_primas': materias_primas, 'titulo': 'Agregar Producto'})

            nuevo_producto.save()
            for materia_id in materias_seleccionadas:
                materia = get_object_or_404(MateriaPrima, id=materia_id)
                cantidad_utilizada = float(request.POST.get(f'cantidad_utilizada_{materia_id}', 0))

                ProductoMateria.objects.create(
                    producto=nuevo_producto,
                    materia=materia,
                    cantidad_utilizada=cantidad_utilizada
                )

                materia.cantidad -= cantidad_utilizada
                materia.save()

            messages.success(request, 'Producto creado exitosamente.')
            return redirect('../productosVer/')  

    data = {
        'form': form,
        'materias_primas': materias_primas,
        'titulo': 'Agregar Producto'
    }
    return render(request, 'productosNuevos.html', data)



def productosVerBodeguero(request):
    productos=Productos.objects.filter(estadoProducto=True)
    busqueda = request.GET.get('produBode','')
    if busqueda :
        productos = Productos.objects.filter(
            Q(nombre__icontains=busqueda)  & 
            Q(estadoProducto=True)
            
        )
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
    proveedores=Proveedores.objects.filter(estado=True)
    busqueda = request.GET.get('proVer','')
    if busqueda :
        proveedores = Proveedores.objects.filter(
            Q(rut__icontains=busqueda) |
            Q(nombre__icontains=busqueda) & 
            Q(estado=True)
        )
    data = {'proveedores' : proveedores, 'titulo':'Tabla Proveedores'}
    return render (request,'proveedoresVer.html',data)

def proveedoresVerBodeguero(request):
    proveedores=Proveedores.objects.all()
    busqueda = request.GET.get('provBodeguero','')
    if busqueda :
        proveedores = Proveedores.objects.filter(
            Q(nombre__icontains=busqueda) & 
            Q(estado=True)
        )
    data = {'proveedores' : proveedores, 'titulo':'Tabla Proveedores'}
    return render (request,'proveedores_bodeguero.html',data)

def proveedoresCrear(request):
    if request.method == 'POST':
        form = ProveedoresForm(request.POST)
        if form.is_valid():
            nueva_proveedor = form.save(commit=False)
            nueva_proveedor.estado = True
            nueva_proveedor.save()
            messages.success(request, 'Proveedor creado exitosamente.')
            return redirect('proveedoresVer')  # Asegúrate de que esta URL esté definida correctamente
        else:
            # Agregar esto para ver los errores
            print(form.errors)
            messages.error(request, 'Hubo un error al crear el proveedor. Verifique los datos ingresados.')

    else:
        form = ProveedoresForm()

    data = {'form': form, 'titulo': 'Agregar Proveedor'}
    return render(request, 'proveedoresCrear.html', data)


def proveedoresActualizar(request,id):
    proveedor = Proveedores.objects.get(id=id)
    form= ProveedoresForm(instance=proveedor)
    if request.method == "POST": 
        form=ProveedoresForm(request.POST,instance=proveedor)
        if form.is_valid():
            nueva_proveedor = form.save(commit=False)
            nueva_proveedor.estado = True
            nueva_proveedor.save()
            messages.success(request, 'Actualización éxitosa.')
            return redirect('../proveedoresVer')
    data={'form':form , 'titulo': 'Actualizar Proveedores'}
    return render(request,'proveedoresCrear.html',data)

def proveedoresDeshabilitar(request,id):
     proveedores=Proveedores.objects.get(id=id)
     proveedores.estado = False
     proveedores.save()
     messages.success(request, 'Proveedor deshabilitado con éxito.')
     return redirect('../proveedoresVer')

def proveedoresDeshabilitados(request):
    proveedores=Proveedores.objects.filter(estado=False)
    data = {'proveedores' : proveedores, 'titulo':'Tabla Proveedores'}
    return render (request,'proveedoresDeshabilitar.html',data)

def proveedoresHabilitar(request,id):
    proveedor=Proveedores.objects.get(id=id)
    proveedor.estado = True
    proveedor.save()
    messages.success(request, 'Proveedor Habilitado con éxito.')
    return redirect('../proveedoresDeshabilitados')


def delete_proveedores(id):
    proveedor = Proveedores.objects.get(id=id)
    if proveedor:
        proveedor.estado = 'False'
        proveedor.save()
    return redirect('proveedoresVer')

"""
Aqui van las views de Usuarios
"""
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    busqueda = request.GET.get('usuarioVer','')
    if busqueda :
        usuarios = Usuario.objects.filter(
            Q(nombre__icontains=busqueda) 
        )
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

def delete_usuario(request, emp_id):
    usuario = Usuario.objects.get(id=emp_id)
    if usuario:
        usuario.estadoUsuario = False
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
            materia.cantidad = total_compras
            materia.save()
            messages.success(request, 'Ingreso éxitoso.')
            return redirect('../../materiaVer/')
        else:
            messages.error(request, "Ingreso Fallido")
            print("Formulario no válido:", form.errors)
    else:
        form = CompraForm()

        # Filtrar proveedores activos en la vista
        form.fields['proveedor'].queryset = Proveedores.objects.filter(estado=True)

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
        form.fields['proveedor'].queryset = Proveedores.objects.filter(estado=True)

    context = {
        'form': form,
        'titulo': 'Agregar Compra',
        'next_id': Compra.objects.count() + 1,  
        'nomMateria': materia,  
    }
    return render(request, 'compras_bodeguero.html', context)


def compras_Ver (request):
    compras=Compra.objects.all()
    fecha_inicio = request.GET.get('fecha_inicio','')
    fecha_fin = request.GET.get('fecha_fin','')
    if fecha_inicio and fecha_fin:  
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            compras = Compra.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
    data = {'compras' : compras, 'titulo':'Tabla Ingresos Materia Prima'}
    return render (request,'compras_ver.html',data)




def bodeguerosVer(request):
    bodeguero=Bodeguero.objects.all()
    busqueda = request.GET.get('datosBodeguero','')
    if busqueda :
        bodeguero = Bodeguero.objects.filter(
            Q(nombre__icontains=busqueda) 
        )
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
