from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Pago(models.Model):
    ESTADO_CHOICES = [
        ("PENDIENTE", _("Pendiente")),
        ("APROBADO", _("Aprobado")),
        ("RECHAZADO", _("Rechazado")),
        ("REEMBOLSADO", _("Reembolsado")),
    ]

    METODO_CHOICES = [
        ("EFECTIVO", _("Efectivo")),
        ("TARJETA_CREDITO", _("Tarjeta de Credito")),
        ("TARJETA_DEBITO", _("Tarjeta de Debito")),
        ("TRANSFERENCIA", _("Transferencia")),
    ]

    reserva = models.OneToOneField(
        "reservas.Reserva", on_delete=models.CASCADE, related_name="pago"
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="PENDIENTE")
    metodo_pago = models.CharField(max_length=30, choices=METODO_CHOICES, default="EFECTIVO")
    fecha_pago = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago #{self.id} - {self.estado_pago}"

    def clean(self):
        if self.monto is not None and self.monto <= 0:
            raise ValidationError({"monto": _("El monto del pago debe ser mayor a 0.")})

    class Meta:
        verbose_name = _("Pago")
        verbose_name_plural = _("Pagos")
