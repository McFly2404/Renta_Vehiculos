from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Sucursal(models.Model):
    nombre    = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono  = models.CharField(max_length=20)
    ciudad    = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"

    class Meta:
        verbose_name        = "Sucursal"
        verbose_name_plural = "Sucursales"


class Vehiculo(models.Model):
    CATEGORIA_CHOICES = [
        ("SEDAN",     "Sedán"),
        ("SUV",       "SUV"),
        ("CAMIONETA", "Camioneta"),
        ("DEPORTIVO", "Deportivo"),
        ("FURGON",    "Furgón"),
    ]

    placa         = models.CharField(max_length=20, unique=True)
    modelo        = models.CharField(max_length=50)
    categoria     = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    capacidad     = models.PositiveIntegerField()
    color         = models.CharField(max_length=30)
    tarifa_diaria = models.DecimalField(max_digits=10, decimal_places=2)
    disponible    = models.BooleanField(default=True)
    sucursal      = models.ForeignKey(
        Sucursal, on_delete=models.CASCADE, related_name="vehiculos"
    )

    def __str__(self):
        return f"{self.placa} - {self.modelo}"

    def clean(self):
        if self.tarifa_diaria is not None and self.tarifa_diaria <= 0:
            raise ValidationError({"tarifa_diaria": "La tarifa diaria debe ser mayor a 0."})
        if self.capacidad is not None and self.capacidad < 1:
            raise ValidationError({"capacidad": "La capacidad mínima es 1."})

    class Meta:
        verbose_name        = "Vehículo"
        verbose_name_plural = "Vehículos"


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ("PENDIENTE",  "Pendiente"),
        ("CONFIRMADA", "Confirmada"),
        ("CANCELADA",  "Cancelada"),
        ("COMPLETADA", "Completada"),
    ]

    # FK usa string label para evitar import circular entre apps
    usuario       = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.CASCADE, related_name="reservas"
    )
    vehiculo      = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, related_name="reservas"
    )
    fecha_inicio   = models.DateField()
    fecha_fin      = models.DateField()
    estado         = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="PENDIENTE")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva #{self.id} - {self.usuario.nombre} - {self.vehiculo.placa}"

    def clean(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio >= self.fecha_fin:
                raise ValidationError(
                    {"fecha_fin": "La fecha de fin debe ser posterior a la de inicio."}
                )
            if self.fecha_inicio < date.today():
                raise ValidationError(
                    {"fecha_inicio": "La fecha de inicio no puede ser en el pasado."}
                )

    class Meta:
        verbose_name        = "Reserva"
        verbose_name_plural = "Reservas"


class ContratoAlquiler(models.Model):
    usuario       = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.CASCADE, related_name="contratos"
    )
    vehiculo      = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, related_name="contratos"
    )
    pago          = models.OneToOneField(
        "pagos.Pago", on_delete=models.CASCADE, related_name="contrato"
    )
    fecha_inicio   = models.DateField()
    fecha_fin      = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contrato #{self.id} - {self.usuario.nombre}"

    class Meta:
        verbose_name        = "Contrato de Alquiler"
        verbose_name_plural = "Contratos de Alquiler"
