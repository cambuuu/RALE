from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import serializers,viewsets
from rest_framework.permissions import *
from django.contrib.auth.models import User,Group
from .models import *
from .serializers import *

# Create your views here.

# Serializers para las tablas
# Sirve para Listar y Agregar

class AbogadoViewSet(viewsets.ModelViewSet):
	queryset = Abogado.objects.all()
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class = AbogadoSerializers

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class = UserSerializers

class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class = GroupSerializers

class ClienteViewSet(viewsets.ModelViewSet):
	queryset = Cliente.objects.all()
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class = ClienteSerializers

class SolicitudViewSet(viewsets.ModelViewSet):
	queryset = Solicitud.objects.all()
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class = SolicitudSerializers

class DocumentosViewSet(viewsets.ModelViewSet):
	queryset = Documento.objects.all()
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class = DocumentoSerializers

# Eliminar

@api_view(['DELETE'])

def AbogadoEliminar(request,pk):
	abogado = Abogado.objects.get(id=pk)
	abogado.delete()

	return Response('Eliminado')

@api_view(['DELETE'])

def ClienteEliminar(request,pk):
	cliente = Cliente.objects.get(id=pk)
	cliente.delete()

	return Response('Eliminado')

@api_view(['DELETE'])

def SolicitudEliminar(request,pk):
	solicitud = Solicitud.objects.get(id=pk)
	solicitud.delete()

	return Response('Eliminado')

@api_view(['DELETE'])

def DocumentoEliminar(request,pk):
	documento = Documento.objects.get(id=pk)
	documento.delete()

	return Response('Eliminado')
