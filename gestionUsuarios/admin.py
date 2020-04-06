from django.contrib import admin

from gestionUsuarios.models import UsuarioInfo, User

# Register your models here.
# Permite gestionar los datos que podrá manipular el administrador de la aplicación.


class UsuarioInfoAdmin(admin.ModelAdmin):

    def username(self, UsuarioInfo):
        if UsuarioInfo:
            return UsuarioInfo.usuario.username

    def email(self, UsuarioInfo):
        if UsuarioInfo:
            return UsuarioInfo.usuario.email

    list_display = ("username", "email", "fechaNacimiento")
    search_fields = ("username", "email", "fechaNacimiento")
    list_filter = ("fechaNacimiento",)

admin.site.register(UsuarioInfo, UsuarioInfoAdmin)
