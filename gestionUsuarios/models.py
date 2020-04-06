from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
# Los modelos serán las tablas de datos que tendrá nuestra base de datos

class UsuarioInfo(models.Model):
    """
        Modelo de datos para la información de los usuarios.

        Se compone de:
        - Un modelo User (con username, email, password, fecha de unión, etc...)
        - Un avatar para el perfil
        - Una pequeña descripción
        - La valoración de su perfil en la aplicación
        - Su fecha de nacimiento
    """

    usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    avatar=models.ImageField(upload_to='avatars')
    bio=models.CharField(max_length=150)
    valoracion=models.IntegerField(default=0)
    fechaNacimiento=models.DateField(default=timezone.now, verbose_name='Fecha de nacimiento')

    def __str__(self):
        return "Usuario: %s con email %s y fecha de creacion %s" % (self.usuario.username, self.usuario.email, self.usuario.date_joined)
    