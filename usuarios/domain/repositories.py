"""
Interfaz del repositorio de Usuarios (Dependency Inversion — SOLID).
El dominio define QUÉ necesita; la infraestructura decide CÓMO.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from usuarios.models import Usuario


class IUsuarioRepository(ABC):

    @abstractmethod
    def obtener_por_id(self, usuario_id: int) -> Optional["Usuario"]:
        ...

    @abstractmethod
    def obtener_por_cedula(self, cedula: str) -> Optional["Usuario"]:
        ...

    @abstractmethod
    def obtener_por_correo(self, correo: str) -> Optional["Usuario"]:
        ...

    @abstractmethod
    def crear(self, nombre: str, cedula: str, correo: str, licencia: str) -> "Usuario":
        ...

    @abstractmethod
    def listar(self):
        ...
