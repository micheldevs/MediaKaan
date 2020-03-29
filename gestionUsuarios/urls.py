from django.conf.urls import url
from . import views

app_name = 'gestionUsuarios'

urlpatterns = [
    url(r'^registro/$', views.register, name='register'),
    url(r'^iniciosesion/$', views.user_login, name='user_login'),
]