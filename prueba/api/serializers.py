from rest_framework import serializers
from django.contrib.auth.models import User,Group
from .models import *

class AbogadoSerializers(serializers.ModelSerializer):
	class Meta:
		model = Abogado
		fields = '__all__'

class UserSerializers(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

class GroupSerializers(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = '__all__'
