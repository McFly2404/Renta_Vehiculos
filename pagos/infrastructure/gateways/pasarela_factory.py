"""
Factory de pasarelas de pago (Factory Method — GoF).
Intercambia implementaciones según el entorno sin tocar el Service.
"""
import os
import uuid
from decimal import Decimal
from pagos.domain.interfaces import IPasarelaPago


class _PasarelaSimulada(IPasarelaPago):
    """Pasarela de desarrollo: aprueba todos los pagos automáticamente."""

    def procesar(self, monto: Decimal, metodo: str, referencia: str) -> dict:
        print(f"[DEV]  Pago simulado: ${monto} | {metodo} | ref={referencia}")
        return {
            "aprobado":           True,
            "codigo_transaccion": str(uuid.uuid4())[:8].upper(),
            "mensaje":            "Pago aprobado (simulado)",
        }


class _PasarelaProduccion(IPasarelaPago):
    """Stub de producción. Integrar con PayU / Stripe / etc."""

    def procesar(self, monto: Decimal, metodo: str, referencia: str) -> dict:
        raise NotImplementedError("Integración con pasarela real pendiente.")


class PasarelaFactory:

    @staticmethod
    def crear() -> IPasarelaPago:
        return _PasarelaProduccion() if os.getenv("ENV") == "PROD" else _PasarelaSimulada()
