from django.contrib import admin
from reservas.models import Sucursal, Vehiculo, Reserva, ContratoAlquiler

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "ciudad", "telefono")

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display  = ("id", "placa", "modelo", "categoria", "tarifa_diaria", "disponible", "sucursal")
    list_filter   = ("categoria", "disponible")
    search_fields = ("placa", "modelo")

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display  = ("id", "usuario", "vehiculo", "fecha_inicio", "fecha_fin", "estado")
    list_filter   = ("estado",)

@admin.register(ContratoAlquiler)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "vehiculo", "fecha_inicio", "fecha_fin")
