from django.shortcuts import render
from AppSoft.models import MateriaPrima,Productos,Proveedores,Usuario
from . import forms
from .forms import MateriaPrimaForm,ProductosForm,ProveedoresForm,UsuarioForm

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
    form = MateriaPrimaForm()
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST)
        if form.is_valid():
            form.save()
    data = {'form' : form , 'titulo': 'Agregar Materia Prima'}
    return render (request,'productosCrear.html',data)

def productosActualizar(request,id):
    materia = MateriaPrima.objects.get(id=id)
    form= MateriaPrimaForm(instance=materia)
    if request.method == "POST": 
        form=MateriaPrimaForm(request.POST,instance=materia)
        if form.is_valid():
            form.save()
    data={'form':form , 'titulo': 'Actualizar Materia Prima'}
    return render(request,'productosCrear.html',data)
"""
Aqui van las views de Proveedores
"""

"""
Aqui van las views de Usuarios
"""
