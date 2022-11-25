from statistics import mode
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from API_Opens.models import Cliente, Abogado, Solicitud

class registrarForm(UserCreationForm):
    class Meta:
        model= User
        fields= ['username','password1','password2']
        help_texts = {k:""for k in fields}

class agregarcliFrom(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_cliente','apellido_cliente','fono_cliente','direccion_cliente']

class agregaraboFrom(forms.ModelForm):
    class Meta:
        model = Abogado
        fields = ['nombre_abogado','apellido_abogado','fono_abogado','direccion_abogado','email_abogado']

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['descripcion']
