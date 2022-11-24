import re
from locale import currency
from re import A

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group, User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from .forms import agregarcliFrom, registrarForm, agregaraboFrom
from API_Opens.models import *
from API_Opens.serializers import *

# Create your views here.

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        user = request.user
        if user.groups.filter(name='cliente').exists():
            return redirect(to='ServicioWEB:hola')

        return redirect(to='ServicioWEB:ahome')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": registrarForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"],
                    password=request.POST["password1"],
                    email=request.POST['email'])
                group = Group.objects.get(name='cliente')
                user.groups.add(group)
                user.save()
                messages.success(request, "Cliente Agregado Correctamente")
                return redirect(to='ServicioWEB:ahome')
            except IntegrityError:
                return render(request, 'signup.html', {"form": registrarForm, "error": "Usuario ya existe."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Contrasenias no coinciden."})

def signup2(request):
    if request.method == 'GET':
        return render(request, 'signup2.html', {"form": registrarForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"],
                    password=request.POST["password1"],
                    # first_name=request.POST['first_name'],
                    # last_name=request.POST['last_name'],
                    email=request.POST['email'])
                group = Group.objects.get(name='abogado')
                user.groups.add(group)
                user.save()
                login(request, user)
                # user = request.user
                # if user.groups.filter(name='abogado').exists():
                #     return redirect(to='ahome')
                # else:
                #     return redirect(to='hola')
            except IntegrityError:
                return render(request, 'signup2.html', {"form": registrarForm, "error": "Usuario ya existe."})

        return render(request, 'signup2.html', {"form": UserCreationForm, "error": "Contrasenias no coinciden."})

@login_required
def signout(request):
    logout(request)
    return redirect(to='ServicioWEB:signin')

@login_required
def ahome(request):
    clientes = User.objects.filter(groups=1)
    emails = Email.objects.all()
    solicitud = Solicitud.objects.filter(prediccion = ['Despido'])
    data = {
        'clientes': clientes,
        'email': emails,
        'solicitud': solicitud,
    }
    user = request.user
    if user.groups.filter(name='cliente').exists():
            return redirect(to='ServicioWEB:hola')
    return render(request, 'ahome.html', data)


@login_required
def miperfil(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
    else:
        user = current_user
    return render(request, 'miperfil.html', {'user': user})

@login_required
def perfilcli(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
    else:
        user = current_user
    return render(request, 'perfilcli.html', {'user': user})


@login_required
def modificarcliente(request,id):
    cliente = Cliente.objects.get(user=id)
    data = {'cform':agregarcliFrom(instance=cliente)}
    if request.method == 'POST':
        cform = agregarcliFrom(data=request.POST, files=request.FILES, instance=cliente)
        if cform.is_valid():
            cform.save()
            messages.success(request, "Perfil modificado Correctamente")
            user = request.user
            if user.groups.filter(name='cliente').exists():
                return redirect(to='ServicioWEB:hola')
            else:
                return redirect(to='ServicioWEB:ahome')
    else:
        cform = agregarcliFrom(instance=cliente)
    return render(request, 'modificarperfil.html',data)


@login_required
def modificarabogado(request, id):
    abogado= get_object_or_404(Abogado, user=id)
    data = {'aform':agregaraboFrom(instance=abogado)}
    if request.method == 'POST':
        aform = agregaraboFrom(data=request.POST, files=request.FILES, instance=abogado)
        if aform.is_valid():
            aform.save()
            messages.success(request, "Perfil modificado Correctamente")
            user = request.user
            if user.groups.filter(name='cliente').exists():
                return redirect(to='ServicioWEB:hola')
            else:
                return redirect(to='ServicioWEB:ahome')
    else:
        aform = agregaraboFrom(instance=abogado)
    return render(request, 'modificarperfila.html',data)


@login_required
def detalle_email(request,id):
    email = Email.objects.get(id = id)
    data = {'email' : email}
    return render(request, 'detalle_email.html',data)

@login_required
def detalle_solicitud(request,id):
    solicitud = Solicitud.objects.get(id = id)
    data = {'solicitud' : solicitud}
    return render(request, 'detalle_solicitud.html', data)

@login_required
def hola(request):
    return render(request, 'hola.html')

@login_required
def uploadFile(request):
    documents = Documento.objects.filter(user=request.user)
    data = {
        'documents':documents
    }
    if request.method =='POST':
        titulo = request.POST["fileTitle"]
        documento = request.FILES["uploadedFile"]
        documento = Documento(
            titulo = titulo,
            documento = documento
        )
        documento.user =request.user
        documento.save()
        user = request.user
        if user.groups.filter(name='abogado').exists():
            return redirect(to='ServicioWEB:signin')
        return render(request, "cargarDoc.html", data)
    return render(request, "cargarDoc.html",data)
    

@login_required
def eliminardoc(request,id):
    doc = get_object_or_404(Documento, id=id)
    doc.delete()
    messages.success(request, "Documento eliminado correctamente")
    return redirect(to='ServicioWEB:cargarDoc')


def documentoscli(request, username):
    current_user = request.user
    if username and username != current_user.username:
            try:
                Documento.objects.get(user=username)
                user=Documento.objects.get(user=username)
            except:
                messages.error(request, "El usuario no ha Subido archivos")
                return redirect(to='ServicioWEB:ahome')
    else:
        current_user = request.user
    return render(request, 'documentoscli.html', {'user': user})

    
def error404view(request):
    return render(request, 'error404view.html')
