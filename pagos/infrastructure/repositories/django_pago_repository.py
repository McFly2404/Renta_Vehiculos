"""Implementación concreta del repositorio de Pagos."""
from typing import Optional
from pagos.models import Pago
from pagos.domain.repositories import IPagoRepository


class DjangoPagoRepository(IPagoRepository):

    def obtener_por_id(self, pago_id: int) -> Optional[Pago]:
        try:
            return Pago.objects.select_related("reserva").get(id=pago_id)
        except Pago.DoesNotExist:
            return None

    def listar_por_reserva(self, reserva_id: int):
        return Pago.objects.filter(reserva_id=reserva_id)
