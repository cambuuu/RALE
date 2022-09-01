from django.db import models

# Create your models here.

class Abogado(models.Model):
	nombre = models.CharField(max_length = 20, default = '')
	apellido = models.CharField(max_length = 20, default = '')
	fono = models.CharField(max_length = 10, default = '')
	
	class Meta:
		db_table = 'Abogado'

	def __str__(self):
		return self.nombre
