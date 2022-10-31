from rest_framework import serializers,viewsets
from django.contrib.auth.models import User,Group
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render


# Create your views here.

class ClienteViewSet(viewsets.ModelViewSet):
	queryset = Cliente.objects.all()
	serializer_class = ClienteSerializers

class PlantillaViewSet(viewsets.ModelViewSet):
	queryset = Plantilla.objects.all()
	serializer_class = PlantillaSerializers

class SolicitudViewSet(viewsets.ModelViewSet):
	queryset = Solicitud.objects.all()
	serializer_class = SolicitudSerializers

class DocumentoViewSet(viewsets.ModelViewSet):
	queryset = Documento.objects.all()
	serializer_class = DocumentoSerializers

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializers

class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializers

@api_view(['GET'])
def Detalle_bitacora_solicitud(request):
	bitacora_solicitud = Bitacora_solicitud.objects.all()
	serializer = BitacoraSolicitudSerializers(bitacora_solicitud, many = False)
	return Response(serializer.data)

@api_view(['GET'])
def Detalle_bitacora_usuario(request):
	bitacora_usuario = Bitacora_usuario.objects.all()
	serializer = BitacoraUsuarioSerializers(bitacora_usuario, many = False)
	return Response(serializer.data)

@api_view(['GET'])
def Detalle_abogado(request):
	abogado = Abogado.objects.all()
	serializer = AbogadoSerializers(abogado, many = False)
	return Response(serializer.data)

@api_view(['GET'])
def Detalle_email(request):
	email = Email.objects.all()
	serializer = EmailSerializers(email, many = False)
	return Response(serializer.data)
