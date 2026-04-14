"""
Builder para la entidad Pago (Builder Pattern — GoF).
Centraliza la construcción y las validaciones de dominio.
"""
from decimal import Decimal
from pagos.models import Pago


class PagoBuilder:

    def __init__(self):
        self._reserva    = None
        self._monto      = None
        self._metodo_pago = "EFECTIVO"
        self._fecha_pago  = None
        self._estado_pago = "APROBADO"

    def para_reserva(self, reserva):
        self._reserva = reserva
        return self

    def con_monto(self, monto):
        valor = Decimal(str(monto))
        if valor <= 0:
            raise ValueError("El monto del pago debe ser mayor a 0.")
        self._monto = valor
        return self

    def con_metodo(self, metodo_pago: str):
        validos = [m[0] for m in Pago.METODO_CHOICES]
        if metodo_pago not in validos:
            raise ValueError(f"Método de pago inválido. Opciones: {validos}")
        self._metodo_pago = metodo_pago
        return self

    def con_estado(self, estado: str):
        validos = [e[0] for e in Pago.ESTADO_CHOICES]
        if estado not in validos:
            raise ValueError(f"Estado inválido. Opciones: {validos}")
        self._estado_pago = estado
        return self

    def en_fecha(self, fecha_pago):
        self._fecha_pago = fecha_pago
        return self

    def build(self) -> Pago:
        if self._reserva is None:
            raise ValueError("El pago debe estar asociado a una reserva.")
        if self._monto is None:
            raise ValueError("El pago debe tener un monto.")
        if self._fecha_pago is None:
            raise ValueError("El pago debe tener una fecha.")

        return Pago.objects.create(
            reserva     = self._reserva,
            monto       = self._monto,
            metodo_pago = self._metodo_pago,
            estado_pago = self._estado_pago,
            fecha_pago  = self._fecha_pago,
        )
