from django.contrib import admin

from gestionUsuarios.models import UsuarioInfo

# Register your models here.
# Permite gestionar los modelos de datos que podrá manipular el administrador de la aplicación.

"""
class UsuarioAdmin(admin.ModelAdmin):
    list_display=("nick", "email", "fechaCreacion")
    search_fields=("nick", "email", "fechaCreacion")
    readonly_fields = ('fechaCreacion',)
    list_filter=("fechaCreacion",)
"""

admin.site.register(UsuarioInfo)