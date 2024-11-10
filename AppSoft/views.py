from django.shortcuts import render,redirect
from AppSoft.models import MateriaPrima,Productos,Proveedores,Compra, Usuario
from . import forms
from .forms import MateriaPrimaForm,ProductosForm,ProveedoresForm,CompraForm, Usuariocuentaform

def crearcuenta(request):
    if request.method == 'POST':
        form = Usuariocuentaform(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.estadoUsuario='True'
            form.save()
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
            if usuario.rol == 'administrador':
                return redirect('productosCrear')  # Redirigir a la URL 'administrador'
            elif usuario.rol=='bodeguero':
                return redirect('materiaVer')#lo mismo pero para el repartidor
        else:
            return render(request, 'login.html', {'error': 'Usuario inválido'})
    return render(request, 'login.html')

"""
Aqui van las views de Materia Prima
"""
def materiaVer (request):
    materia=MateriaPrima.objects.all()
    data = {'materia' : materia, 'titulo':'Tabla Materia Prima'}
    return render (request,'materiaVer.html',data)

def materiaCrear(request):
    form = MateriaPrimaForm()
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST)
        if form.is_valid():
            form.save()
    data = {'form' : form , 'titulo': 'Agregar Materia Prima'}
    return render (request,'materiaCrear.html',data)

def materiaActualizar(request,id):
    materia = MateriaPrima.objects.get(id=id)
    form= MateriaPrimaForm(instance=materia)
    if request.method == "POST": 
        form=MateriaPrimaForm(request.POST,instance=materia)
        if form.is_valid():
            form.save()
    data={'form':form , 'titulo': 'Actualizar Materia Prima'}
    return render(request,'materiaCrear.html',data)

"""
Aqui van las views de Productos
"""
def productosVer (request):
    productos=Productos.objects.all()
    data = {'productos' : productos, 'titulo':'Tabla Productos'}
    return render (request,'productosVer.html',data)

def productosCrear(request):
    form = ProductosForm()
    if request.method == 'POST':
        form = ProductosForm(request.POST)
        if form.is_valid():
            form.save()
    data = {'form' : form , 'titulo': 'Agregar Productos'}
    return render (request,'productosCrear.html',data)

def productosActualizar(request,id):
    producto = Productos.objects.get(id=id)
    form= ProductosForm(instance=producto)
    if request.method == "POST": 
        form=ProductosForm(request.POST,instance=producto)
        if form.is_valid():
            form.save()
    data={'form':form , 'titulo': 'Actualizar Producto'}
    return render(request,'productosCrear.html',data)
"""
Aqui van las views de Proveedores
"""
def proveedoresVer(request):
    proveedores=Proveedores.objects.all()
    data = {'proveedores' : proveedores, 'titulo':'Tabla Proveedores'}
    return render (request,'proveedoresVer.html',data)

def proveedoresCrear(request):
    form = ProveedoresForm()
    if request.method == 'POST':
        form = ProveedoresForm(request.POST)
        if form.is_valid():
            form.save()
    data = {'form' : form , 'titulo': 'Agregar Proveedores'}
    return render (request,'proveedoresCrear.html',data)

def proveedoresActualizar(request,id):
    proveedor = Proveedores.objects.get(id=id)
    form= ProveedoresForm(instance=proveedor)
    if request.method == "POST": 
        form=ProveedoresForm(request.POST,instance=proveedor)
        if form.is_valid():
            form.save()
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

"""
Aqui van las views de ingresos
"""
def compra_agregar(request):
    # sirve para marcar cual es la id siguiente al momento de renderizar el page
    last_compra = Compra.objects.order_by('id').last()
    next_id = last_compra.id + 1 if last_compra else 1

    if request.method == "POST":
        #comprobacion extra en caso de que se suban productos al mismo tiempo, si suena tonto pero pasa 
        if next_id == Compra.objects.order_by('id').last().id:
            next_id+=1
        form = CompraForm(request.POST)
        if form.is_valid():
            form.instance.orden = next_id
            form.save()
            return redirect('compras_ver')

    form = CompraForm()

    materia = MateriaPrima.objects.all()

    context = {
        'form': form,
        'titulo': 'Agregar Compra',
        'materia': materia,
        'next_id': next_id,
    }
    return render(request, 'comprar_agregar.html', context)

def compras_Ver (request):
    compras=Compra.objects.all()
    data = {'compras' : compras, 'titulo':'Tabla Compras'}
    return render (request,'compras_ver.html',data)

