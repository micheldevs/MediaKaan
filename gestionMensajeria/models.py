from djongo import models
from django.contrib.auth.models import User
from gestionArticulos.models import Media

# Create your models here.
# Los modelos serán las tablas de datos que tendrá nuestra base de datos

class Chat(models.Model):
    """
        Modelo de datos para la sesión de chat.

        Se compone de:
        - Una id que hace de clave primaria
        - El articulo del que hay un usuario interesado
        - El usuario interesado
        - La fecha de creación del artículo
    """

    chat_id=models.AutoField(primary_key=True)
    articulo=models.ForeignKey(Media, on_delete=models.CASCADE)
    interesado=models.ForeignKey(User, on_delete=models.CASCADE)
    fechaCreacion=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    msgs=models.ArrayReferenceField(to='Mensaje', on_delete=models.CASCADE, null=True, related_name='messages')

    def __str__(self):
        return "Chat: %s del artículo %s con propietario %s, interesado %s y fecha de creación %s" % (self.chat_id, self.articulo.propietario.username, self.interesado.username, self.fechaCreacion)

class Mensaje(models.Model):
    """
        Modelo de datos para un mensaje de la sesión de chat.

        Se compone de:
        - Una id que hace de clave primaria
        - El articulo del que hay un usuario interesado
        - El usuario interesado
        - La fecha de creación del artículo
    """

    msg_id=models.AutoField(primary_key=True)
    chat=models.ForeignKey(Chat, on_delete=models.CASCADE)
    contenido=models.TextField(max_length=80)
    escribe=models.ForeignKey(User, on_delete=models.CASCADE, related_name='escribe')
    recibe=models.ForeignKey(User, on_delete=models.CASCADE, related_name='recibe')
    fechaHoraMsg=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __str__(self):
        return "Chat: %s con contenido %s que escribe %s y recibe %s en la fecha %s" % (self.msg_id, self.contenido, self.escribe.username, self.recibe.username, self.fechaHoraMsg)