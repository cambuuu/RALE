from django.db import models

# Create your models here.

class Abogado(models.Model):
	nombre = models.CharField(max_length = 20, default = '')
	apellido = models.CharField(max_length = 20, default = '')
	fono = models.CharField(max_length = 10, default = '')
	rut = models.CharField(max_length = 15, default = '')
	direccion = models.CharField(max_length = 50, default = '')
	email = models.CharField(max_length = 30, default = '')

	class Meta:
		db_table = 'Abogado'

	def __str__(self):
		return self.nombre

class Cliente(models.Model):
	nombre_c = models.CharField(max_length = 20, default = '')
	fono_c = models.CharField(max_length = 10, default = '')
	rut_C = models.CharField(max_length = 15, default = '')
	direccion_c = models.CharField(max_length = 50, default = '')
	email_C = models.CharField(max_length = 30, default = '')

	class Meta:
		db_table = 'Cliente'

	def __str__(self):
		return self.nombre_c

class Solicitud(models.Model):
	descripcion = models.TextField(max_length = 500, default = '')
	fecha = models.DateField()
	hora = models.DateTimeField()
	prediccion = models.CharField(max_length = 20, default = '')
	plantilla = models.TextField(max_length = 500, default = '')
	abogado = models.ForeignKey(Abogado, on_delete = models.SET_NULL,null=True)
	cliente = models.ForeignKey(Cliente, on_delete = models.SET_NULL,null=True)

	class Meta:
		db_table = 'Solicitud'

	def __str__(self):
		return self.prediccion

class Documento(models.Model):
	#documento = FileField()
	fecha_documento = models.DateField()
	solicitud = models.ForeignKey(Solicitud, on_delete = models.SET_NULL,null=True)
	cliente = models.ForeignKey(Cliente, on_delete = models.SET_NULL,null=True)

	class Meta:
		db_table = 'Documento'

	def __str__(self):
		return str(self.fecha_documento)
