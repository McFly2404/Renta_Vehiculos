"""
Interfaces de repositorio para Reservas y Vehículos (DIP — SOLID).
El dominio declara QUÉ necesita; la infraestructura decide CÓMO.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from reservas.models import Reserva, Vehiculo


class IVehiculoRepository(ABC):

    @abstractmethod
    def obtener_por_placa(self, placa: str) -> Optional["Vehiculo"]:
        ...

    @abstractmethod
    def obtener_por_id(self, vehiculo_id: int) -> Optional["Vehiculo"]:
        ...

    @abstractmethod
    def listar_disponibles(self):
        ...

    @abstractmethod
    def listar_no_disponibles(self):
        ...

    @abstractmethod
    def listar_todos(self):
        ...

    @abstractmethod
    def marcar_no_disponible(self, vehiculo: "Vehiculo") -> None:
        ...

    @abstractmethod
    def marcar_disponible(self, vehiculo: "Vehiculo") -> None:
        ...


class IReservaRepository(ABC):

    @abstractmethod
    def obtener_por_id(self, reserva_id: int) -> Optional["Reserva"]:
        ...

    @abstractmethod
    def listar_todas(self):
        ...

    @abstractmethod
    def cancelar(self, reserva: "Reserva") -> "Reserva":
        ...
