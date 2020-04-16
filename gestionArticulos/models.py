from django.db import models
from django.contrib.auth.models import User
from gestionArticulos.enums import AccionType, CategoriaType


# Create your models here.
# Los modelos serán las tablas de datos que tendrá nuestra base de datos

class Media(models.Model):
    """
        Modelo de datos para la información de los artículos multimedia de los usuarios.

        Se compone de:
        - Una id que hace de clave primaria
        - El propietario del material multimedia
        - El nombre del artículo
        - Una descripción del artículo
        - Una foto del artículo
        - La acción que se quiere realizar con el artículo (comparto, dono e intercambio)
        - La categoría a la cual pertenece el artículo
        - Los tags del artículo
        - Una clave extranjera con un User que será null inicialmente
        - La fecha de adición del artículo
    """

    media_id=models.AutoField(primary_key=True)
    propietario=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_propietario')
    nombre=models.CharField(max_length=100)
    descripcion=models.CharField(max_length=240)
    fotoart=models.ImageField(upload_to='articulos')
    accion=models.CharField(max_length=12, choices=AccionType.choices(), verbose_name='Acción')
    categoria=models.CharField(max_length=12, choices=CategoriaType.choices(), verbose_name='Categoría')
    tags=models.CharField(max_length=100)
    asignado=models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_asignado', blank=True, null=True)
    fechaAd=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de adición')

    def categoria_text(self):
        return CategoriaType[self.categoria].value
    def tags_as_list(self):
        return self.tags.split(',')

    def __str__(self):
        return "Media: %s con propietario %s, nombre %s y fecha de creación %s" % (self.media_id, self.propietario.username, self.nombre, self.propietario.date_joined)



