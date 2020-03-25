from django.contrib import admin

from gestionUsuarios.models import Usuario

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display=("nick", "email", "fechaCreacion")
    search_fields=("nick", "email", "fechaCreacion")
    readonly_fields = ('fechaCreacion',)
    list_filter=("fechaCreacion",)


admin.site.register(Usuario, UsuarioAdmin)