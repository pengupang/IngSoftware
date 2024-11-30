"""
URL configuration for IngSoftware project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppSoft import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('registro/', views.crearcuenta, name='register'),
    path('comprasVer/',views.compras_Ver,name= 'comprasVer'),
    path('comprasAgregar/<str:nombre>',views.compra_agregar,name='comprasAgregar'),
    
    
    path('materiaVer/',views.materiaVer, name='materiaVer'),
    path('materiaCrear/',views.materiaCrear,name='materiaCrear'),
    path('materiaActualizar/<int:id>',views.materiaActualizar,name='materiaActualizar'),
    path('materiaDeshabilitar/<int:id>',views.materiaDeshabilitar,name='materiaDeshabilitar'),
    path('materiasDeshabilitadas/',views.materiasDeshabilitadas,name='materiasDeshabilitadas'),
    path('materiasHabilitar/<int:id>',views.materiaHabilitar,name='materiasHabilitar'),
    
    

    
    path('productosVer/', views.productosVer, name='productosVer'), 
    path('nuevosProducto/', views.productosCrearNuevo,name='productosCrearNuevo'),
    path('productosActualizar/<int:id>', views.productosActualizar,name='productosActualizar'),
    path('productosDeshabilitar/<int:id>', views.productosDeshabilitar,name='productosDeshabilitar'),
    path('productosDeshabilitados/',views.productosVerDeshabilitados,name='productosDeshabilitados'),
    path('productosHabilitar/<int:id>',views.productosHabilitar,name='productosHabilitar'),
   
   
    path('proveedoresVer/', views.proveedoresVer, name='proveedoresVer'),
    path('proveedoresCrear/', views.proveedoresCrear, name='proveedoresCrear'),
    path('proveedoresActualizar/<int:id>', views.proveedoresActualizar, name='proveedoresActualizar'),
    path('proveedoresDeshabilitar/<int:id>',views.proveedoresDeshabilitar, name='proveedoresDeshabilitar'),
    path('proveedoresDeshabilitados/',views.proveedoresDeshabilitados, name='proveedoresDeshabilitados'),
    path('proveedoresHabilitar/<int:id>',views.proveedoresHabilitar, name='proveedoresHabilitar'),
    path('delete_proveedores/<int:id>/', views.delete_proveedores, name='delete_proveedores'),
    
    
    path('lista_usuarios/', views.lista_usuarios,name='lista_usuarios'),
    path('crear_usuario/', views.crear_usuario,name='crear_usuario'),
    path('actualizar_usuario/<int:id>', views.actualizar_usuario,name='actualizar_usuario'),
    path('delete-usuario/<int:emp_id>/', views.delete_usuario, name='delete_usuario'),
    
    
    path('bodegueroVer/',views.bodeguerosVer,name='bodeguerosVer'),
    path('bodegueroCrear/',views.bodegueroCrear, name='bodegueroCrear'),
    path('materiaCrearBodeguero/', views.materiaCrearBodeguero, name='materiaCrearBodeguero'),
    path('materiaVerBodeguero/', views.materiaVerBodeguero, name='materiaVerBodeguero'),
    path('compras_bodeguero/<str:nombre>',views.compra_agregarBodeguero,name='agregarCompraBodeguero'),
    path('productos_bodeguero',views.productosVerBodeguero, name='verProductosBodeguero'),
    path('proveedores_bodeguero/',views.proveedoresVerBodeguero,name='verProveedoresBodeguero'),
    
    
]
