from django.shortcuts import render,redirect,get_object_or_404
from AppSoft.models import MateriaPrima,Productos,Proveedores,Compra, Usuario, Bodeguero
from . import forms
from .forms import MateriaPrimaForm,ProductosForm,ProveedoresForm,CompraForm, Usuariocuentaform, BodegueroForm

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
        return redirect('../materiaVer/')
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
            return redirect('../productosVer/')
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
            return redirect('../../materiaVer/')
        else:
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