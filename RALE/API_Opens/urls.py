from django.urls import path
from . import views

urlpatterns = [
	path('abogado/',views.Detalle_abogado, name = "lista_abogado"),
	path('email/',views.Detalle_email, name = "lista_email"),
]
