"""Factory de notificadores para el contexto de Reservas."""
import os


class _NotificadorConsola:
    def enviar_confirmacion(self, reserva) -> None:
        print(
            f"[DEV]  Reserva #{reserva.id} | "
            f"{reserva.usuario.nombre} → {reserva.vehiculo.placa} | "
            f"{reserva.fecha_inicio} – {reserva.fecha_fin}"
        )


class _NotificadorEmail:
    def enviar_confirmacion(self, reserva) -> None:
        print(f"[PROD] Confirmación de reserva #{reserva.id} enviada a {reserva.usuario.correo}.")


class NotificadorReservaFactory:

    @staticmethod
    def crear():
        return _NotificadorEmail() if os.getenv("ENV") == "PROD" else _NotificadorConsola()
