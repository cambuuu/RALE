"""RALE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path,include,re_path
from rest_framework import routers
from rest_framework import permissions
from API_Opens.views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.DefaultRouter()
router.register(r'plantilla',PlantillaViewSet)
router.register(r'solicitud',SolicitudViewSet)
router.register(r'documento',DocumentoViewSet)
router.register(r'cliente',ClienteViewSet)
router.register(r'user',UserViewSet)
router.register(r'group',GroupViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="API Opens",
      default_version='v1',
      description="Documentacion API Opens",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('gestion/',include('API_Opens.urls')),
    path('',include('ServicioWEB.urls')),
    re_path(r'documentacion/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
