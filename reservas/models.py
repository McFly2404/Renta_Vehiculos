from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"

    class Meta:
        verbose_name = _("Sucursal")
        verbose_name_plural = _("Sucursales")


class Vehiculo(models.Model):
    CATEGORIA_CHOICES = [
        ("SEDAN", _("Sedan")),
        ("SUV", "SUV"),
        ("CAMIONETA", _("Camioneta")),
        ("DEPORTIVO", _("Deportivo")),
        ("FURGON", _("Furgon")),
    ]

    placa = models.CharField(max_length=20, unique=True)
    modelo = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    capacidad = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    tarifa_diaria = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    sucursal = models.ForeignKey(
        Sucursal, on_delete=models.CASCADE, related_name="vehiculos"
    )

    def __str__(self):
        return f"{self.placa} - {self.modelo}"

    def clean(self):
        if self.tarifa_diaria is not None and self.tarifa_diaria <= 0:
            raise ValidationError({"tarifa_diaria": _("La tarifa diaria debe ser mayor a 0.")})
        if self.capacidad is not None and self.capacidad < 1:
            raise ValidationError({"capacidad": _("La capacidad minima es 1.")})

    class Meta:
        verbose_name = _("Vehiculo")
        verbose_name_plural = _("Vehiculos")


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ("PENDIENTE", _("Pendiente")),
        ("CONFIRMADA", _("Confirmada")),
        ("CANCELADA", _("Cancelada")),
        ("COMPLETADA", _("Completada")),
    ]

    usuario = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.CASCADE, related_name="reservas"
    )
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, related_name="reservas"
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="PENDIENTE")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva #{self.id} - {self.usuario.nombre} - {self.vehiculo.placa}"

    def clean(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio >= self.fecha_fin:
                raise ValidationError(
                    {"fecha_fin": _("La fecha de fin debe ser posterior a la de inicio.")}
                )
            if self.fecha_inicio < date.today():
                raise ValidationError(
                    {"fecha_inicio": _("La fecha de inicio no puede ser en el pasado.")}
                )

    class Meta:
        verbose_name = _("Reserva")
        verbose_name_plural = _("Reservas")


class ContratoAlquiler(models.Model):
    usuario = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.CASCADE, related_name="contratos"
    )
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, related_name="contratos"
    )
    pago = models.OneToOneField(
        "pagos.Pago", on_delete=models.CASCADE, related_name="contrato"
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contrato #{self.id} - {self.usuario.nombre}"

    class Meta:
        verbose_name = _("Contrato de Alquiler")
        verbose_name_plural = _("Contratos de Alquiler")
