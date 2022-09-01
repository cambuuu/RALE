from django.shortcuts import render
from rest_framework import serializers,viewsets
from django.contrib.auth.models import User,Group
from .models import *
from .serializers import *

# Create your views here.

# Serializers para las tablas

class AbogadoViewSet(viewsets.ModelViewSet):
	queryset = Abogado.objects.all()
	serializer_class = AbogadoSerializers

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializers

class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializers
