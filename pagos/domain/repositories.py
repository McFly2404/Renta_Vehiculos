"""Interfaces de repositorio para Pagos (DIP — SOLID)."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from pagos.models import Pago


class IPagoRepository(ABC):

    @abstractmethod
    def obtener_por_id(self, pago_id: int) -> Optional["Pago"]:
        ...

    @abstractmethod
    def listar_por_reserva(self, reserva_id: int):
        ...
