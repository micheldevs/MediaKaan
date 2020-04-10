from django.contrib import admin

from gestionArticulos.models import Media
from gestionUsuarios.models import User

# Register your models here.
# Permite gestionar los datos que podrá manipular el administrador de la aplicación.

class MediaAdmin(admin.ModelAdmin):
    """
    Opciones de filtrado/operación para el modelo de información de los artículos multimedia.
    """

    # Obtención del username del propietario
    def nickpropietario(self, Media):
        if Media:
            return Media.propietario.username

    list_display = ("nickpropietario", "nombre", "accion", "categoria", "tags", "fechaAd")
    readonly_fields = ('fechaAd',)
    search_fields = ("nickpropietario", "nombre", "tags", "fechaAd")
    list_filter = ("accion", "categoria","fechaAd")

admin.site.register(Media, MediaAdmin)