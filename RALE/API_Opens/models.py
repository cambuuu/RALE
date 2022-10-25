from django.db import models

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
