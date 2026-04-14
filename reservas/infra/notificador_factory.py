import os

class NotificadorConsola:
    def enviar_confirmacion(self, reserva):
        print(f"Reserva {reserva.id} confirmada correctamente")


class NotificadorEmail:
    def enviar_confirmacion(self, reserva):
        pass  # Simulación


class NotificadorFactory:

    @staticmethod
    def crear():
        entorno = os.getenv("ENV", "DEV")

        if entorno == "PROD":
            return NotificadorEmail()
        return NotificadorConsola()
