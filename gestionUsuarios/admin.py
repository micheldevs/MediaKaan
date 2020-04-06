from django.contrib import admin

from gestionUsuarios.models import UsuarioInfo, User

# Register your models here.
# Permite gestionar los datos que podrá manipular el administrador de la aplicación.


class UsuarioInfoAdmin(admin.ModelAdmin):

    list_display = ("usuario", "fechaNacimiento")
    search_fields = ("usuario", "fechaNacimiento")
    list_filter = ("fechaNacimiento",)

admin.site.register(UsuarioInfo, UsuarioInfoAdmin)
