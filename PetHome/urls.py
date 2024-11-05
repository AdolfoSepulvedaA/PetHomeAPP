"""
URL configuration for PetHome project.

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
from PetHomeAPP.views import home, lista_animales, solicitar_adopcion, login_view, registrar_animal
from PetHomeAPP.views import register_view, admin_view, logout_view, gestionar_solicitudes, aceptar_solicitud
from PetHomeAPP.views import rechazar_solicitud, mis_solicitudes, recuperar_contrasena, exito_solicitud, historial_solicitudes


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Página de inicio
    path('registro_usuario/', register_view, name='registro_usuario'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin_view, name='admin_view'),
    path('registrar-animal/', registrar_animal, name='registrar_animal'),
    path('animales/', lista_animales, name='lista_animales'),  
    path('solicitar_adopcion/<int:animal_id>/', solicitar_adopcion, name='solicitar_adopcion'),
    path('gestionar_solicitudes/', gestionar_solicitudes, name='gestionar_solicitudes'),
    path('aceptar_solicitud/<int:id>/', aceptar_solicitud, name='aceptar_solicitud'),
    path('rechazar_solicitud/<int:id>/', rechazar_solicitud, name='rechazar_solicitud'),
    path('mis_solicitudes/', mis_solicitudes, name='mis_solicitudes'),
    path('recuperar_contrasena/', recuperar_contrasena, name='recuperar_contrasena'),
    path('exito_solicitud/', exito_solicitud, name='exito_solicitud'),
    path('historial_solicitudes/', historial_solicitudes, name='historial_solicitudes'),
]


