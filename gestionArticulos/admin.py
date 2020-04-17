from django.contrib import admin
from django import forms

from gestionArticulos.models import Media, Tag
from gestionUsuarios.models import User

# Register your models here.
# Permite gestionar los datos que podrá manipular el administrador de la aplicación.

class TagAdmin(admin.ModelAdmin):
    """
    Opciones de filtrado/operación para el modelo de información de los tags de los artículos multimedia.
    """

    list_display = ("name",)
    search_fields = ("name",)

class MediaAdmin(admin.ModelAdmin):
    """
    Opciones de filtrado/operación para el modelo de información de los artículos multimedia.
    """

    # Obtención del username del propietario
    def nickpropietario(self, Media):
        if Media:
            return Media.propietario.username

    # Lista en un string separado por comas en el display los tags de un Media
    def tagsnames(self, Media):
        if Media:
            return ','.join([str(tag.name) for tag in Media.tags.all()])

    # Añade un textarea al formulario del administrador para la descripción de Media
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'descripcion': forms.Textarea}
        return super().get_form(request, obj, **kwargs)

    list_display = ("nickpropietario", "nombre", "tagsnames", "accion", "categoria", "fechaAd")
    readonly_fields = ('fechaAd',)
    search_fields = ("nombre", "fechaAd")
    list_filter = ("accion", "categoria", "fechaAd")

admin.site.register(Tag, TagAdmin)
admin.site.register(Media, MediaAdmin)