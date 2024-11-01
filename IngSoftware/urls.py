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
    path('materiaVer/',views.materiaVer),
    path('materiaCrear/',views.materiaCrear),
    path('materiaActualizar/',views.materiaActualizar),
    path('productosVer/',views.productosVer),
    path('productosCrear/',views.productosCrear),
    path('proveedoresVer/', views.proveedoresVer),
    path('proveedoresCrear/', views.proveedoresCrear),
    path('proveedoresActualizar', views.proveedoresActualizar),
    path('proveedoresDeshabilitar/', views.proveedoresDeshabilitar)
    
]
