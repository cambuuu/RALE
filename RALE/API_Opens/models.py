from django.db import models
from django.conf import settings
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
	id_email = models.ForeignKey('Email' , on_delete = models.SET_NULL, null = True)
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

	class Meta:
		db_table = 'Cliente'

	def __str__(self):
		return self.nombre_cliente

class Bitacora_usuario(models.Model):
	fecha = models.DateField()
	hora = models.DateTimeField()
	detalle_bitacora = models.CharField(max_length = 200)

	class Meta:
		db_table = 'Bitacora_usuario'

	def __str__(self):
		return self.fecha

class Abogado(models.Model):
	nombre_abogado = models.CharField(max_length = 200)
	apellido_abogado = models.CharField(max_length = 200)
	fono_abogado = models.CharField(max_length = 200)
	direccion_abogado = models.CharField(max_length = 200)
	email_abogado = models.CharField(max_length = 200)
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

	class Meta:
		db_table = 'Abogado'

	def __str__(self):
		return self.nombre_abogado

class Solicitud(models.Model):
	descripcion= models.CharField(max_length = 200)
	fecha =  models.DateTimeField()
	prediccion = models.CharField(max_length = 200)
	id_email = models.ForeignKey('Email' , on_delete = models.SET_NULL, null = True)
	id_abogado = models.ForeignKey('Abogado' , on_delete = models.SET_NULL, null = True)

	class Meta:
		db_table = 'Solicitud'

	def __str__(self):
		return self.descripcion

class Documento(models.Model):
	fecha_documento = models.DateField()
	solicitud = models.ForeignKey('Solicitud' , on_delete = models.SET_NULL, null = True)

	class Meta:
		db_table = 'Documento'

	def __str__(self):
		return self.fecha_documento

class Bitacora_solicitud(models.Model):
	fecha_solicitud = models.DateField()
	hora_solicitud = models.DateTimeField()
	detalle_solicitud = models.CharField(max_length = 200)
	estado_solicitud = models.CharField(max_length = 200)
	id_solicitud = models.ForeignKey('Solicitud' , on_delete = models.SET_NULL, null = True)

	class Meta:
		db_table = 'Bitacora_solicitud'

	def __str__(self):
		return self.estado_solicitud
