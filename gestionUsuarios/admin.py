from django.contrib import admin
from django import forms

from gestionUsuarios.models import UsuarioInfo, UsuarioUbicacion, User

# Register your models here.
# Permite gestionar los datos que podrá manipular el administrador de la aplicación.


class UsuarioInfoAdmin(admin.ModelAdmin):
    """
    Opciones de filtrado/operación para el modelo de información adicional del usuario.
    """

    # Obtención del username del usuario
    def username(self, UsuarioInfo):
        if UsuarioInfo:
            return UsuarioInfo.usuario.username

    # Obtención del email del usuario
    def email(self, UsuarioInfo):
        if UsuarioInfo:
            return UsuarioInfo.usuario.email

    list_display = ("username", "email", "fechaNacimiento")
    search_fields = ("username", "email", "fechaNacimiento")
    list_filter = ("fechaNacimiento",)

class UsuarioUbicacionAdmin(admin.ModelAdmin):
    """
    Opciones de filtrado/operación para el modelo de la ubicación del usuario.
    """

    # Obtención del username del usuario
    def username(self, UsuarioUbicacion):
        if UsuarioUbicacion:
            return UsuarioUbicacion.usuario.username
    
    # Añade un textarea al formulario del administrador para la bio del usuario
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'bio': forms.Textarea}
        return super().get_form(request, obj, **kwargs)


    list_display = ("username", "latUb", "lngUb")
    search_fields = ("username", "latUb", "lngUb")

admin.site.register(UsuarioInfo, UsuarioInfoAdmin)
admin.site.register(UsuarioUbicacion, UsuarioUbicacionAdmin)
