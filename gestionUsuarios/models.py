from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Usuario(models.Model):
    nick=models.CharField(max_length=20)
    email=models.EmailField(max_length=35)
    password=models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex='^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                message='La contraseña debe tener mínimo 8 caracteres y al menos una letra o número.',
            ),
        ]
    )
    pathAvatar=models.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex='^(.+)\/([^/]+)$',
                message='El directorio escrito no es correcto.',
            ),
        ],
        verbose_name='Ruta de avatar'
    )
    bio=models.CharField(max_length=150)
    valoracion=models.IntegerField(default=0, blank=True)
    fechaCreacion=models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')
    fechaNacimiento=models.DateField(default=timezone.now, verbose_name='Fecha de nacimiento')

    def __str__(self):
        return "Usuario: %s con email %s y fecha de creacion %s" % (self.nick, self.email, self.fechaCreacion)