from django.urls import path
from . import views

urlpatterns = [
	path('abogado/',views.Detalle_abogado, name = "lista_abogado"),
	path('email/',views.Detalle_email, name = "lista_email"),
	path('bitacoras/',views.Detalle_bitacora_solicitud, name = "bitacora_solicitud"),
	path('bitacorau/',views.Detalle_bitacora_usuario, name = "bitacora_usuario"),
]
