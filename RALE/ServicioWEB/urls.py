from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ServicioWEB'

urlpatterns = [
    path('',views.signin, name='signin'),
    path('signup/',views.signup, name='signup'),
    path('signup2/',views.signup2, name='signup2'),
    path('signout/',views.signout, name='signout'),

    #!ABOGADO
    path('ahome/',views.ahome, name='ahome'),

    #!PERFIL
    path('miperfil/<str:username>/',views.miperfil, name='miperfil'),
    path('perfilcli/<str:username>/',views.perfilcli, name='perfilcli'),
    path('modificarperfilc/<id>',views.modificarcliente, name='modificarcliente'),
    path('modificarperfila/<id>',views.modificarabogado, name='modificarabogado'),

    #!DETALLE
    path('detalle/email/<id>/', views.detalle_email, name='detalle_email'),
    path('detalle/solicitud/<id>/', views.detalle_solicitud, name='detalle_solicitud'),

    #!CLIENTE
    path('hola/',views.hola, name='hola'),

    #!Documentos
    path('cargarDoc/',views.uploadFile, name='cargarDoc'),
    path('eliminardoc/<int:id>',views.eliminardoc, name='eliminardoc'),
    path('documentoscli/<str:username>',views.documentoscli, name='documentoscli'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
