from django.contrib import admin
from .models import Email,Plantilla,Abogado,Solicitud,Documento,Cliente,Bitacora

# Register your models here.

admin.site.register(Email)
admin.site.register(Plantilla)
admin.site.register(Abogado)
admin.site.register(Solicitud)
admin.site.register(Documento)
admin.site.register(Cliente)
admin.site.register(Bitacora)

