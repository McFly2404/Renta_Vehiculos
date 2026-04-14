from django.contrib import admin
from pagos.models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display  = ("id", "reserva", "monto", "metodo_pago", "estado_pago", "fecha_pago")
    list_filter   = ("estado_pago", "metodo_pago")
