"""
Builder para la entidad Reserva (Builder Pattern — GoF).
Centraliza la construcción y las validaciones de dominio.
"""
from datetime import date
from reservas.models import Reserva


class ReservaBuilder:

    def __init__(self):
        self._usuario      = None
        self._vehiculo     = None
        self._fecha_inicio = None
        self._fecha_fin    = None

    def para_usuario(self, usuario):
        self._usuario = usuario
        return self

    def para_vehiculo(self, vehiculo):
        self._vehiculo = vehiculo
        return self

    def en_fechas(self, fecha_inicio, fecha_fin):
        if fecha_inicio >= fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin.")
        if fecha_inicio < date.today():
            raise ValueError("La fecha de inicio no puede ser en el pasado.")
        self._fecha_inicio = fecha_inicio
        self._fecha_fin    = fecha_fin
        return self

    def build(self) -> Reserva:
        if not all([self._usuario, self._vehiculo, self._fecha_inicio, self._fecha_fin]):
            raise ValueError("Faltan datos obligatorios para crear la reserva.")
        return Reserva.objects.create(
            usuario      = self._usuario,
            vehiculo     = self._vehiculo,
            fecha_inicio = self._fecha_inicio,
            fecha_fin    = self._fecha_fin,
            estado       = "PENDIENTE",
        )
