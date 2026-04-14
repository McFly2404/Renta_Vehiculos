"""Factory de notificadores para el contexto de Pagos."""
import os


class _NotificadorConsola:
    def enviar_confirmacion(self, pago) -> None:
        print(f"[DEV]  Pago #{pago.id} | ${pago.monto} | {pago.estado_pago}")


class _NotificadorEmail:
    def enviar_confirmacion(self, pago) -> None:
        print(f"[PROD] Recibo de pago #{pago.id} enviado por email.")


class NotificadorPagoFactory:

    @staticmethod
    def crear():
        return _NotificadorEmail() if os.getenv("ENV") == "PROD" else _NotificadorConsola()
