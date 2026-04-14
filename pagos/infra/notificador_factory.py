import os

class NotificadorConsola:
    def enviar_confirmacion(self, pago):
        print(f"Pago {pago.id} confirmado correctamente")


class NotificadorEmail:
    def enviar_confirmacion(self, pago):
        pass  # Simulación


class NotificadorFactory:

    @staticmethod
    def crear():
        entorno = os.getenv("ENV", "DEV")

        if entorno == "PROD":
            return NotificadorEmail()
        return NotificadorConsola()
