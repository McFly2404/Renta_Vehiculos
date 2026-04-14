"""Excepciones de dominio del contexto Reservas."""


class VehiculoNoEncontradoError(Exception):
    """Vehículo no registrado en el sistema."""


class VehiculoNoDisponibleError(Exception):
    """El vehículo existe pero no está disponible."""


class ReservaNoEncontradaError(Exception):
    """No existe una reserva con ese identificador."""


class ReservaYaCanceladaError(Exception):
    """La reserva ya fue cancelada."""


class FechasInvalidasError(Exception):
    """Las fechas no cumplen las reglas de negocio."""
