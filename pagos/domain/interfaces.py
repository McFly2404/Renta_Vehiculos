"""
Contrato de pasarela de pago (DIP — SOLID).
Permite intercambiar implementaciones sin tocar la lógica de negocio.
"""
from abc import ABC, abstractmethod
from decimal import Decimal


class IPasarelaPago(ABC):

    @abstractmethod
    def procesar(self, monto: Decimal, metodo: str, referencia: str) -> dict:
        """
        Retorna:
            aprobado            (bool)
            codigo_transaccion  (str)
            mensaje             (str)
        """
        ...
