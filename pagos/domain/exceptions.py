"""Excepciones de dominio del contexto Pagos."""


class ReservaNoEncontradaError(Exception):
    """No existe una reserva con ese identificador."""


class PagoYaRegistradoError(Exception):
    """La reserva ya tiene un pago asociado."""


class ReservaCanceladaError(Exception):
    """No se puede pagar una reserva cancelada."""


class MontoInvalidoError(Exception):
    """El monto no cumple las reglas de negocio."""


class MetodoPagoInvalidoError(Exception):
    """Método de pago no reconocido."""


class PagoNoEncontradoError(Exception):
    """No existe un pago con ese identificador."""
