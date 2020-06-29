from django.conf.urls import url
from . import views

app_name = 'gestionMensajeria'

urlpatterns = [
    url(r'^mensajes/$', views.message, name='msg'),
]