from django.contrib import admin

# Register your models here.
# PetHomeAPP/admin.py

from .models import Animal, Usuario, SolicitudAdopcion

admin.site.register(Animal)
admin.site.register(Usuario)
admin.site.register(SolicitudAdopcion)
