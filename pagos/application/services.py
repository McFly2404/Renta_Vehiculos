"""
Capa de Aplicación — Pagos.
SRP: una clase por caso de uso. DIP: dependencias inyectadas por constructor.
"""
from pagos.domain.repositories import IPagoRepository
from pagos.domain.interfaces import IPasarelaPago
from pagos.domain.pago_builder import PagoBuilder
from pagos.domain.exceptions import (
    ReservaNoEncontradaError,
    PagoYaRegistradoError,
    ReservaCanceladaError,
    PagoNoEncontradoError,
)
from reservas.domain.repositories import IReservaRepository


class CrearPagoService:
    """
    Orquesta el registro de un pago.
    Usa la pasarela de pago (Factory) para procesar el cobro.
    """

    def __init__(
        self,
        reserva_repo: IReservaRepository,
        pago_repo:    IPagoRepository,
        notificador,
        pasarela:     IPasarelaPago,
    ):
        self._reserva_repo = reserva_repo
        self._pago_repo    = pago_repo
        self._notificador  = notificador
        self._pasarela     = pasarela

    def ejecutar(self, reserva_id: int, monto, metodo_pago: str, fecha_pago):
        reserva = self._reserva_repo.obtener_por_id(reserva_id)
        if not reserva:
            raise ReservaNoEncontradaError(f"Reserva #{reserva_id} no encontrada.")
        if hasattr(reserva, "pago"):
            raise PagoYaRegistradoError("Esta reserva ya tiene un pago registrado.")
        if reserva.estado == "CANCELADA":
            raise ReservaCanceladaError("No se puede pagar una reserva cancelada.")

        resultado = self._pasarela.procesar(
            monto      = monto,
            metodo     = metodo_pago,
            referencia = f"RESERVA-{reserva_id}",
        )
        estado = "APROBADO" if resultado["aprobado"] else "RECHAZADO"

        pago = (
            PagoBuilder()
            .para_reserva(reserva)
            .con_monto(monto)
            .con_metodo(metodo_pago)
            .con_estado(estado)
            .en_fecha(fecha_pago)
            .build()
        )

        if resultado["aprobado"]:
            reserva.estado = "CONFIRMADA"
            reserva.save(update_fields=["estado"])
            self._notificador.enviar_confirmacion(pago)

        return pago


class ObtenerPagoService:
    """Recupera un pago por su ID."""

    def __init__(self, pago_repo: IPagoRepository):
        self._pago_repo = pago_repo

    def ejecutar(self, pago_id: int):
        pago = self._pago_repo.obtener_por_id(pago_id)
        if not pago:
            raise PagoNoEncontradoError(f"Pago #{pago_id} no encontrado.")
        return pago
