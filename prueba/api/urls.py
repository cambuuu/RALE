from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
	#Eliminar
	path('eliminar/abogado/<int:pk>/',views.AbogadoEliminar, name = "elimnar_abogado"),

]
