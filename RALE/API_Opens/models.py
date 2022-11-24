from re import A
from statistics import mode
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Email(models.Model):
	nombre = models.CharField(max_length = 200)
	fecha = models.CharField(max_length = 200)
	asunto = models.TextField()
	cuerpo = models.TextField()

	class Meta:
		db_table = 'Email'

	def __str__(self):
		return self.nombre

class Plantilla(models.Model):
	asunto_plantilla = models.TextField()
	cuerpo_plantilla = models.TextField()

	class Meta:
		db_table = 'Plantilla'

	def __str__(self):
		return self.asunto_plantilla

class Cliente(models.Model):
	nombre_cliente = models.CharField(max_length = 200)
	apellido_cliente = models.CharField(max_length = 200)
	fono_cliente = models.CharField(max_length = 200)
	direccion_cliente = models.CharField(max_length = 200)
	user= models.OneToOneField(User, on_delete= models.CASCADE)

	class Meta:
		db_table = 'Cliente'

	def __str__(self):
		return f'Cliente de {self.user.username}'

def createCliente(sender,instance, created, **kwargs,):
		if created:
			Cliente.objects.create(user=instance)
			Abogado.objects.create(user=instance)
post_save.connect(createCliente, sender=User)

class Bitacora(models.Model):
	nombretabla = models.CharField(max_length = 50)
	operacion = models.CharField(max_length = 20)
	valoranterior = models.TextField()
	nuevovalor = models.TextField()
	updatedate = models.DateTimeField(auto_now = True)
	usuario = models.CharField(max_length = 20)

	class Meta:
		db_table = 'Bitacora'

	def __str__(self):
		return self.usuario

class Abogado(models.Model):
	nombre_abogado = models.CharField(max_length = 200)
	apellido_abogado = models.CharField(max_length = 200)
	fono_abogado = models.CharField(max_length = 200)
	direccion_abogado = models.CharField(max_length = 200)
	email_abogado = models.CharField(max_length = 200)
	user = models.OneToOneField(User, on_delete= models.CASCADE)

	class Meta:
		db_table = 'Abogado'

	def __str__(self):
		return f'Abogado de {self.user.username}'


class Solicitud(models.Model):
	descripcion= models.CharField(max_length = 200)
	fecha =  models.DateTimeField(auto_now = True)
	prediccion = models.CharField(max_length = 200)
	id_email = models.ForeignKey('Email' , on_delete = models.SET_NULL, null = True)
	id_abogado = models.ForeignKey('Abogado' , on_delete = models.SET_NULL, null = True)

	class Meta:
		db_table = 'Solicitud'

	def __str__(self):
		return self.descripcion

class Documento(models.Model):
	titulo = models.CharField(max_length = 200)
	documento = models.FileField(upload_to = "Uploaded Files/")
	fecha_documento = models.DateTimeField(auto_now = True)
	user= models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		db_table = 'Documento'

	def __str__(self):
		return f'Documento de {self.user.username}'
