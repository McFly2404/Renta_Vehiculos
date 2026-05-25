"""Implementaciones concretas de los repositorios de Reservas y Vehículos."""
from typing import Optional
from reservas.models import Reserva, Vehiculo
from reservas.domain.repositories import IReservaRepository, IVehiculoRepository


class DjangoVehiculoRepository(IVehiculoRepository):

    def obtener_por_placa(self, placa: str) -> Optional[Vehiculo]:
        return (
            Vehiculo.objects
            .select_related("sucursal")
            .filter(placa__iexact=placa.strip())
            .first()
        )

    def obtener_por_id(self, vehiculo_id: int) -> Optional[Vehiculo]:
        try:
            return Vehiculo.objects.select_related("sucursal").get(id=vehiculo_id)
        except Vehiculo.DoesNotExist:
            return None

    def listar_disponibles(self):
        return Vehiculo.objects.select_related("sucursal").filter(disponible=True)

    def listar_no_disponibles(self):
        return Vehiculo.objects.select_related("sucursal").filter(disponible=False)

    def listar_todos(self):
        return Vehiculo.objects.select_related("sucursal").all()

    def marcar_no_disponible(self, vehiculo: Vehiculo) -> None:
        vehiculo.disponible = False
        vehiculo.save(update_fields=["disponible"])

    def marcar_disponible(self, vehiculo: Vehiculo) -> None:
        vehiculo.disponible = True
        vehiculo.save(update_fields=["disponible"])


class DjangoReservaRepository(IReservaRepository):

    def obtener_por_id(self, reserva_id: int) -> Optional[Reserva]:
        try:
            return (
                Reserva.objects
                .select_related("usuario", "vehiculo", "vehiculo__sucursal")
                .get(id=reserva_id)
            )
        except Reserva.DoesNotExist:
            return None

    def listar_todas(self):
        return (
            Reserva.objects
            .select_related("usuario", "vehiculo", "vehiculo__sucursal")
            .all()
            .order_by("-fecha_creacion")
        )

    def cancelar(self, reserva: Reserva) -> Reserva:
        reserva.estado = "CANCELADA"
        reserva.save(update_fields=["estado"])
        return reserva
