from django.contrib import admin
from usuarios.models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display  = ("id", "nombre", "cedula", "correo", "licencia")
    search_fields = ("nombre", "cedula", "correo")
